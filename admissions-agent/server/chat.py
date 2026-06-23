"""Conversational intake — a natural-language chat that builds the client profile and hands off
to the research pipeline, all in one thread.

Each HTTP turn is one ``handle_turn`` call: the client sends the visible transcript + the
accumulating partial profile; we run a short internal tool loop on the Anthropic Messages API
(cheap model, see config.CHAT_MODEL), and return the assistant's next message + the updated profile.
The model fills fields via the ``update_profile`` tool, can pull a real KB teaser via
``preview_from_kb``, and calls ``start_research`` once the search-critical fields are present — at
which point we validate, create the client, and kick off Phase B (skipping Phase A entirely).

State is carried by the client between turns (stateless server): the visible transcript gives
conversational continuity; the partial profile carries extracted facts. Tool_use/tool_result blocks
live only inside a single turn's internal loop.
"""

from __future__ import annotations

import copy
import json
import logging
import os

from lib import profile_io

from . import config, jobs, kb_preview, state
from .client_store import create_client

log = logging.getLogger("admissions.chat")

# Fields the chat must collect before research can start (the schema itself is lenient — this is the
# business rule). research_interests is additionally required for research degrees.
SYSTEM_PROMPT = """\
You are a warm, encouraging study-abroad admissions advisor having a short chat with a prospective
applicant. Your job in this conversation is to learn enough about them to build their personalised
university + scholarship plan, then start the research.

Style: friendly and plain-language. Ask ONE question at a time. Keep messages short. Never sound like
a form. React briefly to what they say before the next question. Do NOT ask for phone number or email.

Collect these (one at a time, in a natural order):
- Full name
- Nationality / citizenship
- Country they currently live in
- Which country they want to study in — UK, US, or both
- Degree level — undergraduate, taught master's (postgraduate_taught), or research/PhD (postgraduate_research)
- Field / subject of study
- Their most recent grade and the grading system it's on (e.g. "UK 2:1", "Nigerian 4.2/5.0 CGPA", "GPA 3.6/4.0")
- Whether they need full funding / a scholarship
- For research degrees (PhD/research master's) ONLY: their research interests

As you learn each fact, call the `update_profile` tool to record it. Map degree level to exactly one
of: undergraduate | postgraduate_taught | postgraduate_research.

As soon as you know their target country, field, degree level, AND nationality, call `preview_from_kb`
once and share the result with them as a quick head-start ("To give you a head start, here are some
that already look relevant…"). Present ONLY what the tool returns — never invent schools or awards.
Then continue collecting anything still missing.

When you have ALL the required fields, tell them you're starting their research now, and call
`start_research`. After that the conversation continues automatically — you don't need to say more.

If `start_research` reports missing fields, ask for those and try again. Be efficient — don't
re-ask things you already know (the current profile is shown to you).
"""

