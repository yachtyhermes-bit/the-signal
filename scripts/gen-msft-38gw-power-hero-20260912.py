#!/usr/bin/env python3
"""Generate hero image for msft-38gw-power-buildout-2026.

Scene: high-voltage substation / switchyard with large transformers and steel
lattice transmission pylons at golden hour, power lines receding to horizon.
Text-free photo-realistic stock photography, 16:9 1920x1080 center-crop.

Usage: python3 gen-msft-38gw-power-hero-20260912.py [1|2|3]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "msft-38gw-power-buildout-2026"

PROMPTS = {
    1: (
        "Professional stock photograph of a large high-voltage electrical substation "
        "switchyard at golden hour, rows of massive steel transformers and porcelain "
        "insulator bushings, tall steel lattice transmission pylons carrying thick high-voltage "
        "power lines receding toward the horizon across open flat countryside, warm low golden "
        "sunlight raking across the steel structures and casting long shadows on dry grass, "
        "clear sky with soft haze near the horizon, dramatic depth, cinematic wide-angle "
        "industrial landscape photography, sharp detail, 4K, shot on a full-frame DSLR, "
        "photo-realistic. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
        "no digital art, no neon, no glowing lines, no abstract shapes, no geometric patterns."
    ),
    2: (
        "Professional stock photograph of high-voltage electricity transmission towers crossing "
        "open farmland at golden hour, tall steel lattice pylons in a receding line with heavy "
        "power lines sagging between them toward a distant substation, warm low sun behind the "
        "towers, long shadows stretching across mown fields, faint haze and dust in the air, "
        "wide cinematic landscape photography, natural realistic lighting, sharp detail, 4K, "
        "shot on a full-frame DSLR, photo-realistic. "
        "No text, no letters, no numbers, no signage, no labels, no logos, no brand marks, "
        "no signage of any kind, no people, no illustration, no digital art, no neon, "
        "no glowing lines, no abstract shapes, no geometric patterns, no server room."
    ),
    3: (
        "Professional stock photograph of a high-voltage electrical substation at sunset, "
        "large boxy gray transformers with cooling fins and steel gantry structures carrying "
        "thick high-tension cables, a steel lattice transmission pylon in the near foreground, "
        "warm golden orange light on brushed metal surfaces, deep gradient sky from gold to "
        "soft blue, gravel yard, cinematic industrial photography, shallow depth of field, "
        "professional lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
        "no digital art, no neon, no glowing lines, no abstract shapes, no geometric patterns."
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
