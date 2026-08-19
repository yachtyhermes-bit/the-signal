#!/usr/bin/env python3
"""Regenerate AMAT hero (amat-china-back-to-growth-ai-supercycle-2026) — attempt 1.

Reason: previous hero had a garbled/hallucinated "AUTOMATION" letter-soup label
on a machine cell frame. New prompt: technician-from-behind composition with
blank, unmarked equipment surfaces (pattern proven in regen-qcom-hero.py).
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "amat-china-back-to-growth-ai-supercycle-2026"

PROMPT = (
    "Ultra-realistic professional photograph inside a vast semiconductor "
    "equipment manufacturing cleanroom: a technician wearing a full white bunny "
    "suit and face shield, seen from behind and slightly to the side, standing "
    "beside a large wafer-fabrication machine and inspecting a circular silicon "
    "wafer held in gloved hands, wide-angle view with tall smooth white and "
    "light-gray equipment cabinets receding into the background, every cabinet "
    "panel completely blank and unmarked, bright even overhead LED lighting, "
    "reflective light-gray anti-static floor, cool blue-white industrial "
    "palette with subtle warm accents, shallow depth of field, photorealistic "
    "corporate photography, high detail, 4K, shot on a full-frame DSLR. "
    "STRICTLY no text, no letters, no numbers, no labels, no engraved plates, "
    "no nameplates, no logos, no brand names, no signage, no banners, no "
    "screens, no monitors, no displays, no UI, no silkscreen markings, no "
    "watermark, no illustration, no digital art, no neon, no glowing lines, "
    "no abstract shapes."
)

TARGET_W, TARGET_H = 1920, 1080
GEN_W, GEN_H = 1440, 810
OUT_DIR = "/home/chino/thesignal/public/img/articles"
BACKUP_DIR = "/home/chino/thesignal/_backup_dist/img/articles"


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)


def generate():
    import fal_client
    print("Generating image with FAL flux/schnell...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": GEN_W, "height": GEN_H},
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
        raise RuntimeError(f"Could not find image URL in result: {list(result.keys())}")
    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    return r.content


def process_and_save(data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print(f"Raw dimensions: {w}x{h}")
    target_ratio = TARGET_W / TARGET_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    if img.size != (TARGET_W, TARGET_H):
        img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"{SLUG}.jpg")
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Saved {out_path} ({img.size[0]}x{img.size[1]}, {os.path.getsize(out_path)} bytes)")
    bak = os.path.join(BACKUP_DIR, f"{SLUG}.jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {bak}")
    return out_path


def main():
    load_fal_key()
    data = generate()
    out = process_and_save(data)
    print(f"DONE: {out}")


if __name__ == "__main__":
    main()
