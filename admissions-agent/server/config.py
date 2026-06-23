"""Environment-driven configuration + path helpers.

The web runtime lives in ``admissions-agent/server/``; the agent it drives lives one
level up in ``admissions-agent/`` (which holds ``CLAUDE.md`` + ``.claude/skills/``).
The SDK runs with ``cwd = AGENT_DIR`` so it auto-loads the orchestrator and skills, and
both the agent and this server read/write the same ``clients/<slug>/`` tree.

On Railway, ``entrypoint.sh`` symlinks ``AGENT_DIR/clients`` and ``AGENT_DIR/kb`` onto a
persistent volume, so no path divergence is needed here — ``CLIENTS_DIR`` is always
``AGENT_DIR/clients`` and the symlink makes it durable.
"""

from __future__ import annotations

import os
from pathlib import Path

# Load a local .env for development. load_dotenv() does NOT override variables already in
# the environment, so on Railway (where vars are injected directly) this is a harmless no-op.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# server/ -> admissions-agent/
AGENT_DIR = Path(os.environ.get("AGENT_DIR", Path(__file__).resolve().parent.parent)).resolve()

CLIENTS_DIR = AGENT_DIR / "clients"
TEMPLATE_DIR = CLIENTS_DIR / "_template"
INTAKE_FORM = AGENT_DIR / "intake" / "intake-form.html"
STATIC_DIR = Path(__file__).resolve().parent / "static"

# Honor guardrail #7: operator approves the client-facing report before release.
APPROVAL_REQUIRED = os.environ.get("APPROVAL_REQUIRED", "true").lower() not in ("0", "false", "no")
# Operator token gates the approval endpoint. If unset, operator endpoints are disabled.
OPERATOR_TOKEN = os.environ.get("OPERATOR_TOKEN") or None

# Model + cost guards. Each phase is capped independently; Phase B does the web research.
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-8")
# The conversational intake chat uses a cheap/fast model (Anthropic Messages API, not the agent CLI).
CHAT_MODEL = os.environ.get("CHAT_MODEL", "claude-haiku-4-5")
CHAT_MAX_TURNS = int(os.environ.get("CHAT_MAX_TURNS", "30"))  # safety cap on intake conversation length
MAX_BUDGET_USD_INTAKE = float(os.environ.get("MAX_BUDGET_USD_INTAKE", "1.50"))
MAX_BUDGET_USD_RESEARCH = float(os.environ.get("MAX_BUDGET_USD_RESEARCH", "12.0"))
MAX_TURNS = int(os.environ.get("MAX_TURNS", "300"))

# Wall-clock caps per phase. A hung SDK run trips these and surfaces as an ERROR the
# applicant can see, instead of an eternal spinner.
MAX_RUN_SECONDS_INTAKE = int(os.environ.get("MAX_RUN_SECONDS_INTAKE", "300"))
MAX_RUN_SECONDS_RESEARCH = int(os.environ.get("MAX_RUN_SECONDS_RESEARCH", "1800"))

# How many agent phases may run concurrently across all clients (worker-thread pool size).
MAX_CONCURRENT_RUNS = int(os.environ.get("MAX_CONCURRENT_RUNS", "4"))


def client_dir(slug: str) -> Path:
    return CLIENTS_DIR / slug


def profile_path(slug: str) -> Path:
    return client_dir(slug) / "client_profile.json"


def status_path(slug: str) -> Path:
    return client_dir(slug) / "status.json"


def questions_path(slug: str) -> Path:
    return client_dir(slug) / "questions.json"


def outputs_dir(slug: str) -> Path:
    return client_dir(slug) / "outputs"


def draft_report_path(slug: str) -> Path:
    return outputs_dir(slug) / "report.draft.md"


def final_report_path(slug: str) -> Path:
    return outputs_dir(slug) / "report.md"


def docx_report_path(slug: str) -> Path:
    """The Word deliverable clients download (rendered from the finalized report.md)."""
    return outputs_dir(slug) / "report.docx"
