#!/usr/bin/env python3
"""Generate hero for amkor-advanced-packaging-bottleneck-2026 (fal flux/schnell).

Subject: Amkor Technology — the world's largest US-headquartered OSAT
(outsourced semiconductor assembly and test). Amkor takes finished silicon
dies from the fabs and turns them into sellable AI accelerators: die attach,
wire bonding, flip chip, 2.5D interposers carrying HBM memory stacks,
wafer-level processing, and the final electrical test that follows. Advanced
packaging is now the bottleneck step between the fab and the AI rack.

Frame: THE PACKAGING / ASSEMBLY / TEST FLOOR — an OSAT back-end line, NOT a
data center and NOT a front-end lithography fab.

Scene 1 (ATTEMPT=1): an automated die-attach / wire-bonding machine placing a
die onto a large organic package substrate inside a warm-lit cleanroom, trays
and magazines of large advanced packages in the mid-ground, bunny-suit
technicians softly out of focus.

Scene 2 (ATTEMPT=2): inspection-station macro of a large AI accelerator
package on a tray — centre silicon die surrounded by HBM memory stacks under
cleanroom light, with a fine probe / vacuum tweezer poised over it.

Deliberately NOT (banned): no data-center long hallway, no server aisle, no
server racks, no cable runs, no GPU rack. NOT a bare chip held in gloved
fingers, NOT a rocket, NOT a power plant, NOT a humanoid robot. NOT neon /
synthwave, NOT glowing lines or light trails, NOT abstract geometric digital
art, NOT a chart / graph / dashboard / screen full of data, NOT a 3D render or
CGI look.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: cleanroom scenes invite machine stencils, wafer markings, HMI
  displays and lot labels, so all lettering, numerals, signage and logos are
  explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-amkor-packaging-hero-20260924.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amkor-advanced-packaging-bottleneck-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no lot numbers, no serial numbers, no etched part markings on "
    "the dies or substrates, no signage, no placards, no warning labels, no "
    "safety posters, no labels, no tags, no stickers, no decals, no painted "
    "markings on machinery, no words on push buttons or switches, no START or "
    "STOP legends, no button lettering, no control-panel instructions, no "
    "machine nameplates, no data plates, no asset tags, no inventory stickers, "
    "no equipment identification plates, no illuminated indicator words, no "
    "brand names, no manufacturer names, no company "
    "names, no corporate logos, no trademarks, no watermarks, no signatures, "
    "no barcodes, no QR codes, no data-matrix codes, no hatching IDs, no "
    "graffiti, no handwriting, no documents, no clipboards with writing, no "
    "wafer scribe lettering, no legible writing of any kind anywhere in the "
    "image. No silkscreen printing, no ink of any kind on any surface, no "
    "printed markings on the substrate, no lettering on the tiny components, "
    "no control panel, no keypad and no buttons are visible in frame at all. "
    "Any display, monitor, HMI panel or machine readout is entirely "
    "blank, dark or softly out of focus with no readable content at all. "
    "Every surface, machine panel, tray, magazine and substrate is plain and "
    "unmarked, carrying no lettering, no numerals and no logos at all. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no abstract geometric "
    "art, no floating holographic elements, no artificial overlay graphics, "
    "no augmented-reality graphics, no wireframe, no charts, no graphs, no "
    "dashboards, no data visualisation, no screens full of data, no data "
    "center, no server room, no server racks, no server aisles, no cable "
    "runs, no GPU racks."
)

COMMON = (
    "Warm yellow cleanroom lighting from recessed ceiling fixtures, with "
    "softer ambient fill from the sides. Shallow depth of field with real "
    "optical lens blur and creamy natural bokeh, honest available-light "
    "exposure, true colour, natural camera noise, very slight film grain, "
    "subtle lens vignette, slight sensor softness in the shadows, no plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no retouched "
    "hyper-clean digital look, no 3D visualisation, no digital illustration, "
    "an actual photograph taken on a real camera, not a rendering, handheld "
    "with a slightly imperfect framing, uneven corner illumination, faint "
    "chromatic fringing on high-contrast edges, a few dust motes drifting in "
    "the air, photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — automated die-attach machine placing a die on a large package substrate.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/2.0 on a full-frame camera, inside a semiconductor packaging and "
        "assembly cleanroom of an outsourced assembly-and-test factory, of an "
        "automated die-attach machine in the middle of a placement cycle. At "
        "the centre of frame, crisp and tack sharp, a gantry-mounted pickup "
        "nozzle head has just lowered onto a large rectangular organic "
        "package substrate clamped flat on the heated bond stage: the "
        "spreader tool holds a single small mirror-bright silicon die, its "
        "edges razor straight, and just beneath it the substrate presents a "
        "wide flat field of clean polished laminate with a simple grid of "
        "plain smooth square die sites and a scatter of soft solder bumps, "
        "its surface one unbroken uniform tone with no printing, no etched "
        "lettering and no marked components anywhere, dust-free and "
        "gleaming. The machine around it "
        "is pale grey and stainless steel with machined aluminium rails, "
        "brushed linear guides, small servo motors and neat bundles of "
        "translucent pneumatic tubing, all unmistakably real industrial "
        "hardware with fine wear on the metal and a faint warm reflection "
        "down its machined flank. On the bench in the sharp near foreground, "
        "partly cropped, sit two open flat trays of finished large advanced "
        "packages — big square lids with exposed central dies ringed by "
        "memory stacks — and a stainless steel vacuum tweezer resting "
        "beside them, catching a small specular highlight. In the mid-ground "
        "just behind the machine, softly blurred, a stack of slotted "
        "magazines and carrier trays holds a further supply of large "
        "packages waiting for test, and beyond them the cleanroom recedes "
        "into gentle warm haze with more assembly tools in a row. To the "
        "right, out of focus and rendered only as soft shapes, a technician "
        "in a white full-body bunny suit with hood, face mask and gloves "
        "leans over a plain bare workbench, hands at work, face turned away, "
        "unidentifiable, with no control panel, keypad or buttons visible in "
        "the frame. The floor is glossy epoxy resin holding soft warm "
        "reflections of the ceiling lights and a faint mirror image of the "
        "machine legs. " + COMMON
        + NO_TEXT
    ),
    # 2 — inspection-station view of a large AI accelerator package on a tray.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2.0 on a full-frame camera, at an inspection station inside a "
        "semiconductor packaging and test cleanroom: a large advanced AI "
        "accelerator package lying on a black anti-static carrier tray on "
        "the near end of a long inspection bench, seen from a shallow "
        "three-quarter high angle at arm's length so the whole package fits "
        "comfortably in the lower middle of the frame with cleanroom air "
        "and bench space around it. The package is a big square organic "
        "substrate carrying one smooth mirror-polished central silicon die "
        "that catches a long soft warm highlight across its plain iridescent "
        "slate-grey face, ringed by eight separate rectangular high "
        "bandwidth memory stacks of stacked thin dies with softly defined "
        "edges and a milky gloss, everything immaculately clean, faintly "
        "reflective and tack sharp in the plane of focus, the substrate "
        "laminate between them a wide unbroken uniform tone with no "
        "printing, no serial marks, no lettering and no marked components "
        "anywhere. A pair of long stainless steel tweezers enters the frame "
        "from the upper right, its tips poised a hair's breadth above the "
        "central die, a tiny warm specular glint along the metal, held by "
        "the white-gloved hand of a technician whose arm and shoulder are "
        "softly out of focus at the right edge of frame. Behind the tray, "
        "out of focus and rendered only as soft warm-grey shapes, the "
        "inspection bench continues with the dark housing of a stereo "
        "microscope, a shallow dish of loose dies and a coiled ribbon "
        "cable, then dissolves into warm cleanroom haze. Warm yellow "
        "cleanroom light rakes across the top of the package from the upper "
        "left, with dark falloff into the background. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wide establishing view down a packaging/assembly line: bonder row,
    #     trays and magazines of large packages, bunny-suit staff out of focus.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera, a wide establishing view standing on "
        "the floor of a semiconductor assembly and test cleanroom, looking "
        "down a line of automatic packaging machines. The nearest machine "
        "stands large at the right of frame, tack sharp: a sturdy pale grey "
        "and stainless steel cabinet with an open dark working aperture, a "
        "machined aluminium gantry toolhead inside it lowered over a large "
        "rectangular package substrate on the heated stage, fine wire "
        "bonding capillaries and a small servo assembly catching warm "
        "specular highlights, brushed metal and faint wear on its flank, no "
        "glass enclosure around it, no screen and no control panel facing "
        "the camera. Beyond it a further five or six identical machines "
        "recede in a straight row toward the vanishing point, each smaller "
        "and softer than the last, their toolheads glowing faintly in the "
        "warm haze and dissolving into bokeh, compressing into a rhythmic "
        "line of pale cabinets against the far wall. In the sharp left "
        "foreground, partly cropped by the frame, sits a stack of open black "
        "slotted magazines and two flat carrier trays holding rows of large "
        "square advanced packages with exposed central dies, their edges "
        "gleaming under the lights, with a loose stainless steel vacuum "
        "tweezer lying on the bench beside them, gently falling out of focus "
        "at the very edge of frame. Down the aisle between the machines, "
        "softly out of focus and rendered only as pale shapes, three workers "
        "stand in white full-body bunny suits with hoods, face masks, "
        "goggles and gloves, seen from behind and in three-quarter view, "
        "bent to their machines with hands at work, faces hidden, one of "
        "them carrying a shallow tray of packages, all unidentifiable and "
        "blurred by the shallow depth of field. Above them a flat ceiling "
        "grid of recessed lamps throws even warm yellow light down the "
        "aisle, and the glossy epoxy floor holds soft warm reflections of "
        "the machine legs and the tray edges. Clean, orderly, working "
        "industrial space with a hint of warm haze in the distance. "
        + COMMON
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


if __name__ == "__main__":
    main()
