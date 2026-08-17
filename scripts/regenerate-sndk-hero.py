#!/usr/bin/env python3
"""Regenerate hero for 'sndk-nand-supercycle-ai-investor-day-2026' via FAL flux/schnell.

Text-free, photo-realistic prompt matching the article's sector (semiconductor /
NAND flash memory). Excludes screens, monitors, signage, brand markings, letters,
numbers. Set ATTEMPT=2 for the adjusted second-attempt prompt.

Usage:
    ATTEMPT=1 python3 scripts/regenerate-sndk-hero.py
    ATTEMPT=2 python3 scripts/regenerate-sndk-hero.py
"""

import io
import os
import sys
import requests

SLUG = "sndk-nand-supercycle-ai-investor-day-2026"
W, H = 1440, 810  # 16:9 generation size

OUTPUT1 = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT2 = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

PROMPT_1 = (
    "Macro photograph inside a semiconductor cleanroom: a robotic arm holding a "
    "stack of glossy silicon memory wafers, iridescent rainbow reflections on the "
    "wafer surfaces, ultra-clean white and blue environment, stainless steel "
    "equipment, soft diffuse lighting, shallow depth of field, photo-realistic, "
    "shot on a full-frame DSLR, sharp detail, 4K. "
    "No text anywhere, no letters, no numbers, no logos, no brand markings, "
    "no signage, no screens, no monitors, no displays, no labels."
)

PROMPT_2 = (
    "Aerial photograph of a massive semiconductor fabrication campus at dusk, "
    "long low concrete buildings with white rooftop air-scrubber units and "
    "cleanroom exhaust stacks, soft blue-hour sky, warm amber window light, "
    "landscaped grounds and access roads, wide-angle architectural photography, "
    "photo-realistic, shot on a full-frame DSLR, sharp detail, 4K. "
    "No text anywhere, no signage, no logos, no brand markings, no letters, "
    "no numbers, no billboards, no screens, no monitors, no vehicles with markings."
)


def get_fal_key():
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
                            return line.split("\n")[0].strip()
            except Exception:
                continue
    return None


def main():
    attempt = os.environ.get("ATTEMPT", "1")
    prompt = PROMPT_2 if attempt == "2" else PROMPT_1

    fal_key = get_fal_key()
    if not fal_key:
        print("ERROR: FAL_KEY not found in env or known key files")
        sys.exit(1)
    os.environ["FAL_KEY"] = fal_key

    import fal_client

    print(f"Generating hero image for '{SLUG}' (attempt {attempt})...")
    print(f"Prompt: {prompt[:130]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
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
    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    from PIL import Image

    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    print(f"Downloaded dimensions: {img.size}")

    # Center-crop to 16:9, then resize to 1920x1080
    tw, th = img.size
    target_ratio = 16 / 9
    if tw / th > target_ratio:
        new_w = int(th * target_ratio)
        left = (tw - new_w) // 2
        img = img.crop((left, 0, left + new_w, th))
    elif tw / th < target_ratio:
        new_h = int(tw / target_ratio)
        top = (th - new_h) // 2
        img = img.crop((0, top, tw, top + new_h))
    img = img.resize((1920, 1080), Image.LANCZOS)
    print(f"Final dimensions: {img.size}")

    for output_path in [OUTPUT1, OUTPUT2]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(output_path)
        print(f"  Saved to {output_path} ({file_size/1024:.1f} KB)")

    print("\nUploading to R2 via r2_upload.py...")
    result_code = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if result_code == 0:
        print("  R2 upload succeeded!")
    else:
        print(f"  R2 upload failed (exit code {result_code})")
        sys.exit(1)

    try:
        resp = requests.head(R2_URL, timeout=30)
        print(f"R2 HEAD: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  R2 verification error: {e}")

    print(f"\nAll done! R2 URL: {R2_URL}")


if __name__ == "__main__":
    main()
