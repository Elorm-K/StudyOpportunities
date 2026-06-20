---
name: document-checklist
description: Use when generating a client's required-documents list. Emits a tailored checklist by country and degree level with per-item status tracking.
---

# Document checklist

Emit the client's **required-documents checklist**, tailored by country × degree level, with a status
per item so progress can be tracked through the application.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `targets.countries`, `targets.degree_level`,
  `targets.target_universities`, and `profile.portfolio` (portfolio-based fields).
- KB: `kb/uk/documents.md`, `kb/us/documents.md`. These are **deferred baselines** (conventional
  lists, not yet primary-source verified) → trigger `knowledge-base-update` to confirm the exact
  requirements on the **target university's** page before presenting as final.

## Process

1. **Branch.** For each country in `targets.countries`, select the document set for the client's
   `targets.degree_level` (UG / PGT / PGR) from the matching KB file:
   - UK: `kb/uk/documents.md` (UG via UCAS / PGT / PGR — PGR adds a research proposal + supervisor
     contact).
   - US: `kb/us/documents.md` (UG via Common App / grad — SOP, recommendations, tests).

2. **Tailor.** Add/remove items for the client's situation: English test only if not exempt;
   GRE/SAT only where required (note test-optional); portfolio if `profile.portfolio`; research
   proposal for PGR; CSS Profile for US internationals seeking aid. Drop anything inapplicable.

3. **Confirm against the target school.** Because the KB lists are deferred baselines, trigger
   `knowledge-base-update` to verify the exact list (and any school-specific extras) on each target
   university's admissions page; cite what you confirm.

4. **Emit with status tracking.** Write `clients/<name>/outputs/document-checklist.md` as a checklist
   grouped by country (and school where they differ), each item with a status:
   `pending` / `in_progress` / `done`. Set `pipeline_state.documents = "done"`.

## Output

- `clients/<name>/outputs/document-checklist.md` — per-item checklist with status, by country × level.
- `pipeline_state.documents = "done"`.

## Guardrails (see ../../../CLAUDE.md)

- The KB document lists are **baselines** — confirm the binding requirements on the target
  university's own page (cite + `last_verified`) before telling the client the list is complete.
- Flag items with long lead times (references, credential evaluation, tests) so they connect to
  `timeline-planning`.
