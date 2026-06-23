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
VOICE = "en-US-AndrewNeural"

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

async def gen():
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE)
    with NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        tmp_path = tmp.name
    with open(tmp_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
    size = os.path.getsize(tmp_path)
    if size < 500:
        print("   ✗ Audio too small")
        os.unlink(tmp_path)
        return
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
        print(f"   ✓ Uploaded {size/1024:.0f} KB")
    else:
        print(f"   ✗ Upload failed: {result.stderr[:200]}")
    os.unlink(tmp_path)

asyncio.run(gen())
