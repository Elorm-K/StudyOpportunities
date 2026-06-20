"""Shared knowledge-base freshness helper.

The one deterministic "should I refresh this KB fact?" check, reused by every skill's freshness
guardrail and by `knowledge-base-update`. Dep-free: parses the few frontmatter fields we need with
minimal regex/line handling (no pyyaml), tolerating trailing `# comments`.

KB files (`kb/*.md`) start with a YAML header, e.g.:
    ---
    title: ...
    last_verified: 2026-06-20        # or null
    source_urls:
      - https://...
    freshness_threshold_days: 365    # comment ok
    status: seeded                   # seeded | partial | deferred | TODO
    ---

Usage (CLI smoke test):  python kb.py
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

# status values that always mean "treat as needing refresh", regardless of date
_STALE_STATUSES = {"todo", "deferred", "partial"}


def _read_header(path: str | Path) -> list[str]:
    """Return the lines of the leading YAML frontmatter block (between the first two '---')."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    out: list[str] = []
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        out.append(ln)
    return out


def _strip_comment(value: str) -> str:
    """Drop a trailing ' # comment' (but not a '#' inside a URL)."""
    return re.sub(r"\s+#.*$", "", value).strip()


def load_frontmatter(path: str | Path) -> dict:
    """Extract the fields we care about: last_verified, freshness_threshold_days, status, source_urls."""
    fm: dict = {"last_verified": None, "freshness_threshold_days": None, "status": None, "source_urls": []}
    header = _read_header(path)
    in_sources = False
    for ln in header:
        if re.match(r"^\s*-\s+\S", ln) and in_sources:
            fm["source_urls"].append(_strip_comment(ln.split("-", 1)[1]))
            continue
        in_sources = False
        m = re.match(r"^(\w+):\s*(.*)$", ln)
        if not m:
            continue
        key, raw = m.group(1), _strip_comment(m.group(2))
        if key == "source_urls":
            in_sources = True  # list items follow on subsequent lines
        elif key == "last_verified":
            fm["last_verified"] = None if raw in ("", "null", "~") else raw
        elif key == "freshness_threshold_days":
            fm["freshness_threshold_days"] = int(raw) if raw.isdigit() else None
        elif key == "status":
            fm["status"] = raw or None
    return fm


def is_stale(path: str | Path, today: date) -> bool:
    """True if this KB file needs a knowledge-base-update before its facts are used.

    Stale when: last_verified is null/missing; status is TODO/deferred/partial; or the entry is older
    than its freshness_threshold_days. A missing threshold defaults to stale-after-365-days.
    """
    fm = load_frontmatter(path)
    if (fm["status"] or "").lower() in _STALE_STATUSES:
        return True
    if not fm["last_verified"]:
        return True
    try:
        verified = date.fromisoformat(fm["last_verified"])
    except ValueError:
        return True  # unparseable date → treat as stale
    threshold = fm["freshness_threshold_days"] or 365
    return (today - verified).days > threshold


def update_frontmatter(
    path: str | Path,
    *,
    last_verified: str,
    add_source_urls: tuple[str, ...] = (),
    status: str | None = None,
) -> None:
    """Stamp the header after a refresh: set last_verified/status, append new source_urls.

    Line-oriented and conservative — only touches the header; the body (figures/tables) is written by
    the agent via Edit.
    """
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{p} has no YAML frontmatter")
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")

    existing = set(load_frontmatter(p)["source_urls"])
    out = lines[: end]  # header lines (excludes closing ---), we rebuild within [1, end)

    new_header: list[str] = [out[0]]  # opening ---
    i = 1
    while i < end:
        ln = lines[i]
        if re.match(r"^last_verified:", ln):
            new_header.append(f"last_verified: {last_verified}")
        elif status is not None and re.match(r"^status:", ln):
            new_header.append(f"status: {status}")
        elif re.match(r"^source_urls:", ln):
            new_header.append(ln)
            # copy existing list items
            j = i + 1
            while j < end and re.match(r"^\s*-\s+\S", lines[j]):
                new_header.append(lines[j])
                j += 1
            for url in add_source_urls:
                if url not in existing:
                    new_header.append(f"  - {url}")
            i = j
            continue
        else:
            new_header.append(ln)
        i += 1

    rebuilt = new_header + lines[end:]
    p.write_text("\n".join(rebuilt) + "\n", encoding="utf-8")


if __name__ == "__main__":
    repo = Path(__file__).resolve().parent.parent
    today = date(2026, 6, 20)  # injected; no Date.now needed

    seeded = repo / "kb" / "grading" / "grade-maps.md"
    deferred = repo / "kb" / "us" / "deadlines.md"

    print(f"grade-maps.md  stale? {is_stale(seeded, today)}  (expect False)")
    print(f"us/deadlines.md stale? {is_stale(deferred, today)}  (expect True)")
    print("frontmatter(grade-maps):", {k: v for k, v in load_frontmatter(seeded).items() if k != 'source_urls'})

    assert is_stale(seeded, today) is False, "seeded+fresh should not be stale"
    assert is_stale(deferred, today) is True, "deferred/null should be stale"
    # threshold check: a fresh file 400 days later is stale (threshold 365)
    assert is_stale(seeded, date(2027, 8, 1)) is True, "past threshold should be stale"
    print("\nOK: freshness logic correct.")
