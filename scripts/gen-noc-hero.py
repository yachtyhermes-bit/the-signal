#!/usr/bin/env python3
"""Generate NOC hero image via FAL flux/schnell, save + upload to R2."""
import os, sys, shutil
import requests
from PIL import Image

W, H = 1200, 675
SLUG = "noc-b21-sentinel-strategic-triad-2026"

PROMPT = (
    "Professional military aviation photograph of a Northrop Grumman B-21 Raider stealth bomber "
    "on the tarmac at dusk. The aircraft is parked on a wet runway with dramatic low-key lighting "
    "from the setting sun breaking through dark storm clouds. The B-21 Raider has a distinctive "
    "flying-wing shape with stealth contours visible. Moody cinematic atmosphere with deep shadows "
    "and subtle rim lighting on the aircraft edges. Shallow depth of field, professional "
    "photography style like Defense News or Aviation Week magazine cover. Photo-realistic, "
    "moody blue-black sky with orange horizon glow. No text labels, no markings visible on "
    "the aircraft. Award-winning military photography composition."
)

OUTDIR = "/home/chino/thesignal/public/img/articles"
BACKUPDIR = "/home/chino/thesignal/_backup_dist/img/articles"

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(BACKUPDIR, exist_ok=True)

    import fal_client

    print(f"Generating image via fal-ai/flux/schnell...")
    print(f"Prompt: {PROMPT[:80]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
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
        print(f"ERROR: Could not find image URL")
        print(f"Result: {result}")
        sys.exit(1)

    print(f"Downloading from: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    # Save to primary location
    out_path = os.path.join(OUTDIR, f"{SLUG}.jpg")
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Saved primary: {out_path}")
    print(f"  Size: {os.path.getsize(out_path)} bytes")

    # Verify and resize if needed
    img = Image.open(out_path)
    print(f"  Dimensions: {img.size}")
    if img.size != (W, H):
        print(f"  Resizing to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        img.save(out_path, "JPEG", quality=92, optimize=True)
        print(f"  Resized size: {os.path.getsize(out_path)} bytes")

    # Copy to backup location
    backup_path = os.path.join(BACKUPDIR, f"{SLUG}.jpg")
    shutil.copy2(out_path, backup_path)
    print(f"Copied to backup: {backup_path}")
    print(f"  Backup size: {os.path.getsize(backup_path)} bytes")

    print(f"\nDone! Image ready at:")
    print(f"  {out_path}")
    print(f"  {backup_path}")

if __name__ == "__main__":
    main()
