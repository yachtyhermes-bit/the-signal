#!/usr/bin/env python3
"""html-nesting-guard.py — catch the unclosed-tag defect class at build time, before a deploy.

The failure this exists to stop: a site-wide nav/search overlay edit shipped a search-close
button missing </svg></button>. The browser kept the <svg>/<button> open and nested the ENTIRE
page inside <div id="searchOverlay"> (opacity:0; visibility:hidden; position:fixed), so
/hive/boardroom/ served HTTP 200 and rendered a blank, unscrollable page.

Static checks per HTML file (scripts and inline styles are stripped first, because JS template
literals contain markup that would wreck naive tag counting):
  TRAP     content markers appear while #searchOverlay / #drawer / .search-overlay is still open
  OVERFLOW the file ends with more open containers than it closed
  IMBALANCE div/section/main/footer counts do not balance (warning only - benign cases exist)

Exit 0 when no TRAP is found; exit 1 otherwise. Usage:
    python3 scripts/html-nesting-guard.py [--root DIR ...] [--quiet]
"""
import argparse
import pathlib
import re
import sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
        'param', 'source', 'track', 'wbr', 'path', 'line', 'circle', 'rect', 'polygon',
        'polyline', 'stop', 'use'}
BLOCK = {'div', 'section', 'main', 'footer', 'article', 'aside', 'nav', 'header'}

# Containers that hide everything inside them when the page loads.
OVERLAY_IDS = {'searchoverlay', 'drawer', 'searchmodal', 'draweroverlay'}
OVERLAY_CLASSES = {'search-overlay', 'drawer', 'search-modal'}
# Evidence that real page content is present.
CONTENT_HINTS = ('<footer', '<main', 'id="leaderboard"', 'class="lb-section', 'class="hero',
                 '<article', 'id="hive', 'class="article-', '</body>')


def strip_script_style(html: str) -> str:
    html = re.sub(r'<script\b[^>]*>.*?</script>', '<!--script-->', html, flags=re.S | re.I)
    html = re.sub(r'<style\b[^>]*>.*?</style>', '<!--style-->', html, flags=re.S | re.I)
    return html


def is_overlay(attrs: dict) -> bool:
    if (attrs.get('id') or '').lower() in OVERLAY_IDS:
        return True
    classes = set((attrs.get('class') or '').split())
    return bool(classes & OVERLAY_CLASSES)


# Elements that carry the page's actual reading content. Deliberately narrow: the nav drawer
# legitimately holds menu markup, so links/buttons/nav must not count as trapped content.
CONTENT_TAGS = {'footer', 'main', 'article', 'h1', 'table'}
CONTENT_IDS = {'leaderboard', 'hivetablebody', 'hivetablewrap'}
CONTENT_CLASSES = {'lb-section', 'hero', 'article-body', 'article-content'}


def is_content(attrs: dict, tag: str) -> bool:
    if tag in CONTENT_TAGS:
        return True
    if (attrs.get('id') or '').lower() in CONTENT_IDS:
        return True
    return bool(set((attrs.get('class') or '').split()) & CONTENT_CLASSES)


class Guard(HTMLParser):
    """Flags real page content that is parsed while a hidden container is still open.

    The test is deliberately stack-based, not positional: an empty <div id="drawerOverlay">
    that closes immediately must never flag the footer that follows it, while a container that
    was never closed will still be on the stack when the content arrives.
    """

    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.stack = []           # (tag, hidden_flag, overlay_label)
        self.trap = None          # (label, content_tag)
        self.text = text

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        attrs = {k.lower(): (v or '') for k, v in attrs}
        outer = next((s for s in reversed(self.stack) if s[1]), None)
        if is_overlay(attrs):
            label = attrs.get('id') or attrs.get('class') or tag
            self.stack.append((tag, True, label))
            return
        inherited = bool(outer)
        label = outer[2] if outer else None
        if inherited and self.trap is None and is_content(attrs, tag):
            self.trap = (label, tag)
        self.stack.append((tag, inherited, label))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def scan(path: pathlib.Path):
    raw = path.read_text(errors='ignore')
    text = strip_script_style(raw)
    guard = Guard(text)
    try:
        guard.feed(text)
    except Exception:
        pass
    problems = []
    if guard.trap:
        label, content_tag = guard.trap
        problems.append(('TRAP', f'<{content_tag}> (page content) is nested inside the hidden '
                                 f'container "{label}", which was never closed'))
    if guard.stack:
        leftover = [t for t, _, _ in guard.stack if t in BLOCK]
        if leftover:
            problems.append(('OVERFLOW', f'{len(leftover)} container(s) never closed: {leftover[:6]}'))
    opens = sum(len(re.findall(rf'<{t}\b', text, re.I)) for t in BLOCK)
    closes = sum(len(re.findall(rf'</{t}>', text, re.I)) for t in BLOCK)
    if opens != closes:
        problems.append(('IMBALANCE', f'{opens} block opens vs {closes} closes'))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', action='append', default=None,
                    help='directory tree to scan (repeatable). Default: _backup_dist public dist')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    repo = pathlib.Path(__file__).resolve().parent.parent
    roots = [pathlib.Path(r) if str(r).startswith('/') else repo / r
             for r in (args.root or ['_backup_dist', 'public', 'dist'])]

    files = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob('*.html')))
    if not files:
        print('html-nesting-guard: no HTML files found; check --root')
        return 0

    traps, overflow, imbalance = [], [], []
    for f in files:
        if '/quarantine/' in str(f) or '/_drafts/' in str(f) or 'node_modules' in str(f):
            continue
        for kind, msg in scan(f):
            rel = str(f).replace(str(repo) + '/', '')
            if kind == 'TRAP':
                traps.append((rel, msg))
            elif kind == 'OVERFLOW':
                overflow.append((rel, msg))
            else:
                imbalance.append((rel, msg))

    if not args.quiet:
        print(f'html-nesting-guard: scanned {len(files)} files '
              f'({", ".join(str(r).replace(str(repo) + "/", "") for r in roots)})')
        for rel, msg in traps:
            print(f'  TRAP      {rel}\n              {msg}')
        for rel, msg in overflow:
            print(f'  OVERFLOW  {rel}\n              {msg}')
        if imbalance:
            print(f'  IMBALANCE {len(imbalance)} file(s) - warning only, often benign:')
            for rel, msg in imbalance[:5]:
                print(f'              {rel}: {msg}')
        if not (traps or overflow):
            print('  no trapped content, no unclosed containers')

    return 1 if traps else 0


if __name__ == '__main__':
    sys.exit(main())
