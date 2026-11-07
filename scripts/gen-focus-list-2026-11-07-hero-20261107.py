#!/usr/bin/env python3
"""Generate hero for focus-list-2026-11-07 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read — four stocks read
slowly over a weekend morning, not a single company story and not a trading
floor.

Scene chosen for THIS edition: a MORNING KITCHEN TABLE in warm autumn daylight.
A plain stoneware mug of black coffee, an OPEN paper notebook with a pen
resting on it, a laptop turned slightly away so only an abstract unreadable
soft chart glow spills from the screen, a small plant blurred in the
background. Photorealistic, shallow depth of field, editorial photography.

Hard rules:
- NO people, no hands, no body parts anywhere in frame or at the edges.
- TEXT-FREE: no letters, words, numbers, prices, tickers, logos, UI labels.
  Notebook pages blank. Mug unmarked. Laptop screen only an abstract glow.
- NOT: trading floor, ticker wall, data center / server room / cable run,
  neon, synthwave, abstract art, CGI / 3D render, HUD.

Usage: cd /home/chino/thesignal && ATTEMPT=1 \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-11-07-hero-20261107.py
"""
import json
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-11-07")
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
    "stickers, no keyboard lettering, no keycap legends. The open notebook's "
    "two visible pages are entirely blank, clean, empty paper with only faint "
    "ruled lines and nothing written or drawn on them. The mug is a plain "
    "unmarked stoneware mug with no design and no printing. The laptop has no "
    "logo, no apple, no emblem and no sticker on its lid, its base or its "
    "hinge, and its keyboard keys are plain unmarked blank keys. The laptop "
    "screen shows ONLY a soft abstract blur of warm light and muted colour "
    "with absolutely no numbers, no axes, no grid labels, no candlesticks, no "
    "readable graph, no interface, no menu bar, no dock, no icons and no text "
    "of any kind — an unrecognisable out-of-focus glow, nothing more. "
    "No people at all: no person, no human, no face, no head, no hands, no "
    "fingers, no arms, no wrists, no shoulders, no legs, no body parts of any "
    "kind anywhere in the frame or at the edges of the frame, and nobody "
    "seated at the table. No phone, no smartphone, no tablet, no smartwatch. "
    "No newspaper, no magazine, no book covers, no printed packaging. "
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
    "the notebook cut into the edges of the frame. It is a real camera "
    "photograph, not a computer image: visible fine film-like grain in the "
    "midtones and shadows, a trace of chromatic aberration on high-contrast "
    "edges, real crumbs and tiny specks on the wooden tabletop, honest wear "
    "on the wood, slightly uneven white balance, and a natural hand-held tilt. "
    "Honest available-light exposure, not a lit set and not an HDR composite. "
    "Shallow depth of field from a wide aperture, real optical lens blur and "
    "creamy natural bokeh, the background falling softly out of focus. Real "
    "texture in the paper, the turned wood, the glaze of the mug and the "
    "leaves of the plant. No plastic CGI sheen, no glossy render, no perfect "
    "symmetry, no immaculate studio cleanliness, no retouched hyper-clean "
    "digital look, no 3D visualisation, no digital illustration, no "
    "concept-art lighting, no video-game aesthetic. Photorealistic, very high "
    "detail, professional editorial stock photography for a business "
    "newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — primary: morning kitchen table, warm autumn light, slightly high angle.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.0 on a full-frame camera from a gentle three-quarter angle at "
        "seated eye height, of an ordinary wooden kitchen table on a quiet "
        "Saturday morning in autumn. Warm low morning sunlight comes in "
        "through a window off to the left, laying a soft bright patch across "
        "the grain of the table and leaving long gentle shadows behind the "
        "objects. In the sharp foreground, just left of centre, stands a plain "
        "unmarked stoneware mug of black coffee, its glaze showing honest "
        "crazing, a thin curl of steam rising. Beside it an open paper "
        "notebook lies flat on the table with its two blank pages facing up, "
        "the spine slightly creased and the paper a warm off-white, and a "
        "simple dark pen rests diagonally across the right-hand page. Further "
        "back and turned slightly away to the right, a slim open laptop sits "
        "at an angle so the viewer sees mostly the back of its plain pale "
        "screen and only a sliver of the display, from which a soft "
        "unreadable abstract glow of pale warm light spills across the keys. "
        "In the soft background, well out of focus, a small potted green plant "
        "and the pale blur of a kitchen wall. Warm autumn morning light, "
        "ordinary, lived-in, unhurried. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — alternate framing: lower, closer on mug and notebook, more bokeh.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera at table height, close and low, of a "
        "worn wooden kitchen table on a calm autumn weekend morning. Warm "
        "morning sun rakes in from a window at the left, glowing softly "
        "through the steam of a plain unmarked stoneware mug of black coffee "
        "that dominates the left foreground, its rim slightly chipped. To its "
        "right an open paper notebook lies flat, both pages completely blank, "
        "a slim dark pen resting across the gutter, the paper catching a "
        "little warm light. Behind the notebook, pushed back and rotated "
        "partly away, a slim open laptop shows the viewer its plain pale back "
        "and just the edge of a screen glowing with a soft diffuse unreadable "
        "wash of muted colour. Far behind, dissolved in creamy bokeh, a small "
        "leafy houseplant and the soft shape of a kitchen windowsill. Warm, "
        "quiet, slightly cluttered, nothing staged. "
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
            "seed": int(os.environ.get("SEED", "718243")),
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
