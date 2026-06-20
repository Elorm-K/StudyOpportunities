# Stage 5 — end-to-end validation + tuning

**Run:** synthetic Ghanaian taught-master's client (Ama Mensah, MSc Public Health, UK, full funding),
KB-only dry run, 2026-06-20. Artifacts in `clients/ama-mensah/`. Goal (per AGENT_SPEC §6 Stage 5):
run one client end-to-end, then tune freshness thresholds + the funding-vs-admission score weights.

## What worked (pipeline validated)
- **Contract + IO:** `client_profile.json` validates against the schema; outputs land in
  `clients/<name>/outputs/`; `pipeline_state` tracks progress (report left `in_progress` behind the gate).
- **Transcript:** `grade_map.py` correctly returns `GradeMapUnavailable` for "Ghana 4.0" → the skill
  applied the cited `grade-maps.md` Ghana table (3.55 → 2:1 ≈ US 3.3). The KB-reference-only decision
  works end-to-end.
- **Level gating:** `funded-position-finder` correctly **skipped** for a taught master's.
- **Timeline:** `next_feasible_intake(2026-06-20, fall)` correctly rolled to **Fall 2027** (Sep 2026
  too soon for the funded cycle); `backplan.py` produced a sensible backwards calendar.
- **Scholarships:** hard-gate-then-rank worked — Commonwealth **PhD** correctly eliminated (level +
  Ghana not on the LDC list); Chevening/Commonwealth/Mastercard/GREAT/GETFund ranked with honest,
  cited caveats (return-service bonds, partial vs full).
- **Approval gate:** report written as `report.draft.md`, not finalized.

## Findings → actions

### 1. Funding axis collapsed for UK taught master's  ✅ TUNED
UK universities don't fund international **taught** students, so `funds_internationals=False` for every
candidate → `funding_attainability = 0.05` → joint scores collapsed to 0.01–0.04 and the ranking
carried no funding information. But the client's funding is real and **portable** (Chevening/Commonwealth).
- **Action:** added `scholarship_route` to `score.py`'s `funding_attainability_from_flags` (→ 0.80 when
  the client realistically holds a portable award, overriding the school-funding collapse). Wired into
  `university-matching/SKILL.md` (set from `scholarship-matching`'s realistic shortlist). After tuning,
  the shortlist ranks meaningfully by admission odds (Leeds 0.60 → LSHTM 0.14). Smoke test asserts the lift.

### 2. Eligibility model is US-shaped  ⚠️ NOTED (no code change)
`classify.py` uses admit-rate + GPA percentile bands (US-undergrad style). UK PGT admissions are
**requirement-based** (meet the 2:1 threshold), so all four candidates came out "target" and the tier
sometimes disagreed with the probability (LSHTM: tier=target but p=0.17). The **probability** is the
more useful signal here than the reach/target/safety tier.
- **Recommendation (future):** add a requirement-based path to `classify.py` for UK PGT
  (meets / borderline / below the stated entry bar) instead of forcing percentile logic. Left as a
  documented limitation — not blocking.

### 3. Scholarship deadlines drive the timeline  ⚠️ NOTED
`backplan.py`'s generic "Apply for scholarships" lead time (24 wks) is far too late for
Chevening/Commonwealth, which close ~10–11 months pre-intake. The run overrode milestones to reflect
the real ~Nov-2026 deadline (correct), but the defaults could mislead.
- **Recommendation (future):** seed scholarship-deadline milestones from `kb/scholarships/*` in the
  default set, or have `timeline-planning` always override the scholarship lead time from KB (the
  SKILL already instructs overriding — reinforced here).

### 4. Freshness thresholds  ✅ REVIEWED — no change
Reviewed all `kb/*` thresholds: deadlines 90d, grades 365d, scholarships 365d, need-blind 365d
(+ "verify on page each cycle"), funded-position catalog 180d (listings never cached). All sound for
their volatility. Scholarship **dates** shift per cycle, but that's handled by the annual re-verify +
the timeline skill's always-live deadline check, not the threshold. No changes made.

## Net Stage-5 changes
- `score.py`: `scholarship_route` funding signal (+ smoke assertion).
- `university-matching/SKILL.md`: documents/uses `scholarship_route`.
- This findings doc; full sample client under `clients/ama-mensah/`.
- Items #2 and #3 logged as future enhancements (not blocking the pipeline).
