#!/usr/bin/env python3
"""Generate hero for focus-list-2026-09-16 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read covering four stocks
(AVGO, CEG, SOFI + one more). It is NOT about a single company, so the hero
must suit a four-stock weekend long read rather than one company.

Scene chosen: a CALM WEEKEND-READING MOMENT at a morning kitchen table in warm
daylight — mug of coffee, an open paper notebook, a pen, and a laptop whose
screen shows only an abstract unreadable wash. Relaxed, unhurried mood.

Deliberately NOT: a trading floor, NOT a stock-ticker wall, NOT a data center /
server room / server aisle / cable run (banned), NOT digital art, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines / light trails, NOT
geometric patterns, NOT abstract art, NOT a chart graphic, NOT a futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame (desk / tabletop scenes attract hands — banned).
- TEXT-FREE: a notebook, a coffee mug and a working laptop are all magnets for
  lettering, so every letter, word, number, percentage, price, logo, brand
  name, watermark, UI element, icon and packaging label is explicitly
  forbidden. The notebook pages are completely blank white paper with nothing
  written or printed on them. The mug is plain unmarked ceramic. The laptop
  screen is a soft, featureless, unreadable wash of blurred colour — no chart,
  no axes, no labels, no interface, no cursor, no icons.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-focus-list-hero-20260916.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-09-16")
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
    "no currency symbols, no dollar signs, no ticker symbols, no charts with "
    "axis labels, no brand names, no company names, no logos, no trademarks, "
    "no watermarks, no signatures, no barcodes, no QR codes, no packaging "
    "labels, no stickers, no mug printing, no newspaper, no magazine, no "
    "headlines, no book spines, no handwriting, no print, no legible writing "
    "or drawn marks of any kind anywhere in the image. The open notebook "
    "pages are pure blank white paper, completely empty and unwritten, "
    "showing nothing but paper and soft shadow. The coffee mug is a plain "
    "unmarked ceramic mug with no design, no logo and no text. The laptop "
    "screen is angled slightly away from the camera, out of focus, and shows "
    "only a soft, featureless, blurred wash of pale colour with absolutely "
    "nothing drawn, written or displayed on it — no chart, no graph line, no "
    "axis, no labels, no numbers, no interface, no menu bar, no dock, no "
    "app icons, no cursor, no window, no user interface, just an out-of-focus "
    "colour field like a photograph of frosted glass, the screen powered off "
    "or showing a single soft flat pale grey glow. The pen is a plain "
    "unbranded matte pen with a plain barrel and no writing on it. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no chart graphics, no futuristic HUD graphics, no hologram, no floating "
    "overlay elements, no augmented-reality graphics, no data center, no "
    "server room, no server racks, no cable runs, no server lights, no "
    "trading floor, no ticker screen, no stock chart display."
)

PROMPTS = {
    # 1 — hero wide: kitchen table seen from slightly above, morning light.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera, of a quiet morning kitchen table set "
        "for unhurried weekend reading, photographed from slightly above the "
        "tabletop. On the warm light-wood kitchen table sits a plain white "
        "unmarked ceramic mug of black coffee with a faint curl of steam, an "
        "open paper notebook with completely blank empty pages, a plain "
        "unbranded matte dark pen resting diagonally on the blank paper, and "
        "a slim open laptop pushed to the right of frame, its screen turned "
        "away from the camera and softly out of focus so it reads only as a "
        "pale featureless wash of light with nothing displayed on it. Behind "
        "the table, a soft out-of-focus kitchen background of pale plaster "
        "wall and a linen curtain melts into creamy bokeh. Warm low morning "
        "sunlight streams in from the left through a window, raking long "
        "gentle shadows across the table grain, with a warm golden highlight "
        "on the mug's rim and the curved edge of the open notebook. Shallow "
        "depth of field: the mug, the blank notebook pages and the pen are "
        "tack sharp while the laptop and the whole background dissolve into "
        "smooth creamy blur. Honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, real optical lens "
        "blur, subtle lens vignette, calm unhurried mood, no people present, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — medium: tighter on mug, notebook and pen beside the laptop base.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close view, shot on a 50mm lens at f/2, across a warm wooden "
        "kitchen table in soft morning light. In the sharp centre of frame "
        "an open paper notebook lies flat, its two facing pages completely "
        "blank and empty, plain white paper with nothing printed or written "
        "on them; a plain unbranded matte black pen rests across the gutter "
        "of the notebook. Just to the left stands a plain white ceramic mug "
        "of coffee with delicate steam catching the light against a dark "
        "out-of-focus background. To the right, the lower half of an open "
        "laptop sits at the edge of frame, tilted away so its screen is "
        "seen edge-on and thrown far out of focus, reading only as a soft "
        "pale grey-pink blur of light with no interface, no chart, no text "
        "and no icons visible at all. The table is warm worn oak with "
        "visible grain; behind it a blurred kitchen wall and a hint of a "
        "potted green plant dissolve into soft bokeh. Warm directional "
        "morning sunlight from the left edge catches the mug's handle, the "
        "white paper and the pen barrel, casting soft long shadows to the "
        "right. Extremely shallow depth of field, real optical blur, honest "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, calm relaxed weekend mood, nobody in frame, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — wider room feel: table in a sunlit morning kitchen nook.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 28mm lens at f/4 of an empty sunlit morning "
        "kitchen nook, a calm weekend scene with nobody present. A small "
        "round light-wood table stands beside a bright window with a sheer "
        "linen curtain, and on the table top sit a plain unmarked white "
        "ceramic mug of coffee letting off gentle steam, an open paper "
        "notebook with completely blank unwritten pages, a plain unbranded "
        "pen laid on the paper, and an open slim laptop angled away from the "
        "camera so only its pale unreadable screen glow is visible — a soft "
        "featureless wash of light with nothing drawn, written or displayed "
        "on it. Soft warm morning sunlight floods through the window from "
        "the left, washing the pale plaster wall, the wooden tabletop and "
        "the blank paper in golden light and laying long soft shadows across "
        "the surface. The background kitchen is simple and ordinary — a pale "
        "wall, a plain wooden counter edge, a small potted herb — melting "
        "into gentle blur. Moderate shallow depth of field with the mug, the "
        "notebook and the pen crisp and the room softening behind them, real "
        "optical blur, honest available-light editorial exposure, natural "
        "camera noise, very slight film grain, subtle lens vignette, relaxed "
        "unhurried weekend atmosphere, empty room with no human figure and "
        "no hands, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
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
