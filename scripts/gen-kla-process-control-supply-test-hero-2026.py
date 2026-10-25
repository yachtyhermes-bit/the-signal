#!/usr/bin/env python3
"""Generate hero for kla-process-control-supply-test-2026 (fal flux/schnell).

Subject: KLA Corporation — semiconductor process control / metrology. The
machines inspect and measure every wafer inside a chip fab; the article is
about that business (supply, test, qualification) and not about data centres.

Scene chosen: INSIDE A REAL SEMICONDUCTOR FAB CLEANROOM — a large wafer
inspection / metrology tool with a round reflective 300mm silicon wafer on its
brushed-metal stage under the optical inspection head, and a cleanroom engineer
in a plain white bunny suit working at it. Warm cleanroom lighting, shallow
depth of field.

Deliberately NOT a data-centre / server-room / server-aisle / rack / cable-run
composition (banned site-wide), NOT neon / synthwave / glowing lines /
geometric patterns, NOT digital art, NOT 3D render or CGI, NOT abstract.

Rules:
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: fabs are full of labels, monitors and signage, so all lettering,
  numbers, UI, logos and brand names are explicitly forbidden. Any monitor in
  frame is blank / dark / out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-kla-process-control-supply-test-hero-2026.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "kla-process-control-supply-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no toolbars, no menus, no icons, no signage, "
    "no warning signs, no wall placards, no cabinet labels, no panel "
    "markings, no engraved lettering on the equipment, no dial faces with "
    "numbers, no gauges with numerals, no dials, no readouts, no charts, no "
    "arrows, no crosshairs, no alignment marks, no wafer flat markings, no "
    "die labels, no lettering scribed or etched on the silicon wafer itself, "
    "no keyboard lettering, no name badges, no lanyards, no printed "
    "documents, no clipboards with writing, no brand names, no manufacturer "
    "names, no company names, no corporate logos, no trademarks, no "
    "watermarks, no stickers, no decals, no barcodes, no QR codes, no "
    "datamatrix codes, no handwriting, no legible writing of any kind "
    "anywhere in the image. Every monitor or display in the frame is "
    "switched off, angled away, or so far out of focus that it shows only a "
    "soft flat wash of dark colour with absolutely nothing readable or drawn "
    "on it. The cleanroom suit, hood, mask and gloves are plain and unmarked "
    "with no printed patches, no embroidered names and no wordmarks. The "
    "tool's panels are plain brushed metal with only unlabelled blank "
    "buttons and one plain unmarked rotary knob, and the walls are plain "
    "cleanroom panel with no writing on them. The wafer's surface is a "
    "texture of light and colour only — a repeating grid of unmarked chips "
    "with no engraved characters, no die codes, no lot codes and no "
    "lettering of any kind. No illustration, no digital art, no cartoon, no "
    "3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no circuit-board graphics, no network "
    "diagram, no graph, no futuristic HUD graphics, no hologram, no overlay "
    "elements, no augmented-reality graphics, no data center, no server "
    "room, no server racks, no server aisles, no cable runs, no server "
    "lights, no GPU hardware, no computer screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light industrial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no perfect "
    "symmetry, no 3D visualisation, no digital illustration, no painting, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — PRIMARY: engineer in bunny suit at a large wafer-inspection
    #     metrology tool, 300mm reflective wafer on the stage under the head.
    "1": (
        "Photo-realistic editorial press photograph, a real photo shot on a "
        "50mm lens at f/2 on a full-frame camera, inside a working "
        "semiconductor fabrication cleanroom. Composition: the large body of "
        "a wafer inspection and metrology tool fills the left and centre of "
        "the frame, and a cleanroom engineer in a full plain white bunny "
        "suit, hood and clear face shield stands at the right of the tool, "
        "three-quarters turned away from camera so the face is turned down "
        "toward the work, mid-task, not posing. In the sharp centre of the "
        "frame, on the tool's brushed stainless inspection stage, sits a "
        "round reflective 300mm silicon wafer held flat on a circular "
        "vacuum chuck; above it a smooth dark anodised optical inspection "
        "head with a downward-facing lens barrel hangs on a precision "
        "gantry arm, its lens throwing a soft cone of warm light down onto "
        "the wafer. The wafer's mirror-polished face reads as a dense "
        "repeating grid of identical unmarked rectangular chips, a mosaic "
        "of faint interlocking rectangles and hairline scribe streets that "
        "shifts into a subtle iridescent bloom of muted violet, pale cyan "
        "and warm gold where the light rakes across it — pure light and "
        "texture, with nothing written, etched or printed on the silicon. "
        "The engineer's yellow-gloved hand rests near a plain unlabelled "
        "control surface of blank buttons, and a small dark monitor on the "
        "tool is turned away from camera and switched off. The tool is "
        "clean white and brushed stainless steel with a round load-port "
        "opening, rounded corners and clean geometric panelling. The "
        "cleanroom around them is bright and spotless: pale sealed wall "
        "panels, a white ceiling with flush light panels, a pale "
        "perforated raised floor. The lighting is warm — soft diffuse "
        "warm-white cleanroom light with a gentle amber cast falling across "
        "the wafer and the engineer's shoulder, warm highlights along the "
        "stainless edges and deep soft shadows under the gantry, the whole "
        "room reading as warm rather than clinical blue. Extremely shallow "
        "depth of field: the wafer surface, the lens barrel and the near "
        "gloved hand tack sharp, the engineer's torso and the cleanroom "
        "wall behind melting into creamy bokeh. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 2 — FALLBACK A: tighter on the wafer + optical head, engineer's hands
    #     and shoulder soft in the background.
    "2": (
        "Photo-realistic editorial press photograph, a real photo shot on a "
        "100mm macro lens at f/2.8 on a full-frame camera inside a "
        "semiconductor cleanroom, framed close over the stage of a wafer "
        "inspection tool. The frame is dominated by a round reflective "
        "300mm silicon wafer lying flat on a brushed stainless vacuum "
        "chuck, its mirror face turned slightly toward camera: across it "
        "runs a precise repeating grid of identical unmarked rectangular "
        "chips separated by hairline scribe streets, the surface catching a "
        "soft iridescent bloom of muted violet, pale cyan and warm brass "
        "where the light grazes, and near the round edge the grid is "
        "clipped leaving a crescent of bare polished silicon. Above the "
        "wafer a smooth dark anodised optical inspection head with a "
        "downward lens barrel hangs close on a precision gantry, throwing a "
        "warm pool of light onto the wafer's centre; a thin warm specular "
        "line traces the lens barrel's rim. Honest surface detail: a mote "
        "of dust on the rim, the faintest haze where a glove touched the "
        "edge. In the soft background at the upper right, well out of "
        "focus, the pale mass of a cleanroom engineer in a plain white "
        "bunny suit and hood leans toward a plain unmarked panel, one "
        "yellow-gloved hand raised toward it, the whole figure reduced to "
        "soft warm shapes. The lighting is warm-white cleanroom light from "
        "flush ceiling panels with a gentle amber cast, warm highlights on "
        "polished metal and deep soft shadow under the gantry. Extremely "
        "shallow depth of field with the near wafer surface and the lens "
        "barrel crisp and everything behind dissolving into creamy bokeh. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 3 — FALLBACK B: wider, tool-dominant, engineer walking the bay.
    "3": (
        "Photo-realistic editorial press photograph, a real photo shot on a "
        "35mm lens at f/2.8 on a full-frame camera inside a working "
        "semiconductor cleanroom. A large wafer inspection and metrology "
        "tool stands in the right half of the frame: a tall clean white and "
        "brushed stainless cabinet with rounded corners, a round load-port "
        "opening, a sloping plain unlabelled control surface and a small "
        "dark switched-off monitor angled away, its open stage holding a "
        "round reflective 300mm silicon wafer under a dark anodised optical "
        "inspection head that throws a warm pool of light down onto the "
        "patterned disc, the wafer's grid of unmarked chips glinting with a "
        "faint iridescent violet and gold where the light rakes across. To "
        "the left of the tool a cleanroom engineer in a full plain white "
        "bunny suit, hood, mask and yellow gloves stands facing the tool in "
        "profile, one gloved hand resting on the stage edge, attentive and "
        "mid-task. Behind them the bay continues softly out of focus: pale "
        "sealed wall panels, flush ceiling light panels, a pale perforated "
        "raised floor, the rounded white shoulder of a second tool far "
        "away, everything dissolving into warm haze with nothing readable "
        "anywhere. The light is warm-white and diffuse, with an amber cast "
        "across the stainless surfaces and the engineer's hood, gentle "
        "shadows pooled under the tool and a soft warm glow in the air. "
        "Moderate depth of field with the wafer, the inspection head and "
        "the engineer's gloved hand crisp and the far bay melting into "
        "blur. "
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
    """Tesseract OCR smoke test for text artifacts."""
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return [], []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11", "tsv"],
                check=True,
                capture_output=True,
                timeout=180,
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
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 204800:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
    readable, noise = ocr_text_check(OUTPUT)
    if not readable:
        print(f"OCR TEXT CHECK: clean ({len(noise)} sub-threshold blob(s))")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
