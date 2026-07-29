#!/usr/bin/env python3
"""Generate a Leidos (LDOS) hero image using FAL flux/schnell.

Theme: Defense IT / military command center — Leidos benefits from Iran escalation (July 29, 2026).
"""

import os
import sys
import requests

SLUG = "ldos-iran-escalation-defense-it-2026"
W, H = 1200, 675
OUTPUTS = [
    f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg",
]

PROMPT = (
    "Professional stock photograph of a modern military command and control operations center. "
    "Multiple large digital display screens on a wall showing tactical battlefield maps, satellite imagery, "
    "and defense data streams. Military personnel in uniforms seated at workstations with monitors. "
    "Muted blue and amber ambient lighting, realistic photo, shallow depth of field, "
    "professional corporate editorial photography, 8K resolution, sharp focus, "
    "high-end commercial grade image for a defense technology company. "
    "No text overlays, no logos, no branding on screens. "
    "Photographed with a full-frame DSLR, wide-angle lens, cinematically graded."
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
