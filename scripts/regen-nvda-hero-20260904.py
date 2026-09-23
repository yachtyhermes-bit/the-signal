#!/usr/bin/env python3
"""Regenerate hero for nvda-hugging-face-acquisition-2026 (fal flux/schnell).

Subject: NVIDIA acquires Hugging Face — the town square where AI is built,
18M developers. 2026-09-04 cron inspection FAILED the previous hero: garbled
AI-hallucinated code gibberish on a background monitor.

Rules (per the-signal-website skill + repo regen lessons):
- PHOTO-REALISTIC stock-photograph style ONLY. No digital art/neon/render.
- TEXT-FREE: no letters/numbers/logos/signage/plaques/screens/UI anywhere;
  absolutely NO monitors, displays, laptops, phones, tablets, whiteboards
  with writing, documents or paper with writing.
- People collaborating with no readable tech in frame.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 python3 scripts/regen-nvda-hero-20260904.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "nvda-hugging-face-acquisition-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no labels, no plaques, no nameplates, "
    "no decals, no stencils, no stenciled writing, no markings of any kind, no "
    "logos, no brand names, no signage, no posters, no screens, no monitors, no "
    "displays, no laptops, no phones, no tablets, no smartwatches, no keyboards "
    "with writing, no UI, no computer interfaces, no code, no dashboards, no "
    "whiteboards with writing, no flip charts, no sticky notes, no paper "
    "documents, no notebooks, no books with titles, no watermark, no captions, "
    "no illustration, no digital art, no cartoon, no 3D render, no neon, no "
    "glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Ultra-realistic cinematic stock photograph of a bright modern open-plan "
        "software company office: a diverse group of developers standing and "
        "seated in a loose circle, engaged in lively discussion with natural "
        "hand gestures and genuine smiles, no computers or devices anywhere in "
        "frame, hands empty or holding plain ceramic coffee mugs, warm sunlight "
        "streaming through floor-to-ceiling windows, leafy green plants, exposed "
        "brick and light wood interior, people looking at each other not at any "
        "object, clean unmarked plain surfaces only, shallow depth of field, "
        "natural skin tones, photorealistic, high detail, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    "2": (
        "Ultra-realistic cinematic stock photograph of an outdoor office "
        "courtyard terrace at golden hour: a small diverse group of software "
        "developers in casual attire chatting warmly around a plain wooden "
        "table with only simple ceramic cups, no electronics, no papers, no "
        "writing anywhere, lush plants and a softly blurred modern glass office "
        "building behind them with no visible signage, warm evening light, "
        "relaxed collaborative mood, shallow depth of field, natural skin "
        "tones, photorealistic, high detail, 16:9 landscape composition. "
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
