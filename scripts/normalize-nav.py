#!/usr/bin/env python3
"""Normalize the site-wide hamburger drawer so every page ships the same menu.

Source of truth: articles/partials/drawer.html (extracted from the homepage,
which carries the complete 19-item menu). Pages are edited by byte-range
surgery rather than full-document re-serialization, so surrounding markup,
scripts and inline styles stay untouched.

Usage:
  python3 scripts/normalize-nav.py            # report only
  python3 scripts/normalize-nav.py --apply    # rewrite files in place
  python3 scripts/normalize-nav.py --apply _backup_dist public articles
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = ROOT / "articles" / "partials" / "drawer.html"
DEFAULT_TARGETS = ("_backup_dist", "public", "articles")
SKIP_DIRS = {"node_modules", ".git", "dist", "tmp"}


def load_canonical() -> str:
    return PARTIAL.read_text(encoding="utf-8").strip()


def find_div_end(text: str, start: int) -> int:
    """Return the index just past the </div> that closes the div starting at `start`."""
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", text[start:], re.I):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return start + m.end()
        else:
            depth += 1
    raise ValueError("unbalanced <div>")


DRAWER_RE = re.compile(r'<div[^>]*\bid\s*=\s*["\']drawer["\'][^>]*>', re.I)

# Desktop-only quick links. The hamburger is hidden from 1024px up, so the two
# account pages that only existed inside the drawer need a visible entry point.
NAV_ACTIONS_RE = re.compile(r'<div[^>]*class="[^"]*\bnav-actions\b[^"]*"[^>]*>', re.I)
NAV_QUICK = ('\n        <a class="nav-quick" href="/insights/">Insights</a>'
             '\n        <a class="nav-quick" href="/watchlist/">Watchlist</a>')


def normalize(path: Path, canonical: str) -> tuple[int, int, bool, str]:
    """Return (links_before, links_after, differs, new_text); caller decides whether to write."""
    text = path.read_text(encoding="utf-8")
    m = DRAWER_RE.search(text)
    if not m:
        return (0, 0, False, text)
    start = m.start()
    end = find_div_end(text, start)
    before = len(re.findall(r'class="[^"]*drawer-link', text[start:end]))
    new_text = text[:start] + canonical + text[end:]
    after = len(re.findall(r'class="[^"]*drawer-link', canonical))

    if "nav-quick" not in new_text:
        m2 = NAV_ACTIONS_RE.search(new_text)
        if m2:
            new_text = new_text[:m2.end()] + NAV_QUICK + new_text[m2.end():]

    return (before, after, new_text != text, new_text)


def main() -> int:
    apply = "--apply" in sys.argv
    dirs = [a for a in sys.argv[1:] if not a.startswith("--")] or list(DEFAULT_TARGETS)
    canonical = load_canonical()
    changed = skipped = 0
    wrong = []
    for d in dirs:
        for path in sorted((ROOT / d).rglob("*.html")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            try:
                before, after, differs, new_text = normalize(path, canonical)
            except Exception as e:  # noqa: BLE001 - report and keep going
                print(f"  ERROR {path.relative_to(ROOT)}: {e}")
                continue
            if before == 0:
                skipped += 1
                continue
            if before != after:
                wrong.append((str(path.relative_to(ROOT)), before, after))
            if differs and apply:
                path.write_text(new_text, encoding="utf-8")
                changed += 1
    count = len(re.findall(r'class="[^"]*drawer-link', canonical))
    print(f"canonical menu items: {count}")
    print(f"files normalized: {changed if apply else 0} (dry run: {len(wrong)} differ)")
    print(f"files without a drawer: {skipped}")
    if wrong:
        print("\nper-file link count before -> after:")
        for name, b, a in wrong[:40]:
            print(f"  {b:2d} -> {a:2d}  {name}")
        if len(wrong) > 40:
            print(f"  ... {len(wrong) - 40} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
