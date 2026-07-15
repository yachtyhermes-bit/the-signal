#!/usr/bin/env python3
"""Generate TTS for all articles using edge-tts CLI subprocess with parallel workers."""

import subprocess, json, os, sys, re, time, glob, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
WORKERS = 4

os.makedirs(TMP_DIR, exist_ok=True)

def gen_one(slug, text):
    out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
        return ("skip", slug, 0)

    # Write text to temp file for edge-tts CLI
    text_path = f"/tmp/signal-tts-txt-{slug}.txt"
    with open(text_path, "w") as f:
        f.write(text[:5000])

    t0 = time.time()
    try:
        result = subprocess.run(
            ["edge-tts", "--voice", VOICE, "-f", text_path, "--write-media", out_path],
            capture_output=True, timeout=180
        )
        elapsed = time.time() - t0
        os.unlink(text_path)

        if result.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            return ("ok", slug, elapsed)
        if os.path.exists(out_path):
            os.unlink(out_path)
        return ("fail", slug, elapsed)
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        os.unlink(text_path)
        if os.path.exists(out_path):
            os.unlink(out_path)
        return ("fail", slug, elapsed)
    except Exception as e:
        elapsed = time.time() - t0
        if os.path.exists(text_path):
            os.unlink(text_path)
        return ("error", f"{slug}: {e}", elapsed)

def prepare_articles():
    """Build list of (slug, text) for articles needing TTS."""
    articles = []
    for jf in sorted(POSTS_DIR.glob("*.json")):
        with open(jf) as f:
            article = json.load(f)
        slug = article.get("slug", "")
        if not slug:
            continue

        out_path = os.path.join(TMP_DIR, f"{slug}.mp3")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
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
        articles.append((slug, text))

    return articles

def upload_all(mp3_files):
    total = len(mp3_files)
    if total == 0:
        print("No MP3s to upload", flush=True)
        return 0, 0

    print(f"\nUploading {total} files to R2...", flush=True)
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    acct = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
    if not token or not acct:
        dv = ROOT / ".dev.vars"
        if dv.exists():
            for _line in dv.read_text().splitlines():
                _line = _line.strip()
                if "=" in _line and not _line.startswith("#"):
                    _k, _v = _line.split("=", 1)
                    _k = _k.strip()
                    _v = _v.strip().strip(chr(34)).strip(chr(39))
                    if _k == "CLOUDFLARE_API_TOKEN":
                        token = _v
                    if _k == "CLOUDFLARE_ACCOUNT_ID":
                        acct = _v

    if not token or not acct:
        print("ERROR: Cloudflare credentials not available", flush=True)
        return 0, total

    ok = fail = 0
    bucket = "the-signal-audio"
    for i, fp in enumerate(mp3_files):
        slug = fp.stem
        key = f"v2/{slug}.mp3"
        try:
            data = fp.read_bytes()
            url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/r2/buckets/{bucket}/objects/{key}"
            req = urllib.request.Request(url, data=data, method="PUT")
            req.add_header("Authorization", f"Bearer {token}")
            req.add_header("Content-Type", "audio/mpeg")
            resp = urllib.request.urlopen(req, timeout=45)
            if resp.status == 200:
                ok += 1
                fp.unlink()
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
            print(f"  Uploaded {ok}/{i+1}", flush=True)
        time.sleep(0.3)

    print(f"Upload done: OK={ok} Fail={fail}", flush=True)
    return ok, fail

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", default="all", choices=["gen", "upload", "all"])
    parser.add_argument("--workers", type=int, default=WORKERS)
    args = parser.parse_args()

    if args.action in ("gen", "all"):
        articles = prepare_articles()
        total = len(articles)
        if total == 0:
            print("All articles already have MP3s generated!", flush=True)
        else:
            print(f"Generating TTS for {total} articles with {args.workers} workers...", flush=True)
            ok = skip = fail = 0
            t0 = time.time()

            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(gen_one, slug, text): slug for slug, text in articles}
                done = 0
                for f in as_completed(futures):
                    status, slug, elapsed = f.result()
                    if status == "ok":
                        ok += 1
                    elif status == "skip":
                        skip += 1
                    else:
                        fail += 1
                    done += 1
                    if done % 20 == 0 or done == total:
                        rate = done / (time.time() - t0)
                        eta = (total - done) / rate if rate > 0 else 0
                        print(f"  [{done}/{total}] ok={ok} skip={skip} fail={fail} | {rate:.1f}/s | ETA {eta:.0f}s", flush=True)

            elapsed = time.time() - t0
            print(f"\nGeneration complete: OK={ok} Skip={skip} Fail={fail} in {elapsed:.0f}s", flush=True)

    if args.action in ("upload", "all"):
        mp3_files = sorted(Path(TMP_DIR).glob("*.mp3"))
        total = len(mp3_files)
        print(f"\nTotal MP3s ready for upload: {total}", flush=True)
        ok, fail = upload_all(mp3_files)
        print(f"Upload summary: OK={ok} Fail={fail}", flush=True)

if __name__ == "__main__":
    main()
