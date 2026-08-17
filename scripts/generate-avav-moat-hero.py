#!/usr/bin/env python3
"""Generate AVAV Switchblade defense drone moat hero image via FAL flux/schnell, save + upload to R2."""
import os
import sys
import requests
from PIL import Image

W, H = 1200, 675
SLUG = "avav-switchblade-defense-drone-moat-2026"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional stock photograph of two military drone operators in camouflage uniforms "
    "kneeling in a grassy field at dusk, one viewing a rugged tablet displaying live aerial "
    "drone footage with a terrain map, the other pointing toward the sky. In the softly blurred "
    "background, a Switchblade-style loitering munition drone with folded wings rests on a "
    "launch tube beside a military ground vehicle. Realistic outdoor scene, natural golden-hour "
    "lighting, shallow depth of field with creamy bokeh, professional photojournalism style like "
    "Defense News magazine. Ultra-realistic photograph, sharp focus on the operators and tablet, "
    "high detail, cinematic quality, natural skin tones and fabric textures. No text overlays, "
    "no logos, no digital art, no abstract elements, no neon lights, no glowing lines, no "
    "geometric patterns."
)

def main():
    import fal_client

    # Resolve FAL_KEY from env or known key files
    key = os.environ.get("FAL_KEY")
    if not key:
        candidates = [
            "/home/chino/video_output/.fal_real",
            "/home/chino/hermes-workspace/studio-api/.env",
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            if "=" in line and line.split("=", 1)[0].strip() == "FAL_KEY":
                                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                                if val:
                                    key = val
                                    break
                            elif "|" in line and "FAL" in line:
                                val = line.split("|", 1)[1].strip()
                                if val:
                                    key = val
                                    break
                            elif line.startswith("fal-") or len(line) > 30:
                                key = line.split("\n")[0].strip()
                                break
                except Exception:
                    continue
            if key:
                break

    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    os.environ["FAL_KEY"] = key

    print(f"Generating image with FAL flux/schnell...")
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

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    file_size = os.path.getsize(OUTPUT)
    print(f"Saved to {OUTPUT}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

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

    print(f"All checks passed!")

    # --- Upload to R2 ---
    print(f"\nUploading to R2...")
    rc = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if rc == 0:
        print(f"R2 upload complete!")
    else:
        print(f"R2 upload failed (exit code {rc})")
        sys.exit(1)

    r2_url = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"
    print(f"All done! Image at: {r2_url}")


if __name__ == "__main__":
    main()
