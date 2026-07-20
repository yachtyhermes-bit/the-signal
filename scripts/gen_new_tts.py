#!/usr/bin/env python3
"""Generate Andrew TTS for new articles (48h) and upload to R2. Longer timeout."""
import asyncio, edge_tts, json, os, sys, time, re, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path("/home/chino/thesignal")
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 600
os.makedirs(TMP_DIR, exist_ok=True)

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
bucket = "the-signal-audio"

cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
new_articles = []
for jf in sorted(POSTS_DIR.glob("*.json")):
    with open(jf) as f:
        article = json.load(f)
    date_str = article.get("date")
    if not date_str:
        continue
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    except:
        continue
    if dt >= cutoff:
        slug = article.get("slug")
        if slug:
            new_articles.append((slug, article))

print(f"New articles: {len(new_articles)}", flush=True)
for slug, _ in new_articles:
    print(f"  {slug}", flush=True)

async def generate_one(slug, text, out_path):
    communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
    with open(out_path, "wb") as fout:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fout.write(chunk["data"])
    return os.path.getsize(out_path) > 500

async def main():
    gen_ok = gen_fail = 0
    for slug, article in new_articles:
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
            print(f"  SKIP {slug} (short)", flush=True)
            continue
        try:
            ok = await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            if ok:
                gen_ok += 1
                print(f"  OK {slug} ({os.path.getsize(out_path)//1024}KB)", flush=True)
            else:
                gen_fail += 1
                print(f"  FAIL {slug} (small output)", flush=True)
        except Exception as e:
            gen_fail += 1
            print(f"  FAIL {slug}: {e}", flush=True)
        await asyncio.sleep(0.1)
    print(f"Gen: OK={gen_ok} Fail={gen_fail}", flush=True)
    return sorted(Path(TMP_DIR).glob("*.mp3"))

def upload_all(mp3_files):
    if not mp3_files:
        print("No MP3s to upload", flush=True)
        return 0, 0
    print(f"Upload {len(mp3_files)} files to R2...", flush=True)
    if not token or not acct:
        print("  Missing R2 credentials!", flush=True)
        return 0, 0
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
            resp = urllib.request.urlopen(req, timeout=60)
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
            print(f"  UPLOAD ERR {slug}: {e}", flush=True)
        time.sleep(0.5)
    return ok, fail

if __name__ == "__main__":
    mp3s = asyncio.run(main())
    upl_ok, upl_fail = upload_all(mp3s)
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print(f"Final: Generated={len(mp3s)} Uploaded={upl_ok} Failed={upl_fail}", flush=True)
