#!/usr/bin/env python3
"""Generate an AMZN (Amazon AWS AI cloud) hero image using FAL flux/schnell."""

import os
import sys
import requests

SLUG = "amzn-aws-ai-cloud-2026"
W, H = 1200, 675
OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
]

PROMPT = (
    "Professional stock photograph of a massive modern hyperscale data center interior. "
    "Long row of tall black server racks receding into the distance, each rack with "
    "small blue and green LED indicator lights, neatly organized fiber optic cables "
    "running along cable trays above the racks, clean polished reflective floor, "
    "cool white professional lighting with subtle blue ambient glow. "
    "Realistic photograph, shallow depth of field focused on the nearest racks, "
    "background softly blurred, professional corporate editorial photography. "
    "No people, no text overlays, no logos, no branding. Photographed with a full-frame "
    "DSLR, wide-angle lens, cinematic color grading, sharp focus, high-end editorial style. "
    "Not abstract art, not digital art, not neon, no glowing lines, no geometric patterns."
)

def main():
    import fal_client

    # FAL_KEY fallback: read from file
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

    for outpath in OUTPUTS:
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "wb") as f:
            f.write(r.content)
        file_size = os.path.getsize(outpath)
        print(f"✅ Saved to {outpath}")
        print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    # Verify and resize if needed
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

    # --- Upload to R2 ---
    print(f"\nUploading to R2 via r2_upload.py...")
    result_code = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if result_code == 0:
        print(f"✅ R2 upload succeeded!")
    else:
        print(f"❌ R2 upload failed (exit code {result_code})")
        sys.exit(1)

    # Verify accessibility
    R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"
    try:
        rr = requests.get(R2_URL, timeout=30)
        if rr.status_code == 200:
            print(f"✅ R2 URL accessible: {R2_URL} ({len(rr.content)} bytes)")
        else:
            print(f"❌ R2 URL check failed: HTTP {rr.status_code}")
    except Exception as e:
        print(f"⚠️  Could not verify R2 URL: {e}")

    print("✅ Done!")

if __name__ == "__main__":
    main()
