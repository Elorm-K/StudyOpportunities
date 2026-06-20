"""Deterministic ranking for discovered funded positions.

Pure functions, no side effects (same style as score.py / classify.py). Ranks shortlisted positions
by a weighted blend of the four axes from the spec's ranking rubric:

    funding_certainty (for INTERNATIONALS) × recency × interest/PI fit × deadline feasibility

The dominant axis is funding certainty *for this client's nationality* — a "fully funded" post that
won't fund internationals scores near zero, mirroring how university-matching's score.py collapses the
admit-but-won't-fund case. Inputs are 0..1; helpers derive recency/deadline from day counts.

Usage (CLI smoke test):  python rank.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Weights (sum to 1.0). Funding certainty dominates — it's the whole point, and the intl caveat is
# where most "fully funded" listings fail.
W_FUNDING = 0.40
W_FIT = 0.25
W_RECENCY = 0.20
W_DEADLINE = 0.15


@dataclass
class Position:
    label: str                  # "PI / position @ institution"
    funding_certainty: float    # 0..1 — confidence it funds THIS client's nationality
    fit: float                  # 0..1 — interest / PI / topic match
    recency: float              # 0..1 — how fresh the posting is
    deadline_feasibility: float # 0..1 — enough lead time to apply well
    meta: dict = field(default_factory=dict)


@dataclass
class RankedPosition:
    label: str
    score: float
    funding_certainty: float
    fit: float
    recency: float
    deadline_feasibility: float

    def as_dict(self) -> dict:
        return {
            "label": self.label,
            "score": round(self.score, 3),
            "funding_certainty": round(self.funding_certainty, 3),
            "fit": round(self.fit, 3),
            "recency": round(self.recency, 3),
            "deadline_feasibility": round(self.deadline_feasibility, 3),
        }


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def recency_from_days(days_since_posted: float) -> float:
    """Map age to a 0..1 recency score. Spec keeps only the last 1–3 months; older drops off fast."""
    if days_since_posted <= 30:
        return 1.0
    if days_since_posted <= 60:
        return 0.7
    if days_since_posted <= 90:
        return 0.4
    return 0.1  # >3 months — should usually be filtered out before ranking


def deadline_feasibility_from_days(days_until_deadline: float, min_days_to_apply: int = 21) -> float:
    """More lead time → more feasible. Past deadline = 0; very tight = low; comfortable = high."""
    if days_until_deadline < 0:
        return 0.0
    if days_until_deadline < min_days_to_apply:
        return _clamp01(days_until_deadline / min_days_to_apply * 0.5)
    if days_until_deadline <= 90:
        return 1.0
    # very far out is fine but slightly discount (priorities may shift / posting may change)
    return 0.85


def score_position(p: Position) -> RankedPosition:
    s = (
        W_FUNDING * _clamp01(p.funding_certainty)
        + W_FIT * _clamp01(p.fit)
        + W_RECENCY * _clamp01(p.recency)
        + W_DEADLINE * _clamp01(p.deadline_feasibility)
    )
    return RankedPosition(p.label, s, p.funding_certainty, p.fit, p.recency, p.deadline_feasibility)


def rank(positions: list[Position]) -> list[RankedPosition]:
    """Score and sort positions by weighted score, descending."""
    return sorted((score_position(p) for p in positions), key=lambda r: r.score, reverse=True)


if __name__ == "__main__":
    import json

    demo = [
        Position("Prof A RA @ US (funds intl, fresh, great fit)",
                 funding_certainty=0.95, fit=0.9,
                 recency=recency_from_days(10), deadline_feasibility=deadline_feasibility_from_days(45)),
        Position("Prof B PhD @ UK ('fully funded' but home-only)",
                 funding_certainty=0.10, fit=0.9,
                 recency=recency_from_days(5), deadline_feasibility=deadline_feasibility_from_days(60)),
        Position("Prof C PhD @ EU (funds intl, ok fit, older)",
                 funding_certainty=0.8, fit=0.55,
                 recency=recency_from_days(75), deadline_feasibility=deadline_feasibility_from_days(120)),
    ]
    ranked = rank(demo)
    print(json.dumps([r.as_dict() for r in ranked], indent=2))
    assert ranked[-1].label.startswith("Prof B"), "home-only funding must rank last despite great fit"
    assert ranked[0].label.startswith("Prof A"), "funds-intl + fresh + good-fit ranks first"
    assert all(0.0 <= r.score <= 1.0 for r in ranked)
    print("\nOK: funds-international beats 'fully funded but home-only' even with equal fit.")
