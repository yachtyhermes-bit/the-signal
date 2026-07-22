#!/usr/bin/env python3
"""Generate Andrew TTS for articles published in the last 48 hours and upload to R2."""
import asyncio, edge_tts, json, os, sys, re, urllib.request, urllib.error, time
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
GEN_TIMEOUT = 120
TMP_DIR = "/tmp/signal-tts"
BUCKET = "the-signal-audio"
os.makedirs(TMP_DIR, exist_ok=True)

now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=48)

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

def parse_date(date_str):
    if not date_str:
        return None
    date_str = date_str.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except:
        return None

async def main():
    json_files = sorted(ROOT.glob("articles/posts/*.json"))
    
    # Filter recent articles
    recent_slugs = []
    for jf in json_files:
        with open(jf) as f:
            article = json.load(f)
        dt = parse_date(article.get("date", ""))
        if dt and dt >= cutoff:
            slug = article.get("slug", "")
            if slug:
                recent_slugs.append((slug, article, jf))
    
    if not recent_slugs:
        print("No articles published in the last 48 hours.")
        return
    
    print(f"Found {len(recent_slugs)} articles from last 48 hours:")
    for slug, article, _ in recent_slugs:
        print(f"  {slug}  (date={article.get('date')})")
    
    gen_ok = gen_skip = gen_fail = 0
    mp3_files = []
    
    for slug, article, _ in recent_slugs:
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            mp3_files.append(Path(out_path))
            print(f"  SKIP {slug} (already exists)")
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
            print(f"  SKIP {slug} (text too short)")
            continue
        
        print(f"  GEN  {slug}...", end=" ", flush=True)
        try:
            await asyncio.wait_for(
                generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
            )
            gen_ok += 1
            mp3_files.append(Path(out_path))
            print("OK")
        except asyncio.TimeoutError:
            gen_fail += 1
            if os.path.exists(out_path):
                os.unlink(out_path)
            print("TIMEOUT")
        except Exception as e:
            gen_fail += 1
            print(f"ERROR: {e}")
    
    print(f"\nGenerated: OK={gen_ok} Skip={gen_skip} Fail={gen_fail}")
    
    if not mp3_files:
        print("No MP3s to upload.")
        return
    
    # Upload to R2
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    
    if not token or not acct:
        print("ERROR: CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set")
        sys.exit(1)
    
    print(f"Uploading {len(mp3_files)} files to R2 bucket '{BUCKET}'...")
    upload_ok = upload_fail = 0
    
    for filepath in mp3_files:
        slug = filepath.stem
        key = f"v2/{slug}.mp3"
        try:
            data = filepath.read_bytes()
            url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/{BUCKET}/objects/{key}"
            req = urllib.request.Request(url, data=data, method="PUT")
            req.add_header("Authorization", f"Bearer {token}")
            req.add_header("Content-Type", "audio/mpeg")
            resp = urllib.request.urlopen(req, timeout=45)
            if resp.status == 200:
                upload_ok += 1
                filepath.unlink()
                print(f"  UPLOAD OK {slug}")
            else:
                upload_fail += 1
                print(f"  UPLOAD FAIL {slug}: HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            upload_fail += 1
            print(f"  HTTP {e.code} {slug}")
        except Exception as e:
            upload_fail += 1
            print(f"  ERROR {slug}: {e}")
        time.sleep(0.5)
    
    print(f"\nUpload complete: OK={upload_ok} Failed={upload_fail}")
    
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Temp files cleaned up.")
    
    return gen_ok, gen_skip, gen_fail, upload_ok, upload_fail

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        gen_ok, gen_skip, gen_fail, upload_ok, upload_fail = result
        if gen_ok > 0:
            print(f"\nSUMMARY: {gen_ok} new MP3s generated and uploaded to R2.")
            print(f"  Generated: {gen_ok} new, {gen_skip} skipped, {gen_fail} failed")
            print(f"  Uploaded: {upload_ok} OK, {upload_fail} failed")
