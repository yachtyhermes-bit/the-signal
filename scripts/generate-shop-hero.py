#!/usr/bin/env python3
"""Generate SHOP hero image via FAL flux/schnell, save + upload to R2."""
import os
import sys
import requests
from PIL import Image

W, H = 1200, 675
SLUG = "shop-agentic-commerce-2026"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional stock photograph of a modern e-commerce fulfillment center warehouse "
    "with rows of organized shelving and packaged cardboard boxes ready for shipping. "
    "A worker in a branded vest uses a tablet computer to scan packages, with a Shopify "
    "point-of-sale terminal visible on a nearby workstation. Warm ambient warehouse lighting "
    "with shallow depth of field, professional commercial photography style like an annual "
    "report photograph. Photo-realistic, sharp focus, 8K, cinematic quality. "
    "No text overlays, no logos except subtle Shopify branding on a screen, no digital art, "
    "no abstract elements, no neon, no glowing lines."
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

    print(f"Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:100]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": W, "height": H},
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

    # --- Upload to R2 ---
    print(f"\nUploading to R2...")
    rc = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if rc == 0:
        print(f"✅ R2 upload complete!")
    else:
        print(f"❌ R2 upload failed (exit code {rc})")
        sys.exit(1)

    r2_url = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"
    print(f"✅ All done! Image at: {r2_url}")

if __name__ == "__main__":
    main()
