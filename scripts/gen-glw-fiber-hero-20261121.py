#!/usr/bin/env python3
"""Generate hero for glw-fiber-round-trip-2026 (fal flux/schnell).

Subject: Corning Incorporated (GLW) optical fiber — fiber demand from AI data
centers, but the stock has unwound ~63% from its June 2026 peak.

Scene: a spool / pancake coil of bare optical fiber strands catching light on a
manufacturing floor. NOT a data center, NOT server racks, NOT a hallway.

Rules: photo-realistic editorial photograph only. No text/letters/numbers/logos,
no neon, no glowing geometric lines, no CGI/illustration look.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-glw-fiber-hero-20261121.py
"""
import os
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "glw-fiber-round-trip-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no labels, no signage, no readable "
    "words, no letters, no numbers, no stencils, no markings, no captions, no barcode, no brand "
    "names, no logos, no watermarks, no printed tags. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game look, no neon, no glowing lines, no fiber-optic "
    "light-trail graphics, no HUD overlays, no geometric patterns."
)

PROMPTS = {
    # (a) spool / pancake coil of bare fiber on a factory floor
    "1": (
        "Professional stock photograph of a large spool wound with thousands of turns of bare "
        "optical fiber, sitting on the concrete floor of a clean manufacturing plant. The "
        "unspooled end of the fiber lifts away from the coil and sweeps across the frame, a "
        "single hair-thin glass strand catching a cool blue-white highlight so it glints like a "
        "fine wire of light. The wound coil shows the dense, faintly iridescent sheen of real "
        "silica glass fiber, pale amber and cool silver where the light grazes the turns. Behind "
        "it, blurred rows of industrial machinery and a matte grey wall fall out of focus. Shot "
        "on a full-frame camera with an 85mm lens at f/2.0, shallow depth of field, cool "
        "blue-white factory lighting with soft falloff, honest dust-free industrial textures, "
        "fine film grain, subtle vignette, no digital polish. Photorealistic, extremely high "
        "detail, professional editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # (b) extreme macro of a bundle of bare glass fiber strands
    "2": (
        "Extreme close-up macro photograph of a bundle of bare optical fiber strands held in a "
        "coil on a factory workbench, dozens of hair-thin clear silica glass cylinders fanned out "
        "and running diagonally across the frame. Each strand is a plain transparent rod: a thin "
        "specular highlight runs along one edge where the ceiling lights reflect off the glass, "
        "and the opposite side falls into plain shadow, with a soft neutral grey backdrop visible "
        "through them. Real polished glass with small honest imperfections, faint dust, and a few "
        "where the strands cross over each other. Only the two nearest strands are in focus; the "
        "rest blur gently out of focus. Shot on a real camera with a 100mm macro lens at f/4, very "
        "shallow depth of field, flat cool-white workshop lighting, no colored gels, no dark "
        "dramatic mood. Fine film grain, subtle vignette, natural color, honest glass texture, "
        "no digital polish, no bloom, no light streaks, no lens flare, no glowing edges. "
        "Photorealistic, extremely high detail, professional editorial photography, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    # (c) fiber draw tower / preform being drawn
    "3": (
        "Photo-realistic documentary photograph inside an optical fiber manufacturing plant, shot "
        "at the bottom of a draw furnace: a thick cylindrical glass preform has been heated until "
        "it necks down into one single hair-thin strand of fiber. The preform stub glows a soft "
        "dull orange only at its narrow melt tip near the top of the frame, and below it the "
        "single strand hangs dead straight in a long fine line, passing a small steel measuring "
        "head and winding onto a grey take-up spool at the bottom. Surrounding the run is real "
        "industrial hardware: a dark steel frame, aluminium guide rollers, black cable runs, "
        "bolted brackets, a scuffed grey painted machine base. Ambient light is cool and dim, "
        "warm only right at the melt tip; light dust haze hangs in the air. Shot on a real camera "
        "with a 35mm lens at f/2.8, shallow depth of field so the far machinery softens, uneven "
        "lamp-lit industrial exposure, mild sensor noise, fine film grain, subtle vignette, worn "
        "metal and honest grime, no symmetry, no CGI sheen, no bloom, no lens flare, no light "
        "streaks, no glowing cable, no luminous lines. Photorealistic, extremely high detail, "
        "professional editorial photography, 16:9 landscape composition. " + NO_TEXT
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
print("PROMPT:", PROMPTS[ATTEMPT])
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

tmp = f"/tmp/glw-fiber-hero-raw-{ATTEMPT}.jpg"
with open(tmp, "wb") as f:
    f.write(r.content)

img = Image.open(tmp).convert("RGB")
w, h = img.size
target = FINAL_W / FINAL_H
if w / h > target:
    nw = int(h * target)
    img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
else:
    nh = int(w / target)
    img = img.crop((0, (h - nh) // 2, w, (h + nh) // 2))
img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)

# keep under 500KB
quality = 92
img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
while os.path.getsize(OUTPUT) > 500 * 1024 and quality > 70:
    quality -= 4
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)

print("Saved:", OUTPUT, img.size, os.path.getsize(OUTPUT), "bytes", "q=", quality)

os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
img.save(BACKUP, "JPEG", quality=quality, optimize=True)
print("Backup:", BACKUP, os.path.getsize(BACKUP), "bytes")
