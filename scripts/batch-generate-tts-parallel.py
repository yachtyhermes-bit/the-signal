#!/usr/bin/env python3
"""Batch generate Andrew TTS for all articles and upload to R2 (parallel version)."""
import asyncio, edge_tts, json, os, sys, time, glob, re, urllib.request, urllib.error
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
PARALLEL = 5  # generate up to 5 concurrently
os.makedirs(TMP_DIR, exist_ok=True)

def text_from_article(article):
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
    return text

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

async def gen_one_with_timeout(slug, text, out_path):
    try:
        return await asyncio.wait_for(
            generate_one(slug, text, out_path), timeout=GEN_TIMEOUT
        )
    except asyncio.TimeoutError:
        if os.path.exists(out_path):
            os.unlink(out_path)
        return False
    except Exception:
        if os.path.exists(out_path):
            os.unlink(out_path)
        return False

async def gen_batch(batch):
    """Generate TTS for a batch of articles in parallel."""
    tasks = []
    for slug, text, out_path in batch:
        tasks.append(gen_one_with_timeout(slug, text, out_path))
    results = await asyncio.gather(*tasks)
    ok = sum(1 for r in results if r is True)
    fail = sum(1 for r in results if r is False)
    return ok, fail

async def gen_all():
    json_files = sorted(POSTS_DIR.glob("*.json"))
    total = len(json_files)
    print(f"Gen TTS for {total} articles (parallel={PARALLEL})...", flush=True)

    gen_ok = gen_skip = gen_fail = 0
    batch = []
    batch_slugs = set()

    # First pass: determine what needs generating
    for jf in json_files:
        with open(jf) as f:
            article = json.load(f)
        slug = article.get("slug")
        if not slug:
            continue
        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            gen_skip += 1
            continue
        text = text_from_article(article)
        if len(text) < 50:
            print(f"  Skip {slug}: text too short", flush=True)
            continue
        batch.append((slug, text, out_path))
        batch_slugs.add(slug)

        if len(batch) >= PARALLEL:
            ok, fail = await gen_batch(batch)
            gen_ok += ok
            gen_fail += fail
            elapsed = gen_ok + gen_fail + gen_skip
            print(f"  {gen_ok} ok, {gen_fail} fail, {gen_skip} skip ({elapsed}/{total})", flush=True)
            batch = []

    # Remaining
    if batch:
        ok, fail = await gen_batch(batch)
        gen_ok += ok
        gen_fail += fail

    elapsed = gen_ok + gen_fail + gen_skip
    print(f"  Done: OK={gen_ok} Skip={gen_skip} Fail={gen_fail} Total={elapsed}", flush=True)
    return list(Path(TMP_DIR).glob("*.mp3"))

def upload_all(mp3_files):
    total = len(mp3_files)
    print(f"Upload {total} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        print("  CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set", flush=True)
        return 0, 0
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
    for f in Path(TMP_DIR).glob("*.mp3"):
        f.unlink()
    print("Cleaned up", flush=True)
    return ok, fail

if __name__ == "__main__":
    mp3s = asyncio.run(gen_all())
    if mp3s:
        upload_all(mp3s)
    else:
        print("No MP3s to upload", flush=True)
