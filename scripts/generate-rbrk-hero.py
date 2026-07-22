#!/usr/bin/env python3
"""Generate a Rubrik (RBRK) hero image using FAL flux/schnell."""
import os
import sys
import requests

SLUG = "rbrk-cyber-resilience-secular-growth-2026"
W, H = 1200, 675
OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
    f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg",
]

PROMPT = (
    "Professional stock photograph of a modern enterprise data center server room. "
    "Rows of sleek server racks with cool blue LED status lights, "
    "clean cable management, raised floor tiles, and overhead cooling vents. "
    "A subtle glowing digital shield or data security icon visible on a monitor "
    "in the foreground. Photorealistic, shallow depth of field, professional lighting, "
    "corporate technology photography style, 8K resolution, sharp focus. "
    "No neon, no abstract art, no glowing lines, no geometric patterns. "
    "Real data center aesthetic with cyan and blue ambient lighting."
)

def main():
    import fal_client

    # Set the FAL key from known location
    fal_key_path = "/home/chino/video_output/.fal_real"
    with open(fal_key_path) as f:
        raw = f.read().strip().split("\n")[0]
        if "|" in raw:
            fal_key = raw.split("|", 1)[1]
        else:
            fal_key = raw
    os.environ["FAL_KEY"] = fal_key

    print(f"Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:120]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {
                "width": W,
                "height": H
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

    print(f"Downloading image...")
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

    print(f"✅ All checks passed!")

if __name__ == "__main__":
    main()
