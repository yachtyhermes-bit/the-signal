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
    - title contains 'just' (institutional-register rule 2026-09-07: headlines
      read like Seeking Alpha/SemiAnalysis, not teasers; 'X Just Did Y' is the
      #1 corpus crutch) or a cheerleader punchline tail ("and All", "and More",
      "or Not", "— and the Stock Is Exploding")

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

# ---- voice / rhythm metrics (added 2026-09-30 after the writer bake-off) ----
# The corpus problem is not slop vocabulary (mean 0.3 hits per 1k words) — it is FLATNESS:
# half the live articles run a sentence-length SD below 9, and 63% are dash-heavy.
SLOP = [
    "delve", "landscape", "testament", "tapestry", "game-changer", "game changer",
    "unlock", "seamless", "robust", "cutting-edge", "revolutionize", "revolutionary",
    "in today's", "moreover", "furthermore", "it's worth noting", "at the end of the day",
    "when it comes to", "realm", "underscore", "paradigm", "synergy", "holistic",
    "the bottom line is", "boasts", "plethora", "myriad", "crucial", "pivotal", "vital",
    "navigate the",
]
SD_FAIL, SD_WARN = 6.0, 9.0        # sentence-length standard deviation
SLOP_FAIL_PER_1K, SLOP_WARN_PER_1K = 3.0, 1.5
DASH_WARN_PER_1K = 15.0

VOWELS = "aeiouy"

def _syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n, prev = 0, False
    for ch in w:
        v = ch in VOWELS
        if v and not prev:
            n += 1
        prev = v
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)

def voice_metrics(title, body, sents):
    """Rhythm, slop and reading-ease numbers. Rhythm is the dial that decides whether
    an article reads like writing or like a filing."""
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", body)
    nw = max(1, len(words))
    lens = [len(s.split()) for s in sents] or [0]
    asl = sum(lens) / len(lens)
    if len(lens) > 1:
        mean = asl
        sd = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** 0.5
    else:
        sd = 0.0
    asw = sum(_syllables(w) for w in words) / nw
    flesch = 206.835 - 1.015 * asl - 84.6 * asw
    low = body.lower()
    slop_hits = [(t, low.count(t)) for t in SLOP if t in low]
    slop_total = sum(n for _, n in slop_hits)
    slop_per_1k = slop_total / nw * 1000
    dashes = body.count(EM_DASH)
    dash_per_1k = dashes / nw * 1000
    return dict(nw=nw, asl=asl, sd=sd, flesch=flesch, slop_total=slop_total,
                slop_per_1k=slop_per_1k, dash_per_1k=dash_per_1k, dashes=dashes,
                slop_hits=[t for t, _ in slop_hits])

def strip_html(s):
    # Remove stats-card block before stripping tags so table contents don't form a 50-word sentence
    s = re.sub(r'<div class="stats-card">.*?</div>\s*</div>', ' ', s, flags=re.S)
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
    if re.search(r"\bjust\b", title, re.I):
        problems.append(("FAIL", "title contains 'just' (institutional register: no 'X Just Did Y' openers)"))
    # ONE sentence (user rule 2026-09-29): a second sentence carrying a verdict/contrast is rejected.
    # Abbreviations are neutralised first so 'U.S.' / 'Inc.' don't read as sentence breaks.
    _t = re.sub(r"\b(?:U\.S|U\.K|E\.U|Inc|Corp|Ltd|Co|Mr|Ms|Dr|St|vs|No|Q[1-4]|e\.g|i\.e|etc)\.", "X", title)
    if re.search(r'[.!?]\s+["\u201c]?[A-Z0-9]', _t):
        problems.append(("FAIL", f"title is more than one sentence — one plain sentence only: {title!r}"))
    if re.search(r"\b(and all|and more|and counting|or not|no more|right now|yet again)\b[.!?\"]*$", title, re.I):
        problems.append(("FAIL", "title ends in a cheerleader punchline tail"))

    # ---- decay / time-anchor checks (skill v1.3.0: the 2-week test) ----
    weekday_re = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", re.I)
    for field, val in (("title", title),
                       ("subtitle", d.get("subtitle", "")),
                       ("summary", d.get("summary", ""))):
        if val and weekday_re.search(val):
            problems.append(("FAIL", f"{field} contains a weekday anchor (use the date once, then relative language)"))
    if len(weekday_re.findall(body)) > 1:
        problems.append(("WARN", "body has >1 weekday anchor (anchor the date once)"))

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

    # ---- voice / rhythm (the dial the bake-off showed actually decides readability) ----
    vm = voice_metrics(title, body, sents)
    if len(sents) >= 30:                      # SD is meaningless on a short piece
        if vm["sd"] < SD_FAIL:
            problems.append(("FAIL", f"flat rhythm: sentence-length SD {vm['sd']:.1f} (< {SD_FAIL}) — vary long and short"))
        elif vm["sd"] < SD_WARN:
            problems.append(("WARN", f"even rhythm: sentence-length SD {vm['sd']:.1f} (< {SD_WARN})"))
    if vm["slop_per_1k"] >= SLOP_FAIL_PER_1K:
        problems.append(("FAIL", f"AI-slop density {vm['slop_per_1k']:.1f}/1k words: {', '.join(vm['slop_hits'])}"))
    elif vm["slop_per_1k"] >= SLOP_WARN_PER_1K:
        problems.append(("WARN", f"slop words present ({vm['slop_per_1k']:.1f}/1k): {', '.join(vm['slop_hits'])}"))
    if vm["dash_per_1k"] > DASH_WARN_PER_1K:
        problems.append(("WARN", f"dash-heavy: {vm['dashes']} em-dashes ({vm['dash_per_1k']:.1f}/1k words)"))
    problems.append(("VOICE",
                     f"rhythm SD {vm['sd']:.1f} | avg sentence {vm['asl']:.1f} words | "
                     f"reading ease {vm['flesch']:.0f} | slop {vm['slop_per_1k']:.1f}/1k | "
                     f"em-dashes {vm['dashes']} ({vm['dash_per_1k']:.1f}/1k)"))

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
