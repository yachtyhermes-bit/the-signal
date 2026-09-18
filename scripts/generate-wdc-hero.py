#!/usr/bin/env python3
"""Generate hero image for 'wdc-hdd-pricing-power-ai-storage-2026' using FAL flux/schnell.

Subject: Western Digital (WDC) — maker of the nearline hard drives that store AI's
data explosion. Drive MANUFACTURING (mirror-like magnetic platters, actuator arms,
ePMR/UltraSMR recording, build-to-order factories).

Scene rules (per repo lessons):
- PHOTO-REALISTIC stock-photograph style ONLY. No digital art / neon / render.
- Scene: OPENED ENTERPRISE HDD inside a precision-manufacturing CLEANROOM —
  explicitly NOT a data center (recent heroes were antennas, data centers,
  power plants, photomask cleanrooms, optical lasers — this must be distinct).
- TEXT-FREE: no text, letters, numbers, logos, watermarks anywhere.
- 1200x675 (16:9), JPEG quality 92.

Usage: python3 scripts/generate-wdc-hero.py
"""
import os
import sys
import hashlib
import requests

SLUG = "wdc-hdd-pricing-power-ai-storage-2026"
W, H = 1200, 675

OUTPUT1 = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT2 = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

PROMPT = (
    "Professional stock photograph of an opened enterprise hard disk drive held in gloved "
    "hands inside a brightly lit precision manufacturing cleanroom, eleven mirror-like "
    "magnetic platters stacked on a spindle reflecting cool white light, the precision "
    "actuator arm with read/write heads swung over the platters, brushed aluminium drive "
    "chassis open on a clean workstation bench, shallow depth of field with the platters "
    "in sharp focus, background softly blurred drive-assembly equipment, professional "
    "lighting, high detail, 8K feel. "
    "No text, no letters, no numbers, no logos, no watermarks, no markings on any surface. "
    "No data center, no server racks, no server aisles, no glowing circuit lines, no neon, "
    "no synthwave, no abstract art, no digital art, no geometric patterns."
)


def load_fal_key():
    """Load FAL_KEY from the studio-api env file (proven pattern)."""
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return True
    return bool(os.environ.get("FAL_KEY"))


def md5sum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("FAL_KEY loaded OK")

    import fal_client

    print(f"\nGenerating hero image for '{SLUG}'...")
    print(f"Prompt: {PROMPT}")

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
        print("ERROR: Could not find image URL in result")
        print(f"Full result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    import io as _io
    from PIL import Image

    # Always re-encode via PIL to guarantee JPEG format, exact 1200x675 dims, q92
    img = Image.open(_io.BytesIO(r.content))
    img = img.convert("RGB")
    if img.size != (W, H):
        print(f"Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)

    for output_path in [OUTPUT1, OUTPUT2]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG", quality=92, optimize=True)
        print(f"Saved: {output_path}")

    file_size = os.path.getsize(OUTPUT1)
    print(f"Local file: {file_size} bytes ({file_size/1024:.1f} KB)")
    print(f"Dimensions: {img.size}")
    local_md5 = md5sum(OUTPUT1)
    backup_md5 = md5sum(OUTPUT2)
    print(f"MD5 (public):   {local_md5}")
    print(f"MD5 (backup):   {backup_md5}")
    assert local_md5 == backup_md5, "public and backup copies differ!"

    # --- Upload to R2 ---
    print("\nUploading to R2 via r2_upload.py...")
    result_code = os.system(f"cd /home/chino/thesignal && python3 scripts/r2_upload.py hero {SLUG}")
    if result_code != 0:
        print(f"R2 upload failed (exit code {result_code})")
        sys.exit(1)
    print("R2 upload succeeded!")

    # --- Verify accessibility + ETag ---
    print("\nVerifying image on R2 CDN...")
    resp = requests.head(R2_URL, timeout=30)
    print(f"   HTTP {resp.status_code}")
    etag = resp.headers.get("ETag", resp.headers.get("etag", ""))
    print(f"   ETag: {etag}")
    etag_clean = etag.strip('"')
    if resp.status_code == 200:
        print(f"Image accessible at: {R2_URL}")
        if etag_clean and etag_clean.lower() == local_md5:
            print(f"ETag matches local MD5: {local_md5}")
        else:
            print(f"ETag mismatch: remote={etag_clean} local={local_md5}")
    else:
        print(f"Got HTTP {resp.status_code}, might not be publicly accessible")

    print(f"\nAll done! R2 URL: {R2_URL}")


if __name__ == "__main__":
    main()
