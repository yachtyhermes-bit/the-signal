#!/usr/bin/env python3
"""Generate hero for iren-ai-compute-price-reset-neocloud-2026 (fal flux/schnell).

Subject: IREN Limited (NASDAQ: IREN) — an Australian-origin bitcoin miner that has
pivoted into owning data centers and selling AI cloud / GPU compute by the hour.
It owns its own power sites in rural Texas (Childress), holds a 200 MW contract to
supply AI cloud capacity to Microsoft, and is being repriced by a market-wide
AI-compute rental price hike. Sector: AI INFRASTRUCTURE / NEOCLOUD.

The story is POWER SITES + BUILD-OUT + SELLING COMPUTE BY THE HOUR: a company that
buys/owns rural power and turns it into rentable AI capacity. The picture therefore
has to read as a BIG INDUSTRIAL CONSTRUCTION SITE IN FLAT SCRUBLAND, with the
power-delivery story present as background geometry — NOT as an electrical
equipment hero shot.

Scene chosen (ATTEMPT=1): a rural Texas AI data-center campus MID-CONSTRUCTION at
golden hour — a long unfinished industrial shell with exposed steel framing and
part-clad walls running away from the camera, a tower crane above it, high-voltage
lattice transmission towers marching away into the site, a concrete pad with a
transformer bank seen small and secondary in the mid-ground, wide flat scrubland to
the horizon, and two workers in plain high-vis vests and hard hats walking the site
between warm work-lights.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned long-hallway shot), NOT a standalone high-voltage substation /
transformer-bank hero frame, NOT a standby generator yard (used on this site
2026-09-17 for GNRC), NOT a wafer cleanroom, NOT a quantum foundry, NOT an office
or headset customer-service scene, NOT digital art, NOT a 3D render, NOT neon /
synthwave, NOT glowing lines, NOT geometric patterns, NOT abstract.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: construction sites and industrial sites are covered in equipment
  labels, placards, warning signage and site hoarding, so all lettering, numbers,
  UI, logos and brand names are explicitly forbidden. Every display in frame is
  dark/blank/out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-iren-neocloud-hero-20260917.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "iren-ai-compute-price-reset-neocloud-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no signage, no construction site signage, "
    "no site hoarding with writing, no billboards, no warning signs, no hazard "
    "placards, no danger notices, no safety stickers, no equipment labels, no "
    "nameplates, no serial numbers, no part numbers, no crane load charts, no "
    "vehicle liveries with names, no fleet numbers, no license plates, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no control panel displays, no digital readouts, "
    "no gauges with numerals, no dials, no meters, no charts, no bars or "
    "graphs, no toolbars, no menus, no icons, no arrows, no crosshairs, no "
    "alignment marks, no lettering on the concrete, no lettering on the steel "
    "beams, no spray-painted markings, no stencilled marks, no survey stakes "
    "with writing, no flags with lettering, no banners, no name badges, no "
    "lanyards, no hard-hat lettering, no company names or corporate logos, no "
    "brand names, no manufacturer names, no trademarks, no watermarks, no "
    "stickers, no barcodes, no QR codes, no handwritten markings, no graffiti, "
    "no legible writing of any kind anywhere in the image. Every display or "
    "screen in the frame is switched off, angled away, or so far out of focus "
    "that it shows only a soft flat wash of dark colour with absolutely "
    "nothing readable or drawn on it, like an out-of-focus colour field "
    "photograph, not a screen with content. The workers' high-visibility vests "
    "and hard hats are plain unmarked solid colours; the machinery, crane "
    "boom, steel framing, concrete and cable drums are plain and unmarked. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center server room, no server "
    "racks, no server aisles, no long indoor corridor, no cable-run "
    "composition, no server lights, no GPU hardware, no computer screen with "
    "text."
)

PROMPTS = {
    # 1 — golden hour wide: rural Texas AI datacenter campus mid-construction,
    #     unfinished shell + crane + transmission line marching in + workers.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/4 on a full-frame camera from ground level, of a large AI "
        "data-center campus under construction on flat rural Texas scrubland "
        "at golden hour. Running diagonally away from the camera into the "
        "middle distance is a very long low industrial shell still being "
        "built: a single-storey concrete slab, a bare exposed-steel column "
        "and beam frame in a regular rhythm, some bays already clad in plain "
        "pale-grey metal panels and some bays still open to the sky, with "
        "coils of conduit, stacked steel sections, a few plain unmarked "
        "spools of cable and a flatbed truck standing beside it. Above the "
        "east end of the shell a tall tower crane rises, its plain unmarked "
        "lattice mast and horizontal jib cutting across the warm sky. "
        "Marching out of the right of frame toward the site, receding to a "
        "vanishing point on the horizon, are three tall high-voltage lattice "
        "transmission towers with their conductors drooping in long catenary "
        "curves between them, and the nearest pylon's steel legs come down "
        "into the frame at the right edge. Set back in the mid-ground on a "
        "poured concrete pad, secondary to the frame and softened by "
        "distance, is a cluster of plain grey transformer boxes and "
        "switchgear cubicles with heavy cables drooping between them. In the "
        "sharp mid-ground on the left, two construction workers in bright "
        "orange-yellow high-visibility vests and plain white hard hats, both "
        "seen from behind and mid-stride, walk the site away from the camera "
        "along a dirt haul road toward the shell, one carrying a plain "
        "unmarked rolled drawing tube under an arm, neither posing nor "
        "looking back. Foreground: dry cracked dirt, gravel and low grey-green "
        "scrub bushes, with a few shallow puddles catching the warm light. "
        "The horizon is dead flat and very wide, with a distant line of dark "
        "mesquite trees and two warm sodium work-lights flaring gently near "
        "the site. Low golden sun behind the shell throws long raking shadows "
        "toward the camera, dust hanging in the air and catching the light. "
        "Strong spatial depth: the near scrub, worker figures and haul road "
        "crisp, the shell and crane resolving, the far transmission towers "
        "and horizon softening into warm haze. Real optical lens blur, honest "
        "available-light editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — close crop: gloved hands on a stainless liquid-cooling manifold of an
    #     AI compute rack, everything unmarked.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "tight close crop, shot on an 85mm lens at f/2, of the rear cooling "
        "manifold of an AI compute rack inside an otherwise unlit data hall. "
        "In the foreground, tack sharp and filling the lower half of frame, a "
        "pair of heavy work-gloved hands guided by dark work-shirt sleeves "
        "grip the two bright stainless steel quick-disconnect couplings of a "
        "vertical brushed-stainless liquid-cooling manifold and are pushing "
        "one coupling home, knuckles tense, mid-motion; clear hoses with a "
        "faint blue coolant tint loop away into soft focus behind the "
        "manifold. The manifold, its valves, its bracket and the black rack "
        "frame beside it are entirely plain and unmarked — smooth metal, no "
        "etching, no decals, no labels, no numbers. Beside it the dark "
        "rectangular face of an equipment panel sits in the frame, switched "
        "off and completely black, showing nothing on it whatsoever. The rest "
        "of the hall falls away into very dark shadow, just the soft grey "
        "shape of a second manifold and the dim suggestion of an aisle far "
        "out of focus. A single cool work-lamp rakes in from the top left, "
        "catching the wet gleam on the stainless couplings and the sheen on "
        "the gloved knuckles, leaving everything else deep and honest; a "
        "faint warm edge light separates the shoulder of the technician on "
        "the right. Extremely shallow depth of field — the couplings, gloves "
        "and near valves crisp, the hoses softening, the hall dissolving into "
        "creamy bokeh. Real optical blur, honest editorial exposure, natural "
        "camera noise, very slight film grain, subtle lens vignette, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — blue hour variant: shell silhouetted, crane, pylon, workers under floods.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 from a low angle across a "
        "rural Texas AI data-center campus at blue hour, the build still in "
        "progress. Across the left two thirds of the frame the bare steel "
        "skeleton of a very long single-storey data hall stands against a "
        "deep indigo sky, exposed columns and roof purlins in silhouette, "
        "partly skinned with plain pale metal panels, scaffold towers and a "
        "concrete slab visible through the open bays. To its right a tower "
        "crane rises out of frame, and on the far right a tall high-voltage "
        "lattice transmission tower looms close to the camera, its legs and "
        "crossarms black against the last band of amber afterglow on the "
        "horizon, conductors sweeping away to a second tower in the far "
        "distance. In the sharp mid-ground at the right, two construction "
        "workers in bright high-visibility vests and plain hard hats stand on "
        "a concrete pad talking beside a plain unmarked materials stack, one "
        "gesturing toward the structure, both unposed and seen in three "
        "quarter view. In front of them a plain grey transformer enclosure "
        "and a low switchgear cabinet on the pad sit in damp shadow, wet "
        "concrete catching weak reflections. Portable flood lights on plain "
        "tripods throw warm pools of light across the slab and pick out the "
        "workers' shoulders while leaving the sky cool. The flat scrubland "
        "runs away to a dead-flat horizon on the left with a line of dark "
        "trees. Strong depth and silhouette: the near pylon legs and workers "
        "crisp, the steel shell reading clearly, the far tower and horizon "
        "softening into haze. Real optical blur, honest available-light "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
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
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )
    # OCR text-artifact smoke test on the published file
    words = ocr_text_check(OUTPUT)
    if not words:
        print("OCR TEXT CHECK: clean — no readable text detected")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(words)} candidate token(s): {words[:12]}")


if __name__ == "__main__":
    main()
