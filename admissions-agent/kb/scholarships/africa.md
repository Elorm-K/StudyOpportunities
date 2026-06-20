---
title: Africa / nationality-specific scholarships
last_verified: 2026-06-20
source_urls:
  - https://mastercardfdn.org/en/frequently-asked-questions/
  - https://mastercardfdn.org/en/articles/becoming-a-mastercard-foundation-scholar/
  - https://mastercardfdn.org/en/what-we-do/our-programs/mastercard-foundation-scholars-program/where-to-apply/
  - https://cscuk.fcdo.gov.uk/scholarships/commonwealth-phd-scholarships-for-least-developed-countries-and-vulnerable-states/
  - https://cscuk.fcdo.gov.uk/scholarships/commonwealth-masters-scholarships/
  - https://cscuk.fcdo.gov.uk/handbook/financial-allowances/
  - https://scholarship.ptdf.gov.ng/guidelines
  - https://www.nddc.gov.ng/
  - https://scholarships.gov.gh/                       # Ghana Scholarships Secretariat (Office of the President)
  - https://scholarships.gov.gh/opportunities          # Ghana bilateral foreign awards
  - https://citinewsroom.com/2020/02/auditor-general-indicts-getfund-for-illegally-funding-foreign-scholarships/  # GETFund bond (Auditor-General 2020; not live-verified)
freshness_threshold_days: 365
status: seeded
---

# Africa / nationality-specific scholarships

> Used by `scholarship-matching` for **nationality-based matching** — the **nationality/origin gate
> is the key hard gate** here. Hard-gate on it FIRST. Several 2026/27 windows have already closed as
> of seeding; deadlines are stored as recurring annual patterns and flagged for re-scrape.

