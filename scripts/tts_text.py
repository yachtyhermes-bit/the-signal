#!/usr/bin/env python3
"""Shared TTS text extraction for The Signal.

Articles embed non-prose blocks inside bodyHtml — chiefly the "The Numbers That
Matter" stats card (`<div class="stats-card">` with a stats-table, rows, grids and
a live-price note). Stripping tags alone keeps all of that text, so the narrator
read the ticker metrics out loud. Every generator must pass bodyHtml through
strip_nonprose() first, and the DOM reader in public/js/tts.js filters the same
class list.

Usage from a script in scripts/ (that dir is on sys.path when run directly):

    from tts_text import strip_nonprose
    text = re.sub(r"<[^>]+>", " ", strip_nonprose(body_html))
"""

import html as _html
import re

# Class markers for blocks that must never be narrated (stats/data/annotation).
SKIP_CLASSES = (
    "stats-card",
    "stats-card-title",
    "stats-card-note",
    "stats-table",
    "stats-row",
    "stats-grid",
    "stat-card",
    "stats-live-badge",
    "data-card",
)

_TAG_RE = re.compile(r"<(/?)([A-Za-z0-9]+)([^>]*)>")


def strip_nonprose(body_html: str) -> str:
    """Drop stats/data blocks (and everything nested inside them) from article HTML.

    Balanced on the tag name, so nested <div>s inside the card go with it.
    """
    if not body_html:
        return ""
    out = []
    i, n = 0, len(body_html)
    while i < n:
        m = _TAG_RE.search(body_html, i)
        if not m:
            out.append(body_html[i:])
            break
        out.append(body_html[i:m.start()])
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if not closing and any(cls in attrs for cls in SKIP_CLASSES):
            depth, j = 1, m.end()
            while depth and j < n:
                m2 = _TAG_RE.search(body_html, j)
                if not m2:
                    j = n
                    break
                if m2.group(2).lower() == name:
                    depth += -1 if m2.group(1) else 1
                j = m2.end()
            out.append(" ")
            i = j
            continue
        out.append(m.group(0))
        i = m.end()
    return "".join(out)


def html_to_text(body_html: str) -> str:
    """Strip tags + entities from (already sanitised) article HTML."""
    text = re.sub(r"<[^>]+>", " ", strip_nonprose(body_html or ""))
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                 ("&#39;", "'"), ("&nbsp;", " ")):
        text = text.replace(a, b)
    text = _html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def article_to_tts_text(article: dict, max_chars: int = 0) -> str:
    """Title + narrated body text for an article dict (no stats-card numbers)."""
    title = (article.get("title") or "").strip()
    body = article.get("bodyHtml") or ""
    text = f"{title}. {html_to_text(body)}" if body else f"{title}. {article.get('summary', '')}"
    if max_chars:
        return text[:max_chars]
    return text
