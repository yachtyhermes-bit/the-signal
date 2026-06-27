#!/usr/bin/env python3
"""Batch generate TTS for all missing articles from the last 30 days.
Runs edge-tts directly (skips R2 upload for speed)."""
import asyncio, json, os, re, sys, shutil
from pathlib import Path
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = PROJECT_ROOT / "articles" / "posts"
AUDIO_DIR = PROJECT_ROOT / "public" / "audio"
PRIMARY_VOICE = "en-US-AndrewNeural"
FALLBACK_VOICES = ["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-SoniaNeural"]
MAX_RETRIES = 3
CUTOFF = datetime.now() - timedelta(days=30)
CUTOFF_STR = CUTOFF.strftime('%Y-%m-%d')

def strip_html(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()

def get_missing_slugs():
    missing = []
    for f in sorted(os.listdir(POSTS_DIR)):
        if not f.endswith('.json'): continue
        try:
            with open(POSTS_DIR / f) as fh:
                art = json.load(fh)
            slug = art.get('slug', '')
            date = (art.get('date', '') or '')[:10]
            if not slug: continue
            if date >= CUTOFF_STR:
                mp3 = AUDIO_DIR / f'{slug}.mp3'
                if not mp3.exists():
                    missing.append((slug, art.get('title', '')))
        except: pass
    return missing

async def generate_one(slug, article):
    """Generate TTS for a single article using edge-tts, with retry + fallback voices."""
    parts = [article.get("title", "")]
    body_html = article.get("bodyHtml", "")
    parts.append(strip_html(body_html) if body_html else article.get("summary", ""))
    text = ". ".join(p for p in parts if p)

    # Cap at 5000 chars like the API does
    text = text[:5000]

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIO_DIR / f'{slug}.mp3'

    voices = [PRIMARY_VOICE] + FALLBACK_VOICES
    for voice in voices:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                communicate = edge_tts.Communicate(text, voice)
                with NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                    tmp_path = tmp.name

                with open(tmp_path, "wb") as f:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])

                size = os.path.getsize(tmp_path)
                if size < 500:
                    print(f"  {slug}: audio too small ({size} bytes), attempt {attempt}/{MAX_RETRIES}")
                    os.unlink(tmp_path)
                    if attempt < MAX_RETRIES:
                        wait = 2 ** attempt
                        await asyncio.sleep(wait)
                    continue

                shutil.copy2(tmp_path, str(out_path))
                os.unlink(tmp_path)
                print(f"  {slug}: {size/1024:.0f} KB (voice: {voice}, attempts: {attempt})")
                return size
            except Exception as e:
                print(f"  {slug}: attempt {attempt}/{MAX_RETRIES} with {voice}: {e}")
                if 'tmp_path' in dir() and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                if attempt < MAX_RETRIES:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
        # If we exhausted retries for this voice, print and move to next
        print(f"  {slug}: voice {voice} failed after {MAX_RETRIES} attempts, trying next voice")

    print(f"  {slug}: all voices exhausted, giving up")
    return 0

async def main():
    missing = get_missing_slugs()
    print(f"Missing {len(missing)} articles (last 30 days)")

    OK = 0
    FAIL = 0

    # Process with semaphore for parallelism (3 at a time to avoid rate limits)
    SEM = asyncio.Semaphore(3)

    async def worker(slug, title):
        nonlocal OK, FAIL
        async with SEM:
            article_path = POSTS_DIR / f'{slug}.json'
            if not article_path.exists():
                print(f"  {slug}: JSON not found")
                FAIL += 1
                return
            with open(article_path) as f:
                article = json.load(f)
            result = await generate_one(slug, article)
            if result >= 500:
                OK += 1
            else:
                FAIL += 1

    tasks = [worker(slug, title) for slug, title in missing]
    await asyncio.gather(*tasks)

    print(f"\nDone: {OK} generated, {FAIL} failed")

asyncio.run(main())
