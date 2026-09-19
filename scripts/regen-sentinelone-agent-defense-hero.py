#!/usr/bin/env python3
"""Regenerate the SentinelOne hero (fal flux/schnell) — logo-free pass.

Attempt 1 produced a clean photo but a vision check spotted a small circular
logo-like emblem on the laptop lids. This pass hard-bans ANY mark, badge,
emblem, symbol or motif on the laptop surfaces, and adds a plain unbranded
surface instruction.
"""

import os
import sys

import requests
from PIL import Image
from fal_client import subscribe as fal_subscribe

SLUG = "sentinelone-autonomous-defense-ai-agents-2026"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

PROMPT = (
    "Photo-realistic editorial stock photograph of a corporate IT staging and "
    "provisioning room, dozens of identical brand-new closed enterprise laptops "
    "arranged in perfectly neat parallel rows on two long plain wooden benches, "
    "every lid shut flat and every chassis angled identically, matte dark grey "
    "and black aluminium shells, a single technician's bare hand and forearm "
    "reaching into the frame from the right to lift one laptop gently up out of "
    "the row, no face visible, the sleeve of a plain dark shirt, soft neutral "
    "daylight falling diffusely from tall high windows on the left wall, faint "
    "dust motes suspended in the light beams, long plain wooden bench tops and a "
    "bare concrete floor, muted greys and blacks with a subtle cool neutral "
    "tone, very shallow depth of field so the lifted laptop and the nearest row "
    "of closed lids are tack sharp while the far rows and the warehouse walls "
    "dissolve into soft smooth bokeh, natural realistic materials and textures, "
    "honest unposed documentary lighting, photorealistic, high detail, "
    "professional editorial photography, 16:9 landscape composition. "
    "ABSOLUTELY CRITICAL: every laptop surface is completely blank, smooth, "
    "plain and unmarked, an utterly featureless matte lid and chassis with "
    "NOTHING on it: no logo, no emblem, no badge, no insignia, no crest, no "
    "circular mark, no symbol, no monogram, no decal, no sticker, no pattern, "
    "no decorative motif, no printed element of any kind anywhere on any laptop "
    "in the room. The scene contains no lettering or imagery whatsoever: no "
    "text, no letters, no words, no numbers, no serial numbers, no asset tags, "
    "no inventory labels, no barcodes, no QR codes, no brand marks, no "
    "manufacturer logos, no corporate names, no signage, no posters, no wall "
    "placards, no watermarks, no captions, no icons. Every single laptop is "
    "completely CLOSED with its lid shut flat, so no screen, no display, no "
    "monitor and no glowing panel is visible anywhere; there are no monitors, "
    "no television screens, no video walls and no computer interfaces in the "
    "room. No illustration, no digital art, no cartoon, no 3D render, no CGI, "
    "no neon, no glowing lines, no glowing edges, no geometric patterns, no "
    "futuristic HUD graphics, no holograms, no abstract shapes."
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
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with fal flux/schnell (logo-free pass)...")
    result = fal_subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("output"):
        image_url = result["output"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url in result: {result}")
        sys.exit(1)
    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded {out_path} bytes={len(r.content)}")
    return Image.open(out_path)


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
    img = generate(PROMPT, OUTPUT)
    img = crop_to_16x9(img.convert("RGB"))
    img.save(OUTPUT, "JPEG", quality=94, optimize=True)
    img.save(BACKUP, "JPEG", quality=94, optimize=True)
    print(f"Saved {OUTPUT} dims={img.size} bytes={os.path.getsize(OUTPUT)}")
    print(f"Saved {BACKUP} bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
