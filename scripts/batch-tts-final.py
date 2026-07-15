#!/usr/bin/env python3
"""Generate TTS for ALL 224 articles sequentially with checkpointing, then upload all to R2."""

import asyncio, edge_tts, json, os, sys, re, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "articles" / "posts"
TMP_DIR = "/tmp/signal-tts"
VOICE = "en-US-AndrewNeural"
MAX_CHARS = 5000
CHECKPOINT = "/tmp/signal-tts-checkpoint.json"

os.makedirs(TMP_DIR, exist_ok=True)

async def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    # Step 1: generate missing
    if action in ("gen", "all"):
        # Load checkpoint
        start_from = 0
        if os.path.exists(CHECKPOINT):
            try:
                cp = json.load(open(CHECKPOINT))
                start_from = cp.get("next_index", 0)
                print(f"Resuming from index {start_from}", flush=True)
            except:
                pass
        
        json_files = sorted(POSTS_DIR.glob("*.json"))
        total = len(json_files)
        gen_ok = 0
        gen_skip = 0
        gen_fail = 0
        
        for i in range(start_from, total):
            jf = json_files[i]
            with open(jf) as f:
                article = json.load(f)
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
                gen_skip += 1
                continue
            
            try:
                communicate = edge_tts.Communicate(text[:MAX_CHARS], VOICE)
                with open(out_path, "wb") as fout:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            fout.write(chunk["data"])
                if os.path.getsize(out_path) > 500:
                    gen_ok += 1
                else:
                    os.unlink(out_path)
                    gen_fail += 1
            except Exception as e:
                gen_fail += 1
                if os.path.exists(out_path):
                    os.unlink(out_path)
            
            # Checkpoint every 10 articles
            if (i + 1) % 10 == 0:
                json.dump({"next_index": i + 1}, open(CHECKPOINT, "w"))
                print(f"  [{i+1}/{total}] ok={gen_ok} skip={gen_skip} fail={gen_fail}", flush=True)
        
        # Final checkpoint
        json.dump({"next_index": total}, open(CHECKPOINT, "w"))
        
        mp3s = list(Path(TMP_DIR).glob("*.mp3"))
        print(f"Generation done: OK={gen_ok} Skip={gen_skip} Fail={gen_fail} TotalMP3s={len(mp3s)}", flush=True)
        
        if action == "gen":
            return
    
    # Step 2: upload to R2
    if action in ("upload", "all"):
        mp3_files = sorted(Path(TMP_DIR).glob("*.mp3"))
        total = len(mp3_files)
        if total == 0:
            print("No MP3s to upload", flush=True)
            return
        
        print(f"Uploading {total} files to R2...", flush=True)
        
        # Credentials
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
            return
        
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
        
        # Clean checkpoint
        if os.path.exists(CHECKPOINT):
            os.unlink(CHECKPOINT)
        
        # Cleanup any remaining mp3s
        for f in Path(TMP_DIR).glob("*.mp3"):
            f.unlink()
        print("Temp dir cleaned", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
