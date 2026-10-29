#!/usr/bin/env python3
"""Hero for credo-aec-moat-competition-test-2026 (fal flux/schnell).

Subject: Credo Technology (CRDO) active electrical cables (AECs) — the short,
thick copper twinaxial cable assemblies that link AI servers and switches inside
a data-centre rack — and the SerDes/retimer silicon inside the connector shell.
Story hook: MaxLinear says it will sell competing retimer silicon to cable
makers and target 20-30% of the 1.6T AEC market; CRDO shares hit a 6-month low.

The picture is the PRODUCT, not the building: a dense copper twinax harness with
its die-cast connector plugging into a switch port, or a macro of that connector
shell and the silicon inside it.

Deliberately NOT a data-centre hallway / server aisle / rack row (banned
site-wide), NOT a server room, NOT a chiller plant, NOT neon / synthwave /
glowing lines / digital art / CGI / 3D render, NOT abstract.

Rules:
- PHOTO-REALISTIC editorial stock photography ONLY, bright and clean.
- TEXT-FREE: no letters/numbers/labels/logos/silk-screen/port numbers/LEDs.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-credo-aec-moat-hero-20261023.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "credo-aec-moat-competition-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no port numbers, no channel numbers, no "
    "serial numbers, no part numbers, no model numbers, no lot codes, no date "
    "codes, no stencilled markings, no laser-etched markings, no die markings, "
    "no printed legends on the connector housing, no silk-screen print on the "
    "circuit board, no silkscreen reference designators, no barcodes, no QR "
    "codes, no two-dimensional matrix codes, no stickers, no decals, no asset "
    "tags, no tie-on labels, no printed paper, no clipboards, no signage, no "
    "warning placards, no nameplates, no brand names, no manufacturer names, "
    "no company names, no corporate logos, no trademarks, no watermarks, no "
    "handwriting, no graffiti, no legible writing of any kind anywhere in the "
    "image. The switch faceplate is plain bare brushed metal with no printing "
    "of any kind and no glowing status lights — every port opening is plain "
    "dark and unlit, with no green or amber indicators and no illuminated "
    "LEDs anywhere. The connector housing is plain matte black moulded "
    "plastic and plain die-cast zinc with no embossed or moulded characters, "
    "no logo badge and no label recess. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no CGI sheen, no neon, no glowing lines, "
    "no light trails, no synthwave, no geometric patterns, no circuit-board "
    "graphic, no network diagram, no fibre-optic light, no laser beam, no "
    "futuristic HUD, no hologram, no augmented-reality overlay, no data "
    "visualisation, no data centre, no server room, no server racks, no "
    "server aisles, no cable trays overhead, no raised floor."
)

PHOTO_TAIL = (
    "Real optical lens blur with creamy out-of-focus background falloff, "
    "honest studio-and-daylight exposure, natural fine sensor grain, subtle "
    "optical vignette, true-to-life colour, clean bright neutral white and "
    "cool grey tones, no plastic CGI sheen, no glossy render, no perfect "
    "symmetry, no 3D visualisation, no digital illustration, no painting, "
    "photorealistic, extremely high detail, professional editorial stock "
    "photography for a financial news site, 16:9 landscape composition, "
    "bright soft professional lighting."
)

PROMPTS = {
    # 1 — PRIMARY: macro of an AEC plug seated in a switch port, twinax pairs
    #     fanning out of the backshell.
    "1": (
        "Professional stock photograph, photo-realistic editorial product "
        "image shot on a 100mm macro lens at f/4 on a full-frame camera, "
        "framed low and close at a shallow three-quarter angle on the front "
        "panel of a data-centre network switch. The subject fills the frame: "
        "a single short, thick active electrical cable plugged into one "
        "rectangular port, its connector shell a plain matte black die-cast "
        "housing with a flat pull-tab latch on top and a machined metal "
        "release bail folded back, seated flush in a plain brushed aluminium "
        "cage that stands a few millimetres proud of the switch's brushed "
        "steel faceplate. The faceplate is plain bare metal running across "
        "the upper half of the frame, its fine horizontal brush grain "
        "catching the light, with three empty neighbouring port openings "
        "beside the occupied one reading as clean dark rectangular slots, "
        "all unlit and completely plain. Emerging from the back of the "
        "connector and sweeping away to the right out of frame is the "
        "cable's harness: a dense flat ribbon of many individually jacketed "
        "twinaxial pairs in matte charcoal-grey and black insulation, "
        "tightly and evenly laid side by side, bound at intervals by slim "
        "black heat-shrink bands and threaded through a small black moulded "
        "comb that keeps the pairs perfectly parallel, the bundle thick and "
        "rigid and slightly flexed so it curves gracefully out of the "
        "backshell and holds its shape. At the very back of the connector, "
        "just behind the strain relief, a short section of the harness is "
        "open where the outer jacket has been cut away: the individual "
        "twinax pairs are exposed there, each a neat figure-of-eight of two "
        "insulated conductors under a thin foil-and-braid shield, and at the "
        "cut ends a few bare copper conductors show as bright warm strands "
        "twisted tightly together, their cut faces gleaming. Fine detail is "
        "everywhere at this distance: the slightly dusty micro-texture of "
        "the moulded plastic, the tiny mould parting line along the "
        "connector's flank, the crisp stamped edge of the metal bail, a "
        "faint fingerprint smudge on the faceplate, minute specks of dust in "
        "the port opening. Bright, clean, even lighting: a large soft key "
        "light from the upper left and a white bounce card on the right fill "
        "the scene almost shadowlessly, so the metal faceplate reads as "
        "bright silver-grey and the black plastic stays open and detailed "
        "rather than crushed, with a soft gentle gradient falling into a "
        "clean pale grey background far behind. Photographic, shallow depth "
        "of field: the connector shell, the port mouth and the nearest "
        "twinax pairs tack sharp, the harness softening as it recedes and "
        "the background dissolving into smooth clean bokeh. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 2 — FALLBACK A: overhead macro of the connector opened up, retimer die
    #     and copper pigtails visible on the internal PCB.
    "2": (
        "Professional stock photograph, photo-realistic editorial technology "
        "image shot on a 90mm macro lens at f/5.6 from directly overhead, "
        "looking straight down at an active electrical cable connector that "
        "has been opened up on a clean matte white work surface. The "
        "connector's top cover is off and set aside at the edge of frame, "
        "exposing its interior: a small dark green printed circuit board "
        "about the size of a matchbox lying inside the plain matte black "
        "die-cast shell, and on that board a single square silicon die in a "
        "flat ceramic package, its lid a polished mirror-dark surface with "
        "faint violet diffraction along the bevel, surrounded by a neat "
        "border of minute surface-mount capacitors and resistors, each a "
        "tiny plain ceramic block with a bright tinned solder fillet, all "
        "completely unmarked. Along one long edge of the board a row of "
        "fine gold-plated contact fingers runs to the card edge that mates "
        "with the switch port; along the opposite edge the cable's twinaxial "
        "pairs are soldered down in a dense even row, each pair's two "
        "conductors stripped and tinned, the bright warm copper catching the "
        "light where the insulation has been cut back, the pairs then "
        "running out of the shell into a flat charcoal-grey ribbon that "
        "sweeps off the right side of the frame. A few short lengths of fine "
        "bare copper wire and one loose twinax pair lie on the white surface "
        "beside the connector, and the small plain metal tweezer that was "
        "used to lift the lid rests at the lower left, all out of focus. "
        "Bright, clean, even overhead light from a large diffused source "
        "directly above plus soft white fill, giving crisp shadowless "
        "detail with gentle modelling in the recesses, the white background "
        "clean and neutral and very slightly warm. Photographic, shallow "
        "depth of field focused on the die and the soldered pigtails, with "
        "the lid at the frame edge and the far end of the ribbon melting "
        "into soft blur. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 3 — FALLBACK B: coiled harness as a studio product shot, connector
    #     standing in the foreground.
    "3": (
        "Professional stock photograph, photo-realistic editorial product "
        "image shot on an 85mm lens at f/8 on a full-frame camera in a "
        "bright studio, a clean still-life of a single short active "
        "electrical cable on a seamless pale grey background. The cable is "
        "laid in a generous loose coil that occupies the right two thirds of "
        "the frame: a thick flat ribbon of many parallel twinaxial pairs in "
        "matte charcoal-black insulation, the individual pairs clearly "
        "readable along the ribbon's edges as an even corduroy of round "
        "insulation ridges, wrapped at two points with slim black "
        "heat-shrink bands, the coil standing a couple of centimetres high "
        "and holding its shape with a slight springy lift at the loose end. "
        "One end of the cable rises toward the camera at the left: its "
        "connector shell a plain matte black die-cast housing with a flat "
        "pull-tab latch and a folded metal bail, angled so its mating face "
        "and the dark rectangular port mouth are visible, the moulded "
        "strain relief flaring where the ribbon enters the backshell, with "
        "a short stretch of the jacket cut back to show a few bare bright "
        "copper conductors twisted at the cut. Everything is completely "
        "plain and unmarked — no printing on the jacket, no moulded "
        "characters on the shell, no label wrap. Bright, clean, even "
        "studio lighting from a large softbox above and slightly left with "
        "a white reflector at the right, casting a soft short shadow onto "
        "the seamless paper and leaving gentle highlights along the top of "
        "the coil and the polished edge of the metal bail. Photographic, "
        "moderate depth of field with the connector and the near edge of "
        "the coil crisp and the far side of the coil softly falling off, "
        "clean commercial product photography, no props, no hands. "
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
    hermes_env = "/home/chino/.hermes/profiles/yachty/.env"
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if line.strip().startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
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
    """Save JPEG at the highest quality that stays under MAX_BYTES."""
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
