#!/usr/bin/env python3
"""Generate hero for sndk-dram-scare-nand-mispricing-2026 (fal flux/schnell).

Subject: SanDisk (SNDK) and the NAND flash market — the DRAM scare that dragged
the whole memory complex down, and the question of whether NAND pricing is
mispriced relative to DRAM. SanDisk's franchise is removable flash: SD and
microSD cards, USB drives, embedded storage.

Scene: photo-realistic editorial still life of a photographer's desk — blank
SD cards fanned in the foreground, a card reader, a mirrorless camera body
softly out of focus behind them, late-afternoon window light.

Deliberately DISTINCT from recent heroes: no data-center hallway, no server
aisle, no silicon die/chip macro, no boardroom, no abstract globe/network
graphic, no hands-on-laptop stock cliche as the primary subject.

Rules: PHOTO-REALISTIC stock photograph only; no digital art / neon / glowing
lines / geometric patterns / text / logos. Generate 1440x810, finalize
1600x900 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-sndk-nand-hero-20261019.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "sndk-dram-scare-nand-mispricing-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no labels, no serial numbers, no "
    "capacity markings, no logos, no brand marks, no trademarks, no icons, "
    "no watermark, no signature. Every memory card in the frame is completely "
    "blank and unmarked — smooth featureless plastic with no printing of any "
    "kind, no barcodes, no stickers. No packaging, no retail blister packs, "
    "no printed paper, no manuals, no box art, no signage anywhere. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no holographic or futuristic HUD graphics, no overlay graphics, no "
    "augmented-reality elements, no server rack, no server aisle, no "
    "data-center hallway, no circuit-board macro, no abstract background."
)

PROMPTS = {
    "1": (
        "A photo-realistic editorial still-life photograph for a business "
        "magazine, shot on a macro lens at f/2.8 with available window light "
        "only, on 35mm film, professional product photojournalism. A worn "
        "walnut photographer's desk in late-afternoon light. In the "
        "foreground, three blank matte-black SD memory cards lie fanned out "
        "on the wood, one propped on its long edge, their smooth unmarked "
        "plastic faces catching a soft raking highlight along the chamfered "
        "edges. Behind them sits a small brushed-aluminium card reader with a "
        "short braided cable curling away, and behind that the soft dark "
        "shoulder of a mirrorless camera body with a metal lens mount, well "
        "out of focus. A few specks of dust and one faint fingerprint on the "
        "nearest card. Warm amber sunlight comes through a window from the "
        "left, laying a hard-edged parallelogram of light across the desk and "
        "leaving cool blue-grey shadow in the rest of the frame; fine wood "
        "grain and small scratches are visible where the light falls. Very "
        "shallow depth of field: the front card and the wood immediately "
        "around it are tack sharp with honest micro-texture, while the reader "
        "and the camera dissolve into creamy bokeh. Real optical blur, "
        "visible fine film grain, subtle vignette, slight chromatic fringing "
        "at the frame edge, honest exposure with true blacks and warm "
        "highlights, relaxed slightly off-centre composition. Photorealistic, "
        "very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched candid photograph taken at a cluttered "
        "repair-bench with a 50mm lens at f/1.8, available light only — "
        "visibly a real camera photograph, not a render. A pair of adult "
        "hands, sleeves rolled to the forearm, hold a blank black microSD "
        "card between thumb and forefinger, sliding it into the slot of a "
        "small metal USB card reader that rests on a scratched steel bench. "
        "A soft warm task lamp from the upper right lights the knuckles and "
        "the card's edge, while cool daylight from a window on the left fills "
        "the shadows with blue. Around the hands the bench is out of focus: a "
        "scattered row of blank SD cards lying flat, the coiled black cable "
        "of the reader, a small screwdriver, and the blurred edge of an open "
        "laptop at the top of the frame. Shallow depth of field — the "
        "fingertips, the card and the reader slot are tack sharp with honest "
        "skin texture, visible pores, fine fabric fibres on the cuff and a "
        "little dust in the metal seams; everything else melts into smooth "
        "bokeh. Real optical blur, visible film grain, faint halation around "
        "the lamp, subtle vignette, honest exposure, candid off-centre "
        "composition. Photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A photo-realistic editorial still-life photograph for a business "
        "magazine, shot on an 85mm lens at f/2. On a dark grey felt mat on a "
        "plain desk, a neat row of five blank matte-black SD cards stands on "
        "their long edges like dominoes, angled slightly away from camera, "
        "with a sixth card lying flat in front of the row. A small "
        "aluminium-bodied card reader lies on its side to the right, its "
        "empty slot facing the lens. Behind the row, the desk falls away into "
        "shadow, with the corner of a black camera strap just visible at the "
        "top right. Cool overcast daylight from a large window on the left "
        "wraps the cards in soft grey light with a thin bright rim along each "
        "top edge, and a faint warm reflection from a wooden floor bounces "
        "into the lower faces. Very shallow depth of field: the third and "
        "fourth cards and the felt texture beneath them are tack sharp with "
        "honest dust and fine moulding seams, while the first card, the "
        "reader and the background go softly out of focus. Real optical blur, "
        "natural fine grain, subtle vignette, honest neutral exposure, "
        "restrained editorial composition with generous negative space on the "
        "right. Photorealistic, very high detail, 16:9 landscape composition. "
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get("STEPS", "28" if "dev" in model or "pro" in model else "4"))
    print("Generating image with " + model + " (steps=" + str(steps) + ")...")
    result = fal_client.subscribe(
        model,
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": steps,
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
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size) + "  bytes=" + str(len(r.content)))
    return img


def crop_to_16x9(img):
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def photo_finish(img, seed=23, grain=6.0, softness=0.9):
    """Borrowed from scripts/hero-photo-finish.py — adds the artefacts a real
    available-light frame carries so the file behaves like a photograph."""
    import numpy as np
    from PIL import ImageFilter

    rng = np.random.default_rng(seed)
    img = img.convert("RGB").filter(ImageFilter.GaussianBlur(softness))
    arr = np.asarray(img).astype(np.float32)

    r = np.roll(arr[:, :, 0], 1, axis=1)
    b = np.roll(arr[:, :, 2], -1, axis=1)
    arr[:, :, 0] = arr[:, :, 0] * 0.7 + r * 0.3
    arr[:, :, 2] = arr[:, :, 2] * 0.7 + b * 0.3

    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2.0, h / 2.0
    dist = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    vig = 1.0 - 0.22 * np.clip(dist / 1.42, 0, 1) ** 2
    arr *= vig[:, :, None]

    lum = rng.normal(0.0, grain, (h, w, 1))
    chroma = rng.normal(0.0, grain * 0.45, (h, w, 3))
    arr += lum + chroma

    arr[:, :, 1] *= 1.012
    arr[:, :, 2] *= 0.985
    arr = arr * 0.94 + 9.0
    arr = np.clip(arr, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    if os.environ.get("FINISH", "1") == "1":
        img = photo_finish(img)
        print("Applied photographic finishing pass")
    img.convert("RGB").save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: " + OUTPUT + "  dimensions=" + str(img.size) + "  bytes=" + str(size))
    if size < 51200:
        img.convert("RGB").save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT)) + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.convert("RGB").save(BACKUP, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + BACKUP)


if __name__ == "__main__":
    main()
