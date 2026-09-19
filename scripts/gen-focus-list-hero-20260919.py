#!/usr/bin/env python3
"""Generate hero for focus-list-2026-09-19 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read covering four stocks
(Microsoft, Arista Networks, Vistra, RTX). It is NOT about a single company, so
the hero must suit a calm weekend-reading moment rather than a company or a
data center.

Scene chosen: a CALM SATURDAY-MORNING READING SPOT on a small apartment BALCONY
table in warm late-summer daylight — plain ceramic cup of coffee with a little
steam, an open paper notebook with completely blank pages, a plain unbranded
pen, and a slim laptop/tablet angled AWAY from camera so its screen is only a
soft featureless out-of-focus wash. Soft-blurred background: a small potted
olive/herb plant, a railing, indistinct rooftops or treetops in creamy bokeh.

Deliberately NOT: a trading floor, NOT a stock-ticker wall, NOT a data center /
server room / server aisle / cable run (banned), NOT digital art, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines / light trails, NOT
geometric patterns, NOT abstract art, NOT a chart graphic, NOT a futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at any edge (tabletop scenes attract hands —
  banned).
- TEXT-FREE: a notebook, a coffee cup and a working screen are all magnets for
  lettering, so every letter, word, number, percentage, price, logo, brand
  name, watermark, UI element, icon and packaging label is explicitly
  forbidden. The notebook pages are completely blank white paper with nothing
  written or printed on them. The cup is plain unmarked ceramic. The screen is
  a soft, featureless, unreadable wash of blurred colour — no chart, no axes,
  no labels, no interface, no cursor, no icons.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Shipped frame: PROMPTS["3"] (default ATTEMPT=3), the wider empty-balcony-corner
composition. Vision inspection of the shipped frame (Gemini 2.5 Flash):
PEOPLE no, TEXT no, notebook pages blank pure white, cup plain unmarked
ceramic, screen a featureless pale grey wash with nothing readable, setting a
balcony with railing + potted olive + blurred rooftops. Prompts 4-6 were
hardened anti-CGI film-stock variants tried during review: 4 rendered a CLOSED
laptop with a faint emblem (rejected), 5 and 6 left the laptop indistinct. The
flux/schnell "slightly smooth / not a real photo" verdict is characteristic of
this model at 4 inference steps — last week's shipped focus-list-2026-09-16
hero gets an identical verdict from the same inspector.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-focus-list-hero-20260919.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-09-19")
# ATTEMPT 3 is the frame that shipped (see docstring). Prompts 4-6 were
# hardened anti-CGI film-look variants tried during review and rejected.
ATTEMPT = os.environ.get("ATTEMPT", "3")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no legs, no body "
    "parts of any kind anywhere in the frame or at the edges of the frame. "
    "No text, no letters, no words, no numbers, no digits, no prices, no "
    "percentages, no currency symbols, no dollar signs, no ticker symbols, "
    "no charts with axis labels, no readable graph, no brand names, no "
    "company names, no logos, no trademarks, no watermarks, no signatures, "
    "no barcodes, no QR codes, no packaging labels, no stickers, no cup "
    "printing, no newspaper, no magazine, no headlines, no book spines, no "
    "handwriting, no print, no legible writing or drawn marks of any kind "
    "anywhere in the image. The open notebook pages are pure blank white "
    "paper, completely empty and unwritten, showing nothing but paper and "
    "soft shadow. The coffee cup is a plain unmarked ceramic cup with no "
    "design, no logo and no text. The laptop screen is angled away from the "
    "camera, out of focus, and shows only a soft, featureless, blurred wash "
    "of pale colour with absolutely nothing drawn, written or displayed on "
    "it — no chart, no graph line, no axis, no labels, no numbers, no "
    "interface, no menu bar, no dock, no app icons, no cursor, no window, no "
    "user interface, just an out-of-focus colour field like a photograph of "
    "frosted glass, the screen powered off or showing a single soft flat "
    "pale grey glow. The pen is a plain unbranded matte pen with a plain "
    "barrel and no writing on it. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no chart graphics, no "
    "futuristic HUD graphics, no hologram, no floating overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no server aisle, no cable runs, no server lights, no trading "
    "floor, no ticker screen, no stock chart display, no glossy plastic "
    "sheen."
)

PROMPTS = {
    # 1 — hero wide: small balcony table seen from slightly above, warm sun.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera, of a quiet Saturday-morning balcony "
        "table set for unhurried weekend reading, photographed from slightly "
        "above the tabletop. On the small weathered outdoor table sits a "
        "plain matte ceramic cup of black coffee with a faint curl of steam, "
        "an open paper notebook with completely blank empty pages, a plain "
        "unbranded matte dark pen resting diagonally on the blank paper, and "
        "a slim laptop pushed to the right of frame, its screen turned away "
        "from the camera and softly out of focus so it reads only as a pale "
        "featureless wash of light with nothing displayed on it. Behind the "
        "table a slim metal balcony railing and a small potted olive plant "
        "in a plain terracotta pot sit in soft focus, and beyond them "
        "indistinct rooftops and treetops dissolve into creamy bokeh. Warm "
        "directional late-summer sunlight rakes in from the side, laying "
        "long gentle shadows across the table surface, with a warm golden "
        "highlight on the cup's rim and the curved edge of the open "
        "notebook. Shallow depth of field: the cup, the blank notebook pages "
        "and the pen are tack sharp while the laptop, the plant, the railing "
        "and the whole background dissolve into smooth creamy blur. Honest "
        "available-light editorial exposure, natural camera noise, very "
        "slight film grain, real optical lens blur, subtle lens vignette, "
        "calm unhurried weekend mood, no people present, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — medium: tighter on cup, blank notebook and pen beside the laptop.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close view, shot on a 50mm lens at f/2, across a small "
        "outdoor balcony table in soft warm daylight. In the sharp centre of "
        "frame an open paper notebook lies flat, its two facing pages "
        "completely blank and empty, plain white paper with nothing printed "
        "or written on them; a plain unbranded matte black pen rests across "
        "the gutter of the notebook. Just to the left stands a plain matte "
        "ceramic cup of coffee with delicate steam catching the light "
        "against a dark out-of-focus background. To the right, the lower "
        "half of a slim open laptop sits at the edge of frame, tilted away "
        "so its screen is seen edge-on and thrown far out of focus, reading "
        "only as a soft pale grey blur of light with no interface, no chart, "
        "no text and no icons visible at all. The table is worn sun-bleached "
        "wood with visible grain; behind it a slim metal railing and a hint "
        "of a small potted olive plant dissolve into soft bokeh. Warm "
        "directional sunlight from the side catches the cup's handle, the "
        "white paper and the pen barrel, casting soft long shadows across "
        "the table. Extremely shallow depth of field, real optical blur, "
        "honest editorial exposure, natural camera noise, very slight film "
        "grain, subtle lens vignette, calm relaxed weekend mood, nobody in "
        "frame, no plastic CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    # 3 — wider feel: the whole empty balcony reading corner in warm light.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 28mm lens at f/4 of an empty sunlit apartment "
        "balcony reading corner, a calm weekend scene with nobody present. A "
        "small round weathered table stands beside the balcony railing, and "
        "on the table top sit a plain unmarked matte ceramic cup of coffee "
        "letting off gentle steam, an open paper notebook with completely "
        "blank unwritten pages, a plain unbranded pen laid on the paper, and "
        "a slim laptop angled away from the camera so only its pale "
        "unreadable screen glow is visible — a soft featureless wash of "
        "light with nothing drawn, written or displayed on it. Warm late-"
        "summer sunlight rakes across the balcony from the side, washing the "
        "table, the blank paper and the potted olive plant in golden light "
        "and laying long soft shadows across the surface. Beyond the slim "
        "metal railing the softly blurred rooftops and treetops of a quiet "
        "neighbourhood melt into creamy bokeh under a pale warm sky. "
        "Moderate shallow depth of field with the cup, the notebook and the "
        "pen crisp and the balcony and city softening behind them, real "
        "optical blur, honest available-light editorial exposure, natural "
        "camera noise, very slight film grain, subtle lens vignette, relaxed "
        "unhurried weekend atmosphere, empty scene with no human figure and "
        "no hands, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 4 — hardened anti-CGI: attempt 3 framing shot as real 35mm film.
    "4": (
        "An actual 35mm film photograph, Kodak Portra 400, shot handheld on "
        "an old manual SLR with a 35mm lens wide open, then scanned — a real "
        "candid snapshot of an empty apartment balcony table on a calm "
        "weekend morning, nobody present. It is definitely a photograph and "
        "not a render: visible film grain across the whole frame, real "
        "optical falloff, slight lens vignette, imperfect focus, a little "
        "camera shake, dust and a faint scratch or two on the film, muted "
        "honest colours, slightly uneven exposure, blown-out highlight where "
        "the sun catches the rim of a plain matte ceramic cup of coffee with "
        "a thin curl of steam, deep soft shadow on the other side. On the "
        "small weathered round table: that plain unmarked ceramic cup, an "
        "open paper notebook lying flat with two completely blank pure white "
        "empty pages, a plain unbranded matte pen lying naturally on the "
        "paper and casting a real soft shadow, and a slim laptop at the "
        "right, angled away from the camera, its screen thrown far out of "
        "focus so it is only a pale featureless blurred wash of light with "
        "nothing displayed on it. Behind the table a slim metal balcony "
        "railing, a small potted olive plant in a plain terracotta pot, and "
        "beyond them indistinct rooftops and treetops rendered as creamy "
        "out-of-focus bokeh. Warm directional late-summer sunlight rakes in "
        "from the side of frame. Shallow depth of field, honest available-"
        "light editorial exposure, real optical blur, natural camera noise, "
        "no people present, nothing rendered, nothing illustrated, no "
        "digital painting, no CGI, no 3D visualisation, no plastic sheen, no "
        "glossy surface, no perfect symmetry, no studio lighting, "
        "photorealistic documentary photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 5 — hardened anti-CGI, tighter three-quarter view of the same table.
    "5": (
        "A genuine unretouched photograph shot on 35mm film with a 50mm lens "
        "at f/2, scanned from a negative — a real everyday snapshot of a "
        "quiet balcony table on a Saturday morning in warm late-summer "
        "daylight, completely empty of people. Real photographic texture: "
        "heavy visible film grain, authentic colour negative look, soft "
        "optical blur in the background, slight off-centre framing, a "
        "hair of motion blur, honest available-light exposure with the "
        "highlights just clipping where the sun rakes across the tabletop. "
        "Sitting on the worn wooden outdoor table: a plain matte ceramic cup "
        "of coffee, steaming gently, plain and unmarked; an open paper "
        "notebook with two perfectly blank pure white pages lying flat; a "
        "plain unbranded matte pen resting across the page at a natural "
        "angle with a soft real shadow beneath it; and a slim laptop on the "
        "far right, tilted away so its screen faces away from the camera and "
        "is far out of focus, a soft pale featureless wash of light with "
        "nothing at all displayed on it. A small potted olive plant and a "
        "slim metal railing sit soft and blurred just behind the table, and "
        "the indistinct rooftops and treetops of the neighbourhood dissolve "
        "into creamy bokeh. Warm directional side light, deep gentle "
        "shadows, shallow depth of field, no people present, nothing "
        "rendered, nothing illustrated, no digital art, no CGI, no 3D "
        "visualisation, no glossy plastic sheen, no perfect symmetry, no "
        "studio lighting, photorealistic documentary stock photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    # 6 — last hardened try: plain amateur-documentary phone-photo framing.
    "6": (
        "A real photograph, taken casually on an ordinary camera and not "
        "generated in any way: it is a slightly imperfect handheld shot of "
        "an empty balcony table on a quiet Saturday morning in warm early-"
        "autumn sun, with nobody at all in the scene. The photo has the "
        "honest, unsmoothed look of real documentary photography — fine "
        "sensor grain in the shadows, a mild lens vignette in the corners, "
        "slightly imperfect focus, an unremarkable colour balance, a "
        "highlight that is just barely blown out where the sunlight strikes "
        "the tabletop, and real world clutter-free everyday detail. On the "
        "small round outdoor table sit four ordinary objects: a plain matte "
        "ceramic cup of coffee giving off a thin wisp of steam, completely "
        "unmarked; an open paper notebook lying flat with two entirely "
        "blank pure white pages with nothing whatsoever printed or written "
        "on them; a plain unbranded matte pen lying naturally across the "
        "page with a real soft shadow under it; and a slim laptop angled "
        "fully away from the camera at the right of frame so its screen is "
        "invisible and only a soft blurred pale wash of out-of-focus light "
        "is visible, with nothing displayed on it. Behind the table, a slim "
        "balcony railing and a small potted olive plant sit softly blurred, "
        "and the indistinct rooftops and treetops of the neighbourhood melt "
        "into creamy bokeh beyond. Warm directional sunlight rakes across "
        "the table from the side. Shallow depth of field, honest available-"
        "light exposure, real optical blur, natural camera noise, no people "
        "present at all, no hands, no figures, nothing rendered, nothing "
        "illustrated, no digital art, no CGI, no 3D visualisation, no "
        "glossy plastic sheen, no studio lighting, no perfect symmetry, "
        "photorealistic documentary photography, 16:9 landscape "
        "composition. "
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
