"""Shared profile IO + validation.

Single source of truth for reading, writing, and validating ``client_profile.json``.
Every skill script MUST go through these helpers — never parse the profile JSON ad hoc.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - jsonschema is a declared dependency
    jsonschema = None

# schema/ lives at the repo root (admissions-agent/), two levels up from lib/.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA_PATH = _REPO_ROOT / "schema" / "client_profile.schema.json"


def schema_path() -> Path:
    """Absolute path to the client_profile JSON Schema."""
    return _SCHEMA_PATH


def load_schema() -> dict[str, Any]:
    """Load and return the client_profile JSON Schema."""
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_profile(path: str | Path) -> dict[str, Any]:
    """Load a client_profile.json from ``path`` and return it as a dict."""
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Validate ``profile`` against the schema.

    Returns the profile unchanged on success; raises ``jsonschema.ValidationError``
    on failure. Raises ``RuntimeError`` if jsonschema is not installed.
    """
    if jsonschema is None:
        raise RuntimeError(
            "jsonschema is required for validation. Install with: pip install -r requirements.txt"
        )
    jsonschema.validate(instance=profile, schema=load_schema())
    return profile


def save_profile(path: str | Path, profile: dict[str, Any], *, validate: bool = True) -> None:
    """Write ``profile`` to ``path`` as pretty JSON.

    Validates against the schema first (unless ``validate=False``) so a skill can
    never persist a malformed profile.
    """
    if validate:
        validate_profile(profile)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        json.dump(profile, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":  # smoke check: validate the _template instance
    import sys

    template = _REPO_ROOT / "clients" / "_template" / "client_profile.json"
    try:
        validate_profile(load_profile(template))
    except Exception as exc:  # noqa: BLE001 - CLI smoke wants the raw error
        print(f"INVALID: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {template} validates against {_SCHEMA_PATH.name}")
