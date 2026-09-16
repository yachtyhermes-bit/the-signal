#!/usr/bin/env python3
"""Generate hero for afrm-affirm-underwriting-moat-fintech-2026 (fal flux/schnell).

Subject: Affirm Holdings (AFRM) — buy-now-pay-later / consumer credit network.
Its moat is the AI-driven underwriting engine plus the merchant network. The
article is about consumer credit being underwritten at the point of sale.

Sector: FINTECH — consumer payments. Scene MUST be a CONSUMER CHECKOUT MOMENT.

Scene chosen (ATTEMPT=1): a young shopper at a small boutique counter tapping a
phone on a compact point-of-sale card terminal, the shop assistant across the
counter, warm retail interior with soft depth of field.

Deliberately NOT a data center / server room / server aisle / cable run (banned),
NOT a trading floor, NOT a stock-ticker wall, NOT digital art, NOT a 3D render,
NOT neon / synthwave, NOT glowing lines, NOT geometric patterns, NOT abstract.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: retail is full of signage, price tags, receipts, terminal screens
  and logos, so all lettering, numbers, prices, currency symbols, UI and brand
  names are explicitly forbidden. Any screen / terminal display in frame is
  blank, dark, switched off or so far out of focus it is an unreadable wash.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-afrm-hero-20260916.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "afrm-affirm-underwriting-moat-fintech-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no prices, no price tags, no currency "
    "symbols, no dollar signs, no percentages, no digits, no sale signs, no "
    "store signage, no hanging signs, no window decals, no posters, no "
    "brand names, no company names, no corporate logos, no trademarks, no "
    "watermarks, no barcodes, no QR codes, no stickers, no labels on "
    "packaging, no handwriting, no legible writing of any kind anywhere in "
    "the image. The payment terminal has NO screen content: its small "
    "display is switched off, dark, angled away, or so far out of focus "
    "that it shows only a soft flat wash of dark grey with absolutely "
    "nothing readable or drawn on it, like an out-of-focus colour field "
    "photograph, not a screen showing a user interface. The phone being "
    "held shows a completely blank dark screen with no interface, no app, "
    "no icons, no numbers and no logos. There are no receipts, no printed "
    "paper slips, no cash register displays, no menus, no chalkboards, no "
    "clothing tags with writing, no shelf-edge labels, no signage of any "
    "kind on the walls or counters. The counter surface is plain and "
    "unmarked, the terminal body is plain dark plastic with unlabelled "
    "blank keys or no keys at all. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no chart graphics, no "
    "graph, no futuristic HUD graphics, no hologram, no floating overlay "
    "elements, no augmented-reality graphics, no data center, no server "
    "room, no server racks, no cable runs, no server lights, no computer "
    "monitor with text."
)

PROMPTS = {
    # 1 — boutique counter: shopper taps phone on a compact card terminal.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 50mm lens at "
        "f/2 on a full-frame camera, of a real consumer checkout moment "
        "inside a small independent boutique clothing shop. In the sharp "
        "centre of frame, a young shopper's hand reaches across a plain "
        "warm-toned wooden counter and taps a smartphone flat against a "
        "compact handheld card payment terminal that sits on a small "
        "unmarked stand. The phone is a plain dark slab held lightly between "
        "thumb and fingers, its screen switched off and dark, reflecting "
        "only a soft smear of shop light, with absolutely nothing displayed "
        "on it. The terminal is a small matte dark-grey plastic wedge with a "
        "flat contactless top and a tiny dark blank display facing away from "
        "the camera. Across the counter, softly out of focus behind the "
        "terminal, stands the shop assistant — a young woman in a plain "
        "unmarked apron over a simple shirt, hands resting relaxed on the "
        "counter edge, calm and attentive, mid-interaction, not posing. "
        "Behind her the boutique interior dissolves into cream: a rail of "
        "colourful folded garments, a pale plaster wall, a small leafy "
        "potted plant, a plain wooden shelf with plain unlabelled objects. "
        "Warm soft window light falls from the left, giving gentle shadows "
        "under the phone and a warm glow across the counter grain, with "
        "tungsten warmth from above. Very shallow depth of field: the "
        "phone, the hand and the top of the terminal are tack sharp while "
        "the assistant and the shop behind melt into creamy bokeh. Real "
        "optical lens blur, honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, subtle lens vignette, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — tighter crop: hands holding a phone against a plain reader + paper.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "tight close crop, shot on an 85mm lens at f/1.8, of the moment a "
        "customer pays at a small shop counter. The frame is filled by two "
        "hands: the customer's hand holding a plain dark smartphone flat "
        "against the top of a small matte-black contactless card reader that "
        "stands on a warm wooden counter, and, just behind and slightly "
        "softer, the shop assistant's hand resting lightly on the counter "
        "beside it. The phone's screen is completely dark and switched off, "
        "catching only a soft reflection of the shop's warm ceiling light "
        "and showing nothing at all. The card reader is a compact plain "
        "unmarked dark plastic unit with a flat top surface, a blank dark "
        "display tilted away from the camera and no visible lettering "
        "anywhere. A small folded plain paper slip lies face-down beside the "
        "reader, entirely blank. The counter is warm grained oak, gently "
        "softened by wear, with a blurred warm-lit shop interior behind: "
        "soft cream walls, a hint of hanging fabric, warm bokeh points of "
        "light from small ceiling lamps. Warm directional light from the "
        "upper left rakes across the knuckles and the phone's edge, with "
        "soft gentle shadow and a warm highlight on the counter grain. "
        "Extremely shallow depth of field — the phone, the fingertips and "
        "the reader's top surface are crisp, the assistant's hand and the "
        "entire background dissolving into heavy creamy bokeh. Honest "
        "editorial exposure, natural camera noise, very slight film grain, "
        "real optical blur, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — wider: small shop interior, counter, shopper and assistant.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 35mm lens at f/2.8 inside a small independent "
        "boutique shop during a purchase. A shopper stands at the right of "
        "frame in the mid-ground, seen from the side and slightly from "
        "behind, leaning in toward a plain light-wood sales counter, one "
        "hand holding a plain dark smartphone down against a small "
        "matte-black card terminal on the counter; their screen is dark and "
        "blank. Behind the counter stands the shop assistant, a young woman "
        "in a plain unmarked linen apron, looking down toward the terminal, "
        "relaxed and mid-task, neither turning toward nor posing for the "
        "camera. The shop around them is warm and ordinary: pale cream "
        "plaster walls, a simple rail of softly coloured garments to the "
        "left melting into blur, a plain wooden shelf holding a leafy "
        "potted plant, a few plain unlabelled folded items, a wide front "
        "window letting in soft overcast daylight from the left. The "
        "counter is bare apart from the terminal and a small plain ceramic "
        "tray. Warm daylight from the window mixes with a soft tungsten "
        "glow from small ceiling lamps, falling across the counter and the "
        "figures' shoulders, gentle shadows pooling on the wooden floor. "
        "Moderate shallow depth of field with the counter and the shopper's "
        "hand crisp and the far wall of the shop softening into gentle "
        "blur, real optical blur, honest available-light editorial "
        "exposure, natural camera noise, very slight film grain, subtle "
        "lens vignette, no plastic CGI sheen, no glossy render, no perfect "
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
