#!/usr/bin/env python3
"""Regenerate hero for spcx-ai-compute-landlord-2026 (fal flux/schnell).

FAIL REASON (attempt 1 of the original generator): the stainless-steel rocket
hull rendered hallucinated lettering ("PCQ7"-style letter soup) on its large
flat reflective surface. Fix: (a) make the vehicle smaller/distant in frame so
there is little continuous hull surface for the model to paint on, and (b)
hammer every prompt with explicit "absolutely no writing/letters/numbers/
markings/decals on the rocket hull" language, and offer a backlit / silhouette
composition where the hull is dark and cannot carry readable text.

Scene: SPACE sector -> rocket / launch-pad scene (data-center and server-room
compositions are forbidden as over-used).

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- Rocket hull plain/blank, scraped of any marking so no brand text renders.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/regen-spcx-hero-20260911.py
    ATTEMPT=2 /home/chino/video-venv/bin/python3 scripts/regen-spcx-hero-20260911.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "spcx-ai-compute-landlord-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The rocket vehicle is a completely plain blank smooth metal cylinder: "
    "absolutely no writing, no letters, no words, no numbers, no serial "
    "numbers, no codes, no names, no logos, no brand names, no decals, no "
    "stencils, no painted or etched markings of any kind anywhere on the "
    "rocket body or fins. Every other surface is completely smooth, plain "
    "and unmarked too: no text, no letters, no numbers, no codes, no labels, "
    "no plaques, no nameplates, no signage, no posters, no screens, no "
    "monitors, no displays, no video walls, no laptops, no phones, no "
    "tablets, no UI, no computer interfaces, no code, no dashboards, no "
    "whiteboards with writing, no paper documents, no notebooks, no books "
    "with titles, no watermark, no captions, no illustration, no digital art, "
    "no cartoon, no 3D render, no neon, no glowing lines, no geometric "
    "patterns."
)

PROMPTS = {
    "1": (
        "Professional wide telephoto stock photograph of a gleaming stainless-"
        "steel reusable rocket rising from an industrial coastal launch pad at "
        "blue hour just before dawn, the vehicle distant and compact in the "
        "frame low above the pad as it clears a huge billowing cloud of white "
        "steam and exhaust, launch-tower gantry and steel latticework to one "
        "side, rows of warm floodlights on masts glowing against a deep cold "
        "blue morning sky with a thin orange band at the horizon, dark flat "
        "scrubland and calm ocean stretching away behind in soft atmospheric "
        "haze, the rocket's smooth reflective hull perfectly blank and clean, "
        "cinematic professional lighting, atmospheric mist, shallow depth of "
        "field, photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic backlit contra-jour stock photograph at dawn of a "
        "slim stainless-steel space rocket standing on a coastal launch pad, "
        "rendered as an almost complete dark silhouette against a bright "
        "glowing sunrise sky of orange, pink and pale blue, the sun flaring "
        "just behind the launch-tower gantry, low drifting ground fog and "
        "vapor wrapping the base of the vehicle, a few warm pad floodlights "
        "still burning, the ocean horizon a thin dark line behind, the whole "
        "vehicle in shadow so its metal skin is smooth, plain, dark and "
        "featureless, strong rim light only, professional cinematographic "
        "lighting, shallow depth of field, photorealistic, high detail, 16:9 "
        "landscape composition. "
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
            raw = f.read().strip().split("\n")[0]
            key = raw.split("|", 1)[1] if "|" in raw else raw
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
