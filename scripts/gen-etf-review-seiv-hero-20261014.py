#!/usr/bin/env python3
"""Generate hero for etf-review-seiv-2026-10-14 (fal flux/schnell).

Article: "The ETF Review: SEIV" — an actively managed U.S. large-cap VALUE
factor ETF (SEI). Theme: patience, measurement, weighing things that are
unfashionable but solid.

Scene chosen (deliberately different from every hero already used in this
series):
An old-fashioned brass BALANCE SCALE — two completely plain, unmarked,
unengraved brass pans hanging from a smooth brass beam on a worn oak desk —
in soft natural morning window light. Beside it lies a folded newspaper turned
so only its blank reverse side shows. Quiet, tactile, unhurried. Reads
"value / measurement / patience" without a single word in frame.

Already used in this series (MUST NOT repeat): an unbranded notebook stack
with a brass stylus and coffee on a walnut desk; a calculator with a notebook
and a tablet; a shelf of books; a market-tote / checkout scene; a lab bench;
two top-down stacks of blank card stock with a brass paperweight; an olive
canvas drawstring pouch with a brass ruler and a paper roll.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no silhouettes,
  no body parts of any kind anywhere in frame or at the frame edges.
- TEXT-FREE: a balance scale is a magnet for engraved graduations and numerals,
  and a newspaper is a magnet for print, so every letter, word, number, degree
  mark, tick mark, graduation, logo, brand, watermark and barcode is explicitly
  forbidden. Beam and pans are perfectly smooth polished brass with no
  markings. The newspaper shows only its blank unprinted reverse side.
- NOT a data-center hallway, NOT neon/synthwave, NOT glowing laser lines,
  NOT a 3D render, NOT CGI sheen, NOT abstract art.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "etf-review-seiv-2026-10-14"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no digits, no symbols, no tick marks, no graduations, no engraved scale markings, "
    "no logos, no branding, no watermarks, no barcodes. "
    "The brass balance-scale beam and both pans are perfectly smooth and completely unmarked, "
    "with no ruling, no engraving and no numbers of any kind. "
    "The newspaper is folded over so only its blank, unprinted reverse side is visible: "
    "not a single letter, headline, column of type or printed line anywhere on it. "
    "No people, no hands, no faces, no human figures, no silhouettes, no body parts. "
    "No neon lights, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Strictly photorealistic editorial still life."
)

BASE = (
    "Professional editorial still life photograph, shot on a 50mm f/2.0 lens on a full-frame camera, "
    "natural soft morning window light raking in from the side with gentle, real, directional shadows. "
    "On a worn oak kitchen table sits an old-fashioned brass BALANCE SCALE: two plain, smooth, "
    "completely unmarked polished brass pans hanging by thin chains from a simple brass beam, "
    "weathered warm patina in the metal. Beside the scale lies a single folded newspaper turned over "
    "so only its blank unprinted back page shows, its edge slightly curled, catching the light. "
    "A small plain linen cloth is folded nearby. "
    "Clean, calm, balanced, contemplative composition; rich organic textures of aged brass, "
    "soft newsprint-free blank paper, natural linen and oak wood grain. "
    "Authentic shallow depth of field with real lens blur behind, honest available-light exposure, "
    "extremely high detail, subtle true film grain, documentary photography, "
    "16:9 landscape aspect ratio. "
)

NO_PAPER = (
    "There is absolutely NO paper, NO newspaper, NO document, NO book, NO notebook, NO card and NO printed "
    "matter anywhere in the scene: every object is cloth, metal, wood or ceramic only. "
    "No statues, no figurines, no monuments, no hooded or robed figures, no carved human shapes. "
)

PROMPTS = {
    1: BASE + NO_TEXT,
    3: (
        "Professional editorial still life photograph, shot on a 50mm f/1.8 lens on a full-frame camera, "
        "natural soft morning window light raking in from the upper left with gentle real directional shadows. "
        "On a worn, gently scuffed oak table sits an antique brass BALANCE SCALE: two plain, smooth, "
        "completely unmarked polished brass pans hanging on delicate chains from a simple brass beam, "
        "lovely warm weathered patina. Beside the scale rests a neatly folded plain natural linen cloth in "
        "soft undyed oatmeal tones, and a small smooth unmarked brass counterweight. "
        "Nothing else on the table. Calm, patient, tactile, contemplative; rich organic textures of aged "
        "brass, dry linen weave and natural oak grain. Shallow depth of field with soft real lens blur in "
        "the background, honest available-light exposure, extremely high detail, subtle true film grain, "
        "documentary photography, 16:9 landscape aspect ratio. " + NO_PAPER + NO_TEXT
    ),
    2: (
        "Documentary editorial photograph, three-quarter view, natural soft morning window light from the "
        "left, real shadows on the table. An antique brass balance scale with two plain, polished, "
        "completely blank brass pans and a smooth unengraved beam stands on a scuffed oak desk; "
        "next to it a folded broadsheet newspaper lies face-down so only its blank unprinted white side "
        "is visible. A worn wooden stool edge and a soft out-of-focus background. "
        "Warm, quiet, patient, tactile. Shallow depth of field, subtle film grain, 50mm lens, "
        "photorealistic, high detail, 16:9 landscape. " + NO_TEXT
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


def main():
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    attempt = int(os.environ.get("ATTEMPT", "1"))
    seed = int(os.environ.get("SEED", "824143"))
    prompt = PROMPTS.get(attempt)
    if not prompt:
        print(f"ERROR: no prompt for ATTEMPT={attempt}")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal flux/schnell (attempt={attempt}, seed={seed})...")
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": seed,
    }
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print(f"ERROR: Could not get image url: {result}")
        sys.exit(1)

    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT)
    print(f"Saved initial image: {OUTPUT} size={img.size} bytes={len(r.content)}")

    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize / upscale to standard 1920x1080
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)

    # Write public copy, then copy the exact same bytes to _backup_dist
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    with open(OUTPUT, "rb") as src, open(BACKUP, "wb") as dst:
        dst.write(src.read())

    print(f"Wrote {OUTPUT}")
    print(f"Wrote {BACKUP}")
    print(f"Final: {img.size} mode={img.mode}")
    print("Done!")


if __name__ == "__main__":
    main()
