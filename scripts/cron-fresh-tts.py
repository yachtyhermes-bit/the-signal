#!/usr/bin/env python3
"""Cron-friendly TTS: only process articles from the last 48 hours, then upload all to R2."""
import asyncio, edge_tts, json, os, sys, time, re, urllib.request, urllib.error
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
            _v = _v.strip().strip('"').strip("'")
            if _k == "CLOUDFLARE_API_TOKEN" and not os.environ.get("CLOUDFLARE_API_TOKEN", ""):
                os.environ["CLOUDFLARE_API_TOKEN"] = _v
            if _k == "CLOUDFLARE_ACCOUNT_ID" and not os.environ.get("CLOUDFLARE_ACCOUNT_ID", ""):
                os.environ["CLOUDFLARE_ACCOUNT_ID"] = _v

TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 120
CUTOFF = datetime.now(timezone.utc) - timedelta(hours=48)

os.makedirs(TMP_DIR, exist_ok=True)

def parse_article_date(date_str):
    """Parse article date string, always returning a timezone-aware datetime in UTC."""
    if not date_str:
        return None
    s = date_str.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def is_fresh(article):
    date_str = article.get("date", "") or ""
    dt = parse_article_date(date_str)
    if dt is None:
        return False
    return dt >= CUTOFF

def extract_text(article):
    title = article.get("title", "")
    body_html = article.get("bodyHtml", "")
    if body_html:
        text = re.sub(r"<[^>]+>", " ", body_html)
        for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                     ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")]:
            text = text.replace(a, b)
        text = re.sub(r"\s+", " ", text).strip()
        return f"{title}. {text}" if title else text
    summary = article.get("summary", "")
    return f"{title}. {summary}" if title else summary

async def generate_one(slug, text, out_path):
    communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
    with open(out_path, "wb") as fout:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fout.write(chunk["data"])
    if os.path.getsize(out_path) > 500:
        return True
    if os.path.exists(out_path):
        os.unlink(out_path)
    return False

async def main():
    json_files = sorted(POSTS_DIR.glob("*.json"))
    fresh = []
    for jf in json_files:
        with open(jf) as f:
            article = json.load(f)
        if is_fresh(article):
            fresh.append((jf, article))

    if not fresh:
        print(f"No fresh articles found (cutoff: {CUTOFF.isoformat()})", flush=True)
        # Still do opportunistic upload of any cached MP3s
        cached = list(Path(TMP_DIR).glob("*.mp3"))
        if cached:
            print(f"Uploading {len(cached)} pre-existing cached MP3s", flush=True)
            upload_all(cached)
        return

    print(f"Found {len(fresh)} fresh articles in last 48 hours", flush=True)
    gen_ok = gen_fail = gen_skip = 0

    for jf, article in fresh:
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            print(f"  SKIP {slug} (cached)", flush=True)
            continue

        text = extract_text(article)
        if len(text) < 50:
            print(f"  SKIP {slug} (text too short)", flush=True)
            continue

        char_count = len(text)
        print(f"  GEN  {slug} ({char_count} chars)...", flush=True)
        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            size = os.path.getsize(out_path)
            print(f"       {slug} OK ({size/1024:.0f} KB)", flush=True)
        except asyncio.TimeoutError:
            # Check if partial file is valid
            if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
                gen_ok += 1
                print(f"       {slug} OK (partial, {os.path.getsize(out_path)/1024:.0f} KB)", flush=True)
            else:
                gen_fail += 1
                timed_out_path = out_path
                if os.path.exists(timed_out_path):
                    os.unlink(timed_out_path)
                print(f"       {slug} TIMEOUT (retrying with 300s)...", flush=True)
                try:
                    await asyncio.wait_for(
                        generate_one(slug, text, out_path), timeout=300
                    )
                    gen_ok += 1
                    print(f"       {slug} OK on retry", flush=True)
                except asyncio.TimeoutError:
                    gen_fail += 1
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
                        gen_ok += 1
                        gen_fail -= 1
                        print(f"       {slug} OK (partial on retry, {os.path.getsize(out_path)/1024:.0f} KB)", flush=True)
                    else:
                        print(f"       {slug} FAIL (timeout on retry)", flush=True)
                        if os.path.exists(out_path):
                            os.unlink(out_path)
        except Exception as e:
            gen_fail += 1
            print(f"       {slug} ERROR: {e}", flush=True)
            if os.path.exists(out_path):
                os.unlink(out_path)

    print(f"Generation complete: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}", flush=True)

    # Upload all MP3s in TMP_DIR (new + any pre-existing cached)
    mp3s = sorted(Path(TMP_DIR).glob("*.mp3"))
    if mp3s:
        upload_all(mp3s)
    else:
        print("No MP3s to upload", flush=True)

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
    for i, filepath in enumerate(mp3_files):
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
            print(f"  {ok}/{i+1} uploaded", flush=True)
        time.sleep(0.3)
    print(f"  Uploaded={ok} Failed={fail}", flush=True)
    # Cleanup any remaining
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
