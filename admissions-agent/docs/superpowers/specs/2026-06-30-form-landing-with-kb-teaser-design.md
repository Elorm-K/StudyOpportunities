# Revert landing page to the structured form + add an instant KB teaser

**Date:** 2026-06-30
**Status:** Approved design, ready for implementation planning
**Area:** `admissions-agent/server/` (HTTP routing, results page, KB preview)

## Problem

The landing page (`GET /`) currently serves the conversational chat intake
(`server/static/chat.html` + `server/chat.py`, Haiku via the Messages API). We want the
**structured intake form** to be the entry point again. The form already exists and is fully
wired (`admissions-agent/intake/intake-form.html`, served at `/form`): it builds a
schema-shaped profile in the browser, POSTs to `/api/intake`, and the existing two-phase flow
takes over (Phase A intake/transcript review → optional clarifying questions →
Phase B full pipeline → operator-approved report).

The one nice thing the chat had that the form path lacks is the **instant KB teaser**: a few
real candidate universities and eligible scholarship names pulled straight from the pre-seeded
KB catalogs (`server/kb_preview.py`), shown before the full research finishes. We want the
form's results page to surface that teaser too.

## Goals

1. `GET /` serves the structured form; the chat moves to a fallback route.
2. The results page shows a compact, fixed-height wait UI — a **sticky carousel** cycling
   tips/progress in place (no ever-growing thread) — and pins the instant KB teaser ("first
   results") as a persistent card above it as soon as it is computed.

## Non-goals

- No change to Phase A / Phase B, `jobs`, `runner`, `state`, the schema, or report rendering.
- No change to the chat conversation logic itself (`server/chat.py`, `/api/chat`).
- No change to the form's client-side profile-building or validation.

## Design

### 1. Routing swap (`server/app.py`)

- `GET /` → serve `intake-form.html` (the existing `/form` handler body). It returns
  `FileResponse(config.INTAKE_FORM)` and 500s if the file is missing — same behavior the
  current `/form` route has.
- `GET /chat` → new route serving `config.STATIC_DIR / "chat.html"` (the body the current `/`
  handler has). `/api/chat` is unchanged.
- `GET /form` → kept as an alias of `/` so existing links keep working.

Net effect: the chat page and its API remain reachable at `/chat`; only the default landing
page changes. Nothing is deleted, so reverting is a one-line route swap.

### 2. KB teaser endpoint

**`server/kb_preview.py`** — add a structured variant alongside the existing string builder:

```python
def preview_payload(profile: dict) -> dict:
    """Structured instant teaser for the results page. {} when nothing matches."""
```

It reuses the existing helpers (`field_to_clusters`, `university_candidates`,
`scholarship_hints`) and returns, e.g.:

```json
{
  "universities": {
    "UK": [{"university": "University of Sheffield", "entry": "2:1", "funds_intl": false}]
  },
  "scholarships": ["Chevening", "Commonwealth"]
}
```

- `funds_intl` is `true` when the catalog row's funding flags contain
  `funds_internationals=yes` (mirrors the label logic in `build_preview`).
- Returns `{}` when there are no university matches and no scholarship hints.
- The existing `build_preview()` (plain-text string consumed by the chat model) is left
  untouched.

**`server/app.py`** — add:

```python
@app.get("/api/clients/{slug}/teaser")
async def get_teaser(slug: str):
    ...
```

- Reads the client's `client_profile.json` (via the same path config the rest of the server
  uses; `client_store` / `config` for the clients dir).
- If the client or profile file does not exist, return `{}` (HTTP 200) rather than 404, so the
  results page degrades silently — the teaser is a nice-to-have, never an error surface.
- Otherwise returns `preview_payload(profile)`.

### 3. Results page (`server/static/results.html`)

The current page is an ever-growing **chat thread** that appends a new bubble for every tip and
progress line, so the page lengthens for the whole wait. We replace the wait UX with a
**compact, fixed-height layout** that does not grow while research runs. The existing Markdown
renderer (`md`/`inline`) is kept and reused for the final report.

The page has up to three stacked regions:

