#!/usr/bin/env python3
"""Generate hero image for take-or-pay-contracts-ai-infrastructure-explainer-2026.

Story: a WEEKLY EXPLAINER on take-or-pay contracts — the contract structures
financing the AI buildout (capacity contracts, prepayments, backlog/RPO, who
bears the downside risk if AI demand disappoints). The article explains the
financing machinery behind AI data centers.

Visual angle: INSTITUTIONAL FINANCE, not infrastructure. A large institutional
finance setting — an empty modern trading floor at dawn before the open, a
glass-walled boardroom overlooking a financial district at dusk, or the marble
atrium of a large financial institution. Photo-realistic, shallow depth of
field, natural realistic light.

Must stay DISTINCT from recent heroes (coastal nuclear plant, containerized
data-center module on a crane, network processor chip macro, linemen on a
transmission tower, rooftop fiber rack, gold quantum processor, rocket on a
launch pad). Never a data-center hallway / server aisle / server room.

Text-free photo-realistic stock photography, 16:9 1920x1080 center-crop.

Usage: python3 gen-take-or-pay-hero-20260913.py [1|2|3|4]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "take-or-pay-contracts-ai-infrastructure-explainer-2026"

# Shared negative-style guard tail required on every prompt.
GUARD = (
    "No text, no letters, no numbers, no signage, no labels, no logos, no brand marks, "
    "no readable writing on any surface, no charts, no graphs, no documents with visible writing, "
    "no people, no illustration, no digital art, no neon, no glowing lines, no holograms, "
    "no abstract shapes, no geometric patterns, no server room, no data center hallway, "
    "no server racks, no server aisle."
)

PROMPTS = {
    # Variant 1 — empty modern trading floor at dawn before the open
    1: (
        "Professional stock photograph of a large empty modern institutional trading floor at dawn "
        "before the market opens: long rows of identical low-partition desks with dark flat monitors "
        "switched off and angled away from the camera, ergonomic chairs pushed in, several wide "
        "curved monitor arms and a few small telephone handsets and coffee cups at the workstations, "
        "the desks receding in a clean repeating perspective toward tall floor-to-ceiling glass "
        "windows that look out onto a cold blue financial-district skyline of office towers in the "
        "early morning haze, cool pale gray-blue dawn light flooding in from the windows and mixing "
        "with rows of soft recessed ceiling lights overhead, polished pale gray stone floor with "
        "faint reflections, a raised glass-walled management office at the far end, still and quiet, "
        "no one present, shallow depth of field with the foreground desk in sharp focus and the far "
        "windows softly blurred, wide cinematic architectural interior photography, natural realistic "
        "lighting, sharp detail, 4K, shot on a full-frame DSLR with a fast prime lens, photo-realistic. "
        + GUARD
    ),
    # Variant 2 — glass-walled corporate boardroom overlooking a financial district at dusk
    2: (
        "Professional stock photograph of an empty executive boardroom on a high floor of a "
        "corporate financial headquarters at dusk: a very long polished dark wood conference table "
        "running diagonally through the frame with neatly arranged black leather high-backed chairs "
        "on both sides, slim brushed-metal table legs, a row of dark glass water glasses and two "
        "closed leather folders on the tabletop, the room enclosed on one side by a glass wall and "
        "on the other by a full-height window wall looking out over a downtown financial district "
        "skyscrapers at blue hour with hundreds of small warm office lights scattered across the "
        "towers, deep blue and faint amber sky beyond, warm low interior ceiling light reflecting "
        "as long soft streaks along the polished table surface, dark gray carpet, calm and "
        "unoccupied, shallow depth of field focused on the near end of the table with the city "
        "softly defocused behind, wide cinematic architectural interior photography, natural "
        "realistic lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        + GUARD
    ),
    # Variant 3 — marble lobby / atrium of a large financial institution
    3: (
        "Professional stock photograph of the grand marble lobby atrium of a large old financial "
        "institution early in the morning before business hours: a vast double-height hall clad in "
        "pale cream and gray veined marble with a polished mirror-smooth stone floor, a row of "
        "tall fluted stone columns on the right, a long plain dark wooden reception counter with a "
        "low brass rail on the left and a small blank security turnstile barrier beside it, two "
        "deep leather armchairs and a low table off to one side, a wide stone staircase sweeping "
        "up in the background, warm early daylight falling in long soft shafts from high clerestory "
        "windows and pooling on the floor, dust motes in the air, completely empty and quiet with "
        "no one in the frame, shallow depth of field with the near marble column in sharp focus and "
        "the far staircase softly blurred, wide cinematic architectural interior photography, "
        "natural realistic lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        + GUARD
    ),
    # Variant 4 — nighttime exterior: institutional banking hall facade + financial district
    4: (
        "Professional stock photograph of the stone facade of a large classical institutional bank "
        "building in a financial district at night, shot from across an empty street: a massive "
        "solid limestone neoclassical frontage with tall columns and a heavy bronze door, a row of "
        "small warm uplights washing the stone from below, wet asphalt road and dark granite curb "
        "in the foreground with soft reflections of the warm uplights, a few black sedans parked "
        "along the curb with lights off, modern glass-and-steel office towers rising behind and "
        "around the old building with scattered lit windows, deep navy night sky with low city "
        "glow, cold and imposing and entirely empty of people, shallow depth of field with the "
        "foreground curb sharp and the towers above softly blurred, wide cinematic urban "
        "architecture photography, natural realistic lighting, sharp detail, 4K, shot on a "
        "full-frame DSLR, photo-realistic. "
        + GUARD
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
    print("Prompt: " + prompt[:200] + "...")
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


def process_and_save(data, attempt=None):
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
    process_and_save(data, attempt)
    print("DONE")


if __name__ == "__main__":
    main()
