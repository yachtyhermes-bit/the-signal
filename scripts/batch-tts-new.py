#!/usr/bin/env python3
"""Generate Andrew TTS for new (last 48h) articles only and upload to R2."""
import asyncio, edge_tts, json, os, sys, time, glob, re
import urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"

# Load R2 creds
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


def get_new_articles():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    articles = []
    for jf in sorted(POSTS_DIR.glob("*.json")):
        with open(jf) as f:
            article = json.load(f)
        date_str = article.get("date", "")
        if not date_str:
            continue
        dt = None
        for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ',
                     '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d', '%B %d, %Y']:
            try:
                dt = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
                break
            except ValueError:
                pass
        if dt is None:
            continue
        if dt >= cutoff:
            articles.append(article)
    return articles


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


def extract_text(article):
    title = article.get("title", "")
    body_html = article.get("bodyHtml", "")
    if body_html:
        text = re.sub(r"<[^>]+>", " ", body_html)
        for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                     ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
            text = text.replace(a, b)
        text = re.sub(r"\s+", " ", text).strip()
        return f"{title}. {text}"
    else:
        return f"{title}. {article.get('summary', '')}"


async def main():
    new_articles = get_new_articles()
    print(f"Found {len(new_articles)} new articles in last 48h")
    if not new_articles:
        print("No new articles to process.")
        return

    gen_ok = gen_fail = gen_skip = 0
    for article in new_articles:
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            print(f"  SKIP {slug} (already exists)")
            continue

        text = extract_text(article)
        if len(text) < 50:
            print(f"  SKIP {slug} (text too short)")
            continue

        print(f"  Generating {slug}...", end=" ", flush=True)
        try:
            await asyncio.wait_for(generate_one(slug, text, out_path), timeout=GEN_TIMEOUT)
            gen_ok += 1
            print(f"OK ({os.path.getsize(out_path)/1024:.0f} KB)")
        except asyncio.TimeoutError:
            gen_fail += 1
            print("TIMEOUT")
            if os.path.exists(out_path):
                os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"ERROR: {e}")

    print(f"\nGeneration: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}")

    # Upload
    mp3_files = [f for f in Path(TMP_DIR).glob("*.mp3") if f.stat().st_size > 500]
    if not mp3_files:
        print("No MP3s to upload")
        return

    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("ERROR: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set")
        return

    upload_ok = upload_fail = 0
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
                upload_ok += 1
                filepath.unlink()
                print(f"  Uploaded {slug}.mp3")
            else:
                upload_fail += 1
                print(f"  Upload FAIL {slug}: HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            upload_fail += 1
            print(f"  HTTP {e.code} {slug}")
        except Exception as e:
            upload_fail += 1
            print(f"  Upload err {slug}: {e}")
        time.sleep(0.5)

    print(f"Upload: OK={upload_ok} Failed={upload_fail}")

    # Cleanup
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up temp files")

if __name__ == "__main__":
    asyncio.run(main())
