"""Deterministic backwards milestone planning for an application timeline.

Pure date math (Python datetime), no side effects. Given a target intake date and a set of milestones
each expressed as a lead time *before* the intake, produce a dated, chronologically-sorted calendar.
Also picks the next feasible intake when the client hasn't fixed one.

The milestone lead times the caller passes should come from the KB (UCAS/visa dates in
kb/uk/deadlines.md, WES/UK ENIC turnaround in kb/grading/grade-maps.md, etc.) — this script only does
the arithmetic so the calendar is reproducible and auditable.

Usage (CLI smoke test):
    python backplan.py            # runs a built-in demo
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Milestone:
    name: str
    weeks_before_intake: int      # lead time before the intake date
    note: str = ""


@dataclass
class DatedMilestone:
    name: str
    due: date
    note: str

    def as_dict(self) -> dict:
        return {"name": self.name, "due": self.due.isoformat(), "note": self.note}


# Default milestone set (lead times are sensible defaults; override per client/country from KB).
DEFAULT_MILESTONES = [
    Milestone("Sit English test (IELTS/TOEFL)", 40, "book early; scores valid ~2 yrs"),
    Milestone("Sit standardized test (GRE/SAT) if required", 38, "skip if test-optional/not required"),
    Milestone("Request official credential evaluation (WES/UK ENIC)", 34,
              "WES ~2-3 business days after docs; UK ENIC ~15 working days — see kb/grading/grade-maps.md"),
    Milestone("Draft & finalize documents (SOP/PS, CV, references)", 30, "give referees 3-4 weeks"),
    Milestone("Submit applications", 26, "by the program/UCAS deadline — see kb/*/deadlines.md"),
    Milestone("Apply for scholarships", 24, "many close before/with admission — see kb/scholarships/*"),
    Milestone("Decisions expected", 12, "varies by program"),
    Milestone("Accept offer & confirm funding", 10, ""),
    Milestone("Apply for student visa", 8,
              "UK: earliest 6 months before start; usually 3 weeks to decide — see kb/uk/deadlines.md"),
    Milestone("Arrange travel & accommodation", 2, ""),
]


def backplan(intake_date: date, milestones: list[Milestone] | None = None) -> list[DatedMilestone]:
    """Return milestones dated backwards from intake_date, sorted earliest-first."""
    ms = milestones if milestones is not None else DEFAULT_MILESTONES
    dated = [
        DatedMilestone(m.name, intake_date - timedelta(weeks=m.weeks_before_intake), m.note)
        for m in ms
    ]
    return sorted(dated, key=lambda d: d.due)


# Common intake months by term.
_TERM_MONTH = {"fall": 9, "autumn": 9, "spring": 1, "winter": 1, "summer": 6}


def next_feasible_intake(today: date, term: str = "fall", min_lead_months: int = 11) -> date:
    """Pick the next intake of `term` that is at least ~min_lead_months away.

    Default: next Fall if it's ≥10–12 months out, else the following year's cycle.
    """
    month = _TERM_MONTH.get(term.lower(), 9)
    candidate = date(today.year, month, 1)
    # require at least min_lead_months of runway
    while (candidate.year - today.year) * 12 + (candidate.month - today.month) < min_lead_months:
        candidate = date(candidate.year + 1, month, 1)
    return candidate


if __name__ == "__main__":
    import json

    intake = date(2027, 9, 20)  # passed in (no Date.now needed)
    cal = backplan(intake)
    print(f"Target intake: {intake.isoformat()}\n")
    print(json.dumps([d.as_dict() for d in cal], indent=2))

    # invariants
    dues = [d.due for d in cal]
    assert dues == sorted(dues), "calendar must be chronological"
    assert all(d.due < intake for d in cal), "all milestones precede intake"
    names = [d.name for d in cal]
    assert any("credential" in n.lower() for n in names), "credential-eval milestone present"
    assert any("visa" in n.lower() for n in names), "visa milestone present"

    today = date(2026, 6, 20)
    nf = next_feasible_intake(today, "fall")
    assert nf == date(2027, 9, 1), f"expected Fall 2027, got {nf}"  # Sep 2026 is <11mo out
    print(f"\nnext_feasible_intake(2026-06-20, fall) = {nf.isoformat()}")
    print("\nOK: chronological, buffers present, next-intake logic sane.")
