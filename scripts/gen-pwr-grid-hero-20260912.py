#!/usr/bin/env python3
"""Generate hero for pwr-ai-power-grid-bottleneck-2026 (fal flux/schnell).

Subject: Quanta Services (NYSE: PWR) — the electrical-infrastructure
contractor building America's high-voltage transmission grid to carry new
AI data-center load. The article is about the power-grid bottleneck: the
transmission lines, towers and crews (not the chips) are what stand between
AI ambition and delivered electricity.

Scene chosen: a high-voltage transmission-line construction scene — utility
linemen in plain hard hats and plain hi-vis vests rigging/climbing a tall
steel lattice transmission tower at golden hour, long catenary power lines
running to the horizon across open countryside, line-stringing equipment and
a bucket truck on the ground below, warm late-afternoon light, shallow depth
of field with the workers and steel lattice crisp and the landscape in soft
bokeh.

Deliberately NOT a data center, server room, server aisle, hallway or any
interior tech scene, and DISTINCT from recent heroes (chip fab, wafer macro,
cryostat, rocket pad, radar dish, jet-engine line, trading floor, container
port, rooftop network rack).

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- Vehicles, equipment and clothing plain and unmarked so no brand text renders.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-pwr-grid-hero-20260912.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "pwr-ai-power-grid-bottleneck-2026")
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
    "walls, no laptops, no phones, no tablets, no keyboards with writing, no "
    "UI, no computer interfaces, no code, no dashboards, no whiteboards with "
    "writing, no paper documents, no notebooks, no books with titles, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, no "
    "3D render, no neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of two utility linemen "
        "in plain unmarked white hard hats and plain unmarked high-visibility "
        "work vests rigging a tall steel lattice high-voltage transmission "
        "tower at golden hour, one lineman climbing the smooth grey galvanized "
        "steel lattice while the other stands on the crossarm handling a "
        "thick conductor cable, the plain unmarked steel tower members and "
        "crossarm rising out of frame, long catenary power lines strung in "
        "neat parallel arcs out to the far horizon across open countryside "
        "of dry gold grass and distant low hills, a plain unmarked white "
        "bucket truck and line-stringing equipment parked below on the dirt "
        "right-of-way, warm low late-afternoon sunlight raking across the "
        "steel lattice and flaring softly behind the wires, dust haze in the "
        "air, shallow depth of field with the linemen and the steel lattice "
        "crisply sharp while the distant landscape and sky melt into smooth "
        "soft bokeh, natural realistic skin tones, photorealistic, high "
        "detail, professional documentary photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic stock photograph of a high-voltage transmission "
        "line crew working on a rural transmission corridor at sunrise, "
        "close view of gloved hands attaching a long white ceramic insulator "
        "string and a thick aluminium conductor to the smooth unmarked "
        "galvanized steel crossarm of a tall lattice transmission pylon, the "
        "worker in a plain unmarked hard hat and plain unmarked high-"
        "visibility vest seen from behind and to the side, the plain "
        "unmarked steel lattice structure receding upward, below and beyond "
        "a long straight row of identical steel pylons marching away down "
        "the right-of-way with power lines dipping in catenary between them, "
        "open farmland and dry grass on both sides, a plain unmarked white "
        "boom truck parked far below in soft focus, warm low golden sunrise "
        "backlight glowing through the wires and rim-lighting the dust and "
        "the worker, very shallow depth of field with the insulator string "
        "and gloved hands tack sharp and the corridor dissolved into smooth "
        "bokeh, photorealistic, high detail, professional editorial "
        "photography, 16:9 landscape composition. "
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
