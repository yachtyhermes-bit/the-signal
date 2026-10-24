#!/usr/bin/env python3
"""Generate hero for googl-external-tpu-sales-chip-business-2026 (fal flux/schnell).

Subject: Alphabet/Google selling TPU AI chips to external customers as a new
business line. The story is silicon supply and manufacturing, not data centres.

Scene chosen: MACRO CLOSE-UP OF A LARGE SILICON WAFER WITH IRIDESCENT CIRCUIT
DIES held in a gloved hand inside a semiconductor cleanroom — cool white
cleanroom lighting with a warm amber rim. Shallow depth of field so the wafer
circuitry is sharp and the cleanroom equipment falls away into soft bokeh.

Deliberately NOT a data-centre hallway / server aisle / rack (banned site-wide),
NOT neon / synthwave / glowing lines / geometric patterns, NOT digital art,
NOT 3D render or CGI, NOT abstract.

Rules:
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: no letters/numbers/labels/logos/signage/screens anywhere. Die
  surfaces carry no part numbers, lot codes, laser-scribe text or matrix codes.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=6 /home/chino/video-venv/bin/python3 \
         scripts/gen-googl-external-tpu-sales-hero-20261024.py

Shipped: ATTEMPT=6. Attempts 1-3 rendered CGI-looking / over-cyan; attempt 2
was photo-real with iridescent dies but hallucinated a small black emblem on
the wafer face; 4-5 were clean but had a blank studio-looking background.
Attempt 6 keeps the sharp die grid, cool-white + warm amber rim, and puts a
blurred stainless wafer-handling tool in the left third so the background
reads as cleanroom equipment. Vision QA (fal gemini-flash): real DSLR photo,
no text/logo, no data-center look, SHIP.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "googl-external-tpu-sales-chip-business-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "lot codes, no date codes, no model numbers, no stencilled markings, no "
    "laser-etched markings, no etched lettering on the silicon, no scribe-line "
    "text, no die markings, no reticle marks, no fiducial lettering, no "
    "equipment nameplates, no asset tags, no warning signs, no safety posters, "
    "no bench labels, no cabinet labels, no barcode labels, no monitor "
    "screens, no digital readouts, no control panels with words, no user "
    "interface, no dashboards, no printed paper, no clipboards with writing, "
    "no signage of any kind, no brand names, no manufacturer names, no company "
    "names, no corporate logos, no trademarks, no watermarks, no stickers, no "
    "decals, no barcodes, no QR codes, no two-dimensional matrix codes, no "
    "handwriting, no graffiti, no legible writing of any kind anywhere in the "
    "image. The wafer is a completely unbranded engineering wafer: every die "
    "on it is a plain rectangular grid of fine metallic interconnect and "
    "polished silicon with no etched characters, no die codes, no lettering of "
    "any kind — only the micro-structure of circuitry and thin-film colour. "
    "The technician's cleanroom suit, hood, mask and gloves are plain and "
    "unmarked with no printed patches, no embroidered names and no wordmarks. "
    "Every machine and surface in the background is plain unmarked metal, "
    "glass and pale plastic with no printed legends and no branding. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphic overlay, no network diagram, no graph, "
    "no futuristic HUD graphics, no hologram, no overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no server aisles, no cable runs, no server lights."
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
    # 1 — PRIMARY: 100mm macro, gloved hand holding a 300mm wafer at an angle,
    #     iridescent dies sharp, cleanroom equipment in creamy bokeh.
    "1": (
        "Professional stock photograph, a real photo shot on a 100mm macro lens "
        "at f/2.8 on a full-frame camera, framed close and slightly high over a "
        "semiconductor cleanroom. The subject fills the centre of the frame: a "
        "large circular 300mm silicon wafer, roughly thirty centimetres across, "
        "held up at a shallow angle to the lens by one hand in a thin pale "
        "white nitrile cleanroom glove. The glove grips the wafer's edge from "
        "below at the lower left, fingertips spread and pressing gently on the "
        "bare rim, the nitrile creased and slightly powdery at the knuckles, a "
        "plain white cleanroom sleeve cuff entering the frame at the lower "
        "left. The wafer's mirror-polished face is turned toward camera so its "
        "full disc of circuitry reads in sharp macro detail: a dense regular "
        "grid of hundreds of identical rectangular dies separated by fine "
        "scribe streets, each die a microscopic city of aluminium and copper "
        "interconnect, and across the whole surface a thin-film iridescence "
        "shifts through soft violet, teal, green and warm gold as the light "
        "rakes across it — real diffraction colour, not a rainbow filter. Near "
        "the wafer's edge the grid is clipped by the round boundary, leaving a "
        "crescent of plain polished silicon with only a faint bloom of "
        "diffraction. At this distance the surface is honest and imperfect: a "
        "few microscopic particles, the faintest haze of a fingerprint near "
        "the rim, a hairline of dust. The lighting is cool white cleanroom "
        "light from broad ceiling panels above and behind the camera, flat and "
        "clinical across most of the wafer, and against that a single warm "
        "amber rim light grazes the wafer's far edge from the upper right, "
        "drawing a thin hot line of amber along the rim and picking out the "
        "glove's edge with a soft warm glow, so the frame holds cool white and "
        "warm amber together. Behind the hand and the wafer, thrown far out of "
        "focus into soft planes of pale grey, white and cool blue, the "
        "indistinct machinery of a cleanroom dissolves into creamy bokeh: the "
        "rounded blank housing of a lithography tool, a stainless panel, the "
        "edge of a laminar-flow bench, a suggestion of a second worker in a "
        "white suit far away and featureless, with nothing readable in any of "
        "it. Photographic, extremely shallow depth of field: the centre of the "
        "wafer and the nearest gloved fingertips tack sharp, the wafer's far "
        "edge and the whole room melting into smooth blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 2 — FALLBACK A: two gloved hands cradling the wafer low over a bench,
    #     top-down three-quarter, wafer dominant, amber rim from the right.
    "2": (
        "Professional stock photograph, a real photo not a render, shot on an "
        "85mm macro lens at f/3.2 from just above bench height in a "
        "semiconductor fabrication cleanroom. A large circular silicon wafer "
        "about thirty centimetres across is cradled flat between two hands in "
        "thin pale white nitrile cleanroom gloves, the hands entering from the "
        "left and right edges of the frame and gripping the wafer only at its "
        "rim, thumbs resting on the polished edge, gloves creased at the "
        "knuckles, plain white cleanroom sleeves at the frame edges. The wafer "
        "is tilted just enough toward the lens that its entire circuit face is "
        "visible: a precise grid of identical rectangular dies running out in "
        "fine scribe streets to the round edge, each die packed with "
        "microscopic interconnect, and the whole disc washed with the soft "
        "iridescent thin-film sheen of a processed wafer — muted violet, pale "
        "cyan, faint green and warm brass shifting across the surface as the "
        "light changes angle, real optical diffraction rather than a printed "
        "rainbow. A few dies near the flat are clearly resolved down to their "
        "internal blocks; a handful of darker dies near the edge sit unpatterned "
        "where the grid is clipped. Honest surface detail: a dust mote caught "
        "on the rim, the faintest smudge where a glove touched the edge. Cool "
        "white cleanroom light falls from broad panels overhead, even and "
        "shadowless across the wafer, while a warm amber kicker from a low lamp "
        "at the right edge rims the wafer's right side and the right glove in "
        "warm light, giving a cool-to-warm gradient across the frame with "
        "honest specular highlights and no coloured gels. Below and behind, far "
        "out of focus, the pale grey surface of a stainless inspection bench "
        "and the soft grey mass of a metrology tool fade into creamy bokeh with "
        "nothing readable anywhere. Photographic, shallow depth of field with "
        "the near half of the wafer and both sets of gloved fingertips sharp, "
        "the far rim and the bench dissolving into blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 3 — FALLBACK B: wafer held up edge-on toward a cool light panel, face
    #     angled away, iridescent sliver; cleanroom depth behind.
    "3": (
        "Professional stock photograph, real documentary photograph shot on a "
        "50mm lens at f/2 in a semiconductor cleanroom, framed at chest height "
        "from slightly to the side. A technician in a plain white cleanroom "
        "bunny suit, hood and face mask, seen three-quarters from behind so the "
        "face is turned away, holds a large circular silicon wafer up between "
        "both gloved hands and tilts it toward a broad cool white light panel, "
        "inspecting it. The wafer is angled steeply away from camera so its "
        "mirror face catches the panel as a broad soft glare and its circuit "
        "grid is seen in sharp foreshortening — concentric bands of tiny dies "
        "compressing toward the far rim, the fine scribe streets flaring into "
        "thin bright lines, and along the wafer's silhouette a narrow band of "
        "thin-film iridescence glows violet, teal and warm gold where the light "
        "grazes the surface at the edge. The gloved hands grip the wafer only "
        "at the rim, thin pale nitrile, the suit's cuffs plain and unmarked. "
        "The lighting is the cleanroom's own: a large diffuse cool white panel "
        "in front of the wafer throwing flat clinical light, with a warm amber "
        "accent from a distant sodium-toned lamp behind the technician rims the "
        "hood, the shoulder and the wafer's near edge in warm light, so the "
        "figure reads cool in front and warm behind. The room falls away into "
        "soft pale grey depth: the blurred white bulk of a wafer-handling tool, "
        "a stainless steel cart, an extractor grille, the pale wall of the bay, "
        "all dissolving into creamy bokeh, nothing readable. Quiet, precise, "
        "industrious mood, honest mixed available light, no coloured gels, no "
        "atmospheric theatrics. Photographic, shallow depth of field with the "
        "gloved hands and the wafer's near rim crisp, the technician's body and "
        "the room softening into blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 4 — SIXTH PASS: attempt-2 composition (cradled wafer, warm rim) but with
    #     an explicit ban on any emblem/logo/pictogram on the wafer face, and
    #     the wafer centre specified as plain die grid only.
    "4": (
        "Professional stock photograph, a real photo shot on an 85mm macro lens "
        "at f/3.2 from just above bench height in a semiconductor cleanroom. A "
        "large circular silicon wafer about thirty centimetres across is held "
        "up between two hands in thin pale white nitrile cleanroom gloves, the "
        "hands entering from the left and right of the frame and gripping the "
        "wafer only at its rim, gloves creased and slightly powdery at the "
        "knuckles, plain white cleanroom sleeve cuffs at the frame edges. The "
        "wafer is tilted about thirty degrees toward the lens, its mirror face "
        "filling the centre of the frame: an unbroken regular grid of identical "
        "rectangular dies separated by fine scribe streets, each die packed "
        "with microscopic interconnect, the grid running right to the round "
        "edge where it is clipped, and the whole disc washed in the soft "
        "thin-film iridescence of a processed wafer — muted violet, pale cyan, "
        "faint green and warm brass drifting across the surface with the "
        "changing light angle. There is absolutely nothing printed, etched, "
        "scored, stamped or drawn on the wafer: no logo, no emblem, no symbol, "
        "no pictogram, no glyph, no monogram, no crest, no badge, no die-array "
        "label, no test-pattern lettering, no centre mark, no notch markings, "
        "no text of any kind — only the plain repeating geometry of the die "
        "grid and bare polished silicon. Honest surface detail: a dust mote on "
        "the rim, the faintest smudge where a glove touched the edge. Cool "
        "white cleanroom light falls from broad panels overhead, even and "
        "shadowless across the wafer, while a warm amber kicker lamp at the "
        "right edge rims the wafer's right side and the right glove in warm "
        "light, giving a cool-to-warm gradient across the frame with honest "
        "specular highlights and no coloured gels. Below and behind, far out of "
        "focus, the pale grey surface of a stainless inspection bench and the "
        "soft grey mass of a metrology tool fade into creamy bokeh with nothing "
        "readable anywhere. Photographic, shallow depth of field with the near "
        "half of the wafer and both sets of gloved fingertips sharp, the far "
        "rim and the bench dissolving into blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 5 — SEVENTH PASS: angled wafer in one gloved hand (no flat full disc
    #     presented to camera, which is where logos appear) in a BRIGHT pale
    #     cleanroom bay that fills the background with out-of-focus equipment.
    "5": (
        "Professional stock photograph, a real photo shot on a 100mm macro lens "
        "at f/2.8 on a full-frame camera in a bright semiconductor cleanroom "
        "bay. A single hand in a thin pale white nitrile cleanroom glove holds a "
        "large circular 300mm silicon wafer up at a steep angle — about "
        "thirty-five degrees to the lens — gripping it only at the rim from "
        "below, fingertips spread on the bare silicon edge, the glove creased "
        "and slightly powdery at the knuckles, a plain white cleanroom sleeve "
        "cuff entering the frame at the lower left. Because of the angle the "
        "wafer reads as a bright ellipse: its mirror face is foreshortened, the "
        "grid of identical rectangular dies compressing toward the far edge, "
        "the fine scribe streets flaring into thin bright lines where they "
        "catch the light, and the whole surface shifting through the muted "
        "thin-film iridescence of a processed wafer — violet, pale cyan, faint "
        "green and warm brass drifting across it as the viewing angle changes. "
        "The nearest band of the grid is resolved down to individual "
        "interconnect at the left of the frame and recedes into compression at "
        "the right. Nothing is printed, etched, stamped, scored or drawn on it: "
        "no logo, no emblem, no symbol, no pictogram, no glyph, no badge, no "
        "monogram, no centre mark, no die label, no notch marking — only bare "
        "polished silicon and the repeating geometry of the die grid. The "
        "lighting is the bay's own: broad cool white panels overhead flood the "
        "whole room with flat, clinical, bright light, and a warm amber kicker "
        "from a lamp at the extreme right rims the wafer's near edge and the "
        "glove with a thin warm line, cool-to-warm across the frame, honest "
        "specular highlights, no coloured gels. Behind the hand the cleanroom "
        "stays bright and pale — not dark — and is thrown far out of focus: the "
        "rounded white housing of a lithography tool filling the upper left, a "
        "stainless steel panel and a laminar-flow bench grille at the right, "
        "pale grey perforated wall panels, the soft white blur of a distant "
        "figure in a cleanroom suit, all dissolving into creamy bokeh with "
        "nothing readable anywhere. Photographic, extremely shallow depth of "
        "field: the near wafer edge, the sharpest band of dies and the gloved "
        "fingertips are tack sharp while the room melts into smooth blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 6 — EIGHTH PASS: adds a big, clearly-shaped middle-ground object (a
    #     stainless wafer-handling tool body occupying the left third) so the
    #     background reads as cleanroom equipment rather than blank backdrop,
    #     while keeping the wafer sharp at the right and no markings on silicon.
    "6": (
        "Professional stock photograph, a real photo shot on a 100mm macro lens "
        "at f/2.8 on a full-frame camera inside a semiconductor cleanroom. "
        "Composition: the right two-thirds of the frame is a large circular "
        "300mm silicon wafer held up at a shallow angle by a hand in a thin "
        "pale white nitrile glove, and the left third is the soft, out-of-focus "
        "body of the equipment it came from. The glove grips the wafer only at "
        "its lower-left rim, fingertips spread on bare silicon, glove creased "
        "and powdery at the knuckles, plain white cleanroom sleeve cuff running "
        "out of the bottom of the frame. The wafer's mirror face is angled "
        "about thirty degrees to the lens, so the grid of identical rectangular "
        "dies compresses toward the far edge: near the left rim the interconnect "
        "inside each die is individually resolved, fine perpendicular scribe "
        "streets separate the dies, and across the whole disc the thin-film "
        "iridescence shifts through muted violet, pale cyan, faint green and "
        "warm brass as the angle changes — real optical diffraction from a "
        "processed wafer, with a few microscopic particles and a faint rim "
        "smudge as honest detail. The wafer carries no marking of any kind: no "
        "logo, no emblem, no symbol, no pictogram, no badge, no monogram, no die "
        "label, no notch marking, no text — only bare polished silicon and the "
        "repeating die grid. Behind and to the left, in the middle ground but "
        "well out of focus, stands a stainless steel wafer-handling tool: a "
        "tall brushed-metal housing with a recessed dark window, a sloping "
        "control surface with no readable display, a round load-port opening, "
        "and a pale grey perforated wall panel behind it, its edges soft and "
        "its details dissolved by the shallow focus. Lighting is the bay's own: "
        "broad cool white ceiling panels flood the room with bright clinical "
        "light, and a warm amber kicker from a lamp at the right edge lays a "
        "thin warm rim along the wafer's right edge and the glove, so the frame "
        "holds cool white and warm amber together with honest specular "
        "highlights and no coloured gels. Photographic, extremely shallow depth "
        "of field: the near wafer edge, the sharpest band of dies and the "
        "gloved fingertips tack sharp, the tool body and the far rim melting "
        "into smooth creamy blur. "
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
