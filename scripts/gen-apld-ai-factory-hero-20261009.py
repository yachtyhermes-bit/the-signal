#!/usr/bin/env python3
"""Hero image for apld-applied-digital-ai-factory-lease-model-2026 via fal flux/schnell.

Subject: Applied Digital (NASDAQ: APLD) builds and leases purpose-built 'AI Factory'
data-centre campuses, securing large amounts of grid power (~2.15 GW interconnected)
and signing 15-year take-or-pay leases with investment-grade hyperscalers.
Theme: a wide elevated exterior photograph of a large-scale AI computing campus under
construction on open flat prairie land at golden hour — long, low windowless
concrete-and-steel shell buildings with rooftop cooling units, tower cranes and steel
framing, a high-voltage substation and lattice transmission towers carrying power lines
toward the site, wide gravel access roads and graded earth.
Distinct from recent heroes (optical transceivers, switch chassis, switchgear, nuclear,
rocket and quantum hardware) and NOT a server-room aisle / data-centre corridor.
NO people, NO hands or body parts, NO text/lettering/numbers/logos anywhere in frame.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "apld-applied-digital-ai-factory-lease-model-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no watermarks, no signage, no flags. "
    "No people, no hands, no faces, no human figures, no silhouettes, no workers. "
    "No neon lights, no synthwave, no glowing lines, no digital or sci-fi effects, "
    "no 3D render sheen, no abstract art, no geometric patterns. "
    "Not a server-room aisle, not a data-centre corridor, not a top-down rooftop aerial. "
    "Strictly photorealistic editorial photography."
)

PROMPT = (
    "Wide elevated exterior documentary photograph of a large-scale AI computing campus "
    "under construction on open flat prairie land at golden hour, shot on a 35mm lens on a "
    "full-frame camera, low-elevation oblique view. "
    "Long, low, windowless concrete-and-steel shell data-centre buildings with rows of "
    "rooftop cooling units stretch across the site; two tall tower cranes and bare steel "
    "framing rise above the newest shell still under construction. "
    "A high-voltage electrical substation with transformers, busbar and lattice steel "
    "transmission towers carries power lines toward the site; wide gravel access roads and "
    "graded brown earth surround the buildings. "
    "Late-afternoon warm side light rakes across the prairie, casting long shadows with "
    "slight atmospheric haze on the horizon, muted earth and steel palette. "
    "Extremely high detail, 8k, documentary industrial photography, 16:9 landscape aspect ratio. "
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
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": 20261010,
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
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT)
    print(f"Saved: {OUTPUT} size={img.size} bytes={len(r.content)}")
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92)
        print(f"Upscaled to {FINAL_W}x{FINAL_H}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92)
    print(f"Copied to {BACKUP}")
    print("Done!")


if __name__ == "__main__":
    main()
