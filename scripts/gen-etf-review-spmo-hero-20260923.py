#!/usr/bin/env python3
"""Generate hero for etf-review-spmo-2026-09-23 (fal flux/schnell).

Article: "The ETF Review: SPY vs SPMO" — winners on one side, losers on the other.

Scene chosen (deliberately different from the recent mug/notebook/laptop/
glasses heroes):
A top-down editorial photograph of a dark walnut desk with two neat, evenly
squared stacks of completely blank plain cream card stock, the left stack
clearly taller than the right, a small gap between them, and a single plain
unbranded brass paperweight resting beside the shorter stack. Soft directional
morning window light raking in from the upper left, shallow depth of field
with real lens blur in the background, honest editorial exposure, very slight
film grain. Calm, tidy, editorial. Reads as "winners on one side, losers on
the other" without a single word in frame.

Deliberately NOT: a coffee mug, NOT a notebook, NOT a pen, NOT a laptop (all
recently used), NOT a trading floor, NOT a stock-ticker wall, NOT a data center
/ server room / cable run (banned), NOT digital art, NOT a 3D render, NOT CGI,
NOT neon / synthwave, NOT geometric abstractions, NOT charts or graphs, NOT a
futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame (desk scenes attract hands — banned).
- TEXT-FREE: card stock is a magnet for lettering, so every letter, word,
  number, percentage, price, ticker, logo, brand name, watermark, barcode,
  label and ruled line is explicitly forbidden. The card stock is completely
  blank and unprinted; the paperweight is plain and unbranded.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-etf-review-spmo-hero-20260923.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etf-review-spmo-2026-09-23")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no body parts of "
    "any kind anywhere in the frame or at the edges of the frame. No text, "
    "no letters, no words, no numbers, no digits, no prices, no percentages, "
    "no currency symbols, no dollar signs, no ticker symbols, no charts, no "
    "graphs, no axis labels, no brand names, no company names, no fund names, "
    "no logos, no trademarks, no watermarks, no signatures, no barcodes, no "
    "QR codes, no packaging labels, no stickers, no stamps, no seals, no "
    "newspaper, no magazine, no headlines, no book spines, no titles, no "
    "handwriting, no print, no printed marks, no engraved marks, no embossed "
    "marks, no ruled lines, no lined paper, no grid, no legible writing or "
    "drawn marks of any kind anywhere in the image. Every sheet of card stock "
    "in both stacks is completely blank and unprinted: plain cream uncoated "
    "card with absolutely nothing written, printed, stamped or embossed on "
    "it, and clean blank unprinted edges, reading only as paper and soft "
    "shadow. There is no readable or unreadable typography anywhere on any "
    "sheet. The brass paperweight is completely plain and unbranded with a "
    "smooth featureless surface, no engraving, no logo, no monogram and no "
    "lettering of any kind. No illustration, no digital art, no cartoon, no "
    "calligraphy, no typographic pattern, no 3D render, no CGI, no neon, no "
    "glowing lines, no light trails, no synthwave, no geometric patterns, no "
    "chart graphics, no futuristic HUD graphics, no hologram, no floating "
    "overlay elements, no augmented reality graphics, no data center, no "
    "server room, no server racks, no cable runs, no server lights, no "
    "trading floor, no ticker screen, no stock chart display."
)

PROMPTS = {
    # 1 — hero wide: top-down dark walnut desk, two blank card stacks, brass
    # paperweight, raking morning light from the upper left.
    "1": (
        "Photo-realistic editorial stock photograph, shot top-down from "
        "directly overhead on a 50mm lens at f/2.2 on a full-frame camera, of "
        "a dark walnut desk with two neat evenly squared stacks of completely "
        "blank plain cream card stock lying flat on it, photographed straight "
        "down from above. The left stack is clearly taller than the right "
        "stack, roughly twice as many sheets, and both stacks are squared "
        "precisely with crisp straight edges and completely blank unprinted "
        "cream card surfaces, no markings of any kind. A small clean gap of "
        "bare dark walnut separates the two stacks. A single plain unbranded "
        "brass paperweight, a simple smooth unadorned low brass dome with no "
        "engraving and no lettering, rests on the desk beside the shorter "
        "right stack. The desk is dark rich walnut with a fine matte grain, "
        "mostly falling out of focus toward the top of frame. Soft "
        "directional morning window light rakes in from the upper left, warm "
        "and low, modelling the crisp edges of the card stacks and throwing "
        "long soft shadows down and to the right across the desk; the "
        "background is a soft out-of-focus fall of quiet daylight and dark "
        "wood. Shallow depth of field with the front edges of both stacks and "
        "the brass paperweight crisply sharp and everything behind dissolving "
        "into smooth creamy bokeh, real optical lens blur, honest available "
        "light editorial exposure, natural camera noise, very slight film "
        "grain, subtle lens vignette, calm tidy unhurried editorial mood, no "
        "people present, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — medium close top-down: tighter on the two stacks and the paperweight.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close top-down view, shot straight down on an 85mm lens at "
        "f/1.8, of two neat evenly squared stacks of completely blank plain "
        "cream card stock on a dark walnut desk. The left stack is markedly "
        "taller than the right stack, both squared with crisp straight edges "
        "and utterly blank unprinted cream card surfaces, no writing, no "
        "numbers, no lines, no printing anywhere. A narrow gap of bare dark "
        "walnut sits between the two stacks. Lying beside the shorter right "
        "stack is one plain unbranded brass paperweight, a simple smooth "
        "unadorned brass dome with no engraving and no lettering. The desk is "
        "dark walnut with a fine matte grain and behind the stacks the "
        "background falls away into an out-of-focus wash of dark wood and "
        "quiet daylight. Warm directional morning sunlight from the upper "
        "left rakes across the scene, lifting the crisp top sheets of both "
        "stacks and the soft curve of the brass and casting long soft shadows "
        "down and to the right. Extremely shallow depth of field, real optical "
        "blur, honest editorial exposure, natural camera noise, very slight "
        "film grain, subtle lens vignette, calm unhurried mood, nobody in "
        "frame, no plastic CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    # 3 — slightly wider top-down desk still life, raking light and clear gap.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot top-down on a 35mm lens at f/2.8 looking straight "
        "down at a calm desk still life in an empty quiet room with nobody "
        "present. On the dark walnut desk lie two neat squared stacks of "
        "completely blank plain cream card stock, the left stack clearly "
        "taller than the right, separated by a small clean gap of bare wood. "
        "Both stacks are evenly squared with crisp straight edges and their "
        "surfaces are entirely blank unprinted cream card, with no writing, "
        "no numbers, no lines and no printing at all. A single plain "
        "unbranded brass paperweight, a smooth simple unadorned brass dome "
        "with no engraving and no lettering, rests on the desk beside the "
        "shorter right stack. The desk is dark rich walnut with a soft matte "
        "grain; from the upper left a window casts warm low morning sunlight "
        "across the stacks, making long gentle shadows down and to the right, "
        "and the out-of-focus background is dark wood and a soft fall of "
        "daylight fading into creamy blur. Moderate shallow depth of field "
        "with the card stacks and the brass paperweight crisp and the rest of "
        "the desk softening behind them, real optical blur, honest available "
        "light editorial exposure, natural camera noise, very slight film "
        "grain, subtle lens vignette, tidy unhurried editorial atmosphere, "
        "empty room with no human figure and no hands, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
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
    if size < 87040:  # <85KB
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")

    # Folded-in verification
    for p in (OUTPUT, BACKUP):
        im = Image.open(p)
        print(f"VERIFY {p}  dims={im.size}  bytes={os.path.getsize(p)}")


if __name__ == "__main__":
    main()
