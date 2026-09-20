#!/usr/bin/env python3
"""Generate hero for globalfoundries-quantum-foundry-chips-award-2026 (fal flux/schnell).

Subject: GlobalFoundries (GFS) has finalized a $375M CHIPS Act award to scale
quantum-chip wafer fabrication at its Malta, New York fab — 300mm wafers on the
22FDX node, cryogenic CMOS control chips designed to run at millikelvin
temperatures inside quantum computers. Sector: SEMICONDUCTOR / QUANTUM HARDWARE.

The story is a FABRICATING WAFERS ON A REAL SEMICONDUCTOR PRODUCTION FLOOR, so
the picture is a cleanroom / fab interior with 300mm silicon — NOT a data hall
and NOT a glowing abstraction of a "quantum" idea.

Scene set for the three attempts (all inside these bounds):
  1 — cleanroom production floor: a 300mm wafer in its carrier at a load port.
  2 — gloved engineer in a full-body white cleanroom suit holding a bare 300mm
      silicon wafer up to the light at a metrology / inspection station, rainbow
      diffraction spreading across the wafer.
  3 — fab interior with a row of process tools down an aisle and a technician in
      a bunny suit walking the service end.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT neon / synthwave, NOT glowing lines, NOT geometric
patterns, NOT digital art / 3D render / CGI / hologram / HUD overlay, NOT abstract,
and NOT the recently used scenes on this site (high-voltage substation, generator
yard, optics / laser lab, boutique checkout counter, office / headset customer
service, night cityscape).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: silicon wafers, fab equipment, control panels and cleanroom suits are
  covered in labels, part numbers, lot codes and UI screens, so all lettering,
  numbers, serial numbers, part numbers, logos and brand names are explicitly
  forbidden. Any display or panel in frame is switched off, angled away, or so far
  out of focus it reads as a flat wash of dark colour.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-gfs-quantum-foundry-hero-20260920.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "globalfoundries-quantum-foundry-chips-award-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "lot numbers, no lot codes, no die identification markings, no laser-scribed "
    "markings on the silicon, no etched or stamped lettering on the wafer "
    "surface, no scribe-line labels, no user interface, no software windows, no "
    "dashboards, no machine control screens showing content, no control panel "
    "displays, no digital readouts, no tool status monitors, no MES terminals, "
    "no toolbars, no menus, no icons, no signage, no warning signs, no placards, "
    "no danger notices, no safety stickers, no hazard tape lettering, no "
    "cleanroom garment lettering, no name badges, no lanyards, no hood or "
    "coverall markings, no equipment brand plates, no tool nameplates, no "
    "manufacturer names, no company names, no corporate logos printed on the "
    "tool skins or the wafer boxes, no logos on the wafer carrier or the FOUP, "
    "no cabinet labels, no panel markings, no equipment labels, no dial faces "
    "with numbers, no gauges with numerals, no dials, no meters, no charts, no "
    "arrows, no crosshairs, no alignment marks, no fiducials, no lettering on "
    "the floor tiles, no floor tape markings, no ceiling grid lettering, no "
    "printed documents, no clipboards with writing, no barcodes, no QR codes, "
    "no datamatrix codes, no RFID tags with any writing, no handwritten "
    "markings, no watermarks, no trademarks, no stickers, no legible writing of "
    "any kind anywhere in the image. Every display, monitor, control screen or "
    "instrument panel in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with absolutely "
    "nothing readable or drawn on it, like an out-of-focus colour field "
    "photograph, not a screen with content. The bare silicon wafers are plain "
    "polished mirrors with no markings whatsoever, the tool exteriors are plain "
    "smooth unmarked panels, the wafer carriers and FOUPs are plain unmarked "
    "translucent plastic, and the cleanroom garments are plain unmarked solid "
    "white fabric. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no wafer-map graph graphic, no network "
    "diagram, no glowing qubit graphic, no futuristic HUD graphics, no hologram, "
    "no overlay elements, no augmented-reality graphics, no data center server "
    "room, no server racks, no server aisles, no cable-run composition, no "
    "server lights, no GPU hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — cleanroom production floor: 300mm wafer in its carrier at a tool load port.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera, inside a modern semiconductor wafer "
        "cleanroom. Center of the sharp mid-ground is a load port on the front "
        "of a large enclosed wafer-processing tool: a translucent plastic front-"
        "opening wafer carrier sits docked on the port, its door open, and "
        "inside it a stack of gleaming bare 300mm silicon wafers is clearly "
        "visible edge-on, their polished surfaces catching the soft overhead "
        "light as thin bright arcs. This is a hand-held documentary frame shot "
        "quickly on the cleanroom floor: the camera is very slightly off-level, "
        "the tool and carrier sit off-centre in frame, and a sliver of the "
        "technician's shoulder clips the near edge. The tool above the port is a plain smooth "
        "unmarked metal enclosure with a soft amber wash of light, no labels, "
        "no nameplates, no readout, no display, no screen and no "
        "indicator window anywhere on its front, which is continuous blank "
        "unmarked brushed metal. There is no screen or display anywhere in the "
        "frame. In the left foreground, tack "
        "sharp, a technician in a plain white full-body cleanroom suit and "
        "goggles, seen three-quarters from behind, is guiding the carrier home "
        "with both gloved hands, elbows slightly bent, mid-task and unposed; the "
        "suit is plain unmarked white fabric with no lettering. The floor is a "
        "grid of pale vinyl tiles buffed to a soft sheen, the ceiling a flat "
        "field of recessed white light panels with a few faint circular air "
        "grilles. Further down the aisle, well out of focus, more process tools "
        "stand as plain grey masses against a pale wall. Cool neutral cleanroom "
        "lighting, honest available-light editorial exposure, gentle highlights "
        "on the wafer edges and the polished floor, a few faint scuff marks and "
        "dried water spots on the floor tiles, the technician's near hand very "
        "slightly motion-blurred, slight highlight clipping on the bright "
        "ceiling light panels. Moderate depth of field: the "
        "gloved hands, the carrier and the near tool face crisp, the far aisle "
        "melting into creamy bokeh. Real optical lens blur, natural camera "
        "noise, clearly visible fine film grain in the midtones and shadows, "
        "subtle optical vignette, mild chromatic aberration on high-contrast "
        "edges, no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — gloved engineer in a cleanroom suit holds a bare 300mm wafer to the light.
    "2": (
        "A genuine photograph taken inside a semiconductor fab, not a render and "
        "not computer generated: a tight three-quarter crop, shot on an 85mm "
        "lens at f/2, of an engineer in a full-body white cleanroom suit "
        "holding a single bare 300mm silicon wafer up to the light at an "
        "inspection station. The wafer is the subject of the frame, held edge-on "
        "and tilted slightly toward the camera between two white-gloved hands, "
        "and across its whole polished mirror surface a soft rainbow diffraction "
        "spreads in broad iridescent bands of violet, green and gold where the "
        "thin films catch the light — a natural interference effect, not a "
        "graphic. The wafer is completely plain, with no lettering, no scribed "
        "markings, no die labels and no part numbers anywhere on it. The "
        "engineer's hooded head is turned away in soft profile toward the wafer, "
        "face mostly hidden behind a plain hood and clear safety goggles, "
        "unposed and mid-inspection. The suit is plain unmarked white fabric "
        "with no badges, no lettering, no logos. Behind them, heavily out of "
        "focus, the pale vertical mass of an inspection bench and a process tool "
        "dissolve into a clean cream-grey wash, one small panel in the far "
        "background reduced to a flat dark out-of-focus rectangle with nothing "
        "readable on it. Cool diffuse cleanroom light from above, honest "
        "available-light editorial exposure, delicate specular highlights on the "
        "wafer rim. Extremely shallow depth of field — the wafer and the gloved "
        "fingertips crisp, the sleeves and hood already softening, the room "
        "behind in heavy creamy bokeh. Real optical blur, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — fab aisle between process tools, technician in a bunny suit walking away.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 down the service aisle of a "
        "semiconductor fabrication cleanroom. The aisle runs away from the "
        "camera in a gentle one-point perspective: on the left and right stand "
        "long rows of large enclosed wafer process tools, plain smooth unmarked "
        "metal and pale grey panel-faced cabinets, shoulder height to well over "
        "head height, their front faces a repeating rhythm of blank doors, dark "
        "switched-off displays reading as flat black rectangles, and small "
        "unmarked handles, with slim service gaps between them. Near the middle "
        "of the frame, walking away from the camera at the service end of the "
        "row, is a technician in a plain white bunny suit with the hood up and a "
        "half-mask visible in profile, mid-stride, unposed, gloved hands at "
        "their sides — plain unmarked white fabric, no badges and no lettering. "
        "The floor is a buffed pale vinyl tile grid catching a long soft "
        "reflection of the ceiling light panels; the ceiling is a flat plane of "
        "recessed white fixtures and faint air grilles. Far down the aisle the "
        "tools and the technician soften into haze. Cool even cleanroom lighting "
        "with a subtle warm accent from a distant service lamp, honest "
        "available-light editorial exposure, deep but gentle shadows pooling "
        "between the tools. Moderate depth of field with the nearest tool edges "
        "and the technician crisp and the far end of the aisle dissolving into "
        "creamy bokeh, real optical blur, natural camera noise, very slight film "
        "grain, subtle lens vignette, no plastic CGI sheen, no glossy render, no "
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
