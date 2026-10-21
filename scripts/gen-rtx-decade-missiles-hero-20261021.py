#!/usr/bin/env python3
"""Generate hero for a-decade-of-missiles-rtx (fal flux/schnell).

Subject: RTX / Raytheon missile production ramp — Tomahawk, AMRAAM, SM-6 backlog.
Scene: a vast missile assembly hall, rows of finished grey cruise missiles on
transport cradles running deep into the frame. Production-at-scale is the thesis.

Rules: photo-realistic editorial photograph only, no text/logos/labels anywhere,
no people or hands, no CGI/neon/HUD look, no fake screens.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-rtx-decade-missiles-hero-20261021.py
"""
import os
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "a-decade-of-missiles-rtx")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, no "
    "numbers, no glyphs, no stencils, no markings, no captions, no labels, no signage, no logos, "
    "no brand names, no watermarks, no insignia, no flags. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game look, no neon, no glowing lines, no HUD graphics."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, shot on a full-frame camera with a 35mm lens at "
        "f/2.2, not a render and not CGI: inside a vast, dimly lit missile assembly hall at an "
        "aerospace plant. In the sharp foreground and stretching away into the distance are long rows "
        "of finished grey cruise missiles resting on wheeled steel transport cradles, their pointed "
        "noses and tail fins catching the light, arranged in neat lines that converge toward the far "
        "end of the hall. Heavy steel roof trusses and overhead gantry cranes span the ceiling; "
        "industrial lamps cast warm pools of light down the aisles, leaving the far corners in soft "
        "shadow and faint atmospheric haze. Polished concrete floor with painted guide lines, "
        "scattered tool carts and empty assembly fixtures, no people anywhere. Real lens blur down the "
        "aisles, natural sensor noise, very slight film grain, subtle vignette, honest textures on "
        "painted metal and concrete, no CGI sheen, no perfect symmetry. Photorealistic, extremely high "
        "detail, authentic editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "Documentary editorial photograph taken on a real camera, 50mm lens at f/2.8, not computer "
        "generated: a wide view down the centre aisle of a missile final-assembly building. To both "
        "sides, ranks of completed grey air-to-air and cruise missiles sit in individual metal "
        "cradles on rails, receding into the depth of the hall. Overhead, a lattice of steel girders, "
        "ducting and crane rails fills the upper frame, lit by cold daylight from high clerestory "
        "windows mixed with warm sodium work lamps. The floor is sealed grey concrete, clean and "
        "reflective at the highlights. No workers, no hands, no people in frame. Shallow depth of "
        "field with the nearest missiles tack sharp and the far end of the hall melting into soft "
        "haze; real optical blur, mild sensor noise, film grain, subtle vignette, authentic industrial "
        "textures, no CGI polish. Photorealistic, high detail, editorial photojournalism, 16:9 "
        "landscape composition. " + NO_TEXT
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

tmp = "/tmp/rtx-hero-raw.jpg"
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
print("Backup:", BACKUP)
