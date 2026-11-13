#!/usr/bin/env python3
"""Hero for amat-record-quarter-dram-mix-2026 (fal flux/schnell).

Subject: Applied Materials — the largest semiconductor equipment maker. Its
record fiscal Q4 was carried by the DRAM / memory mix rather than logic, so the
picture is about the machines that deposit and etch films onto blanket and
patterned wafers inside a chip fab.

Scene: INSIDE A WORKING SEMICONDUCTOR FAB CLEANROOM. A process engineer in a
plain white bunny suit holds a 300mm silicon wafer up to the light to inspect
it, with a deposition / etch tool bay softly out of focus behind them. Warm
amber cleanroom light, shallow depth of field, real photograph.

Deliberately NOT a data centre / server room / server aisle / racks / cable
runs (banned site-wide), NOT neon / synthwave / glowing lines / geometric
patterns, NOT digital art, NOT 3D render or CGI, NOT abstract, no text.

HARD CAP: 3 fal flux/schnell generations total. Never a 4th.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 \
      scripts/gen-amat-record-quarter-dram-mix-hero-2026.py
  ATTEMPT=1 FINALIZE=1 ...   # crop/save/mirror the staged attempt
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amat-record-quarter-dram-mix-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
FINALIZE = os.environ.get("FINALIZE") == "1"
STAGE = f"/tmp/{SLUG}-attempt{ATTEMPT}.jpg"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 480 * 1024

NO_TEXT = (
    "The whole scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no toolbars, no menus, no icons, no signage, "
    "no warning signs, no hazard symbols, no yellow warning triangles, no "
    "exclamation-mark pictograms, no safety placards, no pictograms of any "
    "kind, no wall placards, no cabinet labels, no panel "
    "markings, no engraved lettering on the equipment, no dial faces with "
    "numbers, no gauges with numerals, no readouts, no charts, no arrows, "
    "no crosshairs, no alignment marks, no wafer flat markings, no die "
    "labels, no lettering scribed or etched on the silicon wafer itself, "
    "no name badges, no lanyards, no printed documents, no clipboards with "
    "writing, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no trademarks, no watermarks, no stickers, no decals, "
    "no barcodes, no QR codes, no handwriting, no legible writing of any "
    "kind anywhere in the image. Every monitor and display is switched off, "
    "angled away, or so far out of focus that it shows only a soft flat "
    "wash of dark colour with nothing readable on it. The cleanroom suit, "
    "hood, mask and gloves are plain and unmarked with no printed patches, "
    "no embroidered names and no wordmarks. Tool panels are plain brushed "
    "metal with only blank unlabelled buttons, and the walls are plain "
    "cleanroom panel with no writing. The wafer's surface is a texture of "
    "light and colour only — a grid of unmarked chips with no engraved "
    "characters, no die codes, no lot codes and no lettering of any kind. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph, no "
    "futuristic HUD graphics, no hologram, no overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no server aisles, no cable runs, no server lights, no GPU "
    "hardware."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light industrial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no digital illustration, no painting, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — PRIMARY: engineer holds the wafer up to inspect it, tool bay behind.
    "1": (
        "Photo-realistic editorial press photograph, a real photograph shot "
        "on an 85mm lens at f/2 on a full-frame camera, inside a working "
        "semiconductor fabrication cleanroom. A process engineer in a full "
        "plain white bunny suit, white hood, clear face shield and pale "
        "yellow gloves stands at the centre-left of the frame holding a "
        "round 300mm silicon wafer up in both gloved hands at chest height, "
        "turning it slightly to inspect its surface against the light, "
        "mid-task and not posing, face angled down toward the wafer. The "
        "wafer is a thin mirror-polished disc seen at a slight angle: its "
        "face catches a bloom of warm amber light and shows a dense "
        "repeating grid of identical unmarked rectangular chips with "
        "hairline scribe streets, shading from warm gold through pale "
        "violet to soft cyan where the light rakes across it — pure light "
        "and texture, nothing written on it. Behind the engineer, softly "
        "out of focus, the cleanroom tool bay recedes: the rounded pale "
        "white and brushed stainless bodies of two deposition and etch "
        "process tools with dark recessed load-port openings, a low "
        "transfer chamber, and a hint of a second engineer in a bunny suit "
        "far down the bay, all reduced to soft warm shapes. The cleanroom "
        "itself is spotless: pale sealed wall panels, a white ceiling with "
        "flush light panels, a pale perforated raised floor, everything "
        "immaculately clean. The lighting is warm — soft diffuse warm-white "
        "cleanroom light with a gentle amber cast, warm highlights running "
        "along the wafer's edge and the engineer's shoulder, deep soft "
        "shadows under the tool bays, the room reading warm rather than "
        "clinical blue. Extremely shallow depth of field: the wafer, the "
        "gloved fingers at its rim and the front of the suit's shoulder "
        "tack sharp, the tool bay and the far cleanroom melting into creamy "
        "bokeh. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 2 — FALLBACK A: tighter on the held wafer, engineer's torso in bokeh.
    "2": (
        "Photo-realistic editorial press photograph, a real photograph shot "
        "on a 100mm lens at f/2.8 on a full-frame camera inside a "
        "semiconductor cleanroom, framed close on a 300mm silicon wafer "
        "held up between two pale yellow gloved hands. The round "
        "mirror-polished wafer fills the centre of the frame at a slight "
        "three-quarter angle, its face a dense repeating grid of identical "
        "unmarked rectangular chips separated by hairline scribe streets, "
        "the surface blooming with warm amber, muted violet and pale cyan "
        "as the cleanroom light rakes across it; near the round edge the "
        "grid is clipped, leaving a crescent of bare polished silicon, and "
        "a thumb in a yellow glove presses lightly on the rim. Behind the "
        "hands, well out of focus, the soft white mass of the engineer's "
        "bunny-suited torso and hood, and further back the pale blurred "
        "bodies of deposition and etch tools with dark load-port openings "
        "and the warm glow of ceiling light panels in the haze. The "
        "lighting is warm-white with an amber cast, warm specular "
        "highlights on the wafer's edge and deep soft shadow inside the "
        "room, the room reading distinctly warm rather than cold. The "
        "blurred tool cabinets behind are plain unmarked pale surfaces "
        "carrying no labels, no stickers and no symbols of any kind. "
        "Extremely shallow depth of field, the near wafer surface and "
        "the gloved fingertips crisp, everything else dissolving into "
        "creamy bokeh. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 3 — FALLBACK B: over-the-shoulder, wafer lifted toward a warm light
    #     panel, bay in deep bokeh with its faces turned away from camera.
    "3": (
        "Photo-realistic editorial press photograph, a real photograph shot "
        "on a 50mm lens at f/1.8 on a full-frame camera inside a working "
        "semiconductor cleanroom, from just behind and to the left of a "
        "process engineer. The engineer fills the left third of the frame in "
        "plain white bunny suit and hood, back three-quarters to camera, "
        "head tilted up, and lifts a round 300mm silicon wafer high in both "
        "pale yellow gloved hands toward a warm ceiling light panel, "
        "inspecting its face. The wafer is seen from behind at a steep angle "
        "so it reads as a dark translucent disc with a thin blazing warm rim "
        "where the light wraps around its edge, and a faint inner glow of "
        "amber and deep violet showing through the patterned film. Beyond "
        "the engineer's shoulder, the tool bay falls away in layers of warm "
        "haze: the soft pale masses of two deposition and etch tools with "
        "their cabinet faces turned away from camera and their dark recessed "
        "load ports reading as deep shadowed rectangles, a low transfer "
        "chamber, a pale perforated raised floor, and the glow of ceiling "
        "light panels. Every one of those tools is a plain unmarked pale "
        "surface in shadow carrying no labels, no stickers, no pictograms "
        "and no symbols of any kind. The light is warm and directional: a "
        "pool of amber light from the ceiling panel above rinsing the "
        "engineer's hood and shoulders and flaring the wafer's rim, warm "
        "highlights along the stainless edges, and deep soft amber-brown "
        "shadow filling the bay behind — the room reads distinctly warm, "
        "never cold or clinical blue. Very shallow depth of field: the "
        "wafer's rim and the near glove tack sharp, the engineer's hood and "
        "the whole tool bay dissolving into creamy bokeh. "
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
    if abs(cur_ratio - target_ratio) < 0.005:
        pass
    elif cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)


def save_bounded(img, path):
    for q in (93, 91, 89, 87, 85, 82, 79, 75):
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)

    if FINALIZE:
        if not os.path.exists(STAGE):
            print(f"ERROR: staged attempt missing: {STAGE}")
            sys.exit(1)
        img = Image.open(STAGE)
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
        return

    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    with open("/home/chino/thesignal/.last_hero_prompt.txt", "a") as fh:
        fh.write(f"\n\n=== {SLUG} ATTEMPT {ATTEMPT} ===\n{prompt}\n")
    generate(prompt, STAGE)


if __name__ == "__main__":
    main()
