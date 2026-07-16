#!/usr/bin/env python3
"""Generate a photorealistic Reddit HQ hero image for The Signal using FAL flux/schnell."""

import os
import sys
import requests

OUTPUT = "/home/chino/thesignal/public/img/articles/rddt-ai-data-licensing-moat-2026.jpg"
SLUG = "rddt-ai-data-licensing-moat-2026"
W, H = 1200, 675

PROMPT = (
    "Professional stock photograph of the Reddit headquarters building exterior in "
    "San Francisco. The Reddit logo visible on the building sign or entrance. Modern "
    "tech office architecture with glass facade, clear blue sky, professional "
    "real-estate photography style. Shallow depth of field, professional lighting, "
    "photorealistic, 8K resolution, sharp focus, high detail."
)

def main():
    import fal_client

    print(f"Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:80]}...")

    # Use the subscribe method which blocks until complete
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

    # Extract the image URL
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

    # Download the image
    print(f"Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    # Save to output path
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    file_size = os.path.getsize(OUTPUT)
    print(f"✅ Saved to {OUTPUT}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    # Verify dimensions
    from PIL import Image
    img = Image.open(OUTPUT)
    print(f"   Dimensions: {img.size}")

    if img.size != (W, H):
        print(f"⚠️  Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")
        print(f"   New dimensions: {img.size}")

    if file_size < 10240:
        print(f"⚠️  File too small ({file_size} bytes), re-saving with higher quality...")
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    print(f"✅ All checks passed!")


if __name__ == "__main__":
    main()
