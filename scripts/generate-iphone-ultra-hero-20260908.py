#!/usr/bin/env python3
"""Generate hero image for apple-foldable-iphone-ultra-2026 via FAL flux/schnell.

Photo-realistic editorial/product photography of an OPEN foldable smartphone.
No datacenter/server-room, no abstract art, no neon, no text/logos/watermarks.
"""

import os
import sys
import hashlib
import requests

SLUG = "apple-foldable-iphone-ultra-2026"
W, H = 1200, 675
OUTPUT_PUBLIC = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT_BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
OUTPUTS = [OUTPUT_PUBLIC, OUTPUT_BACKUP]

PROMPT = (
    "Ultra-realistic premium product-advertising editorial photograph of an elegant, "
    "sleek OPEN foldable smartphone with a large seamless crease-free inner display, "
    "gently held in one hand above a bright minimal white marble café table, soft diffused "
    "daylight from a large window, blurred modern interior background with warm neutral "
    "tones and leafy green plants, shallow depth of field, professional studio-quality "
    "lighting, a few tasteful reflective highlights glinting off the polished titanium "
    "edges and glass, crisp sharp focus on the device, high-end editorial tech-magazine "
    "style. The device has no brand logo, no name, and the display shows no text, no "
    "icons, no UI, no apps — the inner screen is completely plain and dark and unmarked. "
    "No text anywhere in the frame, no letters, no numbers, no watermark, no signage. "
    "Photorealistic, natural color grading, full-frame DSLR look, 50mm lens, 16:9 "
    "landscape composition, 1200x675."
)


def load_fal_key():
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    real_path = "/home/chino/video_output/.fal_real"
    with open(real_path) as f:
        raw = f.read().strip().split("\n")[0]
    if "|" in raw:
        raw = raw.split("|", 1)[1]
    os.environ["FAL_KEY"] = raw
    return raw


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    import fal_client
    from PIL import Image

    key = load_fal_key()
    print(f"FAL key loaded: {key[:8]}...{key[-4:]} (len {len(key)})")

    print(f"Generating hero image for '{SLUG}'...")
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
        print(f"ERROR: no image URL in result: {result}")
        sys.exit(1)
    print(f"Image URL: {image_url}")

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    # Save raw bytes to public path first
    os.makedirs(os.path.dirname(OUTPUT_PUBLIC), exist_ok=True)
    with open(OUTPUT_PUBLIC, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT_PUBLIC)
    print(f"Downloaded dimensions: {img.size}, bytes: {len(r.content)}")

    # Verify/resize to exactly 1200x675
    if img.size != (W, H):
        print(f"Resizing from {img.size} to ({W}, {H}) with LANCZOS...")
        img = img.resize((W, H), Image.LANCZOS)

    # Save final JPEG to both locations
    for outpath in OUTPUTS:
        img.save(outpath, "JPEG", quality=92, optimize=True)
        size = os.path.getsize(outpath)
        print(f"Saved {outpath}: {size} bytes ({size/1024:.1f} KB)")
        if size < 10240:
            print(f"  File <10KB ({size}), re-saving quality=98...")
            img.save(outpath, "JPEG", quality=98, optimize=True)
            size = os.path.getsize(outpath)
            print(f"  New size: {size} bytes ({size/1024:.1f} KB)")

    # Final verification of both copies
    for outpath in OUTPUTS:
        im = Image.open(outpath)
        print(f"Final check {outpath}: dims={im.size}, bytes={os.path.getsize(outpath)}, md5={md5_of(outpath)}")

    print("LOCAL_SAVE_DONE")


if __name__ == "__main__":
    main()
