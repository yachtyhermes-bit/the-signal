#!/usr/bin/env python3
"""Upload ALL valid MP3s from /tmp/signal-tts/ to R2 bucket the-signal-audio/v2/.
Use as a dedicated upload step after generating TTS via individual one-shot calls.

Usage:
    python3 scripts/tts-upload.py

Uploads every .mp3 in /tmp/signal-tts/ larger than 500 bytes to
v2/{slug}.mp3 in R2. Deletes local files on successful upload.
"""
import os, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = "/tmp/signal-tts"

# Load credentials from .dev.vars
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

token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
if not token or not acct:
    print("CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
    sys.exit(1)

mp3_files = list(Path(TMP_DIR).glob("*.mp3"))
mp3_files = [f for f in mp3_files if f.stat().st_size > 500]
if not mp3_files:
    print("No MP3s to upload", flush=True)
    sys.exit(0)

print(f"Uploading {len(mp3_files)} files to R2...", flush=True)
ok = fail = 0
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
            ok += 1
            filepath.unlink()
            print(f"  OK {slug}", flush=True)
        else:
            fail += 1
            print(f"  FAIL {slug}: HTTP {resp.status}", flush=True)
    except urllib.error.HTTPError as e:
        fail += 1
        print(f"  HTTP {e.code} {slug}", flush=True)
    except Exception as e:
        fail += 1
        print(f"  ERR {slug}: {e}", flush=True)
    time.sleep(0.3)

print(f"\nUpload complete: OK={ok} Failed={fail}", flush=True)
if ok:
    remaining = list(Path(TMP_DIR).glob("*.mp3"))
    if remaining:
        for f in remaining:
            f.unlink()
        print(f"Cleaned {len(remaining)} leftover files", flush=True)
