"""Merge the applicant's answers from the second form back into client_profile.json.

Each question in ``questions.json`` is self-describing: it carries the ``target_path``
(dotted path into the profile) and a ``merge`` rule, so this module stays generic and
never hardcodes question semantics. The merged profile is re-validated against the
schema before saving, so a bad path can't corrupt the data contract.
"""

from __future__ import annotations

from typing import Any

from lib import profile_io

from . import config, state


def _navigate(root: dict[str, Any], parts: list[str]) -> tuple[Any, str]:
    """Return (container, final_key) for a dotted path, creating dict nodes as needed."""
    node: Any = root
    for key in parts[:-1]:
        if not isinstance(node, dict) or key not in node:
            raise KeyError(f"path segment '{key}' not found")
        node = node[key]
    return node, parts[-1]


def _apply_one(profile: dict[str, Any], target_path: str, merge: str, value: Any) -> None:
    parts = target_path.split(".")
    container, key = _navigate(profile, parts)
    if not isinstance(container, dict):
        raise KeyError(f"'{target_path}' does not address a settable field")

    if merge == "set":
        container[key] = value
    elif merge == "append":
        cur = container.get(key)
        if not isinstance(cur, list):
            raise KeyError(f"'{target_path}' is not a list; cannot append")
        if isinstance(value, list):
            cur.extend(v for v in value if v not in cur)
        elif value not in cur:
            cur.append(value)
    elif merge.startswith("replace_index:"):
        idx = int(merge.split(":", 1)[1])
        cur = container.get(key)
        if not isinstance(cur, list):
            raise KeyError(f"'{target_path}' is not a list; cannot replace index")
        while len(cur) <= idx:
            cur.append("")
        cur[idx] = value
    else:
        raise ValueError(f"unknown merge rule: {merge}")


def apply_answers(slug: str, answers: dict[str, Any]) -> None:
    """Apply ``{question_id: value}`` to the profile, validate, save, clear questions.json.

    Skips answers whose value is empty/None and questions that aren't found.
    Raises if the resulting profile fails schema validation.
    """
    questions_doc = state.read_questions(slug) or {}
    by_id = {q.get("id"): q for q in questions_doc.get("questions", []) if isinstance(q, dict)}

    profile = profile_io.load_profile(config.profile_path(slug))

    for qid, value in (answers or {}).items():
        q = by_id.get(qid)
        if q is None:
            continue
        if value is None or value == "" or value == []:
            continue
        _apply_one(profile, q["target_path"], q.get("merge", "set"), value)

    profile_io.save_profile(config.profile_path(slug), profile)  # validates on write
    state.clear_questions(slug)
