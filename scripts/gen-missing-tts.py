#!/usr/bin/env python3
"""Generate Andrew TTS for specific articles, then upload to R2."""
import asyncio, edge_tts, json, os, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'articles' / 'posts'
TMP_DIR = '/tmp/signal-tts'
VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000

os.makedirs(TMP_DIR, exist_ok=True)

# Latest 5 slugs (by mtime)
LATEST = [
    'sofi-fintech-bank-charter-galileo-2026',
    'crowdstrike-ai-security-platform-2026',
    'coreweave-leveraged-ai-infrastructure-bull-bear-2026',
    'amazon-aws-ai-kuiper-dark-horse-2026',
    'alphabet-ai-cloud-waymo-undervalued-2026',
]

async def gen_one(slug):
    jf = POSTS_DIR / f'{slug}.json'
    if not jf.exists():
        print(f"  ⚠️  No JSON for {slug}")
        return None

    with open(jf) as f:
        article = json.load(f)

    out_path = os.path.join(TMP_DIR, f'{slug}.mp3')
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        print(f"  ⏭️  Already cached: {slug}")
        return out_path

    title = article.get('title', '')
    body_html = article.get('bodyHtml', '')
    if body_html:
        text = re.sub(r'<[^>]+>', ' ', body_html)
        for e, r in [('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"'),('&#39;',"'"),('&nbsp;',' ')]:
            text = text.replace(e, r)
        text = re.sub(r'\s+', ' ', text).strip()
        text = f"{title}. {text}"
    else:
        summary = article.get('summary', '')
        text = f"{title}. {summary}"

    if len(text) < 50:
        print(f"  ⚠️  Text too short: {slug}")
        return None

    try:
        communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
        with open(out_path, 'wb') as fout:
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    fout.write(chunk['data'])
        if os.path.getsize(out_path) > 500:
            print(f"  ✅ Generated: {slug} ({os.path.getsize(out_path)} bytes)")
            return out_path
        else:
            os.unlink(out_path)
            print(f"  ⚠️  Too small: {slug}")
            return None
    except Exception as e:
        print(f"  ❌ Error {slug}: {e}")
        return None

def upload_one(filepath):
    slug = os.path.splitext(os.path.basename(filepath))[0]
    env = {**os.environ}
    try:
        r = subprocess.run([
            'npx', 'wrangler', 'r2', 'object', 'put',
            f'the-signal-audio/v2/{slug}.mp3',
            '--file', filepath, '--remote'
        ], capture_output=True, text=True, timeout=45,
           cwd=str(ROOT), env=env)
        if r.returncode == 0:
            print(f"  📤 Uploaded: {slug}")
            return True
        else:
            print(f"  ❌ Upload failed [{slug}]: {r.stderr[:120]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏰ Timeout: {slug}")
        return False
    except Exception as e:
        print(f"  ❌ Error {slug}: {e}")
        return False

async def main():
    print("🎙️  Checking latest 5 articles for Andrew TTS...\n")

    results = {}
    for slug in LATEST:
        fp = await gen_one(slug)
        results[slug] = fp
        await asyncio.sleep(0.2)

    print("\n── Upload phase ──")
    generated = []
    skipped = []
    for slug in LATEST:
        fp = results[slug]
        if fp:
            # Check if already in cache (wasn't freshly generated)
            jf = POSTS_DIR / f'{slug}.json'
            with open(jf) as f:
                article = json.load(f)
            gen_time = os.path.getmtime(fp)
            json_time = os.path.getmtime(jf)
            is_fresh = gen_time >= json_time - 60  # generated after the json was last touched
            # Actually, better: if file existed before we ran, it's a skip
            # We already printed "Already cached" vs "Generated" above
            # Let's just upload all that exist and report
            ok = upload_one(fp)
            if ok:
                generated.append(slug)
            else:
                # still count as attempted
                generated.append(f"{slug} (upload failed)")
        else:
            skipped.append(slug)
        time.sleep(1.5)

    print("\n═══════════════════════════════════════")
    print(f"✅ Generated & uploaded: {len([s for s in generated if '(upload failed)' not in s])}")
    for s in generated:
        print(f"   • {s}")
    print(f"⏭️  Skipped (no content to generate): {len(skipped)}")
    for s in skipped:
        print(f"   • {s}")
    print("═══════════════════════════════════════")

if __name__ == '__main__':
    asyncio.run(main())
