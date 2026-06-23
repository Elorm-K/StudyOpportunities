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

2. **Assemble the Markdown draft.** Compose, in order, the sections that have outputs:
   1. **Client summary** — name, target countries/level/field, funding need.
   2. **Grade mapping** — UK band / US GPA, with the **planning-estimate caveat** (`is_official=false`;
      official WES/UK ENIC still required).
   3. **University shortlist** — the 6–7 per country, ranked by admission × funding (joint-score
      reasoning per school).
   4. **Scholarship plan** — eligible awards (hard-gates passed) + competitiveness notes; be honest
      where full funding is unlikely.
   5. **Funded positions** — *if available*.
   6. **Timeline** — the dated milestone calendar.
   7. **Document checklist** — by country × level, with status.
   - **Every figure carries its source + `last_verified`** (carried through from the sourced outputs).
     No uncited numbers; no over-promised funding.

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
