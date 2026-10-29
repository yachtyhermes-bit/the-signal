#!/usr/bin/env python3
"""Cron regen: nand-flash-supercycle-explainer-2026 hero (garbled chip markings).

Original hero (2026-10-25) carried hallucinated laser-etched part numbers on the
NAND packages ("SAMPUNG", blocks of "0000"). Flux renders chip faces as text
magnets, so this pass changes the CAMERA ANGLE rather than just asking harder:
the board is viewed from the connector end at a grazing angle, so every chip
top faces away from the lens into shadow and there is no readable surface left.

Usage:
  ATTEMPT=A /home/chino/video-venv/bin/python3 scripts/regen-nand-hero-cron-20261026.py
  ATTEMPT=B /home/chino/video-venv/bin/python3 scripts/regen-nand-hero-cron-20261026.py
"""

import os
import shutil
import sys

import requests

SLUG = os.environ.get("SLUG", "nand-flash-supercycle-explainer-2026")
ATTEMPT = os.environ.get("ATTEMPT", "A")
W, H = 1536, 864
FINAL_W, FINAL_H = 1920, 1080

OUT_LIVE = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
OUT_MIRROR = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"

NO_TEXT = (
    "No lettering anywhere in the frame: no text, no letters, no words, no "
    "numbers, no part numbers, no serial numbers, no date codes, no etched or "
    "laser-printed markings on any component, no silkscreen printing on the "
    "circuit board, no reference designators, no labels, no stickers, no "
    "barcodes, no logos, no brand names, no watermarks, no captions, no "
    "signage, no readable writing of any kind. Every component surface is "
    "plain, smooth, uniform and blank. No illustration, no digital art, no "
    "3D render, no CGI, no neon, no glowing lines, no futuristic HUD, no "
    "hologram, no data center, no server racks, no server aisle."
)

