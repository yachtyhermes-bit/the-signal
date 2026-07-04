#!/usr/bin/env python3
"""Generate Andrew TTS for specific missing slugs and upload to R2."""
import asyncio, edge_tts, json, os, subprocess, re, urllib.request

VOICE = 'en-US-AndrewNeural'
MAX_CHARS = 5000
TMP = '/tmp/signal-tts'
os.makedirs(TMP, exist_ok=True)

# Read token from .dev.vars
token = ''
account_id = 'a0b3e792abdcd46a7614dc201ff2170f'
bucket = 'the-signal-audio'

with open('/home/chino/thesignal/.dev.vars') as f:
    for line in f:
        if 'CLOUDFLARE_API_TOKEN' in line:
            raw = line.strip().split('=', 1)[1].strip()
            token = raw.strip("'\"").strip()
            break

if not token:
    print("ERROR: No CLOUDFLARE_API_TOKEN found")
    exit(1)

SLUGS = [
    'microsoft-azure-ai-copilot-enterprise-2026',
    'marvell-ai-custom-chips-data-center-2026',
]

async def gen_one(slug):
    jf = f'/home/chino/thesignal/articles/posts/{slug}.json'
    if not os.path.exists(jf):
        print(f'  SKIP {slug}: article JSON not found')
        return False
    with open(jf) as f:
        a = json.load(f)
    title = a.get('title', '')
    body = a.get('bodyHtml', '')
    text = re.sub(r'<[^>]+>', ' ', body)
    text = f'{title}. {text}'[:MAX_CHARS]
    
    out = os.path.join(TMP, f'{slug}.mp3')
    comm = edge_tts.Communicate(text, VOICE)
    with open(out, 'wb') as fo:
        async for chunk in comm.stream():
            if chunk['type'] == 'audio':
                fo.write(chunk['data'])
    sz = os.path.getsize(out)
    
    if sz < 500:
        print(f'  FAIL {slug}: too small ({sz} bytes)')
        return False
    
    # Upload using urllib (no token in command string)
    key = f'v2/{slug}.mp3'
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/buckets/{bucket}/objects/{key}'
    
    with open(out, 'rb') as fo:
        data = fo.read()
    
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'audio/mpeg')
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            status = resp.status
    except Exception as e:
        print(f'  UPLOAD FAIL {slug}: {e}')
        os.unlink(out)
        return False
    
    os.unlink(out)
    if status == 200:
        print(f'  OK {slug}: {sz} bytes → R2')
        return True
    else:
        print(f'  UPLOAD FAIL {slug}: HTTP {status}')
        return False

async def main():
    ok = 0
    for slug in SLUGS:
        print(f'Generating {slug}...')
        if await gen_one(slug):
            ok += 1
    print(f'\nDone: {ok}/{len(SLUGS)} uploaded')

if __name__ == '__main__':
    asyncio.run(main())
