#!/usr/bin/env python3
"""Hero image for nbis-microsoft-neocloud-cull-delivery-2026.

Story: Nebius (NBIS) — a 'neocloud' renting out AI GPU data-center capacity,
flagship site in Finland. Angle: Microsoft consolidating its neocloud suppliers.

Required scene: EXTERIOR winter Nordic data-center campus — low white/grey
industrial buildings with rooftop cooling units, snow on the ground,
high-voltage pylons and power lines in the foreground/mid-ground, overcast
northern light, light snowfall. Photo-real documentary, wide establishing shot.

Banned: server aisle / hallway / rack close-ups, abstract or digital art,
neon, glowing lines, geometric patterns, text/signage/logos, faces.

Usage: /home/chino/video-venv/bin/python3 gen-nbis-neocloud-hero.py [1|2|3]
"""
import io
import os
import sys

import requests
from PIL import Image

SLUG = "nbis-microsoft-neocloud-cull-delivery-2026"

TARGET_W, TARGET_H = 1536, 1024
OUT_DIR = "/home/chino/thesignal/public/img/articles"
BACKUP_DIR = "/home/chino/thesignal/_backup_dist/img/articles"

GUARD = (
    "No text, no letters, no numbers, no signage, no labels, no logos, no brand marks, "
    "no screens, no monitors, no displays, no UI, no people, no faces, no illustration, "
    "no digital art, no CGI look, no neon, no glowing lines, no holograms, no abstract shapes, "
    "no geometric patterns, no server room, no data-center hallway, no server aisle, "
    "no racks of servers, no cable trays indoors."
)

PROMPTS = {
    # 1 — wide establishing shot, pylons in foreground, light snowfall
    1: (
        "Photo-realistic documentary photograph, wide establishing shot of a large Nordic "
        "data-center campus in deep winter. Three long low industrial buildings clad in pale "
        "grey and white metal panels with flat roofs, rows of grey rooftop air-handling and "
        "cooling units, a few narrow windows, sitting on a flat snow-covered plain. Thick even "
        "snow covers the ground and the access road, ploughed snowbanks along the verge. In the "
        "foreground a line of tall steel lattice high-voltage transmission pylons with heavy "
        "cables sagging between them marches diagonally across the frame toward the buildings. "
        "Overcast flat northern winter light, pale grey-white sky, light snowfall drifting "
        "through the air, cold blue-grey colour palette, faint snow haze softening the distant "
        "treeline of dark spruce forest. Shot on a full-frame DSLR at 50mm, f/4, shallow depth "
        "of field with the nearest pylon slightly soft and the buildings sharp. Natural "
        "realistic lighting, crisp fine detail, editorial news photography. " + GUARD
    ),
    # 2 — elevated view over snowy campus, pylons mid-ground, snowfall
    2: (
        "Photo-realistic documentary photograph taken from a slight rise overlooking a Nordic "
        "AI data-center campus in winter. Low wide white and light-grey industrial halls with "
        "banks of grey rooftop cooling units and ventilation stacks stretch across a snow-"
        "covered site, service road cleared of snow running between them, chain-link perimeter "
        "fence with a plain gate and no markings, a small electrical substation with grey "
        "transformers and busbars beside the buildings. Two tall steel lattice transmission "
        "pylons rise from the snow in the middle ground with power lines strung across the "
        "frame overhead. Flat overcast northern light, uniform pale grey sky, fine light "
        "snowfall, snow drifts against the building walls, sparse dark spruce forest on the "
        "horizon. Long lens compression, shallow depth of field, muted cold colours, authentic "
        "editorial press photograph, sharp detail, 4K. " + GUARD
    ),
    # 3 — ground level, buildings behind pylons, heavier snow clouds
    3: (
        "Photo-realistic documentary photograph of a Nordic data-center campus under a heavy "
        "overcast winter sky, shot at ground level from an empty snow-covered field. A very "
        "large low white industrial building with a flat roof and a dense array of grey rooftop "
        "cooling units sits in the middle distance, a second lower grey building behind it, "
        "bare snow-covered ground in the foreground with faint tyre tracks and scattered dry "
        "grass stems poking through the snow. Tall steel lattice high-voltage pylons stand in "
        "the foreground field with thick cables curving overhead across the top of the frame, "
        "a small grey transformer kiosk at their base. Diffuse flat grey-white light, no "
        "shadows, light snow falling, cold desaturated blue-grey tones, dark treeline far "
        "behind the buildings. Wide establishing shot, 35mm, shutter-speed still, natural "
        "realistic lighting, editorial photojournalism, sharp fine detail. " + GUARD
    ),
}


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

    print("Prompt: " + prompt[:240] + "...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": 1344, "height": 896},
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
        raise RuntimeError("No image URL in result: " + str(list(result.keys())))
    print("Image URL: " + str(image_url))
    r = requests.get(image_url, timeout=180)
    r.raise_for_status()
    return r.content


def process_and_save(data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print("Raw dimensions: %dx%d" % (w, h))
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
    quality = 88
    img.save(out_path, "JPEG", quality=quality, optimize=True)
    # keep under 400KB
    while os.path.getsize(out_path) > 400 * 1024 and quality > 60:
        quality -= 4
        img.save(out_path, "JPEG", quality=quality, optimize=True)
    size_kb = os.path.getsize(out_path) / 1024.0
    print("Saved %s (%dx%d, %.1f KB, q=%d)" % (out_path, img.size[0], img.size[1], size_kb, quality))

    bak = os.path.join(BACKUP_DIR, SLUG + ".jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=quality, optimize=True)
    print("Mirrored to " + bak)
    return out_path


def main():
    attempt = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if attempt not in PROMPTS:
        print("attempt must be 1, 2 or 3")
        sys.exit(2)
    load_fal_key()
    print("=== [%s] attempt %d ===" % (SLUG, attempt))
    data = generate(PROMPTS[attempt])
    process_and_save(data)
    print("DONE")


if __name__ == "__main__":
    main()
