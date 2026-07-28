#!/usr/bin/env python3
"""Generate Andrew TTS for only recent articles and upload to R2."""
import asyncio, edge_tts, json, os, sys, time, re
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

cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
recent_articles = []

for jf in sorted(POSTS_DIR.glob("*.json")):
    with open(jf) as f:
        article = json.load(f)
    date_str = article.get("date", "")
    if not date_str:
        continue
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt >= cutoff:
            recent_articles.append(article)
    except:
        pass

print(f"Found {len(recent_articles)} recent articles", flush=True)
for a in recent_articles:
    print(f"  {a.get('slug')} ({a.get('date')})", flush=True)

if not recent_articles:
    print("No recent articles to process.", flush=True)
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

async def gen_all():
    gen_ok = gen_fail = gen_skip = 0
    for article in recent_articles:
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            print(f"  Skip {slug} (exists)", flush=True)
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
            sz = os.path.getsize(out_path)
            print(f"  OK {slug}.mp3 ({sz} bytes)", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            if os.path.exists(out_path):
                os.unlink(out_path)
            print(f"  TO {slug}", flush=True)
        except Exception as e:
            gen_fail += 1
            print(f"  ERR {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)
    print(f"Gen done: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)
    slugs = {a.get("slug") for a in recent_articles if a.get("slug")}
    return [m for m in Path(TMP_DIR).glob("*.mp3") if m.stem in slugs]

def upload_all(mp3_files):
    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return
    total = len(mp3_files)
    print(f"Upload {total} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("  Missing R2 credentials", flush=True)
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
                print(f"  HTTP {resp.status} {slug}", flush=True)
        except urllib.error.HTTPError as e:
            fail += 1
            print(f"  HTTP {e.code} {slug}", flush=True)
        except Exception as e:
            fail += 1
            print(f"  ERR {slug}: {e}", flush=True)
        time.sleep(0.5)
    print(f"Upload done: OK={ok} Failed={fail}", flush=True)
    slugs = {a.get("slug") for a in recent_articles if a.get("slug")}
    for f in Path(TMP_DIR).glob("*.mp3"):
        if f.stem in slugs:
            try:
                f.unlink()
            except:
                pass

if __name__ == "__main__":
    mp3s = asyncio.run(gen_all())
    upload_all(mp3s)
