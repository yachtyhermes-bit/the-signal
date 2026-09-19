#!/usr/bin/env python3
"""Generate hero for sentinelone-autonomous-defense-ai-agents-2026 (fal flux/schnell).

Subject: SentinelOne (NASDAQ: S) — the AI-native endpoint security company. The
article is about autonomous AI agents doing endpoint defence (and the week that
Google disclosed its Gemini model autonomously hacked three real companies during
a security test). The human-scale counterpart to that story is the fleet of
endpoints themselves.

Scene chosen: a corporate IT STAGING / PROVISIONING ROOM — dozens of identical
closed enterprise laptops sitting in neat rows on long wooden benches, lids shut,
chassis angled identically, one technician's hand (no face visible) reaching in
to lift a single laptop from the row. Soft neutral warehouse daylight from high
windows, very shallow depth of field, faint dust in the air, muted greys and
blacks with a subtle cool tone. Reads instantly as "the endpoints" — a physical,
human-scale scene about devices being protected.

Deliberately NOT a data-center hallway / server aisle / rack row, NOT a security
operations center with monitors, NOT a video wall with a world map, NOT a chip
fab cleanroom, NOT a bare silicon wafer (all recent heroes on this site), NOT
digital art, NOT neon / synthwave, NOT glowing lines, NOT geometric patterns,
NOT a 3D render, NOT an illustration, NOT a cartoon.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: no letters, numbers, logos, brand marks, stickers, labels, barcodes,
  asset tags, signage, screens, displays, UI, code, dashboards or watermarks.
  Every laptop is CLOSED so no screen is ever visible.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-sentinelone-agent-defense-hero-20260919.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "sentinelone-autonomous-defense-ai-agents-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering or imagery: no text, "
    "no letters, no words, no numbers, no serial numbers, no asset tags, no "
    "inventory labels, no sticky notes, no barcodes, no QR codes, no stickers, "
    "no brand marks, no manufacturer logos, no corporate names, no signage, no "
    "posters, no wall placards, no signage of any kind, no watermark, no "
    "captions. Every single laptop is completely CLOSED with its lid shut flat, "
    "so no screen, no display, no monitor and no glowing panel is visible "
    "anywhere, and the laptop bodies are perfectly plain, smooth and unmarked "
    "with no printed logos, no lettering and no decorative badges of any kind. "
    "There are no monitors, no television screens, no video walls and no "
    "computer interfaces anywhere in the room. Every surface — the benches, the "
    "walls, the floor and the laptop shells — is plain, smooth and unmarked. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no glowing edges, no geometric patterns, no futuristic "
    "HUD graphics, no holograms, no abstract shapes."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a corporate IT staging "
        "and provisioning room, dozens of identical brand-new closed enterprise "
        "laptops arranged in perfectly neat parallel rows on two long plain "
        "wooden benches, every lid shut flat and every chassis angled "
        "identically, matte dark grey and black aluminium shells, a single "
        "technician's bare hand and forearm reaching into the frame from the "
        "right to lift one laptop gently up out of the row, no face visible, "
        "the sleeve of a plain dark shirt, soft neutral daylight falling "
        "diffusely from tall high windows high on the left wall, faint dust "
        "motes suspended in the light beams, long wooden bench tops and a "
        "concrete floor, muted greys and blacks with a subtle cool neutral "
        "tone, very shallow depth of field so the lifted laptop and the "
        "nearest row of closed lids are tack sharp while the far rows and the "
        "warehouse walls dissolve into soft smooth bokeh, natural realistic "
        "materials and textures, honest unposed documentary lighting, "
        "photorealistic, high detail, professional editorial photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic documentary photograph, shot on an 85mm lens at a "
        "shallow aperture, inside a corporate IT asset staging and "
        "provisioning room where several dozen identical unopened enterprise "
        "laptops sit in meticulous evenly spaced rows across wide bare wooden "
        "bench tops, all lids closed flat and all bodies squared the same way, "
        "plain matte dark grey and black machines with perfectly smooth "
        "unmarked shells, one technician's hand entering the frame from the "
        "lower right to pick a single laptop up off the bench, only the hand "
        "and forearm visible, plain neutral clothing, no face in frame, soft "
        "overcast daylight diffusing through tall industrial windows and "
        "washing evenly across the room, fine dust drifting in the air, muted "
        "grey black and warm-wood palette with a faint cool cast, extremely "
        "shallow depth of field so the hand and the laptop being lifted are "
        "crisply sharp while the ranks of closed laptops behind fall away "
        "into creamy smooth bokeh, natural realistic textures on metal "
        "plastic and wood, quiet human-scale warehouse atmosphere, "
        "photorealistic, high detail, professional editorial press "
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
