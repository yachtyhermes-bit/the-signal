#!/usr/bin/env python3
"""Regenerate hero for lrcx-ai-memory-3d-stacking-moat-2026 (fal flux/schnell).

Subject: Lam Research (LRCX) — a semiconductor plasma-etch and deposition
process-equipment maker. The AI/memory 3D-stacking moat comes from the fact
that stacking HBM/3D NAND dies requires extreme etch/deposition precision.

Scene chosen: an extreme macro view of the reflective, iridescent surface of a
bare 300mm silicon wafer held by the smooth metal end-effector of a robotic
vacuum wafer-handling arm inside a fab tool load-port — abstract rainbow
diffraction across the fine grid of dies, cool blue-violet industrial light,
blurred plain polished-aluminium machine surfaces around, very shallow depth
of field. Deliberately NOT the "person in a bunny suit holding a wafer"
composition (already used for QCOM) and NOT a radar (LMT).

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- Machine bodies plain/scraped of any marking so no brand text can render.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/regen-lrcx-hero-20260910.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "lrcx-ai-memory-3d-stacking-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
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
    "walls, no laptops, no phones, no tablets, no keyboards with writing, no "
    "UI, no computer interfaces, no code, no dashboards, no whiteboards with "
    "writing, no paper documents, no notebooks, no books with titles, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, no "
    "3D render, no neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Extreme close-up macro stock photograph of the polished iridescent "
        "mirror surface of a bare 300 millimetre silicon wafer, held from "
        "beneath by the smooth rounded metal end-effector of a robotic vacuum "
        "wafer-handling arm inside the load-port of a semiconductor process "
        "tool: the wafer's flawless reflective face fills most of the frame "
        "and shows soft abstract rainbow diffraction — faint bands of cyan, "
        "violet and pale gold — gliding across its ultra-fine grid of "
        "countless rectangular integrated-circuit dies, all without any "
        "printed marking, while the smooth plain brushed-aluminium blade of "
        "the robot arm curves in from one edge, softly out of focus, "
        "surrounded by blurred plain polished-aluminium machine surfaces of "
        "the tool body with no panel seams visible, cool blue-violet "
        "industrial cleanroom lighting and hints of soft teal reflections, "
        "extremely shallow depth of field with only a band of the wafer "
        "surface crisply sharp and everything else melting into soft bokeh, "
        "crisp macro detail, photorealistic, high detail, professional "
        "industrial product photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic macro industrial photograph looking across the "
        "glossy surface of a bare polished silicon wafer at a shallow raking "
        "angle, held suspended by the rounded smooth tip of a robotic vacuum "
        "wafer-handling arm inside a semiconductor fab tool: the wafer face "
        "is a perfect mirror with subtle oil-slick iridescence — faint "
        "pastel rainbow sheen of rose, cyan and violet — rippling gently "
        "over the faint regular grid of microchip dies, every die completely "
        "plain and unmarked, the plain unmachined brushed metal end-effector "
        "blurred softly in the foreground, cool blue-white cleanroom task "
        "lighting above with soft industrial blue shadows, the surrounding "
        "polished aluminium tool chamber walls rendered as smooth blurred "
        "panels of grey metal, very shallow depth of field with the wafer "
        "edge and dies sharply resolved and the background dissolved into "
        "smooth out-of-focus aluminium bokeh, photorealistic, high detail, "
        "professional lighting, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Photorealistic extreme macro shot of the silvery mirrored surface of "
        "a bare 300mm silicon wafer inside a semiconductor deposition and "
        "etch tool, the wafer resting on a smooth plain metal lift-pin and "
        "end-effector, seen so close that the faint microscopic lattice of "
        "individual circuit dies forms a delicate unmarked honeycomb grid "
        "across the frame, thin-film interference producing soft shifting "
        "rainbow hues of pale violet, cyan and warm silver drifting over the "
        "surface, cool blue-violet industrial lighting grazing in from the "
        "left with soft reflections of plain polished machine metal around, "
        "everything beyond the focal plane melting into smooth grey "
        "aluminium bokeh, extremely shallow depth of field, crisp tack-sharp "
        "macro detail on the silicon surface, photorealistic, high detail, "
        "professional industrial photography, 16:9 landscape composition. "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
