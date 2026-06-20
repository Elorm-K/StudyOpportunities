---
name: timeline-planning
description: Use when building a client's application milestone calendar. Backwards-plans from the target intake through testing, documents, credential evaluation, deadlines, funding, and visa buffers.
---

# Timeline planning

Produce a **dated milestone calendar** by backwards-planning from the client's target intake. Anchor
the real deadlines to the KB (cite them), then let `scripts/backplan.py` do the date arithmetic so the
calendar is reproducible.

## Inputs

- `client_profile.json` (via `lib/profile_io.py`): `targets.intake`, `targets.countries`,
  `targets.degree_level`, plus `tests` and `academics` (to know whether testing / credential-eval
  milestones apply).
- KB deadlines: **`kb/uk/deadlines.md`** (UCAS UG dates + UK visa lead time are verified);
  `kb/us/deadlines.md` and UK PGT/PGR are **deferred** → trigger `knowledge-base-update` for the
  client's specific program/cycle. Credential-eval turnaround (WES / UK ENIC) from
  `kb/grading/grade-maps.md`.

## Process

1. **Fix the intake.** Use `targets.intake` if set. Otherwise call
   `backplan.next_feasible_intake(today, term)` — default next **Fall** if it's ≥10–12 months out,
   else the following cycle. State the assumption to the client.

2. **Pull the real deadlines (cite them).** Branch on country × level and read the binding dates from
   the KB:
   - UK UG → UCAS equal-consideration / Oxbridge+med / Clearing (verified in `kb/uk/deadlines.md`).
   - UK PGT/PGR, US UG/grad → deferred; refresh via `knowledge-base-update` for the specific program.
   - Visa buffer (UK: apply up to 6 months ahead, ~3 weeks to decide) and credential-eval turnaround.

3. **Build the milestone set.** Convert each deadline/buffer into a `Milestone(name,
   weeks_before_intake, note)`. Override `backplan.py`'s defaults so "Submit applications" lands on the
   *actual* program deadline (e.g. UCAS 14 Jan, not the generic default), and drop milestones that
   don't apply (no GRE if not required; no credential eval if not needed yet).

4. **Compute the calendar.** Run `backplan(intake_date, milestones)` → a chronologically-sorted dated
   list. Sanity-check that nothing falls in the past relative to today; if the next feasible intake is
   too soon to hit a deadline, roll to the following cycle and say so.

5. **Write the output.** Save `clients/<name>/outputs/timeline.md` (dated calendar + the cited
   deadlines it's built from). Set `pipeline_state.timeline = "done"`.

## Output

- `clients/<name>/outputs/timeline.md` — dated milestone calendar with cited source deadlines.
- `pipeline_state.timeline = "done"`.

## Why a script

Backwards date math from an intake across many milestones is mechanical and error-prone by hand.
`backplan.py` keeps it deterministic and auditable; the skill's judgement is in *which* milestones and
*what* lead times (from the KB), not the arithmetic.

## Guardrails (see ../../../CLAUDE.md)

- Cite every deadline with its source + `last_verified`; refresh deferred/stale KB before using it.
- Build in realistic buffers (credential eval, visa) — don't present a timeline that can't actually be
  met; if the intake is infeasible, recommend the next cycle.
