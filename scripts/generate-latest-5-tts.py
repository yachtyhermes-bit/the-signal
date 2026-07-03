#!/usr/bin/env python3
"""Generate Andrew TTS for the latest 5 articles only."""
import asyncio, edge_tts, json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'articles' / 'posts'
TMP_DIR = '/tmp/signal-tts'
VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000

os.makedirs(TMP_DIR, exist_ok=True)

async def main():
    # Get latest 5 articles by mtime
    json_files = sorted(POSTS_DIR.glob('*.json'), key=lambda f: os.path.getmtime(f), reverse=True)[:5]

    results = {'generated': [], 'skipped': [], 'errors': []}

    for jf in json_files:
        with open(jf) as f:
            article = json.load(f)
        slug = article.get('slug')
        if not slug:
            results['errors'].append(f'{jf.name}: no slug')
            continue

        out_path = os.path.join(TMP_DIR, f'{slug}.mp3')

        # Check if already exists in /tmp
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            results['skipped'].append(slug)
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
            results['skipped'].append(f'{slug} (too short)')
            continue

        try:
            communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
            with open(out_path, 'wb') as fout:
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':
                        fout.write(chunk['data'])
            if os.path.getsize(out_path) > 500:
                results['generated'].append(slug)
            else:
                os.unlink(out_path)
                results['errors'].append(f'{slug} (too small)')
        except Exception as e:
            results['errors'].append(f'{slug}: {e}')

    # Report
    print("=" * 60)
    print("🎙️  ANDREW TTS GENERATION REPORT (Latest 5 Articles)")
    print("=" * 60)
    print(f"\n✅ GENERATED ({len(results['generated'])}):")
    for s in results['generated']:
        fpath = os.path.join(TMP_DIR, f'{s}.mp3')
        size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        print(f"   • {s} ({size/1024:.0f} KB)")
    print(f"\n⏭️  SKIPPED ({len(results['skipped'])}):")
    for s in results['skipped']:
        print(f"   • {s}")
    if results['errors']:
        print(f"\n❌ ERRORS ({len(results['errors'])}):")
        for e in results['errors']:
            print(f"   • {e}")
    print()

if __name__ == '__main__':
    asyncio.run(main())
