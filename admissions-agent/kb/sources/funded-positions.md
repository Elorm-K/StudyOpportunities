---
title: Funded-position source catalog
last_verified: 2026-06-20
source_urls:
  - https://www.jobs.ac.uk/phd
  - https://euraxess.ec.europa.eu/jobs/search
  - https://www.nature.com/naturecareers/jobs/phd-position/
  - https://www.timeshighereducation.com/unijobs/listings/
  - https://www.ukri.org/manage-your-award/studentship-guidance/guidance-for-training-grant-holders/
  - https://www.ukri.org/wp-content/uploads/2021/02/UKRI-030221-Guidance-International-Eligibility-Implementation-training-grant-holders-V2.pdf
  - https://www.lshtm.ac.uk/study/fees-and-funding/funding-scholarships/ukri-international-recruitment-lshtm
freshness_threshold_days: 180   # the CATALOG is slow-changing...
status: partial   # 4 sources + UKRI rules verified; FindAPhD/NSF/CSrankings/ProFellow/social NOT verified
---

# Funded-position source catalog

> Feeds the Stage-3 `funded-position-finder` skill (not yet built). **Live position listings are NEVER
> cached — always re-fetch.** Only this catalog of *where to look* lives here. Rows marked ⚠️ were in
> scope but their verification was cut off by a session limit — verify via `knowledge-base-update`
> (rerun after reset) before relying on them.

| Source | URL | Coverage | Free/paid | Filter mechanics | Intl-eligibility caveat | Status |
|--------|-----|----------|-----------|------------------|-------------------------|--------|
| **jobs.ac.uk** | jobs.ac.uk/phd | UK-centric; ~23–24 disciplines (Eng&Tech, Physical/Env Sci, CS, Maths, …) | Free | By discipline (live per-discipline counts) | UK funding often home-only — read each advert | ✅ |
| **EURAXESS** | euraxess.ec.europa.eu/jobs/search | Europe + beyond (EU Commission portal); PhD + funded fellowships (Horizon Europe, MSCA) | Free | Offer type (Job/Hosting/Funding), country, field, career stage R1–R4, sector, level, **funding programme & type**, deadline | MSCA/Horizon often international-friendly — verify per call | ✅ |
| **Nature Careers** | nature.com/naturecareers/jobs/phd-position/ | Global; sciences | Free to search | Discipline, location, **salary band**, hours, duration, qualification, recruiter, sector; many list "fully funded" + salary | Funding shown per listing — confirm intl eligibility | ✅ |
| **THEunijobs** | timeshighereducation.com/unijobs/listings/ | Global (Asia/Asia-Pacific heavy), 7 disciplines, ~1,200 listings | Free to search | Job type, discipline, location, salary band, contract, hours — **no funding-status or intl-eligibility filter** | No funding filter — must open each listing | ✅ |
| FindAPhD | findaphd.com | UK/global PhD listings | Free (paid extras) | funding filter to student's status | "fully funded" ≠ funded for internationals | ⚠️ NOT VERIFIED |
| NSF Award Search | nsf.gov | US — identify funded PI labs (not job ads) | Free | by award, PI, institution, abstract | indirect (find funded labs, then email PI) | ⚠️ NOT VERIFIED |
| CSrankings | csrankings.org | CS research groups by institution/area | Free | by area, geography | indirect (find active groups) | ⚠️ NOT VERIFIED |
| ProFellow | profellow.com | fellowships DB | freemium | by field/level | varies | ⚠️ NOT VERIFIED |
| Society boards (ACM, IEEE, APS, …) | per society | discipline-specific | varies | discipline | varies | ⚠️ NOT VERIFIED |
| Social (Bluesky / X "recruiting PhD students" / LinkedIn keyword→Posts→Past-week) | — | noisiest, most recent | free | manual search patterns | high verification burden; "scans social media" aggregator claims are marketing — verify against the official source | ⚠️ NOT VERIFIED |

## Structural funding & eligibility rules to bake in (UKRI — verified)

- **30% international cohort cap:** from AY 2021/22, UKRI normally limits international students to
  **30% of each cohort** per doctoral training grant (varies slightly by research council).
- **Home-fee-only from UKRI:** for an international student on a UKRI studentship, only the **home
  fee level** can be claimed from UKRI funding; the **home↔international fee gap** must be covered by
  the institution, a co-funder, a fee waiver, or the student.
- **Full awards, open to all:** since AY 2021/22 every UKRI studentship must be open to home **and**
  international students, and all receive a **full award** (stipend + home-level fees); fees-only
  awards were abolished.
- **US model (to verify + expand):** funding is via **RA / TA / fellowship** awarded by the
  department/PI — admission and funding are effectively one decision. (Detail not verified this run.)
- **Never cache listings:** postings change daily; `funded-position-finder` must re-fetch and stamp
  `last_verified` on every shortlisted position.

## Background — verified on-demand
FindAPhD, NSF Award Search, CSrankings, ProFellow, society boards, and the social-channel techniques
are **background priority** — `knowledge-base-update` verifies/expands them (and the US
RA/TA/fellowship structural detail) when the Stage-3 `funded-position-finder` skill needs them.
