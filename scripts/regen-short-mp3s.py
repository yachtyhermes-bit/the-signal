#!/usr/bin/env python3
"""Regenerate short MP3s (title+summary) with full article body text."""
import asyncio, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'articles' / 'posts'
AUDIO_DIR = ROOT / 'public' / 'audio'
VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000
THRESHOLD = 500000  # 500KB - files smaller than this need regeneration

def strip_html(html):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def generate_mp3(text, output_path):
    import edge_tts
    tts = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
    with open(output_path, 'wb') as f:
        async for chunk in tts.stream():
            if chunk['type'] == 'audio':
                f.write(chunk['data'])
    return os.path.getsize(output_path) > 500

def main():
    print("🔍 Finding short MP3s to regenerate...\n")
    
    short_files = []
    for mp3 in sorted(AUDIO_DIR.glob('*.mp3')):
        if mp3.stat().st_size < THRESHOLD:
            slug = mp3.stem
            json_path = POSTS_DIR / f'{slug}.json'
            if json_path.exists():
                short_files.append((slug, mp3))
    
    if not short_files:
        print("✅ No short MP3s found. All files are full-body.")
        return
    
    print(f"Found {len(short_files)} short MP3s to regenerate:\n")
    for slug, mp3 in short_files:
        size_kb = mp3.stat().st_size // 1024
        print(f"  • {slug} ({size_kb} KB)")
    
    print(f"\n🎙️  Regenerating with full article body text...\n")
    
    async def regen_all():
        success = 0
        failed = 0
        
        for i, (slug, old_mp3) in enumerate(short_files, 1):
            json_path = POSTS_DIR / f'{slug}.json'
            with open(json_path) as f:
                article = json.load(f)
            
            title = article.get('title', '')
            body_html = article.get('bodyHtml', '')
            if body_html:
                text = f"{title}. {strip_html(body_html)}"
            else:
                summary = article.get('summary', '')
                text = f"{title}. {summary}"
            
            tmp_path = old_mp3.with_suffix('.tmp.mp3')
            
            try:
                ok = await generate_mp3(text, tmp_path)
                if ok:
                    # Replace old file with new
                    old_mp3.unlink()
                    tmp_path.rename(old_mp3)
                    new_size_kb = old_mp3.stat().st_size // 1024
                    print(f"  [{i}/{len(short_files)}] {slug} — ✓ {new_size_kb} KB")
                    success += 1
                else:
                    print(f"  [{i}/{len(short_files)}] {slug} — ✗ Generation failed")
                    if tmp_path.exists():
                        tmp_path.unlink()
                    failed += 1
            except Exception as e:
                print(f"  [{i}/{len(short_files)}] {slug} — ✗ Error: {e}")
                if tmp_path.exists():
                    tmp_path.unlink()
                failed += 1
            
            await asyncio.sleep(0.2)
        
        return success, failed
    
    success, failed = asyncio.run(regen_all())
    
    print(f"\n{'='*50}")
    print(f"Done. ✓ {success} regenerated, ✗ {failed} failed")

if __name__ == '__main__':
    main()
