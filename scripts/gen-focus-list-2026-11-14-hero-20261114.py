#!/usr/bin/env python3
"""Generate hero for focus-list-2026-11-14 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read — four stocks read
slowly over a weekend morning, not a single company story and not a trading
floor.

Scene chosen for THIS edition: a QUIET WEEKEND MORNING READING CORNER.
A wooden side table / desk beside a rain-speckled window with low autumn light.
A plain unmarked ceramic mug of coffee, one closed hardcover book with a
completely blank cover, a folded wool blanket over the back of an empty
armchair, a small stack of blank paper. Photorealistic, shallow depth of
field, editorial photography.

Hard rules:
- NO people, no hands, no body parts anywhere in frame or at the edges.
- TEXT-FREE: no letters, words, numbers, prices, tickers, logos, UI labels.
  Book cover completely blank. Mug unmarked. Paper stack blank. No keyboard.
- NOT: trading floor, ticker wall, data center / server room / cable run,
  neon, synthwave, abstract art, CGI / 3D render, HUD.

Usage: cd /home/chino/thesignal && ATTEMPT=1 \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-11-14-hero-20261114.py
"""
import json
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-11-14")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "The frame is completely free of every kind of lettering. No text, no "
    "letters, no words, no handwriting, no scribbles, no pen marks on the "
    "paper, no numbers, no digits, no prices, no percentages, no currency "
    "symbols, no ticker symbols, no axis labels, no chart legend, no brand "
    "names, no company names, no logos, no emblems, no trademarks, no "
    "watermarks, no signatures, no barcodes, no QR codes, no labels, no "
    "stickers, no embossing, no foil stamping. The closed hardcover book has "
    "a completely blank, plain, unprinted cloth cover with no title, no "
    "author name, no spine text, no dust jacket artwork and no design of any "
    "kind — a single solid muted colour with only the weave of the cloth "
    "visible. The mug is a plain unmarked ceramic mug with no design and no "
    "printing. The stack of loose paper is entirely blank, clean, empty paper "
    "with nothing written or drawn on it, and no sheets of paper anywhere in "
    "the frame carry any marking. There is no laptop, no computer, no "
    "keyboard, no screen and no device of any kind in the frame. "
    "No people at all: no person, no human, no face, no head, no hands, no "
    "fingers, no arms, no wrists, no shoulders, no legs, no body parts of any "
    "kind anywhere in the frame or at the edges of the frame, and nobody "
    "seated in the armchair or standing at the window. No phone, no "
    "smartphone, no tablet, no smartwatch. "
    "No newspaper, no magazine, no printed packaging. "
    "No illustration, no cartoon, no digital art, no 3D render, no CGI, no "
    "video-game still, no concept art, no matte painting, no neon, no "
    "synthwave colour, no glowing light trails, no abstract geometric art, no "
    "floating holographic elements, no wireframe, no dashboard, no data "
    "visualisation, no data center, no server room, no server racks, no server "
    "aisle, no cable run, no trading floor, no ticker wall, no robots."
)

COMMON = (
    "This is a quiet observational editorial still life, not a staged product "
    "shot and not a hero render: the objects sit loosely off-centre, the "
    "framing is relaxed and a little careless, and the edge of the table and "
    "the armchair cut into the edges of the frame. It is a real camera "
    "photograph, not a computer image: visible fine film-like grain in the "
    "midtones and shadows, a trace of chromatic aberration on high-contrast "
    "edges, real dust and tiny specks on the wooden tabletop, honest wear on "
    "the wood, slightly uneven white balance, and a natural hand-held tilt. "
    "Honest available-light exposure, not a lit set and not an HDR composite. "
    "Shallow depth of field from a wide aperture, real optical lens blur and "
    "creamy natural bokeh, the background falling softly out of focus. Real "
    "texture in the paper, the wood grain, the glaze of the mug, the weave of "
    "the wool blanket and the condensation on the window glass. No plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no immaculate studio "
    "cleanliness, no retouched hyper-clean digital look, no 3D visualisation, "
    "no digital illustration, no concept-art lighting, no video-game "
    "aesthetic. Photorealistic, very high detail, professional editorial "
    "stock photography for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — primary: side table by a rain-streaked window, armchair just behind.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.0 on a full-frame camera from a gentle three-quarter angle at "
        "seated eye height, of a quiet reading corner in an ordinary home on "
        "a slow weekend morning in late autumn. Low, soft autumn daylight "
        "comes in through a tall window off to the left, its glass speckled "
        "with fine rain droplets, and the light falls in a pale diffuse wash "
        "across a small worn wooden side table set beside the window. In the "
        "sharp foreground, left of centre, stands a plain unmarked ceramic "
        "mug of black coffee, its glaze showing honest crazing at the rim, a "
        "thin curl of steam rising and dissolving. Just to its right a single "
        "closed hardcover book lies flat on the table, bound in plain muted "
        "cloth with a completely blank cover and no jacket. Near the front "
        "edge, slightly out of focus, a small stack of loose blank paper sits "
        "square and untouched. Behind the table and pushed to the right, the "
        "back of an empty upholstered armchair fills the soft background, a "
        "folded grey wool blanket draped loosely over its back, its arm and "
        "cushion empty. Through the blur beyond the window, only a pale wash "
        "of autumn garden green and amber, unrecognisable. Cool-silver "
        "rainlight against warm wood tones, ordinary, lived-in, unhurried. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — alternate framing: lower and closer on the mug, book and window rain.
    # Hardened: the previous draw added a phone lying on an OPEN book, so this
    # prompt states the object set positively and insists the book is shut.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera at table height, close and low, of a "
        "worn wooden side table in a quiet reading corner on a calm autumn "
        "Sunday morning. The tabletop holds exactly three things and is "
        "otherwise bare: one plain unmarked ceramic mug of black coffee, one "
        "shut hardcover book lying flat with its front cover facing straight "
        "up, and one short stack of loose blank paper. There is nothing else "
        "on the table — no telephone, no device, no tray, no cutlery, no "
        "keys, no glasses. Cool rain-washed daylight seeps in from a tall "
        "window at the left, thousands of tiny droplets beaded on the glass "
        "and sliding in thin trails, and the light glows softly through the "
        "steam of the mug that dominates the left foreground, its rim "
        "slightly uneven, the glaze finely crazed. To its right the shut "
        "hardcover book lies at a slight angle, plain muted cloth binding "
        "with a completely blank unprinted cover, its pages fully enclosed "
        "between the boards so no paper edges or printed pages are exposed, "
        "one corner of the cover just lifting. The short stack of wholly "
        "blank paper sits half-hidden behind it, the edges catching a little "
        "pale light. Behind and above, softly out of focus, the heavy wool "
        "texture of a blanket folded over the back of an empty armchair, and "
        "the rain-speckled glass of the window fading into creamy bokeh. "
        "Quiet, still, slightly dusty, nothing staged. "
        + COMMON
        + NO_TEXT
    ),
}


def load_fal_key():
    for env_path in (
        "/home/chino/.hermes/profiles/yachty/.env",
        "/home/chino/hermes-workspace/studio-api/.env",
    ):
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("FAL_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
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
            "seed": int(os.environ.get("SEED", "928451")),
        },
    )
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("output"):
        image_url = result["output"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image URL in result: {json.dumps(result)[:400]}")
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


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    with open(f"/home/chino/thesignal/.last_hero_prompt_{SLUG}.txt", "w") as f:
        f.write(prompt + "\n")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 500_000 and quality > 70:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dims={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=quality, optimize=True)
    print(f"Mirrored to {BACKUP}  bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
