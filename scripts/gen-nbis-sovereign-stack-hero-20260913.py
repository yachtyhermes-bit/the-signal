#!/usr/bin/env python3
"""Generate hero image for nbis-palantir-sovereign-ai-stack-2026.

Scene: modular containerized data-center modules (shipping-container-scale
units) being lifted by a construction crane onto concrete pads at an
industrial site, steel frames, cable trays, gravel and site fencing, with
high-voltage transmission pylons far on the horizon.

Distinctive point: the crane + modular modules construction site — NOT a
data center server aisle / long hallway.

Text-free photo-realistic stock photography, 16:9 1920x1080 center-crop.

Usage: python3 gen-nbis-sovereign-stack-hero-20260913.py [1|2|3]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "nbis-palantir-sovereign-ai-stack-2026"

PROMPTS = {
    # Variant 1 — dusk, low wide-angle from across the gravel pad, crane mid-lift
    1: (
        "Professional stock photograph of a modular data center construction site at dusk: "
        "large white shipping-container-scale modular compute modules with ribbed steel skins "
        "and closed service doors, one module suspended mid-air from the hook and cables of a "
        "tall yellow construction crane lifting it toward a row of concrete foundation pads, "
        "bundles of black power and fiber cable trays laid across the gravel yard, galvanized "
        "steel frames and open floor beams on the pads awaiting the next module, chain-link site "
        "fencing and a few bare utility poles at the edges, deep orange and purple dusk sky "
        "overhead, tall steel lattice high-voltage transmission pylons small on the far horizon "
        "behind the site, cool blue shadows on the ground, warm sodium work lights beginning to "
        "glow, no people visible, cinematic wide-angle industrial photography, natural realistic "
        "lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
        "no digital art, no neon, no glowing lines, no holograms, no abstract shapes, "
        "no geometric patterns, no server room, no data center hallway, no server racks indoors."
    ),
    # Variant 2 — blue hour, elevated three-quarter view of the whole pad
    2: (
        "Professional stock photograph taken from an elevated three-quarter angle of a "
        "modular data center under construction during blue hour: rows of container-sized "
        "modular compute units in pale gray and white, one unit hanging from the lifting "
        "cables of a lattice-boom construction crane as it is lowered onto a concrete pad, "
        "several concrete pads already occupied by seated modules with exposed steel skids "
        "and cable entry points, long parallel cable trays and conduit runs in trenches across "
        "the compacted gravel and crushed stone yard, steel structural framing stacked beside "
        "the pads, orange mesh construction fencing along the perimeter, faint warm work-light "
        "glow on the module surfaces against a deep blue twilight sky, distant high-voltage "
        "lattice transmission pylons tiny along the far horizon, crisp cold shadows, wide "
        "cinematic industrial landscape photography, natural realistic lighting, sharp detail, "
        "4K, shot on a full-frame DSLR, photo-realistic. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
        "no digital art, no neon, no glowing lines, no holograms, no abstract shapes, "
        "no geometric patterns, no server room, no data center hallway, no server racks indoors."
    ),
    # Variant 3 — overcast daylight, tight ground-level view along the module row
    3: (
        "Professional stock photograph of a modular data center construction site under an "
        "overcast flat daylight sky: a ground-level view along the side of long container-shaped "
        "modular compute units resting on concrete plinths, their ribbed pale metal cladding "
        "weathered with a few scuffs and louvered cooling panels but no markings, a mobile "
        "construction crane on the right with its boom raised over a module it is about to set "
        "down, heavy lifting slings and shackles hanging from the hook block, coiled steel "
        "cables and stacked cable trays on the wet gravel in the foreground, steel support "
        "beams and a stack of galvanized frames beside the pads, muddy tire tracks, temporary "
        "site fencing in the middle distance, tall steel lattice high-voltage transmission "
        "pylons faint and small far away on the flat horizon, muted gray and green tones, soft "
        "diffused light with no harsh shadows, documentary industrial photography, sharp detail, "
        "4K, shot on a full-frame DSLR, photo-realistic. "
        "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
        "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
        "no digital art, no neon, no glowing lines, no holograms, no abstract shapes, "
        "no geometric patterns, no server room, no data center hallway, no server racks indoors."
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
