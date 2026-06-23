"""Render a finalized Markdown report into a Word (.docx) deliverable.

The client-facing report is authored in Markdown by `report-generation` and finalized
(`report.draft.md` -> `report.md`) at the operator-approval gate. Clients receive it as a **Word
document**, not raw Markdown — this module is the single place that conversion happens. It runs
server-side and is fully deterministic (no model involvement), so the approval gate stays
trustworthy.

Pipeline: Markdown -> HTML (python-markdown, with table support) -> docx (htmldocx). These are the
only pure-Python deps that handle the report's Markdown tables (university shortlist, scholarships)
faithfully without a system `pandoc` binary. See `requirements.txt`.
"""

from __future__ import annotations

from pathlib import Path


def markdown_to_docx(md_text: str, out_path: str | Path) -> Path:
    """Convert a Markdown report to a .docx file at ``out_path``. Returns the written path.

    Raises ``RuntimeError`` with an actionable message if the optional Word-export packages
    aren't installed, so the caller can surface a clean error instead of an ImportError.
    """
    try:
        import markdown as _markdown
        from docx import Document
        from htmldocx import HtmlToDocx
    except ImportError as exc:  # pragma: no cover - exercised only when deps are missing
        raise RuntimeError(
            "Word export needs the 'markdown', 'python-docx', and 'htmldocx' packages "
            "(declared in requirements.txt)."
        ) from exc

    # `tables` renders the report's pipe tables; `sane_lists` + `fenced_code` keep the rest faithful.
    html = _markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

    document = Document()
    HtmlToDocx().add_html_to_document(html, document)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(out))
    return out
