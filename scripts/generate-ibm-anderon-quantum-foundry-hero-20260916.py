#!/usr/bin/env python3
"""Generate hero image for slug 'ibm-anderon-quantum-foundry-chips-award-2026'.

FAL flux/schnell, photo-realistic professional stock-photo style only.
Scene: semiconductor cleanroom fab floor (300mm quantum wafer fab), engineers in
white cleanroom suits handling a large reflective silicon wafer, gold-plated
cryostat hardware softly blurred in the background.

Deliberately DISTINCT from recent heroes: not a gold cryostat close-up (ionq),
not a TSMC wafer-carrier cleanroom framing, no data-center hallway, no abstract
/digital art, no neon/glowing lines/geometric patterns, no text of any kind.
"""

import os
import sys

import requests

SLUG = "ibm-anderon-quantum-foundry-chips-award-2026"
W, H = 1536, 864          # 16:9
PAD = 512                  # generate slightly larger, then center-crop to exact 16:9

OUTPUT1 = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
OUTPUT2 = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"

R2_URL = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/" + SLUG + ".jpg"

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no letters, "
    "no numbers, no codes, no serial numbers, no etched or engraved markings, "
    "no labels, no plaques, no nameplates, no decals, no stencils, no signage, "
    "no posters, no screens, no monitors, no displays, no laptops, no phones, "
    "no tablets, no user interfaces, no code, no dashboards, no whiteboards, "
    "no paper documents, no watermark, no captions, no logos, no brand names, "
    "no illustration, no digital art, no cartoon, no 3D render, no neon, "
    "no glowing lines, no geometric patterns, no holograms."
)

PROMPT = (
    "Professional stock photograph inside a modern semiconductor fabrication "
    "cleanroom. Two engineers wearing full white cleanroom bunny suits with "
    "hoods, face masks and gloves stand beside a wafer handling tool, carefully "
    "lifting and inspecting a large glossy 300 millimetre reflective silicon "
    "wafer with both gloved hands; the mirror-like wafer catches soft window "
    "and ceiling light and shows faint iridescent rainbow diffraction colours. "
    "Behind them, softly out of focus, a tall gold-plated cryogenic refrigerator "
    "with stacked polished copper plates and wafer-processing equipment with "
    "round loading ports fade into a busy fab floor receding into the distance. "
    "Bright brushed stainless steel and white epoxy surfaces, a highly "
    "reflective polished floor, cool blue-white cleanroom lighting with gentle "
    "atmospheric haze, clean and orderly, shallow depth of field with the wafer "
    "and the front engineer tack sharp and the background softly blurred, "
    "photo-realistic, photojournalistic industrial photography, natural "
    "imperfections, shot on a full-frame DSLR with an 85mm lens, high resolution. "
    + NO_TEXT
)


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as fh:
            for line in fh:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    break
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)


def generate():
    load_fal_key()
    import fal_client

    print("Generating hero image for '" + SLUG + "'...")
    print("Prompt: " + PROMPT[:160] + "...")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    print("Result keys: " + str(list(result.keys())))

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print("ERROR: Could not find image URL in result")
        print("Full result: " + str(result))
        sys.exit(1)

    print("Image URL: " + image_url)

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    return r.content


def fit_exact(data):
    """Center-crop / resize to exactly W x H, return (bytes, size)."""
    import io

    from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGB")
    print("   Generated dimensions: " + str(img.size))

    target_ratio = W / H
    w, h = img.size
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=92, optimize=True)
    if len(buf.getvalue()) < 10240:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=98, optimize=True)
    return buf.getvalue(), img.size


def main():
    raw = generate()
    data, size = fit_exact(raw)
    print("   Final dimensions: " + str(size))

    for outpath in (OUTPUT1, OUTPUT2):
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "wb") as fh:
            fh.write(data)
        print("Saved to " + outpath + " (" + str(len(data)) + " bytes)")


if __name__ == "__main__":
    main()
