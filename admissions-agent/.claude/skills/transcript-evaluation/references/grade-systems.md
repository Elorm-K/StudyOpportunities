# Grade systems reference

Per-system conversion detail for `transcript-evaluation`. The authoritative figures live in
`kb/grading/grade-maps.md` (sourced + dated). This file mirrors the bands that `scripts/grade_map.py`
encodes, so a reviewer can see what the script does without reading Python.

> **All conversions are planning estimates** — `is_official` is always `false`. An official WES (US)
> or UK ENIC evaluation is required for the actual application.

## Systems currently covered by grade_map.py

| System key | Accepts | Output |
|------------|---------|--------|
| `Nigerian 5.0 CGPA` | a 0.00–5.00 CGPA | class + UK band + US GPA |
| `UK honours` | First / 2:1 / 2:2 / Third | UK band + US GPA |
| `US 4.0` | a 0.00–4.00 GPA | UK band (approx) + US GPA |
| `percentage` | 0–100% (generic scale) | UK band + US GPA |

### Nigerian 5.0 CGPA → UK band → US GPA (estimate)
| CGPA (≥) | Class | UK band | US GPA |
|----------|-------|---------|--------|
| 4.50 | First Class | First | 3.7 |
| 3.50 | Second Class Upper | 2:1 | 3.3 |
| 2.40 | Second Class Lower | 2:2 | 2.7 |
| 1.50 | Third Class | Third | 2.0 |

### UK honours → US GPA (estimate)
| UK class | US GPA |
|----------|--------|
| First | 3.7 |
| 2:1 | 3.3 |
| 2:2 | 2.7 |
| Third | 2.0 |

### Percentage → UK band (generic estimate; verify per country)
| % (≥) | UK band | US GPA |
|-------|---------|--------|
| 70 | First | 3.7 |
| 60 | 2:1 | 3.3 |
| 50 | 2:2 | 2.7 |
| 40 | Third | 2.0 |

## In the KB but NOT encoded in grade_map.py (apply from grade-maps.md)

`kb/grading/grade-maps.md` holds **per-university** conversions for several systems that are **not**
encoded in `grade_map.py` (by decision — they're per-institution, not single national standards, and
the inverted Philippine 1.00–5.00 scale needs care). A client reporting these triggers
`GradeMapUnavailable` → **apply the cited table from `grade-maps.md` directly** (or
`knowledge-base-update` for the target university):
- 🟢 **Leading, verified:** **Ghana** (4.0 national classes) and **Bangladesh** (4.00 CGPA) — full
  cited tables in grade-maps.md. (Plus Philippines, Malaysia, Thailand — per-university, confirmed.)
- ⚪ **Background, on-demand:** Vietnam, Indonesia — not yet verified; do not assert.

> Note: Ghana + Bangladesh are leading countries but intentionally remain **KB-reference only** (not
> in `grade_map.py`) for now — so transcript-evaluation routes them through the grade-maps.md table.

## Not yet covered at all (trigger knowledge-base-update)

Any other system — German 1.0–5.0, Indian division/percentage, French 20-point, etc. When a client
presents one, `grade_map.py` raises `GradeMapUnavailable`; source the conversion via
`knowledge-base-update`, add it to `kb/grading/grade-maps.md`, then extend `grade_map.py`.

## Official credential evaluation (flag to the client)

| Application region | Service | See |
|--------------------|---------|-----|
| US | WES | `kb/grading/grade-maps.md` (cost + timeline) |
| UK | UK ENIC | `kb/grading/grade-maps.md` (cost + timeline) |
