#!/usr/bin/env python3
"""Generate FTNT hero image using FAL flux/schnell."""
import os
import sys
import requests
import shutil

SLUG = "ftnt-boring-cyber-consolidator-2026"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1200, 675

PROMPT = (
    "Professional stock photograph of a modern enterprise network security operations center, "
    "rows of server racks with blinking status lights, large screens displaying network security dashboards and firewall traffic maps, "
    "clean corporate data center environment with cool blue and white LED lighting, "
    "security monitoring station with multiple monitors, enterprise technology atmosphere. "
    "Photo-realistic, shallow depth of field, professional corporate lighting. "
    "No text overlays, no logos, no branding. Ultra-realistic, sharp focus, high detail, 8K resolution."
)

def main():
    import fal_client

    print(f"Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:100]}...")

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

    # Save to primary location
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    file_size = os.path.getsize(OUTPUT)
    print(f"✅ Saved to {OUTPUT}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    # Verify and resize dimensions
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

    # Copy to backup location
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy2(OUTPUT, BACKUP)
    backup_size = os.path.getsize(BACKUP)
    print(f"✅ Copied to {BACKUP}")
    print(f"   Size: {backup_size} bytes ({backup_size/1024:.1f} KB)")

    print(f"✅ All checks passed!")

if __name__ == "__main__":
    main()
