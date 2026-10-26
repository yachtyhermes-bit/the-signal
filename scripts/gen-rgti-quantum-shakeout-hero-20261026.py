#!/usr/bin/env python3
"""Generate hero for rgti-quantum-shakeout-government-backstop-2026 (fal flux/schnell).

Subject: Rigetti Computing (RGTI) and the quantum-computing stock shakeout as
Washington weighs a government backstop for the sector.

Scene (mandatory): a real quantum computing laboratory built around a large
gold-plated DILUTION REFRIGERATOR — the chandelier-style cryostat with stacked
gold circular plates and dense silver coaxial cabling — with an engineer's
gloved hand / laptop in frame for scale, cold blue-white lab light.

Banned: data centre corridor, server aisle, rack rows, neon/synthwave, glowing
lines, geometric patterns, digital art, CGI, text/logos/watermarks anywhere.

HARD CAP: 3 FAL generations. Prompts 1-3 below.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 \
        scripts/gen-rgti-quantum-shakeout-hero-20261026.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "rgti-quantum-shakeout-government-backstop-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
MODEL = "fal-ai/flux/schnell"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
RAW = f"/home/chino/thesignal/tmp/{SLUG}-raw-attempt{ATTEMPT}.jpg"
W, H = 1536, 864
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no words, no "
    "numbers, no part numbers, no serial numbers, no stencilled markings, no "
    "equipment nameplates, no asset tags, no warning signs, no safety posters, "
    "no bench labels, no cabinet labels, no barcode labels, no whiteboard "
    "writing, no printed paper, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no watermarks, no "
    "stickers, no decals, no QR codes, no handwriting anywhere in the image. "
    "The laptop screen is turned away from the lens or shows only a plain "
    "featureless glow with no readable interface. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no synthwave, no glowing "
    "lines, no light trails, no geometric patterns, no circuit-board graphic "
    "overlay, no network diagram, no graph, no futuristic HUD graphics, no "
    "hologram, no overlay elements. No data center, no server room, no server "
    "racks, no server aisles, no blinking rack lights."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light laboratory exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no perfect "
    "symmetry, no 3D visualisation, no digital illustration, no painting, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — PRIMARY: full chandelier cryostat, three-quarter wide, engineer's
    #     gloved hand at the frame for scale, laptop on bench in foreground.
    "1": (
        "Professional stock photograph of a dilution refrigerator in a quantum "
        "computing laboratory. A real photograph, not a render. The subject "
        "fills the centre of the frame: a large chandelier-style cryostat "
        "hanging from a heavy aluminium support frame, built as a vertical "
        "stack of six circular gold-plated copper plates of decreasing "
        "diameter, the widest at the top and tapering down to a small gold "
        "mixing chamber at the bottom, each plate mirror-bright polished gold "
        "with visible machined edges and mounting holes. Between the plates "
        "hundreds of fine silver coaxial cables hang in dense vertical looms, "
        "gathered into braided bundles and gently draping from stage to stage, "
        "catching thin specular highlights, with thin stainless rods and "
        "brass fittings joining the plates. The cryostat is enclosed at the "
        "top by a brushed stainless vacuum can flange and a ring of ports. To "
        "the right of the frame, at waist height, a researcher in a plain "
        "white lab coat and pale blue nitrile gloves reaches in and rests one "
        "gloved hand flat on the support frame's rail, giving human scale "
        "against the cryostat; only the hand, forearm and edge of the coat "
        "are in frame, the person's body cropped away. In the near foreground "
        "left, slightly out of focus, an open laptop sits on a stainless "
        "laboratory bench beside a coil of spare coax, its screen angled away "
        "from the camera. The lighting is the lab's own cold blue-white "
        "fluorescent and LED ceiling light: flat, clinical, bright, with a "
        "soft falloff into the corners and honest specular glints on the gold "
        "plates and silver braid. Behind the cryostat the room reads as a "
        "working lab — pale grey walls, a stainless optical table edge, a "
        "rack of plain unmarked instrument boxes, cable trays overhead — all "
        "softened into gentle blur by the shallow depth of field. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 2 — FALLBACK A: lower three-quarter angle, closer, plates and cable
    #     looms dominant, two gloved hands adjusting a coax connector, laptop
    #     glowing softly at the lower right.
    "2": (
        "Professional stock photograph, a real documentary photograph shot on "
        "an 85mm lens at f/2.2 inside a quantum computing laboratory, framed "
        "from slightly below and to the left of a dilution refrigerator. The "
        "cryostat dominates the right two-thirds of the frame, seen in "
        "three-quarter view from just under plate level so the stacked gold "
        "circular plates recede upward in a strong repeating rhythm: six "
        "polished gold-plated copper plates, each a machined disc with a "
        "rolled edge, separated by stainless spacers, the underside of the "
        "nearest plate throwing a soft warm reflection onto the one below. "
        "Dense looms of fine silver coaxial cable pour down between the "
        "plates in hundreds of strands, bundled with pale thread ties and "
        "fanning out into small gold connector blocks at each stage, some "
        "strands catching the light as thin bright lines. At the lower left, "
        "a pair of hands in pale blue nitrile gloves work at one of the "
        "connector blocks, one thumb steadying a plate edge while the other "
        "hand seats a coax connector; plain white lab coat cuffs at the "
        "wrists, the rest of the person out of frame. In the lower right "
        "corner, out of focus on a stainless bench, an open laptop throws a "
        "soft pale glow upward onto the underside of the lowest plate, its "
        "screen turned away from the camera. Cold blue-white overhead "
        "laboratory lighting from broad ceiling panels rakes down through the "
        "cable looms, leaving deep cool shadows between the plates, with the "
        "gold reading warm against the blue-white room. The background is a "
        "clean research lab in soft bokeh: pale grey wall panels, the dull "
        "stainless mass of a vacuum pump, a cable tray, an unmarked "
        "instrument chassis, nothing readable. Photographic, shallow depth of "
        "field with the nearest plate edge, the silver braid and the gloved "
        "hands tack sharp and the upper stages and room melting into blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 3 — FALLBACK B: macro of the superconducting quantum processor chip in
    #     its gold sample holder, wirebonded, lab background.
    "3": (
        "Professional stock photograph, a real macro photograph shot on a "
        "100mm macro lens at f/2.8 on a full-frame camera inside a quantum "
        "computing laboratory. Extreme close view of a superconducting "
        "quantum processor chip mounted in its sample holder: a square "
        "silicon die about five millimetres across, its surface a precise "
        "grid of machined aluminium resonator and qubit structures in pale "
        "silver on dark blue-grey silicon, sitting in a recessed pocket of a "
        "solid gold-plated copper block with a machined bevelled lip. Fine "
        "gold wirebonds arc in neat parallel rows from the chip's bond pads "
        "out to the surrounding gold circuit traces, each wire a bright thin "
        "curve catching the light, dozens of them on all four sides, with "
        "small silver connector launchers bolted to the block at the frame "
        "edges. The gold block is heavy, brushed and polished in places, "
        "showing honest tool marks, tiny handling scratches and the faint "
        "matte bloom of a used part. One fingertip in a pale blue nitrile "
        "glove rests at the extreme lower right edge of the frame, just "
        "touching the block's corner, out of focus, giving scale. The "
        "lighting is cool blue-white laboratory light from above and slightly "
        "behind, raking across the chip so the fine structures throw micro "
        "shadows and the gold traces flare with soft warm highlights, while "
        "the recess stays in cool shadow. Behind the block, thrown far out of "
        "focus, the pale grey and stainless shapes of the lab fade into "
        "creamy bokeh: the base of a gold plate, a coil of coax, the edge of "
        "an optical bench, nothing readable. Photographic, extremely shallow "
        "depth of field: the chip surface, the wirebond arcs and the near "
        "bevelled lip of the block tack sharp, the room dissolving. "
        + PHOTO_TAIL
        + " "
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
    print(f"Generating image with {MODEL}...")
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
    result = fal_client.subscribe(MODEL, arguments=args)
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
    print(f"Downloaded raw: {out_path}  size={img.size}  bytes={len(r.content)}")
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
    img = img.convert("RGB")
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


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
        tsv_path = base + ".tsv"
        if not os.path.exists(tsv_path):
            return [], []
        with open(tsv_path, errors="ignore") as f:
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
        if conf >= min_conf:
            readable.append((text, conf))
        else:
            noise.append((text, conf))
    return readable, noise


def finalize(img, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(out_path)
    if size < 204800:
        img.save(out_path, "JPEG", quality=98, optimize=True)
        size = os.path.getsize(out_path)
    return size


def main():
    if os.environ.get("CHECK_ONLY") == "1":
        for p in (OUTPUT, BACKUP):
            if not os.path.exists(p):
                print(f"ERROR: missing {p}")
                sys.exit(1)
            v = Image.open(p)
            print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
        readable, noise = ocr_text_check(OUTPUT)
        if not readable:
            print(f"OCR TEXT CHECK: clean ({len(noise)} sub-threshold blob(s))")
        else:
            print(f"OCR TEXT CHECK: WARNING {len(readable)} token(s): {readable[:12]}")
        return

    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, RAW)
    img = crop_to_16x9(img)
    size = finalize(img, OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    readable, noise = ocr_text_check(OUTPUT)
    if not readable:
        print(f"OCR TEXT CHECK: clean ({len(noise)} sub-threshold blob(s))")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