1. **Teaser card (pinned, optional).** On load, fire one
   `fetch('/api/clients/' + slug + '/teaser')`. When it resolves with a non-empty payload,
   render a single persistent card and pin it **above** the carousel (guarded by a `teaserShown`
   flag so it appears once). It does **not** rotate — it stays put for the whole wait so the
   client can keep reading the real matches. Content:
   - Lead label: `Early matches from our knowledge base`.
   - For each country with candidates: a `<strong>` heading (`UK universities that fit your
     field`) followed by one line per university: `<name> — entry: <entry> (funds intl |
     scholarship-route funding)`.
   - If scholarships present: `Scholarships you may be eligible for: A, B, C.`
   - Trailing caveat: the same "quick preview from our knowledge base — your full plan will rank
     these…" note used in `build_preview`.
   - Built from the structured teaser JSON by the page's own helpers; does not use the Markdown
     renderer. A failed/empty teaser fetch is swallowed — no card, no error.

2. **Sticky carousel (the wait UI).** A single fixed-height card, `position: sticky` near the
   top, that **cross-fades through one message at a time, in place** — it replaces content
   rather than appending, so the page height stays constant during the wait. It cycles the same
   `PROGRESS` and `TIPS` content the current page uses, interleaved, advancing every ~7–8s, and
   keeps cycling the tips if research runs long. Each slide shows its lead label (e.g. `While you
   wait` for tips) and the message. No typing indicator and no thread.

3. **Report (replaces the wait UI).** On `done`, fetch the report and render it with the
   existing Markdown renderer + `.docx` download button. When the report renders, the carousel
   and the teaser card are removed/hidden — the report is the full ranked deliverable and
   supersedes the teaser.

State handling (the existing poll loop / state machine is kept; only what it drives changes):

- `queued` / `running_intake` / `running_research` / `awaiting_approval` → carousel runs (and
  the approval message can be surfaced as a carousel slide or the subheading).
- `awaiting_answers` → stop the carousel and show the "Answer the questions →" CTA in place of
  the carousel (the teaser card, if shown, stays pinned above).
- `error` → stop the carousel and show the error in place of it.
- `done` → render the report as in (3).

## Flow after the change

1. User lands on `/` → fills the form → Submit → POST `/api/intake` → redirect to
   `/clients/<slug>/results`.
2. Results page: the sticky carousel starts cycling progress/tips immediately; the teaser fetch
   fires and, within a second or two, pins the teaser card above the carousel. Page stays
   compact — no growing thread.
3. Phase A runs. If clarifying questions are produced, the carousel is replaced by the "Answer
   the questions →" CTA (teaser stays pinned above); otherwise Phase B proceeds and the carousel
   keeps cycling.
4. On `done`, the carousel + teaser are cleared and the report renders with the .docx download
   button.

## Testing / verification

- Static check: `/` returns the form HTML; `/chat` returns the chat HTML; `/form` still returns
  the form. (`curl` against a locally running server, or assert the route handlers return the
  expected `FileResponse` targets.)
- `preview_payload` unit check: feed a sample profile (e.g. Ghana / UK / PGT / public-health,
  the ama-mensah shape) and assert it returns real catalog universities and scholarship names,
  and `{}` for a profile with no country/field.
- `GET /api/clients/<slug>/teaser` returns the structured payload for an existing client and
  `{}` for an unknown slug.
- Manual: submit the form and confirm (a) the sticky carousel cycles tips/progress in place
  without the page growing, (b) the teaser card pins above it within a second or two, and (c) on
  completion the carousel + teaser clear and the report renders.

## Risks / notes

- The teaser depends on the submitted profile carrying `targets.countries`,
  `targets.fields_of_study`, `targets.degree_level`, and `identity.nationality`. The form marks
  countries, degree level, field, and nationality as required, so these are present at submit
  time.
- Local OAuth-only environments cannot run the chat (needs `ANTHROPIC_API_KEY`); moving chat to
  `/chat` and the form to `/` actually makes the default path work locally again, since the form
  → `/api/intake` path uses the agent SDK (CLI/OAuth), not the Messages API key.
