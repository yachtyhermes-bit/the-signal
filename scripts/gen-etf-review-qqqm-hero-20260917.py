#!/usr/bin/env python3
"""Generate hero for etf-review-qqqm-2026-09-17 (fal flux/schnell).

Article: "The ETF Review: QQQM" — a deep-dive on the Invesco NASDAQ 100 ETF
(QQQM), a fund that holds 106 stocks inside one wrapper.

Scene chosen (deliberately different from the recent mug/notebook/laptop heroes):
A neat stack of plain, completely unmarked paper booklets (prospectus/pamphlet
sized, plain pale covers with nothing printed on them) on a light wooden desk in
soft morning window light, with a simple pair of unbranded reading glasses
resting on top of the stack. Calm, tidy, unhurried, editorial. Shallow depth of
field, real lens blur, warm directional light from the left, honest editorial
exposure, very slight film grain. Reads as "paperwork that explains what is
inside the wrapper".

Deliberately NOT: a coffee mug, NOT a notebook, NOT a pen, NOT a laptop (all
recently used), NOT a trading floor, NOT a stock-ticker wall, NOT a data center
/ server room / cable run (banned), NOT digital art, NOT a 3D render, NOT CGI,
NOT neon / synthwave, NOT glowing lines / light trails, NOT geometric patterns,
NOT chart graphics, NOT a futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame (desk scenes attract hands — banned).
- TEXT-FREE: booklets and glasses are magnets for lettering, so every letter,
  word, number, percentage, price, logo, brand name, watermark, barcode, spine
  title and packaging label is explicitly forbidden. The booklet covers and any
  visible page edges are completely blank/plain. The glasses are plain
  unbranded frames with no temple branding.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-etf-review-qqqm-hero-20260917.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etf-review-qqqm-2026-09-17")
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
    "marks, no legible writing or drawn marks of any kind anywhere in the "
    "image. Every paper booklet in the stack is completely blank and "
    "unmarked: plain pale unprinted covers with absolutely nothing written, "
    "printed, stamped or embossed on them, and blank unprinted page edges, "
    "reading only as clean paper and soft shadow. There is no readable or "
    "unreadable typography anywhere on any sheet or cover. The reading "
    "glasses are completely plain and unbranded with smooth featureless "
    "frames, no logo, no brand name and no lettering on the temples, no "
    "hinge marks, no text of any kind. No illustration, no digital art, no "
    "cartoon, no lettering, no calligraphy, no typographic pattern, no 3D "
    "render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no chart graphics, no futuristic HUD "
    "graphics, no hologram, no floating overlay elements, no augmented "
    "reality graphics, no data center, no server room, no server racks, no "
    "cable runs, no server lights, no trading floor, no ticker screen, no "
    "stock chart display."
)

PROMPTS = {
    # 1 — hero wide: stack of blank booklets + unbranded glasses, morning light.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 50mm lens at "
        "f/2.2 on a full-frame camera, of a neat stack of plain completely "
        "unmarked paper booklets resting on a light wooden desk, photographed "
        "from a low three-quarter angle just above desk level. The stack "
        "holds four or five softcover booklets of prospectus or pamphlet "
        "size, their covers plain pale off-white and pale grey uncoated card "
        "with absolutely nothing printed on them, the page edges clean and "
        "blank. A simple pair of plain unbranded reading glasses with thin "
        "dark metal frames rests on top of the stack, folded, one temple arm "
        "hanging slightly over the edge of the booklet beneath it. The desk "
        "is pale warm-toned wood with a fine matte grain, mostly out of "
        "focus toward the back of frame. Soft directional morning window "
        "light comes from the left, warm and low, modelling the stack and "
        "laying a long soft shadow to the right across the desk; a blurred "
        "pale plaster wall and a soft fall of quiet daylight fill the "
        "out-of-focus background. Shallow depth of field with the front "
        "booklet edges and the resting glasses crisply sharp and everything "
        "behind dissolving into smooth creamy bokeh, real optical lens blur, "
        "honest available-light editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, calm tidy unhurried "
        "mood, no people present, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — medium close: tighter on the top booklet and the folded glasses.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close view, shot on an 85mm lens at f/1.8, of a tidy stack "
        "of plain unmarked paper booklets on a light wooden desk in soft "
        "morning light. The sharp centre of frame is the top booklet of the "
        "stack, a plain pale cream card cover completely blank and "
        "unprinted, and lying folded on it a simple pair of plain unbranded "
        "reading glasses with thin dark metal frames and clear lenses, their "
        "folded temple arm catching a thin line of warm light. The lower "
        "booklets in the stack show only clean blank page edges and pale "
        "plain covers receding into soft focus, with no lettering, no logo "
        "and no printing anywhere. The desk surface is warm light wood with "
        "fine grain, and behind the stack the background falls away into an "
        "out-of-focus wash of pale wall and quiet daylight. Warm directional "
        "morning sunlight from the left edge rakes across the stack, lifting "
        "the paper edges and the metal of the glasses and casting soft long "
        "shadows to the right. Extremely shallow depth of field, real "
        "optical blur, honest editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, calm unhurried mood, "
        "nobody in frame, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — slightly wider desk still life: stack, glasses, soft window falloff.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 35mm lens at f/2.8 of a calm desk still life in "
        "an empty quiet room with nobody present. In the centre of the pale "
        "wooden desk sits a neat squared stack of plain completely unmarked "
        "softcover paper booklets, pamphlet sized, pale off-white and pale "
        "grey covers with nothing printed on them at all, their page edges "
        "clean and blank. A simple pair of plain unbranded reading glasses "
        "rests folded on top of the stack, thin dark frames, no branding "
        "anywhere. The desk is pale warm wood with a soft matte grain; to the "
        "left a window casts warm low morning sunlight across the stack, "
        "making a long gentle shadow to the right, and the out-of-focus "
        "background is a plain pale plaster wall with a soft fall of "
        "daylight fading into creamy blur. Moderate shallow depth of field "
        "with the booklets and the glasses crisp and the room softening "
        "behind them, real optical blur, honest available-light editorial "
        "exposure, natural camera noise, very slight film grain, subtle lens "
        "vignette, tidy unhurried editorial atmosphere, empty room with no "
        "human figure and no hands, no plastic CGI sheen, no glossy render, "
        "no perfect symmetry, no 3D visualisation, no digital illustration, "
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
