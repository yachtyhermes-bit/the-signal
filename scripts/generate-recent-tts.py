#!/usr/bin/env python3
"""Generate Andrew TTS for articles from the last 48 hours and upload to R2."""
import asyncio, edge_tts, json, os, re, urllib.request, urllib.error, time, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 120
ROOT = Path("/home/chino/thesignal")
POSTS_DIR = ROOT / "articles" / "posts"

os.makedirs(TMP_DIR, exist_ok=True)

# Read credentials from .dev.vars
DEV_VARS = ROOT / ".dev.vars"
if DEV_VARS.exists():
    for line in DEV_VARS.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "CLOUDFLARE_API_TOKEN" and not os.environ.get("CLOUDFLARE_API_TOKEN", ""):
                os.environ["CLOUDFLARE_API_TOKEN"] = v
            if k == "CLOUDFLARE_ACCOUNT_ID" and not os.environ.get("CLOUDFLARE_ACCOUNT_ID", ""):
                os.environ["CLOUDFLARE_ACCOUNT_ID"] = v


def get_recent_articles():
    """Filter articles from the last 48 hours."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=48)
    recent = []
    for jf in sorted(POSTS_DIR.glob("*.json")):
        with open(jf) as f:
            article = json.load(f)
        date_str = article.get("date", "")
        if not date_str:
            continue
        if date_str.endswith("Z"):
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        elif "T" in date_str:
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        if dt >= cutoff:
            recent.append((dt, article))
    return recent


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


async def gen_all(recent_articles):
    gen_ok = gen_fail = 0
    for dt, article in sorted(recent_articles, key=lambda x: (x[0], x[1].get("slug", ""))):
        slug = article.get("slug", "")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")

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
            print(f"  Skip {slug}: text too short", flush=True)
            continue

        print(f"  Generating TTS: {slug} ({len(text[:MAX_CHARS])} chars)...", flush=True)
        try:
            await asyncio.wait_for(generate_one(slug, text, out_path), timeout=GEN_TIMEOUT)
            gen_ok += 1
            print(f"  OK: {slug} ({os.path.getsize(out_path)} bytes)", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            print(f"  TIMEOUT: {slug}", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"  ERROR {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)

    print(f"\nGeneration done: {gen_ok} OK, {gen_fail} Failed", flush=True)
    return list(Path(TMP_DIR).glob("*.mp3"))


def upload_all(mp3_files):
    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return

    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("ERROR: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return

    print(f"Uploading {len(mp3_files)} files to R2...", flush=True)
    bucket = "the-signal-audio"
    up_ok = up_fail = 0
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
                filepath.unlink()
                print(f"  Uploaded: {slug}", flush=True)
            else:
                up_fail += 1
                print(f"  Upload fail {slug}: HTTP {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            up_fail += 1
            print(f"  HTTP {e.code} {slug}", flush=True)
        except Exception as e:
            up_fail += 1
            print(f"  Upload err {slug}: {e}", flush=True)
        time.sleep(0.5)

    print(f"\nUploaded={up_ok} Failed={up_fail}", flush=True)
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up", flush=True)


async def main():
    recent_articles = get_recent_articles()
    print(f"Found {len(recent_articles)} articles from last 48h", flush=True)
    if not recent_articles:
        print("No new articles to process", flush=True)
        return
    for dt, article in recent_articles:
        slug = article.get("slug", "?")
        print(f"  {dt.date()} - {slug} - {article.get('title', '')[:60]}", flush=True)

    mp3s = await gen_all(recent_articles)
    upload_all(mp3s)


if __name__ == "__main__":
    asyncio.run(main())
