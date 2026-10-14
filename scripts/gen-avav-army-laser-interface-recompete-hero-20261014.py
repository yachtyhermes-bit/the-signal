#!/usr/bin/env python3
"""Generate hero for avav-army-laser-interface-recompete-2026 (fal flux/schnell).

Subject: AeroVironment (AVAV) — the Army re-opening the internal interfaces
(components / modules) of its high-energy LASER counter-drone weapon (LOCUST
X3 / E-HEL) to rival bidders, i.e. a "recompete" of the guts of the system.
Related kit: beam-director turrets, optics apertures, gimbal yokes, cabling,
test enclosures, engineers inspecting hardware.

Frame (ATTEMPT=1): A GROUND-BASED LASER WEAPON'S BEAM-DIRECTOR TURRET ON A
CONCRETE PEDESTAL inside a chain-link test enclosure, with two engineers
kneeling to inspect open avionics cabling at the base of the pedestal, wire
looms and connector boxes open on the pad. Daylight, overcast-bright. NOT on a
vehicle, NOT a data center, NOT a server room, NOT a cleanroom, NOT a factory
line, NOT a lab, NOT an aerial drone shot.

Deliberately NOT (banned): no data-center long hallway, no server aisle, no
server racks, no cable runs of the data-center kind, no GPU rack, no fibre
patch panel, no satellite bus, no cleanroom, no semiconductor packaging line,
no bare chip macro, no humanoid robot, no gas power station, no dilution
refrigerator, no steam turbine, no boardroom, no security ops desk, no desert
transmission towers. NOT neon / synthwave, NOT glowing light trails or a
visible laser beam, NOT abstract geometric digital art, NOT a chart / graph /
dashboard / screen full of data, NOT a 3D render or CGI look.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY. Lean hard on documentary
  reportage cues: available light, sensor noise, dust, wear, clutter,
  imperfect handheld framing.
- Keep it non-graphic: hardware and engineers only, no combat, no explosions,
  no fire, no injured people, no violence.
- TEXT-FREE: military hardware invites stencils, unit patches, tail numbers,
  HUD reticles and maker's brand names, so all lettering and numerals are
  explicitly forbidden, and any screen is blank / dark.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-avav-army-laser-interface-recompete-hero-20261014.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "avav-army-laser-interface-recompete-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no serial numbers, no unit patches, no name tapes, no rank "
    "insignia, no national flags, no tail numbers, no vehicle markings, no "
    "stencilled letters or numerals on the airframe or launcher or optics "
    "mount, no signage, no placards, no warning labels, no safety posters, "
    "no labels, no tags, no stickers, no decals, no painted markings on "
    "machinery or vehicles, no words on push buttons or switches, no START "
    "or STOP legends, no button lettering, no control-panel instructions, "
    "no machine nameplates, no data plates, no asset tags, no inventory "
    "stickers, no equipment identification plates, no illuminated indicator "
    "words, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no trademarks, no watermarks, no signatures, no "
    "barcodes, no QR codes, no data-matrix codes, no hatching IDs, no "
    "graffiti, no handwriting, no documents, no clipboards with writing, no "
    "map cards or laminated cards with writing, no legible writing of any "
    "kind anywhere in the image. No brand name or maker's mark printed or "
    "embossed on any piece of equipment: no name stamped, engraved, moulded "
    "or cast into a pedestal, yoke, clamp, connector, housing, panel, "
    "equipment case, latch, buckle, helmet, radio, antenna, mast, jack or "
    "cable, no embossed logo or wordmark on any metal, rubber or plastic "
    "hardware anywhere. No HUD or targeting-reticle lettering, no range "
    "figures, no crosshair annotation text, no printed markings on the "
    "optics, no lettering on the tiny components, no control panel, no "
    "keypad and no buttons are visible in frame at all. Any display, "
    "monitor, sight, scope, eyepiece, tablet or machine readout is entirely "
    "blank, dark or softly out of focus with no readable content at all. "
    "Every surface, hull panel, camera body, rail, harness, case, clothing "
    "and vehicle is plain and unmarked, carrying no lettering, no numerals "
    "and no logos at all. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no video-game still, no concept art, no matte painting, "
    "no neon, no glowing lines, no light trails, no visible laser beam, no "
    "glowing energy beam, no lens flare trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no augmented-reality "
    "graphics, no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no screens full of data, no data center, no server room, "
    "no server racks, no server aisles, no data-center cable runs, no GPU "
    "racks."
)

COMMON = (
    "This is unposed documentary photojournalism caught in a single "
    "unrehearsed moment, not a staged product shot and not a hero render: "
    "the subject sits off-centre, the horizon is very slightly tilted, the "
    "framing is loose and a little careless, and foreground clutter cuts "
    "into the bottom of the frame. Bright overcast midday light with a thin "
    "high cloud layer diffusing the sun, soft directional shadows, honest "
    "available-light exposure, shallow depth of field from a wide aperture, "
    "real optical lens blur and creamy natural bokeh, unobtrusive grain "
    "visible in the smooth mid-tones, faint chromatic fringing on "
    "high-contrast edges, subtle lens vignette, slight sensor softness in "
    "the shadows, a little dust and grit in the air, scuffed worn surfaces "
    "with real fingerprints, smears, chips and grime on every object, "
    "asymmetric unidealised composition, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no immaculate showroom cleanliness, no "
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial reportage "
    "photography for a newspaper, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — a ground-based laser weapon's beam-director turret on a concrete
    #     pedestal inside a fenced test enclosure; engineers inspecting open
    #     avionics cabling at the base of the pedestal.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.2 on a full-frame camera in bright overcast daylight, inside a "
        "fenced outdoor test enclosure on a defence proving ground. In the "
        "sharp centre of the frame, sitting slightly off-centre and rising "
        "from a rough weathered concrete pedestal bolted to a scuffed "
        "concrete pad, a ground-based high-energy laser weapon's "
        "beam-director turret: a heavy matte dark-grey cast housing with a "
        "large plain circular optics aperture at its front roughly thirty "
        "centimetres across, dark, uncapped and unlit, its coated glass "
        "catching only a dull flat reflection of the overcast sky, mounted "
        "on a gimballed elevation yoke with two big dark trunnion bearings "
        "and a smaller square secondary sensor housing beside it, the "
        "housing plain and matte and unlabelled, no lettering and no "
        "markings anywhere on the metal, fine pale grit settled along every "
        "panel seam and recess, the paint scuffed and chipped back to bare "
        "metal on the corners, a thin cold highlight running the rim of the "
        "aperture ring. The pedestal itself is heavy industrial concrete "
        "with chipped edges and a bolted flange, a sealed connector box and "
        "a coiled cable wrap on its side, dark grease at the pivot, a "
        "stabilising strut running down to the pad. Around the base of the "
        "pedestal the concrete apron is littered with working clutter: a "
        "loom of thick grey and dark cabling pulled out of an opened "
        "connector box and laid in loops across the pad, bundled wire "
        "harness ties, a spare sealed connector with its dust cap hanging "
        "loose, a woven nylon lifting strap, a taped-over spare optics "
        "cover, a plastic parts tray, two abandoned spanners, bootprints in "
        "the grit and a paper coffee cup on its side. Two engineers in "
        "plain dark navy work coveralls kneel and crouch at the base of the "
        "pedestal in the near foreground, seen from behind and in "
        "three-quarter rear view, faces completely hidden and "
        "unidentifiable, one leaning in to inspect the open cable loom "
        "with both hands, the other holding a small plain dark unlabelled "
        "tablet with a blank dark screen and a coil of cable, no patch, "
        "tape, badge or lettering anywhere on their coveralls. Behind them "
        "the enclosure reads clearly: a tall galvanised chain-link security "
        "fence with plain posts and a roll of concertina on the top rail "
        "running across the mid-ground, a second plainer turret pedestal "
        "and a stack of timber pallets as soft blurred shapes beyond it, "
        "and past the fence the proving ground opens into flat dry "
        "scrubland with a faint dirt track under a pale washed bright "
        "overcast sky. Nothing is firing, no beam is visible, nothing is "
        "flying, the scene is calm, workmanlike and technical. "
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
