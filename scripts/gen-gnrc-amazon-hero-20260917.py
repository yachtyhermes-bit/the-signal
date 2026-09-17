#!/usr/bin/env python3
"""Generate hero for gnrc-amazon-data-center-generator-warrant-2026 (fal flux/schnell).

Subject: Generac Holdings (GNRC) — the up-to-$8B long-term supply agreement signed
with Amazon on Sept 16, 2026 to supply backup power generators for Amazon's data
centers, with Amazon receiving a warrant for up to 1.69M GNRC shares that vests
as Amazon pays. Sector: AI POWER (data-center power infrastructure).

The story is DATACENTER STANDBY POWER — the diesel/gas generator sets that hold a
data hall up when the grid drops, and that Generac is being paid billions to build
for Amazon. So the picture is a data-center STANDBY GENERATOR YARD / genset plant,
NOT the inside of a building.

Scene chosen: OUTDOORS ON A DATA-CENTER POWER YARD AT DUSK — a row of very large
industrial standby generator sets in weatherproof acoustic enclosures sitting on a
concrete pad, tall exhaust stacks with faint heat shimmer, louvered radiator ends
catching the last warm light, a power engineer in a high-visibility vest and white
hard hat walking the pad past them mid-task, the plain wall of a data-center hall
and a chain-link fence softening into the background.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT a high-voltage substation / transformer bank / lattice
transmission tower / overhead power line scene (recently used on this site), NOT a
wafer-inspection cleanroom, NOT a boutique checkout counter, NOT an optics or laser
lab, NOT a quantum foundry, NOT an office or headset customer-service scene, NOT
digital art, NOT a 3D render, NOT neon / synthwave, NOT glowing lines, NOT
geometric patterns, NOT abstract.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: generator yards are wall-to-wall with equipment labels, warning
  placards, panel markings, fuel signage and control displays, so all lettering,
  numbers, UI, logos and brand names are explicitly forbidden. Any control
  panel display in frame is blank / dark / switched off / out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-gnrc-amazon-hero-20260917.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "gnrc-amazon-data-center-generator-warrant-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no control panel displays, no digital readouts, "
    "no toolbars, no menus, no icons, no signage, no warning signs, no "
    "placards, no danger notices, no safety stickers, no fuel signage, no "
    "generator nameplates, no equipment labels, no engraved or stamped "
    "lettering on the generator housings or engine, no cabinet labels, no "
    "panel markings, no dial faces with numbers, no gauges with numerals, no "
    "dials, no meters, no charts, no arrows, no crosshairs, no alignment "
    "marks, no lettering on the concrete pad, no chain-link fence banners, no "
    "keyboard lettering, no name badges, no lanyards, no hard-hat lettering, "
    "no printed documents, no clipboards with writing, no brand names, no "
    "manufacturer names, no company names, no corporate logos, no trademarks, "
    "no watermarks, no stickers, no barcodes, no QR codes, no datamatrix "
    "codes, no handwritten markings, no graffiti, no license plates, no "
    "legible writing of any kind anywhere in the image. Every display or "
    "control screen in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with "
    "absolutely nothing readable or drawn on it, like an out-of-focus colour "
    "field photograph, not a screen with content. The generator enclosures, "
    "louvered panels, exhaust stacks, radiator ends, conduits, heavy cables "
    "and concrete pad are plain and unmarked, and the worker's vest and hard "
    "hat are plain unmarked solid colours. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center server room, no server "
    "racks, no server aisles, no cable-run composition, no server lights, no "
    "GPU hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — dusk wide: row of big standby gensets on a data-center power pad + engineer walking.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera, of a data-center standby power yard at "
        "dusk. In the sharp mid-ground a row of very large industrial standby "
        "diesel generator sets sits on a wide poured-concrete pad: each unit "
        "is a big pale-grey weatherproof acoustic enclosure, roughly the size "
        "of a small truck, with louvered cooling panels on its flank and end, "
        "a tall dark vertical exhaust stack rising above it with a faint "
        "shimmer of heat in the air, heavy black power cables sweeping down "
        "into a trench, and a plain unmarked service door. The enclosures are "
        "plain and completely unmarked — no nameplates, no labels, no "
        "lettering of any kind. Walking away from the camera along the "
        "concrete pad between two of the generator rows is a single power "
        "engineer seen from behind: an orange high-visibility vest over dark "
        "work clothing, a plain white hard hat, work gloves, mid-stride with "
        "one hand relaxed and the other holding a plain blank clipboard, "
        "neither turning nor posing, their figure crisp in the mid-ground. "
        "Behind the generator rows, softened well out of focus, is the plain "
        "flat wall of a data-center hall with a row of blank dark vent "
        "louvers, and a chain-link fence at the right edge. Dusk sky above, a "
        "deep blue-grey band with the last warm amber light low on the "
        "horizon, warm sodium work-lights throwing soft pools onto the "
        "concrete and rimming the engineer's shoulders. Moderate depth of "
        "field: the nearest enclosure corner crisp, the far generator row and "
        "the building melting into creamy bokeh. Real optical lens blur, "
        "honest available-light editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — close crop: gloved hands servicing an opened genset enclosure.
    "2": (
        "A genuine photograph taken on a data-center power yard, not a render "
        "and not computer generated: a tight close crop, shot on an 85mm lens "
        "at f/2, of an industrial standby generator set being serviced. A "
        "large weatherproof acoustic enclosure stands open, one heavy plain "
        "side panel swung wide on gas struts, and inside the lit interior the "
        "dark mass of a big multi-cylinder diesel engine block is visible "
        "with its plain unmarked pipework, a filter housing and a thick "
        "bundled wiring harness. In the foreground, tack sharp, two "
        "work-gloved hands in a dark work shirt sleeve grip a heavy wrench "
        "and a plain unmarked ratchet on a large bolt low on the engine "
        "casting, knuckles tense, mid-turn — the hands and the tool are the "
        "subject of the frame. Everything metal is plain and unmarked: no "
        "nameplates, no cast-in lettering, no decals, no labels anywhere. "
        "Level with the enclosure, the louvered cooling end of the unit fills "
        "the right of frame, its slats catching a warm raking light, and low "
        "left a corner of stained concrete pad with a coil of heavy black "
        "cable. Behind the open panel the rest of the yard dissolves: another "
        "generator enclosure reduced to a soft grey shape, an exhaust stack "
        "as a dark out-of-focus vertical, the dusk sky a flat pale wash. Warm "
        "work-light spilling out of the enclosure interior onto the hands and "
        "the open panel edge, cool blue-grey dusk light on the enclosure "
        "exterior, giving strong contrast and honest shadows. Extremely "
        "shallow depth of field — the wrench, hands and near bolt crisp, the "
        "engine block softening, the far yard in heavy creamy bokeh. Real "
        "optical blur, honest editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — low angle on a single giant genset + engineer inspecting it, blue hour.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 from a low angle beside a "
        "data-center standby power installation at blue hour. Filling the "
        "left two thirds of the frame, seen from below and close, is a single "
        "enormous industrial standby generator set in a pale grey acoustic "
        "enclosure on a raised concrete plinth: the louvered radiator end "
        "faces the camera, its horizontal slats stacked from the plinth to "
        "well above head height, and behind it a tall plain exhaust stack "
        "rises out of frame against an indigo sky. The enclosure is entirely "
        "plain — smooth painted panels, unmarked hinges and latches, no "
        "nameplates, no labels, no lettering, no warning placards. Standing "
        "at the plinth on the right of frame, in sharp focus in the "
        "mid-ground, is a power engineer in a dark work jacket and a plain "
        "white hard hat, bent slightly forward with a gloved hand resting "
        "flat against the enclosure flank as if feeling for vibration, face "
        "turned down toward the machine, unposed. Wet concrete underfoot "
        "catches weak reflections of the yard lights, a low steel guard rail "
        "and a chain-link fence edge the pad, and in the far distance the "
        "flat roofline of a data-center hall sits against the last band of "
        "amber afterglow on the horizon. Soft blue-hour ambient light with a "
        "single warm work-lamp flaring gently at the top right, honest "
        "shadows pooling under the plinth. Moderate depth of field with the "
        "louvers and the engineer crisp and the far hall and fence softening "
        "into haze, real optical blur, honest available-light editorial "
        "exposure, natural camera noise, very slight film grain, subtle lens "
        "vignette, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
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
