#!/usr/bin/env python3
"""Generate hero for rtx-navy-sewip-electronic-warfare-2026 (fal flux/schnell).

Subject: RTX / Raytheon shipboard electronic warfare for the US Navy — the SEWIP
program and the AN/SLQ-32 family of shipboard electronic attack / electronic
support systems fitted to surface combatants.

Scene: an Arleigh Burke-class guided-missile destroyer at sea, octagonal
AN/SPY-1 phased-array panels and EW radomes on the superstructure, grey
overcast North Atlantic light. Alternate: tight shot of radar/EW arrays and
dome antennas against a flat sea horizon.

Rules: photo-realistic editorial photograph only. No data centre, no server
room, no neon/glowing lines/geometric art, no CGI sheen, no text/lettering
anywhere (including hull numbers, flags with lettering, insignia).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-rtx-navy-sewip-hero-20261120.py
"""
import os
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "rtx-navy-sewip-electronic-warfare-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no hull numbers, no readable words, "
    "no letters, no numbers, no glyphs, no stencils, no markings, no captions, no labels, no "
    "signage, no logos, no brand names, no watermarks, no insignia, no flags bearing lettering. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no video-game look, no "
    "neon, no glowing lines, no HUD graphics, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a United States Navy Arleigh Burke-class guided-missile "
        "destroyer at sea, its distinctive octagonal AN/SPY-1 phased-array radar panels set flat "
        "into the grey steel superstructure and several electronic-warfare radomes and dome "
        "antennas mounted on the mast and deckhouse, the ship cutting through choppy grey North "
        "Atlantic water with a light bow spray. Shot on a full-frame camera with a long lens from "
        "another vessel, shallow depth of field, grey-blue overcast light, low flat cloud, sea haze "
        "softening the far horizon, weathered haze-grey paint with salt streaking, honest metal and "
        "water textures, natural sensor noise and very slight film grain, subtle vignette, no CGI "
        "sheen, no perfect symmetry. Photorealistic, extremely high detail, professional editorial "
        "lighting, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic documentary photograph, shot on a real camera with a 50mm lens at f/4, of "
        "the upper superstructure of a modern United States Navy surface warship at sea, seen from "
        "a low angle on deck: the flat octagonal face of a large grey phased-array radar panel "
        "fills one side of the frame, surrounded by smaller electronic-warfare dome antennas and "
        "rectangular array tiles bolted to the painted steel deckhouse, with thin whip antennas and "
        "a lattice mast rising against a flat, featureless overcast sky and a hazy grey sea horizon "
        "at the bottom of frame. Dull grey-blue overcast daylight, soft even illumination, salt "
        "staining and honest paint wear on the steel, real lens blur on the near antenna, mild "
        "sensor noise, film grain, subtle vignette, authentic maritime textures, no CGI polish. "
        "Photorealistic, high detail, editorial photojournalism, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Editorial stock photograph of an Arleigh Burke-class destroyer steaming in open ocean "
        "under heavy grey overcast, a three-quarter bow view so the angled superstructure and the "
        "octagonal phased-array panels are clearly visible, electronic-warfare radomes clustered "
        "on the mast above the bridge, white bow wave and dark choppy swell, distant rain squall "
        "blurring the horizon. Real camera, 85mm lens, compressed perspective, natural flat "
        "diffused daylight, weathered grey paint, wet steel highlights, honest water spray, mild "
        "grain, slight atmospheric haze, no CGI sheen. Photorealistic, high detail, professional "
        "editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
}

args = {
    "prompt": PROMPTS[ATTEMPT],
    "image_size": "landscape_16_9",
    "num_inference_steps": 4,
    "num_images": 1,
    "enable_safety_checker": True,
}

import fal_client  # noqa: E402

print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)

image_url = None
if isinstance(result, dict):
    imgs = result.get("images") or []
    if imgs:
        image_url = imgs[0].get("url")
if not image_url:
    raise SystemExit(f"ERROR: no image URL in result: {str(result)[:300]}")

print("Image URL:", image_url)
r = requests.get(image_url, timeout=180)
r.raise_for_status()

tmp = f"/tmp/rtx-sewip-hero-raw-{ATTEMPT}.jpg"
with open(tmp, "wb") as f:
    f.write(r.content)

img = Image.open(tmp).convert("RGB")
# center-crop to 16:9 then resize to 1920x1080
w, h = img.size
target = FINAL_W / FINAL_H
if w / h > target:
    nw = int(h * target)
    img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
else:
    nh = int(w / target)
    img = img.crop((0, (h - nh) // 2, w, (h + nh) // 2))
img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
img.save(OUTPUT, "JPEG", quality=92, optimize=True)
print("Saved:", OUTPUT, img.size, os.path.getsize(OUTPUT), "bytes")

os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
img.save(BACKUP, "JPEG", quality=92, optimize=True)
print("Backup:", BACKUP, os.path.getsize(BACKUP), "bytes")
