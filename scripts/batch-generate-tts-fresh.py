#!/usr/bin/env python3
"""Generate Andrew TTS for FRESH articles only (last 48h) and upload to R2."""
import asyncio, edge_tts, json, os, sys, time, glob, re
import urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

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

now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=48)

# Collect fresh articles only
fresh_articles = []
for jf in sorted(POSTS_DIR.glob("*.json")):
    with open(jf) as f:
        article = json.load(f)
    date_str = article.get("date", article.get("createdAt", ""))
    try:
        ds = date_str.replace("Z", "+00:00")
        article_dt = datetime.fromisoformat(ds)
        if article_dt.tzinfo is None:
            article_dt = article_dt.replace(tzinfo=timezone.utc)
        if article_dt >= cutoff:
            fresh_articles.append((jf, article))
    except Exception:
        pass

print(f"Fresh articles found: {len(fresh_articles)}", flush=True)
for jf, a in fresh_articles:
    print(f"  {a.get('slug', '?')}: {a.get('date', a.get('createdAt', '?'))}", flush=True)

if not fresh_articles:
    print("No fresh articles to process. Silent exit.", flush=True)
    sys.exit(0)

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

async def gen_fresh():
    gen_ok = gen_skip = gen_fail = 0
    for jf, article in fresh_articles:
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            print(f"  Skip {slug} (already exists)", flush=True)
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
            print(f"  Skip {slug} (text too short)", flush=True)
            continue
        print(f"  Generating TTS for {slug} ({len(text)} chars)...", flush=True)
        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            print(f"  OK {slug}", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            print(f"  Timeout {slug}", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"  Error {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)
    print(f"  Generated: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)
    return list(Path(TMP_DIR).glob("*.mp3"))

def upload_all(mp3_files):
    total = len(mp3_files)
    print(f"Upload {total} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("  CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return
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
                print(f"  Uploaded {slug}.mp3", flush=True)
            else:
                fail += 1
                print(f"  Upload fail {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            fail += 1
            print(f"  HTTP {e.code} {slug}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  Upload err {slug}: {e}", flush=True)
        time.sleep(0.5)
    print(f"  Uploaded={ok} Failed={fail}", flush=True)

# Generate and upload only the fresh MP3s generated in THIS run
fresh_mp3s = asyncio.run(gen_fresh())

# Detect which MP3s were actually generated this run (fresh articles only)
our_mp3s = []
for slug, _, _ in [(a.get("slug"), jf, a) for jf, a in fresh_articles]:
    f = Path(TMP_DIR) / f"{slug}.mp3"
    if f.exists() and f.stat().st_size > 500:
        our_mp3s.append(f)

if our_mp3s:
    upload_all(our_mp3s)
else:
    print("No MP3s to upload.", flush=True)

# Cleanup any leftover fresh article MP3s
for f in our_mp3s:
    if f.exists():
        f.unlink()
