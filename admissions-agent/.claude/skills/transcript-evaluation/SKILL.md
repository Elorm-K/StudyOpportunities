---
name: transcript-evaluation
description: Use when a client's self-reported grades need mapping to UK bands and US GPA. Converts the grading system + result captured at intake into a UK honours band + US 4.0 GPA planning estimate.
---

# Transcript evaluation

Turn the client's **self-reported** academic record into usable UK/US grade equivalents: take the
grading system + result captured at intake and **map** it to a UK honours band and US 4.0 GPA.

The agent does **not** parse transcripts or any uploaded document — grades come only from the
client's self-reported answers (`client-intake`'s 5 academic questions). Every mapping is a
**planning estimate**, never an official credential evaluation. Set
`mapped_grades.is_official = false` always, and tell the client an official WES (US) / UK ENIC
evaluation will be needed for the actual application.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): the self-reported `academics.qualifications[]`
  (`grading_system` + `raw_grade`) captured by `client-intake`.

## Process

1. **Confirm the inputs are present.** Read the self-reported `grading_system` and `raw_grade` from
   `academics.qualifications[]`. If either is missing or too vague to map, route back to
   `client-intake` to capture it — do **not** invent or parse a value.

2. **Map the grade.** Call `scripts/grade_map.py` with the self-reported grading system + raw grade.
   It returns a UK band and US GPA via deterministic table lookups (no re-derivation in prose, so
   results are reproducible and auditable). Tables come from `references/grade-systems.md`
   (sourced from `kb/grading/grade-maps.md`).
   - If the grading system or grade isn't in the tables, the conversion is missing → trigger
     `knowledge-base-update` to source it, then retry. Don't guess a mapping.

3. **Store results.** Write `academics.mapped_grades`:
   - `uk_band`, `us_gpa` from the mapping
   - `is_official = false` (always)
   - `source` = how it was derived (e.g. "grade_map.py table lookup")
   Keep the raw values in `qualifications[]`. Save via `save_profile` (validates the schema).

4. **Flag the official evaluation.** Tell the client which official service applies and its cost /
   timeline (from `kb/grading/grade-maps.md`): WES for US applications, UK ENIC for UK. State
   clearly the current mapping is a planning estimate only.

5. **Update state.** Set `pipeline_state.transcript = "done"`.

## Output

- `academics.mapped_grades` populated (`is_official = false`).
- A note to the client on the required official evaluation (service, cost, timeline).
- `pipeline_state.transcript = "done"`.

## Why a script here

Grade conversions are deterministic table lookups. Encoding them as testable Python
(`grade_map.py`) — rather than re-deriving in prose each run — makes results reproducible and
auditable.

## Guardrails (see ../../../CLAUDE.md)

- `is_official` is **always false** here. The mapping drives matching; it is not a credential.
- Grades are self-reported — never parse or infer them from an uploaded document.
- Cite the conversion source; if missing/stale, refresh via `knowledge-base-update` before using.
