"""Background job orchestration: launch the two phases as asyncio tasks, drive status
transitions, and resume in-flight runs after a restart.

In-process asyncio tasks (not RQ/Redis) — appropriate for a single-instance first test.
Crash-resumability lives in pipeline_state + status.json on the persistent volume: the boot
sweep relaunches Phase B for any client left mid-run (re-running done stages is a no-op per
CLAUDE.md routing).
"""

from __future__ import annotations

import asyncio
import logging

from lib import profile_io

from . import config, runner, state
from .client_store import get_lock

log = logging.getLogger("admissions.jobs")

# Keep strong refs so tasks aren't garbage-collected mid-flight.
_TASKS: set[asyncio.Task] = set()


def _spawn(coro) -> None:
    task = asyncio.create_task(coro)
    _TASKS.add(task)
    task.add_done_callback(_TASKS.discard)


def start_intake(slug: str) -> None:
    _spawn(_intake_flow(slug))


def start_research(slug: str) -> None:
    _spawn(_research_flow(slug))


async def _intake_flow(slug: str) -> None:
    async with get_lock(slug):
        state.write_status(slug, state.RUNNING_INTAKE, message="Reviewing your answers…")
        try:
            cost = await runner.run_intake(slug)
        except Exception as exc:  # noqa: BLE001
            log.exception("intake failed for %s", slug)
            state.write_status(slug, state.ERROR, error=str(exc)[:500], message="Something went wrong during review.")
            return

        questions = state.read_questions(slug)
        if state.questions_valid(questions):
            intro = (questions or {}).get("intro") or "A couple of quick questions to sharpen your search."
            state.write_status(slug, state.AWAITING_ANSWERS, message=intro, cost_usd=cost)
            return
        # No (valid) questions -> record intake cost, then chain straight into research.
        state.write_status(slug, state.RUNNING_INTAKE, message="Starting your research…", cost_usd=cost)

    # Released the lock; chain Phase B as its own task so it re-acquires cleanly.
    start_research(slug)


async def _research_flow(slug: str) -> None:
    async with get_lock(slug):
        state.write_status(slug, state.RUNNING_RESEARCH, message="Researching universities, scholarships, and a plan for you…")
        try:
            cost = await runner.run_research(slug)
        except Exception as exc:  # noqa: BLE001
            log.exception("research failed for %s", slug)
            state.write_status(slug, state.ERROR, error=str(exc)[:500], message="Something went wrong during research.")
            return

        if config.APPROVAL_REQUIRED:
            if config.draft_report_path(slug).exists() and not config.final_report_path(slug).exists():
                state.write_status(slug, state.AWAITING_APPROVAL, message="Your report is being reviewed before release.", cost_usd=cost)
            elif config.final_report_path(slug).exists():
                state.write_status(slug, state.DONE, message="Your report is ready.", cost_usd=cost)
            else:
                state.write_status(slug, state.ERROR, error="No draft report was produced.", message="Research finished but no report was produced.", cost_usd=cost)
        else:
            if config.final_report_path(slug).exists():
                state.write_status(slug, state.DONE, message="Your report is ready.", cost_usd=cost)
            else:
                state.write_status(slug, state.ERROR, error="No final report was produced.", message="Research finished but no report was produced.", cost_usd=cost)


def resume_sweep() -> None:
    """On boot, relaunch any client left mid-run. Safe: done stages are not redone."""
    if not config.CLIENTS_DIR.exists():
        return
    for child in config.CLIENTS_DIR.iterdir():
        if not child.is_dir() or child.name == "_template":
            continue
        slug = child.name
        st = state.read_status(slug)
        if not st:
            continue
        s = st.get("state")
        if s == state.RUNNING_INTAKE:
            log.info("resuming intake for %s", slug)
            start_intake(slug)
        elif s == state.RUNNING_RESEARCH:
            log.info("resuming research for %s", slug)
            start_research(slug)


def promote_report(slug: str) -> None:
    """Operator approval: deterministically promote draft -> final and mark done.

    Pure file copy + a profile flag flip — never a model re-invocation — so the gate
    cannot be spoofed by model output. report.md does not exist until this runs.
    """
    draft = config.draft_report_path(slug)
    final = config.final_report_path(slug)
    if not draft.exists():
        raise FileNotFoundError("no draft report to approve")
    final.write_text(draft.read_text(encoding="utf-8"), encoding="utf-8")
    try:
        profile = profile_io.load_profile(config.profile_path(slug))
        profile["pipeline_state"]["report"] = "done"
        profile_io.save_profile(config.profile_path(slug), profile)
    except Exception:  # noqa: BLE001 - report is already finalized; flag flip is best-effort
        log.exception("could not flip pipeline_state.report for %s", slug)
    state.write_status(slug, state.DONE, message="Your report is ready.")
