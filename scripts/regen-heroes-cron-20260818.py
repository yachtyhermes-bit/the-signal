#!/usr/bin/env python3
"""Regenerate failing hero images (cron 2026-08-18): text-free photo-realistic prompts, 16:9 1920x1080 output."""
import os
import sys
import io
import requests
from PIL import Image

SLUGS = [
    {
        "slug": "hii-nuclear-shipbuilding-duopoly-2026",
        "prompt": (
            "Professional stock photograph of a massive nuclear-powered submarine in a vast indoor shipyard "
            "dry dock. Dark stealthy submarine hull with smooth clean surfaces, workers in orange safety vests "
            "and hard hats welding near the bow, towering scaffolding and heavy industrial gantry structures, "
            "bright industrial lighting, moody atmosphere, realistic industrial photography, sharp detail, 4K, "
            "shot on a full-frame DSLR. "
            "No painted lettering or numbers on any equipment, no signage, no banners, no labels, no logos, "
            "no brand markings, no text anywhere in the image, no screens, no monitors, no displays, no UI, "
            "no people faces close-up, no illustration, no digital art, no neon, no abstract shapes."
        ),
    },
    {
        "slug": "hbm-ai-memory-bottleneck-explainer-2026",
        "prompt": (
            "Professional stock photograph macro shot of stacked high-bandwidth memory modules in a cleanroom "
            "manufacturing environment. Tall stacks of smooth dark silicon memory dies with completely blank "
            "unmarked surfaces, gold contact pins, a precise robotic probe arm lowering toward the stack, "
            "shallow depth of field, cool blue and silver industrial palette, bright even cleanroom lighting, "
            "realistic semiconductor photography, 4K, shot on a full-frame DSLR. "
            "No text, no letters, no numbers, no markings, no engravings, no labels, no logos, no brand marks, "
            "no screens, no monitors, no displays, no UI, no signage, no people, no illustration, no digital art, "
            "no neon, no abstract shapes."
        ),
    },
]

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


def generate(slug, prompt, attempt):
    import fal_client
    print(f"\n=== [{slug}] attempt {attempt} ===")
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


def process_and_save(slug, data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print(f"Raw dimensions: {w}x{h}")
    # Center-crop to 16:9
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
    # Resize to 1920x1080
    if img.size != (TARGET_W, TARGET_H):
        img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Saved {out_path} ({img.size[0]}x{img.size[1]}, {os.path.getsize(out_path)} bytes)")
    # Also mirror to backup dist if that dir exists
    bak = os.path.join(BACKUP_DIR, f"{slug}.jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {bak}")
    return out_path


def main():
    load_fal_key()
    for item in SLUGS:
        slug = item["slug"]
        for attempt in (1, 2):
            try:
                data = generate(slug, item["prompt"], attempt)
                process_and_save(slug, data)
                break
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt == 2:
                    print(f"ERROR: both generation attempts failed for {slug}")
                    sys.exit(1)
    print("\nAll regenerations complete.")


if __name__ == "__main__":
    main()
