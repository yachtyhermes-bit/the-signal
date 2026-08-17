#!/usr/bin/env python3
"""Generate a Zscaler hero image using FAL flux/schnell — photo-realistic security operations center."""

import os
import sys
import requests

SLUG = "zs-cloud-native-zero-trust-moat-2026"
W, H = 1200, 675
OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
]

PROMPT = (
    "Professional stock photograph of a modern cloud data center security operations center "
    "with rows of server racks and large security monitoring dashboards on wall screens. "
    "Realistic photo, shallow depth of field, professional lighting, cool blue ambient glow "
    "from monitors, clean modern facility, a few security analysts working at desks in the "
    "background. No text overlays, no logos, no branding. Photographed with a full-frame DSLR, "
    "cinematic color grading, sharp focus, high-end corporate editorial style."
)


def main():
    import fal_client

    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        fal_key_path = "/home/chino/video_output/.fal_real"
        with open(fal_key_path) as f:
            raw = f.read().strip().split("\n")[0]
            if "|" in raw:
                fal_key = raw.split("|", 1)[1]
            else:
                fal_key = raw
        os.environ["FAL_KEY"] = fal_key

    print(f"Generating hero image for '{SLUG}'...")
    print(f"Prompt: {PROMPT[:120]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {
                "width": W,
                "height": H,
            },
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    print(f"Result keys: {list(result.keys())}")

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print(f"ERROR: Could not find image URL in result")
        print(f"Full result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    for outpath in OUTPUTS:
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "wb") as f:
            f.write(r.content)
        file_size = os.path.getsize(outpath)
        print(f"✅ Saved to {outpath}")
        print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    from PIL import Image
    img = Image.open(OUTPUTS[0])
    print(f"   Dimensions: {img.size}")

    if img.size != (W, H):
        print(f"⚠️  Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        for outpath in OUTPUTS:
            img.save(outpath, "JPEG", quality=92, optimize=True)
            file_size = os.path.getsize(outpath)
            print(f"   Saved {outpath}: {file_size} bytes ({file_size/1024:.1f} KB)")

    for outpath in OUTPUTS:
        file_size = os.path.getsize(outpath)
        if file_size < 10240:
            print(f"⚠️  File too small ({file_size} bytes), re-saving with higher quality...")
            img.save(outpath, "JPEG", quality=98, optimize=True)
            file_size = os.path.getsize(outpath)
            print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    print("✅ Local save complete!")


if __name__ == "__main__":
    main()
