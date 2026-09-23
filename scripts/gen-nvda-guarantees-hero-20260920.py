#!/usr/bin/env python3
"""Generate hero for nvidia-ai-guarantees-off-balance-sheet-2026 (fal flux/schnell).

Subject: Nvidia (NVDA) is backstopping the financing of the AI buildout it sells
into — it has guaranteed the residual value of ~$105bn of data-centre leases
behind a 4.25 GW Ohio campus leased to OpenAI, part of roughly $300bn of AI
infrastructure guarantees Big Tech keeps off balance sheets.
Sector: ai (chips / AI infrastructure).

The story is THE HARDWARE AND THE PAPER BEHIND IT, so the picture is a real,
tactile AI accelerator module on a bench — NOT a data hall, NOT a glowing
abstraction of "AI compute".

Scene set for the three attempts (all inside these bounds):
  1 — PRIMARY: tight shallow-depth-of-field editorial photo of a large bare AI
      accelerator module — a big square silicon package on a dense green/black
      PCB with rows of memory modules — held / inspected with gloved hands at
      an electronics quality-assurance bench under a bench lamp, plain unmarked
      board, side/three-quarter lighting, wood-topped ESD bench, blurred lab.
  2 — macro of the underside of an accelerator board: the ball-grid array and
      power-delivery components resting on an anti-static mat, one warm bench
      lamp raking across it.
  3 — a technician in a plain lab coat and gloves seating a large processor
      module into a CPU-style socket on a test bench, shot from slightly above
      at an angle.

BANNED composition: any data-centre long hallway / server aisle / rack row.
BANNED style: neon, synthwave, glowing lines, digital art, 3D render, CGI,
abstract geometry, holograms, HUD overlays, text of any kind.
Deliberately NOT any of the recently used heroes on this site (cleanroom wafer
carrier at a load port, satellite phone on a nautical chart, coffee cup +
notebook on a balcony table, rows of laptops in a provisioning room, phone over
a cafe table, hard-drive platters, parabolic tracking antennas at dusk, a
suburban street at dusk with power lines).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: silicon packages, PCBs, connectors, bench gear and lab garments are
  covered in silkscreen, part numbers, lot codes, logos and UI screens, so all
  lettering, numbers, serial numbers, part numbers, logos and brand names are
  explicitly forbidden. Any display or panel in frame is switched off, angled
  away, or so far out of focus it reads as a flat wash of dark colour.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-nvda-guarantees-hero-20260920.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "nvidia-ai-guarantees-off-balance-sheet-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "lot numbers, no lot codes, no date codes, no die identification markings, "
    "no laser-scribed markings on the silicon, no etched or stamped lettering "
    "on the chip package or the heat spreader, no silkscreen lettering or "
    "reference designators on the printed circuit board, no white board "
    "silkscreen printing, no component markings, no capacitor or resistor "
    "markings, no solder-mask lettering, no pin-one dots with numbers, no "
    "connector labels, no board revision marks, no printed reference "
    "designators such as U1, C245, R12 or J3, no printed part numbers, no "
    "printed alphanumeric codes of any kind on the circuit board, on the chip "
    "package, on the chip lid, on the heat spreader, on the capacitors, the "
    "inductors, the connectors, the sockets or the pin headers, no small "
    "white or yellow silkscreen printing anywhere on the board, no fake "
    "lettering that only resembles text, no user interface, no software "
    "windows, no dashboards, no machine control screens showing content, no "
    "control panel displays, no digital readouts, no instrument displays, no "
    "toolbars, no menus, no icons, no signage, no warning signs, no placards, "
    "no danger notices, no safety stickers, no hazard tape lettering, no lab "
    "coat lettering, no name badges, no lanyards, no pocket or sleeve "
    "markings, no equipment brand plates, no tool nameplates, no manufacturer "
    "names, no company names, no corporate logos anywhere on the chip, the "
    "board, the sockets, the trays, the anti-static mat, the bench or the lab "
    "coats, no cabinet labels, no panel markings, no equipment labels, no dial "
    "faces with numbers, no gauges with numerals, no dials, no meters, no "
    "charts, no arrows, no crosshairs, no alignment marks, no fiducials, no "
    "lettering on the floor tiles, no floor tape markings, no printed "
    "documents, no clipboards with writing, no barcodes, no QR codes, no "
    "datamatrix codes, no RFID tags with any writing, no handwritten markings, "
    "no watermarks, no trademarks, no stickers, no legible writing of any kind "
    "anywhere in the image. Every display, monitor, control screen or "
    "instrument panel in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with "
    "absolutely nothing readable or drawn on it, like an out-of-focus colour "
    "field photograph, not a screen with content. The chip package and the "
    "circuit board are plain unmarked surfaces with no printing whatsoever: "
    "the green solder mask is a smooth uniform field, the chip lid is a bare "
    "polished metal square, the sockets and connectors are plain unmarked "
    "plastic, and the lab garments are plain unmarked solid fabric. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no glowing chip "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, no "
    "augmented-reality graphics, no data center server room, no server racks, "
    "no server aisles, no long data-center hallway, no cable-run composition, "
    "no server lights, no GPU rack hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — PRIMARY: gloved hands inspecting a big bare accelerator module at a QA bench.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2 on a full-frame camera, at an electronics quality-assurance bench "
        "in a lab: a tight, shallow-depth-of-field frame of a large bare AI "
        "accelerator module being inspected with gloved hands. The module is "
        "the subject — a big square chip package, a plain polished metal lid "
        "roughly the size of a matchbox side, seated in the centre of a dense "
        "printed circuit board filled with neat rows of small black memory "
        "modules and rows of tiny surface-mount components, the whole board a "
        "deep green with an even matte finish. The board is held tilted up at "
        "a slight three-quarter angle toward the light by two hands in white "
        "anti-static gloves, thumbs braced on the board's near edge, the "
        "fingers steady and mid-inspection, unposed. The board and the chip "
        "are completely plain and unmarked: no printing, no silkscreen "
        "lettering, no logo, no part numbers, a smooth uniform green surface "
        "and a bare metal lid. The green solder mask carries no printing "
        "whatsoever — no white silkscreen outlines around the components, no "
        "tiny reference codes beside the parts, no stencilled blocks of "
        "lettering — and the rows of memory modules and the tiny components "
        "are plain matte black plastic with nothing written on them. The bench beneath is a warm honey-toned wood top "
        "with a worn edge, and the hands rest just above it. To the side, a "
        "single articulated bench lamp throws warm directional side light that "
        "rakes low across the board, so the rows of memory modules throw short "
        "crisp shadows and the metal lid carries a soft broad highlight with a "
        "bright specular sliver along its chamfered edge. The background is a "
        "blurred workbench laboratory: soft grey instrument masses, a pale wall "
        "and one dark shape reading only as a featureless out-of-focus block, "
        "all dissolved into creamy "
        "bokeh. The bench top is bare apart from the board itself — no loose "
        "papers, no documents, no labelled trays, no taped-down notes. "
        "Very shallow depth of field — the chip package, the nearest "
        "memory modules and the gloved thumbs are crisp, the far corner of the "
        "board and the whole room are heavily blurred. Honest available-light "
        "editorial exposure with warm lamp colour, natural camera noise, "
        "clearly visible fine film grain in the midtones and shadows, subtle "
        "lens vignette, mild chromatic aberration on the high-contrast gold "
        "edges of the board, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — macro of the underside of an accelerator board on an anti-static mat.
    "2": (
        "A real macro photograph, not a render and not computer generated, "
        "shot on a 100mm macro lens at f/4 close up on the underside of a "
        "large AI accelerator board laid face-down on a dark-blue anti-static "
        "mat. The frame is filled with the reverse of the circuit board: a "
        "dense, near-regular field of hundreds of tiny shiny solder balls "
        "forming the ball-grid array under the big square processor footprint, "
        "each ball catching its own pin-sharp pinpoint of light, surrounded by "
        "rows of small dark power-delivery inductors, chunky capacitors and "
        "flat rectangular MOSFET packages. The board is plain and unmarked: a "
        "smooth uniform green solder mask with no silk screen lettering, no "
        "part numbers, no reference designators, no logo, no printed text of "
        "any kind. A single warm bench lamp rakes across the board from a low "
        "angle at the left, so the ball grid throws a long soft pattern of "
        "highlights and the components cast short hard shadows to the right; "
        "the anti-static mat beneath is a matte charcoal-blue textured surface, "
        "also plain and unmarked. The edges of the frame fall away into soft "
        "dark blur, and the far background is a featureless warm grey wash with "
        "nothing identifiable in it. Extremely shallow depth of field — a "
        "narrow band of the solder balls and the nearest components is crisp "
        "and the rest of the board melts into creamy bokeh. Available-light "
        "editorial exposure, warm directional lamp colour, natural camera "
        "noise, visible fine film grain, subtle vignette, mild chromatic "
        "aberration on the bright solder highlights, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — technician seating a big processor module into a socket on a test bench.
    "3": (
        "A genuine documentary photograph taken in a hardware lab, not a render "
        "and not computer generated: shot on a 35mm lens at f/2.8 from "
        "slightly above and behind, at an angle, a technician in a plain white "
        "lab coat and white anti-static gloves seating a large processor module "
        "into a heavy CPU-style socket on an open test bench. The hands are the "
        "sharp focus of the frame: both gloved hands press the big square "
        "metal-lidded module down into the socket with steady, careful pressure, "
        "fingertips spread flat on the lid, elbows angled in, mid-task and "
        "unposed. The socket and the test board are plain and unmarked — a dark "
        "green board with uniform matte finish, a bare metal retention frame "
        "with no printing, no logo, no part numbers, no silkscreen lettering "
        "anywhere. The technician's face is out of frame or turned away; the "
        "coat is plain unmarked fabric with no badges, no pockets with logos, "
        "no lettering. The bench top is a warm wood laminate; beside it a dark "
        "instrument sits as a soft out-of-focus mass with a switched-off face "
        "showing only flat black. Cool overhead lab light from above with a "
        "warm accent from a bench lamp on the right, honest available-light "
        "editorial exposure, deep but gentle shadows under the hands, a few "
        "small dust specks on the board catching the light. Moderate-to-shallow "
        "depth of field: the hands, the module and the socket frame crisp, the "
        "technician's torso and the bench behind softening into creamy bokeh. "
        "Real optical blur, natural camera noise, very slight film grain, "
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


if __name__ == "__main__":
    main()
