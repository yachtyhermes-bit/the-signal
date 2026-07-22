#!/usr/bin/env python3
"""Generate a hero image for 'crm-agentforce-doubt-discount-2026' using FAL flux/schnell."""

import os
import sys
import requests

SLUG = "crm-agentforce-doubt-discount-2026"
W, H = 1200, 675

OUTPUT1 = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT2 = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional high-end stock photograph of a modern corporate office with a large AI analytics dashboard "
    "displayed on a wall-mounted screen, showing enterprise AI performance metrics and data visualizations. "
    "Salesforce-themed blue and white color palette. A sleek glass conference room or executive boardroom, "
    "dark moody ambient lighting with dramatic shadows, rain-streaked windows overlooking a city skyline at dusk. "
    "Photo-realistic, shallow depth of field, professional lighting, ultra-realistic, sharp focus, high detail. "
    "No text overlays, no logos, no branding. Photographed with a full-frame DSLR, cinematic grading."
)

def main():
    import fal_client

    # Set FAL_KEY from the studio-api env file
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    break

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero image for '{SLUG}'...")
    print(f"Prompt: {PROMPT[:100]}...")

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

    # Save to both locations
    from PIL import Image
    img_data = r.content

    for output_path in [OUTPUT1, OUTPUT2]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(img_data)

        file_size = os.path.getsize(output_path)
        print(f"✅ Saved to {output_path}")
        print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

        # Verify and resize if needed
        img = Image.open(output_path)
        print(f"   Dimensions: {img.size}")

        if img.size != (W, H):
            print(f"⚠️  Resizing from {img.size} to ({W}, {H})...")
            img = img.resize((W, H), Image.LANCZOS)
            img.save(output_path, "JPEG", quality=92, optimize=True)
            file_size = os.path.getsize(output_path)
            print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")
            print(f"   New dimensions: {img.size}")

        if file_size < 10240:
            print(f"⚠️  File too small ({file_size} bytes), re-saving with higher quality...")
            img.save(output_path, "JPEG", quality=98, optimize=True)
            file_size = os.path.getsize(output_path)
            print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    print("✅ Local saves complete!")

    # --- Upload to R2 ---
    print(f"\nUploading to R2 via r2_upload.py...")
    result = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if result == 0:
        print(f"✅ R2 upload succeeded!")
    else:
        print(f"❌ R2 upload failed (exit code {result})")
        sys.exit(1)

    # Verify accessibility
    print(f"\nVerifying image on R2 CDN...")
    try:
        resp = requests.head(R2_URL, timeout=30)
        print(f"   HTTP {resp.status_code}")
        if resp.status_code == 200:
            print(f"✅ Image accessible at: {R2_URL}")
        else:
            print(f"⚠️  Got HTTP {resp.status_code}, might not be publicly accessible")
    except Exception as e:
        print(f"⚠️  Verification error: {e}")

    print(f"\n✅ All done! R2 URL: {R2_URL}")


if __name__ == "__main__":
    main()
