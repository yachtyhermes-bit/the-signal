#!/usr/bin/env python3
"""Generate hero for vst-vistra-data-center-power-ppa-2026 (fal flux/schnell).

Subject: Vistra Corp (NYSE: VST), a Texas independent power producer with ~44,000 MW
of gas, nuclear, coal, solar and battery generation and ~5 million retail electricity
customers, selling long-dated power contracts to AI data centres — here a new 20-year,
207 MW PPA feeding an AI data-centre campus near Odessa, Texas. Thesis: power, not
chips, is the AI buildout's binding constraint, and Vistra owns the electrons.

The picture therefore has to read as LARGE-SCALE ELECTRICITY GENERATION AND DELIVERY
IN THE TEXAS LANDSCAPE — a generation plant AND the wires leaving it. Transmission +
generation is the point: this company sells electrons.

Scene chosen (ATTEMPT=1): EXTERIOR OF A LARGE COMBINED-CYCLE NATURAL GAS POWER STATION
ON THE WEST TEXAS PLAINS IN THE WARM LOW LIGHT OF LATE AFTERNOON. Two long turbine
halls in plain ribbed metal, a row of tall slim exhaust stacks trailing soft white
water-vapour plumes, boxy heat-recovery steam generators and big silver process pipes
on steel trestles, a dirt access road, and in the mid-ground a high-voltage switchyard
with transformer banks on concrete pads under steel lattice gantries, from which a line
of lattice transmission towers marches away to the flat horizon. Deliberately no
cooling towers and no containment domes, so it cannot read as a nuclear station.

Why it is visibly different from recent heroes on this site:
- BANNED data-center server halls / server aisles / GPU racks / long glowing blue
  corridors: absent, and no data-centre building of any kind is in frame.
- CEG 9/22 (nuclear plant TURBINE HALL INTERIOR, open rotor on a service stand): this
  is outdoors, daylight, no interior, no machine hall, no nuclear equipment.
- IREN 9/17 (rural Texas AI data-centre CAMPUS MID-CONSTRUCTION at golden hour, tower
  crane, exposed steel framing, unfinished shells): no construction site, no crane, no
  scaffolding, no unfinished building — this plant is finished, operating and running.
- GNRC 9/17 (data-centre STANDBY GENERATOR YARD at dusk with enclosure boxes): this is
  a utility-scale generating station in full daylight with no generator enclosures, no
  data centre and no dusk.
- NRG 9/18 (ordinary SUBURBAN street at dusk): no houses, no street, no cars, no dusk.
- PWR 9/12 (high-voltage grid / standalone substation hero frame): here the switchyard
  is secondary mid-ground geometry — the GENERATING PLANT dominates the frame.
- No wafer cleanroom, quantum lab, office, headset service scene, chart or diagram.

ATTEMPT=2 alternative: switchyard-side ground-level view looking down the line of
transmission towers marching across flat plains toward a low sun, plant small on the
right horizon, shallow depth of field on the nearest tower steelwork.
ATTEMPT=3 alternative: low golden-hour view along the plant's perimeter fence line,
long rows of turbine hall cladding and steam plumes receding, distant switchyard.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: power stations are wall-to-wall with nameplates, tag numbers, warning
  placards and pipeline markers, so all lettering, numbers, UI, logos and brand names
  are explicitly forbidden.
- No tight close-ups of faces (no people required in this composition at all).
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

SHIPPED: ATTEMPT=1, third render of that prompt. Flux/schnell is stochastic and the
first two ATTEMPT=1 rolls (plus ATTEMPT=2 and 3) were scored "render/illustration/CGI"
by scripts/vision_inspect.py, though all five passed the text/scene checks. The third
ATTEMPT=1 roll passed both vision checks as an authentic photograph (gas plant with
turbine halls, exhaust stacks and plumes plus a switchyard of transformer banks and a
line of lattice pylons marching to the flat horizon, golden-hour light, no text, no
data centre). ATTEMPT=2's roll also passed as a photograph but showed only the pylon
line with no generating plant, so it was not used; it remains available for a reshoot
without repeating the shipped composition. All six candidate renders scored NO TEXT.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-vst-power-ppa-hero-20260923.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "vst-vistra-data-center-power-ppa-2026")
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
    "placards, no danger notices, no safety stickers, no pipeline markers, no "
    "equipment nameplates, no equipment labels, no engraved or stamped "
    "lettering on any pipe, stack, transformer, valve or steelwork, no "
    "cabinet labels, no panel markings, no dial faces with numbers, no gauges "
    "with numerals, no dials, no meters, no charts, no arrows, no crosshairs, "
    "no alignment marks, no lettering on the concrete pads or the steel "
    "gantries or the lattice towers, no fencing banners, no brand names, no "
    "manufacturer names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no stickers, no barcodes, no QR codes, no "
    "handwritten markings, no graffiti, no licence plates, no legible writing "
    "of any kind anywhere in the image. Every surface of the turbine halls, "
    "exhaust stacks, heat-recovery steam generators, pipework, transformer "
    "banks and lattice towers is plain, unmarked and unbranded. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center, no data-center building, "
    "no server room, no server racks, no server aisles, no cable-run "
    "composition, no server lights, no GPU hardware, no computer screen. "
    "No wind turbines, no solar panel arrays, no cooling towers, no nuclear "
    "containment dome, no smokestack belching black soot."
)

PROMPTS = {
    # 1 — combined-cycle gas station on the plains, switchyard + line of towers.
    "1": (
        "Photo-realistic professional editorial stock photograph, shot on a "
        "28mm lens at f/5.6 on a full-frame camera from ground level across "
        "flat West Texas scrubland in the warm low light of late afternoon. "
        "Dominating the left and centre of the frame is a large combined-cycle "
        "natural gas power station: two long low turbine halls clad in plain "
        "ribbed pale-grey metal panels, and along their roofline a row of tall "
        "slender steel exhaust stacks rising high against the sky, each one "
        "trailing a soft white plume of water vapour that leans sideways in "
        "the breeze and catches the warm light. Between and behind the halls "
        "stand three big boxy heat-recovery steam generators, their heavy "
        "ductwork climbing into the stacks, while a run of large-diameter "
        "silver process pipes is carried along the plant on squat steel "
        "trestles, everything plain, matte and completely unmarked. In the "
        "sharp mid-ground to the right, a high-voltage switchyard spreads "
        "across the ground: rows of squat grey transformer banks sitting on "
        "pale concrete pads, steel lattice gantries carrying thick grey "
        "conductors between them, and tall steel lattice transmission towers "
        "hung with long strings of insulators, from which the high-voltage "
        "line marches away in a receding row of towers toward the low flat "
        "horizon. A pale dirt access road curves across the foreground "
        "between low clumps of mesquite and dry buffalo grass, and a simple "
        "unmarked steel perimeter fence runs along the near edge of the "
        "switchyard. The land is dead flat and enormous, the sky a wide pale "
        "blue with thin high cirrus, the sun low and warm behind the plant so "
        "the tower steelwork throws long shadows across the stubble. No "
        "people, no vehicles, no buildings of any other kind, no trees, no "
        "hills. Shallow depth of field: the near turbine halls, pipe run and "
        "switchyard crisp with fine detail, the last towers and the horizon "
        "dissolving into warm atmospheric haze. Real optical lens blur, "
        "honest available-light editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — switchyard + transmission line marching to the horizon, plant small.
    "2": (
        "Photo-realistic professional editorial stock photograph, shot on a "
        "50mm lens at f/4 on a full-frame camera at ground level beside a "
        "high-voltage switchyard on the flat West Texas plains in the warm "
        "low light of late afternoon. The nearest steel lattice transmission "
        "tower fills the left of the frame in crisp sharp focus, its grey "
        "galvanised angle-iron members and bolted gusset plates thick and "
        "tactile, long strings of grey insulators hanging from its crossarms, "
        "all plain, weathered and completely unmarked. From it, thick grey "
        "conductors sweep away in a receding line of identical lattice towers "
        "that dwindle smaller and smaller across the enormous flat plain "
        "toward the low horizon, the far towers softening into warm "
        "atmospheric haze. On the right, seen at a distance and slightly out "
        "of focus, sits a large combined-cycle natural gas power station: "
        "long low turbine halls in plain ribbed pale-grey metal, a row of "
        "tall slender exhaust stacks trailing soft white water-vapour plumes "
        "that lean in the breeze, boxy heat-recovery steam generators and "
        "silver pipe runs on steel trestles, plus a few squat grey transformer "
        "banks on concrete pads, all plain and unbranded. Underfoot is dry "
        "cracked earth and low buffalo grass, with a dirt service track "
        "running off toward the towers. The sun is low and warm off to one "
        "side, gilding the tower steelwork and throwing very long shadows "
        "across the flat ground, the sky a wide pale blue with thin high "
        "cirrus. No people, no vehicles, no houses, no other buildings, no "
        "trees, no hills. Shallow depth of field as described, real optical "
        "lens blur, honest available-light editorial exposure, natural camera "
        "noise, very slight film grain, subtle lens vignette, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — perimeter fence line, plant flanks and plumes receding, switchyard far.
    "3": (
        "Photo-realistic professional editorial stock photograph, shot on a "
        "35mm lens at f/5.6 on a full-frame camera at ground level just "
        "outside the perimeter of a large combined-cycle natural gas power "
        "station on the flat plains of West Texas, in the warm low light of "
        "late afternoon. Running away from the camera on the right is the "
        "long flank of the station's turbine hall, a vast wall of plain "
        "ribbed pale-grey metal cladding with tall louvred vents and a run of "
        "thick insulated steam pipes supported on squat steel rollers along "
        "its base, everything matte, weathered and completely unmarked. "
        "Above and beyond the hall, a row of tall slender steel exhaust "
        "stacks recedes into the distance, each trailing a soft white plume "
        "of water vapour that drifts sideways in the breeze and glows in the "
        "low sun, with the boxy frames of heat-recovery steam generators and "
        "their heavy ductwork stepping down between them. In the left "
        "distance, softened well out of focus, a high-voltage switchyard "
        "shows rows of squat grey transformer banks under steel lattice "
        "gantries with a line of lattice transmission towers marching off "
        "toward the horizon. In the near foreground a simple unmarked steel "
        "chain-link perimeter fence runs along the frame with dry buffalo "
        "grass and low mesquite at its foot and a pale dirt track alongside "
        "it. The land is dead flat and enormous, the sun low and warm off to "
        "one side so the fence posts and pipe supports cast long shadows. No "
        "people, no vehicles, no houses, no other buildings, no trees, no "
        "hills. Shallow depth of field: the near fence, grass and turbine "
        "hall wall crisp, the far switchyard and towers dissolving into warm "
        "haze. Real optical lens blur, honest available-light editorial "
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
    img = img.convert("RGB")
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )
    print(f"MD5 {os.popen('md5sum ' + OUTPUT).read().strip()}")


if __name__ == "__main__":
    main()
