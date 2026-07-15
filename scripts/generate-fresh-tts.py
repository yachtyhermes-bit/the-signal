#!/usr/bin/env python3
"""Generate Andrew TTS for articles from the last 48 hours and upload to R2."""
import asyncio, edge_tts, json, os, sys, time, glob, re, datetime
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

now = datetime.datetime.now(datetime.timezone.utc)
cutoff = now - datetime.timedelta(hours=48)

recent_articles = []
for jf in sorted(POSTS_DIR.glob("*.json")):
    with open(jf) as f:
        article = json.load(f)
    date_str = article.get("date", "")
    if not date_str:
        continue
    try:
        dt = datetime.datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
    except:
        continue
    if dt >= cutoff:
        recent_articles.append(article)

if not recent_articles:
    print("No fresh articles in last 48h. Nothing to do.", flush=True)
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
    print(f"Found {len(recent_articles)} fresh articles (since {cutoff.isoformat()})", flush=True)
    gen_ok = gen_skip = gen_fail = 0
    mp3_files = []
    for article in recent_articles:
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            mp3_files.append(Path(out_path))
            print(f"  [skip] {slug} (already exists)", flush=True)
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
            print(f"  [skip] {slug} (text too short)", flush=True)
            continue
        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            mp3_files.append(Path(out_path))
            print(f"  [ok] {slug}", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            print(f"  [timeout] {slug}", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"  [error] {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)
    print(f"  OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)
    return mp3_files

def upload_all(mp3_files):
    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return 0, 0
    total = len(mp3_files)
    print(f"Upload {total} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("  CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return 0, total
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
                print(f"  [uploaded] {slug}", flush=True)
            else:
                fail += 1
                print(f"  [upload fail] {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            fail += 1
            print(f"  [HTTP {e.code}] {slug}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  [upload err] {slug}: {e}", flush=True)
        time.sleep(0.5)
    print(f"  Uploaded={ok} Failed={fail}", flush=True)
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up", flush=True)
    return ok, fail

if __name__ == "__main__":
    mp3s = asyncio.run(gen_fresh())
    ok, fail = upload_all(mp3s)
    print(f"\nDONE: {ok} generated & uploaded, {fail} failed", flush=True)
