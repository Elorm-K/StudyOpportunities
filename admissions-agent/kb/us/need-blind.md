---
title: US need-blind / full-need-for-internationals schools
last_verified: 2026-06-20
source_urls:
  - https://www.nafsa.org/about/about-international-education/financial-aid-undergraduate-international-students  # most US colleges are need-AWARE for intl
  - https://sfs.mit.edu/undergraduate-students/apply-for-aid/international/        # MIT
  - https://admission.princeton.edu/cost-aid/how-princetons-aid-program-works     # Princeton
  - https://admissions.yale.edu/financial-aid-international-applicants             # Yale
  - https://www.amherst.edu/offices/financialaid/international_students            # Amherst
  - https://college.harvard.edu/financial-aid/how-aid-works                       # Harvard
freshness_threshold_days: 365  # but ALWAYS re-verify on the school's own page before presenting
status: seeded
---

# US need-blind & full-need-for-internationals schools

> **Context:** most US colleges are **need-aware** for international applicants — ability to pay can
> affect admission and aid is limited (NAFSA). Only a very small group admits internationals
> **without regard to ability to pay** *and* **meets 100% of demonstrated need**. This file mirrors
> the verified list in `kb/scholarships/us.md`.
>
> **Guardrail (CLAUDE.md #5):** the membership of this group shifts — **re-verify each school on its
> own financial-aid page** before presenting. `university-matching/scripts/score.py` up-ranks schools
> on this list via `funding_attainability_from_flags(need_blind_for_intl=..., meets_full_need_for_intl=...)`.

| School | Need-blind for intl? | Meets full need for intl? | Verified | Source |
|--------|----------------------|---------------------------|----------|--------|
| **MIT** | Yes | Yes (100% need, need-based) | 2026-06-20 | sfs.mit.edu |
| **Princeton** | Yes | Yes (100% need met with grants, no loans) | 2026-06-20 | admission.princeton.edu |
| **Yale** | Yes | Yes (full need, no loans) | 2026-06-20 | admissions.yale.edu |
| **Amherst** | Yes | Yes (100% of calculated need) | 2026-06-20 | amherst.edu |
| **Harvard** | Yes | Yes (100% of need) | 2026-06-20 | college.harvard.edu |

> **Effective class year:** not separately asserted per school in this pass — each page reflects
> current policy as of 2026-06-20. Confirm the policy still holds (and applies to the client's
> entry year) on the school's page before presenting.
>
> **Not asserted here:** specific aid dollar amounts (institution-specific), and the full ~10-school
> count the spec mentions — this list holds only schools confirmed on their own pages. Trigger
> `knowledge-base-update` to extend it (e.g. other full-need-for-intl schools) when needed.
