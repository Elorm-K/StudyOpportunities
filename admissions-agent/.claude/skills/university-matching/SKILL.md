---
name: university-matching
description: Use when generating the ranked shortlist of universities for a client. Produces 6–7 schools per target country, ranked by admission probability × funding attainability, with per-school reasoning and cited current data.
---

# University matching

Generate the client's ranked university shortlist: **6–7 schools per target country**, ranked by the
**joint score of admission probability × funding attainability** — never admission odds alone. A
school that admits the client but won't fund internationals must rank below a harder school that
funds fully.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `targets` (countries, degree_level, fields,
  research interests, schools_per_country), `academics.mapped_grades`, `tests`, `funding`,
  `identity.nationality`.
- KB: `kb/us/need-blind.md` (funding signal for US), plus live data (see below).

## Process

1. **Build the candidate set per country.** For each country in `targets.countries`, assemble
   candidate programs that actually offer the client's field at their degree level. Live-search to
   confirm the **program exists** for the target intake — don't shortlist a program that isn't
   offered.

2. **Get current data per candidate (cite everything).** For each candidate, gather:
   - current **admit rate** and **score/grade ranges** (for admission probability),
   - **tuition/fees** and **funding-for-internationals** facts (for funding attainability).
   Pull from KB if fresh; otherwise trigger `knowledge-base-update`. Every figure shown to the
   client needs a source URL + `last_verified`.

3. **Estimate the two axes (0..1).**
   - **admission_probability** — read it from `clients/<name>/outputs/eligibility.json` (written by
     `eligibility-assessment`: per-school `tier` + `admission_probability` + cited admit rate). If
     `eligibility` hasn't run for a candidate, invoke `eligibility-assessment` first rather than
     guessing.
   - **funding_attainability** — use `score.py`'s `funding_attainability_from_flags(...)`:
     - `scholarship_route=True` → funding is via a **portable** award the client can realistically win
       (e.g. Chevening/Commonwealth for an eligible nationality), usable at any eligible school. Set it
       from `scholarship-matching`'s *realistic* shortlist. **Essential for UK taught master's**, where
       universities rarely fund international students themselves — without it every UK PGT school
       collapses to ~0.05 and the funding axis is meaningless (Stage-5 finding).
     - `funds_internationals=False` → hard down-rank (the "admits but won't fund" case),
     - `need_blind_for_intl` / `meets_full_need_for_intl` (US, from `kb/us/need-blind.md` —
       **verify on the school's own page**) → up-rank,
     - `fully_funded_route=True` (e.g. funded PhD assistantship) → up-rank.

4. **Score and rank.** Call `scripts/score.py`:
   - `rank_per_country(candidates, per_country=targets.schools_per_country or 7)` returns the top
     6–7 per country by joint score.
   Write a short `reasoning` per candidate explaining the two axes.

5. **Present the shortlist.** One ranked table per country: school, program, admit rate, fee,
   funding-for-internationals, admission probability, funding attainability, joint score, reasoning,
   and source links. State which numbers are provisional.

6. **Persist.** Write the shortlist into the client's outputs and set
   `pipeline_state.university_match = "done"`.

## Why a script here

The joint score must be applied consistently across schools and runs. `score.py` encodes the rule
(product of the two axes, with the won't-fund-internationals collapse) as deterministic, auditable
code rather than ad-hoc prose ranking.

## Guardrails (see ../../../CLAUDE.md)

- Rank by **funding-aware** joint score, not admission odds alone.
- Verify need-blind / full-need claims on the university's own page before presenting.
- Cite every admit rate, fee, and funding fact with a source + date; refresh stale KB first.
- Don't over-promise funding — be explicit when a school admits but is unlikely to fund this client.
