---
title: Grade conversion maps
last_verified: 2026-06-20
source_urls:
  - https://www.careers.ox.ac.uk/translating-qualifications        # UK class -> US GPA (First 3.7, 2:1 ~3.5)
  - https://www.kcl.ac.uk/abroad/applying/gpa-equivalent-by-country # UK mark boundaries (70/60/50/40)
  - https://www.wes.org/evaluations-and-fees/                       # WES course-by-course fees
  - https://www.wes.org/current-processing/                         # WES processing times
  - https://www.enic.org.uk/individuals/statement-of-comparability/cost  # UK ENIC fee
  - http://eng.oouagoiwoye.edu.ng/2018/05/17/classification-of-degrees/  # Nigerian 5.0 class boundaries
  - https://ice.unilag.edu.ng/resources/studentguide.pdf                 # UNILAG award regulations (5.0 scale)
  - https://www.qub.ac.uk/Study/international-students/your-country/Philippines/         # Philippines GPA -> UK band
  - https://www.ed.ac.uk/studying/international/postgraduate-entry/asia/malaysia          # Malaysia GPA -> UK band
  - https://www.surrey.ac.uk/thailand/entry-requirements                                  # Thailand GPA -> UK 2:1
  - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/696347/Overseas_degree_equivalency-methodology.pdf  # UK NARIC 2015: conversions are institution-set
  - https://coh.ug.edu.gh/node/118                                          # Ghana: Univ. of Ghana national class boundaries (4.0 FGPA)
  - https://sheffield.ac.uk/international/entry-requirements/ghana          # Ghana -> UK band (3.6/3.0/2.0)
  - https://www.southampton.ac.uk/uni-life/international/your-country/africa/ghana.page  # Ghana (stricter: First 3.75, 2:1 3.25)
  - https://sheffield.ac.uk/international/entry-requirements/bangladesh     # Bangladesh CGPA -> UK band
  - https://www.qmul.ac.uk/international-students/regions/south-asia/entry-requirements/bangladesh/  # Bangladesh CGPA -> UK band + HSC/SSC note
  - https://www.surrey.ac.uk/bangladesh/entry-requirements                 # Bangladesh (institution-dependent 2:1 floor)
freshness_threshold_days: 365  # conversion tables change slowly; costs/fees revised ~yearly
status: seeded
---

# Grade conversion maps

> **All conversions here are PLANNING ESTIMATES, never official.** `transcript-evaluation` sets
> `mapped_grades.is_official = false` always. The official application requires a WES (US) / UK ENIC
> evaluation (see costs below). Mappings vary by institution and by evaluator (WES, ENIC, and
> individual universities differ) — present them as guidance, not a fixed formula. These tables are
> the source of truth that `.claude/skills/transcript-evaluation/scripts/grade_map.py` encodes; when
> updating one, reconcile the other.

## UK honours bands ↔ US 4.0 GPA (approximate)

| UK class | UK mark band | US GPA (approx) | Confidence |
|----------|-------------|-----------------|------------|
| First Class Honours | 70%+ | ~3.7 | Oxford Careers Service (stated) |
| Upper Second (2:1) | 60–69% | ~3.5 (commonly 3.3–3.7) | Oxford Careers Service (stated) |
| Lower Second (2:2) | 50–59% | ~3.0 (commonly 2.7–3.0) | **approximate — not stated on an official .ac.uk page; common practice** |
| Third Class | 40–49% | ~2.0–2.7 | **approximate — not stated on an official .ac.uk page; common practice** |

- UK mark boundaries (70 / 60 / 50 / 40) per King's College London.
- First (3.7) and 2:1 (~3.5) are the cleanest citable .ac.uk figures (Oxford). The 2:2 and Third
  GPA values are **common-practice approximations** — flag them as such to the client, or trigger
  `knowledge-base-update` for a school-specific figure when it matters.
- `grade_map.py` currently encodes First→3.7, 2:1→3.3, 2:2→2.7, Third→2.0 (planning estimates).

