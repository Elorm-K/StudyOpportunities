---
name: university-matching
description: Use when generating the ranked shortlist of universities for a client. Produces 6–7 schools per target country, ranked by admission probability × funding attainability, with per-school reasoning and cited current data.
---

# University matching

Generate the client's ranked university shortlist: **6–7 schools per target country**, ranked by the
**joint score of admission probability × funding attainability** — never admission odds alone. A
school that admits the client but won't fund internationals must rank below a harder school that
funds fully.

**Composition — balanced, never top-heavy.** Each per-country set should contain **at most one
reach/top-tier school**, with the **majority drawn from target and safety tiers** (use the `tier`
from `eligibility.json`). The goal is a realistic reach/target/safety mix, not an all-elite list — see
CLAUDE.md "Composition". Ranking math is unchanged; this only constrains which schools fill the slots.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `targets` (countries, degree_level, fields,
  research interests, schools_per_country), `academics.mapped_grades`, `tests`, `funding`,
  `identity.nationality`.
- KB (suggest from these first): `kb/universities/uk.md`, `kb/universities/us.md` — the pre-seeded
  university/program catalog (admit rate, grade/score range, intl fees, funds-intl flags per
  university × field cluster). `kb/us/need-blind.md` (authoritative need-blind list for US). Live
  data is the fallback only (see below).

## Process

**KB-first (default).** This skill *suggests* from the pre-seeded catalog; it does **not** research
live by default. Live search is a fallback for catalog misses and stale entries only — see step 1.

1. **Build the candidate set per country from the catalog.** For each country in `targets.countries`,
   select catalog rows from `kb/universities/<country>.md` whose **field cluster** matches the
   client's `targets.fields_of_study` and whose degree level matches. These are the suggested
   candidates — no live search when the catalog covers the field.
   **Live fallback only when:** (a) the field cluster has no or too-thin coverage for that country
   (fewer than `schools_per_country`), or (b) a needed catalog entry is stale
   (`lib/kb.is_stale(path, today)`). In those cases invoke `knowledge-base-update` (or an in-skill
   allow-listed search) to confirm the program exists and fill the gap, then write it back to the
   catalog so the next client reuses it.

2. **Read the current data per candidate from the catalog (cite everything).** Each catalog row
   already carries:
   - **admit rate** and **score/grade ranges** (for admission probability),
   - **intl tuition/fees** and **funding-for-internationals** flags (for funding attainability),
   - a source URL + `last_verified`.
   Use those directly. Only re-fetch a specific figure if its entry is stale. Every figure shown to
   the client must still carry its source URL + `last_verified` from the catalog.

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
   Then **enforce the balanced composition**: keep at most one reach/top-tier school and fill the rest
   from target + safety (by `tier`). If the top of the joint-ranked list is all reaches, swap the
   surplus reaches for the best-scoring target/safety candidates so the set stays a realistic mix.
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
