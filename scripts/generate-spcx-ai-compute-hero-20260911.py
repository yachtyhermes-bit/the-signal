#!/usr/bin/env python3
"""Generate hero for spcx-ai-compute-landlord-2026 (fal flux/schnell).

Subject: SpaceX / SPCX — the AI-compute article frames SpaceX as the
"landlord" of orbital AI compute. Per the task brief, the SPACE sector
warrants a ROCKET / LAUNCH-PAD scene (data-center / server-room compositions
are explicitly forbidden as over-used).

Scene (mandatory): a gleaming stainless-steel reusable rocket standing or
lifting off from an industrial launch pad at blue hour / dawn, with a
launch-tower gantry, floodlights, and low vapor or steam drifting around the
base, ocean or scrubland horizon behind it. Shallow depth of field,
professional cinematographic lighting, 16:9 landscape.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- Machine/rocket bodies plain/scraped of any marking so no brand text renders.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/generate-spcx-ai-compute-hero-20260911.py
    ATTEMPT=2 MODEL=fal-ai/flux/dev ...   # fallback to the other FAL model
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "spcx-ai-compute-landlord-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
MODEL = os.environ.get("MODEL", "fal-ai/flux/schnell")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no "
    "letters, no numbers, no codes, no serial numbers, no etched or engraved "
    "markings, no labels, no plaques, no nameplates, no decals, no stencils, "
    "no stenciled writing, no markings of any kind, no logos, no brand names, "
    "no signage, no posters, no screens, no monitors, no displays, no video "
    "walls, no laptops, no phones, no tablets, no UI, no computer interfaces, "
    "no code, no dashboards, no whiteboards with writing, no paper documents, "
    "no notebooks, no books with titles, no watermark, no captions, no "
    "illustration, no digital art, no cartoon, no 3D render, no neon, no "
    "glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a gleaming polished stainless-steel "
        "reusable rocket standing on a concrete industrial launch pad at blue "
        "hour just before dawn, the tall reflective metal booster catching the "
        "cool blue ambient light along one edge and warm amber floodlight from "
        "the other, its flanks perfectly smooth and plain with no markings, a "
        "tall steel launch-tower gantry with dark latticework of beams and "
        "articulated arms beside it, low banks of white vapor and steam "
        "drifting softly around the base of the rocket, the distant flat "
        "horizon of dark scrubland and ocean behind under a deep blue sky with "
        "faint warm orange glow near the horizon line, bright floodlights on "
        "the pad raking long shadows across the concrete, atmospheric haze and "
        "soft mist, cinematic professional lighting, shallow depth of field "
        "with the rocket sharply in focus against a softly blurred background, "
        "photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic wide telephoto stock photograph of a tall stainless-"
        "steel space rocket moments after liftoff from an industrial coastal "
        "launch pad at dawn, the gleaming metal booster rising above a billow "
        "of white steam and rocket exhaust smoke around the pad, its smooth "
        "reflective hull completely unmarked and plain, the launch-tower "
        "gantry with dark steel framework to one side, rows of floodlights on "
        "masts glowing warm against a cold blue morning sky, the ocean and low "
        "flat scrubland horizon stretching away behind in soft atmospheric "
        "haze, low drifting vapor hugging the ground, warm rim light on the "
        "metal against cool blue shadows, shallow depth of field, professional "
        "cinematographic lighting, photorealistic, high detail, 16:9 landscape "
        "composition. "
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


def generate(prompt, out_path, model=MODEL):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print(f"Generating image with {model}...")
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "enable_safety_checker": False,
    }
    if "schnell" in model:
        args["num_inference_steps"] = 4
    result = fal_client.subscribe(model, arguments=args)
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
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} MODEL={MODEL}")
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
