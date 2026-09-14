#!/usr/bin/env python3
"""Generate hero for adbe-ai-first-arr-creative-software-moat-2026 (fal flux/schnell).

Subject: Adobe (NASDAQ: ADBE) — creative software (Photoshop, Illustrator,
Acrobat, Firefly) and the "will AI eat creative software" debate.

Scene chosen: a creative professional's studio workstation — a pen display
tablet with a stylus being used by a designer's hand, colour swatch cards
fanned across a wooden desk, and a colour-calibrated monitor softly out of
focus behind showing only an abstract photographic colour gradient (no user
interface, no readable content). Warm window light, shallow depth of field,
moody editorial look.

Deliberately NOT a data-center / server-rack / power-grid / silicon-die /
rocket composition. No neon, no glowing lines, no HUD overlays, no 3D-render
look, no geometric patterns.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines.
- TEXT-FREE: the workstation naturally carries screens, keyboards, product
  boxes and packaging, so UI text, keyboard lettering, logos, brand names,
  labels and captions are explicitly forbidden. No watermark, no captions.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-adbe-creative-moat-hero-20260914.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "adbe-ai-first-arr-creative-software-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no user interface, no software windows, "
    "no toolbars, no menus, no icons, no filename labels, no captions, no "
    "subtitles, no keyboard lettering, no engraving, no printed packaging, "
    "no product boxes, no brand names, no manufacturer names, no logos, no "
    "trademarks, no watermarks, no stickers, no barcodes, no QR codes, no "
    "signage, no legible writing of any kind anywhere in the image. The "
    "monitor behind shows only a soft abstract photographic colour gradient "
    "with absolutely nothing readable or drawn on it, like an out-of-focus "
    "colour field photograph, not a computer screen with content. The "
    "keyboard is plain and blank, the stylus is plain and unmarked, the "
    "tablet surface is plain matte black glass with nothing displayed on it. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no colour-wheel diagram, no spectrum chart, no swatch grid "
    "graphic, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no cable runs, no computer screen with text."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a creative "
        "professional's studio workstation, shot from a low three-quarter "
        "angle across a warm wooden desk. In the near foreground and tack "
        "sharp, a designer's hand holds a stylus and draws on the matte black "
        "glass surface of a pen display tablet, the hand relaxed and natural "
        "with a plain unmarked sleeve, the stylus plain matte black and "
        "completely unlabelled. Scattered across the wooden desk beside the "
        "tablet are fanned colour swatch cards — a spread of matte printed "
        "colour chips in warm ochres, dusty terracottas, muted teals and soft "
        "greens, fanned like a hand of cards, their surfaces carrying pure "
        "colour rectangles and nothing else, absolutely no words, numbers or "
        "codes on them. A plain blank keyboard and a ceramic coffee cup sit "
        "softly out of focus further back. Behind everything, a "
        "colour-calibrated studio monitor is softly out of focus, showing "
        "only an abstract photographic colour gradient — a soft blurred wash "
        "of warm amber dissolving into dusty blue, pure colour field with no "
        "interface, no windows, no readable content. Warm late-afternoon "
        "window light falls across the desk from the left, raking across the "
        "wood grain and catching the edge of the hand, while the room behind "
        "falls into deep moody shadow. Very shallow depth of field: the "
        "stylus tip and the near swatch cards are tack sharp, everything "
        "behind melts into smooth creamy bokeh. Real optical blur, fine "
        "surface texture on the wood, honest natural lighting with gentle "
        "quiet contrast, subtle lens vignette, natural camera noise and very "
        "slight film grain, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a fast 50mm lens at f/1.8, not a render "
        "and not computer generated: a graphic designer's desk in a quiet "
        "studio, styled as an authentic business-press stock photo. A hand "
        "enters from the lower right, resting on a black pen display tablet "
        "and holding a slim digital stylus above the matte glass drawing "
        "surface, the fingers relaxed mid-stroke, a plain dark sleeve at the "
        "wrist with no branding. Fanned across the aged wooden desktop in "
        "front of the tablet is a set of loose printed colour swatch cards — "
        "heavy stock cards in warm cream, rust, sage, slate blue and "
        "mustard, each showing a single flat block of colour plus a thin "
        "paler band, deliberately fanning in an arc like playing cards, "
        "completely blank of any characters or codes. Further back on the "
        "desk, a plain unbranded keyboard and a small brass desk lamp sit "
        "blurred. Behind them, out of focus into softness, a professional "
        "colour-calibrated monitor glows with nothing but a smooth abstract "
        "photographic colour gradient, a seamless wash from warm peach to "
        "cool slate, no user interface and nothing legible on it. Warm "
        "afternoon window light comes in from the left through soft sheer "
        "curtains, giving a warm golden key on the desk and the hand with "
        "gentle shadow falloff into a dark uncluttered background of plain "
        "studio wall in shadow. Extremely shallow depth of field melts the "
        "monitor and lamp into creamy bokeh while the stylus, the hand and "
        "the nearest swatch cards stay crisp. Honest available-light moody "
        "exposure, slightly underexposed edges, real optical blur, natural "
        "camera noise and very slight film grain, faint dust on the wood, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine documentary-style photograph, not a render and not "
        "computer generated, of a creative workstation in a real studio just "
        "before dusk. The composition is built around a warm wooden desk "
        "seen at a slight diagonal. In the immediate foreground, softly "
        "sharp, the top of a black pen display tablet lies on the desk with "
        "a plain matte stylus resting across it and a designer's hand loosely "
        "holding the stylus, the fingers and knuckles catching a warm "
        "highlight, the sleeve plain and unbranded. Spread wide across the "
        "wood to the left of the tablet is an arc of printed colour swatch "
        "cards, each a heavy card printed with a single flat colour patch — "
        "warm browns, muted olives, pale blues and soft greys — fanned and "
        "overlapping like a spread deck, their surfaces bearing only flat "
        "colour with no writing, no numbering and no codes whatsoever. In the "
        "middle distance, blurred by distance, sit a plain blank keyboard and "
        "a small notebook with a plain cover. Behind the desk a "
        "colour-calibrated studio monitor stands softly and heavily out of "
        "focus, its panel filled edge to edge with a smooth abstract "
        "photographic colour gradient, warm amber bleeding gently into "
        "dusky blue like an out-of-focus colour-field photograph, with no "
        "interfaces, no windows and nothing readable anywhere on it. Warm "
        "window light streams in low from the left, backlighting faint dust "
        "in the air and grazing the desk grain, while the right side of the "
        "frame and the room behind fall away into deep moody shadow. "
        "Extremely shallow depth of field, creamy smooth bokeh behind the "
        "near plane, real optical blur, natural camera noise and very slight "
        "film grain, subtle lens vignette, honest underexposed editorial "
        "lighting, no plastic CGI sheen, no glossy render, no perfect "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
