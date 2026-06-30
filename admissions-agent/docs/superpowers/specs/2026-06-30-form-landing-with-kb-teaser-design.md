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
2. The results page shows the existing tips/progress drip immediately, and inserts the instant
   KB teaser ("first results") as soon as it is computed.

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

- The tips + progress drip still starts immediately on load (unchanged — "tips first").
- On load, fire one `fetch('/api/clients/' + slug + '/teaser')`. When it resolves with a
  non-empty payload, render a single teaser bubble and append it to the thread, guarded by a
  `teaserShown` flag so it appears once.
- Bubble content:
  - Lead label: `Early matches from our knowledge base`.
  - For each country with candidates: a `<strong>` line (`UK universities that fit your field`)
    followed by one line per university: `• <name> — entry: <entry> (funds intl |
    scholarship-route funding)`.
  - If scholarships present: `Scholarships you may be eligible for: A, B, C.`
  - Trailing caveat: the same "quick preview from our knowledge base — your full plan will rank
    these…" note used in `build_preview`.
- The teaser is built from the structured JSON in the page's own helpers; it does not reuse the
  markdown renderer.
- Failure of the teaser fetch is swallowed (no bubble, no error) — the page proceeds with the
  normal drip + report flow.

## Flow after the change

1. User lands on `/` → fills the form → Submit → POST `/api/intake` → redirect to
   `/clients/<slug>/results`.
2. Results page: tips/progress drip starts; teaser fetch fires; teaser bubble appears within a
   second or two.
3. Phase A runs. If clarifying questions are produced, the page shows the "Answer the
   questions →" CTA (existing behavior); otherwise Phase B proceeds.
4. On `done`, the report renders in-thread with the .docx download button (existing behavior).

## Testing / verification

- Static check: `/` returns the form HTML; `/chat` returns the chat HTML; `/form` still returns
  the form. (`curl` against a locally running server, or assert the route handlers return the
  expected `FileResponse` targets.)
- `preview_payload` unit check: feed a sample profile (e.g. Ghana / UK / PGT / public-health,
  the ama-mensah shape) and assert it returns real catalog universities and scholarship names,
  and `{}` for a profile with no country/field.
- `GET /api/clients/<slug>/teaser` returns the structured payload for an existing client and
  `{}` for an unknown slug.
- Manual: submit the form and confirm the teaser bubble appears on the results page ahead of the
  full report.

## Risks / notes

- The teaser depends on the submitted profile carrying `targets.countries`,
  `targets.fields_of_study`, `targets.degree_level`, and `identity.nationality`. The form marks
  countries, degree level, field, and nationality as required, so these are present at submit
  time.
- Local OAuth-only environments cannot run the chat (needs `ANTHROPIC_API_KEY`); moving chat to
  `/chat` and the form to `/` actually makes the default path work locally again, since the form
  → `/api/intake` path uses the agent SDK (CLI/OAuth), not the Messages API key.
