#!/usr/bin/env python3
"""Regenerate HBM hero (cron 2026-08-19): text-free photo-realistic prompt, 16:9 1920x1080.

Usage: python3 regen-hbm-hero-20260819.py [1|2]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "hbm-ai-memory-bottleneck-explainer-2026"

PROMPTS = {
    1: (
        "Professional stock photograph macro shot of stacked high-bandwidth memory modules in a "
        "semiconductor cleanroom manufacturing environment. Tall stacks of smooth dark silicon memory "
        "dies with completely blank unmarked surfaces, gold contact pins, a precise robotic probe arm "
        "lowering toward the stack, shallow depth of field, cool blue and silver industrial palette, "
        "bright even cleanroom lighting, realistic semiconductor photography, 4K, shot on a full-frame "
        "DSLR. No text, no letters, no numbers, no markings, no engravings, no labels, no logos, no "
        "brand marks, no screens, no monitors, no displays, no UI, no signage, no people, no "
        "illustration, no digital art, no neon, no abstract shapes."
    ),
    2: (
        "Professional stock photograph of a modern semiconductor fabrication cleanroom aisle at a "
        "medium distance. Rows of tall smooth white and light-gray equipment cabinets with completely "
        "blank unmarked doors, a robotic wafer-handling arm moving a circular silicon wafer in the "
        "foreground, bright even overhead lighting, reflective light-gray anti-static floor, cool "
        "blue-white palette, shallow depth of field, realistic industrial photography, 4K, shot on a "
        "full-frame DSLR. No text, no letters, no numbers, no markings, no silkscreen printing, no "
        "labels, no logos, no brand marks, no chips with printed markings, no screens, no monitors, "
        "no displays, no UI, no signage, no people, no illustration, no digital art, no neon, no "
        "abstract shapes."
    ),
}

TARGET_W, TARGET_H = 1920, 1080
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


def generate(prompt):
    import fal_client
    print(f"Prompt: {prompt[:150]}...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": 1440, "height": 810},
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
    attempt = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    load_fal_key()
    print(f"=== [{SLUG}] attempt {attempt} ===")
    data = generate(PROMPTS[attempt])
    process_and_save(data)
    print("DONE")


if __name__ == "__main__":
    main()
