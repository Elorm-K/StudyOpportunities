# Conversational (chat) intake → research → report, in one thread

**Date:** 2026-06-23
**Status:** approved (build)

## Context

Today the hosted flow is: HTML intake form → Phase A (LLM validates intake, may emit a
clarifying-questions form) → second answers form → Phase B (the KB-first research pipeline) →
report. The user wants to **scrap the HTML form** and make intake a **natural-language chat** that
collects the profile conversationally, narrows the search as it goes, and flows straight into the
research — all in one continuous thread.

Decisions (confirmed with the user):
- **LLM-powered natural chat** (free-form understanding), accepting per-user token cost.
- Use a **cheap/fast model for the chat** (`claude-haiku-4-5`); keep **Opus** for the research run.
- **One continuous thread**: chat collects everything, then the same page shows the live research
  progress (the chat-style wait we built) and the report in-thread. This **collapses Phase A** — the
  chat does the clarifying; research starts as soon as the required fields are satisfied.

Honest expectation set with the user: chat speeds *intake* and sharpens *targeting* (better-scoped
profile → more KB-first hits, fewer slow live fallbacks), but the multi-minute research run itself is
unchanged — not instant.

## Architecture

### Enhancement (chosen): Instant KB teaser
The headline "faster answer" feature. As soon as the chat knows **target country + field of study +
degree level + nationality**, the chat surfaces a few **real** candidate schools and the flagship
scholarships the applicant is eligible for — pulled directly from the KB catalogs — *before* the
full research finishes. This is deterministic and cheap (reads `kb/universities/<country>.md` filtered
by field cluster + degree level, and `kb/scholarships/*` hard-gated on nationality); it does **no**
web research and does not invent schools.

- Exposed to the chat model as a tool **`preview_from_kb()`** (the model calls it once the four
  fields are known); the backend returns a small structured list of real catalog rows + eligible
  flagship awards, and the model presents them verbatim ("While I build your full plan, based on what
  you've told me these look relevant: …"). The model is instructed to present ONLY what the tool
  returns — no fabricated schools.
- Needs a small **field-of-study → cluster** mapper (cs-data / engineering / business / public-health
  / law / social-dev / sciences — the catalog's own taxonomy) so the catalog can be filtered.
- The teaser is a *preview*, clearly labelled as such; the cited, funding-scored shortlist still comes
  from the full Phase B run that follows.

### Components
1. **`server/static/chat.html`** (new landing page; replaces the form as the default entry).
   Reuses the existing chat-bubble UI. Holds the transcript client-side, POSTs each user turn,
   renders assistant replies, then — after handoff — polls status and renders progress + report
   **in the same thread** (the wait logic from `results.html` is merged in here).
2. **`server/chat.py`** (new). Endpoint `POST /api/chat`: takes the running transcript + current
   partial profile, calls the **Anthropic Messages API** (`claude-haiku-4-5`) with two tools:
   - `update_profile(patch)` — the model fills/edits `client_profile.json` fields as it learns them.
   - `start_research()` — the model calls this once the **schema-required** fields are satisfied.
   Returns: assistant text (next question / acknowledgement), the updated partial profile, and a
   `ready` flag. Stateless per turn — the client sends transcript + partial profile each call.
3. **System prompt** generated from the existing question bank
   (`.claude/skills/client-intake/references/intake-questions.md`) + the schema's required fields,
   encoding the branching rules (UK vs US; degree level; research-only fields like research
   interests). Instructs the model to ask one thing at a time, confirm ambiguous answers, and only
   call `start_research` when required fields are present.
4. **Handoff** (server, on `start_research`): assemble the final profile, **validate against
   `schema/client_profile.schema.json`**, write it via `client_store.create_client`, then call the
   existing `jobs.start_research(slug)`. Transcript-evaluation (grade mapping) runs at the front of
   Phase B as today. Everything downstream (KB-first matching, Word `.docx`, approval gate) unchanged.

### Data flow
```
user msg ─► POST /api/chat (Haiku + tools)
          ◄─ assistant msg + profile patch (+ ready?)
   …repeat until required fields satisfied…
model calls start_research ─► validate profile ─► create_client ─► jobs.start_research(slug)
chat.html then polls /api/clients/{slug}/status ─► progress + tips in-thread ─► report + .docx
```

## Cost & limits
- Intake ≈ 8–15 short Haiku turns ≈ a few cents/user. Opus runs only the research.
- Caps: ~25 intake turns max; bounded max_tokens per turn. Turn-cap → graceful "let's start with
  what we have" then validate + proceed (or ask for the one missing required field).

## Error handling / edge cases
- Required fields gate: server re-validates against the schema regardless of the model's `ready`
  signal; if invalid, return the validation gap so the chat keeps asking.
- Missing `ANTHROPIC_API_KEY` → `/api/chat` returns a clear 503 (chat needs the Messages API).
- Prompt-injection: intake is user-supplied text; the model only fills profile fields via the
  `update_profile` tool (no tool can run shell/research from the chat) — research stays behind the
  validated handoff.
- Local dev: direct Messages API needs a key; OAuth-only local can't run the live chat (test with a
  key or a mock). Railway/HF have the key.

## Scope
- **In:** chat.html, chat.py, `/api/chat`, system-prompt builder, handoff to `jobs.start_research`,
  `anthropic` dep, make chat the default landing page, **Instant KB teaser** (`preview_from_kb` tool
  + field→cluster mapper reading the KB catalogs).
- **Keep as fallback:** `intake-form.html` stays in the repo (unlinked) for quick revert.
- **Out (v1):** token-streaming (Haiku fast enough non-streaming + typing indicator); server-side
  transcript persistence (client holds it until handoff); changing any research-stage behavior.

## Verification
- Unit: system-prompt builder includes all schema-required fields; profile assembled from a scripted
  transcript validates against the schema; `start_research` handoff calls `create_client` +
  `jobs.start_research` (mock the SDK).
- Live (with a key): run a real chat to completion, confirm it produces a conforming
  `client_profile.json` and transitions into Phase B in-thread.
- Regression: the existing form path still works if re-linked (fallback intact).
