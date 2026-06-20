"""Deterministic grade conversion: confirmed grade -> UK band + US GPA.

Pure functions, no side effects. Conversions are table lookups so results are reproducible and
auditable. Every result is a PLANNING ESTIMATE — ``is_official`` is always False. Callers must
trigger ``knowledge-base-update`` when a system/grade is not covered here, rather than guessing.

The tables below are seeded with commonly-used conversion bands as a starting point. They are
ESTIMATES pending verification against ``kb/grading/grade-maps.md`` (which is sourced from the
research reports + authoritative providers). When the KB is seeded, reconcile these tables with it.

Usage (CLI smoke test):
    python grade_map.py "Nigerian 5.0 CGPA" "4.52"
    python grade_map.py "UK honours" "First Class"
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field


@dataclass
class GradeMapResult:
    uk_band: str
    us_gpa: str
    is_official: bool = False  # ALWAYS False — planning estimate, not a credential evaluation
    source: str = "grade_map.py table lookup"
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "uk_band": self.uk_band,
            "us_gpa": self.us_gpa,
            "is_official": self.is_official,
            "source": self.source,
            "notes": self.notes,
        }


class GradeMapUnavailable(Exception):
    """Raised when the system/grade is not covered. Caller should trigger knowledge-base-update."""


# --- Normalization -------------------------------------------------------------------------------

def _norm(text: str) -> str:
    """Lowercase, strip accents/punctuation noise, collapse whitespace."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", text.strip().lower())


# Aliases -> canonical grading-system key.
_SYSTEM_ALIASES = {
    "nigerian 5.0 cgpa": "ng_5",
    "nigeria 5.0": "ng_5",
    "nigerian cgpa": "ng_5",
    "5.0 cgpa": "ng_5",
    "uk honours": "uk_honours",
    "uk honors": "uk_honours",
    "british honours": "uk_honours",
    "us 4.0": "us_4",
    "us gpa": "us_4",
    "4.0 gpa": "us_4",
    "4.0 scale": "us_4",
    "percentage": "percentage",
    "percent": "percentage",
}


def canonical_system(grading_system: str) -> str | None:
    key = _norm(grading_system)
    if key in _SYSTEM_ALIASES:
        return _SYSTEM_ALIASES[key]
    # loose contains-match for free-text answers
    for alias, canon in _SYSTEM_ALIASES.items():
        if alias in key:
            return canon
    return None


# --- Conversion tables (ESTIMATES — reconcile with kb/grading/grade-maps.md) ----------------------

# Nigerian 5.0 CGPA -> class -> (UK band, US GPA). Ranges are inclusive of the lower bound.
_NG_5_BANDS = [
    (4.50, "First Class", "First", "3.7"),
    (3.50, "Second Class Upper (2:1)", "2:1", "3.3"),
    (2.40, "Second Class Lower (2:2)", "2:2", "2.7"),
    (1.50, "Third Class", "Third", "2.0"),
    (0.00, "Pass", "Pass / below honours", "1.0"),
]

# UK honours class -> (UK band label, US GPA).
_UK_HONOURS = {
    "first": ("First", "3.7"),
    "first class": ("First", "3.7"),
    "1st": ("First", "3.7"),
    "2:1": ("2:1", "3.3"),
    "upper second": ("2:1", "3.3"),
    "second class upper": ("2:1", "3.3"),
    "2:2": ("2:2", "2.7"),
    "lower second": ("2:2", "2.7"),
    "second class lower": ("2:2", "2.7"),
    "third": ("Third", "2.0"),
    "third class": ("Third", "2.0"),
}

# Percentage -> (UK band, US GPA). Generic; many countries differ — verify per system in KB.
_PERCENTAGE_BANDS = [
    (70.0, "First", "3.7"),
    (60.0, "2:1", "3.3"),
    (50.0, "2:2", "2.7"),
    (40.0, "Third", "2.0"),
    (0.0, "Below honours", "1.0"),
]


def _first_number(raw: str) -> float | None:
    m = re.search(r"\d+(?:\.\d+)?", raw)
    return float(m.group()) if m else None


# --- Public API ----------------------------------------------------------------------------------

def map_grade(grading_system: str, raw_grade: str) -> GradeMapResult:
    """Map a confirmed grade to a UK band + US GPA planning estimate.

    Raises GradeMapUnavailable if the system or grade is not covered — the caller should then
    trigger knowledge-base-update and retry rather than guessing.
    """
    system = canonical_system(grading_system)
    if system is None:
        raise GradeMapUnavailable(
            f"Grading system not covered: {grading_system!r}. Trigger knowledge-base-update."
        )

    estimate_note = "Planning estimate only — not an official WES/UK ENIC evaluation."

    if system == "ng_5":
        cgpa = _first_number(raw_grade)
        if cgpa is None or cgpa > 5.0:
            raise GradeMapUnavailable(f"Could not read a 5.0-scale CGPA from {raw_grade!r}.")
        for threshold, klass, uk, gpa in _NG_5_BANDS:
            if cgpa >= threshold:
                return GradeMapResult(uk, gpa, notes=[f"Nigerian {cgpa}/5.0 ≈ {klass}.", estimate_note])

    if system == "uk_honours":
        key = _norm(raw_grade)
        for alias, (uk, gpa) in _UK_HONOURS.items():
            if alias in key:
                return GradeMapResult(uk, gpa, notes=[estimate_note])
        raise GradeMapUnavailable(f"Unrecognized UK honours class: {raw_grade!r}.")

    if system == "us_4":
        gpa = _first_number(raw_grade)
        if gpa is None or gpa > 4.0:
            raise GradeMapUnavailable(f"Could not read a 4.0-scale GPA from {raw_grade!r}.")
        # Approximate the UK band from the US GPA.
        if gpa >= 3.7:
            uk = "First"
        elif gpa >= 3.3:
            uk = "2:1"
        elif gpa >= 2.7:
            uk = "2:2"
        else:
            uk = "Third"
        return GradeMapResult(uk, f"{gpa:.2f}".rstrip("0").rstrip("."), notes=[estimate_note])

    if system == "percentage":
        pct = _first_number(raw_grade)
        if pct is None or pct > 100.0:
            raise GradeMapUnavailable(f"Could not read a percentage from {raw_grade!r}.")
        for threshold, uk, gpa in _PERCENTAGE_BANDS:
            if pct >= threshold:
                return GradeMapResult(
                    uk, gpa,
                    notes=[
                        f"{pct}% mapped on a generic UK scale.",
                        "Percentage scales vary by country — verify in kb/grading/grade-maps.md.",
                        estimate_note,
                    ],
                )

    raise GradeMapUnavailable(f"No mapping path for system {system!r}.")  # pragma: no cover


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python grade_map.py "<grading system>" "<raw grade>"', file=sys.stderr)
        raise SystemExit(2)
    try:
        result = map_grade(sys.argv[1], sys.argv[2])
    except GradeMapUnavailable as exc:
        print(f"UNAVAILABLE: {exc}", file=sys.stderr)
        raise SystemExit(1)
    import json
    print(json.dumps(result.as_dict(), indent=2))
