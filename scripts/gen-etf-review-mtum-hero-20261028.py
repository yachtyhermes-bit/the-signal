#!/usr/bin/env python3
"""Generate hero for etf-review-mtum-2026-10-28 (fal flux/schnell).

Article: "The ETF Review: MTUM — iShares MSCI USA Momentum Factor ETF"
The picture must read as a physical metaphor for momentum and rotating weight
without any literal chart, ticker, screen or finance prop.

Scene chosen (deliberately different from previous ETF Review heroes):
a polished brass gyroscope — the classic three-ring gimbal instrument — on a
plain matte slate-grey surface, soft directional window light from the left,
shallow depth of field, quiet editorial still-life mood, cool neutral tones
with warm brass highlights.

Deliberately NOT a repeat of:
- etf-review-pave-2026-10-21 — worn drafting table, blueprint, steel rule,
  brass plumb bob.
- etf-review-shld-2026-09-30 — olive canvas pouch + brass rod + paper roll.
- etf-review-spmo-2026-09-23 — top-down card stacks + brass paperweight.
- the brass balance scale hero, the plain unmarked booklets with coffee hero.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. Never illustration, never
  a 3D-render/CGI look, never neon/synthwave.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts.
- TEXT-FREE: flux invents fake lettering on any flat surface that could hold a
  label, and draws tick marks on anything that reads as an instrument. The
  gyroscope base and rings are therefore specified as plain, smooth, unmarked
  brass with no engraving, no graduations, no numerals, no scale of any kind.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-etf-review-mtum-hero-20261028.py
"""
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etf-review-mtum-2026-10-28")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Everything in the frame is plain and unmarked: the brass base and the "
    "brass rings are smooth bare metal with absolutely no engraving, no "
    "stamped marks, no etched marks, no numerals, no letters, no tick marks, "
    "no graduations, no measurement scale, no dial face and no maker's mark "
    "anywhere on the instrument or on the grey surface beneath it. "
    "No text of any kind anywhere in the image: no letters, no words, no "
    "numbers, no digits, no labels, no tags, no stickers, no logos, no "
    "trademarks, no monograms, no watermarks, no signatures, no barcodes, no "
    "printed marks, no handwriting, no symbols, no arrows, no icons. "
    "No people at all: no person, no human, no face, no head, no hands, no "
    "fingers, no arms, no wrists, no shoulders, no body parts anywhere in the "
    "frame or at the edges of the frame. Nothing else on the surface: no "
    "chart, no graph, no trading screen, no monitor, no phone, no tablet, no "
    "paper, no notebook, no pen, no ruler, no tools, no coins, no keys, no "
    "watch, no glasses, no cup, no plant. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no plastic sheen, no glossy computer "
    "graphics look, no neon, no glowing lines, no light trails, no synthwave, "
    "no data centre, no server room, no cables, no floating overlay graphics, "
    "no hologram, no abstract art, no geometric pattern wallpaper."
)

PROMPTS = {
    # 1 — primary. Instrument named first and largest in the frame; base
    # described as a plain smooth brass disc so flux has no face to letter.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a full-frame "
        "camera with an 85mm lens at f/2.0 in a quiet empty studio, of a "
        "single polished brass gyroscope — the classic instrument of three "
        "concentric brass gimbal rings mounted one inside the other on short "
        "pivots, around a small central brass axle — standing upright on a "
        "plain matte slate-grey surface. The three rings are smooth rounded "
        "bands of polished brass, the outer ring the largest, each ring "
        "nested inside the next at a slightly different angle so the gimbal "
        "reads clearly as a rotating mechanism, their metal catching warm soft "
        "highlights along the top left of each curve and falling into deep "
        "warm shadow underneath. The instrument rests on a small plain smooth "
        "brass disc base with a simple short stem, the base completely bare "
        "and unmarked, no face, no dial, no plate. Soft directional daylight "
        "from an unseen window on the left, low and diffused, modelling the "
        "brass gently and laying one long soft shadow to the right across the "
        "grey surface. The slate-grey surface is matte, fine-grained and "
        "plain, cool neutral grey, empty on every side of the instrument with "
        "calm negative space around it and the far surface dissolving into a "
        "cool grey out-of-focus background. Cool neutral tones overall with "
        "warm brass highlights, shallow depth of field with the near rings "
        "and the base crisp and the rear of the outer ring softening into "
        "real optical blur, honest available-light exposure, natural camera "
        "noise, very slight film grain, subtle lens vignette, quiet sober "
        "editorial still-life mood, no perfect symmetry, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    # 2 — fallback: closer, lower angle, more negative space, matte brass
    # rather than mirror-polished to cut the render sheen.
    "2": (
        "A real editorial still-life photograph, shot from a low three-quarter "
        "angle just above the surface on a 50mm lens at f/2.0, in an empty "
        "quiet studio: a single brass gyroscope of three concentric gimbal "
        "rings, the classic three-ring instrument, standing on a plain matte "
        "slate-grey tabletop that fills the lower third of the frame and runs "
        "away out of focus behind. The rings are brushed, lightly tarnished "
        "brass with a soft satin finish rather than a mirror shine, plain "
        "smooth bands of rounded cross-section nested one inside another and "
        "tilted at slightly different angles around a slim central axle, "
        "mounted on a short plain brass stem and a small round base that is "
        "smooth, bare and completely featureless. Soft directional window "
        "light from the left grazes the brass, one gentle highlight along the "
        "top of each ring and one long soft shadow stretching to the right "
        "over the grey. The grey tabletop is plain and unbroken with wide calm "
        "empty space around the instrument and nothing else on it at all. "
        "Background falls into a cool, dim, softly graduated grey haze. Cool "
        "neutral palette, warm brass highlights, shallow depth of field with "
        "the front of the outer ring and the stem sharp and the background "
        "melting into smooth optical blur, honest available-light exposure, "
        "natural film grain, faint dust, subtle vignette, quiet unhurried "
        "editorial mood, no perfect symmetry, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. " + NO_TEXT
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
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size)
          + "  bytes=" + str(len(r.content)))
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
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: " + OUTPUT + "  dimensions=" + str(img.size)
          + "  bytes=" + str(size))
    if size < 102400:  # <100KB
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT))
              + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print("Mirrored to " + BACKUP)

    for p in (OUTPUT, BACKUP):
        im = Image.open(p)
        print("VERIFY " + p + "  dims=" + str(im.size)
              + "  bytes=" + str(os.path.getsize(p)))


if __name__ == "__main__":
    main()
