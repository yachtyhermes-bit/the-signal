#!/usr/bin/env python3
"""REGEN hero for smci-export-control-guilty-plea-2026 (garbled chassis badge).

The previous hero showed an AI-hallucinated 3-letter logo badge on the front
faceplate of the dark server chassis ("DEP"/"dcp"/"GIEP" — no real brand).
This regen keeps the same subject (rack-mount AI server chassis on a pallet in
a dim warehouse) but reframes to a low three-quarter REAR angle so no
badge-bearing front panel faces the lens: plain matte surfaces and bare-metal
handles carry the frame. NO text, NO badges, NO labels, NO logos anywhere.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "smci-export-control-guilty-plea-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: absolutely no writing, no letters, "
    "no words, no numerals, no model numbers, no part codes, no badges, no nameplates, "
    "no logos, no branding, no stickers, no decals, no silkscreen markings, no symbols, "
    "no glyphs, no watermarks, no signage. The chassis panels are bare matte metal with no "
    "marking of any kind anywhere on them. No people, no hands, no faces, no human figures. "
    "No neon, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Strictly photorealistic editorial photography."
)

PROMPT = (
    "Professional editorial photograph shot on a 50mm lens at f/2.0 on a full-frame camera, "
    "shallow depth of field, of a single rack-mount AI server chassis resting on a wooden pallet "
    "in a dim, empty warehouse under a single hard overhead lamp. The camera is low and to the "
    "rear three-quarter, so the front panel with its badge faces away from the lens and the visible "
    "surfaces are plain matte black brushed metal with plain perforated ventilation grilles and bare "
    "metal rail handles. Empty orange steel shelving and stacks of wooden pallets recede into deep "
    "shadow behind, a faded yellow floor line painted across dark concrete. Cool dim industrial "
    "lighting, deep shadows, realistic dust and scuffs, subtle film grain, extremely high detail, "
    "8k resolution, documentary warehouse hardware photography, 16:9 landscape aspect ratio. "
    + NO_TEXT
)


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


def gen(seed, out):
    import fal_client
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": seed,
    })
    url = None
    if result.get("images"):
        url = result["images"][0]["url"]
    elif result.get("image"):
        url = result["image"]
    if not url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    img = Image.open(out)
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(out, "JPEG", quality=92)
    print(f"saved {out} size={Image.open(out).size} bytes={os.path.getsize(out)}")


if __name__ == "__main__":
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261011
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/smci_regen_1.jpg"
    gen(seed, out)
