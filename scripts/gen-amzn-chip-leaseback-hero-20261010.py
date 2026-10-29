#!/usr/bin/env python3
"""Hero image for amzn-nvidia-chip-sale-leaseback-2026 via fal flux/schnell.

Subject: Amazon (NASDAQ: AMZN) is reportedly moving ~$8bn of Nvidia Grace Blackwell
AI accelerator chips into a special purpose vehicle funded by outside investors and
then leasing the same hardware back — an off-balance-sheet way to fund its AI
data-centre buildout.
Physical subject: a large AI accelerator compute module (GPU card / rack-mount
accelerator tray with finned heatsink, power connector, circuit board) that is
being transferred, held and financed rather than simply owned.
Composition: tightly framed macro/product photograph on a grounded anti-static
electronics-lab workbench, 50mm lens, shallow depth of field, soft neutral light,
out-of-focus test equipment behind. Industrial, real, documentary.
NOT a data-centre corridor / server-room aisle. NOT a glowing microchip macro with
light trails. NOT an abstract finance or chart graphic.
NO people, NO hands or body parts, NO text/lettering/numbers/logos anywhere in frame.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "amzn-nvidia-chip-sale-leaseback-2026"
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
    "Not a server-room aisle, not a data-centre corridor, not a top-down aerial. "
    "Strictly photorealistic editorial product photography."
)

PROMPT = (
    "Tightly framed macro product photograph of a large AI accelerator compute module "
    "resting flat on a grounded anti-static mat on a metal electronics-lab workbench, "
    "shot on a 50mm lens at f/2.8 on a full-frame camera, shallow depth of field. "
    "The module is a heavy rack-mount accelerator tray: a wide printed circuit board with "
    "a large finned aluminium heatsink block, exposed copper vapour-chamber plate, rows of "
    "square high-density power connectors, gold edge contacts, thick braided power cables "
    "and small cylindrical capacitors and chokes around the board edge. "
    "Matte black metal shroud and brushed aluminium surfaces show fine machining marks, "
    "slight dust and realistic wear; the heatsink fins catch soft directional light. "
    "Soft neutral diffused professional studio lighting from above and to the left, gentle "
    "shadows on the workbench, cool grey-white background with out-of-focus laboratory test "
    "equipment, meters and cables softly blurred behind. "
    "Clean, industrial, real, documentary stock photography, sharp focus on the heatsink and "
    "connectors, extremely high detail, 8k, 16:9 landscape aspect ratio. "
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
