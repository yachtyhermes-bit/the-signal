#!/usr/bin/env python3
"""Generate hero for ionq-superion-256-quantum-foundry-2026 (fal flux/schnell).

Subject: IonQ (NYSE: IONQ) — quantum computing hardware. IonQ now owns a
semiconductor foundry (SkyWater) and fabricates its own 256-qubit trapped-ion
quantum processing units — vertical integration, building quantum computers
like chips.

Scene (mandatory, chosen subject): a QUANTUM COMPUTING LABORATORY — a tall
multi-stage dilution refrigerator (cryostat) with gold/copper-plated circular
plates stacked vertically, fine wire looms and copper shielding, standing in a
clean research lab under cool blue-white machine lighting. Close framing so the
stacked circular gold plates and delicate wiring read clearly. Shallow depth
of field, professional cinematographic lighting, 16:9 landscape.

Visually distinct from recent heroes (rocket pad, radar, chip-fab cleanroom,
jet engine line, fintech office, container port, data-center aisles, neon
abstract) — this is quantum cryogenic hardware in a research lab.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- All surfaces plain/smooth so no text renders.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/generate-ionq-superion-256-hero-20260911.py
    ATTEMPT=2 MODEL=fal-ai/flux/dev ...   # fallback to the other FAL model
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ionq-superion-256-quantum-foundry-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
MODEL = os.environ.get("MODEL", "fal-ai/flux/schnell")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no "
    "letters, no numbers, no codes, no serial numbers, no etched or engraved "
    "markings, no labels, no plaques, no nameplates, no decals, no stencils, "
    "no stenciled writing, no markings of any kind, no logos, no brand names, "
    "no signage, no posters, no screens, no monitors, no displays, no video "
    "walls, no laptops, no phones, no tablets, no UI, no computer interfaces, "
    "no code, no dashboards, no whiteboards with writing, no paper documents, "
    "no notebooks, no books with titles, no watermark, no captions, no "
    "illustration, no digital art, no cartoon, no 3D render, no neon, no "
    "glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a large gold-plated dilution "
        "refrigerator cryostat standing in a bright clean research "
        "laboratory, a tall vertical stack of gleaming circular copper and "
        "gold-plated plates connected by thick vertical rods and dense "
        "delicate wire looms and fine ribbon cables cascading between the "
        "discs, polished copper radiation shielding rings around each stage, "
        "the whole tall golden instrument finely machined and completely "
        "plain and unmarked, cool blue-white machine lighting glancing off "
        "the polished metal surfaces, deep soft shadows between the plates, "
        "a smooth unmarked white lab wall and a blurred instrument frame in "
        "the far background, shallow depth of field with the cryostat "
        "sharply in focus and the background softly blurred, atmospheric "
        "clean-room haze, professional cinematographic lighting, "
        "photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic close-up stock photograph of a golden ion-trap "
        "quantum computer chip mounted on a polished wafer stage inside a "
        "research laboratory, the small square chip machined from gold and "
        "copper with a fine grid of delicate micro-scale electrodes and "
        "hair-thin wire bonds catching soft light, held in a precision "
        "machined copper mount with layered gold shielding plates, "
        "surrounded by thin cabling and small polished metal components, "
        "the metal surfaces smooth plain and completely unmarked, cool "
        "blue-white laboratory lighting with warm gold reflections along "
        "the polished edges, a softly blurred clean lab bench and instrument "
        "rack far behind, extreme shallow depth of field with the chip "
        "sharply in focus, photorealistic macro detail, professional "
        "cinematographic lighting, 16:9 landscape composition. "
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


def generate(prompt, out_path, model=MODEL):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print(f"Generating image with {model}...")
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "enable_safety_checker": False,
    }
    if "schnell" in model:
        args["num_inference_steps"] = 4
    result = fal_client.subscribe(model, arguments=args)
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
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} MODEL={MODEL}")
    img = generate(prompt, OUTPUT)
    img = img.convert("RGB")
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
