#!/usr/bin/env python3
"""Generate Andrew TTS audio for articles published in the last 48 hours and upload to R2."""
import asyncio, edge_tts, json, os, sys, re, time
import urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path("/home/chino/thesignal")
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 300
os.makedirs(TMP_DIR, exist_ok=True)

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


def parse_date(date_str):
    """Parse article date string to timezone-aware datetime."""
    if not date_str:
        return None
    try:
        ds = date_str.replace("Z", "+00:00")
        pub_date = datetime.fromisoformat(ds)
        if pub_date.tzinfo is None:
            pub_date = pub_date.replace(tzinfo=timezone.utc)
        return pub_date
    except ValueError:
        pass
    try:
        pub_date = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return pub_date
    except ValueError:
        return None


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
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

    recent = []
    for jf in sorted(POSTS_DIR.glob("*.json")):
        with open(jf) as f:
            article = json.load(f)
        pub_date = parse_date(article.get("date", ""))
        if pub_date and pub_date >= cutoff:
            recent.append(article)

    print(f"Articles in last 48h: {len(recent)}", flush=True)
    if not recent:
        print("No recent articles to process.", flush=True)
        return []

    for a in recent:
        print(f"  {a.get('date','?')}  {a.get('slug','?')}", flush=True)

    gen_ok = gen_skip = gen_fail = 0
    for article in recent:
        slug = article.get("slug", "")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
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
            continue

        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            print(f"  GEN OK {slug}", flush=True)
        except asyncio.TimeoutError:
            gen_fail += 1
            if os.path.exists(out_path):
                os.unlink(out_path)
            print(f"  TIMEOUT {slug}", flush=True)
        except Exception as e:
            gen_fail += 1
            print(f"  ERROR {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)

    print(f"Generation: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)
    return list(Path(TMP_DIR).glob("*.mp3"))


def upload_all(mp3_files):
    total = len(mp3_files)
    if not total:
        print("No MP3s to upload.", flush=True)
        return

    print(f"Uploading {total} MP3s to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
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
                print(f"  Uploaded {slug}", flush=True)
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

    print(f"Upload: OK={ok} Failed={fail}", flush=True)
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up.", flush=True)


if __name__ == "__main__":
    mp3s = asyncio.run(main())
    if mp3s:
        upload_all(mp3s)
    else:
        print("No MP3s to upload.", flush=True)
