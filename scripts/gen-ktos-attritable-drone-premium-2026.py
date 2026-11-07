#!/usr/bin/env python3
"""Hero for ktos-attritable-drone-premium-2026 (Kratos Defense — jet-powered
attritable combat drones / Valkyrie, hypersonics, satellite ground systems).

Scene: a single sleek grey jet-powered unmanned combat aircraft on a desert
test-range ramp at golden-hour dusk — no cockpit canopy, no propeller, swept
wings, dorsal intake. Heat haze off the tarmac, dry scrub desert, distant
mountains, a couple of ground-crew silhouettes far off at the edge of frame.
200mm telephoto, low three-quarter angle, shallow depth of field, editorial
aviation photojournalism. Strictly photorealistic; no text/insignia/logos.

Usage:
    gen-ktos-attritable-drone-premium-2026.py [--seed N]
"""
import argparse
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = "ktos-attritable-drone-premium-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080
SEED = 20261107

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no tail numbers, no roundels, no insignia, "
    "no unit markings, no watermarks, no signage, no captions. Ground crew appear only as "
    "small distant silhouettes, no visible faces, no close-up people. No neon, no synthwave, "
    "no glowing lines, no digital fantasy effects, no 3D render sheen, no lens flares, "
    "no infographic overlays. Strictly photorealistic editorial photography."
)

PROMPT = (
    "Professional editorial aviation photograph shot on a 200mm telephoto lens at f/4 on a "
    "full-frame camera, shallow depth of field, of a single sleek matte-grey jet-powered "
    "unmanned combat aircraft parked on a concrete ramp at a remote desert test range during "
    "golden-hour dusk. The aircraft is a drone: absolutely no cockpit canopy and no propeller, "
    "a smooth unbroken nose with a dorsal engine intake behind it, long slender fuselage, "
    "swept-back wings and a V-tail, landing gear on the sun-baked concrete, seen from a low "
    "three-quarter front angle so the airframe fills the frame diagonally. Plain unmarked "
    "matte grey composite skin with faint panel lines and a dull operational finish, faint dust "
    "on the lower fuselage. Shimmering heat haze rising off the concrete around the wheels. "
    "Behind and to the side in soft focus: dry scrub desert of sage and creosote, a weathered "
    "low concrete revetment, and barren brown mountains on the horizon under a warm amber and "
    "dusty-rose sky. Two small distant ground-crew silhouettes far off at the edge of the ramp, "
    "out of focus, tiny in frame. Warm low sun raking across the airframe from camera left, "
    "long soft shadows, realistic atmospheric dust and grain, muted cinematic colour grade, "
    "extremely high detail, documentary photojournalism, 16:9 landscape aspect ratio. "
    + NO_TEXT
)


def load_fal_key():
    """Resolve FAL_KEY from env, yachty profile .env, or the repo's known key files."""
    if os.environ.get("FAL_KEY"):
        return os.environ["FAL_KEY"]
    candidates = [
        "/home/chino/.hermes/profiles/yachty/.env",
        "/home/chino/hermes-workspace/studio-api/.env",
        "/home/chino/video_output/.fal_real",
    ]
    for path in candidates:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        return key
                elif "|" in line and "FAL" in line:
                    key = line.split("|", 1)[1].strip()
                    if key:
                        return key
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    import fal_client

    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    os.environ["FAL_KEY"] = key

    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": args.seed,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT).convert("RGB")
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    # q88 keeps a 1920x1080 photo under the 500KB cap
    img.save(OUTPUT, "JPEG", quality=88, optimize=True, progressive=True)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copyfile(OUTPUT, BACKUP)
    print("Saved", OUTPUT, Image.open(OUTPUT).size, os.path.getsize(OUTPUT), "bytes")


if __name__ == "__main__":
    main()
