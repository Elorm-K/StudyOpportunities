# Ranking rubric

How to score shortlisted positions. The deterministic weighting lives in `scripts/rank.py`; this
explains the four axes so a reviewer understands the numbers without reading Python.

## Axes (each 0..1)

| Axis | Weight | What it measures | How to set it |
|------|--------|------------------|---------------|
| **funding_certainty** (for internationals) | **0.40** | Confidence the position funds **this client's nationality** in full | 1.0 = explicit full funding open to internationals (confirmed on source); ~0.5 = funded but intl-eligibility unclear; ~0.1 = "fully funded" but home-only / UK fee-gap unresolved |
| **fit** | 0.25 | Interest / PI / topic match to `targets.research_interests` | 1.0 = direct subfield + admired-PI match; lower as it drifts from the stated interest |
| **recency** | 0.20 | How fresh the posting is | `recency_from_days()`: ≤30d→1.0, ≤60→0.7, ≤90→0.4, older→0.1 (usually filtered out) |
| **deadline_feasibility** | 0.15 | Enough lead time to apply well | `deadline_feasibility_from_days()`: past→0, tight(<21d)→low, 21–90d→1.0, far→0.85 |

`score = 0.40·funding + 0.25·fit + 0.20·recency + 0.15·deadline` (all clamped 0..1).

## Why funding dominates
The point of this skill is **funded** positions for **internationals**. A perfect-fit, just-posted PhD
that won't fund the client is not a real option — so `funding_certainty` is weighted highest and a
home-only post scores near the bottom even with great fit/recency (mirrors `university-matching`'s
funding-aware joint score).

## Use
After filtering to {funded-for-nationality · eligible · recent · interest-matched}, set the four axes
per position (use the day-count helpers for recency/deadline), run `rank.py`, and present highest-score
first with the per-axis breakdown so the operator sees *why* each ranks where it does.
