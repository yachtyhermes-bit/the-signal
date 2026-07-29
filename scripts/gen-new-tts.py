#!/usr/bin/env python3
"""Generate Andrew TTS for the 7 new articles (last 48h) and upload to R2."""
import asyncio, edge_tts, json, os, sys, time, glob, re, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 120

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

os.makedirs(TMP_DIR, exist_ok=True)

NEW_SLUGS = [
    "coin-everything-platform-2026",
    "crdo-ai-networking-dominance-2026",
    "ionq-quantum-computing-momentum-2026",
    "nbis-europe-sovereign-ai-moat-2026",
    "rtx-iran-war-backlog-supercycle-2026",
    "smci-margin-turnaround-ai-server-2026",
    "vst-nuclear-meta-pjm-rebound-2026",
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
    gen_ok = gen_skip = gen_fail = 0
    for slug in NEW_SLUGS:
        jf = POSTS_DIR / f"{slug}.json"
        if not jf.exists():
            print(f"  SKIP {slug}: JSON not found", flush=True)
            gen_skip += 1
            continue
        with open(jf) as f:
            article = json.load(f)
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            print(f"  SKIP {slug}: MP3 exists", flush=True)
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
            print(f"  SKIP {slug}: text too short", flush=True)
            gen_skip += 1
            continue
        print(f"  GEN {slug}...", flush=True)
        try:
            await asyncio.wait_for(generate_one(slug, text, out_path), timeout=GEN_TIMEOUT)
            gen_ok += 1
            print(f"    OK ({os.path.getsize(out_path)} bytes)", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            print(f"    TIMEOUT", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"    ERROR: {e}", flush=True)
        await asyncio.sleep(0.1)

    print(f"\nGeneration: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)

    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("R2 creds not set, skipping upload", flush=True)
        return

    mp3_files = []
    for slug in NEW_SLUGS:
        p = Path(TMP_DIR) / f"{slug}.mp3"
        if p.exists() and p.stat().st_size > 500:
            mp3_files.append(p)

    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return

    bucket = "the-signal-audio"
    ok = fail = 0
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
                ok += 1
                filepath.unlink()
                print(f"  UPLOAD OK {slug}", flush=True)
            else:
                fail += 1
                print(f"  UPLOAD FAIL {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            fail += 1
            print(f"  HTTP {e.code} {slug}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  Upload err {slug}: {e}", flush=True)
        time.sleep(0.5)

    print(f"\nUpload: OK={ok} Failed={fail}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
