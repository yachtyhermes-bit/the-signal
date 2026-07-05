#!/usr/bin/env python3
"""Batch generate Andrew TTS for all articles and upload to R2 via wrangler.
Generates all MP3s first, then uploads with proper delays."""
import asyncio, edge_tts, json, os, subprocess, sys, time, glob
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'articles' / 'posts'
TMP_DIR = '/tmp/signal-tts'
VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000

os.makedirs(TMP_DIR, exist_ok=True)

# ─── Phase 1: Generate all MP3s ───
async def gen_all():
    json_files = sorted(POSTS_DIR.glob('*.json'))
    print(f"🎙️  Generating Andrew TTS for {len(json_files)} articles...")
    
    gen_ok = 0
    gen_skip = 0
    
    for i, jf in enumerate(json_files):
        with open(jf) as f:
            article = json.load(f)
        slug = article.get('slug')
        if not slug:
            continue
        
        out_path = os.path.join(TMP_DIR, f'{slug}.mp3')
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            continue
        
        title = article.get('title', '')
        # Use full bodyHtml instead of just summary
        body_html = article.get('bodyHtml', '')
        if body_html:
            import re
            text = re.sub(r'<[^>]+>', ' ', body_html)
            text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
            text = re.sub(r'\s+', ' ', text).strip()
            text = f"{title}. {text}"
        else:
            summary = article.get('summary', '')
            text = f"{title}. {summary}"
        if len(text) < 50:
            continue
        
        try:
            communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
            with open(out_path, 'wb') as fout:
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':
                        fout.write(chunk['data'])
            if os.path.getsize(out_path) > 500:
                gen_ok += 1
            else:
                os.unlink(out_path)
                print(f"  ⚠️  Too small: {slug}")
        except Exception as e:
            print(f"  ❌ Gen error {slug}: {e}")
        
        if (i + 1) % 30 == 0:
            print(f"  ... {gen_ok} generated so far ({i+1}/{len(json_files)})")
        await asyncio.sleep(0.1)
    
    print(f"  ✅ {gen_ok} generated, {gen_skip} already cached")
    return glob.glob(f'{TMP_DIR}/*.mp3')

# ─── Phase 2: Upload all to R2 via Cloudflare API ───
def upload_all(mp3_files):
    total = len(mp3_files)
    print(f"\n📤 Uploading {total} files to R2 directly via Cloudflare API...")
    
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    acct = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
    if not token or not acct:
        print("  ❌ CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set")
        return
    
    ok = 0
    fail = 0
    bucket = 'the-signal-audio'
    
    for i, filepath in enumerate(mp3_files):
        slug = os.path.splitext(os.path.basename(filepath))[0]
        key = f'v2/{slug}.mp3'
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            url = f'https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/{bucket}/objects/{key}'
            req = urllib.request.Request(url, data=data, method='PUT')
            req.add_header('Authorization', f'Bearer {token}')
            req.add_header('Content-Type', 'audio/mpeg')
            
            resp = urllib.request.urlopen(req, timeout=45)
            if resp.status == 200:
                ok += 1
                os.unlink(filepath)
            else:
                fail += 1
                print(f"  ❌ Upload failed [{slug}]: HTTP {resp.status} {resp.read()[:100]}")
        except urllib.error.HTTPError as e:
            fail += 1
            body = e.read()[:150]
            print(f"  ❌ HTTP {e.code} [{slug}]: {body}")
        except Exception as e:
            fail += 1
            print(f"  ❌ Error {slug}: {e}")
        
        if (i + 1) % 25 == 0:
            print(f"  📤 {ok}/{i+1} uploaded...")
        
        time.sleep(0.5)
    
    print(f"\n📊 Done: {ok} uploaded, {fail} failed, {total - ok - fail} skipped")
    
    # Cleanup remaining temp files
    for f in glob.glob(f'{TMP_DIR}/*.mp3'):
        os.unlink(f)
    print("🧹 Cleaned up temp files")

if __name__ == '__main__':
    mp3s = asyncio.run(gen_all())
    if mp3s:
        upload_all(mp3s)
    else:
        print("No MP3s to upload")
