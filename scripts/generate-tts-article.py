#!/usr/bin/env python3
"""Generate Andrew TTS for the latest article and upload to R2."""
import asyncio, edge_tts, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = ROOT / 'content' / 'articles'
VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000

async def main():
    # Find latest 5 JSON articles sorted by filename (newest last)
    json_files = sorted(ARTICLES_DIR.glob('*.json'))
    
    if not json_files:
        print("No articles found.")
        return
    
    # Take the latest 5
    latest = json_files[-5:]
    print(f"📂 Found {len(json_files)} article(s), processing latest {len(latest)}...")
    
    for jf in latest:
        with open(jf) as f:
            article = json.load(f)
        
        slug = article.get('slug')
        if not slug:
            print(f"  ⚠️  No slug in {jf.name}")
            continue
        
        title = article.get('title', '')
        body_html = article.get('bodyHtml', '')
        
        if body_html:
            text = re.sub(r'<[^>]+>', ' ', body_html)
            text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
            text = re.sub(r'\s+', ' ', text).strip()
            text = f"{title}. {text}"
        else:
            summary = article.get('summary', '')
            text = f"{title}. {summary}"
        
        if len(text) < 50:
            print(f"  ⚠️  Text too short: {slug}")
            continue
        
        text = text[:MAX_CHARS]
        
        # Check if already on R2
        r2_key = f"v2/{slug}.mp3"
        r = subprocess.run(
            ['npx', 'wrangler', 'r2', 'object', 'get', f'the-signal-audio/{r2_key}',
             '--file', '/dev/null'],
            capture_output=True, text=True, timeout=30,
            cwd=str(ROOT)
        )
        if r.returncode == 0:
            print(f"  ✅ Already on R2: {slug} — skipping")
            continue
        
        # Generate
        tmp_path = f'/tmp/signal-tts-{slug}.mp3'
        os.makedirs('/tmp', exist_ok=True)
        
        print(f"  🎙️  Generating TTS for: {slug} ({len(text)} chars)...", end=' ', flush=True)
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            with open(tmp_path, 'wb') as fout:
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':
                        fout.write(chunk['data'])
            
            size = os.path.getsize(tmp_path)
            if size < 500:
                os.unlink(tmp_path)
                print(f"❌ too small ({size} bytes)")
                continue
            
            print(f"OK ({size} bytes)")
            
            # Upload to R2
            print(f"  📤 Uploading to R2...", end=' ', flush=True)
            r = subprocess.run(
                ['npx', 'wrangler', 'r2', 'object', 'put',
                 f'the-signal-audio/{r2_key}',
                 '--file', tmp_path, '--remote'],
                capture_output=True, text=True, timeout=45,
                cwd=str(ROOT)
            )
            
            if r.returncode == 0:
                print(f"✅")
                os.unlink(tmp_path)
            else:
                print(f"❌ exit={r.returncode}: {r.stderr[:100]}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
