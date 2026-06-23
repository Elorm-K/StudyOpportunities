# Intake question bank

Branching question bank for `client-intake`. Ask **only** the questions whose branch applies. Each
question is tagged with the downstream skill(s) it feeds, so intake captures exactly what the search
needs. Order: identity → targets/branching switches → academics (5 questions) → tests → funding →
profile.

Legend for branches: `[ALL]` always ask · `[UG]` undergraduate · `[PGT]` postgraduate taught ·
`[PGR]` postgraduate research · `[UK]` / `[US]` target country · `[FUND]` only if full funding
required.

---

## A. Identity `[ALL]`
| # | Question | Feeds | Profile field |
|---|----------|-------|---------------|
| A1 | Full name? | report-generation | `identity.full_name` |
| A2 | Nationality (all citizenships)? | scholarship-matching, funded-position-finder | `identity.nationality` |
| A3 | Country of residence? | timeline-planning (visa) | `identity.country_of_residence` |
| A4 | Date of birth? | document-checklist | `identity.date_of_birth` |

## B. Targets & branching switches `[ALL]` — ask these early; they gate everything else
| # | Question | Feeds | Profile field |
|---|----------|-------|---------------|
| B1 | Which countries are you targeting — UK, US, or both? | orchestrator routing, matching | `targets.countries` |
| B2 | What level — undergraduate, taught master's, or research (MRes/PhD)? | routing, deadlines, documents | `targets.degree_level` |
| B3 | Field(s) of study? | university-matching | `targets.fields_of_study` |
| B4 | Do you require full funding? | scholarship-matching, university-matching scoring | `targets.full_funding_required`, `funding.needs_scholarship` |
| B5 | Any specific universities already in mind? | university-matching | `targets.target_universities` |
| B6 | Which intake/start term are you aiming for? | timeline-planning | `targets.intake` |
| B7 | How many schools per country? (default 7) | university-matching | `targets.schools_per_country` |

### Research-only `[PGR]`
| # | Question | Feeds | Profile field |
|---|----------|-------|---------------|
| B8 | Specific research interests / subfield? **Push back if vague** — "CS" → ask for the subfield, problem, methods. | university-matching, funded-position-finder | `targets.research_interests` |
| B9 | Any labs, professors, or papers you admire? | funded-position-finder (PI discovery) | `targets.research_interests` (note PIs) / `profile.research` |

> **Vagueness rule:** B3/B8 must be specific enough to build a search query. If the answer can't
> seed a query, ask a follow-up before continuing.

## C. Academics — the 5 questions `[ALL]`
Ask each directly — academics are **self-reported**; the agent never parses transcripts or uploaded
documents. All values are self-reported → `is_official` stays false.

| # | Question | Feeds | Profile field |
|---|----------|-------|---------------|
| C1 | University / institution attended (name + country)? | transcript-evaluation, university-matching | `academics.qualifications[].institution`, `.institution_country` |
| C2 | Degree / qualification + field of study? | transcript-evaluation | `academics.qualifications[].name` |
| C3 | Grading system used (Nigerian 5.0 CGPA / UK honours / percentage / US 4.0 / other)? | transcript-evaluation (grade_map) | `academics.qualifications[].grading_system` |
| C4 | Your result / CGPA (the raw grade)? | transcript-evaluation, eligibility-assessment | `academics.qualifications[].raw_grade` |
| C5 | Graduation date (or expected)? | timeline-planning, eligibility-assessment | `academics.qualifications[].graduation_date` |

> **Consistency check:** the format of C4 must match the system named in C3 (e.g. a "4.52" with
> "UK honours" is a mismatch — re-ask). Set `source = confirmed` after the client verifies.

## D. Tests
| # | Question | Branch | Feeds | Profile field |
|---|----------|--------|-------|---------------|
| D1 | English test taken/planned (IELTS/TOEFL) + score + date? | `[ALL]` | eligibility, documents | `tests.english` |
| D2 | SAT/ACT taken + score? | `[UG][US]` | eligibility, matching | `tests.standardized[]` |
| D3 | GRE/GMAT taken + score? | `[PGT][PGR][US]` | eligibility, matching | `tests.standardized[]` |

## E. Funding
| # | Question | Branch | Feeds | Profile field |
|---|----------|--------|-------|---------------|
| E1 | Self-funding budget per year (if any)? | `[ALL]` | matching scoring | `funding.budget` |
| E2 | Any sponsor (self/family/government/none)? | `[ALL]` | scholarship-matching | `funding.sponsor` |
| E3 | Open to partial funding / lower-cost options if full funding isn't realistic? | `[FUND]` | scholarship-matching | `funding.needs_scholarship` (context) |

## F. Profile / competitiveness
| # | Question | Branch | Feeds | Profile field |
|---|----------|--------|-------|---------------|
| F1 | Relevant work experience (hours / years)? | `[ALL]` | scholarship-matching, eligibility | `profile.work_experience_hours` |
| F2 | Research output (publications, projects)? | `[PGR][PGT]` | funded-position-finder, scholarship | `profile.research` |
| F3 | Notable extracurriculars / leadership? | `[ALL]` | scholarship-matching | `profile.extracurriculars` |
| F4 | Portfolio (if a portfolio-based field)? | `[ALL]` | document-checklist | `profile.portfolio` |
