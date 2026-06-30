"""Instant KB teaser for the conversational intake.

Once the chat knows target country + field + degree level + nationality, it surfaces a few REAL
candidate universities and eligible scholarships pulled straight from the pre-seeded KB catalogs —
before the full research runs. Deterministic and cheap: reads the markdown catalogs, no web, no LLM,
and never invents schools. The chat model presents only what this returns.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import config

# field-of-study keyword → catalog cluster tag (the catalog's own taxonomy)
_CLUSTER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "cs-data": ("computer", "data science", "data analy", "software", "ai", "artificial intelligence",
                "machine learning", " ml", "informatics", "computing"),
    "engineering": ("engineering", "mechanical", "electrical", "electronic", "civil", "aerospace",
                    "chemical eng", "robotics"),
    "business": ("business", "management", "finance", "mba", "accounting", "economics", "marketing"),
    "public-health": ("public health", "epidemiolog", "global health", "health", "medicine", "nursing",
                      "pharmac"),
    "law": ("law", "legal", "llm", "jurisprudence"),
    "social-dev": ("development", "social", "policy", "international relations", "politics",
                   "sociolog", "anthropolog", "public administration"),
    "sciences": ("physics", "chemistry", "biolog", "mathematic", "environmental", "geolog",
                 "neuroscience", "science"),
}


def field_to_clusters(fields: list[str]) -> set[str]:
    """Map free-text fields of study to catalog cluster tags (best-effort, may return several)."""
    blob = " ".join(f.lower() for f in (fields or []))
    hits = {tag for tag, kws in _CLUSTER_KEYWORDS.items() if any(k in blob for k in kws)}
    return hits


def _catalog_path(country: str) -> Path | None:
    cc = (country or "").strip().lower()
    if cc in ("uk", "united kingdom", "u.k.", "britain", "england", "scotland", "wales"):
        return config.AGENT_DIR / "kb" / "universities" / "uk.md"
    if cc in ("us", "usa", "united states", "u.s.", "u.s.a.", "america"):
        return config.AGENT_DIR / "kb" / "universities" / "us.md"
    return None


def _table_rows(path: Path) -> list[list[str]]:
    """Return the catalog table's data rows as lists of cells (header + separator skipped)."""
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s.startswith("|") or "---" in s:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0].lower() == "university":
            continue  # header
        if len(cells) >= 8:
            rows.append(cells)
    return rows


def university_candidates(country: str, clusters: set[str], degree_level: str, limit: int = 6) -> list[dict]:
    """Real catalog rows matching the client's field cluster(s) + degree level, de-duped by school."""
    path = _catalog_path(country)
    if not path or not path.exists():
        return []
    dl = (degree_level or "").strip().lower()
    out: list[dict] = []
    seen: set[str] = set()
    for cells in _table_rows(path):
        uni, row_clusters, row_degree = cells[0], cells[1].lower(), cells[2].lower()
        if clusters and not any(c in row_clusters for c in clusters):
            continue
        if dl and dl not in row_degree:
            continue
        key = uni.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append({"university": uni, "entry": cells[4], "funding": cells[6], "source": cells[7]})
        if len(out) >= limit:
            break
    return out


def _scholarship_files(countries: list[str], nationalities: list[str]) -> list[Path]:
    base = config.AGENT_DIR / "kb" / "scholarships"
    files: list[Path] = []
    cc = " ".join(c.lower() for c in (countries or []))
    if "uk" in cc or "united kingdom" in cc or "britain" in cc:
        files.append(base / "uk.md")
    if "us" in cc or "united states" in cc or "america" in cc:
        files.append(base / "us.md")
    nat = " ".join(n.lower() for n in (nationalities or []))
    if any(a in nat for a in ("nigeria", "ghana", "kenya", "africa", "south africa")):
        files.append(base / "africa.md")
    if any(a in nat for a in ("bangladesh", "indonesia", "malaysia", "vietnam", "philippines", "thailand")):
        files.append(base / "seasia.md")
    return [f for f in files if f.exists()]


def scholarship_hints(countries: list[str], nationalities: list[str], limit: int = 6) -> list[str]:
    """Bolded award names from rows that mention the nationality or are open to all — a teaser, not a match."""
    nats = [n.lower() for n in (nationalities or []) if n]
    names: list[str] = []
    seen: set[str] = set()
    for path in _scholarship_files(countries, nationalities):
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s.startswith("|"):
                continue
            low = s.lower()
            eligible = any(n in low for n in nats) or "all eligible" in low or "no country" in low \
                or "all nationalities" in low or "no nationality" in low
            if not eligible:
                continue
            m = re.search(r"\*\*(.+?)\*\*", s)  # first bolded cell = award name
            if not m:
                continue
            name = m.group(1).strip()
            key = name.lower()
            if key not in seen and len(name) < 80:
                seen.add(key)
                names.append(name)
            if len(names) >= limit:
                return names
    return names


def preview_payload(profile: dict) -> dict:
    """Structured instant teaser for the results page. Returns {} when nothing matches.

    Same KB lookup as ``build_preview`` (real catalog rows, no web, no LLM) but shaped as JSON the
    results page renders into the pinned 'Early matches' card:
        {"universities": {"UK": [{"university","entry","funds_intl"}]},
         "scholarships": ["Chevening", ...]}
    """
    targets = profile.get("targets") or {}
    identity = profile.get("identity") or {}
    countries = targets.get("countries") or []
    fields = targets.get("fields_of_study") or []
    degree = targets.get("degree_level") or ""
    nats = identity.get("nationality") or []
    clusters = field_to_clusters(fields)

    universities: dict[str, list[dict]] = {}
    for country in countries:
        unis = university_candidates(country, clusters, degree, limit=5)
        if unis:
            universities[country] = [
                {
                    "university": u["university"],
                    "entry": u["entry"],
                    "funds_intl": "funds_internationals=yes" in u["funding"],
                }
                for u in unis
            ]
    scholarships = scholarship_hints(countries, nats)

    if not universities and not scholarships:
        return {}
    return {"universities": universities, "scholarships": scholarships}


def build_preview(profile: dict) -> str:
    """A short, plain-text teaser the chat model relays verbatim. Empty string if nothing matches."""
    targets = profile.get("targets") or {}
    identity = profile.get("identity") or {}
    countries = targets.get("countries") or []
    fields = targets.get("fields_of_study") or []
    degree = targets.get("degree_level") or ""
    nats = identity.get("nationality") or []
    clusters = field_to_clusters(fields)

    lines: list[str] = []
    for country in countries:
        unis = university_candidates(country, clusters, degree, limit=5)
        if unis:
            lines.append(f"{country} universities that fit your field:")
            for u in unis:
                fund = "funds intl" if "funds_internationals=yes" in u["funding"] else "scholarship-route funding"
                lines.append(f"  • {u['university']} — entry: {u['entry']} ({fund})")
    sch = scholarship_hints(countries, nats)
    if sch:
        lines.append("Scholarships you may be eligible for: " + ", ".join(sch) + ".")

    if not lines:
        return ""
    return ("\n".join(lines) +
            "\n\n(This is a quick preview from our knowledge base — your full plan will rank these "
            "by your admission odds and funding fit, with sources for every figure.)")
