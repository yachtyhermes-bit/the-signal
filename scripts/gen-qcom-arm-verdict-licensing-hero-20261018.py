#!/usr/bin/env python3
"""Generate hero for qcom-arm-verdict-licensing-2026 (fal flux/schnell).

Subject: Delaware jury verdict (Oct 13, 2026) finding Arm breached its
architecture licence agreement with Qualcomm. Story = smartphone application
processor architecture, licensing royalties, who controls the instruction set.

Scene: macro photograph on a technician's workbench — an opened smartphone
showing its exposed logic board, with a single application-processor chip held
in fine tweezers just above the board. Warm neutral workshop tones.

Deliberately DISTINCT from recent heroes: no data-center hallway / server
aisle, no plain wafer close-up, no bunny-suited technician holding a wafer,
no sealed chip package still-life on a metal tray.

Rules: PHOTO-REALISTIC stock photograph only; no digital art / neon / glowing
lines / geometric patterns / text. Generate 1440x810, finalize 1920x1080
center-crop JPEG q92, mirror to _backup_dist.

Usage:
  SLUG=qcom-arm-verdict-licensing-2026 ATTEMPT=1 \
    /home/chino/video-venv/bin/python3 scripts/gen-qcom-arm-verdict-licensing-hero-20261018.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "qcom-arm-verdict-licensing-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no digits, no part numbers, no serial numbers, no lot "
    "codes, no batch codes, no date codes, no QR codes, no barcodes, no "
    "datamatrix codes, no silkscreen printing, no etched markings, no labels, "
    "no stickers, no tags, no painted markings, no stamped symbols, no brand "
    "names, no manufacturer names, no product names, no logos, no "
    "trademarks, no watermark, no signature, no caption, no ruler or "
    "measurement graduations, no letter-like or typography-like markings of "
    "any kind anywhere in the image. The chip, the tweezers, the circuit "
    "board and every surface in the frame are plain and unmarked. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no futuristic HUD graphics, no overlay elements, no augmented-reality "
    "graphics, no server rack, no server aisle, no data-center hallway."
)

PROMPTS = {
    "1": (
        "Photo-realistic macro stock photograph shot on a repair technician's "
        "workbench, professional editorial photography. An opened smartphone "
        "lies flat on a warm-toned wooden bench mat, its back cover removed to "
        "expose a densely populated green-grey logic board with rows of tiny "
        "surface-mount components, shield cans and a ribbon cable trailing "
        "softly out of focus. Directly above the board, held in a pair of slim "
        "stainless-steel precision tweezers, is a single square application-"
        "processor package — a small dark ceramic chip with a mirrored metal "
        "lid catching a soft sheen — angled slightly toward the camera as if "
        "about to be set into its socket. Warm neutral workshop lighting: a "
        "soft key light from the upper left and a faint amber practical glow "
        "from a bench lamp at the right edge. Extremely shallow depth of field "
        "from a macro lens at f/2.8: the chip, the tweezer tips and the "
        "nearest few components are tack sharp with honest micro-texture, "
        "while the rest of the handset and the bench melt into creamy bokeh. "
        "Real optical blur, natural fine sensor grain, subtle lens vignette, "
        "slightly imperfect handheld framing, honest exposure, no plastic "
        "sheen, no perfect symmetry. Photorealistic, very high detail, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched close-up photograph taken in a phone repair "
        "workshop — visibly a real camera photograph, not a render and not "
        "computer generated. A disassembled handset sits on a worn warm-grey "
        "anti-static bench mat, its glass and frame pushed aside, revealing "
        "the exposed circuit board inside: layered metal shields, hair-thin "
        "copper traces and an array of minuscule capacitors and resistors. A "
        "technician's fine steel tweezers enter from the upper right, pinching "
        "one corner of a small square processor die lifted just a centimetre "
        "above its empty socket on the board. The die is dark with a thin "
        "polished metallic rim. Warm neutral workshop colour grade: tungsten "
        "bench light from the left, soft bounce fill, a gentle warm highlight "
        "on the tweezers. Macro lens shallow focus — chip and tweezers sharp, "
        "board falling quickly into soft bokeh; a little fine dust on the mat, "
        "faint haze, natural grain, slight chromatic fringing on the metal "
        "edges, minor vignette. Imperfect honest composition. Photorealistic, "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A professional editorial stock photograph, macro, shot from a low "
        "three-quarter angle across a technician's workbench: an opened "
        "smartphone chassis rests on a warm brown bench surface with a few "
        "softly blurred tools behind it, and beside it a single application-"
        "processor chip is suspended in fine stainless tweezers, hovering a "
        "few millimetres above the exposed logic board where it belongs. The "
        "board reads as real electronics — protected by metal shield cans, "
        "studded with tiny components, its solder joints catching pinpricks of "
        "warm light. Warm neutral workshop tones: honey-amber bench lamp key "
        "light, cool soft fill from a window, gentle shadow falloff. Very "
        "shallow depth of field, chip and tweezer tips tack sharp, the rest "
        "creamy bokeh; real optical blur, natural fine grain, honest exposure, "
        "subtle vignette, faint airborne dust. No glossy CGI sheen, no perfect "
        "symmetry. Photorealistic, very high detail, 16:9 landscape "
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
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size) + "  bytes=" + str(len(r.content)))
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
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.convert("RGB").save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: " + OUTPUT + "  dimensions=" + str(img.size) + "  bytes=" + str(size))
    if size < 51200:
        img.convert("RGB").save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT)) + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.convert("RGB").save(BACKUP, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + BACKUP)


if __name__ == "__main__":
    main()
