#!/usr/bin/env python3
"""Generate hero for irdm-rocket-lab-acquisition-spectrum-2026 (fal flux/schnell).

Subject: Iridium Communications (IRDM) — Rocket Lab's acquisition of Iridium and
the satellite-spectrum / L-band connectivity angle.

Scene chosen: SATCOM TERMINALS IN THE REAL WORLD — a rugged handheld satellite
phone with a thick stubby antenna resting on a paper nautical chart on a ship's
bridge chart table, brass parallel ruler and a coffee mug beside it, grey ocean
and horizon through the bridge window behind. Overcast maritime light, shallow
depth of field.

Deliberately NOT: a rocket launch pad (Sept 9 RKLB), a rocket in flight
(Sept 11 SPCX), a satellite in orbit (Aug 21 ASTS, June IRDM), a large
parabolic ground-station dish array (Sept 18 LHX), a data center / server room /
server rack / cable run, digital art, abstract art, neon/synthwave, glowing
lines, geometric patterns, illustration, a close-up human face.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: chart tables are wall-to-wall with printed charts, chart titles,
  compass roses, lat/long numerals, phone keypads and screens, so all lettering,
  numbers, UI, logos and brand names are explicitly forbidden. Any display in
  frame is blank / dark / switched off / out of focus.
- Generate 1536x864 (16:9), finalize 1920x1080, identical bytes to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/generate-irdm-rocket-lab-hero-20260919.py
"""

import os
import sys

import requests

