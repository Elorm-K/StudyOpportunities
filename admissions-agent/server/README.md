# Admissions agent — hosted web runtime

A thin FastAPI service that drives the existing Claude Code agent (`CLAUDE.md` + `.claude/skills/`)
headlessly via the **Claude Agent SDK**, so an applicant can use it end-to-end in a browser:

```
intake form  →  Phase A (validate + clarify)  →  [easy questions, only if unclear]  →
answers  →  Phase B (research → draft report)  →  [operator approves]  →  report
```

Control flow is decided by **file existence**, never by parsing model output: Phase A writes
`clients/<slug>/questions.json` and stops if it needs clarification; the runtime renders a second
form from it, merges the answers back into `client_profile.json`, then runs Phase B.

## Layout

| File | Role |
|---|---|
| `app.py` | FastAPI endpoints + serves the three pages |
| `runner.py` | the two SDK invocations (Phase A / Phase B) + their prompts |
| `jobs.py` | asyncio task launch, status transitions, boot resume-sweep, report promotion |
| `state.py` | `status.json` / `questions.json` IO (atomic) + state constants |
| `client_store.py` | create client from `clients/_template`, slugify, per-client lock |
| `answers.py` | merge second-form answers via each question's `target_path`/`merge` rule |
| `config.py` | env config + path helpers (loads `.env` locally) |
| `static/questions.html`, `static/results.html` | second form + polling results page (self-contained) |
| `Dockerfile`, `entrypoint.sh` | Railway image + volume wiring |

All profile reads/writes go through the existing `lib/profile_io.py` (schema-validated).

## Run locally

```bash
cd admissions-agent
pip install -r requirements.txt          # also need the `claude` CLI on PATH (npm i -g @anthropic-ai/claude-code)
cp .env.example .env                      # leave ANTHROPIC_API_KEY unset to use your logged-in `claude` CLI
uvicorn server.app:app --reload --port 8000
# open http://localhost:8000
```

`claude` CLI auth: locally, if `ANTHROPIC_API_KEY` is unset the SDK uses your logged-in CLI (OAuth).
On Railway, set a real `ANTHROPIC_API_KEY`.

## Endpoints

- `GET /` — intake form · `POST /api/intake` — submit profile → `{slug, results_url}`
- `GET /api/clients/{slug}/status` — poll · `GET/POST /api/clients/{slug}/questions|answers`
- `GET /clients/{slug}/results` · `GET /api/clients/{slug}/report`
- `POST /api/operator/clients/{slug}/approve` (header `X-Operator-Token`) · `GET /api/operator/queue`
- `GET /healthz`

## Deploy to Railway

1. Service **Root Directory** = `admissions-agent`; **Dockerfile path** = `server/Dockerfile`.
2. Attach a **Volume** mounted at `/data` (persists `clients/` and `kb/`).
3. Variables: `ANTHROPIC_API_KEY` (required), `OPERATOR_TOKEN` (required for approval),
   optional `APPROVAL_REQUIRED`, `CLAUDE_MODEL`, `MAX_BUDGET_USD_INTAKE`, `MAX_BUDGET_USD_RESEARCH`.

## Cost & safety notes

- Each full run is many model turns + web searches per target country — real money. `MAX_BUDGET_USD_*`
  caps each phase; `CLAUDE_MODEL` (e.g. `claude-sonnet-4-6`) trades quality for cost.
- The agent runs with `permission_mode=bypassPermissions` (can run Bash) — the container is the only
  sandbox. Keep the image minimal and the volume scoped.
- `APPROVAL_REQUIRED=true` honors guardrail #7: `report.md` is created only when the operator approves.
