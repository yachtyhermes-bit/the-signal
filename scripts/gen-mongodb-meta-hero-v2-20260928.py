#!/usr/bin/env python3
"""Regenerate the MongoDB / Meta hero WITHOUT any human hand or body part.

v1 (generate-mongodb-meta-hero.py) asked flux for "a single human hand reaches in
from the right edge and pulls one drawer slightly open" - which violates the house
rule (no hands, no body parts in heroes) and read as random creepy fingers.

v2 keeps the metaphor - a vast card-catalog archive hall standing in for the record
layer an application reads from - but the open drawer is lit and open on its own.
No people, no hands, no fingers, no arms anywhere in frame.
"""
import os
import sys
import requests
from PIL import Image

OUTPUT = "/home/chino/thesignal/public/img/articles/mongodb-meta-ceo-enterprise-ai-platform-2026.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

PROMPT = (
    "Ultra-realistic professional stock photograph of a vast historic archive hall "
    "filled with tall wooden cabinets of small index-card catalog drawers, thousands "
    "of identical drawers receding into soft focus in the distance, warm ambient "
    "window light mixed with gentle overhead lamps, honey-colored aged oak, clean and "
    "beautifully lit. In the near foreground on the left, one single drawer stands "
    "open on its own, glowing softly warm from a hidden lamp inside it, its interior "
    "too dark to read, shallow depth of field, the open drawer tack sharp and the deep "
    "rows of cabinets dissolving into creamy bokeh, no people anywhere, cinematic "
    "corporate editorial photography, 85mm lens look, high detail, natural warm color "
    "palette, clean uncluttered space on the right side of the frame. "
    "STRICTLY no people, no humans, no hands, no fingers, no arms, no body parts, "
    "no mannequins, no statues of people, no text, no letters, no numbers, no logos, "
    "no brand names, no labels, no signage, no watermark, no screens, no visible faces, "
    "no glowing lines, no neon, no holograms."
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


def generate(prompt, out_path, seed):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print(f"Generating (flux/schnell, seed={seed})...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "seed": seed,
            "enable_safety_checker": False,
        },
    )
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("output"):
        image_url = result["output"]
    if not image_url:
        print(f"ERROR: no image url in result: {str(result)[:300]}")
        sys.exit(1)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"  raw: {img.size}, {len(r.content)} bytes")
    return img


def crop_to_16x9(img):
    w, h = img.size
    target = FINAL_W / FINAL_H
    cur = w / h
    if cur > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur < target:
        new_h = int(w / target)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 4207
    stage = "/tmp/mongodb-hero-raw.jpg"
    img = generate(PROMPT, stage, seed).convert("RGB")
    for path in (OUTPUT,
                 "/home/chino/thesignal/_backup_dist/img/articles/mongodb-meta-ceo-enterprise-ai-platform-2026.jpg"):
        out = crop_to_16x9(img)
        out.save(path, "JPEG", quality=92, optimize=True)
        print(f"  wrote {path}  {out.size}  {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
