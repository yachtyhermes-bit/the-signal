#!/usr/bin/env python3
"""Regenerate hero for ktos-low-cost-engine-industrial-base-2026 (fal flux/schnell).

Subject: Kratos/GE second-sourcing the JASSM's engine — small jet engine
production line, affordable-mass drone/missile propulsion buildout.

2026-09-08 cron inspection FAILED the current hero: AI-hallucinated garbled
etched markings (fake serial/technical label gibberish) on the jet engine
casing in the foreground, plus indistinct monitor stations.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock-photograph style ONLY. No digital art/neon/render.
- TEXT-FREE: no letters/numbers/logos/signage/plaques/screens/UI anywhere;
  absolutely NO monitors, displays, video walls, laptops, phones, tablets,
  whiteboards with writing, documents or paper with writing.
- Engine casings completely smooth and unmarked — no etched serial numbers,
  no engraved lettering, no stenciled markings, no nameplates; keep engines
  at mid-distance and softly blurred so no marking can render.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 python3 scripts/regen-ktos-hero-20260908.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ktos-low-cost-engine-industrial-base-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
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
    "walls, no laptops, no phones, no tablets, no smartwatches, no keyboards "
    "with writing, no UI, no computer interfaces, no code, no dashboards, no "
    "maps with labels, no whiteboards with writing, no flip charts, no sticky "
    "notes, no paper documents, no notebooks, no books with titles, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, no "
    "3D render, no neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Ultra-realistic cinematic stock photograph of a modern aerospace "
        "engine assembly hall at mid-distance: several small jet engines, "
        "each a compact turbofan with a large intake fan and smooth bare "
        "metal casings with NO etched serial numbers and NO engraved "
        "lettering, mounted on plain wheeled assembly stands in a clean "
        "bright factory bay, a few workers in light industrial uniforms as "
        "small distant figures between the stands, yellow overhead gantry "
        "crane rails, polished pale concrete floor with worn yellow safety "
        "lines, soft cool daylight from high windows, engines softly out of "
        "focus toward the background so no surface detail or marking can "
        "render, shallow depth of field, photorealistic, high detail, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic editorial stock photograph of a wide aerospace "
        "manufacturing hangar interior: a long clean aisle between rows of "
        "abstract industrial assembly stations, one engineer in a light "
        "uniform seen from behind at a distance wheeling a small jet engine "
        "on a low trolley toward the camera, the engine angled so its casing "
        "reads as smooth unmarked metal with no visible lettering or etched "
        "numbers, the nearest machinery softly blurred at the edges of the "
        "frame so no logo, label or screen detail can appear, warm "
        "industrial lighting with soft haze, polished concrete floor, "
        "photorealistic, high detail, 16:9 landscape composition. "
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
            if "|" in raw:
                key = raw.split("|", 1)[1]
            else:
                key = raw
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
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
