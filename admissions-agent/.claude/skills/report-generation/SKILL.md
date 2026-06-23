---
name: report-generation
description: Use when assembling the client-facing deliverable. Compiles the pipeline outputs into one cited Markdown report and pauses for operator approval before finalizing.
---

# Report generation

Assemble the whole pipeline into **one clean, client-facing Markdown report** — and **do not finalize
it without the operator's approval** (the human-approval gate). This is the consequential output, so a
human signs off before anything goes to the client.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`) — identity, targets, mapped grades.
- The section artifacts in `clients/<name>/outputs/` from earlier stages:
  - `eligibility.json` (reach/target/safety + admission_probability)
  - the ranked **university shortlist** (from `university-matching`)
  - the **scholarship plan** (from `scholarship-matching`)
  - `timeline.md` (from `timeline-planning`)
  - `document-checklist.md` (from `document-checklist`)
  - **funded positions** — *optional*: include only if present (`funded-position-finder` is deferred;
    skip the section gracefully if its output doesn't exist).

## Process

1. **Check completeness + freshness.** Confirm the prerequisite stages are `done` in
   `pipeline_state`. For any figure that's stale (`lib/kb.is_stale`), trigger `knowledge-base-update`
   first — the report must not ship an out-of-date number.

2. **Assemble the Markdown draft.** Compose the sections that have outputs **in this exact order**
   (the checklist is always LAST):
   1. **Client summary** — first name, target countries/level/field, funding need, and the assumed
      intake (earliest feasible **Fall** unless the client asked for Spring — see `timeline.md`).
   2. **Grade mapping** — UK band / US GPA, with the **planning-estimate caveat** (`is_official=false`;
      official WES/UK ENIC still required). Keep this brief.
   3. **University shortlist** — **ordered from target → safety** (most-attainable-with-funding first,
      down to the safest). **Cap at 10 schools total by default**; only include more if the client
      explicitly asked for a longer list (`targets.schools_per_country` / an explicit request). **Make
      each university name a Markdown link** to its course/source page (e.g. `[University of Leeds](https://…)`)
      so the list stays scannable. One tight line of joint-score reasoning (admission × funding) per school.
   4. **Scholarship plan** — eligible awards (hard-gates passed) + a short competitiveness note each; be
      honest where full funding is unlikely. **Link each award name** to its source
      (e.g. `[Chevening](https://…)`) instead of spelling out long URLs, so the section stays compact.
      Include large non-government awards (private trusts/foundations/corporate), not just the
      government flagships.
   5. **Funded positions** — *if available*. **Link each position/title** to its listing so the section
      stays short rather than printing full URLs.
   6. **Your plan** — the dated milestone calendar from `timeline.md`, built from the earliest feasible
      Fall intake (or the client's requested Spring).
   7. **Document checklist** — by country × level, with status. **This is the LAST section.**
   - **Every figure carries its source + `last_verified`** (carried through from the sourced outputs).
     No uncited numbers; no over-promised funding. Where a name is linked, the link IS its citation.

3. **Write the DRAFT.** Save `clients/<name>/outputs/report.draft.md`. Present it to the **operator**
   (not the client) for review.

4. **Approval gate — STOP here.** Wait for the operator's explicit approval. Do not finalize, send, or
   set the stage done without it. If the operator requests changes, revise the draft and re-present.

5. **Finalize on approval only.** Write `clients/<name>/outputs/report.md` and set
   `pipeline_state.report = "done"`.

## Output

- `clients/<name>/outputs/report.draft.md` → (after approval) `clients/<name>/outputs/report.md`.
- `pipeline_state.report = "done"` (only post-approval).

## Guardrails (see ../../../CLAUDE.md)

- **Human approval required** before any client-facing report is finalized (guardrail #7).
- Cite every figure with source + `last_verified`; refresh stale facts via `knowledge-base-update`
  first.
- Grade conversions are estimates; never promise full funding without a verified source — present
  honest alternatives where it's unlikely.

> **Author in Markdown; deliver as Word.** This skill writes Markdown (`report.draft.md` →
> `report.md`). The **client-facing deliverable is a Word document (.docx)** — rendered from the
> finalized `report.md` server-side and deterministically by `lib/report_docx.py` (served at
> `GET /api/clients/<slug>/report.docx`). Do **not** generate the .docx from inside this skill; keep
> authoring in Markdown so the approval gate stays a pure file promotion.
