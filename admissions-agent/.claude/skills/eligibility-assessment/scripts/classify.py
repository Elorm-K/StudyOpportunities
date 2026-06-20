"""Deterministic admission classification: reach / target / safety + admission probability.

Pure functions, no side effects (same style as score.py / grade_map.py). Classifies how a client
stands against a candidate school using the school's admit rate and its applicant stat distribution
(25th / 50th / 75th percentiles of GPA or test score). Produces an `admission_probability` in 0..1
that `university-matching/scripts/score.py` consumes as its admission axis.

Everything here is a PLANNING ESTIMATE — admit rates and percentile bands must be cited from the KB
(or refreshed via knowledge-base-update); this script only turns those numbers into a tier + score.

Usage (CLI smoke test):
    python classify.py            # runs a built-in demo
    python classify.py 0.06 3.9 3.7 3.9 4.0   # admit_rate applicant p25 p50 p75
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

# Tunable thresholds (documented so the classification is auditable).
REACH_ADMIT_RATE = 0.15      # below this admit rate, a school is a reach regardless of fit
SAFETY_ADMIT_RATE = 0.40     # a safety also needs a reasonably high admit rate
PROB_FLOOR = 0.02            # never report 0 or 1 — these are estimates
PROB_CEIL = 0.95


@dataclass
class Eligibility:
    tier: str                 # "reach" | "target" | "safety"
    admission_probability: float
    rationale: str

    def as_dict(self) -> dict:
        return {
            "tier": self.tier,
            "admission_probability": round(self.admission_probability, 3),
            "rationale": self.rationale,
        }


def _clamp(x: float, lo: float = PROB_FLOOR, hi: float = PROB_CEIL) -> float:
    return max(lo, min(hi, x))


def classify(admit_rate: float, applicant_stat: float, p25: float, p50: float, p75: float) -> Eligibility:
    """Classify a candidate school for this applicant and estimate admission probability.

    Args:
        admit_rate: school's overall admit rate, 0..1.
        applicant_stat: the client's comparable stat (e.g. GPA or test score), same scale as p25/p50/p75.
        p25, p50, p75: the school's admitted/applicant distribution for that stat.

    Tiers (per spec §5.3):
        reach  — admit_rate < 0.15 OR applicant below the 25th percentile
        safety — applicant above the 75th percentile AND a high admit rate
        target — otherwise (applicant within the middle 50%)
    """
    if not (p25 <= p50 <= p75):
        raise ValueError(f"percentiles must be ordered p25<=p50<=p75, got {p25},{p50},{p75}")

    below_p25 = applicant_stat < p25
    above_p75 = applicant_stat > p75

    # --- tier ---
    if admit_rate < REACH_ADMIT_RATE or below_p25:
        tier = "reach"
    elif above_p75 and admit_rate >= SAFETY_ADMIT_RATE:
        tier = "safety"
    else:
        tier = "target"

    # --- admission probability ---
    # Anchor on admit_rate, then nudge by where the applicant sits in the band.
    # fit in [-1, +1]: -1 = at/below p25, 0 = at p50, +1 = at/above p75.
    if applicant_stat <= p50:
        denom = (p50 - p25) or 1.0
        fit = max(-1.0, (applicant_stat - p50) / denom)
    else:
        denom = (p75 - p50) or 1.0
        fit = min(1.0, (applicant_stat - p50) / denom)

    # A strong-fit applicant beats the base admit rate; a weak-fit one trails it.
    # Scale the nudge by headroom so it stays in 0..1.
    if fit >= 0:
        prob = admit_rate + fit * (1.0 - admit_rate) * 0.6
    else:
        prob = admit_rate + fit * admit_rate * 0.6
    prob = _clamp(prob)

    rationale = (
        f"admit_rate={admit_rate:.0%}, applicant {applicant_stat} vs band "
        f"[{p25}/{p50}/{p75}] (fit={fit:+.2f}) → {tier}. Planning estimate."
    )
    return Eligibility(tier=tier, admission_probability=prob, rationale=rationale)


if __name__ == "__main__":
    import json

    if len(sys.argv) == 6:
        ar, app, a, b, c = (float(x) for x in sys.argv[1:])
        print(json.dumps(classify(ar, app, a, b, c).as_dict(), indent=2))
        raise SystemExit(0)

    # Demo: GPA on a 4.0 scale.
    demos = [
        ("Elite (6% admit), applicant at median", classify(0.06, 3.9, 3.85, 3.95, 4.0)),
        ("Mid (35% admit), applicant in band", classify(0.35, 3.4, 3.2, 3.5, 3.8)),
        ("Accessible (70% admit), applicant above p75", classify(0.70, 3.9, 3.0, 3.3, 3.6)),
        ("Mid (35% admit), applicant below p25", classify(0.35, 2.9, 3.2, 3.5, 3.8)),
    ]
    for label, e in demos:
        print(f"\n{label}")
        print(json.dumps(e.as_dict(), indent=2))

    # invariants
    assert demos[0][1].tier == "reach", "elite low-admit → reach"
    assert demos[1][1].tier == "target", "mid in-band → target"
    assert demos[2][1].tier == "safety", "high-admit above-p75 → safety"
    assert demos[3][1].tier == "reach", "below p25 → reach"
    assert all(0.0 <= d[1].admission_probability <= 1.0 for d in demos)
    print("\nOK: tiers + admission_probability in [0,1] as expected.")
