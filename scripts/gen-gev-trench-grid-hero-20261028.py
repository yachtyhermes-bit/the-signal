#!/usr/bin/env python3
"""Generate hero image for gev-trench-grid-acquisition-2026.

Scene: high-voltage electrical substation / switchyard with large power
transformers, insulator stacks, bushings and steel lattice transmission towers
at golden hour / blue-hour dusk. Text-free photo-realistic stock photography,
16:9 1920x1080 center-crop.

Usage: python3 gen-gev-trench-grid-hero-20261028.py [1|2|3]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "gev-trench-grid-acquisition-2026"

PROMPTS = {
    1: (
        "Professional stock photograph of a high-voltage electrical substation at dusk, "
        "three massive oil-filled power transformers in a row with cooling fins, tall stacks "
        "of porcelain insulator bushings and thick aluminum bus bars above them, a steel "
        "lattice transmission tower rising behind, heavy cables strung in catenary curves "
        "against a deep blue evening sky with the last warm orange band of sunset low on the "
        "horizon, warm sodium work lights glowing on the steel structures, gravel switchyard "
        "floor with wet reflections, shallow depth of field, professional lighting, cinematic "
        "industrial landscape photography, sharp detail, 4K, shot on a full-frame DSLR, "
        "realistic photo. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no people, no server room, no data center, no hallway, no interior, "
        "no screens, no monitors, no illustration, no digital art, no neon, no glowing lines, "
        "no abstract shapes, no geometric patterns, no HUD overlays."
    ),
    2: (
        "Professional stock photograph of a large electrical substation switchyard at golden "
        "hour, rows of giant gray power transformers with ceramic insulator bushings and "
        "radiator banks, steel lattice gantry frames overhead carrying high-voltage conductors, "
        "a tall transmission pylon in the near foreground, warm low golden sunlight raking "
        "across brushed metal and galvanized steel, long shadows on the gravel yard, dry grass "
        "at the edges, soft haze near the horizon, wide-angle industrial landscape photography, "
        "shallow depth of field, professional lighting, sharp detail, 4K, shot on a full-frame "
        "DSLR, realistic photo. "
        "No text, no letters, no numbers, no signage, no labels, no logos, no brand marks, "
        "no people, no server room, no data center, no hallway, no interior, no screens, "
        "no illustration, no digital art, no neon, no glowing lines, no abstract shapes, "
        "no geometric patterns, no HUD overlays."
    ),
    3: (
        "Unretouched documentary photograph of a working high-voltage substation in flat "
        "overcast daylight, a cluster of weathered gray power transformers with rust streaks, "
        "chipped paint and dusty ceramic insulator bushings, steel lattice transmission tower "
        "and sagging conductors behind them, galvanized conduit and gravel yard, scrubby weeds "
        "at the base of the equipment, flat soft gray sky, muted natural color, slight sensor "
        "grain, minor lens vignetting, imperfect framing like a press wire photo, 35mm lens, "
        "f/5.6, realistic photo, photojournalism. "
        "No text, no letters, no numbers, no signage, no labels, no logos, no brand marks, "
        "no people, no server room, no data center, no hallway, no interior, no screens, "
        "no illustration, no digital art, no neon, no glowing lines, no abstract shapes, "
        "no geometric patterns, no HUD overlays, no lens flare, no dramatic lighting."
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
    print("Prompt: " + prompt[:160] + "...")
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
        raise RuntimeError("Could not find image URL in result: " + str(list(result.keys())))
    print("Image URL: " + str(image_url))
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    return r.content


def process_and_save(data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print("Raw dimensions: " + str(w) + "x" + str(h))
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
    out_path = os.path.join(OUT_DIR, SLUG + ".jpg")
    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print("Saved " + out_path + " (" + str(img.size[0]) + "x" + str(img.size[1]) + ", " + str(os.path.getsize(out_path)) + " bytes)")
    bak = os.path.join(BACKUP_DIR, SLUG + ".jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + bak)
    return out_path


def main():
    attempt = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    load_fal_key()
    print("=== [" + SLUG + "] attempt " + str(attempt) + " ===")
    data = generate(PROMPTS[attempt])
    process_and_save(data)
    print("DONE")


if __name__ == "__main__":
    main()