PROMPTS = {
    # A — grazing angle from the connector end: chip tops turned away into shadow.
    "A": (
        "A genuine close-up documentary photograph, real camera and real "
        "optics, definitely not a render: an opened 2.5-inch solid-state "
        "drive lies on a worn grey anti-static workbench mat, and the camera "
        "sits almost level with the bench, shooting down the length of the "
        "exposed green circuit board from the SATA connector end. Because of "
        "that low grazing angle the row of black flash memory packages and "
        "the small square controller are seen mostly edge-on from behind, "
        "their top faces turned completely away from the lens and sitting in "
        "soft shadow, so they read as simple dark rectangles with no visible "
        "surface detail at all. The bright metal edge of the pried-off "
        "aluminium lid anchors the lower left of the frame, catching a warm "
        "specular highlight, and fine copper traces, tiny silver capacitors "
        "and gold contact fingers run away from the camera in perspective. "
        "A steel precision tweezer and two loose screws lie on the mat in the "
        "near foreground, thrown well out of focus. Warm practical light from "
        "a single desk lamp behind and slightly right of the board rims the "
        "metal edges and drops the mid-ground into gentle amber shadow. "
        "Extremely shallow depth of field focused on the connector and the "
        "near edge of the aluminium shell, everything further up the board "
        "dissolving into smooth creamy bokeh. Natural sensor noise, slight "
        "film grain, mild vignette, honest uneven white balance, soft corners. "
        "No studio polish, no glossy sheen, no perfect symmetry, no product "
        "render look. Photo-realistic, high detail, editorial stock "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # B — subject swap: no manufactured flat panel facing the lens at all.
    "B2": (
        "A genuine macro photograph taken inside a semiconductor cleanroom, "
        "real camera and real optics, not a render: a gloved hand in a clean "
        "white nitrile glove holds a fragment of a silicon memory wafer up "
        "towards the light at a slight angle, filling the centre of the frame. "
        "The wafer surface is a dense, perfectly regular grid of identical "
        "rectangular memory dies separated by thin saw lanes, and shallow "
        "diffraction off the microscopic circuitry breaks the reflected light "
        "into soft iridescent green, violet and gold bands that sweep across "
        "the grid in a diagonal wash. The sawn edges of the fragment catch a "
        "thin bright rim, and the glove fabric and a second wafer lying on a "
        "polished stainless steel bench sit far behind, melted into smooth "
        "bokeh. Cool clean overhead light with a faint warm practical from the "
        "left, gentle falloff into the corners. Extremely shallow depth of "
        "field across the wafer surface, the near third tack sharp and the "
        "rest softening into an abstract shimmer. Natural sensor noise, very "
        "slight grain, mild vignette, honest white balance, no studio gloss. "
        "Photo-realistic, very high detail, editorial stock photography, 16:9 "
        "landscape composition. " + NO_TEXT +
        " No wafer batch code, no scribe-line characters, no die identification "
        "marks, no flat-orientation stamps, no fab logos, no printed anything "
        "on the wafer or the steel bench; the wafer pattern is pure repeating "
        "geometry with zero characters."
    ),
    # B — closed drive, single corner lifted: almost no board surface exposed.
    "B": (
        "An ordinary, slightly underexposed photograph taken handheld on a "
        "workbench with a 60mm macro lens at f/4, real hardware, not a render: "
        "an assembled 2.5-inch solid-state drive in its brushed silver "
        "aluminium shell lies diagonally on a dark grey anti-static mat, one "
        "corner lifted by a thin metal pry tool so a narrow dark gap opens "
        "along the seam and the shadowed circuitry inside is only glimpsed, "
        "not shown. Small scratched screws, a folded strip of blue thermal pad "
        "and a pair of tweezers are scattered around it. The shell dominates "
        "the frame: plain brushed metal with faint fingerprints, a hairline "
        "scratch and a dull warm reflection from a single desk lamp off to the "
        "left, which falls off quickly into shadow towards the right edge. "
        "The mat has a subtle crosshatch texture and a little dust. Modest "
        "depth of field with natural optical falloff, the near corner of the "
        "drive sharp and the far bench edge softly blurred. Real optics: "
        "highlight bloom on the metal, visible sensor noise in the shadows, "
        "slightly cluttered unposed framing, mild vignetting. No studio "
        "lighting, no CGI sheen, no 3D visualisation, no digital "
        "illustration, no product-render polish. Photo-realistic, high "
        "detail, documentary editorial photography, 16:9 landscape "
        "composition. " + NO_TEXT
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get("STEPS", "28" if ("dev" in model or "pro" in model) else "4"))
    print("Generating with " + model + " steps=" + str(steps))
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": steps,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
    result = fal_client.subscribe(model, arguments=args)
    url = None
    if result.get("images"):
        url = result["images"][0]["url"]
    elif result.get("output"):
        url = result["output"]
    elif result.get("image"):
        url = result["image"]
    if not url:
        print("ERROR: no image url: " + str(result))
        sys.exit(1)
    print("URL: " + url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    from PIL import Image

    img = Image.open(out_path)
    print("Downloaded " + out_path + " " + str(img.size) + " " + str(len(r.content)) + "b")
    return img


def crop_to_16x9(img):
    from PIL import Image

    target = FINAL_W / FINAL_H
    w, h = img.size
    cur = w / h
    if cur > target:
        nw = int(h * target)
        left = (w - nw) // 2
        img = img.crop((left, 0, left + nw, h))
    elif cur < target:
        nh = int(w / target)
        top = (h - nh) // 2
        img = img.crop((0, top, w, top + nh))
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = crop_to_16x9(generate(prompt, OUT_LIVE))
    img.save(OUT_LIVE, "JPEG", quality=94, optimize=True)
    if os.path.getsize(OUT_LIVE) < 102400:
        img.save(OUT_LIVE, "JPEG", quality=98, optimize=True)
    os.makedirs(os.path.dirname(OUT_MIRROR), exist_ok=True)
    shutil.copy2(OUT_LIVE, OUT_MIRROR)
    from PIL import Image

    v = Image.open(OUT_LIVE)
    print("FINAL " + OUT_LIVE + " " + str(v.size) + " " + str(os.path.getsize(OUT_LIVE)) + "b")


if __name__ == "__main__":
    main()
