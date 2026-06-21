"""Status + questions state: the protocol the front end polls and the runtime drives.

All control-flow decisions are made by *file existence* and the ``state`` field here —
never by parsing model chat text. Writes are atomic (write-temp + ``os.replace``) so a
poll can never read a half-written file.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from . import config

# --- status states ---
QUEUED = "queued"
RUNNING_INTAKE = "running_intake"
AWAITING_ANSWERS = "awaiting_answers"
RUNNING_RESEARCH = "running_research"
AWAITING_APPROVAL = "awaiting_approval"
DONE = "done"
ERROR = "error"


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_status(slug: str) -> dict[str, Any] | None:
    p = config.status_path(slug)
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_status(
    slug: str,
    state: str,
    *,
    message: str = "",
    error: str | None = None,
    cost_usd: float | None = None,
) -> dict[str, Any]:
    prev = read_status(slug) or {}
    total_cost = round((prev.get("cost_usd") or 0.0) + (cost_usd or 0.0), 6)
    data = {
        "slug": slug,
        "state": state,
        "message": message,
        "error": error,
        "updated_at": now_iso(),
        "cost_usd": total_cost,
        "links": {
            "status": f"/api/clients/{slug}/status",
            "questions": f"/clients/{slug}/questions",
            "results": f"/clients/{slug}/results",
            "report": f"/api/clients/{slug}/report",
        },
    }
    _atomic_write_json(config.status_path(slug), data)
    return data


def read_questions(slug: str) -> dict[str, Any] | None:
    p = config.questions_path(slug)
    if not p.exists():
        return None
    try:
        with p.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


_VALID_TYPES = {"select", "multiselect", "text", "boolean"}
_VALID_MERGES_PREFIX = ("set", "append", "replace_index:")


def questions_valid(data: dict[str, Any] | None) -> bool:
    """A questions.json the runtime is willing to surface to the applicant."""
    if not isinstance(data, dict):
        return False
    qs = data.get("questions")
    if not isinstance(qs, list) or not qs:
        return False
    for q in qs:
        if not isinstance(q, dict):
            return False
        if not q.get("id") or not q.get("prompt"):
            return False
        if q.get("type") not in _VALID_TYPES:
            return False
        if not isinstance(q.get("target_path"), str) or not q["target_path"]:
            return False
        merge = q.get("merge", "set")
        if not isinstance(merge, str) or not merge.startswith(_VALID_MERGES_PREFIX):
            return False
    return True


def clear_questions(slug: str) -> None:
    p = config.questions_path(slug)
    if p.exists():
        p.unlink()
