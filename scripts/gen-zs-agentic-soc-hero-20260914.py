#!/usr/bin/env python3
"""Generate hero for zs-agentic-soc-security-agents-2026 (fal flux/schnell).

Subject: Zscaler (NASDAQ: ZS) — enterprise cloud security. The article is
about AI agents becoming the new attack surface, and Zscaler's answer being
an "Agentic SOC" where AI agents do the security-operations work. Context:
AI-infrastructure/semiconductor names selling off on an AI-slowdown scare
while cybersecurity names rally.

Scene chosen: an OVER-THE-SHOULDER CLOSE-UP of a single security analyst at
a modern workstation — shot from behind and slightly above the shoulder, the
person's back and one ear in the near frame, two monitors ahead showing
blurred, unreadable out-of-focus dashboard charts (no legible UI, no text),
warm natural daylight from a window at the side, very shallow depth of field,
professional stock-photography look.

Deliberately NOT the site's prior Zscaler hero (a diverse cybersecurity team
in a bright SOC facing a curved world-map telemetry wall), and critically NOT
a data-center long-hallway / server-aisle composition, no racks, no cable
runs, no neon, no HUD/overlay graphics.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  signage anywhere. Any screen content is heavily blurred and completely
  unreadable. No name tags or lanyards with writing.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-zs-agentic-soc-hero-20260914.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "zs-agentic-soc-security-agents-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no labels, no name tags, no "
    "lanyards with writing, no plaques, no nameplates, no decals, no "
    "stencils, no signage, no posters, no logos, no brand names, no "
    "watermark, no captions, no legible writing of any kind anywhere in the "
    "image. The monitors show only heavily blurred, soft, completely "
    "unreadable out-of-focus shapes with no recognizable user interface, no "
    "menus, no code and no distinguishable characters. No illustration, no "
    "digital art, no cartoon, no 3D render, no neon, no glowing lines, no "
    "synthwave, no geometric patterns, no HUD graphics, no overlay elements, "
    "no augmented-reality graphics, no data-center hallway, no server aisle, "
    "no server racks, no cable runs."
)

PROMPTS = {
    "1": (
        "Photo-realistic stock photograph, shot with a fast 85mm lens wide "
        "open, over-the-shoulder close-up of one single security analyst "
        "seated at a modern minimalist workstation, seen from just behind and "
        "slightly above the right shoulder so the back of the person's head "
        "and the top of one shoulder fill the near foreground soft and "
        "out-of-focus, the analyst turned toward two large plain monitors on "
        "the desk ahead, both monitors displaying only soft blurred "
        "unreadable dashboard shapes in muted cool blue and grey tones with "
        "no legible content whatsoever, warm golden window daylight falling "
        "in from the side across a plain desk surface with a simple plain "
        "unmarked coffee cup, a plain notebook with completely blank pages "
        "and a plain pen, one small potted green plant, a plain light-grey "
        "office wall and softly blurred unmarked background, warm and cool "
        "light mixing naturally, very shallow depth of field with the "
        "analyst's shoulder and the near desk edge soft and the monitors "
        "melting into smooth creamy bokeh, natural realistic skin and fabric "
        "textures, no readable information anywhere in frame, "
        "photorealistic, high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Candid documentary-style corporate stock photograph of a single "
        "concentrated security analyst at a modern desk, framed over the "
        "shoulder from behind, the analyst leaning slightly forward toward "
        "two wide monitors that glow softly with completely blurred, "
        "unreadable out-of-focus chart shapes and gentle colour gradients, "
        "no readable charts and no recognizable interface, warm afternoon "
        "sunlight streaming through a large window at the left casting soft "
        "warm highlights on the analyst's shoulder and the plain desk, "
        "background of a calm modern open-plan office dissolved into soft "
        "blur with no signage and no readable detail, minimal props: a plain "
        "unmarked white mug, a plain closed laptop off to the side, a small "
        "plant with soft green leaves, shallow depth of field isolating the "
        "near shoulder and monitor bezels while everything else falls into "
        "smooth bokeh, natural realistic textures and skin tones, muted "
        "colour palette, photorealistic, high detail, editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        with open(real_path) as f:
            raw = f.read().strip().split("\n")[0]
            key = raw.split("|", 1)[1] if "|" in raw else raw
            if key:
                os.environ["FAL_KEY"] = key
                return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with fal flux/schnell...")
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
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
