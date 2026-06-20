"""Tests for grade_map.py. Run: python test_grade_map.py  (no pytest dependency).

Covers representative conversions per grading system, boundary cases, the always-false
is_official invariant, and the GradeMapUnavailable contract for uncovered inputs.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grade_map import GradeMapUnavailable, canonical_system, map_grade  # noqa: E402


def check(label: str, cond: bool) -> None:
    if not cond:
        raise AssertionError(f"FAILED: {label}")
    print(f"  ok: {label}")


def expect_unavailable(label: str, system: str, grade: str) -> None:
    try:
        map_grade(system, grade)
    except GradeMapUnavailable:
        print(f"  ok: {label} (raised GradeMapUnavailable)")
        return
    raise AssertionError(f"FAILED: {label} should have raised GradeMapUnavailable")


def main() -> None:
    print("grade_map: Nigerian 5.0 CGPA")
    r = map_grade("Nigerian 5.0 CGPA", "4.52")
    check("4.52/5.0 -> First / 3.7", r.uk_band == "First" and r.us_gpa == "3.7")
    check("First Class is a planning estimate (is_official False)", r.is_official is False)
    check("3.50 is the 2:1 lower boundary", map_grade("Nigerian 5.0 CGPA", "3.50").uk_band == "2:1")
    check("3.49 falls to 2:2", map_grade("Nigerian 5.0 CGPA", "3.49").uk_band == "2:2")
    check("2.40 is the 2:2 lower boundary", map_grade("Nigerian 5.0 CGPA", "2.40").uk_band == "2:2")

    print("grade_map: UK honours")
    check("'First Class' -> First", map_grade("UK honours", "First Class").uk_band == "First")
    check("'2:1' -> 2:1", map_grade("UK honours", "2:1").uk_band == "2:1")
    check("'upper second' alias -> 2:1", map_grade("UK honours", "upper second").uk_band == "2:1")

    print("grade_map: US 4.0")
    check("3.8 GPA -> First band", map_grade("US 4.0", "3.8").uk_band == "First")
    check("3.0 GPA -> 2:2 band", map_grade("US 4.0", "3.0").uk_band == "2:2")

    print("grade_map: percentage")
    check("72% -> First", map_grade("percentage", "72%").uk_band == "First")
    check("55% -> 2:2", map_grade("percentage", "55%").uk_band == "2:2")

    print("grade_map: is_official is ALWAYS false")
    for sys_name, grade in [("Nigerian 5.0 CGPA", "4.9"), ("UK honours", "First"), ("US 4.0", "4.0"), ("percentage", "90")]:
        check(f"{sys_name} {grade}: is_official False", map_grade(sys_name, grade).is_official is False)

    print("grade_map: canonical_system aliasing")
    check("'Nigeria 5.0' canonicalizes to ng_5", canonical_system("Nigeria 5.0") == "ng_5")
    check("unknown system -> None", canonical_system("Klingon honours") is None)

    print("grade_map: GradeMapUnavailable contract")
    expect_unavailable("uncovered system (German 1.0)", "German 1.0 scale", "1.3")
    expect_unavailable("out-of-range Nigerian CGPA (6.0)", "Nigerian 5.0 CGPA", "6.0")
    expect_unavailable("unreadable UK class", "UK honours", "summa cum laude")

    print("\nALL grade_map TESTS PASSED")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
