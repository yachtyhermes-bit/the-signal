#!/usr/bin/env python3
"""Batch generate Andrew TTS for all articles — chunked for foreground execution."""

import asyncio, edge_tts, json, os, sys, glob, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 150  # seconds per article
STATE_FILE = "/tmp/signal-tts-progress.json"

os.makedirs(TMP_DIR, exist_ok=True)

# Load how many we've already tried
state = {"generated": 0, "skipped": 0, "failed": 0, "last_index": -1}
if os.path.exists(STATE_FILE):
    try:
        state = json.load(open(STATE_FILE))
    except:
        pass

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

async def gen_chunk(start_idx):
    json_files = sorted(POSTS_DIR.glob("*.json"))
    total = len(json_files)
    gen_ok = state["generated"]
    gen_skip = state["skipped"]
    gen_fail = state["failed"]

    for i in range(start_idx, total):
        jf = json_files[i]
        with open(jf) as f:
            article = json.load(f)
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            state["skipped"] = gen_skip
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
            continue
        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            state["generated"] = gen_ok
        except asyncio.TimeoutError:
            gen_fail += 1
            state["failed"] = gen_fail
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            state["failed"] = gen_fail
        state["last_index"] = i
        json.dump(state, open(STATE_FILE, "w"))
        if (i + 1) % 25 == 0:
            print(f"  [{i+1}/{total}] ok={gen_ok} skip={gen_skip} fail={gen_fail}", flush=True)

    mp3s = list(Path(TMP_DIR).glob("*.mp3"))
    print(f"Generation complete: OK={gen_ok} Skip={gen_skip} Fail={gen_fail} TotalMP3s={len(mp3s)}", flush=True)
    return mp3s, gen_ok, gen_skip, gen_fail

def upload_all(mp3_files):
    total = len(mp3_files)
    if total == 0:
        print("No MP3s to upload", flush=True)
        return 0, 0
    print(f"Uploading {total} files to R2...", flush=True)

    # Read credentials from .dev.vars
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        dev_vars = ROOT / ".dev.vars"
        if dev_vars.exists():
            for _line in dev_vars.read_text().splitlines():
                _line = _line.strip()
                if "=" in _line and not _line.startswith("#"):
                    _k, _v = _line.split("=", 1)
                    _k = _k.strip()
                    _v = _v.strip().strip(chr(34)).strip(chr(39))
                    if _k == "CLOUDFLARE_API_TOKEN":
                        token = _v
                    if _k == "CLOUDFLARE_ACCOUNT_ID":
                        acct = _v
    if not token or not acct:
        print("  ERROR: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return 0, total

    ok = fail = 0
    import urllib.request, urllib.error
    bucket = "the-signal-audio"
    for i, filepath in enumerate(sorted(mp3_files)):
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
            else:
                fail += 1
                print(f"  Upload fail {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            fail += 1
            print(f"  HTTP {e.code} {slug}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  Upload err {slug}: {e}", flush=True)
        if (i + 1) % 25 == 0:
            print(f"  Uploaded {ok}/{i+1}", flush=True)
        time.sleep(0.3)
    print(f"Upload complete: OK={ok} Fail={fail}", flush=True)
    return ok, fail

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "gen"

    if action == "gen":
        start_idx = state["last_index"] + 1
        print(f"Starting from index {start_idx} (prev: gen={state['generated']} skip={state['skipped']} fail={state['failed']})", flush=True)
        mp3s, gok, gskip, gfail = asyncio.run(gen_chunk(start_idx))
        print(f"DONE: GenResult mp3s={len(mp3s)} ok={gok} skip={gskip} fail={gfail}", flush=True)

    elif action == "upload":
        mp3_files = sorted(Path(TMP_DIR).glob("*.mp3"))
        print(f"Uploading {len(mp3_files)} existing MP3s from {TMP_DIR}", flush=True)
        ok, fail = upload_all(mp3_files)
        print(f"DONE: UploadResult ok={ok} fail={fail}", flush=True)

    elif action == "all":
        # Generate then upload
        start_idx = state["last_index"] + 1
        print(f"Starting generation from index {start_idx}", flush=True)
        mp3s, gok, gskip, gfail = asyncio.run(gen_chunk(start_idx))
        print(f"Gen done: {len(mp3s)} mp3s, ok={gok} skip={gskip} fail={gfail}", flush=True)
        ok, fail = upload_all(mp3s)
        print(f"Upload done: ok={ok} fail={fail}", flush=True)
        if os.path.exists(STATE_FILE):
            os.unlink(STATE_FILE)

    else:
        print(f"Unknown action: {action}. Use: gen, upload, all", flush=True)