TOOLS = [
    {
        "name": "update_profile",
        "description": (
            "Record facts you've learned about the applicant. Pass only the fields you just learned, "
            "nested under identity/targets/academics/tests/funding/profile. Examples: "
            '{"identity": {"full_name": "Ama Mensah", "nationality": ["Ghana"], "country_of_residence": "Ghana"}}, '
            '{"targets": {"countries": ["UK"], "degree_level": "postgraduate_taught", "fields_of_study": ["Public Health"], "full_funding_required": true}}, '
            '{"academics": {"qualifications": [{"name": "BSc Public Health", "grading_system": "Ghanaian First Class", "raw_grade": "First Class"}]}}, '
            '{"targets": {"research_interests": ["maternal health"]}}'
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "identity": {"type": "object"},
                "targets": {"type": "object"},
                "academics": {"type": "object"},
                "tests": {"type": "object"},
                "funding": {"type": "object"},
                "profile": {"type": "object"},
            },
        },
    },
    {
        "name": "preview_from_kb",
        "description": (
            "Fetch a few REAL candidate universities and scholarships from our knowledge base to share "
            "as a quick preview. Call once you know target country + field + degree level + nationality."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "start_research",
        "description": (
            "Start the full research pipeline. Call ONLY when you have the full name, nationality, "
            "country of residence, target country/countries, degree level, field of study, an academic "
            "grade, and funding need — plus research interests for a research degree."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
]


def _deep_merge(base: dict, patch: dict) -> dict:
    """Recursively merge patch into base (lists and scalars replace; dicts merge)."""
    for k, v in (patch or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def _missing_required(profile: dict) -> list[str]:
    identity = profile.get("identity") or {}
    targets = profile.get("targets") or {}
    academics = profile.get("academics") or {}
    missing: list[str] = []
    if not (identity.get("full_name") or "").strip():
        missing.append("full name")
    if not (identity.get("nationality") or []):
        missing.append("nationality")
    if not (identity.get("country_of_residence") or "").strip():
        missing.append("country of residence")
    if not (targets.get("countries") or []):
        missing.append("target country (UK/US)")
    if not (targets.get("degree_level") or "").strip():
        missing.append("degree level")
    if not (targets.get("fields_of_study") or []):
        missing.append("field of study")
    if not (academics.get("qualifications") or []):
        missing.append("most recent grade")
    if (targets.get("degree_level") or "") == "postgraduate_research" and not (targets.get("research_interests") or []):
        missing.append("research interests")
    return missing


_QUAL_KEY_MAP = {
    "name": "name", "degree": "name", "title": "name", "qualification": "name",
    "grading_system": "grading_system", "system": "grading_system", "scale": "grading_system",
    "raw_grade": "raw_grade", "result": "raw_grade", "grade": "raw_grade", "raw": "raw_grade", "score": "raw_grade",
    "institution": "institution", "school": "institution", "university": "institution",
    "institution_country": "institution_country", "country": "institution_country",
    "graduation_date": "graduation_date", "graduated": "graduation_date", "date": "graduation_date", "year": "graduation_date",
}


def _normalize_quals(profile: dict) -> None:
    """Map free-form qualification keys the model may emit onto the schema's exact keys."""
    quals = ((profile.get("academics") or {}).get("qualifications"))
    if not isinstance(quals, list):
        return
    out = []
    for q in quals:
        if not isinstance(q, dict):
            continue
        nq: dict = {}
        for k, v in q.items():
            tgt = _QUAL_KEY_MAP.get(str(k).lower())
            if tgt:
                nq[tgt] = v
        src = str(q.get("source", "")).lower()
        nq["source"] = src if src in ("parsed", "self_reported", "confirmed", "") else "self_reported"
        if not nq.get("source"):
            nq["source"] = "self_reported"
        out.append(nq)
    profile["academics"]["qualifications"] = out


def _prune_to_schema(instance, schema):
    """Drop any properties not allowed by the schema so a model-shaped profile always validates."""
    t = schema.get("type")
    if t == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        addl = schema.get("additionalProperties", True)
        out = {}
        for k, v in instance.items():
            if k in props:
                out[k] = _prune_to_schema(v, props[k])
            elif addl is True:
                out[k] = v
        return out
    if t == "array" and isinstance(instance, list) and isinstance(schema.get("items"), dict):
        return [_prune_to_schema(x, schema["items"]) for x in instance]
    return instance


def _start_research(profile: dict) -> str:
    """Assemble a valid profile from the template base, create the client, kick off Phase B. Returns slug."""
    base = profile_io.load_profile(config.TEMPLATE_DIR / "client_profile.json")
    _deep_merge(base, copy.deepcopy(profile))
    _normalize_quals(base)
    base.setdefault("pipeline_state", {})["intake"] = "done"  # the chat did intake; skip Phase A
    base = _prune_to_schema(base, profile_io.load_schema())  # strip any stray model-supplied keys
    slug = create_client(base)  # validates against the schema, raises on failure
    state.write_status(slug, state.RUNNING_RESEARCH,
                       message="Researching universities, scholarships, and a plan for you…")
    jobs.start_research(slug)
    return slug


def handle_turn(messages: list[dict], profile: dict) -> dict:
    """Run one assistant turn (with an internal tool loop). Returns {reply, profile, done, slug}."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {"error": "chat_unavailable",
                "reply": "The chat isn't configured right now (missing API key). Please try the form.",
                "profile": profile, "done": False}

    try:
        import anthropic  # imported lazily so the rest of the server runs without the package locally
    except ImportError:
        return {"error": "chat_unavailable",
                "reply": "The chat isn't available right now. Please use the form instead.",
                "profile": profile, "done": False}

    client = anthropic.Anthropic()
    profile = copy.deepcopy(profile or {})
    # Reconstruct the Anthropic message list from the visible transcript (text only).
    convo: list[dict] = [{"role": m["role"], "content": m["content"]}
                         for m in (messages or []) if m.get("content")]
    if not convo:
        convo = [{"role": "user", "content": "(start)"}]

    system = SYSTEM_PROMPT + "\n\nCurrent profile so far:\n" + json.dumps(profile, ensure_ascii=False) \
        + "\n\nStill missing: " + (", ".join(_missing_required(profile)) or "nothing — you may start research")

    done = False
    slug = None
    reply = ""
    for _ in range(6):  # internal tool loop within this one HTTP turn
        resp = client.messages.create(
            model=config.CHAT_MODEL,
            max_tokens=1024,
            system=system,
            tools=TOOLS,
            messages=convo,
        )
        if resp.stop_reason != "tool_use":
            reply = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
            break

        convo.append({"role": "assistant", "content": [b.model_dump() for b in resp.content]})
        tool_results = []
        for block in resp.content:
            if getattr(block, "type", "") != "tool_use":
                continue
            if block.name == "update_profile":
                _deep_merge(profile, dict(block.input or {}))
                result = "recorded"
            elif block.name == "preview_from_kb":
                result = kb_preview.build_preview(profile) or "No catalog matches yet — keep asking."
            elif block.name == "start_research":
                missing = _missing_required(profile)
                if missing:
                    result = "Cannot start yet — still missing: " + ", ".join(missing) + ". Ask for these."
                else:
                    try:
                        slug = _start_research(profile)
                        done = True
                        result = "Research started."
                    except Exception as exc:  # noqa: BLE001
                        log.exception("chat handoff failed")
                        result = f"Could not start research: {exc}"
            else:
                result = "unknown tool"
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
        convo.append({"role": "user", "content": tool_results})
        # refresh the missing-fields hint after tool effects
        system = SYSTEM_PROMPT + "\n\nCurrent profile so far:\n" + json.dumps(profile, ensure_ascii=False) \
            + "\n\nStill missing: " + (", ".join(_missing_required(profile)) or "nothing — you may start research")
        if done:
            # let the model say its closing line, then stop
            final = client.messages.create(model=config.CHAT_MODEL, max_tokens=512,
                                            system=system, tools=TOOLS, messages=convo)
            reply = "".join(b.text for b in final.content if getattr(b, "type", "") == "text").strip()
            break

    if not reply:
        reply = "Thanks — let's keep going." if not done else "Great — starting your research now."
    return {"reply": reply, "profile": profile, "done": done, "slug": slug}
