#!/usr/bin/env python3
"""Batch generate Andrew TTS for all articles and upload to R2 via wrangler.
Generates all MP3s first, then uploads with proper delays."""
import asyncio, edge_tts, json, os, subprocess, sys, time, glob
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

# ─── Phase 2: Upload all to R2 ───
def upload_all(mp3_files):
    total = len(mp3_files)
    print(f"\n📤 Uploading {total} files to R2...")
    
    ok = 0
    fail = 0
    
    for i, filepath in enumerate(mp3_files):
        slug = os.path.splitext(os.path.basename(filepath))[0]
        
        try:
            env = {**os.environ}
            # Ensure wrangler can auth — some subshells lose the token
            if not env.get('CLOUDFLARE_API_TOKEN'):
                env['CLOUDFLARE_API_TOKEN'] = os.environ.get('CLOUDFLARE_API_TOKEN', '')
            if not env.get('CLOUDFLARE_ACCOUNT_ID'):
                env['CLOUDFLARE_ACCOUNT_ID'] = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
            r = subprocess.run([
                'npx', 'wrangler', 'r2', 'object', 'put',
                f'the-signal-audio/v2/{slug}.mp3',
                '--file', filepath, '-y', '--remote'
            ], capture_output=True, text=True, timeout=45,
               cwd=str(ROOT), env=env)
            
            if r.returncode == 0:
                ok += 1
                # Clean up individual file after upload
                os.unlink(filepath)
            else:
                fail += 1
                print(f"  ❌ Upload failed [{slug}]: exit={r.returncode} err={r.stderr[:80]}")
        except subprocess.TimeoutExpired:
            fail += 1
            print(f"  ⏰ Timeout: {slug}")
        except Exception as e:
            fail += 1
            print(f"  ❌ Error {slug}: {e}")
        
        if (i + 1) % 25 == 0:
            print(f"  📤 {ok}/{i+1} uploaded...")
        
        time.sleep(1.2)
    
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
