#!/usr/bin/env python3
"""Generate an RTX (Raytheon Technologies) hero image using FAL flux/schnell."""

import os
import sys
import requests

TODAY = "2026-07-28"
SLUG = f"rtx-{TODAY}"
W, H = 1200, 675
OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
]

PROMPT = (
    "Professional stock photograph of a US Patriot missile defense system battery deployed in a field. "
    "Multiple launcher vehicles with missile canisters angled upward at dusk, with a phased-array radar "
    "system in the background. Military-grade hardware, olive-green vehicles, rugged terrain. "
    "Dramatic golden hour lighting with long shadows, shallow depth of field foreground to background, "
    "professional commercial photography, 8K resolution, sharp focus, cinematic color grading, "
    "high-end corporate editorial style. "
    "No text overlays, no logos, no branding. Photographed with a full-frame DSLR, telephoto lens."
)

def main():
    import fal_client

    # FAL_KEY is already in environment
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        # Fallback: read from file
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

    print(f"\n✅ All done! Final slug: {SLUG}")


if __name__ == "__main__":
    main()
