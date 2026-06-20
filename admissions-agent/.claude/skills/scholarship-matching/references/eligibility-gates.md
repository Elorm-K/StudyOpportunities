# Eligibility gates

The **hard gates** `scholarship-matching` applies BEFORE ranking. An award failing any gate is
**removed** from results — never shown as a long-shot. Apply in order; stop at the first failure.

## Gate order

1. **Nationality gate.** Is the client a citizen of an eligible country? Many awards are restricted
   (e.g. Chevening → Chevening-eligible countries; Commonwealth → Commonwealth countries; some US
   awards exclude certain nationalities). Check `identity.nationality` against the award's eligible
   list AND any exclusions. *Fail → remove.*

2. **Degree-level gate.** Does the award fund the client's level (`targets.degree_level`:
   undergraduate / postgraduate_taught / postgraduate_research)? Many awards are master's-only or
   PhD-only. *Fail → remove.*

3. **Field gate.** Does the award allow the client's `fields_of_study`? Some are subject-restricted
   (STEM-only, development-only, excludes certain fields). *Fail → remove.*

4. **Funding-need / type gate.** Does the award's funding type match the client's need
   (`targets.full_funding_required`)? A partial award may still pass if the client accepts partial
   funding; a need-based award may require demonstrated need. *Mismatch → remove or down-flag per
   the client's stated flexibility.*

## Secondary (post-gate) ranking signals — NOT gates

Applied only to awards that pass all gates, to order them by realistic competitiveness:

- academic band fit (`academics.mapped_grades` vs the award's typical bar — remember it's an estimate),
- test scores (`tests`) where the award requires them,
- work experience / leadership (`profile`),
- research output (`profile.research`) for research awards,
- award selectivity (how many awarded vs applicants, if known).

> Keep gates and ranking strictly separate. Gates eliminate; ranking orders survivors.
