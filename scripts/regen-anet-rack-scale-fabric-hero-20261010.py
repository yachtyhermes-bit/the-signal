#!/usr/bin/env python3
"""REGEN hero for anet-ethernet-rack-scale-ai-fabric-2026 (garbled faceplate text).

The previous hero showed AI-hallucinated letter soup on the switch faceplate
("PET60ET", "OB-342", sigma glyphs) where port model markings sat. This regen
keeps the same subject (high-density Ethernet switch + fibre for AI rack fabric)
but reframes so the port faceplate is turned away / out of focus: the fibre
patch-cable harness and heat-sink body carry the frame instead.
NO text, NO port labels, NO model markings anywhere.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "anet-ethernet-rack-scale-ai-fabric-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: absolutely no writing, no letters, "
    "no words, no numerals, no model numbers, no part codes, no port labels, no silkscreen "
    "markings, no symbols, no glyphs, no logos, no branding, no stickers, no decals, no "
    "watermarks, no signage. The equipment faceplates are bare brushed metal with no "
    "marking of any kind. No people, no hands, no faces, no human figures, no silhouettes. "
    "No neon, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Strictly photorealistic editorial photography."
)

PROMPT = (
    "Professional editorial photograph shot on an 85mm lens at f/1.8 on a full-frame camera, "
    "shallow depth of field, of a dense harness of fiber-optic patch cables fanning out of the "
    "rear of a high-density Ethernet network switch on a workstation testing bench. "
    "The camera looks along the length of the cable bundle and the ribbed heat-sink body of the "
    "switch from a low three-quarter rear angle, so no front panel is facing the lens; the port "
    "faceplate is turned away and lost in soft focus. Warm amber and green optical tones in the "
    "glass fibre, black cable jackets, cool aluminium grey metal, workshop bench with faint dust, "
    "blurred tooling far behind. Professional overhead lighting, subtle film grain, extremely high "
    "detail, 8k resolution, documentary hardware photography, 16:9 landscape aspect ratio. "
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
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261010
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/anet_regen_1.jpg"
    gen(seed, out)
