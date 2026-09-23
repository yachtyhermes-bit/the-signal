#!/usr/bin/env python3
"""Generate TTS for ONE article slug and exit. Designed for cron use where
each article needs its own separate terminal call to reset the 600s wall clock.

Usage:
    python3 scripts/tts-one.py asml-q2-blowout-record-guidance-euv-2026
"""
import asyncio, edge_tts, json, sys, os, re
# ── shared TTS text extraction (drops the 'Numbers That Matter' stats card) ──
try:
    from tts_text import strip_nonprose  # noqa: E402
except ImportError:  # executed from another cwd
    import sys as _sys
    _sys.path.insert(0, '/home/chino/thesignal/scripts')
    from tts_text import strip_nonprose  # noqa: E402

from pathlib import Path

slug = sys.argv[1]
ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 300
os.makedirs(TMP_DIR, exist_ok=True)

out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
    print(f"SKIP {slug} (already exists)")
    sys.exit(0)

jf = ROOT / "articles" / "posts" / f"{slug}.json"
if not jf.exists():
    print(f"NOT FOUND {slug}")
    sys.exit(1)

with open(jf) as f:
    article = json.load(f)

title = article.get("title", "")
body_html = article.get("bodyHtml", "")
if body_html:
    text = re.sub(r"<[^>]+>", " ", strip_nonprose(body_html))
    for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
        text = text.replace(a, b)
    text = re.sub(r"\s+", " ", text).strip()
    text = f"{title}. {text}"
else:
    text = f"{title}. {article.get('summary', '')}"

async def gen():
    communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
    with open(out_path, "wb") as fout:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fout.write(chunk["data"])
    sz = os.path.getsize(out_path)
    if sz > 500:
        print(f"OK {slug} ({sz} bytes)")
    else:
        os.unlink(out_path)
        print(f"FAIL {slug} (too small: {sz})")

asyncio.run(gen())
