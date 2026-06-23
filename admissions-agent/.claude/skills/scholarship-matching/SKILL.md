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

**KB-first (default).** This skill *suggests* awards from the pre-seeded scholarship catalog; it does
**not** research live by default. Live search is a fallback for catalog misses and stale entries only.

1. **Assemble the candidate award pool from the KB** for the client's target countries — both the
   flagship awards and the **smaller / independent awards** sections in the `kb/scholarships/*.md`
   files. Suggest from these directly. **Live fallback only when:** (a) a needed entry is stale
   (`lib/kb.is_stale(path, today)`), or (b) the client's nationality/field has no KB coverage. In
   those cases invoke `knowledge-base-update` to fetch from an authoritative source and write the
   dated, sourced entry back to the catalog so the next client reuses it.

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

   **Mix in large NON-government awards (don't just list the obvious government flagships).** Alongside
   the general government/inter-governmental schemes (Chevening, Commonwealth, GREAT, Fulbright, PTDF,
   GETFund, LPDP…), deliberately surface the **large privately-funded awards** the client qualifies
   for — **private trusts/endowments** (Rhodes, Gates Cambridge, Clarendon, Knight-Hennessy),
   **foundations** (Mastercard Foundation, Aga Khan, AAUW, MMEG, P.E.O.), and **corporate** awards
   (NLNG, etc.). These are often overlooked, are frequently full-value, and can be a better fit than a
   competitive government scheme. Include at least one or two strong non-government options whenever
   the client is eligible.

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
