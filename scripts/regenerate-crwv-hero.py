#!/usr/bin/env python3
"""Regenerate hero for 'crwv-q2-2026-earnings-ai-cloud-inflection' via FAL flux/schnell.

Attempt 1 prompt: exterior AI cloud data center campus at dusk — architectural,
photo-realistic, zero text/signage/logos/letters/numbers anywhere.
"""

import os
import sys
import requests

SLUG = "crwv-q2-2026-earnings-ai-cloud-inflection"
W, H = 1440, 810  # 16:9 generation size

OUTPUT1 = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT2 = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional aerial photograph of a massive AI cloud data center campus at dusk. "
    "Rows of long, low concrete warehouse buildings with white cooling towers and rooftop HVAC units, "
    "a large electrical substation with tall transmission towers and power lines, "
    "blue-hour sky with soft clouds, warm amber light glowing from louvered ventilation grilles on the building facades, "
    "gravel service roads and security fencing, wide-angle architectural photography, "
    "photo-realistic, shot on a full-frame DSLR, sharp detail, 4K. "
    "No text anywhere, no signage, no logos, no brand markings, no letters, no numbers, "
    "no billboards, no screens, no monitors, no vehicles with markings."
)


def main():
    import fal_client

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

    print(f"Generating hero image for '{SLUG}' (attempt: {os.environ.get('ATTEMPT', '1')})...")
    print(f"Prompt: {PROMPT[:120]}...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print(f"ERROR: Could not find image URL in result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")
    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    from PIL import Image
    import io

    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    print(f"Downloaded dimensions: {img.size}")

    # Center-crop to 16:9, then resize to 1920x1080
    tw, th = img.size
    target_ratio = 16 / 9
    if tw / th > target_ratio:
        new_w = int(th * target_ratio)
        left = (tw - new_w) // 2
        img = img.crop((left, 0, left + new_w, th))
    elif tw / th < target_ratio:
        new_h = int(tw / target_ratio)
        top = (th - new_h) // 2
        img = img.crop((0, top, tw, top + new_h))
    img = img.resize((1920, 1080), Image.LANCZOS)
    print(f"Final dimensions: {img.size}")

    for output_path in [OUTPUT1, OUTPUT2]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(output_path)
        print(f"✅ Saved to {output_path} ({file_size/1024:.1f} KB)")

    print("✅ Local saves complete!")

    # Upload to R2
    print("\nUploading to R2 via r2_upload.py...")
    result_code = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if result_code == 0:
        print("✅ R2 upload succeeded!")
    else:
        print(f"❌ R2 upload failed (exit code {result_code})")
        sys.exit(1)

    try:
        resp = requests.head(R2_URL, timeout=30)
        print(f"R2 HEAD: HTTP {resp.status_code}")
    except Exception as e:
        print(f"⚠️  R2 verification error: {e}")

    print(f"\n✅ All done! R2 URL: {R2_URL}")


if __name__ == "__main__":
    main()