## Foreign systems → UK band / US GPA

### Nigeria (5.0 CGPA scale)
Standard NUC-framework class boundaries, confirmed across Nigerian university regulations
(Olabisi Onabanjo University; UNILAG; University of Nigeria, Nsukka):

| Class | CGPA band (5.0 scale) | UK band (est.) | US GPA (est.) |
|-------|-----------------------|----------------|---------------|
| First Class | 4.50 – 5.00 | First | 3.7 |
| Second Class Upper (2:1) | 3.50 – 4.49 | 2:1 | 3.3 |
| Second Class Lower (2:2) | 2.40 – 3.49 | 2:2 | 2.7 |
| Third Class | 1.50 – 2.39 | Third | 2.0 |
| Pass | 1.00 – 1.49 | Pass / below honours | 1.0 |

> The 2.40 lower bound for 2:2 varies slightly between institutions (some use 2.50). Confirm against
> the client's specific university regulations when the grade sits near a boundary.

### Methodology note — why there is no single official table

There is **no free, authoritative master table** mapping these systems to UK bands / US GPA:
- UK ENIC's **Statement of Comparability does not comment on grades** at all
  (enic.org.uk/individuals/statement-of-comparability).
- ENIC/Ecctis **International Grade Comparisons** data sits behind paid membership (~£953–£4,944/yr),
  so its numeric conversions can't be cited from a public URL.
- The UK NARIC/DfE 2015 study covers only 41 countries (incl. Nigeria, India, Pakistan) — **not**
  Ghana, Vietnam, Philippines, Indonesia, Malaysia, Thailand, or Bangladesh.
