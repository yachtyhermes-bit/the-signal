#!/usr/bin/env python3
"""Regenerate hero for lmt-australia-air-battle-management-2026 (fal flux/schnell).

Subject: Lockheed Martin A$1.32bn contract for Tranche 2B of Project AIR6500,
the Joint Air Battle Management System — the software "brain" fusing Australian
air and missile-defence sensors into a single battlespace picture.

Scene chosen: a ground-based military air-defence radar array on a windswept
coastal headland at dawn — an operator/command vehicle parked nearby, long
shadows, distant ocean. Photorealistic and thematically on-point for an air
battle management / sensor-fusion story, and visually distinct from recent
Signal heroes (semiconductor cleanroom, jet-engine assembly hall).

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock-photograph style ONLY. No digital art/neon/render.
- TEXT-FREE: no letters/numbers/logos/signage/plaques/screens/UI anywhere;
  absolutely NO monitors, displays, video walls, laptops, phones, tablets,
  whiteboards with writing, documents or paper with writing.
- Equipment bodies plain/unmarked — no unit markings, tail numbers, insignia,
  stencils, decals or nameplates; keep equipment at mid-distance and softly
  blurred so no marking can render.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 python3 scripts/regen-lmt-hero-20260910.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "lmt-australia-air-battle-management-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no "
    "letters, no numbers, no codes, no serial numbers, no etched or engraved "
    "markings, no labels, no plaques, no nameplates, no decals, no stencils, "
    "no stenciled writing, no markings of any kind, no military unit insignia, "
    "no roundels, no flags, no logos, no brand names, no signage, no posters, "
    "no screens, no monitors, no displays, no video walls, no laptops, no "
    "phones, no tablets, no keyboards with writing, no UI, no computer "
    "interfaces, no code, no dashboards, no maps with labels, no whiteboards "
    "with writing, no paper documents, no notebooks, no books with titles, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, no "
    "3D render, no neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Ultra-realistic cinematic stock photograph of a ground-based military "
        "air-defence radar installation on a windswept coastal headland at "
        "dawn: a large rotating phased-array radar antenna on a sturdy wheeled "
        "trailer, its panels completely smooth, plain and unmarked, angled "
        "toward a pale pink-and-blue dawn sky, a plain unmarked military "
        "support truck parked at mid-distance beside it, weathered grass and "
        "low scrub over a rocky bluff, cold ocean haze and a faint distant "
        "horizon of sea behind, long soft shadows stretching toward the "
        "camera, cool blue-and-amber dawn light, shallow depth of field with "
        "the radar softly sharp and the background dissolved into mist, "
        "photorealistic, high detail, professional lighting, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic editorial stock photograph of a mobile air-defence "
        "radar unit deployed on a bare windswept coastal headland in early "
        "morning light: a tall dark antenna array on a wheeled trailer seen at "
        "mid-distance against the bright sky, its flat panels perfectly "
        "smooth, matte and entirely blank with absolutely no lettering, "
        "numbers, codes, badges, emblems or markings on the antenna or its "
        "frame, a single plain indistinct military support vehicle as a soft "
        "unbranded boxy shape a short distance away on a dirt track with no "
        "grille badge, no maker's mark and no number plates, tussocky "
        "windswept grass and exposed rock, drifting sea mist rolling in from "
        "the indigo ocean in the far background, dramatic soft dawn light "
        "raking low across the ground casting long shadows, shallow depth of "
        "field with the vehicle soft and out of focus, photorealistic, high "
        "detail, professional lighting, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Ultra-realistic cinematic stock photograph of a modern military "
        "air-defence radar antenna parked on a dusty inland hilltop at first "
        "light: a large flat planar antenna array on a towed trailer seen in "
        "silhouette from a low angle against the bright dawn horizon, the "
        "panel face turned away so its surface is a plain matte blank with no "
        "marking of any kind, a soft-focus unmarked support truck and a low "
        "plain operator shelter tent beside it with no badges, brand marks or "
        "number plates, dry golden grass and red earth underfoot, faint dust "
        "haze in the air, a deep blue sky warming to gold on the horizon, "
        "crisp directional dawn light and long shadows, shallow depth of "
        "field, photorealistic, high detail, professional lighting, 16:9 "
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
    if size < 10240:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
