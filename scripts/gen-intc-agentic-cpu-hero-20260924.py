#!/usr/bin/env python3
"""Generate a hero image for 'intc-agentic-cpu-14a-wildcard-2026' using FAL flux/schnell.

Scene brief: macro product photograph of a bare, unmarked microprocessor chip held
between the gloved fingertips of a technician's hand above a dark anti-static work mat.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-intc-agentic-cpu-hero-20260924.py
"""

import os
import sys
import hashlib
import requests

SLUG = "intc-agentic-cpu-14a-wildcard-2026"

# Generate at 16:9, then finalise to 1920x1080 (cover-resize + centre-crop)
GEN_W, GEN_H = 1440, 810
W, H = 1920, 1080

OUTPUT1 = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
OUTPUT2 = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

# --- Prompt variants (reworked per attempt if the previous render was garbled
# --- or contained any text / markings) -----------------------------------------

PROMPT_1 = (
    "Extreme macro product photograph. A single bare square microprocessor chip — a plain, "
    "unmarked square of polished dark grey silicon with a smooth brushed metal heat spreader, "
    "completely featureless, no printing of any kind — held gently between the powder-free "
    "nitrile-gloved fingertips of a technician's hand, suspended a few centimetres above a matte "
    "dark charcoal anti-static work mat. A pair of fine stainless-steel precision tweezers and a "
    "second identical bare chip rest on the mat below, thrown heavily out of focus. "
    "Dramatic low raking side light from the left carves a bright rim along the chip edge, deep "
    "black shadows, cool neutral desaturated tones, faint steel-blue highlights on the silicon. "
    "Very shallow depth of field, 100mm macro lens at f/2.8, pin-sharp focus on the chip surface, "
    "the background falling away into darkness. Photo-realistic editorial documentary photography, "
    "high detail, natural grain, shot on full-frame DSLR. The chip is the hero of the frame and "
    "fills the centre of the composition. "
    "Absolutely no text, letters, words, numbers, symbols, serial numbers, part numbers, model "
    "numbers, QR codes, barcodes, logos, brand names, trademarks, labels or printed markings "
    "anywhere in the image — the chip surface is entirely blank; no screens, monitors or displays "
    "in frame."
)

PROMPT_2 = (
    "Photorealistic macro photograph of an unmarked blank microprocessor chip held in a gloved "
    "hand. The chip is a perfectly smooth, featureless, uniform dark grey square with a clean "
    "pristine surface — a completely plain object, like a polished blank tile, with absolutely "
    "nothing printed, stamped, etched, engraved or written on it. Two plain gloved fingertips "
    "pinch the chip by its edges. Behind it there is only darkness and a smooth, seamless, "
    "untextured matte black rubber work surface. Hard raking light rakes across the silicon from "
    "one side, carving a bright edge highlight, while the rest of the frame falls into deep "
    "shadow. Cold neutral palette, grey and black only. 100mm macro lens, f/2.8, extreme shallow "
    "depth of field, realistic photographic grain, editorial product photography captured on a "
    "camera. The scene is minimal and clean: one chip, one hand, one plain dark surface. "
    "There is no writing anywhere in this picture: no letters, no characters, no digits, no "
    "numbers, no codes, no model identifiers, no serial numbers, no logos, no brand names, no "
    "labels, no labels on the surface, no signage, no screens. Every surface is blank."
)

PROMPT_3 = (
    "Photorealistic macro photograph of a single blank unmarked microprocessor chip held up "
    "between the gloved fingertips of a technician's hand, a few centimetres above a smooth "
    "matte dark grey anti-static work mat. The chip is a plain featureless square of dark grey "
    "silicon and metal — a completely smooth, uniform, pristine surface with nothing whatsoever "
    "printed, stamped, engraved or written on it, no markings at all. In the blurred background, "
    "far out of focus and mostly lost in shadow, a pair of small steel precision tweezers and a "
    "second plain blank chip lie flat on the mat. Strong single-source raking side light, long "
    "deep shadows, cool neutral grey tones, muted and moody. Shot on a 100mm macro lens at f/2.8 "
    "with extreme shallow depth of field: the chip in the hand is tack sharp, the mat behind "
    "melts into darkness. Authentic documentary photography, realistic optical detail, subtle "
    "sensor grain, not a render, not an illustration. The chip is the hero of the frame. "
    "No writing anywhere in this image: no letters, no words, no characters, no digits, no "
    "numbers, no serial numbers, no part numbers, no QR codes, no barcodes, no logos, no brand "
    "names, no labels, no printed markings, no signage, no screens, no monitors. Every surface "
    "is blank and unbranded."
)

PROMPTS = {1: PROMPT_1, 2: PROMPT_2, 3: PROMPT_3}


def load_fal_key():
    """Copy of the proven block from gen-intc-hero.py."""
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    break
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)


def finalise(raw_bytes, output_path):
    """Save raw image, cover-resize to 1920x1080 and centre-crop."""
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    print(f"   FAL returned: {img.size}")

    # Cover-resize (preserve aspect) so both sides >= target, then centre-crop.
    src_w, src_h = img.size
    scale = max(W / src_w, H / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    if (new_w, new_h) != (src_w, src_h):
        img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    img = img.crop((left, top, left + W, top + H))
    print(f"   Finalised to: {img.size} (centre-crop from {new_w}x{new_h})")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=92, optimize=True)

    file_size = os.path.getsize(output_path)
    print(f"   Saved {output_path} — {file_size} bytes ({file_size/1024:.1f} KB)")

    if file_size < 10240:
        print("   File too small, re-saving at quality 98...")
        img.save(output_path, "JPEG", quality=98, optimize=True)
        file_size = os.path.getsize(output_path)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    return img.size


def main():
    import fal_client

    attempt = int(os.environ.get("ATTEMPT", "1"))
    if attempt not in PROMPTS:
        print(f"ERROR: unsupported ATTEMPT={attempt} (expected 1-3)")
        sys.exit(1)
    prompt = PROMPTS[attempt]

    load_fal_key()

    print(f"Generating hero image for '{SLUG}' (ATTEMPT={attempt})...")
    print(f"Prompt: {prompt}")

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {
                "width": GEN_W,
                "height": GEN_H,
            },
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    print(f"Result keys: {list(result.keys())}")

    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print("ERROR: Could not find image URL in result")
        print(f"Full result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    print("Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    raw = r.content

    # Save to BOTH locations (identical bytes: same finalise pipeline twice)
    for output_path in [OUTPUT1, OUTPUT2]:
        finalise(raw, output_path)

    print("\nLocal saves complete!")

    md5 = hashlib.md5(open(OUTPUT1, "rb").read()).hexdigest()
    md5_b = hashlib.md5(open(OUTPUT2, "rb").read()).hexdigest()
    print(f"   md5 {OUTPUT1}: {md5}")
    print(f"   md5 {OUTPUT2}: {md5_b}")
    if md5 != md5_b:
        print("   WARNING: copies differ!")

    print(f"\nDone. R2 URL will be: {R2_URL}")


if __name__ == "__main__":
    main()
