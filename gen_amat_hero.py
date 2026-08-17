#!/usr/bin/env python3
"""Generate a photo-realistic hero image for 'amat-q3-fy2026-earnings-preview-2026' using FAL flux/schnell."""

import os
import sys
import requests

SLUG = "amat-q3-fy2026-earnings-preview-2026"
W, H = 1200, 675

OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
]

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional stock photograph of a semiconductor fabrication cleanroom. "
    "Engineers in white bunny suits working beside massive chip manufacturing equipment, "
    "large wafer processing machines with stainless steel panels, yellow filtered lighting "
    "typical of photolithography areas, clean bright facility interior. "
    "Realistic photo, shallow depth of field, professional lighting, editorial documentary photography. "
    "No text, no labels, no logos, no markings. "
    "Not abstract art, not digital art, not neon, no glowing lines, no geometric patterns."
)


def load_fal_key():
    """Try several known FAL key locations, in order."""
    candidates = [
        os.environ.get("FAL_KEY"),
        "/home/chino/hermes-workspace/studio-api/.env",  # FAL_KEY=... line
        "/home/chino/video_output/.fal_real",            # raw key, maybe token|key
    ]
    for cand in candidates:
        if not cand:
            continue
        if os.path.exists(cand):
            try:
                with open(cand) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("FAL_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
                # raw key file: first non-empty line
                with open(cand) as f2:
                    raw = f2.read().strip().split("\n")[0]
                if "|" in raw:
                    raw = raw.split("|", 1)[1]
                if raw:
                    return raw
            except Exception:
                continue
    return None


def main():
    import fal_client

    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    os.environ["FAL_KEY"] = key

    print(f"Generating hero image for '{SLUG}'...")
    print(f"Prompt: {PROMPT[:120]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    print(f"Result keys: {list(result.keys())}")

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print("ERROR: Could not find image URL in result")
        print(f"Full result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    img_data = r.content

    from PIL import Image

    for output_path in OUTPUTS:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(img_data)

        file_size = os.path.getsize(output_path)
        print(f"Saved to {output_path}")
        print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

        img = Image.open(output_path)
        print(f"   Dimensions: {img.size}")

        if img.size != (W, H):
            print(f"Resizing from {img.size} to ({W}, {H})...")
            resample = getattr(Image, "Resampling", Image).LANCZOS
            img = img.resize((W, H), resample)
            img.save(output_path, "JPEG", quality=90)
            print(f"   Resized dimensions: {img.size}")

    print(f"\nR2 URL (expected): {R2_URL}")


if __name__ == "__main__":
    main()
