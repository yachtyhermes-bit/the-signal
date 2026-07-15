#!/usr/bin/env python3
"""Parallel batch TTS generator — generates all articles using concurrent workers."""

import asyncio, edge_tts, json, os, sys, glob, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 180
CONCURRENCY = 8  # 8 parallel workers

os.makedirs(TMP_DIR, exist_ok=True)

async def generate_one(slug, text):
    out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        return ("skip", slug)
    try:
        communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
        with open(out_path, "wb") as fout:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    fout.write(chunk["data"])
        if os.path.getsize(out_path) > 500:
            return ("ok", slug)
        os.unlink(out_path)
        return ("fail", slug)
    except asyncio.TimeoutError:
        if os.path.exists(out_path):
            os.unlink(out_path)
        return ("fail", slug)
    except Exception as e:
        if os.path.exists(out_path):
            os.unlink(out_path)
        return ("error", f"{slug}: {e}")

async def worker(sem, slug, text, results):
    async with sem:
        status, detail = await generate_one(slug, text)
        results.append((status, detail))

async def main():
    json_files = sorted(POSTS_DIR.glob("*.json"))
    total = len(json_files)
    print(f"Total articles: {total}", flush=True)

    articles = []
    for jf in json_files:
        with open(jf) as f:
            article = json.load(f)
        slug = article.get("slug")
        if not slug:
            continue
        title = article.get("title", "")
        body_html = article.get("bodyHtml", "")
        if body_html:
            text = re.sub(r"<[^>]+>", " ", body_html)
            for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                         ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
                text = text.replace(a, b)
            text = re.sub(r"\s+", " ", text).strip()
            text = f"{title}. {text}"
        else:
            text = f"{title}. {article.get('summary', '')}"
        if len(text) < 50:
            continue
        articles.append((slug, text))
    
    print(f"Articles to process: {len(articles)}", flush=True)
    
    sem = asyncio.Semaphore(CONCURRENCY)
    results = []
    
    tasks = [worker(sem, slug, text, results) for slug, text in articles]
    
    # Progress reporting while tasks run
    total_tasks = len(tasks)
    done_count = 0
    start = time.time()
    
    # Use gather with periodic progress check
    for i, coro in enumerate(asyncio.as_completed(tasks), 1):
        await coro
        elapsed = time.time() - start
        rate = i / elapsed if elapsed > 0 else 0
        eta = (total_tasks - i) / rate if rate > 0 else 0
        ok = sum(1 for r in results if r[0] == "ok")
        skip = sum(1 for r in results if r[0] == "skip")
        fail = sum(1 for r in results if r[0] in ("fail", "error"))
        if i % 10 == 0 or i == total_tasks:
            print(f"  [{i}/{total_tasks}] ok={ok} skip={skip} fail={fail} | {rate:.1f}/s | ETA {eta:.0f}s", flush=True)
    
    elapsed = time.time() - start
    ok = sum(1 for r in results if r[0] == "ok")
    skip = sum(1 for r in results if r[0] == "skip")
    fail = sum(1 for r in results if r[0] in ("fail", "error"))
    
    mp3s = list(Path(TMP_DIR).glob("*.mp3"))
    print(f"\n=== DONE in {elapsed:.0f}s ===", flush=True)
    print(f"OK={ok} Skip={skip} Fail={fail} TotalMP3s={len(mp3s)}", flush=True)
    
    if fail > 0:
        failed = [r[1] for r in results if r[0] in ("fail", "error")]
        print(f"Failed articles ({len(failed)}): {failed[:10]}...", flush=True)
    
    # Write list of all slugs for upload
    slug_list = [f.stem for f in sorted(mp3s)]
    Path("/tmp/signal-tts-slugs.json").write_text(json.dumps(slug_list))
    print(f"Slugs written to /tmp/signal-tts-slugs.json ({len(slug_list)} slugs)", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
