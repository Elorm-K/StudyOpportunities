---
title: US university / program catalog
last_verified: 2026-06-22
source_urls:
  - https://sfs.mit.edu/undergraduate-students/apply-for-aid/international/
  - https://admission.princeton.edu/apply/international-students
  - https://admissions.yale.edu/financial-aid-international-applicants
  - https://financialaid.stanford.edu/undergrad/how/international.html
  - https://cc-seas.financialaid.columbia.edu/how/aid/works
  - https://grad.berkeley.edu/financial/doctoral-funding/
freshness_threshold_days: 365  # admit/fee figures are revised per cycle — re-verify annually
status: seeded
---

# US university / program catalog

> **Purpose.** Pre-seeded candidate catalog so `university-matching` and `eligibility-assessment`
> **suggest from here first** instead of researching every client live (CLAUDE.md "KB-first
> suggestion"). Live search is a fallback only — for a field cluster not covered below, or a row whose
> figures are stale (`lib/kb.is_stale`). When the fallback runs, **write the new row back here** so the
> next client reuses it.
>
> **Coverage is bounded** — a starter set of commonly-targeted schools across the clusters Nigerian /
> Ghanaian / Bangladeshi applicants most often pursue. A thin match (fewer than `schools_per_country`)
> for a client's field should trigger the live fallback, not a falsely-confident shortlist.
>
> **Need-blind / full-need (CLAUDE.md guardrail #5):** the authoritative list lives in
> `kb/us/need-blind.md`. This catalog mirrors its flags for convenience but **the school's own
> financial-aid page is the source of truth — re-verify before presenting.** Verified 2026-06-22:
> **need-blind + full-need for intl** = MIT, Princeton, Yale, Harvard, Amherst. **Need-aware for intl
> but meets full need** = Stanford, Columbia, Cornell. All others here are need-aware with limited
> master's aid for internationals.
>
> **Funding by level:** US **PhD** offers are usually **fully funded** (tuition waiver + stipend via
> assistantship) regardless of nationality — `fully_funded_route=yes`. US **master's** funding for
> internationals is usually limited (`funds_internationals=limited`). PhD `need_blind`/`meets_full_need`
> are marked `n/a`/`n/p` because doctoral support is merit/assistantship-based, not need-assessed.
>
> **`n/p` figures** (some admit rates, JS-gated tuition grids) are official figures not statically
> verifiable — NOT fabricated. Trigger the live fallback for that specific figure when a client needs it.

## Field clusters

Tag each row with one or more clusters so matching can filter by the client's `targets.fields_of_study`:

`cs-data` (computer science, data science, AI) · `engineering` · `business` (management, finance, MBA) ·
`public-health` (public health, epidemiology, global health) · `law` · `social-dev` (social sciences,
development, international relations, public policy) · `sciences` (natural/physical/life sciences)

## Funding-for-internationals flags (feed `university-matching/scripts/score.py`)

Encode the "Funds intl?" column with these keys so `funding_attainability_from_flags(...)` maps directly:

- `funds_internationals=yes|limited|no` — does the school fund international students from its own funds?
- `need_blind_for_intl=yes|no` — admission decided without regard to ability to pay.
- `meets_full_need_for_intl=yes|no` — meets 100% of demonstrated need for internationals.
- `fully_funded_route=yes` — a funded PhD studentship / assistantship exists for internationals.
- `scholarship_route=<award>` — the realistic portable award (e.g. Fulbright; set by `scholarship-matching`).

## Catalog

| University | Field cluster(s) | Degree level | Admit rate | Typical grade/score range | Intl tuition (per year) | Funds intl? (flags) | Source | last_verified |
|------------|------------------|--------------|-----------|---------------------------|-------------------------|---------------------|--------|---------------|
| MIT | cs-data, engineering | undergraduate | 4.6% (Class of 2029) | SAT EBRW 740–780; Math 780–800; ACT 34–36 (mid-50%) | $64,310 tuition; $89,340 COA (2025-26) | funds_internationals=yes; need_blind_for_intl=yes; meets_full_need_for_intl=yes; scholarship_route=MIT need-based aid (no merit) | https://sfs.mit.edu/undergraduate-students/apply-for-aid/international/ | 2026-06-22 |
| MIT | cs-data, engineering | postgraduate_research | n/p | n/p | covered by funding (full tuition + stipend + health; EECS RA ~$4,547/mo) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=n/a; fully_funded_route=yes | https://www.eecs.mit.edu/academics/graduate-programs/funding/ | 2026-06-22 |
| Princeton | social-dev, engineering | undergraduate | 4.6% | SAT EBRW 740–780; Math 770–800; ACT 34–35 (mid-50%) | $65,210 tuition; $86,680 COA (2025-26) | funds_internationals=yes; need_blind_for_intl=yes; meets_full_need_for_intl=yes; scholarship_route=need-based grant (no loans, no merit) | https://admission.princeton.edu/apply/international-students | 2026-06-22 |
| Princeton | engineering, sciences | postgraduate_research | n/p | n/p | covered by funding (full tuition + health + base stipend, all enrolled years) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=n/a; fully_funded_route=yes | https://gradschool.princeton.edu/financial-support/financial-support-model | 2026-06-22 |
| Yale | public-health, social-dev | undergraduate | 3.87% | SAT EBRW 720–770; Math 730–790 (mid-50%); ACT n/p | $72,500 tuition; $97,985 COA (2026-27) | funds_internationals=yes; need_blind_for_intl=yes; meets_full_need_for_intl=yes; scholarship_route=Yale need-based aid (no loans) | https://admissions.yale.edu/financial-aid-international-applicants | 2026-06-22 |
| Yale | sciences, public-health | postgraduate_research | n/p | n/p | covered by funding (tuition fellowship + 12-mo stipend ≥$50,777, 2025-26, min 5 yrs) | funds_internationals=yes; need_blind_for_intl=n/p; meets_full_need_for_intl=n/p; fully_funded_route=yes | https://gsas.yale.edu/graduate-financial-support-fellowships/funding-phd-students | 2026-06-22 |
| Harvard | public-health, social-dev | undergraduate | 4.2% (Class of 2029) | SAT EBRW 670–790; Math 680–800; ACT 31–36 (10th–90th pctile) | Net $0 for families <$100K; free tuition up to $200K (2025-26); sticker COA n/p | funds_internationals=yes; need_blind_for_intl=yes; meets_full_need_for_intl=yes; scholarship_route=Harvard need-based grant | https://college.harvard.edu/financial-aid/how-aid-works | 2026-06-22 |
| Harvard | public-health, sciences | postgraduate_research | n/p | n/p | covered by funding (tuition + health + 12-mo stipend ≥$50,000) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=yes; fully_funded_route=yes | https://gsas.harvard.edu/financial-support/funding-and-aid/financial-support-phd-students | 2026-06-22 |
| Stanford | cs-data, engineering | undergraduate | 3.61% | SAT 1510–1570; ACT 34–35 (mid-50%, Class of 2028) | $67,731 tuition; $97,545 COA (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=yes; scholarship_route=Stanford need-based institutional aid | https://financialaid.stanford.edu/undergrad/how/international.html | 2026-06-22 |
| Stanford | cs-data, engineering | postgraduate_research | n/p | n/p | covered by funding (5-yr guaranteed: tuition allowance + stipend) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=n/a; fully_funded_route=yes; scholarship_route=RA/TA + Stanford Graduate Fellowship | https://www.cs.stanford.edu/phd-program-overview/funding | 2026-06-22 |
| Columbia | engineering, public-health | undergraduate | 3.99% | SAT 1510–1560; ACT 34–36 (mid-50%, Class of 2029) | $70,170 tuition; ~$96,260 COA (2025-26) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=yes; scholarship_route=Columbia need-based grant (no loans) | https://cc-seas.financialaid.columbia.edu/how/aid/works | 2026-06-22 |
| Columbia | engineering, public-health | postgraduate_research | n/p | n/p | covered by funding (assistantship/fellowship: full tuition exemption + stipend) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=n/a; fully_funded_route=yes; scholarship_route=TA/RA or Fellowship | https://bulletin.columbia.edu/columbia-engineering/graduate-studies/financial-aid-graduate-study/ | 2026-06-22 |
| Cornell | engineering, cs-data | undergraduate | 8.4% (Fall 2024) | SAT 1510–1560 (EBRW 730–770; Math 770–800); ACT 33–35 (mid-50%) | $73,946 tuition; $99,734 COA (2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=yes; scholarship_route=none (all aid need-based; no merit) | https://finaid.cornell.edu/frequently-asked-questions-about-international-financial-aid | 2026-06-22 |
| Cornell | engineering, sciences | postgraduate_research | n/p | n/p | covered by funding (full tuition + fees + health + stipend; 99% of PhDs funded) | funds_internationals=yes; need_blind_for_intl=n/a; meets_full_need_for_intl=n/a; fully_funded_route=yes; scholarship_route=fellowship/RA/TA | https://gradschool.cornell.edu/financial-support/ | 2026-06-22 |
| Amherst College | social-dev, sciences | undergraduate | 9.0% | SAT 1450–1550 (EBRW 700–760; Math 720–790); ACT 32–35 (mid-50%) | $63,500 tuition; ~$98,460 COA (2025-26) | funds_internationals=yes; need_blind_for_intl=yes; meets_full_need_for_intl=yes; scholarship_route=need-based aid (no merit) | https://www.amherst.edu/admission/apply/international | 2026-06-22 |
| Carnegie Mellon University | cs-data, engineering | postgraduate_taught | n/p (UG Fall 2024 11.7% for context) | n/p (no GPA/GRE minimums; GRE "strongly recommended" for MSCS) | SCS master's $62,200; CIT master's $61,510 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no | https://www.cmu.edu/sfs/tuition/graduate/scs.html | 2026-06-22 |
| Carnegie Mellon University | cs-data, engineering | postgraduate_research | n/p | n/p | covered by funding (full-tuition scholarship + stipend, all admitted doctoral students) | funds_internationals=yes; fully_funded_route=yes; scholarship_route=full-tuition scholarship + stipend | https://www.csd.cmu.edu/phd-financial-support | 2026-06-22 |
| University of Michigan–Ann Arbor | engineering | postgraduate_taught | n/p | n/p | $63,796 (2025-26, non-resident, Rackham Engineering pre-candidate) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no | https://ro.umich.edu/sites/default/files/attachments/tuition/FeeBulletin-2025-2026.pdf | 2026-06-22 |
| University of Michigan–Ann Arbor | engineering | postgraduate_research | n/p | n/p | covered by funding (full tuition + 12-mo stipend + benefits) | funds_internationals=yes; fully_funded_route=yes; scholarship_route=Rackham PhD funding package | https://rackham.umich.edu/funding/funding-for-the-phd-degree/ | 2026-06-22 |
| University of Michigan–Ann Arbor | business | postgraduate_taught | n/p | n/p | $81,152 (2025-26, non-resident MBA tuition); total COA $111,966 | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=Ross merit MBA scholarships (intl eligibility not confirmed) | https://michiganross.umich.edu/graduate/full-time-mba/admissions/tuition-financial-aid | 2026-06-22 |
| Georgia Institute of Technology | cs-data, engineering | postgraduate_taught | n/p | Desirable min GPA 3.0/4.0; GRE n/p | ~$33,612/yr (out-of-country MS/PhD rate, Fall 2025) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=GRA/GTA assistantship (dept-awarded, not guaranteed) | https://www.cc.gatech.edu/funding-sources | 2026-06-22 |
| Georgia Institute of Technology | cs-data, engineering | postgraduate_research | n/p | n/p | covered by funding (tuition waiver + stipend; PhD GRA/GTA 50% FTE = $3,400/mo + waiver) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes; scholarship_route=GRA/GTA | https://www.cc.gatech.edu/funding-sources | 2026-06-22 |
| University of California, Berkeley | cs-data, engineering | postgraduate_taught | n/p | Min GPA 3.0/4.0; GRE not required nor accepted (EECS) | ~$39,864/yr (nonresident grad academic, 2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=limited dept block-grant fellowships | https://registrar.berkeley.edu/tuition-fees/fee-schedule/ | 2026-06-22 |
| University of California, Berkeley | cs-data, engineering, sciences | postgraduate_research | n/p | Min GPA 3.0/4.0; GRE not required nor accepted (EECS) | covered by funding (tuition + all fees + NRST + health + stipend; 5–6 yr packages) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=yes (within funded package); fully_funded_route=yes; scholarship_route=Doctoral funding package | https://grad.berkeley.edu/financial/doctoral-funding/ | 2026-06-22 |
| Johns Hopkins University (Bloomberg SPH) | public-health | postgraduate_taught | n/p | GRE/GMAT/MCAT optional & unscored; requires ≥2 yrs health-related work experience OR a doctoral degree | ~$69,870–$104,805 total (80-credit MPH; annual rate n/p); intl = domestic | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=Bloomberg Fellows / Sommer Scholars + need-based grants up to 25% (intl aid "extremely limited") | https://publichealth.jhu.edu/academics/mph/tuition-and-funding | 2026-06-22 |
| Johns Hopkins University (Bloomberg SPH) | public-health | postgraduate_research | n/p | Avg grad GPA ~3.50; GRE not used | covered by funding (full tuition + min stipend $52,000 (2026-27) + fees + health, ≥4 yrs) | funds_internationals=yes; need_blind_for_intl=n/p; meets_full_need_for_intl=yes (via funded route); fully_funded_route=yes; scholarship_route=Brown / Vivien Thomas / Sommer Scholars (intl covered) | https://publichealth.jhu.edu/academics/phd-in-health-policy-and-management/phd-funding | 2026-06-22 |
| Boston University (School of Public Health) | public-health | postgraduate_taught | n/p | No min GPA; competitive ≥3.0; GRE not required/considered | $34,935/semester (2025-26) ≈ $69,870/yr; ~$104,805 total for 48 credits | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=BUSPH scholarships (auto) + one-time $25,000 Access Grant (intl ineligible for US federal aid) | https://www.bu.edu/sph/admissions/tuition-and-funding/ | 2026-06-22 |
| Boston University (Questrom School of Business) | business | postgraduate_research | n/p | GMAT or GRE required (no waivers); GPA/score n/p | covered by funding (full tuition + fees + health + stipend $49,650 (2026-27), up to 5 yrs) | funds_internationals=yes; need_blind_for_intl=n/p; meets_full_need_for_intl=yes (full funding); fully_funded_route=yes; scholarship_route=Questrom doctoral fellowship (all admitted; no nationality restriction) | https://www.bu.edu/questrom/phd-program/fellowships/ | 2026-06-22 |
| University of Illinois Urbana-Champaign | cs-data, engineering | postgraduate_taught | n/p (rates gated behind login) | Min UG GPA 3.20 (CS MS); GRE not required | $39,344 (2025-26, non-resident, Grainger Engineering rate) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=no | https://catalog.illinois.edu/graduate/engineering/computer-science-ms/ | 2026-06-22 |
| University of Illinois Urbana-Champaign | cs-data, engineering | postgraduate_research | n/p (gated) | Min UG GPA 3.40 (CS PhD); min grad GPA 3.00; GRE not required | covered by funding (tuition waiver + stipend) for funded PhDs; else non-resident $39,344 (2025-26) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=n/p; fully_funded_route=yes; scholarship_route=graduate assistantship (TA/RA) + fellowships | https://catalog.illinois.edu/graduate/engineering/computer-science-phd/ | 2026-06-22 |
| Purdue University (West Lafayette) | cs-data, engineering | postgraduate_taught | ~7.4% (CS dept MS+PhD combined, Fall 2024) | Major & cumulative GPA typically >3.5/4.0; GRE not required/considered | $22,232 (2025-26, non-resident, CS/Eng differential) + $400/yr intl fee | funds_internationals=limited; need_blind_for_intl=n/p; meets_full_need_for_intl=no; fully_funded_route=no; scholarship_route=competitive assistantship/fellowship (selected MS only) | https://www.purdue.edu/treasurer/finance/bursar-office/tuition/fee-rates-2025-2026/graduate-tuition-and-fees-2025-2026/ | 2026-06-22 |
| Purdue University (West Lafayette) | cs-data, engineering | postgraduate_research | ~7.4% (CS dept MS+PhD combined, Fall 2024) | Major & cumulative GPA typically >3.5/4.0; GRE not required/considered | covered by funding (tuition remission + stipend) for funded PhDs; else $22,232 (2025-26) + $400/yr intl fee | funds_internationals=yes; need_blind_for_intl=n/p; meets_full_need_for_intl=yes; fully_funded_route=yes; scholarship_route=research/teaching assistantship + fellowships | https://www.cs.purdue.edu/graduate/financial_support/assistantships.html | 2026-06-22 |
