---
name: eligibility-assessment
description: Use when classifying candidate universities as reach/target/safety for a client and estimating admission probability. Produces the per-school admission_probability that university-matching's scorer consumes.
---

# Eligibility assessment

Classify each candidate university as **reach / target / safety** for this client and compute an
**admission probability** per school. This runs *before* `university-matching` and produces the
admission axis its joint scorer (`score.py`) needs — so keep the output machine-readable.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `targets.target_universities`,
  `targets.fields_of_study`, `targets.countries`, `targets.degree_level`, `academics.mapped_grades`
  (the UK band / US GPA planning estimate), `tests`.
- KB (suggest from first): `kb/universities/<country>.md` — the pre-seeded catalog carries the
  **admit rate + grade/score band** per candidate school. Read these directly. Live fallback
  (`knowledge-base-update`) only when a school is absent from the catalog or its entry is stale
  (`lib/kb.is_stale(path, today)`).

## Process

1. **Assemble the candidate longlist.** Start from `targets.target_universities`; expand with a
   sensible field/country longlist (enough to yield 6–7 viable per country downstream). Each candidate
   is `{school, country}`.

2. **Read cited data per school from the catalog.** For each candidate take the **admit rate** and
   the **score/grade band** (p25/p50/p75) from `kb/universities/<country>.md`. Suggest from the
   catalog directly — live `knowledge-base-update` only for a school the catalog doesn't cover or
   whose entry is stale. Every admit rate shown carries its source + `last_verified`.

3. **Pick the applicant stat.** Use the client's comparable figure on the same scale as the band —
   typically `mapped_grades.us_gpa` (US 4.0 schools) or the relevant test score. Remember the grade
   is a **planning estimate** (`is_official=false`).

4. **Classify + score.** Run `scripts/classify.py` →
   `classify(admit_rate, applicant_stat, p25, p50, p75)`:
   - **reach** if `admit_rate < 0.15` OR applicant below p25,
   - **safety** if applicant above p75 AND admit rate ≥ 0.40,
   - **target** otherwise.
   It returns `admission_probability` (0..1) anchored on admit rate and nudged by band fit.

5. **Write the handoff.** Save `clients/<name>/outputs/eligibility.json` as a list of
   `{school, country, admit_rate, tier, admission_probability, source, last_verified}`. This is the
   contract `university-matching` reads. Set `pipeline_state.eligibility = "done"`.

## Output

- `clients/<name>/outputs/eligibility.json` (per-school tier + admission_probability + sources).
- `pipeline_state.eligibility = "done"`.

## Why a script

The reach/target/safety thresholds and the probability heuristic must be applied identically across
schools and runs. `classify.py` encodes them as deterministic, auditable code (like `grade_map.py` /
`score.py`) instead of re-deriving the cutoffs in prose each time.

## Guardrails (see ../../../CLAUDE.md)

- Cite every admit rate and score band with a source + `last_verified`; refresh stale KB first.
- Admission probabilities are **planning estimates**, not predictions — say so.
- The applicant's mapped grade is itself an estimate (`is_official=false`); don't present a tier as
  guaranteed.
