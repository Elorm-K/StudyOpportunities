"""FastAPI HTTP layer: serve the forms, accept intake, drive the two-phase flow, release
the report behind the operator approval gate. Thin — all logic lives in jobs/runner/state.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from starlette.concurrency import run_in_threadpool

import jsonschema

from lib import report_docx

from . import chat, config, jobs, state
from .answers import apply_answers
from .client_store import create_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("admissions.app")

app = FastAPI(title="Admissions Agent")


@app.on_event("startup")
async def _startup() -> None:
    jobs.resume_sweep()


@app.get("/healthz")
async def healthz():
    return {"ok": True, "approval_required": config.APPROVAL_REQUIRED, "model": config.CLAUDE_MODEL}


# --- applicant-facing pages ---

@app.get("/")
async def chat_page():
    return FileResponse(config.STATIC_DIR / "chat.html", media_type="text/html")


@app.get("/form")
async def intake_form():
    """Structured-form intake — kept as a fallback (e.g. if the chat/API key is unavailable)."""
    if not config.INTAKE_FORM.exists():
        raise HTTPException(500, "intake form not found")
    return FileResponse(config.INTAKE_FORM, media_type="text/html")


@app.get("/clients/{slug}/questions")
async def questions_page(slug: str):
    return FileResponse(config.STATIC_DIR / "questions.html", media_type="text/html")


@app.get("/clients/{slug}/results")
async def results_page(slug: str):
    return FileResponse(config.STATIC_DIR / "results.html", media_type="text/html")


# --- applicant-facing API ---

@app.post("/api/intake")
async def submit_intake(request: Request):
    try:
        profile = await request.json()
    except Exception:
        raise HTTPException(400, "invalid JSON body")
    if not isinstance(profile, dict):
        raise HTTPException(400, "expected a client profile object")
    try:
        slug = create_client(profile)
    except jsonschema.ValidationError as exc:
        raise HTTPException(422, f"profile failed validation: {exc.message}")
    state.write_status(slug, state.QUEUED, message="Received — starting review.")
    jobs.start_intake(slug)
    return {"slug": slug, "results_url": f"/clients/{slug}/results", "status_url": f"/api/clients/{slug}/status"}


@app.post("/api/chat")
async def chat_turn(request: Request):
    """One conversational-intake turn. Body: {messages: [{role,content}], profile: {}}."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "invalid JSON body")
    messages = body.get("messages") if isinstance(body, dict) else None
    profile = body.get("profile") if isinstance(body, dict) else None
    if not isinstance(messages, list) or not isinstance(profile, dict):
        raise HTTPException(400, "expected {messages: [...], profile: {...}}")
    return await run_in_threadpool(chat.handle_turn, messages, profile)


@app.get("/api/clients/{slug}/status")
async def get_status(slug: str):
    st = state.read_status(slug)
    if st is None:
        raise HTTPException(404, "unknown client")
    return st


@app.get("/api/clients/{slug}/questions")
async def get_questions(slug: str):
    st = state.read_status(slug)
    if st is None:
        raise HTTPException(404, "unknown client")
    if st.get("state") != state.AWAITING_ANSWERS:
        raise HTTPException(409, "no questions are pending for this client")
    q = state.read_questions(slug)
    if not state.questions_valid(q):
        raise HTTPException(409, "no questions are pending for this client")
    return q


@app.post("/api/clients/{slug}/answers")
async def submit_answers(slug: str, request: Request):
    st = state.read_status(slug)
    if st is None:
        raise HTTPException(404, "unknown client")
    if st.get("state") != state.AWAITING_ANSWERS:
        raise HTTPException(409, "this client is not awaiting answers")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "invalid JSON body")
    answers = body.get("answers") if isinstance(body, dict) else None
    if not isinstance(answers, dict):
        raise HTTPException(400, "expected {\"answers\": {id: value}}")
    try:
        apply_answers(slug, answers)
    except jsonschema.ValidationError as exc:
        raise HTTPException(422, f"answers produced an invalid profile: {exc.message}")
    except (KeyError, ValueError) as exc:
        raise HTTPException(422, f"could not apply answers: {exc}")
    state.write_status(slug, state.RUNNING_RESEARCH, message="Thanks — starting your research…")
    jobs.start_research(slug)
    return {"ok": True, "results_url": f"/clients/{slug}/results"}


@app.get("/api/clients/{slug}/report")
async def get_report(slug: str):
    st = state.read_status(slug)
    if st is None:
        raise HTTPException(404, "unknown client")
    s = st.get("state")
    if s == state.AWAITING_APPROVAL:
        raise HTTPException(409, "report is under review")
    final = config.final_report_path(slug)
    if not final.exists():
        raise HTTPException(404, "report not ready")
    return JSONResponse({"markdown": final.read_text(encoding="utf-8")})


@app.get("/api/clients/{slug}/report.docx")
async def get_report_docx(slug: str):
    """Download the finalized report as a Word document — the client-facing deliverable.

    Rendered from report.md on demand and cached; re-rendered if the Markdown is newer.
    """
    st = state.read_status(slug)
    if st is None:
        raise HTTPException(404, "unknown client")
    if st.get("state") == state.AWAITING_APPROVAL:
        raise HTTPException(409, "report is under review")
    final = config.final_report_path(slug)
    if not final.exists():
        raise HTTPException(404, "report not ready")
    docx = config.docx_report_path(slug)
    if not docx.exists() or docx.stat().st_mtime < final.stat().st_mtime:
        try:
            report_docx.markdown_to_docx(final.read_text(encoding="utf-8"), docx)
        except RuntimeError as exc:
            raise HTTPException(503, str(exc))
    return FileResponse(
        docx,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{slug}-study-plan.docx",
    )


# --- operator-facing API (token-gated) ---

def _require_operator(token: str | None) -> None:
    if not config.OPERATOR_TOKEN:
        raise HTTPException(503, "operator endpoints are not configured (set OPERATOR_TOKEN)")
    if token != config.OPERATOR_TOKEN:
        raise HTTPException(401, "invalid operator token")


@app.get("/api/operator/queue")
async def operator_queue(x_operator_token: str | None = Header(default=None)):
    _require_operator(x_operator_token)
    pending = []
    if config.CLIENTS_DIR.exists():
        for child in config.CLIENTS_DIR.iterdir():
            if not child.is_dir() or child.name == "_template":
                continue
            st = state.read_status(child.name)
            if st and st.get("state") == state.AWAITING_APPROVAL:
                pending.append(st)
    return {"awaiting_approval": pending}


@app.get("/api/operator/clients/{slug}/draft")
async def operator_draft(slug: str, x_operator_token: str | None = Header(default=None)):
    _require_operator(x_operator_token)
    draft = config.draft_report_path(slug)
    if not draft.exists():
        raise HTTPException(404, "no draft for this client")
    return PlainTextResponse(draft.read_text(encoding="utf-8"))


@app.post("/api/operator/clients/{slug}/approve")
async def operator_approve(slug: str, x_operator_token: str | None = Header(default=None)):
    _require_operator(x_operator_token)
    try:
        jobs.promote_report(slug)
    except FileNotFoundError as exc:
        raise HTTPException(404, str(exc))
    return {"ok": True, "state": state.DONE}
