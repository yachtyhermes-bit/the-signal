#!/usr/bin/env python3
"""
prose-lint.py — deterministic smoothness gate for The Signal articles.

Checks an article JSON's bodyHtml (and title) against the mechanical
readability rules in the signal-article-style skill (2026-09-06):

  HARD FAIL (exit 1):
    - sentence longer than 34 words
    - more than one em-dash PAIR in a sentence (i.e. 3+ dashes — stacked
      dashes; a single balanced pair like "— X —" is fine)
    - banned tics: "and that's the whole story", "in one breath", "in a
      nutshell", "it's not just X, it's Y" mic-drop constructions
    - paragraph longer than 6 sentences
    - title longer than 14 words or ending in a "— and ..." mic-drop

  WARN (exit 0, printed):
    - sentence 28-34 words
    - paragraph 5-6 sentences
    - paragraph longer than 65 words
    - article average sentence length > 18 words
    - article outside 500-900 words

Usage:
    python3 prose-lint.py articles/posts/<slug>.json [more.json ...]
    python3 prose-lint.py --last 3        # lint the N most recently dated articles
    python3 prose-lint.py --all           # lint every article JSON

Exit code 1 if any file has a HARD FAIL (gate), 0 otherwise.
Run it in the swarm before writing the JSON, and in the fact-check cron as a
post-publish backstop. Fix all FAILs; treat WARNs as editorial judgment.
"""
import json
import re
import sys
import glob
import os

HARD_SENT = 34
WARN_SENT = 28
HARD_PARA_SENTS = 6
WARN_PARA_SENTS = 5
WARN_PARA_WORDS = 65
WARN_AVG = 18
MIN_WORDS = 500
MAX_WORDS = 900

BANNED = [
    "and that's the whole story",
    "in one breath",
    "in a nutshell",
    "and that's the story",
    "that's the whole story",
]

EM_DASH = "\u2014"

def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).strip()

def split_sentences(txt):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", txt) if s.strip()]

def split_paragraphs(body_html):
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body_html, re.S)
    return [strip_html(p) for p in paras if strip_html(p)]

def lint_file(path):
    problems = []  # (level, msg)
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    slug = os.path.basename(path)
    title = d.get("title", "")
    body = strip_html(d.get("bodyHtml", ""))
    paras = split_paragraphs(d.get("bodyHtml", ""))
    words = body.split()

    # ---- title checks ----
    tw = title.split()
    if len(tw) > 14:
        problems.append(("FAIL", f"title {len(tw)} words (>14): {title!r}"))
    if re.search(r"\u2014\s+and\b", title):
        problems.append(("FAIL", "title ends in a '\u2014 and ...' mic-drop"))

    # ---- banned tics ----
    low = body.lower()
    for tic in BANNED:
        if tic in low:
            problems.append(("FAIL", f"banned tic: {tic!r}"))

    # ---- sentence checks ----
    sents = split_sentences(body)
    for s in sents:
        n = len(s.split())
        if n > HARD_SENT:
            problems.append(("FAIL", f"sentence {n} words (> {HARD_SENT}): {s[:110]}..."))
        elif n > WARN_SENT:
            problems.append(("WARN", f"sentence {n} words (> {WARN_SENT}): {s[:110]}..."))
        if s.count(EM_DASH) >= 3:
            problems.append(("FAIL", f"stacked em-dashes ({s.count(EM_DASH)}x): {s[:110]}..."))

    # ---- paragraph checks ----
    for p in paras:
        nw = len(p.split())
        ns = len(split_sentences(p))
        if ns > HARD_PARA_SENTS:
            problems.append(("FAIL", f"paragraph {ns} sentences (> {HARD_PARA_SENTS}): {p[:110]}..."))
        elif ns >= WARN_PARA_SENTS:
            problems.append(("WARN", f"paragraph {ns} sentences: {p[:110]}..."))
        if nw > WARN_PARA_WORDS:
            problems.append(("WARN", f"paragraph {nw} words (> {WARN_PARA_WORDS}): {p[:110]}..."))

    # ---- whole-article checks ----
    if sents:
        avg = sum(len(s.split()) for s in sents) / len(sents)
        if avg > WARN_AVG:
            problems.append(("WARN", f"avg sentence {avg:.1f} words (> {WARN_AVG})"))
    nw = len(words)
    if nw < MIN_WORDS or nw > MAX_WORDS:
        problems.append(("WARN", f"article {nw} words (target {MIN_WORDS}-{MAX_WORDS})"))

    return slug, problems, len(words), len(sents)

def main():
    args = sys.argv[1:]
    paths = []
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--all":
        paths = sorted(glob.glob("articles/posts/*.json"))
    elif args[0] == "--last":
        n = int(args[1]) if len(args) > 1 else 3
        dated = []
        for p in glob.glob("articles/posts/*.json"):
            try:
                with open(p, encoding="utf-8") as f:
                    date = json.load(f).get("date", "")
            except Exception:
                continue
            dated.append((date, p))
        dated.sort(reverse=True)
        paths = [p for _, p in dated[:n]]
    else:
        paths = args

    any_fail = False
    for path in paths:
        if not os.path.exists(path):
            print(f"missing: {path}")
            any_fail = True
            continue
        slug, problems, nw, ns = lint_file(path)
        fails = [m for lvl, m in problems if lvl == "FAIL"]
        warns = [m for lvl, m in problems if lvl == "WARN"]
        status = "FAIL" if fails else ("warn" if warns else "PASS")
        print(f"{status.upper():4s} {slug}  ({nw} words, {ns} sentences)")
        for lvl, m in problems:
            print(f"      [{lvl}] {m}")
        if fails:
            any_fail = True
    return 1 if any_fail else 0

if __name__ == "__main__":
    sys.exit(main())
