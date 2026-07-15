#!/usr/bin/env python3
"""Generate Andrew TTS for the 4 fresh articles found in last 48h, upload to R2."""
import asyncio, edge_tts, json, os, sys, time, re, glob
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
DEV_VARS = ROOT / ".dev.vars"
if DEV_VARS.exists():
    for _line in DEV_VARS.read_text().splitlines():
        _line = _line.strip()
        if "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            _v = _v.strip().strip(chr(34)).strip(chr(39))
            if _k == "CLOUDFLARE_API_TOKEN" and not os.environ.get("CLOUDFLARE_API_TOKEN", ""):
                os.environ["CLOUDFLARE_API_TOKEN"] = _v
            if _k == "CLOUDFLARE_ACCOUNT_ID" and not os.environ.get("CLOUDFLARE_ACCOUNT_ID", ""):
                os.environ["CLOUDFLARE_ACCOUNT_ID"] = _v

TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 120
os.makedirs(TMP_DIR, exist_ok=True)

FRESH_SLUGS = [
    "arista-networks-nvidia-paradox-ai-2026",
    "axon-ai-policing-moat-2026",
    "northrop-grumman-defense-backlog-moat-2026",
    "salesforce-agentforce-ai-growth-2026",
]

async def generate_one(slug, text, out_path):
    communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
    with open(out_path, "wb") as fout:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fout.write(chunk["data"])
    if os.path.getsize(out_path) > 500:
        return True
    os.unlink(out_path)
    return False

async def main():
    gen_ok = gen_fail = gen_skip = 0
    for slug in FRESH_SLUGS:
        jf = POSTS_DIR / f"{slug}.json"
        if not jf.exists():
            print(f"MISSING: {slug}.json")
            gen_fail += 1
            continue
        with open(jf) as f:
            article = json.load(f)
        print(f"[{slug}] date={article.get('date','?')}", flush=True)

        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            print(f"  SKIP (already exists in tmp)", flush=True)
            gen_skip += 1
            continue

        title = article.get("title", "")
        body_html = article.get("bodyHtml", "")
        if body_html:
            text = re.sub(r"<[^>]+>", " ", body_html)
            for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                         ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
                text = text.replace(a, b)
            text = re.sub(r"\s+", " ", text).strip()
            text = f"{title}. {text}"
        else:
            text = f"{title}. {article.get('summary', '')}"

        if len(text) < 50:
            print(f"  SKIP (text too short: {len(text)} chars)")
            gen_skip += 1
            continue

        try:
            print(f"  Generating TTS ({len(text[:MAX_CHARS])} chars)...", flush=True)
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            print(f"  OK: {slug}.mp3 ({os.path.getsize(out_path)} bytes)", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            print(f"  TIMEOUT {slug}", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"  ERROR {slug}: {e}", flush=True)

        await asyncio.sleep(0.1)

    print(f"\nTTS Gen: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)

    # Upload
    mp3_files = sorted(Path(TMP_DIR).glob("*.mp3"))
    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return

    print(f"Upload {len(mp3_files)} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("  CREDS MISSING: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return

    up_ok = up_fail = 0
    bucket = "the-signal-audio"
    for filepath in mp3_files:
        slug = filepath.stem
        key = f"v2/{slug}.mp3"
        try:
            data = filepath.read_bytes()
            url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/{bucket}/objects/{key}"
            req = urllib.request.Request(url, data=data, method="PUT")
            req.add_header("Authorization", f"Bearer {token}")
            req.add_header("Content-Type", "audio/mpeg")
            resp = urllib.request.urlopen(req, timeout=45)
            if resp.status == 200:
                up_ok += 1
                print(f"  UPLOAD OK: {key}", flush=True)
                filepath.unlink()
            else:
                up_fail += 1
                print(f"  Upload fail {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            up_fail += 1
            print(f"  HTTP {e.code} {slug}: {e.read().decode()[:200]}", flush=True)
        except Exception as e:
            up_fail += 1
            print(f"  Upload err {slug}: {e}", flush=True)
        time.sleep(0.5)

    print(f"Upload: OK={up_ok} Failed={up_fail}", flush=True)

    # Cleanup leftovers
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
