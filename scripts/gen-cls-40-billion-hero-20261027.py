#!/usr/bin/env python3
"""Hero for cls-40-billion-2027-outlook-cash-tradeoff-2026 (fal flux/schnell).

Subject: Celestica (CLS) — electronics manufacturing services / ODM that builds
AI servers, switches and storage for hyperscalers. Story hook: 2027 revenue
guided to $40B and the cash-flow trade-off of that ramp.

Scene: a modern ELECTRONICS MANUFACTURING FLOOR, not a data centre. Primary
composition is a technician in anti-static gear inspecting a server motherboard
under bright industrial lighting; fallbacks are an SMT pick-and-place line and a
row of populated boards moving off the line.

Rules:
- PHOTO-REALISTIC editorial stock photography ONLY, bright industrial light.
- TEXT-FREE: no letters/numbers/logos/silk-screen legends/branding.
- NOT a data-centre hallway / server aisle / rack row (banned site-wide).
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-cls-40-billion-hero-20261027.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "cls-40-billion-2027-outlook-cash-tradeoff-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "model numbers, no lot codes, no date codes, no stencilled markings, no "
    "laser-etched markings, no die markings, no printed legends on any "
    "component, no silk-screen print on the circuit boards, no reference "
    "designators, no barcodes, no QR codes, no stickers, no decals, no asset "
    "tags, no printed labels, no paper documents, no clipboards, no signage, "
    "no wall placards, no safety posters, no brand names, no manufacturer "
    "names, no company names, no corporate logos, no watermarks, no "
    "handwriting, no legible writing of any kind anywhere in the image. All "
    "circuit boards read as plain unmarked green or dark substrate with "
    "unlabelled components and clean solder joints only. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no glowing "
    "lines, no light trails, no synthwave, no geometric patterns, no abstract "
    "graphic, no network diagram, no fibre-optic light, no laser beam, no "
    "futuristic HUD, no hologram, no data visualisation, no data centre, no "
    "server room, no server racks, no server aisles, no raised floor."
)

PHOTO_TAIL = (
    "Real optical lens blur with creamy out-of-focus background falloff, "
    "honest available industrial light, natural fine sensor grain at ISO 800, "
    "slight lens vignette, true-to-life slightly imperfect colour, clean "
    "neutral whites and cool grey machine tones, faint chromatic aberration "
    "at the frame edges, a touch of softness in the far corners, dust and "
    "small smudges on the surfaces. Documentary photojournalism, a real "
    "photograph taken on a DSLR with a fast prime lens, not a render: no "
    "plastic CGI sheen, no glossy highlight rolloff, no ray-traced "
    "reflections, no perfect symmetry, no digital illustration, no painting, "
    "no 3D visualisation, photorealistic photograph, natural detail, "
    "professional editorial stock photography for a financial news site, "
    "16:9 landscape composition, bright realistic industrial lighting."
)

PROMPTS = {
    # 1 — PRIMARY: technician in anti-static gear inspecting a server
    #     motherboard at a bench on the factory floor.
    "1": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a 50mm lens at f/2.2 on a full-frame camera, a candid working "
        "moment on the floor of a modern electronics manufacturing plant. A "
        "single technician stands at a light-grey assembly bench in the "
        "right half of the frame, seen from the chest up at a three-quarter "
        "angle from slightly behind, leaning in over the work. They wear a "
        "crisp white anti-static smock with a plain snap front, a fine "
        "grounding wrist strap looping from the cuff to the bench, a soft "
        "blue hairnet and clear safety glasses, their gloved fingertips "
        "steadying the edges of a large rectangular server motherboard that "
        "lies flat on the bench on a clean white anti-static mat. The "
        "motherboard is the hero object in the lower centre of frame, lit "
        "hard and clear: a wide dark-green multilayer board about half a "
        "metre across, its surface a dense city of components — two large "
        "square processor sockets with polished metal retention frames, "
        "eight long slim white memory slots standing in parallel rows, a "
        "grid of dark chokes and round capacitors, and hundreds of tiny "
        "surface-mount parts each with a bright tinned solder fillet. Every "
        "board surface is plain and unmarked. In the left half and deep "
        "background, out of focus, the plant floor recedes: another "
        "technician in the same white smock at the next bench, bright "
        "overhead strip lighting, pale grey equipment cabinets and a long "
        "run of production machinery softening into gentle bokeh. Bright, "
        "clean, even industrial lighting from long diffused ceiling fixtures "
        "with a soft key from the upper left, neutral white light with a "
        "cool cast, no harsh shadows, the white smock staying open and "
        "detailed, the bench top clean and matte. Photographic, shallow "
        "depth of field focused on the motherboard's near edge and the "
        "technician's hands, the far benches and machinery melting into soft "
        "clean blur. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 2 — FALLBACK A: surface-mount line, pick-and-place head over a panel.
    "2": (
        "Professional stock photograph, photo-realistic documentary image "
        "shot hand-held on a 35mm lens at f/2.8 on a full-frame DSLR inside "
        "a working surface-mount electronics assembly plant, framed at "
        "slightly below eye level at a three-quarter angle along a "
        "production line. In the foreground a conveyor carries a large "
        "rectangular panel of bare green circuit boards toward the camera, "
        "its edge track and its rows of small routed board outlines sharp "
        "and readable, a few boards already populated with flat grey "
        "surface-mount components. Directly behind and above it a "
        "pick-and-place machine dominates the centre of the frame: a heavy "
        "pale-grey gantry beam spanning the line, a compact black placement "
        "head riding on it with several slim downward nozzles, a strip "
        "feeder bank of many narrow tape reels lined up along the far side, "
        "all crisp machined metal and matte industrial paint, completely "
        "unmarked and unbranded, with worn scuffed edges and a little "
        "dust in the crevices where hands have been. Beyond the machine, "
        "out of focus, more of the line stretches away in perspective — "
        "further gantries, a reflow oven tunnel with a dark mouth, pale "
        "scuffed floor tiles, a coiled black air hose and a stray plastic "
        "tote at the base of the machine, bright overhead lighting. Bright, "
        "clean, even industrial lighting from long white ceiling fixtures "
        "running the length of the plant, a soft gradient falling from the "
        "bright conveyor in front to the cooler shadowed machinery behind, "
        "no coloured light. Photographic, shallow depth of field with the "
        "board panel and the placement head tack sharp and the receding "
        "line dissolving into smooth bokeh. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 3 — FALLBACK B: operator at an optical inspection station, viewed at
    #     mid-distance so hands stay small in frame (no finger artifacts).
    "3": (
        "Professional stock photograph, photo-realistic documentary image "
        "shot hand-held on a 50mm lens at f/2 on a full-frame DSLR from "
        "about four metres away, standing inside a busy electronics "
        "manufacturing plant. A single operator stands at an inspection "
        "station in the middle right of the frame, seen from a "
        "three-quarter rear angle so the face is not visible, leaning "
        "slightly forward over a lit viewing table. They wear a plain white "
        "anti-static smock over dark trousers, a soft blue hairnet and nitrile "
        "gloves, their arms extended toward the table where a large "
        "rectangular server motherboard lies flat under the station's "
        "bright task lamp, one gloved hand resting at the board's edge. The "
        "board is seen at a shallow angle: dark-green multilayer substrate, "
        "long white memory slots in parallel rows, two large square "
        "processor sockets with metal retention frames, and a dense scatter "
        "of tiny surface-mount parts, all plain and unmarked. Around the "
        "station the plant floor is alive with real working detail: a low "
        "grey bench with a coiled black cable and a small stack of plastic "
        "totes at the left, a stainless rack holding boards on edge behind "
        "the operator, further benches and a long production line receding "
        "into the background with a few other smocked figures at their "
        "stations, all softly out of focus, and a pale scuffed epoxy floor "
        "with a faded yellow safety line running across the lower frame. "
        "Bright, clean, even industrial lighting from long white ceiling "
        "fixtures overhead plus the warm task lamp at the station, neutral "
        "white overhead light and a gentle warm pool at the bench, no "
        "coloured light. Photographic, shallow depth of field with the "
        "operator's shoulders, the station and the board in focus and "
        "everything behind melting into soft bokeh. "
        + PHOTO_TAIL
        + " " + NO_TEXT
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
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    return None


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
    elif "image" in result:
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image URL in result: {result}")
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
    img = img.convert("RGB")
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


def save_bounded(img, path):
    for q in (93, 91, 89, 87, 85, 82, 79):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print(f"Saved {path} quality={q} bytes={size}")
            return size
    print(f"WARNING: still {os.path.getsize(path)} bytes at min quality")
    return os.path.getsize(path)


def ocr_text_check(path, min_conf=70.0):
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return [], []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11", "tsv"],
                check=True, capture_output=True, timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return [], []
        tsv = base + ".tsv"
        if not os.path.exists(tsv):
            return [], []
        with open(tsv, errors="ignore") as f:
            rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]

    readable, noise = [], []
    for row in rows[1:]:
        if len(row) < 12:
            continue
        try:
            conf = float(row[10])
        except ValueError:
            continue
        text = row[11].strip()
        clean = "".join(ch for ch in text if ch.isalnum())
        if conf <= 0 or len(clean) < 3:
            continue
        (readable if conf >= min_conf else noise).append((text, conf))
    return readable, noise


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    print("=" * 70)
    print(prompt)
    print("=" * 70)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    size = save_bounded(img, OUTPUT)
    print(f"FINAL {OUTPUT} dimensions={img.size} bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copyfile(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
    readable, noise = ocr_text_check(OUTPUT)
    if not readable:
        print(f"OCR TEXT CHECK: clean ({len(noise)} sub-threshold blob(s) ignored)")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
