#!/usr/bin/env python3
"""Regenerate hero for axon-ai-agents-counter-drone-defense-2026 (fal flux/schnell).

Subject: Axon AI agents + counter-drone defense for police. 2026-09-04 cron
inspection FAILED the previous hero: garbled AI-hallucinated text on the
officer's sleeve patch.

Rules (per the-signal-website skill + repo regen lessons):
- PHOTO-REALISTIC stock-photograph style ONLY. No digital art/neon/render.
- TEXT-FREE: no letters/numbers/logos/signage/plaques/screens/UI anywhere;
  no uniform patches/badges with writing, no vehicle lettering/decals.
- Keep officer distant/silhouetted so no uniform details are readable.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 python3 scripts/regen-axon-hero-20260904.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "axon-ai-agents-counter-drone-defense-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no labels, no plaques, no nameplates, "
    "no decals, no stencils, no stenciled writing, no markings of any kind, no "
    "uniform patches, no badge lettering, no embroidered writing, no logos, no "
    "brand names, no signage, no posters, no vehicle lettering, no license "
    "plates, no screens, no monitors, no displays, no laptops, no phones, no "
    "tablets, no UI, no computer interfaces, no dashboards, no watermark, no "
    "captions, no illustration, no digital art, no cartoon, no 3D render, no "
    "neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Ultra-realistic cinematic stock photograph at dusk: a lone police "
        "officer seen from behind and far away, a small dark silhouette standing "
        "on a rooftop observation deck with hands relaxed, looking up at a "
        "small quadcopter drone hovering in the sky above a sprawling city "
        "skyline, deep blue and orange gradient sky, city lights beginning to "
        "twinkle, subtle haze, officer is too distant for any uniform detail to "
        "be visible, smooth unmarked rooftop, wide 16:9 landscape composition, "
        "photorealistic, high detail, shallow depth of field. " + NO_TEXT
    ),
    "2": (
        "Ultra-realistic cinematic stock photograph at blue hour: view across a "
        "city skyline at dusk with a small quadcopter drone with four propellers "
        "hovering in the foreground sky, tiny red navigation lights on the "
        "drone, soft orange and purple clouds, no people in the foreground, "
        "only a barely visible distant silhouette of an officer on a rooftop "
        "far below the horizon line of the frame, no readable detail anywhere, "
        "wide 16:9 landscape composition, photorealistic, high detail. "
        + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        with open(real_path) as f:
            key = f.read().strip()
            if key:
                os.environ["FAL_KEY"] = key
                return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with fal flux/schnell...")
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
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
    return img


def crop_to_16x9(img):
    """Center-crop to 16:9, then resize to 1920x1080."""
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H  # 16/9
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 10240:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")


if __name__ == "__main__":
    main()
