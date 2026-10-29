#!/usr/bin/env python3
"""Hero image for nbis-contract-backed-debt-neocloud-financing-2026 via fal flux/schnell.

Subject: Nebius Group (NASDAQ: NBIS), the AI "neocloud" that rents out GPU
capacity and finances its data-centre buildout with debt secured against
signed customer contracts.
Physical subject: a single fully-populated GPU compute rack cabinet standing in
a purpose-built compute hall, with its liquid-cooling loop attached.
Composition: close, three-quarter-view documentary photograph of ONE rack filling
most of the frame, 35mm lens, shallow depth of field, cool overhead industrial
light. The rack reads as a heavy, expensive, LEASED industrial asset.
NOT a data-centre corridor / symmetrical vanishing-point server aisle.
NOT a GPU board macro, NOT an export crate, NOT a construction site, NOT a
transmission tower, NOT a photonics lab bench.
NO people, NO hands or body parts, NO text/lettering/numbers/logos anywhere in frame.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "nbis-contract-backed-debt-neocloud-financing-2026"
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
    "no 3D render sheen, no abstract art, no geometric patterns, no charts, no HUD overlays. "
    "Not a receding server-room corridor, not a long symmetrical vanishing-point aisle, "
    "not a top-down aerial. Strictly photorealistic editorial stock photography."
)

PROMPT = (
    "Close, three-quarter-view documentary photograph of ONE fully-populated GPU compute "
    "rack cabinet standing in a purpose-built compute hall, filling most of the frame, "
    "shot on a 35mm lens at f/2.0 on a full-frame camera, shallow depth of field. "
    "The rack is a heavy industrial asset: brushed stainless and powder-coated steel, fine "
    "machining marks, realistic dust, scuffs and wear on the door frames and handles, "
    "thin horizontal vent slots, dense rows of discreet dark drive and compute sleds barely "
    "visible behind a perforated metal front door. "
    "Its liquid-cooling loop is attached to the rack: thick black insulated coolant hoses with "
    "woven texture and metal quick-disconnect couplings curling down the side, a stainless "
    "coolant distribution manifold with round pressure gauges and brass valves, and drip-free "
    "connectors, with a raised-floor cable tray carrying heavy coiled power and network cables "
    "along the base of the rack. "
    "Cool overhead industrial lighting casts soft top-down highlights on the metal edges and "
    "gentle shadows on the grey raised floor; a blurred curved concrete wall and dim ceiling "
    "structure recede softly out of focus behind the single rack. "
    "Heavy, expensive, well-used leased industrial equipment, no glowing accents, "
    "clean documentary editorial stock photography, extremely high detail, 8k, "
    "16:9 landscape aspect ratio. "
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
        "seed": 20261011,
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
