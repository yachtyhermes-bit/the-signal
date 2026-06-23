#!/usr/bin/env python3
"""prebuild-tts.py — Pre-generate Jenny TTS MP3s for articles missing from R2.
Runs before build.js. Generates MP3s via edge-tts, uploads to R2 via wrangler.

Usage: source .dev.vars && python3 scripts/prebuild-tts.py
"""

import os, sys, json, subprocess, asyncio, glob, time
from html.parser import HTMLParser

VOICE = 'en-US-AndrewNeural'
BUCKET = 'the-signal-audio'
ARTICLES_GLOB = 'articles/posts/*.json'
R2_PREFIX = 'v2'

# ---- Text extraction ----

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
    def handle_data(self, data):
        t = data.strip()
        if len(t) > 10:
            self.texts.append(t)

def get_article_text(slug):
    path = f'{ARTICLES_GLOB.replace("*.json", "")}/{slug}.json'
    real_path = os.path.join(os.path.dirname(__file__), '..', path)
    if not os.path.exists(real_path):
        return None
    with open(real_path) as f:
        article = json.load(f)
    extractor = TextExtractor()
    extractor.feed(article.get('bodyHtml', ''))
    text = '. '.join(extractor.texts)
    return text[:5000] if len(text) > 5000 else text

# ---- R2 operations via REST API ----

def list_r2_objects():
    """List all v2/*.mp3 objects in R2 using Cloudflare REST API."""
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
    
    # Fallback: read from .dev.vars if env vars not set
    if (not token or not account_id):
        dev_vars_path = os.path.join(os.path.dirname(__file__), '..', '.dev.vars')
        if os.path.exists(dev_vars_path):
            with open(dev_vars_path) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        if k == 'CLOUDFLARE_API_TOKEN': token = v
                        elif k == 'CLOUDFLARE_ACCOUNT_ID': account_id = v
    if not token or not account_id:
        print("ERROR: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set")
        sys.exit(1)

    import urllib.request
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/buckets/{BUCKET}/objects?limit=200&prefix={R2_PREFIX}/'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            if data.get('success'):
                return {o['key'] for o in data.get('result', [])}
            else:
                print(f"R2 list API error: {data.get('errors', [])}")
                return set()
    except Exception as e:
        print(f"R2 list request failed: {e}")
        return set()

def upload_to_r2(slug, mp3_path):
    """Upload MP3 to R2 using wrangler CLI with --remote flag."""
    key = f'{R2_PREFIX}/{slug}.mp3'
    result = subprocess.run(
        ['npx', 'wrangler', 'r2', 'object', 'put', f'{BUCKET}/{key}',
         '--file', mp3_path, '--remote'],
        capture_output=True, text=True, timeout=60,
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    if result.returncode != 0:
        print(f"    wrangler stderr: {result.stderr.strip()[:200]}")
    return result.returncode == 0

# ---- Jenny generation ----

async def generate_jenny(text, output_path):
    """Generate Jenny TTS MP3 from text using edge-tts."""
    try:
        import edge_tts
    except ImportError:
        print("    edge-tts not installed, skipping")
        return False
    tts = edge_tts.Communicate(text, VOICE)
    with open(output_path, 'wb') as f:
        async for chunk in tts.stream():
            if chunk['type'] == 'audio':
                f.write(chunk['data'])
    return os.path.getsize(output_path) > 500

# ---- Main ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pre-generate Jenny TTS MP3s for articles missing from R2')
    parser.add_argument('--recent', type=int, metavar='HOURS', default=0,
                        help='Only process articles modified in the last N hours (0 = all)')
    args = parser.parse_args()

    root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(root)

    # Get all article slugs
    article_files = list(glob.glob(ARTICLES_GLOB))
    
    # Filter by recency if requested
    if args.recent > 0:
        cutoff = time.time() - (args.recent * 3600)
        recent_files = [f for f in article_files if os.path.getmtime(f) > cutoff]
        article_files = recent_files
        print(f"⏱️  Recent ({args.recent}h): {len(article_files)} articles modified")
    
    slugs = sorted([os.path.splitext(os.path.basename(f))[0] for f in article_files])
    total = len(slugs)
    print(f"📄 Articles to check: {total}")

    if not slugs:
        print("No articles to process.")
        return

    # Get existing R2 objects
    r2_objects = list_r2_objects()
    in_r2 = len(r2_objects)
    print(f"☁️  Jenny MP3s in R2: {in_r2}")

    # Find missing
    missing = [s for s in slugs if f'{R2_PREFIX}/{s}.mp3' not in r2_objects]
    if not missing:
        print("✅ All checked articles have Jenny MP3s. Nothing to generate.")
        return

    print(f"🎙️  Missing from R2: {len(missing)} — generating now...\n")
    
    # Estimate time
    est_seconds = len(missing) * 25
    print(f"⏱️  Estimated: ~{est_seconds//60}m {est_seconds%60}s\n")

    success = 0
    skipped = 0
    failed = 0

    for i, slug in enumerate(missing):
        text = get_article_text(slug)
        if not text:
            print(f"  [{i+1}/{len(missing)}] {slug} — ⚠️  SKIP (no text)")
            skipped += 1
            continue

        mp3_path = f'/tmp/tts-pre-{slug}.mp3'

        try:
            # Generate
            ok = asyncio.run(generate_jenny(text, mp3_path))
            if not ok:
                print(f"  [{i+1}/{len(missing)}] {slug} — ✗ GENERATION FAILED")
                failed += 1
                continue

            # Upload
            if upload_to_r2(slug, mp3_path):
                success += 1
                print(f"  [{i+1}/{len(missing)}] {slug} — ✓ {(os.path.getsize(mp3_path)/1024):.0f}KB")
            else:
                failed += 1
                print(f"  [{i+1}/{len(missing)}] {slug} — ✗ UPLOAD FAILED")
        finally:
            if os.path.exists(mp3_path):
                os.remove(mp3_path)

        # Small delay between uploads to respect rate limits
        if i < len(missing) - 1:
            time.sleep(0.3)

    print(f"\n{'='*50}")
    print(f"Done. ✓ {success}  ⚠️ {skipped}  ✗ {failed}")
    print(f"R2 coverage: {in_r2} → {in_r2 + success}/{total} articles")

if __name__ == '__main__':
    main()
