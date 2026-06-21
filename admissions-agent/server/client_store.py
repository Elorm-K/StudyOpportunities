"""Create a client folder from the template and write its validated profile.

All profile validation goes through the existing ``lib/profile_io.py`` — never
reimplemented here. Per-client async locks serialize the SDK run against the
answers-merge so they can't interleave for the same client.
"""

from __future__ import annotations

import asyncio
import re
import secrets
import shutil
from typing import Any

# admissions-agent/ is on sys.path (uvicorn runs from there), so `lib` imports cleanly.
from lib import profile_io

from . import config

_LOCKS: dict[str, asyncio.Lock] = {}


def get_lock(slug: str) -> asyncio.Lock:
    lock = _LOCKS.get(slug)
    if lock is None:
        lock = asyncio.Lock()
        _LOCKS[slug] = lock
    return lock


def _slugify(name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", (name or "client").lower()).strip("-")
    return base or "client"


def new_slug(full_name: str) -> str:
    """A readable, unguessable-enough slug: ``ada-mensah-3f9c2a``."""
    return f"{_slugify(full_name)}-{secrets.token_hex(3)}"


def create_client(profile: dict[str, Any]) -> str:
    """Validate the submitted profile, copy ``_template`` to a fresh slug, write it.

    Raises ``jsonschema.ValidationError`` if the profile doesn't match the contract.
    """
    profile_io.validate_profile(profile)  # fail fast before creating anything
    full_name = (profile.get("identity") or {}).get("full_name", "")
    slug = new_slug(full_name)
    dest = config.client_dir(slug)
    # token_hex collision is astronomically unlikely; loop just in case.
    while dest.exists():
        slug = new_slug(full_name)
        dest = config.client_dir(slug)
    shutil.copytree(config.TEMPLATE_DIR, dest)
    profile_io.save_profile(config.profile_path(slug), profile)  # re-validates on write
    return slug
