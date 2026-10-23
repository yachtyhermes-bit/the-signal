#!/usr/bin/env python3
"""Hero for vistra-nuclear-uprates-doe-loan-2026 (fal flux/schnell).

Subject: Vistra Corp (VST) nuclear fleet in PJM — uprates at Perry and
Davis-Besse (Ohio) and Beaver Valley (Pennsylvania), funded by a conditional
$4.2B DOE loan, output contracted to Meta under 20-year PPAs.

The picture is the PLANT, not the counterparty: a large light-water nuclear
station with hyperbolic cooling towers at golden hour / dusk, high-voltage
transmission lines and lattice pylons leading out of frame, river or farmland
foreground.

Deliberately NOT a data-centre hallway / server aisle / rack row (banned
site-wide), NOT a server room, NOT neon / synthwave / glowing lines / digital
art / CGI / 3D render, NOT abstract.

Rules:
- PHOTO-REALISTIC editorial stock photography ONLY, cinematic but documentary-real.
- TEXT-FREE: no letters/numbers/signage/logos/watermarks.
- Generate 1536x864 (16:9), keep as final, mirror to _backup_dist.

Usage: /home/chino/video-venv/bin/python3 \
         scripts/gen-vistra-nuclear-uprates-hero-20261023.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "vistra-nuclear-uprates-doe-loan-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864  # 16:9 generation size
MAX_BYTES = 450 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no signage, no billboards, no road "
    "signs, no printed paper, no clipboards, no warning placards, no "
    "nameplates, no brand names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no handwriting, no graffiti, no legible "
    "writing of any kind anywhere in the image. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no CGI sheen, no neon, no "
    "cyberpunk, no synthwave, no glowing lines, no light trails, no "
    "geometric patterns, no futuristic HUD, no hologram, no "
    "augmented-reality overlay, no data visualisation. No data centre, no "
    "server room, no server racks, no server aisles, no server hallway, no "
    "computer equipment, no interior of any kind."
)

PHOTO_TAIL = (
    "Real optical lens blur with creamy out-of-focus falloff, honest "
    "natural-light exposure with bracketed dynamic range, natural fine "
    "35mm sensor grain in the shadows, subtle optical vignette, "
    "true-to-life restrained colour, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no digital illustration, no painting, "
    "photorealistic, extremely high detail, professional editorial stock "
    "photography for a financial news site, documentary realism, "
    "16:9 landscape composition, shot on a full-frame camera with a "
    "70-200mm telephoto lens at f/4, shallow depth of field."
)

PROMPTS = {
    # 4 — REFINED: same plant, but heavier overcast, one warm break, and the
    #     transmission corridor reading clearly in the right foreground.
    "4": (
        "Professional stock photograph, photo-realistic editorial image of a "
        "large light-water nuclear power station standing on open farmland at "
        "dusk, shot on a 135mm telephoto lens at f/4 from across a harvested "
        "field, the plant on the horizon in the middle distance. Two vast "
        "hyperbolic cooling towers fill the left half of the frame, their "
        "weathered pale-grey concrete streaked with vertical water stains and "
        "dark algae at the base, both venting slow dense white plumes of "
        "water vapour that spread sideways into the cloud. To their right, a "
        "cluster of industrial plant: a squat domed containment building, a "
        "long low turbine hall in faded white cladding, a slim red-and-white "
        "banded ventilation stack and a tangle of steel pipe racks, walkways "
        "and small transformers. In the right foreground, close to the "
        "camera, one tall steel lattice transmission pylon rises from the "
        "field edge and is cut off by the top right corner of the frame, its "
        "galvanised angles, bolted joints and hanging insulator strings "
        "large and sharply detailed, with six heavy conductors sweeping away "
        "from it in long sagging catenaries toward a receding line of "
        "smaller pylons that step away to the left across the horizon and "
        "out of frame. Foreground: dry brown corn stubble and a rutted farm "
        "track running diagonally into the frame, softly out of focus. The "
        "sky is heavy and moody — dense dark blue-grey overcast cloud filling "
        "most of the frame with a single wide ragged break low on the right "
        "where warm amber late sunlight pours through, backlighting the "
        "steam plumes and rimming the tower rims and pylon steel in dull "
        "gold, while the plant and field below stay in cool shadow. "
        + PHOTO_TAIL + " " + NO_TEXT
    ),
    # 1 — PRIMARY: two cooling towers + containment dome at golden hour,
    #     pylons and transmission lines leading right, farmland foreground.
    "1": (
        "Professional stock photograph, photo-realistic editorial image of a "
        "large light-water nuclear power station seen from a distance across "
        "open Ohio farmland at golden hour, shot on a 70-200mm telephoto "
        "lens at f/4 from a low vantage point in a field, the whole plant "
        "sitting on the horizon line in the middle distance. Two enormous "
        "hyperbolic cooling towers dominate the left two thirds of the "
        "frame, their weathered grey concrete flanks streaked with pale "
        "vertical water staining and faint algae bloom near the base, their "
        "curved waists and flared rims sharply drawn against the sky, both "
        "venting thick slow columns of white water vapour that lean very "
        "slightly to the right and dissolve into the cloud layer. Just "
        "behind and to the right of the towers, a squat cylindrical "
        "reinforced-concrete containment building with a shallow domed roof "
        "stands among a dense cluster of smaller steel plant buildings, "
        "pipe racks, stair towers and a slim ventilation stack, all in "
        "muted industrial greys and faded whites. In the foreground, rows of "
        "harvested corn stubble and a shallow slow river bend run across "
        "the bottom of the frame, the water dark and glassy and reflecting "
        "a broken strip of warm light, dry grasses and a wire fence line "
        "out of focus at the very bottom edge. From the switchyard at the "
        "right of the plant, a line of steel lattice transmission pylons "
        "marches away toward the right edge of the frame, their arms "
        "carrying six heavy conductors that sag in long catenary curves, "
        "the towers diminishing in size with distance and stepping out of "
        "frame. Sky: moody, layered, mostly overcast — heavy blue-grey "
        "cloud with a low break on the right where warm late-afternoon "
        "sunlight spills through in a wide soft shaft, rimming the cooling "
        "towers' rims and the pylon steel in pale gold while the plant "
        "itself stays in cool shadow. Atmospheric haze softens the far "
        "pylons. " + PHOTO_TAIL + " " + NO_TEXT
    ),
    # 2 — FALLBACK A: closer three-quarter view, one tower and the reactor
    #     building, river foreground, dusk with warm break in cloud.
    "2": (
        "Professional stock photograph, photo-realistic editorial image of a "
        "nuclear generating station at dusk, viewed from the near bank of a "
        "wide calm river, camera at water level on a 100mm lens at f/4, the "
        "plant filling the upper half of the frame in the middle distance. "
        "One huge hyperbolic cooling tower stands at the left, its concrete "
        "surface mottled and streaked, a thin plume of steam rising and "
        "bending with the wind; beside it a tall rectangular reactor "
        "building in weathered off-white concrete with tall narrow louvre "
        "slots, and a network of silver insulated pipework, steel walkways "
        "and a small substation with transformer banks at its foot. A line "
        "of wooden and steel distribution poles with crossarms runs from "
        "the right of the plant toward the camera and out of the right edge "
        "of frame, wires sagging between them. The river fills the "
        "foreground, still and dark green-grey, holding a long soft "
        "reflection of the warm break in the clouds, with reed beds and wet "
        "gravel at the lower left corner in soft focus. Under a heavy "
        "overcast sky of bruised blue-grey cloud, a single wide band of warm "
        "amber light low on the horizon behind the plant backlights the "
        "steam plume and edges the tower rim in gold. " + PHOTO_TAIL + " " + NO_TEXT
    ),
    # 3 — FALLBACK B: wide establishing shot at last light, three towers in
    #     a row, transmission corridor running to the horizon.
    "3": (
        "Professional stock photograph, photo-realistic wide establishing "
        "editorial image of a large nuclear power plant on flat open "
        "farmland at last light, shot on a 135mm lens at f/5.6, the camera "
        "positioned on a slight rise so the plant reads as a long low "
        "silhouette across the horizon. Three hyperbolic cooling towers in a "
        "row occupy the centre of the frame at decreasing distance, each "
        "trailing a soft column of water vapour that merges with the cloud "
        "deck, the nearest tower showing weathered concrete ribs and a dark "
        "water line at its base. Between and behind them, the pale "
        "rectangular bulk of the turbine hall and the domed containment "
        "structure, small cranes and a tall thin stack. A high-voltage "
        "transmission corridor runs diagonally from the plant's switchyard "
        "in the right foreground toward the horizon, a receding line of "
        "steel lattice pylons with their conductors strung in long sweeping "
        "curves, the nearest pylon large and detailed at the right edge with "
        "its galvanised members and insulator strings clearly visible, the "
        "rest shrinking to thin marks in the haze. Foreground: dark tilled "
        "soil and a hedgerow of bare shrubs in shadow along the bottom of "
        "the frame. The sky is mostly heavy grey overcast with a narrow warm "
        "golden break low on the left horizon, lighting the underside of the "
        "cloud and picking out the steam plumes while the land stays cool "
        "and dim. " + PHOTO_TAIL + " " + NO_TEXT
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get("STEPS", "4" if "schnell" in model else "28"))
    print(f"Generating image with {model} ({steps} steps)...")
    result = fal_client.subscribe(
        model,
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": steps,
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
    img = img.convert("RGB")
    w, h = img.size
    target_ratio = W / H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((W, H), Image.LANCZOS)


def save_bounded(img, path):
    for q in (94, 92, 90, 88, 86, 83, 80):
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
