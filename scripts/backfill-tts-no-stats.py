#!/usr/bin/env python3
"""Backfill: regenerate TTS audio for articles whose bodyHtml embeds a stats/data
block (the "Numbers That Matter" card), so the existing mp3s stop narrating ticker
metrics. Text comes from scripts/tts_text.py (stats blocks stripped), audio is
written to /tmp and uploaded straight to R2 as v2/<slug>.mp3 — public/audio and
dist/ are untouched.

3 workers, one edge-tts CLI subprocess each (isolated; the most reliable parallel
mode per the signal-tts-batch skill).
"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, "/home/chino/thesignal/scripts")
from tts_text import article_to_tts_text, SKIP_CLASSES  # noqa: E402
import r2_upload  # noqa: E402  (loads creds from .dev.vars on import)

ROOT = Path("/home/chino/thesignal")
TMP = Path("/tmp/tts-backfill")
TMP.mkdir(exist_ok=True)
EDGE = "/home/chino/thesignal/.venv/bin/edge-tts"
VOICE = "en-US-AndrewNeural"
WORKERS = 3
LOG = open("/tmp/tts-backfill.log", "a", buffering=1)


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n")


def affected():
    out = []
    for p in sorted((ROOT / "articles" / "posts").glob("*.json")):
        try:
            a = json.loads(p.read_text())
        except Exception:
            continue
        b = a.get("bodyHtml") or ""
        if a.get("slug") and any(cls in b for cls in SKIP_CLASSES):
            out.append(a)
    return out


def one(art):
    slug = art["slug"]
    text = article_to_tts_text(art)
    if len(text) < 50:
        return slug, "skip", 0
    txt_file = TMP / f"{slug}.txt"
    mp3 = TMP / f"{slug}.mp3"
    txt_file.write_text(text)
    for attempt, timeout in ((1, 300), (2, 420)):
        try:
            subprocess.run([EDGE, "--voice", VOICE, "--file", str(txt_file),
                            "--write-media", str(mp3)],
                           capture_output=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            continue
        if mp3.exists() and mp3.stat().st_size > 500:
            size = mp3.stat().st_size
            ok = r2_upload.upload_to_r2(str(mp3), f"v2/{slug}.mp3", "audio/mpeg")
            if ok:
                mp3.unlink(missing_ok=True)
                txt_file.unlink(missing_ok=True)
                return slug, "ok", size
    return slug, "fail", 0


def main():
    arts = affected()
    log(f"[{time.strftime('%H:%M:%S')}] backfill start — {len(arts)} articles, {WORKERS} workers")
    ok = fail = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(one, a): a["slug"] for a in arts}
        for i, f in enumerate(as_completed(futs), 1):
            slug, status, size = f.result()
            ok += status == "ok"
            fail += status == "fail"
            if status != "ok" or i % 10 == 0:
                log(f"  [{i}/{len(arts)}] {status} {slug} {size} ok={ok} fail={fail}")
    log(f"[{time.strftime('%H:%M:%S')}] backfill done — ok={ok} fail={fail} in {(time.time()-t0)/60:.1f} min")


main()