SLUG = os.environ.get("SLUG", "irdm-rocket-lab-acquisition-spectrum-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
W, H = 1536, 864            # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

OUTPUT1 = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
OUTPUT2 = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
R2_URL = ("https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/"
          + SLUG + ".jpg")

NO_TEXT = (
    "Absolutely no lettering anywhere in the scene: no text, no letters, no "
    "words, no numbers, no numerals, no coordinates, no latitude or longitude "
    "figures, no printed chart titles, no chart legends, no compass rose "
    "labels, no depth soundings, no navigation warnings, no printed documents, "
    "no forms, no paperwork, no handwritten notes, no keypad characters, no "
    "button labels, no screen content, no phone display text, no UI, no menus, "
    "no icons, no signage, no plaques, no stickers, no labels, no nameplates, "
    "no brand names, no manufacturer names, no company names, no corporate "
    "logos, no trademarks, no watermarks, no serial numbers, no part numbers, "
    "no barcodes, no QR codes, no mug printing, no mug slogan, no engravings, "
    "no stencils, no markings on the brass ruler, no markings on the phone, no "
    "readable writing of any kind. The paper nautical chart is seen at a "
    "shallow angle and slightly out of focus so it reads only as a pale "
    "blue-grey field of soft line-work and contour shading with no legible "
    "printing, like an out-of-focus map texture. The satellite phone's small "
    "display is switched off and dark, a blank grey-black glass rectangle with "
    "nothing on it. No illustration, no digital art, no cartoon, no painting, "
    "no 3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no futuristic HUD graphics, no hologram, "
    "no overlay graphics, no abstract shapes, no data center, no server room, "
    "no server racks, no server aisle, no cable-run composition, no GPU "
    "hardware, no computer monitors, no satellite dish array, no parabolic "
    "antenna farm, no rocket, no launch pad, no spacecraft, no satellite in "
    "orbit, no starfield, no person's face in close-up."
)

PROMPTS = {
    # 1 — the brief: satphone on a chart table on a ship's bridge, brass ruler + mug.
    "1": (
        "Professional stock photograph, a genuine camera photograph and not a "
        "render, shot on a 50mm lens at f/2 on a full-frame DSLR: a rugged "
        "handheld satellite phone with a thick stubby antenna and a plain "
        "rubberised dark grey body rests on a paper nautical chart spread "
        "across a weathered wooden chart table on the bridge of a ship. The "
        "phone lies at a slight angle in the sharp foreground, its thick "
        "antenna standing up, its small display switched off and plain dark, "
        "its body smooth and unmarked. Beside it on the chart lies a well-worn "
        "brass parallel ruler, its metal edge scuffed and warm from handling, "
        "and a plain white ceramic coffee mug, the coffee inside still faintly "
        "steaming. The chart itself is soft pale blue-grey paper with faint "
        "contour line-work, deliberately slightly out of focus and at a "
        "shallow angle so no printing is legible. Behind the table, beyond a "
        "wooden window frame, the real world shows through the bridge window: "
        "a flat grey overcast ocean and a blurred horizon line dissolving into "
        "pale misty sky, out of focus and soft. Overcast maritime daylight "
        "falls evenly through the window, cool and diffuse, with gentle "
        "shadows under the phone, the ruler and the mug. Shallow depth of "
        "field: the satellite phone and the brass ruler tack sharp, the coffee "
        "mug and chart surface softening, the window and ocean beyond melting "
        "into creamy bokeh. Real optical lens blur, honest available-light "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photo-realistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — wider bridge interior: chart table + satphone with the ocean beyond.
    "2": (
        "A real documentary photograph taken on a working ship's bridge, not a "
        "render and not computer generated, shot on a 35mm lens at f/2.8: the "
        "navigation chart table of a ship's bridge, seen from an angle across "
        "the table. Spread out on its worn varnished surface is a large paper "
        "nautical chart, its pale blue-grey line-work softening out of focus "
        "toward the back, and on it rest the working tools of the watch: a "
        "rugged handheld satellite phone with a thick stubby antenna, its "
        "plain rubberised dark grey body unmarked and its small display dark "
        "and switched off; a scuffed brass parallel ruler; and a plain white "
        "coffee mug. Farther along the table, softly blurred, a folded pair of "
        "dividers and a rolled paper chart. Behind the table a wooden window "
        "frame divides the frame, and through the bridge windows the grey "
        "overcast sea meets a flat pale horizon under low cloud, everything "
        "beyond the glass soft and out of focus. No person is visible. "
        "Overcast maritime daylight, cool diffuse and shadowless, with gentle "
        "warmth on the brass. Shallow depth of field, the satellite phone and "
        "ruler crisp in the mid-ground, the far chart and the ocean window "
        "dissolving into creamy bokeh. Real optical lens blur, honest "
        "available-light editorial exposure, natural camera noise, very slight "
        "film grain, subtle lens vignette, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photo-realistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — tight close crop on the phone + antenna on the chart, ruler edge, mug bottom-left.
    "3": (
        "A genuine photograph, not a render and not computer generated: a "
        "tight close crop shot on an 85mm macro lens at f/2 of a rugged "
        "handheld satellite phone lying on a paper nautical chart. The phone "
        "fills the centre of the frame at a three-quarter angle: a plain "
        "rubberised dark grey body with moulded grip ribs, a chunky stubby "
        "helical antenna angled up and back, a plain unmarked keypad of smooth "
        "featureless rubber keys with no characters on them, and a small "
        "display switched off and completely dark. The chart beneath it is "
        "pale blue-grey paper, its contour line-work and fine mesh reading "
        "only as a soft out-of-focus texture around the phone. The scuffed "
        "edge of a worn brass parallel ruler enters from the lower right, "
        "catching a warm highlight, and the soft foot of a plain white coffee "
        "mug sits blurred at the lower left corner. Everything beyond the "
        "chart is creamy bokeh: a hint of varnished wood at the table edge and "
        "a pale grey wash of window light and overcast sea. Diffuse overcast "
        "maritime daylight from the upper left, soft honest shadows, no hard "
        "specular glare. Extremely shallow depth of field — antenna tip and "
        "phone body tack sharp, chart and ruler edge falling softly away. "
        "Real optical lens blur, honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, subtle lens vignette, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photo-realistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as fh:
            for line in fh:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        with open(real_path) as fh:
            raw = fh.read().strip().split("\n")[0]
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
    print("Generating image with fal-ai/flux/schnell ...")
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
        print("ERROR: no image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    from PIL import Image

    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size)
          + "  bytes=" + str(len(r.content)))
    return img


def crop_to_16x9(img):
    from PIL import Image

    target_ratio = FINAL_W / FINAL_H
    w, h = img.size
    cur = w / h
    if cur > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT1)
    img = crop_to_16x9(img)
    img.save(OUTPUT1, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT1)
    if size < 81920:
        img.save(OUTPUT1, "JPEG", quality=98, optimize=True)
        size = os.path.getsize(OUTPUT1)
    print("Saved final hero: " + OUTPUT1 + "  dimensions=" + str(img.size)
          + "  bytes=" + str(size))
    os.makedirs(os.path.dirname(OUTPUT2), exist_ok=True)
    img.save(OUTPUT2, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + OUTPUT2)
    from PIL import Image

    for p in (OUTPUT1, OUTPUT2):
        v = Image.open(p)
        print("VERIFY " + p + " dimensions=" + str(v.size[0]) + "x"
              + str(v.size[1]) + " bytes=" + str(os.path.getsize(p)))
    with open("/tmp/irdm_hero_prompt.txt", "w") as fh:
        fh.write(prompt)


if __name__ == "__main__":
    main()
