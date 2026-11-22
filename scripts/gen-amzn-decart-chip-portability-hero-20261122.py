#!/usr/bin/env python3
"""Hero image for amzn-decart-chip-portability-deal-2026 via fal flux/schnell.

Subject: Amazon reportedly nearing a ~$7.5B acquisition of Decart, whose software
lets AI models run across different chips (Nvidia GPUs, Google TPUs, Amazon
Trainium) — breaking hardware lock-in.

Physical subject: two physically different large AI accelerator modules side by
side on an anti-static mat on an electronics-lab workbench, with a technician's
gloved hands and a test probe softly out of focus behind them.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "amzn-decart-chip-portability-deal-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1600, 900

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no part numbers, no labels, no stickers with text, no logos, "
    "no branding, no watermarks, no signage. "
    "No neon lights, no synthwave, no glowing lines, no digital or sci-fi effects, "
    "no 3D render sheen, no plastic CGI look, no abstract art, no geometric patterns, "
    "no diagrams. Not a server room, not a data-center aisle, not a rack corridor, "
    "no racks receding into the distance. Strictly photorealistic editorial photography."
)

PROMPT = (
    "Photorealistic high-end editorial press photograph, close-up on a lab workbench: "
    "two physically different large AI accelerator modules lying side by side on a grey "
    "anti-static mat, shot on an 85mm lens at f/2 on a full-frame camera, shallow depth of field. "
    "Left module: a broad GPU-style accelerator carrier board, a heavy printed circuit board "
    "with a large finned aluminium heatsink, exposed copper vapour chamber, thick braided power "
    "cables and gold edge connector. Right module: a distinctly different custom ASIC module, "
    "a smaller square package on a compact green board with a machined metal lid, dense rows of "
    "surface-mount capacitors and fine traces, seated in a metal retention frame. "
    "The two boards differ clearly in shape, size and layout, sitting flat and parallel, "
    "both softly dusted with realistic wear and handling marks. "
    "In the softly blurred background a technician's blue nitrile gloved hands hold a fine "
    "test probe over a bench instrument, completely out of focus, only shapes and light. "
    "Warm directional lab lighting from the upper left, warm tungsten and grey workbench tones, "
    "gentle shadows, out-of-focus insulated test leads and a matte metal bench edge behind. "
    "Sharp focus on the two modules, extremely fine material detail, natural colour, "
    "documentary stock photography, 16:9 landscape framing. "
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


def main():
    import fal_client
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261122
    out = sys.argv[2] if len(sys.argv) > 2 else OUTPUT

    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal flux/schnell (seed={seed})...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": seed,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(r.content)

    img = Image.open(out).convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.Resampling.LANCZOS)

    # fit under 400KB
    q = 90
    while q >= 60:
        img.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(out)
        if size <= 400 * 1024:
            break
        q -= 4
    print(f"Saved {out} size={img.size} bytes={os.path.getsize(out)} quality={q}")


if __name__ == "__main__":
    main()
