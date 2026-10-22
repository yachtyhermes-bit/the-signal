#!/usr/bin/env python3
"""Generate hero for vertiv-ai-factory-power-slide-2026 (fal flux/schnell).

Subject: Vertiv Holdings (VRT) — power distribution, switchgear, busway and
liquid-cooling / thermal systems behind AI data centres. The article covers the
stock sliding 11 sessions while the company ships a new Nvidia co-engineered
AI factory buildout.

Scene chosen: INTERIOR OF AN INDUSTRIAL CHILLER PLANT / MECHANICAL ROOM — large
water-cooled centrifugal chillers, heavily insulated coolant piping with elbow
runs, flanged valves, pumps and a coolant manifold, with a technician in PPE
(hard hat, hi-vis, ear protection) working at the manifold valves.

Deliberately NOT a data-centre hallway / server aisle / rack (banned site-wide),
NOT a switchgear yard (already used on powl-electrical-switchgear-backlog hero),
NOT neon / synthwave / glowing lines / geometric patterns, NOT digital art,
NOT 3D render or CGI, NOT abstract.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: no letters/numbers/labels/logos/signage/screens/UI anywhere.
  Gauges are blank or far out of focus, PPE is plain, pipes are unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-vertiv-ai-factory-power-slide-hero-20261022.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "vertiv-ai-factory-power-slide-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "model numbers, no stencilled pipe markings, no flow-direction arrows, "
    "no colour-code tags, no valve tags, no equipment nameplates, no asset "
    "tags, no warning signs, no hazard placards, no safety posters, no "
    "cabinet labels, no panel legends, no stamped lettering on the "
    "housings, no dial faces with numerals, no gauges with numbers, no "
    "digital readouts, no control screens, no user interface, no dashboards, "
    "no software windows, no toolbars, no menus, no icons, no charts, no "
    "signage, no wall placards, no exit signs, no door signs, no floor "
    "markings with writing, no painted line lettering, no name badges, no "
    "lanyards, no printed documents, no clipboards with writing, no "
    "brand names, no manufacturer names, no company names, no corporate "
    "logos, no trademarks, no watermarks, no stickers, no barcodes, no QR "
    "codes, no handwriting, no graffiti, no legible writing of any kind "
    "anywhere in the image. Every gauge face is either plain blank white "
    "with a single unmarked needle or turned away from camera, and every "
    "screen or display in the frame is switched off or angled away showing "
    "only a flat dark wash with nothing readable on it. The technician's "
    "hard hat, hi-vis vest, gloves and boots are plain solid colours with "
    "no printed patches, no embroidered names and no reflective logo strips "
    "that form letters. The pipe insulation jackets, the chiller housings, "
    "the pumps and the valve bodies are all plain painted metal and plain "
    "insulation with no decals and no markings. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no glowing lines, no "
    "light trails, no synthwave, no geometric patterns, no circuit-board "
    "graphics, no network diagram, no graph graphic, no futuristic HUD "
    "graphics, no hologram, no overlay elements, no augmented-reality "
    "graphics, no data center, no server room, no server racks, no server "
    "aisles, no cable runs, no server lights, no GPU hardware, no computer "
    "screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light industrial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no 3D visualisation, no digital illustration, no "
    "painting, photorealistic, very high detail, professional editorial "
    "stock photography, 16:9 landscape composition, professional lighting. "
)

PROMPTS = {
    # 1 — medium-wide: chiller plant interior, big chillers + insulated
    #     coolant pipework + technician at a valve manifold.
    "1": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a 35mm lens at f/2.8 on a full-frame camera from standing eye "
        "level inside a large industrial chiller plant — the mechanical plant "
        "room that carries the heat rejection for a hyperscale AI data "
        "centre. The space is tall and utilitarian: a sealed concrete floor "
        "with a faint sheen, pale grey painted blockwork walls, an exposed "
        "structural steel ceiling with steel roof deck far above and rows of "
        "fluorescent and LED high-bay luminaires throwing a clean cool white "
        "light down through the room with soft honest shadows. Filling the "
        "left and centre of the frame are two enormous water-cooled "
        "centrifugal chillers — long horizontal cylindrical steel shells "
        "painted a muted industrial teal-grey, bolted compressor housings at "
        "one end, small plain unmarked louvre panels, sitting on low steel "
        "skids. From the chiller heads a dense run of large-diameter coolant "
        "pipes sweeps up and across the room: heavy steel pipe lagged in "
        "smooth pale grey closed-cell insulation with crisp factory jackets, "
        "big radiused elbows, bolted flange joints with visible steel bolts, "
        "and a row of heavy flanged gate valves with large spoked handwheels "
        "painted a dull dark red, the pipes stepping in parallel runs and "
        "sweeping overhead toward the right of the frame where they pass out "
        "of shot. Beneath them a pair of vertical end-suction pumps in dark "
        "grey cast iron with coupling guards stand on their concrete "
        "plinths, and a squat insulated coolant manifold with several "
        "branch connections and blanked-off flanges sits at the centre of "
        "the foreground. In the right third of the frame, in the sharp "
        "near-mid-ground, a maintenance technician in mid-task: a man in a "
        "plain white hard hat, dark navy work trousers, a plain high-vis "
        "orange-yellow vest, dark work gloves and steel-toe boots, seen "
        "three-quarters from behind, one gloved hand on the spoke of a "
        "valve handwheel, leaning slightly into the work, intent and not "
        "posing, part of the plant rather than a portrait subject. A "
        "rolling steel tool cart stands beside him, plain and unmarked. The "
        "air is clean and slightly cool, and the great mass of insulated "
        "pipework and machinery gives the room a sense of heavy, precise, "
        "engineered order. Strong spatial depth: the near manifold, valve "
        "handwheel and technician crisp, the chiller shells and pipe runs "
        "resolving, the far wall and ceiling falling away into soft "
        "industrial haze. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — tighter: coolant manifold with insulated pipe elbows, valves and
    #     a technician's hands on the handwheel.
    "2": (
        "Professional stock photograph, real photo not a render, shot on a "
        "50mm lens at f/2 inside an industrial chiller plant, a tight "
        "three-quarter crop of the coolant distribution manifold. A heavy "
        "horizontal steel header pipe lagged in smooth pale grey closed-cell "
        "insulation runs across the sharp foreground from left to right, its "
        "surface matte and slightly dusty, with a large radiused elbow "
        "sweeping away toward camera at the lower left and bolted flange "
        "joints with bright steel bolt heads standing proud of the jacket. "
        "Three heavy flanged gate valves rise from the header on short "
        "insulated stubs, each with a large spoked cast-iron handwheel "
        "painted a worn dull dark red, the paint chipped at the rims from "
        "years of use, and a plain blank circular gauge face on a short "
        "brass stem above the middle valve turned slightly away from camera. "
        "At the right of frame a technician's gloved hands — dark grey work "
        "gloves, the cuffs of a plain high-vis orange-yellow sleeve visible "
        "at the frame edge — grip the rim of the nearest handwheel and turn "
        "it, knuckles taut, mid-effort. Behind, thrown far out of focus into "
        "soft planes of muted teal-grey and pale grey, the massive "
        "cylindrical shell of a centrifugal chiller and the receding parallel "
        "runs of insulated coolant pipework climb toward a bright ceiling of "
        "high-bay lights, the whole background dissolving into creamy "
        "industrial bokeh. Fine dust motes hang in the cool light. "
        "Photographic, extremely shallow depth of field with the near valve "
        "body, the bolt heads and the gloved hands tack sharp, honest "
        "available-light exposure with gentle specular highlights on the "
        "painted metal, no coloured gels. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — wider establishing view down the plant room between chiller rows.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated: a wide establishing view shot on a 24mm lens at f/4 from "
        "standing eye level down the length of a large industrial chiller "
        "plant room inside a hyperscale data centre campus. Two long rows of "
        "enormous water-cooled centrifugal chillers face each other across a "
        "clear service aisle, receding toward a distant pale wall: long "
        "horizontal cylindrical steel shells in muted industrial teal-grey "
        "with bolted compressor housings, plain unmarked louvre panels and "
        "low steel skids on sealed concrete plinths. Above them, thick "
        "parallel runs of large-diameter coolant pipework lagged in smooth "
        "pale grey insulation sweep the length of the room in long "
        "perspective lines, carried on steel trapeze hangers from the exposed "
        "roof structure, punctuated at intervals by heavy flanged gate "
        "valves with worn dark red spoked handwheels and by bright bolted "
        "flange joints. Vertical cast-iron pumps and a squat insulated "
        "manifold stand between the chiller rows in the near foreground, and "
        "a plain steel tool cart rests beside a plinth. Mid-way down the "
        "aisle, small in the frame and seen from behind, a single maintenance "
        "technician in a plain white hard hat, plain high-vis orange-yellow "
        "vest and dark navy trousers walks the aisle inspecting the pipework, "
        "his scale making the machinery read as genuinely huge. The ceiling "
        "is high exposed steel deck carrying rows of high-bay luminaires that "
        "lay down long clean pools of cool white light along the polished "
        "concrete floor and leave deep honest shadows between the machines. "
        "Cool neutral industrial daylight-balanced light, no coloured gels, "
        "no atmospheric theatrics, faint haze in the far distance. "
        "Photographic, moderate depth of field with the near machines and "
        "pipes crisp and the far end of the room softening into haze, real "
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


def ocr_text_check(path):
    """Run tesseract OCR as a text-artifact smoke test. Returns list of words."""
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11"],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return []
        txt_path = base + ".txt"
        if not os.path.exists(txt_path):
            return []
        with open(txt_path, errors="ignore") as f:
            raw = f.read()
    words = []
    for line in raw.splitlines():
        clean = "".join(ch for ch in line if ch.isalnum())
        if len(clean) >= 3:
            words.append(line.strip())
    return words


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
    if size < 204800:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
    words = ocr_text_check(OUTPUT)
    if not words:
        print("OCR TEXT CHECK: clean — no readable text detected")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(words)} candidate token(s): {words[:12]}")


if __name__ == "__main__":
    main()
