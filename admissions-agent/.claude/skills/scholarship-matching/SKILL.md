---
name: scholarship-matching
description: Use when finding scholarships a client is realistically eligible for and can win. Hard-gates awards on nationality, degree level, field, and funding need first, then ranks the survivors by realistic competitiveness.
---

# Scholarship matching

Find the scholarships this client is **realistically eligible for and can win**. The order is
non-negotiable: **hard-gate first, then rank**. Never surface a categorically-ineligible award.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `identity.nationality`, `targets.degree_level`,
  `targets.fields_of_study`, `targets.countries`, `targets.full_funding_required`,
  `academics.mapped_grades`, `tests`, `profile`.
- KB: `kb/scholarships/uk.md`, `kb/scholarships/us.md`, `kb/scholarships/africa.md`,
  `kb/scholarships/seasia.md` (Southeast Asia + Bangladesh — read for SE-Asian/Bangladeshi clients;
  note many carry **return-service bonds**, a hard gate for clients aiming to settle abroad).
- References: `references/uk-awards.md`, `references/us-awards.md`, `references/eligibility-gates.md`.

## Process

1. **Assemble the candidate award pool** for the client's target countries from the KB scholarship
   files. Refresh any stale entries via `knowledge-base-update` first (figures shift each cycle).

2. **Hard-gate (eliminate, don't rank).** Drop any award that fails a categorical gate — see
   `references/eligibility-gates.md`. The gates, in order:
   - **nationality** — eligible citizenships (and any country exclusions),
   - **degree level** — UG / taught master's / research,
   - **field** — subject restrictions,
   - **funding need / type** — full vs partial, and whether the award matches the client's need.
   An award failing any gate is **removed**, never shown as a long-shot.

3. **Rank the survivors by realistic competitiveness.** For awards that pass all gates, rank by how
   well the profile fits the award's selection criteria (academic band, experience, leadership,
   research output) and the award's selectivity. Surface the strongest realistic targets first;
   note what would strengthen a weak-but-possible application.

4. **Be honest about odds.** If full funding is unlikely, say so and present partial-funding or
   lower-cost routes rather than over-promising (guardrail). Pair scholarship results with the
   funding-aware university shortlist from `university-matching`.

5. **Present + persist.** Output a ranked table: award, value (full/partial), the gates it passed,
   a competitiveness note, deadline, and source link (cited + dated). Write results to the client's
   outputs and set `pipeline_state.scholarship_match = "done"`.

## Guardrails (see ../../../CLAUDE.md)

- **Hard-gate before ranking** — never surface categorically-ineligible awards.
- Cite every award's value, deadline, and eligibility with a source + `last_verified`.
- Don't over-promise — be explicit when full funding is a long shot; offer alternatives.
