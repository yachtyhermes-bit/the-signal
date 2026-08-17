#!/usr/bin/env python3
"""Generic hero image generator for The Signal using FAL flux/schnell.

Usage:
    generate-hero.py --slug <slug> --prompt "<prompt>"
    generate-hero.py --slug <slug> --prompt "<prompt>" --width 1200 --height 675

Saves to public/img/articles/<slug>.jpg (1200x675, JPEG q92).
"""
import argparse
import os
import sys

import requests


def get_fal_key():
    """Resolve FAL_KEY from env or known local files."""
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    candidates = [
        "/home/chino/video_output/.fal_real",
        "/home/chino/hermes-workspace/studio-api/.env",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        if "=" in line and line.split("=", 1)[0].strip() == "FAL_KEY":
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val:
                                return val
                        elif "|" in line and "FAL" in line:
                            val = line.split("|", 1)[1].strip()
                            if val:
                                return val
                        elif line.startswith("fal-") or len(line) > 30:
                            # bare key file (one key per line)
                            return line.split("\n")[0].strip()
            except Exception:
                continue
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate a hero image via FAL flux/schnell")
    parser.add_argument("--slug", required=True, help="Article slug (output filename base)")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=675)
    args = parser.parse_args()

    slug = args.slug
    W, H = args.width, args.height
    outpath = f"/home/chino/thesignal/public/img/articles/{slug}.jpg"

    fal_key = get_fal_key()
    if not fal_key:
        print("ERROR: FAL_KEY not found in env or known key files")
        sys.exit(1)
    os.environ["FAL_KEY"] = fal_key

    import fal_client

    print(f"Generating hero image for '{slug}'...")
    print(f"Prompt: {args.prompt[:140]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": args.prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print(f"ERROR: Could not find image URL in result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "wb") as f:
        f.write(r.content)
    file_size = os.path.getsize(outpath)
    print(f"Saved to {outpath}")
    print(f"   Size: {file_size} bytes ({file_size / 1024:.1f} KB)")

    from PIL import Image

    img = Image.open(outpath)
    print(f"   Dimensions: {img.size}")

    if img.size != (W, H):
        print(f"Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        img.save(outpath, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(outpath)
        print(f"   Saved {outpath}: {file_size} bytes ({file_size / 1024:.1f} KB)")

    if file_size < 10240:
        print(f"File too small ({file_size} bytes), re-saving with higher quality...")
        img.save(outpath, "JPEG", quality=98, optimize=True)
        file_size = os.path.getsize(outpath)
        print(f"   New size: {file_size} bytes ({file_size / 1024:.1f} KB)")

    print(f"DONE {outpath}")


if __name__ == "__main__":
    main()
