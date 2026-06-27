#!/usr/bin/env python3
"""Force-regenerate TTS audio for a single article, bypassing the R2 cache check.
Usage: python3 scripts/regenerate-tts.py <slug>"""
import asyncio, json, os, re, subprocess, sys
from pathlib import Path
from tempfile import NamedTemporaryFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CF_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
BUCKET = "the-signal-audio"
OBJECT_PREFIX = "v2/"
PRIMARY_VOICE = "en-US-AndrewNeural"
FALLBACK_VOICES = ["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-SoniaNeural"]
MAX_RETRIES = 3

slug = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Usage: python3 scripts/regenerate-tts.py <slug>")
article_path = PROJECT_ROOT / "articles" / "posts" / f"{slug}.json"
if not article_path.exists():
    sys.exit(f"Article not found: {article_path}")

with open(article_path) as f:
    article = json.load(f)

def strip_html(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

parts = [article.get("title", "")]
body_html = article.get("bodyHtml", "")
parts.append(strip_html(body_html) if body_html else article.get("summary", ""))
text = ". ".join(p for p in parts if p)

print(f"🎙 {article.get('title','')[:80]}...")
print(f"   {len(text)} chars")

async def gen_with_retry(slug, text, voice):
    """Try to generate TTS with a single voice, with retries."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice)
            with NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name
            with open(tmp_path, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
            size = os.path.getsize(tmp_path)
            if size >= 500:
                return tmp_path, size
            print(f"   Audio too small ({size} bytes), attempt {attempt}/{MAX_RETRIES}")
            os.unlink(tmp_path)
        except Exception as e:
            print(f"   Attempt {attempt}/{MAX_RETRIES} with {voice}: {e}")
            if 'tmp_path' in dir() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            if attempt < MAX_RETRIES:
                wait = 2 ** attempt
                print(f"   Retrying in {wait}s...")
                await asyncio.sleep(wait)
    return None, 0

async def gen():
    voices = [PRIMARY_VOICE] + FALLBACK_VOICES
    for voice in voices:
        tmp_path, size = await gen_with_retry(slug, text, voice)
        if tmp_path:
            print(f"   Voice: {voice}")
            break
    if not tmp_path:
        print("   All voices exhausted, giving up")
        return
    # Save local copy to public/audio/ so static path works
    local_dir = PROJECT_ROOT / "public" / "audio"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / f"{slug}.mp3"
    import shutil
    shutil.copy2(tmp_path, str(local_path))
    print(f"   Saved local: {local_path} ({size/1024:.0f} KB)")
    result = subprocess.run(
        ['npx', 'wrangler', 'r2', 'object', 'put',
         f'{BUCKET}/{OBJECT_PREFIX}{slug}.mp3',
         '--file', tmp_path, '--remote'],
        capture_output=True, text=True, timeout=60,
        cwd=str(PROJECT_ROOT),
        env={**os.environ, 'CLOUDFLARE_API_TOKEN': CF_API_TOKEN,
             'CLOUDFLARE_ACCOUNT_ID': CF_ACCOUNT_ID}
    )
    if result.returncode == 0:
        print(f"   Uploaded {size/1024:.0f} KB to R2")
    else:
        print(f"   R2 upload skipped (CF credentials not set)")
    os.unlink(tmp_path)

asyncio.run(gen())
