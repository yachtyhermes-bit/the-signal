#!/usr/bin/env python3
"""
validate-blocklist.py — Check all published articles against the known meme/placeholder
YouTube ID blocklist. Auto-strips blocked video IDs (safe operation — videos are optional).
Non-zero exit if any article was modified so the deploy pipeline knows to rebuild.

Blocklist synced from: signal-article-publishing/references/known-placeholder-video-ids.md
"""
import json, os

ARTICLES_DIR = "articles/posts"
BLOCKED_IDS = {
    "dQw4w9WgXcQ",  # Rick Astley — Never Gonna Give You Up (the original rickroll)
    "oHg5SJYRHA0",  # Rick Astley — Never Gonna Give You Up (alternate URL)
    "xFrG64wTeG8",  # Rick Astley — Never Gonna Let You Down (companion rickroll)
    "9bZkp7q19f0",  # PSY — Gangnam Style (classic meme)
    "kJQP7kiw5Fk",  # Luis Fonsi — Despacito (most-viewed, common lazy placeholder)
    "RgKAFK5djSk",  # See You Again — Wiz Khalifa (common emotional filler)
    "JGwWNGJdvx8",  # Shape of You — Ed Sheeran (generic placeholder)
}

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    if "/embed/" in url:
        return url.split("/embed/")[-1].split("?")[0]
    return url  # assume raw ID


def main():
    if not os.path.isdir(ARTICLES_DIR):
        print(f"  ⚠️  Articles directory not found: {ARTICLES_DIR}")
        return

    modified = False
    for fname in sorted(os.listdir(ARTICLES_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(ARTICLES_DIR, fname)
        try:
            with open(fpath) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ⚠️  Invalid JSON in {fname}: {e}")
            continue

        slug = data.get("slug", fname.replace(".json", ""))
        videos = data.get("videos", [])
        if not videos:
            continue

        new_videos = []
        stripped = False
        for v in videos:
            vid = extract_video_id(v.get("url", ""))
            if vid in BLOCKED_IDS:
                print(f"    🚫 Stripped blocked video '{vid}' from {slug}")
                stripped = True
                continue
            new_videos.append(v)

        if stripped:
            data["videos"] = new_videos
            with open(fpath, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            modified = True

    if not modified:
        print("    ✅ No blocked video IDs found")


if __name__ == "__main__":
    main()
