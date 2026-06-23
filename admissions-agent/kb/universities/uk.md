---
title: UK university / program catalog
last_verified: 2026-06-22
source_urls:
  - https://www.ox.ac.uk/admissions/graduate/fees-and-funding/funding/clarendon
  - https://www.gatescambridge.org/programme/the-scholarship/
  - https://www.imperial.ac.uk/study/courses/postgraduate-taught/computing/
  - https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/global-health-and-development-msc
  - https://www.lse.ac.uk/study-at-lse/graduate/msc-development-studies
  - https://www.lshtm.ac.uk/study/fees-and-funding/funding-scholarships/masters-funding
freshness_threshold_days: 365  # admit/fee figures are revised per cycle — re-verify annually
status: seeded
---

# UK university / program catalog

> **Purpose.** Pre-seeded candidate catalog so `university-matching` and `eligibility-assessment`
> **suggest from here first** instead of researching every client live (CLAUDE.md "KB-first
> suggestion"). Live search is a fallback only — for a field cluster not covered below, or a row whose
> figures are stale (`lib/kb.is_stale`). When the fallback runs, **write the new row back here** so the
> next client reuses it.
>
> **Coverage is bounded** — this is a starter set of commonly-targeted schools across the clusters
> Nigerian / Ghanaian / Bangladeshi applicants most often pursue. A thin match (fewer than
> `schools_per_country`) for a client's field should trigger the live fallback, not a falsely-confident
> shortlist.
>
> **UK admissions are requirement-based**, not percentile-based. For taught postgraduate (PGT), the
> **entry grade requirement** (e.g. UK 2:1 / First, or the country-equivalent in `kb/grading/grade-maps.md`)
> matters more than an "admit rate" — UK schools rarely publish programme admit rates, so admit rate is
> `n/p` (not published) on every row here; rely on the entry-requirement column.
>
> **Funding reality (UK PGT):** UK universities rarely fund international taught-master's students
> directly — funding usually comes via a **portable scholarship** (Chevening / Commonwealth / Gates /
> Clarendon — see `kb/scholarships/uk.md`). That is why `score.py` needs `scholarship_route` set from
> `scholarship-matching`; the per-school flag here records only what the *school itself* offers. No UK
> school here is need-blind or meets-full-need for internationals (UK PGT aid is merit/partial-discount).
>
> **`n/p` figures** (e.g. some intl tuition cells) are official figures published only behind
> JavaScript fee tools that couldn't be statically verified — they are NOT fabricated. Trigger the live
> fallback for that specific figure when a client needs it, then write it back.

## Field clusters

Tag each row with one or more clusters so matching can filter by the client's `targets.fields_of_study`:

`cs-data` (computer science, data science, AI) · `engineering` · `business` (management, finance, MBA) ·
`public-health` (public health, epidemiology, global health) · `law` · `social-dev` (social sciences,
development, international relations, public policy) · `sciences` (natural/physical/life sciences)

## Funding-for-internationals flags (feed `university-matching/scripts/score.py`)

Encode the "Funds intl?" column with these keys so `funding_attainability_from_flags(...)` maps directly:

- `funds_internationals=yes|limited|no` — does the school fund international students from its own funds?
- `need_blind_for_intl=yes|no` — admission decided without regard to ability to pay (rare; US-centric).
- `meets_full_need_for_intl=yes|no` — meets 100% of demonstrated need for internationals.
- `fully_funded_route=yes` — a funded PhD studentship / assistantship exists for internationals.
- `scholarship_route=<award>` — the realistic portable award (set authoritatively by `scholarship-matching`).

## Catalog

| University | Field cluster(s) | Degree level | Admit rate | Typical grade/score range (entry requirement) | Intl tuition (per year) | Funds intl? (flags) | Source | last_verified |
|------------|------------------|--------------|-----------|-----------------------------------------------|-------------------------|---------------------|--------|---------------|
| University of Oxford | cs-data | postgraduate_taught | n/p | First / strong 2:1 in CS or related; A-Level maths + programming | £41,250 (2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Clarendon | https://www.ox.ac.uk/admissions/graduate/courses/msc-advanced-computer-science | 2026-06-22 |
| University of Oxford | business | postgraduate_taught | n/p | First or strong 2:1; strong quantitative (MSc Financial Economics) | £59,360 (2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Clarendon | https://www.sbs.ox.ac.uk/programmes/degrees/msc-financial-economics | 2026-06-22 |
| University of Oxford | cs-data | postgraduate_research | n/p | Strong 2:1 / First (most Clarendon scholars ≥First); DPhil CS | £34,700 (2026-27) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes; scholarship_route=Clarendon | https://www.ox.ac.uk/admissions/graduate/fees-and-funding/funding/clarendon | 2026-06-22 |
| University of Cambridge | cs-data | postgraduate_taught | n/p | First-class honours in CS/numerate field; IELTS 7.5 (7.0 each) | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Gates | https://www.postgraduate.study.cam.ac.uk/courses/directory/cscsmpacs/requirements | 2026-06-22 |
| University of Cambridge | business | postgraduate_taught | n/p | Good honours + strong record + work experience (Master of Finance, Judge) | £60,000 (2025-26 & 2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Gates | https://www.jbs.cam.ac.uk/masters-degrees/master-of-finance/fees-funding/ | 2026-06-22 |
| University of Cambridge | cs-data | postgraduate_research | n/p | Strong 2:1 / First-class honours typical | n/p | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes; scholarship_route=Gates | https://www.gatescambridge.org/programme/the-scholarship/ | 2026-06-22 |
| Imperial College London | engineering, cs-data | postgraduate_taught | n/p | First-class degree (UK First or equiv); high English requirement | £46,000 (2026 entry) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=GREAT/Women in STEM | https://www.imperial.ac.uk/study/courses/postgraduate-taught/computing/ | 2026-06-22 |
| Imperial College London | business | postgraduate_taught | n/p | First or 2:1 in highly quantitative subject; IELTS 7.0 (6.5 each) | £51,000 (2026 entry, total programme) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Dean's Impact/African Future Leader Award | https://www.imperial.ac.uk/business-school/masters/finance/fees-and-funding/ | 2026-06-22 |
| Imperial College London | engineering, cs-data | postgraduate_research | n/p | First-class MEng/Master's or First Bachelor's + distinction MSc | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes (EPSRC DTP is Home-only); scholarship_route=Imperial College PhD Scholarship | https://www.imperial.ac.uk/computing/prospective-students/courses/phd/scholarships/ | 2026-06-22 |
| UCL | cs-data | postgraduate_taught | n/p | UK 2:1 or intl equivalent; UCL English Level 2 | £42,700 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=GREAT (East London Scholarship is UK-only) | https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/computer-science-msc | 2026-06-22 |
| UCL | public-health | postgraduate_taught | n/p | UK 2:1 or intl equivalent (Global Health & Development MSc) | £35,400 (2026-27) | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Commonwealth Shared/African Graduate Scholarship | https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/global-health-and-development-msc | 2026-06-22 |
| UCL | cs-data | postgraduate_research | n/p | Strong Master's / First Bachelor's (UK 2:1+ typical) | £34,700 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes (some studentships intl-eligible); scholarship_route=UCL Research Opportunity/CSC-UCL | https://www.ucl.ac.uk/prospective-students/graduate/research-degrees/computer-science-4-year-programme-mphil-phd | 2026-06-22 |
| LSE | social-dev | postgraduate_taught | n/p | UK 2:1 in any discipline (MSc Development Studies) | £30,400 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=LSE Master's Awards/Excellence; Chevening (external) | https://www.lse.ac.uk/study-at-lse/graduate/msc-development-studies | 2026-06-22 |
| King's College London | law | postgraduate_taught | n/p | High UK 2:1, final mark ≥65% (law or ≥70% law-content degree) (LLM) | £38,300 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening (external) | https://www.kcl.ac.uk/study/postgraduate-taught/courses/master-of-laws-llm/fees | 2026-06-22 |
| King's College London | public-health | postgraduate_taught | n/p | UK 2:1 (Global Health MSc) | £38,300 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening (external) | https://www.kcl.ac.uk/study/postgraduate-taught/courses/global-health-msc/fees | 2026-06-22 |
| Queen Mary University of London | law | postgraduate_taught | n/p | UK 2:1 (law or law-substantial degree) (LLM) | £18,975 (2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening; Roy Goode (half fee waiver) | https://www.qmul.ac.uk/postgraduate/taught/coursefinder/courses/laws-llm/ | 2026-06-22 |
| Queen Mary University of London | cs-data | postgraduate_taught | n/p | UK 2:1 in CS/EE/SE/IT/Maths (good 2:2 case-by-case); IELTS 6.5 | £17,650 (2025-26) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening | https://www.qmul.ac.uk/postgraduate/taught/coursefinder/courses/advanced-computer-science-msc/ | 2026-06-22 |
| LSHTM | public-health | postgraduate_taught | n/p | UK 2:1 in relevant discipline (or medical degree); 2:2 + ~2 yrs exp considered | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening; Commonwealth Shared/Master's | https://www.lshtm.ac.uk/study/courses/masters-degrees/public-health | 2026-06-22 |
| LSHTM | public-health | postgraduate_research | n/p | Strong 2:1 / Master's in relevant field (PhD/DrPH) | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; fully_funded_route=yes (Commonwealth PhD: CSC 80% + LSHTM 20% + stipend); scholarship_route=Commonwealth PhD; UKRI (overseas top-up) | https://www.lshtm.ac.uk/study/fees-and-funding/funding-scholarships/research-degree-funding | 2026-06-22 |
| University of Edinburgh | cs-data | postgraduate_taught | n/p | UK 2:1 (typical offer UK 1st) in a quantitative discipline; IELTS 7.0 (6.5 each) | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening/Commonwealth (external) | https://study.ed.ac.uk/programmes/postgraduate-taught/902-data-science | 2026-06-22 |
| University of Manchester | engineering | postgraduate_taught | n/p | UK 2:1 in a relevant science/engineering discipline; IELTS 7.0 (6.5 each) | £38,400 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Manchester Master's Bursary / merit | https://www.manchester.ac.uk/study/masters/courses/list/08025/msc-aerospace-engineering/ | 2026-06-22 |
| University of Manchester | cs-data | postgraduate_taught | n/p | UK 1st (70% avg) typical; min 50% CS content; IELTS 7.0 (6.5 each) | £39,400 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Manchester Master's Bursary / merit | https://www.manchester.ac.uk/study/masters/courses/list/21573/msc-advanced-computer-science/ | 2026-06-22 |
| University of Warwick | business, cs-data | postgraduate_taught | n/p | UK 2:1 (or equivalent); IELTS 7.0 | £38,150 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=WBS scholarships/Chevening | https://warwick.ac.uk/study/postgraduate/courses-2026/msc-business-analytics/ | 2026-06-22 |
| University of Sheffield | engineering, sciences | postgraduate_taught | n/p | UK 2:1 in a relevant subject; IELTS 6.5 (6.0 each) | n/p | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=International Postgraduate Scholarship (£3,000 fee reduction, automatic for self-funded overseas PGT) | https://sheffield.ac.uk/international/fees-and-funding/scholarships/postgraduate/international-postgraduate-scholarship | 2026-06-22 |
| University of Leeds | business | postgraduate_taught | n/p | UK 2:1 (hons) in any subject; IELTS 6.5 (no band <6.0) | £32,750 (2026-27, total for 12-month MSc) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Leeds Business School Excellence Scholarship (10/20/50% tuition) | https://courses.leeds.ac.uk/a078/management-msc | 2026-06-22 |
| University of Leeds | engineering | postgraduate_taught | n/p | UK 2:1 (hons) in engineering (2:2 + 3 yrs exp considered); IELTS 6.5 (no band <6.0) | £33,500 (2026-27, total for MSc) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening/Commonwealth (external) | https://courses.leeds.ac.uk/f360/advanced-mechanical-engineering-msc-eng- | 2026-06-22 |
| University of Birmingham | public-health | postgraduate_taught | n/p | UK 2:1 relevant to public health (2:2 + work exp considered); IELTS 6.5 (no band <6.0) | £30,420 (2026 entry, MPH full-time) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Birmingham Masters Scholarship (£3,000 discount) | https://www.birmingham.ac.uk/study/postgraduate/subjects/medicine-courses/public-health-mph | 2026-06-22 |
| University of Glasgow | cs-data | postgraduate_taught | n/p | UK 2:1 (Computing-major, ≥50% computing modules); IELTS 6.5 (no subtest <6.0) | £34,470 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=World Changers Glasgow (£5,000); Glasgow African Excellence Award (full tuition waiver, ~16); Glasgow Caribbean Excellence Award (full tuition waiver) | https://www.gla.ac.uk/postgraduate/taught/datascience/ | 2026-06-22 |
| University of Surrey | engineering, cs-data | postgraduate_taught | n/p | UK 2:2 (electronic/electrical/computer eng, maths, physics, telecoms); IELTS 6.5 | £25,900 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=International Excellence Award (PG) (£5,000 off tuition) | https://www.surrey.ac.uk/postgraduate/electronic-engineering-msc | 2026-06-22 |
| University of Edinburgh | public-health | postgraduate_taught | n/p | UK 2:1 or intl equivalent (Global Health Policy MSc); IELTS 7.0 (6.0 each) | n/p | funds_internationals=yes; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Mastercard Foundation Scholars Program (full, African nationals, UK 2:1+, age ≤35); Chevening/Commonwealth Shared (external) | https://study.ed.ac.uk/programmes/postgraduate-taught/384-global-health-policy | 2026-06-22 |
| University of Manchester | public-health | postgraduate_taught | n/p | UK 2:1 (2:2 + ~3 yrs public-health experience considered) (Master of Public Health MPH, on campus); IELTS 6.5 (6.0 each) | £29,900 (2026 entry) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=Chevening; Commonwealth Shared/Master's (external) | https://www.manchester.ac.uk/study/masters/courses/list/21021/mph-master-of-public-health-on-campus/ | 2026-06-22 |
| University of Liverpool | public-health | postgraduate_taught | n/p | UK 2:2 or above (Master of Public Health MPH); IELTS 7.0 (no band <6.5) | £30,000 (2026-27) | funds_internationals=limited; need_blind_for_intl=no; meets_full_need_for_intl=no; scholarship_route=PG Global Advancement Scholarship - Country (£2,500, incl. Ghana, automatic); Commonwealth Postgraduate Bursary; Chevening (external) | https://www.liverpool.ac.uk/courses/master-of-public-health-mph | 2026-06-22 |
