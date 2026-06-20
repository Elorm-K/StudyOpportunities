"""Joint university scorer: admission probability x funding attainability.

Pure functions, no side effects. The core rule from the spec: rank by the JOINT score, not admission
odds alone. A school that admits the client but won't fund internationals should rank BELOW a harder
school that funds fully.

Inputs per candidate are normalized 0..1:
  - admission_probability: chance this client is admitted (from eligibility-assessment).
  - funding_attainability: chance this client secures the funding they need at this school.

funding_attainability can be supplied directly, or derived from flags via funding_attainability_from_flags():
  - need_blind_for_intl / meets_full_need_for_intl (US): strong up-rank (verify on the school page).
  - funds_internationals: if False, hard down-rank — the "admits but won't fund" case.
  - fully_funded_route: e.g. funded PhD assistantship — strong up-rank.

Usage (CLI smoke test): python score.py   (runs a built-in demo)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Candidate:
    name: str
    country: str
    admission_probability: float          # 0..1
    funding_attainability: float          # 0..1
    reasoning: str = ""
    flags: dict = field(default_factory=dict)


@dataclass
class ScoredCandidate:
    name: str
    country: str
    admission_probability: float
    funding_attainability: float
    joint_score: float
    reasoning: str

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "country": self.country,
            "admission_probability": round(self.admission_probability, 3),
            "funding_attainability": round(self.funding_attainability, 3),
            "joint_score": round(self.joint_score, 3),
            "reasoning": self.reasoning,
        }


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def funding_attainability_from_flags(
    *,
    funds_internationals: bool = True,
    need_blind_for_intl: bool = False,
    meets_full_need_for_intl: bool = False,
    fully_funded_route: bool = False,
    base: float = 0.5,
) -> float:
    """Derive a 0..1 funding-attainability estimate from boolean signals.

    The "admits but won't fund internationals" case collapses toward 0, which is the whole point of
    scoring on the joint metric.
    """
    if not funds_internationals:
        return 0.05  # hard down-rank: admission is moot if they won't fund this client
    score = base
    if need_blind_for_intl:
        score += 0.2
    if meets_full_need_for_intl:
        score += 0.25
    if fully_funded_route:
        score += 0.25
    return _clamp01(score)


def joint_score(admission_probability: float, funding_attainability: float) -> float:
    """The joint metric: product of the two normalized probabilities."""
    return _clamp01(admission_probability) * _clamp01(funding_attainability)


def score_candidate(c: Candidate) -> ScoredCandidate:
    js = joint_score(c.admission_probability, c.funding_attainability)
    return ScoredCandidate(
        name=c.name,
        country=c.country,
        admission_probability=_clamp01(c.admission_probability),
        funding_attainability=_clamp01(c.funding_attainability),
        joint_score=js,
        reasoning=c.reasoning,
    )


def rank(candidates: list[Candidate]) -> list[ScoredCandidate]:
    """Score and sort candidates by joint score, descending."""
    return sorted(
        (score_candidate(c) for c in candidates),
        key=lambda s: s.joint_score,
        reverse=True,
    )


def rank_per_country(candidates: list[Candidate], per_country: int = 7) -> dict[str, list[ScoredCandidate]]:
    """Return the top `per_country` (default 6–7) ranked candidates for each country."""
    by_country: dict[str, list[Candidate]] = {}
    for c in candidates:
        by_country.setdefault(c.country, []).append(c)
    return {country: rank(group)[:per_country] for country, group in by_country.items()}


if __name__ == "__main__":
    import json

    # Demo: an easy-to-enter school that won't fund internationals should rank BELOW a hard,
    # fully-funding school.
    demo = [
        Candidate(
            "Easy U (won't fund intl)", "US",
            admission_probability=0.85,
            funding_attainability=funding_attainability_from_flags(funds_internationals=False),
            reasoning="High admit odds but no funding for internationals.",
        ),
        Candidate(
            "Hard U (need-blind, full need)", "US",
            admission_probability=0.18,
            funding_attainability=funding_attainability_from_flags(
                need_blind_for_intl=True, meets_full_need_for_intl=True),
            reasoning="Low admit odds but need-blind + meets full need for internationals.",
        ),
        Candidate(
            "Mid U (funded PhD route)", "US",
            admission_probability=0.45,
            funding_attainability=funding_attainability_from_flags(fully_funded_route=True),
            reasoning="Moderate odds, fully-funded assistantship available.",
        ),
    ]
    ranked = rank(demo)
    print(json.dumps([s.as_dict() for s in ranked], indent=2))
    assert ranked[-1].name == "Easy U (won't fund intl)", "won't-fund school must rank last"
    print("\nOK: joint scoring down-ranks the admit-but-won't-fund-internationals school.")
