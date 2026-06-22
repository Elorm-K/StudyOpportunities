"""Background job orchestration: launch the two phases on a worker thread pool, drive
status transitions, and resume in-flight runs after a restart.

Each phase runs in its OWN thread with its OWN event loop (via ``asyncio.run``), never on
uvicorn's request loop. The Claude Agent SDK's ``query()`` does enough synchronous/CPU work
between awaits (message parsing, session-store I/O, subprocess calls) that running it on the
HTTP event loop starves request handling — the submit POST or the status polls hang for the
whole multi-minute run. Off-loop worker threads keep the server responsive.

In-process threads (not RQ/Redis) — appropriate for a single-instance first test.
Crash-resumability lives in pipeline_state + status.json on the persistent volume: the boot
sweep relaunches Phase B for any client left mid-run (re-running done stages is a no-op per
CLAUDE.md routing).
"""

from __future__ import annotations

import asyncio
import logging
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Coroutine

from lib import profile_io

from . import config, runner, state
from .client_store import get_lock

log = logging.getLogger("admissions.jobs")

# A bounded pool of worker threads, each running one agent phase to completion in its own
# event loop. Capacity caps concurrent in-flight clients (the SDK runs are expensive).
_POOL = ThreadPoolExecutor(max_workers=config.MAX_CONCURRENT_RUNS, thread_name_prefix="agent")
# Keep strong refs so Futures aren't garbage-collected mid-flight.
_FUTURES: set[Future] = set()


def _spawn(coro_fn: Callable[[], Coroutine[Any, Any, None]], label: str) -> None:
    """Run an async job flow to completion on a worker thread (its own event loop)."""

    def _runner() -> None:
        asyncio.run(coro_fn())

    fut = _POOL.submit(_runner)
    _FUTURES.add(fut)

    def _done(f: Future) -> None:
        _FUTURES.discard(f)
        exc = f.exception()
        if exc is not None:  # a crash before the flow's own try/except could otherwise vanish
            log.error("job %s crashed: %r", label, exc)

    fut.add_done_callback(_done)


def start_intake(slug: str) -> None:
    _spawn(lambda: _intake_flow(slug), f"intake:{slug}")


def start_research(slug: str) -> None:
    _spawn(lambda: _research_flow(slug), f"research:{slug}")


async def _intake_flow(slug: str) -> None:
    log.info("intake start: %s", slug)
    with get_lock(slug):
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
            log.info("intake done (awaiting answers): %s", slug)
            return
        # No (valid) questions -> record intake cost, then chain straight into research.
        state.write_status(slug, state.RUNNING_INTAKE, message="Starting your research…", cost_usd=cost)

    # Released the lock; chain Phase B as its own job so it re-acquires cleanly.
    log.info("intake done (chaining research): %s", slug)
    start_research(slug)


async def _research_flow(slug: str) -> None:
    log.info("research start: %s", slug)
    with get_lock(slug):
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
    log.info("research done: %s ($%.4f)", slug, cost)


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
