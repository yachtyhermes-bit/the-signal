#!/usr/bin/env python3
"""Regenerate LUNR GEO hero image — attempt 1 (text-free, emblem-plate-free prompt).

The previous hero had an AI-hallucinated red/white emblem with garbled letter
shapes on a suspended equipment cylinder. New prompt: wide scene, satellite bus
and solar wings as the subject, all surrounding equipment soft-blurred and far
from camera, no emblem plates anywhere.
"""
import os
import sys
import requests
from PIL import Image

OUTPUT = "/home/chino/thesignal/public/img/articles/lunr-geo-satellite-contract-record-backlog-space-2026.jpg"
W, H = 1440, 810  # 16:9 generation size; final output 1920x1080
FINAL_W, FINAL_H = 1920, 1080

PROMPT = (
    "Ultra-realistic professional stock photograph, wide establishing shot of a "
    "large geostationary communications satellite under assembly in a vast "
    "aerospace cleanroom: the white satellite bus with its large folded solar "
    "panel wings dominates the center frame, two engineers in white cleanroom "
    "bunny suits and hoods work beside it seen from behind at a distance, "
    "bright even overhead industrial lighting, clean white walls and sealed "
    "reflective floor, soft depth of field, distant equipment cabinets heavily "
    "blurred in the background, photorealistic corporate aerospace photography, "
    "high detail, 16:9 composition. "
    "STRICTLY no text, no letters, no numbers, no logos, no brand names, no "
    "emblem plates, no nameplates, no engraved plates, no labels, no stickers, "
    "no signage, no screens, no monitors, no displays, no visible UI, no "
    "watermark, no abstract art, no digital art, no neon, no glowing lines, no "
    "geometric patterns, no cartoon, no illustration."
)


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with FAL flux/schnell...")
    print(f"Prompt: {prompt[:120]}...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
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
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
    return img


def crop_to_16x9(img):
    """Center-crop to 16:9, then resize to 1920x1080."""
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H  # 16/9
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    img = generate(PROMPT, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 10240:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")


if __name__ == "__main__":
    main()