- UK universities are autonomous and **set their own country-specific entry standards** (e.g. "75%
  from country X = 2:1"), so equivalences differ by institution.

→ The most citable figures are therefore **individual UK universities' published country pages**
(used below). Treat them as representative planning estimates, confirm against the specific target
university, and trigger `knowledge-base-update` for school-specific figures when it matters.

### West Africa & Southeast Asia (per-university citations; UK band confirmed, US GPA derived)

US GPA below is **derived** from the UK band via the table above (estimate), unless a US-scale figure
was directly cited. All entries are planning estimates.

#### Philippines (4-yr Bachelor; and University of the Philippines inverted 1.00–5.00 scale)
Source: Queen's University Belfast country page (degrees awarded from 2022).

| Origin grade | UK band | US GPA (derived) | Confidence |
|--------------|---------|------------------|------------|
| GPA 3.0/4.0 (or UP **1.5 or better** on the inverted scale) | 2:1 | ~3.3 | qub.ac.uk (stated) |
| GPA 2.5/4.0 (or UP **2.0 or better**) | 2:2 | ~2.7 | qub.ac.uk (stated) |

> UP scale is **inverted** (1.00 highest, 5.00 lowest) — do not read it as a normal GPA.

#### Malaysia (Bachelor Honours, 4.0 CGPA)
Source: University of Edinburgh postgraduate-entry country page.

| CGPA / grade | UK band | US GPA (derived) | Confidence |
|--------------|---------|------------------|------------|
| 3.6+ (A average) | First | ~3.7 | ed.ac.uk (stated) |
| 3.0–3.3 (B/B+ average) | 2:1 | ~3.3 | ed.ac.uk (stated) |

#### Thailand (4.0 scale)
Source: University of Surrey Thailand entry-requirements page.

| GPA | UK band | US GPA (derived) | Confidence |
|-----|---------|------------------|------------|
| 2.6 or 3.0 / 4.0 (institution-dependent) | 2:1 | ~3.3 | surrey.ac.uk (stated) |

#### Ghana 🟢 LEADING (4.0 GPA national classes)
National class boundaries from University of Ghana; UK mapping from Sheffield (canonical). US GPA is
**derived** (no primary US figure published; Scholaro is secondary).

| Class (national) | Ghana GPA (4.0) | UK band | US GPA (derived) | Source |
|------------------|-----------------|---------|------------------|--------|
| First Class | 3.60–4.00 | First | ~3.7 | coh.ug.edu.gh; sheffield (3.6) |
| Second Class Upper | 3.00–3.59 | 2:1 | ~3.3 | sheffield/edinburgh (3.0) |
| Second Class Lower | 2.00–2.99 | 2:2 | ~2.7 | sheffield (2.0) |
| Third Class | 1.50–1.99 | Third | ~2.0 | coh.ug.edu.gh |

> **Institution variation:** Southampton sets stricter cutoffs (First GPA **3.75**, 2:1 **3.25**) vs
> Sheffield (First 3.6, 2:1 3.0). So a Ghanaian near a boundary (~3.0–3.25, ~3.6–3.75) may be 2:1 or
> 2:2 / First or 2:1 depending on the target university — check the specific school. UG uses **FGPA**
> (weighted), distinct from a plain CGPA.

#### Bangladesh 🟢 LEADING (4.00 university CGPA)
University Bachelor uses the **4.00 CGPA** scale — NOT the secondary-school **HSC/SSC GPA-5.00** scale
(don't confuse them). UK mappings vary widely by UK institution *and* by the Bangladeshi university
attended; ranges below span the cited UK pages. US GPA derived (no primary figure).

| UK band | Bangladesh CGPA (typical range across UK unis) | US GPA (derived) | Source |
|---------|-----------------------------------------------|------------------|--------|
| First | ~3.5–4.0 (Sheffield 4.0; QMUL 3.2–3.7) | ~3.7 | sheffield/qmul |
| 2:1 | ~3.0–3.75 (Sheffield 3.5; QMUL 3.0–3.3; Surrey 3.25–3.75) | ~3.3 | sheffield/qmul/surrey |
| 2:2 | ~2.3–3.0 (Sheffield 3.0; QMUL 2.3–2.7) | ~2.7 | sheffield/qmul |

> Sheffield is notably strict (CGPA **4.0** = First). Confirm against the target university and the
> client's specific Bangladeshi institution when near a boundary. (HSC/SSC GPA-5.00: ~5.0 ≈ 80%+,
> used for UG entry — QMUL.)

#### Vietnam, Indonesia — background (on-demand)
Not a leading region; filled **on-demand by `knowledge-base-update`** when such a client appears
(`grade_map.py` raises `GradeMapUnavailable` meanwhile). Unverified starting points to CHECK, not
present: Vietnam 10-point (xuất sắc/giỏi/khá) + 4.0; Indonesia 4.0 IPK.

### Other systems
_Not seeded (German 1.0–5.0, Indian division/percentage, French 20-point, etc.). Same procedure:
trigger `knowledge-base-update`, add here, extend `grade_map.py`._

## Official credential evaluation (required for the real application)

| Service | Region | Cost | Turnaround | Notes |
|---------|--------|------|------------|-------|
| **WES** (World Education Services) | US | Course-by-Course **from ~USD $186** (+3% increase effective 1 Jan 2026; excludes delivery/tax). ICAP upgrade **+$53**. | ~2–3 business days to process documents after they arrive; full evaluation time varies once documents are verified. | Re-confirm exact base fee on the live fee page before quoting. |
| **UK ENIC** (operated by Ecctis) | UK | Statement of Comparability **£49.50** + delivery (bundled total ~£69.60). Fast Track: **£173.50** (48h) / **£223.50** (24h). | Standard **15 working days** from receipt of all documents + payment; Fast Track 1–2 working days. | — |

> **Verify-before-quoting:** WES base price ($186) and the Jan-2026 increase came from official-site
> search snippets, not a fetched fee table. Re-confirm at https://www.wes.org/evaluations-and-fees/
> before presenting as a firm figure (this is why `freshness_threshold_days` is 365 — re-verify each
> cycle). All figures last verified 2026-06-20.
