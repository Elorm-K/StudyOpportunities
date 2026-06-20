"""Tests for score.py. Run: python test_score.py  (no pytest dependency).

Covers the funding-attainability flag logic, the joint-score ordering invariant (a fully-funded
harder school outranks an easy-admit school that won't fund internationals), the need-blind boost,
and rank_per_country grouping/capping.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from score import (  # noqa: E402
    Candidate,
    funding_attainability_from_flags,
    joint_score,
    rank,
    rank_per_country,
)


def check(label: str, cond: bool) -> None:
    if not cond:
        raise AssertionError(f"FAILED: {label}")
    print(f"  ok: {label}")


def main() -> None:
    print("score: funding_attainability_from_flags")
    wont_fund = funding_attainability_from_flags(funds_internationals=False)
    check("won't-fund-internationals collapses to ~0", wont_fund <= 0.05)
    base = funding_attainability_from_flags()
    check("need-blind boosts above base", funding_attainability_from_flags(need_blind_for_intl=True) > base)
    check("need-blind + full-need is strong", funding_attainability_from_flags(need_blind_for_intl=True, meets_full_need_for_intl=True) >= 0.9)
    check("fully-funded route boosts above base", funding_attainability_from_flags(fully_funded_route=True) > base)
    check("scores clamp to <= 1.0", funding_attainability_from_flags(need_blind_for_intl=True, meets_full_need_for_intl=True, fully_funded_route=True) <= 1.0)

    print("score: joint_score")
    check("joint is the product", abs(joint_score(0.5, 0.4) - 0.2) < 1e-9)
    check("joint clamps out-of-range inputs", joint_score(2.0, 2.0) == 1.0)

    print("score: ordering invariant (THE core rule)")
    easy_no_fund = Candidate("Easy U", "US", 0.85, funding_attainability_from_flags(funds_internationals=False))
    hard_full_need = Candidate("Hard U", "US", 0.18, funding_attainability_from_flags(need_blind_for_intl=True, meets_full_need_for_intl=True))
    mid_funded = Candidate("Mid U", "US", 0.45, funding_attainability_from_flags(fully_funded_route=True))
    ranked = rank([easy_no_fund, hard_full_need, mid_funded])
    check("won't-fund-internationals school ranks LAST", ranked[-1].name == "Easy U")
    check("a harder fully-needs-met school outranks the easy no-fund school",
          next(s for s in ranked if s.name == "Hard U").joint_score > next(s for s in ranked if s.name == "Easy U").joint_score)
    check("ranked output is sorted descending by joint score",
          all(ranked[i].joint_score >= ranked[i + 1].joint_score for i in range(len(ranked) - 1)))

    print("score: rank_per_country grouping + cap")
    candidates = [
        Candidate("US-A", "US", 0.6, 0.6), Candidate("US-B", "US", 0.5, 0.5), Candidate("US-C", "US", 0.4, 0.4),
        Candidate("UK-A", "UK", 0.7, 0.7), Candidate("UK-B", "UK", 0.3, 0.3),
    ]
    per = rank_per_country(candidates, per_country=2)
    check("groups by country", set(per.keys()) == {"US", "UK"})
    check("caps each country at per_country=2", len(per["US"]) == 2 and len(per["UK"]) == 2)
    check("keeps the top US candidates", {s.name for s in per["US"]} == {"US-A", "US-B"})

    print("\nALL score TESTS PASSED")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
