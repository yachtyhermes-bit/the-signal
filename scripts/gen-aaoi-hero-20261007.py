#!/usr/bin/env python3
"""Generate hero for aaoi-hyperscaler-optical-transceiver-ramp-2026 (fal flux/schnell).

Subject: Applied Optoelectronics (NASDAQ: AAOI) — high-speed optical transceivers
(400G / 800G / 1.6T) and laser-diode manufacturing for hyperscale AI data centers.
Thesis: AAOI builds the optical engines, laser diodes and external light sources that
connect GPU clusters with fiber optics inside hyperscale AI data centers.

Scene chosen (per task brief): a CLEANROOM SEMICONDUCTOR / OPTICAL-PHOTONICS setting —
a bunny-suited fab technician (or precision robotic pick-and-place) assembling and
inspecting optical laser transceiver modules / fiber-optic laser diodes / silicon
photonics packaging under clean lab lighting. Shallow depth of field, professional
lighting, realistic photography.

Deliberately NOT a data-center hallway / server aisle / server racks / cable runs.
No abstract art, no digital art, no neon/synthwave, no glowing lines, no geometric
patterns.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon, synthwave,
  CGI, 3D render, cartoon, glowing lines, light trails, HUD, holograms.
- NO data-center hallway / server aisle / server racks / cable runs (banned).
- TEXT-FREE / no legible text: no readable words, numbers, labels, logos, gibberish.
- FACES NOT clearly readable (mask/visor, side/behind, out of focus) or anonymous.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-aaoi-hero-20261007.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "aaoi-hyperscaler-optical-transceiver-ramp-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no glyphs, no code, no captions, no labels, no legends, no menus, no file "
    "names, no browser chrome, no logos, no brand names, no company marks, no watermarks, no "
    "signatures, no garbled lettering. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no video-game look, no neon, no synthwave, no glowing holographic lines, "
    "no light trails, no futuristic HUD graphics, no augmented-reality overlays, no abstract "
    "digital patterns, no circuit-board graphics overlay. Not a data-center hallway, no server "
    "aisle, no server racks, no cable runs, no rack of network gear, no abstract cyberspace."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, shot on a full-frame camera with a 50mm "
        "macro-capable lens at f/2.5, not a render and not CGI: inside a bright, ultra-clean "
        "semiconductor / optical-photonics cleanroom. In tack-sharp focus in the foreground a "
        "technician wearing a full white cleanroom bunny suit, hairnet and safety glasses sits "
        "at a precision optical assembly station, using fine tweezers to place a tiny gold "
        "laser-diode chip onto a small optical transceiver module held in a machined metal "
        "fixture under a stereo microscope. The transceiver module is a small rectangular "
        "device — brushed aluminium housing, tiny gold-plated pins, a short coil of thin "
        "single-mode fiber optic pigtail with a small blue connector coupler emerging from it. "
        "Tiny fibre-optic strands, precision components, a lens and a micro ribbon of gold "
        "bond wires are visible on the work surface. The technician is seen from behind and in "
        "three-quarter profile, face turned away and only partly visible through the visor and "
        "glasses so it is not identifiable. The cleanroom around them is softly blurred: "
        "stainless-steel benches, a laminar-flow hood, plain white walls and ceiling panels, "
        "other technicians out of focus in the background, all bathed in even, bright, diffuse "
        "cleanroom light. Shot at f/2.5 with very shallow depth of field — the tweezers, the "
        "optical module and the tiny die are razor sharp while the room melts into creamy "
        "optical bokeh; real lens blur, natural sensor noise, very slight film grain, subtle "
        "vignette, honest realistic textures on metal, glass and fabric, no CGI sheen, no "
        "perfect symmetry. Photorealistic, extremely high detail, 8k resolution, authentic "
        "editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "Professional editorial stock photograph taken on a real camera, 85mm lens at f/2.8, "
        "not computer generated: a macro view inside a pristine semiconductor and silicon "
        "photonics cleanroom. The sharp focal point is a precision robotic pick-and-place arm "
        "with a tiny vacuum nozzle gently lowering a miniature optical laser diode onto a "
        "small silicon-photonics photonic integrated circuit die mounted in a gold-plated "
        "package on a machined fixture. Around it a shallow tray holds several finished and "
        "part-finished optical transceiver modules — small brushed-aluminium housings with "
        "gold pins and short loops of thin fibre-optic pigtail cable with blue and green "
        "connector couplers. Fine gold bond wires, a tiny lens, and precise metal tooling are "
        "crisply visible. In the soft-blurred background, a technician in a full white "
        "cleanroom bunny suit and hairnet stands out of focus, seen from behind and to the "
        "side so the face is not visible, monitoring the process on a plain screen turned away "
        "from the camera so nothing on it is legible. The cleanroom is bright and even, lit by "
        "diffuse ceiling light, plain white walls, stainless-steel bench; nothing self-lit, no "
        "neon, no glowing lines. Very shallow depth of field, the robotic nozzle and the die "
        "tack sharp, the room falling into creamy bokeh; real optical lens blur, natural "
        "sensor noise, very slight film grain, subtle vignette, honest textures on metal, "
        "glass and plastic, no CGI sheen, no perfect symmetry. Photorealistic, extremely high "
        "detail, 8k resolution, authentic editorial photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph, real camera, 35mm lens at f/2.2, not a "
        "render: a bright modern optical-component manufacturing cleanroom. In the sharp "
        "foreground a technician in a full white cleanroom bunny suit, hairnet and safety "
        "glasses works at a stainless-steel bench, carefully inspecting a small fibre-optic "
        "optical transceiver module through a stereo microscope, one gloved hand holding fine "
        "tweezers, a short coil of thin single-mode fibre-optic pigtail with a blue connector "
        "coupler resting on a clean mat beside a row of several identical tiny brushed-metal "
        "transceiver modules. First light of the cleanroom is bright and diffuse. The "
        "technician is shown from behind and in three-quarter profile, the face hidden by the "
        "hood, visor and glasses so it is not identifiable. Behind them the cleanroom extends "
        "into soft blur: laminar-flow hoods, polished stainless benches, plain white walls and "
        "ceiling panels, another bunny-suited technician out of focus in the mid-ground, a "
        "cart of parts. Very shallow depth of field with the tweezers, the module and the "
        "fibre pigtail sharp and the room behind melting into creamy bokeh; real lens blur, "
        "natural sensor noise, very slight film grain, subtle vignette, honest realistic "
        "textures on metal, glass, fibre and fabric, no CGI look, no illustration, no perfect "
        "symmetry. Photorealistic, extremely high detail, 8k resolution, authentic editorial "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "4": (
        "Photojournalistic candid documentary photograph, shot on a Fujifilm X-T5 with a 56mm "
        "lens at f/2, real available cleanroom light, unretouched, not a render and not CGI: "
        "inside a manufacturing cleanroom for high-speed optical transceivers and laser "
        "diodes. In the sharp foreground on the stainless-steel bench rest a small tray of "
        "finished optical transceiver modules — compact brushed-aluminium and gold-plated "
        "housings, each with a short pigtail of thin single-mode fibre optic cable ending in a "
        "small blue or green LC-style connector coupler — beside a fibre-cleaving tool and a "
        "reel of bare optical fibre. A technician in a white bunny suit stands just behind, "
        "seen from behind and to the side, both gloved hands carefully placing a tiny laser "
        "diode onto a module in a precision fixture; the face is turned away and not "
        "identifiable. The cleanroom is bright and diffuse with plain white walls, ceiling "
        "panels and laminar-flow hoods softly out of focus; another operator works further "
        "down the bench in soft blur. Genuinely imperfect candid composition, very shallow "
        "depth of field with the modules and fibre sharp and everything behind melting into "
        "creamy bokeh, natural sensor grain, faint chromatic aberration at the frame edges, "
        "realistic fabric and skin texture, no studio lighting, no neon, no glowing lines, no "
        "perfect symmetry. Photorealistic, extremely high detail, authentic editorial "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro lens at f/2.8 on a "
        "full-frame camera, of the precision assembly of an optical laser transceiver inside a "
        "bright semiconductor cleanroom. In the tack-sharp centre of frame a small optical "
        "module sits in a machined metal fixture on a stainless-steel bench: a compact "
        "rectangular housing of brushed aluminium and gold plating with a tiny window, fine "
        "gold-plated pins, and a short, neatly coiled pigtail of thin single-mode fibre-optic "
        "cable ending in a small blue connector coupler. A gloved hand holding fine anti-static "
        "tweezers is mid-motion, placing a tiny gleaming laser-diode chip onto the module, "
        "crisply lit from the front and side by even diffuse cleanroom light. The hand and arm "
        "belong to a technician in a white cleanroom bunny suit, only a sleeve and glove in "
        "frame; a soft-focus bunny-suited colleague stands further back, seen from behind so "
        "the face is not visible. The cleanroom around the work dissolves into creamy bokeh: "
        "polished stainless benches, plain white walls and ceiling panels, a laminar-flow "
        "hood. Warm-neutral balanced lighting, soft realistic shadows, nothing self-lit, no "
        "neon, no glowing lines. Very shallow depth of field, the die, tweezers and module "
        "razor sharp; real optical lens blur, honest available-light exposure, natural camera "
        "noise, very slight film grain, subtle lens vignette, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital illustration. "
        "Photorealistic, extremely high detail, professional editorial stock photography, 16:9 "
        "landscape composition. " + NO_TEXT
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
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
