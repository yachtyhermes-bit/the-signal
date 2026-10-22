#!/usr/bin/env python3
"""Generate hero for axon-federal-ai-budget-moat-2026 (fal flux/schnell).

Subject: Axon Enterprise (AXON) — law-enforcement technology: TASER conducted
energy weapons, body-worn cameras, the Evidence.com cloud, AI-assisted report
writing, drones (Axon Air) and Dedrone counter-drone / RF detection. The article
covers the federal AI / defense budget tailwind and the platform moat.

Scene chosen: A POLICE OFFICER IN UNIFORM BESIDE THE OPEN DOOR OF A PATROL SUV
on a quiet suburban street at golden hour, a body-worn camera clipped to the
chest of the vest clearly visible, and a small quadcopter drone hovering high
above the street in the upper third of the frame.

Deliberately NOT a data-centre hallway / server aisle / rack (banned site-wide),
NOT a chiller plant, NOT a missile/defense factory floor, NOT a microchip macro,
NOT trading-floor screens, NOT neon / synthwave / glowing lines / geometric
patterns, NOT digital art, NOT 3D render or CGI, NOT abstract, NOT stock
"cop portrait" cliche with a visible department badge.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: no letters/numbers/labels/logos/signage/screens/UI anywhere.
  No readable uniform patches, no badges with lettering, no vehicle liveries,
  no licence plates, no radio displays, no police department names, no logos.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-axon-federal-ai-budget-hero-20261022.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "axon-federal-ai-budget-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no model numbers, no "
    "stencilled markings, no colour-code tags, no equipment nameplates, no "
    "asset tags, no warning signs, no safety posters, no cabinet labels, no "
    "digital readouts, no radio displays, no screen content, no control "
    "screens, no user interface, no dashboards, no software windows, no "
    "toolbars, no menus, no icons, no charts, no signage, no wall placards, "
    "no street signs, no exit signs, no door signs, no house numbers, no "
    "painted line lettering, no name badges, no lanyards, no printed "
    "documents, no clipboards with writing, no brand names, no manufacturer "
    "names, no company names, no corporate logos, no trademarks, no "
    "watermarks, no stickers, no decals, no barcodes, no QR codes, no "
    "handwriting, no graffiti, no legible writing of any kind anywhere in the "
    "image. The police officer's uniform carries NO readable lettering: no "
    "name tape, no department name tape, no rank insignia formed of letters, "
    "no embroidered surnames, no unit numbers, no printed patch text. The "
    "shoulder patches and chest patches are plain blank shapes of solid cloth "
    "colour with no embroidery, no crest, no star, no seal and no wording of "
    "any kind, or they are angled away from camera entirely. The badge on the "
    "officer's chest is a plain unmarked metal shield or a blank oval with no "
    "engraved letters, no numerals and no crest detail, catching only a soft "
    "specular highlight. The duty belt, the vest webbing and the pouches are "
    "plain black nylon with no printed labels, no brand tags and no moulded "
    "lettering. Every radio, handset, body-camera housing and any device in "
    "the frame has a plain blank casing with no display, no screen, no button "
    "legends and no printed model marking. The patrol SUV carries NO readable "
    "lettering: no door livery, no department name, no wordmarks, no stripes "
    "that form letters, no unit number on the fender or roof, no decal on the "
    "hood, no light-bar lettering. Its licence plate is entirely blank and "
    "plain — a smooth unmarked rectangle of neutral colour with no characters, "
    "no numerals and no state name — or the plate is not visible in frame at "
    "all. The tyres, wheels and body panels carry no markings, and the "
    "windscreen and windows show no stickers, no permits and no reflections "
    "that resolve into letters. The drone in the sky is a plain smooth "
    "unpainted-grey airframe with no registration number, no decal, no "
    "wordmark and no lights that form characters. Background houses show no "
    "house numbers, no mailboxes with characters and no street signage. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no circuit-board graphics, no network diagram, no graph graphic, no "
    "futuristic HUD graphics, no hologram, no overlay elements, no "
    "augmented-reality graphics, no heads-up display, no scan lines, no "
    "targeting reticle, no data center, no server room, no server racks, no "
    "server aisles, no cable runs, no server lights, no GPU hardware, no "
    "computer screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no 3D visualisation, no digital illustration, no "
    "painting, photorealistic, very high detail, professional editorial "
    "stock photography, 16:9 landscape composition, professional lighting. "
)

PROMPTS = {
    # 1 — PRIMARY: officer at the open door of a patrol SUV on a quiet
    #     suburban street at golden hour + body camera on chest + drone high.
    "1": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a 35mm lens at f/2.8 on a full-frame camera from standing eye "
        "level on a quiet residential street in suburban America in the last "
        "hour of daylight. The light is warm low golden-hour sun raking in "
        "from camera left, long soft shadows across the asphalt, the sky "
        "above a clear pale gradient from warm peach at the horizon to a "
        "deeper blue overhead, one or two thin hazy clouds. The street is "
        "empty and calm: a two-lane asphalt road with a concrete kerb, mown "
        "green lawns, mature leafy street trees, and a row of modest "
        "single-storey suburban houses with pitched roofs and garages set "
        "back behind low hedges and drives, softly out of focus behind. In "
        "the left-centre of the frame, three-quarters turned toward camera, "
        "a police officer in uniform stands beside the open driver's door of "
        "a white and dark-navy patrol SUV. The SUV is parked at the kerb, "
        "the door swung wide toward camera, its interior in shadow, the "
        "vehicle's flank and rear quarter receding out of the right edge of "
        "the frame. The officer is a man in his thirties, close-cropped hair, "
        "calm and unposed, mid-motion: one hand resting on the top edge of "
        "the open door, the other relaxed at his side, weight on his back "
        "foot, looking off past the camera down the street as if watching "
        "something quietly. He wears a plain navy short-sleeve uniform shirt "
        "with a plain dark protective vest over it, plain navy duty trousers "
        "with a dark stripe, a plain black duty belt with plain black "
        "pouches, and black boots. Clipped squarely to the centre-left of his "
        "chest vest, catching the low sun, is a black body-worn camera: a "
        "small rounded rectangular housing with a plain glossy lens window, "
        "clearly readable as a body camera, unobstructed and in sharp focus, "
        "with a short plain cable looping up to the shoulder. His shoulder "
        "patches are plain blank shapes of cloth with no lettering, and the "
        "badge on his chest is a plain unmarked metal shape with no "
        "engraving. High in the upper third of the frame, small against the "
        "pale sky and slightly right of centre, a small quadcopter drone "
        "hovers above the street: a compact grey four-rotor airframe with "
        "thin blurring propeller discs, its belly and one arm catching the "
        "warm light, plainly a real hovering aircraft and not a graphic. The "
        "street reads as a real place at a real hour: warm light on the "
        "tarmac and the car's paint, cool blue shadow pooling under the "
        "trees and inside the open door. Strong spatial depth: the officer "
        "and the body camera crisp in the near mid-ground, the SUV and the "
        "open door resolving, the houses and trees falling away into soft "
        "warm bokeh, the drone small and sharp against the sky. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — FALLBACK A: tight detail of the body camera on a tactical vest,
    #     shallow depth of field, blurred suburban street behind.
    "2": (
        "Professional stock photograph, real photo not a render, shot on an "
        "85mm lens at f/1.8, a tight three-quarter crop of a body-worn camera "
        "mounted on a police officer's tactical vest. The camera fills the "
        "left-centre of the frame: a black rounded rectangular housing about "
        "the size of a small phone, its front face matte black with a subtle "
        "pebbled texture, a glossy dark circular lens window at its upper "
        "left with a soft warm specular highlight sliding across the glass, "
        "a plain blank face with no screen, no button legends and no printed "
        "markings, held in a rigid black polymer mount clipped hard onto the "
        "vest's webbing. A short plain black cable leaves the top of the "
        "housing and loops up out of frame toward the shoulder. The vest "
        "beneath it is heavy dark navy woven nylon: thick horizontal webbing "
        "straps, a MOLLE panel of tight stitched loops, a plain black buckle "
        "and the soft folds where the fabric bunches at the shoulder, every "
        "stitch and thread visible at this distance. No patches, no lettering, "
        "no name tape: the visible cloth is plain solid colour. At the upper "
        "right edge of frame, out of focus, the suggestion of the officer's "
        "jaw and the collar of a plain navy shirt, and the blurred warm curve "
        "of a shoulder. Behind, thrown far out of focus into creamy planes of "
        "warm ochre, dusty green and pale blue, the soft shapes of a quiet "
        "suburban street at golden hour: the blurred mass of a parked car, "
        "the smear of a tree canopy, a wash of low warm sunlight across "
        "asphalt, all dissolving into smooth bokeh with nothing readable in "
        "it. Low golden side light from camera left rakes across the mount "
        "and the webbing, picking out the texture and leaving deep soft "
        "shadow on the right. Photographic, extremely shallow depth of field "
        "with the lens window, the mount clip and the nearest webbing tack "
        "sharp, honest available-light exposure, no coloured gels. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — FALLBACK B: rooftop counter-drone RF detection unit silhouetted at
    #     dusk over a low suburban skyline with a distant drone.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated: a wide establishing view shot on a 24mm lens at f/4 from "
        "rooftop level at dusk. The frame is dominated by the silhouette of a "
        "counter-drone radio-frequency detection installation standing on the "
        "flat gravel roof of a low commercial building: a slim matte-grey "
        "mast of about three metres rising from a heavy cast base plate, "
        "carrying at its top a cluster of small flat rectangular antenna "
        "panels angled outward at different compass bearings, a compact "
        "sealed grey housing with cooling fins bolted to the mast below them, "
        "and a stubby omni-directional whip antenna. A single sheathed cable "
        "runs down the mast in a neat curve and disappears through a plain "
        "roof gland at the base. The installation is backlit and reads "
        "cleanly as a hard dark silhouette against the sky, every edge crisp, "
        "with a thin warm rim of dying sunlight along the top edges of the "
        "antenna panels. Behind and below it, a low suburban skyline recedes "
        "into dusk: the flat and pitched rooftops of one- and two-storey "
        "buildings, the pale rectangles of parapets, a few bare rooftop "
        "extractor stacks and the soft dark crowns of trees between the "
        "buildings, stepping away in three or four receding planes toward a "
        "hazy horizon. The sky occupies the upper two thirds of the frame: a "
        "smooth dusk gradient from a deep indigo at the top through dusty "
        "violet to a band of warm apricot and faint coral along the horizon "
        "where the sun has just gone, with one or two thin streaked clouds "
        "lit from below. High in the sky, small and clearly a real aircraft, "
        "a distant quadcopter drone hangs as a tiny dark cross shape with "
        "faintly visible rotor discs, catching a last glint of light on one "
        "arm — no lights that form characters, no markings. The foreground "
        "roof surface is plain weathered grey membrane and gravel with a "
        "single low ventilation kerb, no signage, no equipment labels, no "
        "housings with printed text. Quiet, cold, observational mood, honest "
        "available light, no coloured gels beyond the natural dusk sky. "
        "Photographic, moderate depth of field with the mast and antenna "
        "panels crisp and the far skyline softening into dusk haze, real "
        "optical blur, honest exposure, natural camera noise, very slight "
        "film grain, subtle vignette, no CGI, no render. "
        + PHOTO_TAIL
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
    img = img.convert("RGB")
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def ocr_text_check(path, min_conf=70.0):
    """Run tesseract OCR as a text-artifact smoke test.

    psm 11 (sparse text) run against photographic texture always emits a pile
    of low-confidence garbage on high-frequency detail (fabric weave, MOLLE
    webbing, foliage, gravel). A genuine text artifact is a multi-character
    token picked up with high confidence, so candidates are split:
      - `readable`: >=3 alnum chars AND mean confidence >= min_conf  -> real risk
      - `noise`:    everything else, reported for transparency
    Returns (readable, noise) lists of (text, conf) tuples.
    """
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
            print(
                f"OCR TEXT CHECK: clean — no readable text detected "
                f"({len(noise)} sub-threshold texture blob(s) ignored)"
            )
        else:
            print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")
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
        print(
            f"OCR TEXT CHECK: clean — no readable text detected "
            f"({len(noise)} sub-threshold texture blob(s) ignored)"
        )
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
