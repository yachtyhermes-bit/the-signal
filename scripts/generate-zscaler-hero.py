#!/usr/bin/env python3
"""Generate a ZS hero image using FAL flux/schnell, save locally, upload to R2."""

import os
import sys
import requests

OUTPUT = "/home/chino/thesignal/public/img/articles/zs-zero-trust-cloud-moat-2026.jpg"
SLUG = "zs-zero-trust-cloud-moat-2026"
W, H = 1200, 675

PROMPT = (
    "Professional stock photograph of a modern zero-trust cybersecurity operations center, "
    "rows of server racks with blue LED indicators, large wall-mounted security dashboards "
    "showing network traffic and threat analytics, clean corporate data center environment. "
    "Photo-realistic, shallow depth of field, professional lighting, dark tones with cool blue accents. "
    "No text overlays, no logos, no branding. Ultra-realistic, sharp focus, high detail."
)

R2_URL = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/zs-zero-trust-cloud-moat-2026.jpg"


def main():
    import fal_client

    print("Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:80]}...")

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
    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    # Save to output path
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    file_size = os.path.getsize(OUTPUT)
    print(f"Saved to {OUTPUT}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    # Verify dimensions
    from PIL import Image

    img = Image.open(OUTPUT)
    print(f"   Dimensions: {img.size}")

    if img.size != (W, H):
        print(f"Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")
        print(f"   New dimensions: {img.size}")

    if file_size < 10240:
        print(f"File too small ({file_size} bytes), re-saving with higher quality...")
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    print("Local save complete!")

    # --- Upload to R2 ---
    print("\nUploading to R2...")

    # Read token from .dev.vars
    token = ""
    with open("/home/chino/thesignal/.dev.vars") as f:
        for line in f:
            if line.startswith("CLOUDFLARE_API_TOKEN="):
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

    if not token:
        print("ERROR: CLOUDFLARE_API_TOKEN not found in .dev.vars")
        sys.exit(1)

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "image/jpeg",
    }

    with open(OUTPUT, "rb") as fh:
        resp = requests.put(R2_URL, headers=headers, data=fh.read())

    print(f"R2 upload HTTP {resp.status_code}")
    if resp.status_code in (200, 201):
        print(f"Uploaded to {R2_URL}")
    else:
        print(f"Upload failed: {resp.text}")
        sys.exit(1)

    print("All done!")


if __name__ == "__main__":
    main()
