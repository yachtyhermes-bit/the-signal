#!/usr/bin/env python3
"""Hero image for gfs-tsmc-interposer-supply-deal-2026 via fal flux/schnell.

Subject: GlobalFoundries (GFS) and TSMC's $2B, five-year silicon-interposer /
CoWoS advanced-packaging supply agreement (GF builds interposers for TSMC at
Malta, NY; first U.S. source of these interposers).

Frame: a semiconductor manufacturing / advanced-packaging scene about silicon
wafers — NOT a data center, NOT a server room, NOT a bare lithography tool.

Scene: a cleanroom technician in a full white bunny suit, hood, mask and
gloves holds a polished 300mm silicon wafer up to the light for inspection,
with advanced-packaging fab equipment softly out of focus behind.

Rules:
- PHOTO-REALISTIC editorial press photograph ONLY. Shallow depth of field,
  professional lighting, rich saturated darks, high dynamic range. 16:9.
- TEXT-FREE: all lettering, numerals, signage, lot codes and logos forbidden.
- NO neon/synthwave, NO glowing lines, NO abstract/geometric digital art, NO
  CGI look, NO data-center hallway or server aisle.

Usage: python3 scripts/gen-gfs-tsmc-interposer-hero-20261008.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = "gfs-tsmc-interposer-supply-deal-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080
SEED = 20261008

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no lot numbers, no serial numbers, no etched part markings, no "
    "wafer scribe lettering, no signage, no placards, no warning labels, no "
    "safety posters, no labels, no tags, no stickers, no decals, no painted "
    "markings on machinery, no words on push buttons or switches, no button "
    "lettering, no control-panel instructions, no machine nameplates, no "
    "data plates, no asset tags, no inventory stickers, no equipment "
    "identification plates, no illuminated indicator words, no brand names, "
    "no manufacturer names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no signatures, no barcodes, no QR codes, no "
    "data-matrix codes, no goggles with branded text, no graffiti, no "
    "handwriting, no documents, no clipboards with writing, no legible "
    "writing of any kind anywhere in the image. No silkscreen printing, no "
    "ink of any kind on any surface. Any display, monitor, HMI panel or "
    "machine readout is entirely blank, dark or softly out of focus with no "
    "readable content at all. Every surface, machine panel and wall is plain "
    "and unmarked, carrying no lettering, no numerals and no logos at all. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no artificial overlay "
    "graphics, no augmented-reality graphics, no wireframe, no charts, no "
    "graphs, no dashboards, no data visualisation, no screens full of data, "
    "no data center, no server room, no server racks, no server aisles, no "
    "cable runs, no GPU racks."
)

COMMON = (
    "Cool neutral white cleanroom lighting from recessed ceiling fixtures "
    "with softer ambient fill from the sides and rich deep shadow falloff, "
    "high dynamic range, shallow depth of field with real optical lens blur "
    "and creamy natural bokeh, honest available-light exposure, true colour, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "slight sensor softness in the shadows, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no retouched hyper-clean digital look, no "
    "3D visualisation, no digital illustration, an actual photograph taken on "
    "a real camera, not a rendering, handheld with a slightly imperfect "
    "framing, uneven corner illumination, faint chromatic fringing on "
    "high-contrast edges, photorealistic, very high detail, professional "
    "editorial stock photography, 16:9 landscape composition. "
)

PROMPT = (
    "Photo-realistic editorial press photograph, shot on an 85mm lens at "
    "f/2.0 on a full-frame camera, inside a sparkling semiconductor "
    "manufacturing cleanroom. Centred and tack sharp in the plane of focus, "
    "a cleanroom technician in a full white body bunny suit with an integral "
    "hood, face mask and white nitrile gloves stands at a stainless steel "
    "inspection bench and holds a single polished 300 millimetre silicon "
    "wafer up to the light with both hands, examining its reflective "
    "mirrored mirror-like surface as it catches a long soft specular "
    "highlight and reflects a faint iridescent rainbow sheen across its "
    "plain unpatterned face. The wafer's surface is a smooth uniform mirror "
    "with no printing, no scribe lettering, no die text and no logos "
    "anywhere. The technician is seen in three-quarter profile from the "
    "side, face partly turned away and partly hidden behind the wafer and "
    "the mask, unidentifiable, their suit plain and unmarked with no "
    "flashes, badges or patches. Behind and to either side of them, softly "
    "out of focus and rendered as gentle warm-grey shapes and creamy bokeh, "
    "advanced-packaging fab equipment recedes into haze: the pale grey and "
    "brushed stainless steel housings of wafer-handling and inspection tools "
    "with machined aluminium rails, small servo motors and neat bundles of "
    "translucent pneumatic tubing, and a partially open front-loading wafer "
    "pod with a fan of stacked wafers catching faint light. The glossy epoxy "
    "floor holds soft reflections of the ceiling lights and the stainless "
    "bench legs. Cool white light rakes across the top of the wafer from the "
    "upper right with deep shadow falloff into the background. Orderly, "
    "immaculate, quietly working industrial space with a faint haze of "
    "filtered air drifting through the frame. "
    + COMMON
    + NO_TEXT
)


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
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": SEED,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT).convert("RGB")
    print(f"Downloaded: {OUTPUT} size={img.size} bytes={len(r.content)}")

    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT} dimensions={img.size} bytes={size}")
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved higher quality: {os.path.getsize(OUTPUT)} bytes")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP} bytes={os.path.getsize(BACKUP)}")
    print("Done!")


if __name__ == "__main__":
    main()
