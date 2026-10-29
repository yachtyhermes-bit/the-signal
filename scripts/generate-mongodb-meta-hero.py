#!/usr/bin/env python3
"""Generate the MongoDB / Meta enterprise-AI hero image.

Concept: a vast physical card-catalog archive hall — a wall of index-card
drawers read as a monument to records/data. A single hand pulls one drawer.
Photo-realistic, shallow depth of field, no text/numbers/logos anywhere.
Deliberately NOT a data center / server aisle.
"""
import os
import sys
import requests
from PIL import Image

OUTPUT = "/home/chino/thesignal/public/img/articles/mongodb-meta-ceo-enterprise-ai-platform-2026.jpg"
SLUG = "mongodb-meta-ceo-enterprise-ai-platform-2026"
W, H = 1440, 810          # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080  # final 16:9 output

PROMPT = (
    "Ultra-realistic professional stock photograph of a vast historic archive hall "
    "filled with tall wooden cabinets of small index-card catalog drawers, thousands "
    "of identical drawers receding into soft focus in the distance, warm ambient "
    "window light mixed with gentle overhead lamps, honey-colored aged oak, clean "
    "and beautifully lit. In the near foreground a single human hand reaches in from "
    "the right edge and pulls one drawer slightly open, shallow depth of field, the "
    "hand and open drawer tack sharp, the deep rows of cabinets dissolving into "
    "creamy bokeh, cinematic corporate editorial photography, 85mm lens look, "
    "high detail, natural color palette. "
    "STRICTLY no text, no letters, no numbers, no logos, no brand names, no labels, "
    "no signage, no watermark, no screens, no visible faces, no glowing lines, no "
    "neon, no holograms."
)


def load_fal_key():
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    for env_path in ["/home/chino/hermes-workspace/studio-api/.env",
                     "/home/chino/video_output/.fal_real"]:
        if os.path.exists(env_path):
            try:
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("FAL_KEY="):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val:
                                os.environ["FAL_KEY"] = val
                                return val
            except Exception:
                continue
    return None


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with FAL flux/schnell...")
    print(f"Prompt: {prompt[:160]}...")
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
    target_ratio = FINAL_W / FINAL_H
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
    img = img.convert("RGB")
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 10240:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")


if __name__ == "__main__":
    main()
