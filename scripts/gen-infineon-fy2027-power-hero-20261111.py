#!/usr/bin/env python3
"""Generate hero for infineon-fy2027-ai-power-guidance-raise-2026 (fal flux/schnell).

Subject: Infineon lifting its fiscal-2027 data-center power revenue target to
~EUR 4bn; power semiconductors (SiC / GaN / IGBT modules) as the real AI
data-center bottleneck.

Scene chosen: POWER SEMICONDUCTOR MANUFACTURING, not a data center.

  ATTEMPT 1 — Fab cleanroom: technician in a white bunny suit holds up a large
  SiC power wafer, rainbow diffraction sheen, amber-yellow cleanroom light,
  wafer-handling tool and FOUP pod soft in the background.  [QC: disc read as
  a plain gold metal disc, no device pattern — rejected]
  ATTEMPT 2 — Cleanroom retune: silvery mirror wafer, strong rainbow
  diffraction, visible die grid and flat notch, open wafer cassette behind.
  ATTEMPT 3 — Macro: power semiconductor module / SiC die on a copper
  substrate with aluminium bond wires, industrial lab bench.

Deliberately NOT a data-center hallway / server aisle / server room. No digital
art, neon, synthwave, glowing lines, geometric abstraction, text, logos.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=2 /home/chino/video-venv/bin/python3 \
    scripts/gen-infineon-fy2027-power-hero-20261111.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "infineon-fy2027-ai-power-guidance-raise-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no laser-scribed characters, no "
    "silkscreen text, no nameplates, no equipment model plates, no decals, no "
    "pictogram symbols or icons on any machine or wall, no brand names, no "
    "logos, no watermark, no captions, no legible writing of any kind "
    "anywhere. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no synthwave, no glowing lines, no light trails, no "
    "holograms, no futuristic HUD graphics, no augmented-reality overlays, no "
    "abstract digital patterns, no geometric abstraction, no charts, no "
    "graphs, no data visualization, no science-fiction styling. Not a "
    "data-center hallway, no server aisle, no server racks, no rack of "
    "blinking lights, no rows of computers."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with an 85mm lens at f/2.0, real available cleanroom light, not "
        "a render and not CGI: inside a modern semiconductor fabrication "
        "cleanroom. In the right half of the frame, in the sharp focal plane, a "
        "technician wearing a full white cleanroom bunny suit — one-piece "
        "coverall, white hood, white face mask, safety glasses and white nitrile "
        "gloves — stands holding up a large polished silicon-carbide power "
        "wafer with both gloved hands, turning it slightly to inspect it. The "
        "wafer is a 200mm mirror-finish disc about 20cm across, its surface "
        "catching the light in a fine iridescent rainbow diffraction sheen. "
        "Photorealistic, extremely high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with an 85mm lens at f/2.2, real available cleanroom light, not "
        "a render and not CGI: inside a semiconductor fabrication cleanroom, "
        "wafer inspection bench. In the sharp focal plane, right of centre, a "
        "technician in a white cleanroom bunny suit — one-piece coverall, "
        "hood up, white face mask, safety glasses, white nitrile gloves — holds "
        "a single large semiconductor wafer up to the light by its very rim so "
        "the disc faces the camera at a shallow angle. The wafer is 200mm "
        "across, silver-grey polished silicon, its face covered edge to edge "
        "in a dense grid of tens of thousands of tiny rectangular power-device "
        "cells, each about a centimetre wide, their aluminium top metal "
        "catching pin-sharp specular glints; a flat ground edge and a small "
        "orientation notch are visible on the rim. Across the whole disc the "
        "wet-looking mirror surface splits the light into strong iridescent "
        "rainbow diffraction bands — oil-slick violet, cyan, green and rose "
        "rippling over the cell grid — so the wafer clearly reads as a "
        "semiconductor wafer and not as a plain metal plate. The gloved "
        "fingers grip only the outer edge and are slightly soft. Directly "
        "behind the technician, out of focus, an open black wafer cassette "
        "stands on the bench, its machined slots stacked with a dozen more "
        "mirror-polished discs whose edges catch thin bright lines of light; "
        "further back a stainless wafer-handling load port and pale cleanroom "
        "wall panels dissolve into haze. Warm amber-yellow cleanroom light "
        "fills the room and gives the white suit a golden cast, while a cooler "
        "white beam from a laminar-flow hood above picks out the wafer; "
        "nothing in the frame emits its own light, no LEDs, no glow, no "
        "lens flare. Shallow depth of field: the wafer face and the near rim "
        "are razor sharp, the technician's shoulders, cassette and background "
        "melt into smooth creamy bokeh. Real optical lens blur, natural sensor "
        "noise, fine film grain, subtle vignette, slightly off-centre casual "
        "framing, authentic documentary feel, no plastic CGI sheen, no perfect "
        "symmetry. Photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition, wide "
        "horizontal framing. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic macro editorial photograph, shot on a 100mm macro lens "
        "at f/2.8, real bench light, not a render and not CGI: an extreme "
        "close-up of an open power semiconductor module on a grey anti-static "
        "lab bench. The module occupies the centre-right of the frame: a "
        "rectangular copper substrate with a thick nickel-plated copper base "
        "plate, its edges milled bright where they have been machined, and on "
        "top a neat row of bare silicon-carbide power dies — small dark "
        "blue-black squares about 8mm across with fine matte surfaces and tiny "
        "metallised gate pads in the corners. Heavy aluminium bond wires loop "
        "in shallow arcs from die to die and down to thick copper busbar "
        "terminals, the aluminium dull and slightly oxidised with a faint "
        "satin sheen, the wire loops casting crisp little shadows on the die "
        "surfaces. A thin film of clear silicone gel has been partly peeled "
        "back from the housing and curls along one edge. Solder fillets and "
        "flux residue catch the light, fingerprint smudges and a little "
        "workshop dust sit in the recesses — honest, used, handled hardware. To "
        "the left, deeply out of focus, the corner of a grey industrial "
        "inspection microscope and a spool of aluminium wire. Warm tungsten "
        "task lighting from the left rakes low across the copper and the wire "
        "loops, with cool daylight fill from a high window on the right; "
        "nothing emits its own light, no LEDs, no glow. Very shallow depth of "
        "field: the nearest three dies and their bond wires are razor sharp, "
        "the rear of the module and the bench fall into creamy bokeh. Real "
        "macro-lens bokeh, natural sensor noise, faint dust motes, fine film "
        "grain, slight chromatic aberration at frame edges, subtle vignette, "
        "framing slightly off-centre. Photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    with open("/home/chino/thesignal/.last_hero_prompt.txt", "a") as fh:
        fh.write(f"\n\n=== {SLUG} ATTEMPT {ATTEMPT} ===\n{prompt}\n")
    img = generate(prompt, OUTPUT)
    img = img.convert("RGB")
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 60:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
