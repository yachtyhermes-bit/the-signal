#!/usr/bin/env python3
"""Regenerate eqix + sofi heroes (cron 2026-09-02 QA): text-free photo-realistic
prompts, 16:9 1920x1080 center-crop.

- eqix-inference-exchange-2026: FAIL — hallucinated building-top signage read
  inconsistently ("PILOT/MILLE", "PLMU/Muberbenz"...) = AI-hallucinated text.
- sofi-ai-digital-bank-flywheel-2026: FAIL — phone-screen UI text is mush:
  contradictory reads across passes, garbled tokens ("HEDPO", "FOGI Have").

Usage: SLUG=eqix-inference-exchange-2026 ATTEMPT=1|2 python3 regen-heroes-20260902.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size; final output 1920x1080
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no labels, no plaques, no "
    "nameplates, no decals, no stencils, no stenciled writing, no markings of "
    "any kind, no logos, no brand names, no roof signs, no signage, no "
    "billboards, no posters, no screens, no monitors, no displays, no phones "
    "with glowing screens, no UI, no watermark, no captions, no illustration, "
    "no digital art, no cartoon."
)

PROMPTS = {
    "eqix-inference-exchange-2026": {
        "1": (
            "Ultra-realistic cinematic photograph of a modern global business "
            "district skyline at golden hour seen from across a wide calm "
            "river: dense clusters of sleek glass skyscrapers in the "
            "midground, and along the near waterfront low wide windowless "
            "data-center buildings with rows of rooftop cooling units and "
            "dim blue-white security lights, warm low sun flaring behind the "
            "towers, long golden reflections shimmering on the water, a few "
            "wispy clouds catching orange light, photorealistic, high detail, "
            "16:9 landscape composition. " + NO_TEXT
        ),
        "2": (
            "Ultra-realistic cinematic photograph of a vast modern "
            "data-center campus at golden hour from a low wide angle: long "
            "low windowless concrete-and-metal buildings with rows of rooftop "
            "cooling units, tall electrical substation towers with plain "
            "steel lattice in the background, a few employees in plain "
            "workwear walking between buildings with faces not visible and no "
            "phones in hand, warm orange sunlight raking across the plain "
            "facades casting long shadows, clear sky with soft haze, "
            "photorealistic, high detail, 16:9 landscape composition. " + NO_TEXT
        ),
    },
    "sofi-ai-digital-bank-flywheel-2026": {
        "1": (
            "Ultra-realistic cinematic photograph of a sleek modern "
            "financial-technology company campus at golden hour: a low wide "
            "glass headquarters building with warm glowing interior light "
            "behind its plain glass curtain wall, a minimalist reflecting "
            "pool in the foreground mirroring the warm sky, a few green trees "
            "and clean modern concrete walkways, soft sunlight and long "
            "shadows, photorealistic, high detail, 16:9 landscape "
            "composition. " + NO_TEXT
        ),
        "2": (
            "Ultra-realistic cinematic photograph of a bright modern "
            "financial services building lobby interior at golden hour: warm "
            "sunlight streaming through floor-to-ceiling plain glass walls, "
            "minimalist smooth stone reception desk with a small green plant, "
            "clean white surfaces with warm wood accents, soft out-of-focus "
            "city skyline visible through the glass, no people, photorealistic, "
            "high detail, 16:9 landscape composition. " + NO_TEXT
        ),
    },
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
    if SLUG not in PROMPTS:
        print(f"ERROR: no prompt for SLUG={SLUG}")
        sys.exit(1)
    prompt = PROMPTS[SLUG][ATTEMPT]
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