| Award | Provider | Level | Value | Nationality / origin gate (KEY) | Other hard gates | Source |
|-------|----------|-------|-------|---------------------------------|------------------|--------|
| **Mastercard Foundation Scholars** | Mastercard Foundation (via **partner universities** — each its own application) | Secondary, **undergraduate, Master's** (no general PhD track at Foundation level) | **Comprehensive/"full"**: tuition, accommodation, books, mentoring, leadership dev, return airfare. No single fixed figure (varies by partner). | **African national** | Financial need; ethical-leadership commitment; **age**: UG ≤29, graduate ≤35 at application. **Per-partner deadlines** | mastercardfdn.org |
| **Commonwealth PhD (LDC/vulnerable states)** | CSC (FCDO) | PhD (full-time, UK) | **Full**: tuition + **£1,452/mo** (**£1,781/mo London**) + airfare + visa | Citizen/refugee/BPP of: **Bangladesh, Cameroon, The Gambia, Kenya, Kiribati, Lesotho, Malawi, Mozambique, Nigeria, Pakistan, Rwanda, Sierra Leone, Solomon Islands, Sri Lanka, Tanzania, Togo, Tuvalu, Uganda, Zambia** (19) | Permanent residence in eligible country; ≥**2:1** (or 2:2 + Master's); not already PhD-registered; unable to afford UK study | cscuk.fcdo.gov.uk |
| **Commonwealth Master's (low/middle-income)** | CSC (FCDO) | Taught Master's (UK) | **Full**: tuition + **£1,452/mo** (**£1,781/mo London**) + airfare + visa | Citizen/refugee/BPP of an eligible **low/middle-income Commonwealth** country (**44**, incl. Ghana, India, Nigeria, Kenya, South Africa, Pakistan — broader than the PhD list; note **India/Ghana/South Africa qualify for Master's but NOT the LDC PhD stream**) | ≥**2:1** (or 2:2 + PG qual); financial need | cscuk.fcdo.gov.uk |
| **PTDF Overseas Postgraduate (Nigeria)** | Petroleum Technology Development Fund (Nigeria govt) | MSc & PhD (UK PhDs split-site via CPESK) | Return flights, health insurance, tuition + bench fees, accommodation/living allowances. **Total figure NOT FOUND on official source** (do not import third-party "fully funded" numbers) | **Nigerian citizen who has completed NYSC** | ≥**2:1** (or 2:2 + relevant industry experience); verified NIN; 5 O-Level credits incl. English & Maths; oil-and-gas-relevant field | scholarship.ptdf.gov.ng |
| **NDDC Foreign Postgraduate (Niger Delta)** | Niger Delta Development Commission (Nigeria govt) | Foreign Master's | Value **pegged to prevailing Naira exchange rate — no fixed figure published (NOT FOUND on official source)** | **Indigene of one of the 9 Niger Delta states**: Abia, Akwa Ibom, Bayelsa, Cross River, Delta, Edo, Imo, Ondo, Rivers | Admission already secured into a foreign Master's; First Class or 2:1; completed NYSC | nddc.gov.ng |
| **GETFund Overseas Postgraduate (Ghana)** 🟢 | Ghana Education Trust Fund (Ghana govt) | Master's / PhD abroad | Tuition + living (figure not on a live primary page) | **Ghanaian citizen** | ⚠️ **Return-service bond — return to Ghana & serve ≥5 yrs; breach = refund all + 15% interest** (per Auditor-General 2020; **5yr/15% not live-verified** — confirm current terms). Key hard gate for clients wanting to settle abroad | getfund.gov.gh (via citinewsroom/AG report) |
| **Ghana Scholarships Secretariat / Authority** 🟢 | Office of the President (Ghana), est. 1960 | UG + PG abroad | Varies by award | **Ghanaian citizen** | Administers **foreign/bilateral awards** (Chinese Govt, Australian Awards, Serbia, Mauritius) sourced via Ministry of Foreign Affairs — mostly **non-UK/US destinations**; selected applicants forwarded to awarding country | scholarships.gov.gh |

## Mastercard Foundation — partner model (model as parent + per-partner children)

Mastercard is **not a single award** — eligibility/value/deadline vary by partner; the
"African national + financial need + leadership + age cap" gate is program-wide, the rest is
partner-specific. Verified partners include:

- **University of Edinburgh, UK** — Phase Two (2023–2030): full scholarships for 80 UG + 120 PG African students; climate-leadership focus.
- **Pan-Atlantic University, Nigeria**; **Sciences Po, France** (1,450 African students over a decade); University of Global Health Equity (Rwanda); Mohammed VI Polytechnic (Morocco); EARTH University (Costa Rica); Makerere University (Uganda).
- Full directory: https://mastercardfdn.org/en/what-we-do/our-programs/mastercard-foundation-scholars-program/where-to-apply/
- **US partner universities not confirmed in this pass** — verify per-partner before asserting any US institution.

## Deadline windows (recurring; all 2026/27 cycles closed as of 2026-06-20)

- **Mastercard** — no central deadline; each partner sets its own. Check the chosen partner page.
- **Commonwealth (both)** — cycle opens ~autumn (Sept–Oct); via Nominating Agency.
- **PTDF** — 2026 round closed **27 Feb 2026**; annual, expect next cycle late in the year.
- **NDDC** — cycle-based, announced on the NDDC portal; no fixed recurring date confirmable officially.

## Caveats

- Stipend figures (CSC £1,452/£1,781) are per-cycle rates CSC may revise before scholars arrive.
- PTDF and NDDC values are genuinely unquantified on official sources — present as "fully funded per
  the scheme" without a fabricated number, and trigger `knowledge-base-update` for the live figure.
- **GETFund (Ghana)** — the return-service bond (≥5 yrs / refund + 15%) traces to the Auditor-General's
  2020 audit, not a live GETFund page (their scholarship pages are JS-rendered) — flag the bond as
  real but **confirm current terms** before advising. The **Ghana Scholarships Secretariat** mostly
  brokers awards to **non-UK/US** countries (China, Australia, Serbia, Mauritius) — low relevance for
  a UK/US-focused client; their UK/US Commonwealth/Chevening routes are the better fit.
