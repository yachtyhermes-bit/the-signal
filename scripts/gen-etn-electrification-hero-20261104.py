#!/usr/bin/env python3
"""Generate hero for etn-electrification-backlog-orders-2026 (fal flux/schnell).

Subject: Eaton Corporation (NYSE: ETN) — large electrical-equipment manufacturer
of switchgear, switchboards, power distribution gear, breakers, UPS.

Scene chosen: ELECTRICAL EQUIPMENT MANUFACTURING, not a data center.

  ATTEMPT 1 — an industrial assembly bay with a row of large grey metal
  switchgear/switchboard cabinets, doors open showing copper busbars, breaker
  compartments and dense control wiring, a technician wiring one in soft focus.
  ATTEMPT 2 — outdoor utility-scale substation switchgear installation: rows of
  grey metal-clad switchgear enclosures on concrete pads, buswork and insulators.
  ATTEMPT 3 — close detail of a breaker compartment with copper busbars.

Deliberately NOT a data-center hallway / server aisle / server room. No digital
art, neon, synthwave, glowing lines, geometric abstraction, text, logos.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-etn-electrification-hero-20261104.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etn-electrification-backlog-orders-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no silkscreen text, no display showing "
    "characters, no brand names, no logos, no watermark, no captions, no "
    "legible writing of any kind anywhere. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no synthwave, no glowing "
    "geometric lines, no light trails, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no charts, no "
    "graphs, no data visualization. Not a data-center hallway, no server "
    "aisle, no server racks, no rack of blinking lights."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 35mm lens at f/2.2, real available factory light, not a "
        "render and not CGI: the assembly bay of a heavy electrical equipment "
        "plant. A long row of tall rectangular industrial switchgear cabinets "
        "stands on a grey concrete floor, each cabinet a matte light-grey "
        "powder-coated steel enclosure about two metres high, doors swung open. "
        "Inside the nearest cabinet, in sharp focus, the exposed interior of a "
        "low-voltage switchboard: thick copper busbars bolted to insulating "
        "supports, rows of moulded-case circuit breakers clipped onto DIN rails, "
        "and dense bundles of control wiring in grey and black, laced neatly "
        "along the side wall with cable ties. Rivets, hinges, door gaskets and "
        "the brushed steel frame carry honest industrial wear, light dust and "
        "fingerprints. Two metres back, softly out of focus, a technician in a "
        "dark navy work shirt, safety glasses and a hard hat crouches at the "
        "next cabinet with a torque wrench, seen from behind and the side so the "
        "face is not identifiable; a second empty cabinet further down the row, "
        "a rolling tool trolley, coiled cable on the floor. Cool neutral "
        "overhead high-bay lighting with a little warm afternoon daylight from "
        "high windows on the left; nothing in the frame emits its own light, no "
        "glow, no LED strips. Shallow depth of field: the copper busbars and "
        "breakers of the nearest open cabinet are razor sharp, the technicians "
        "and the far end of the bay melt into soft bokeh. Real optical lens "
        "blur, natural sensor noise, fine film grain, subtle vignette, tactile "
        "metal and copper texture, slightly off-centre casual framing, no "
        "plastic CGI sheen, no perfect symmetry. Photorealistic, extremely high "
        "detail, authentic editorial stock photography, 16:9 landscape "
        "composition, wide horizontal framing. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic editorial photograph, shot on a full-frame camera with "
        "a 50mm lens at f/2.8, real daylight, not a render and not CGI: a "
        "utility-scale electrical switchgear installation outdoors at an "
        "industrial substation. Three long rows of large grey metal-clad "
        "switchgear enclosures sit bolted to poured concrete pads, each "
        "enclosure a plain windowless steel box about two and a half metres "
        "tall with bolted panel seams, ventilation louvres and a hinged front "
        "door, connected along their tops by runs of silver aluminium bus duct. "
        "Behind them, tall porcelain insulators and steel lattice structures "
        "carry heavy conductors overhead. The nearest enclosure door is ajar, "
        "showing a dark interior glimpse of breaker compartments. Ground is "
        "clean swept concrete with expansion joints and a shallow rainwater "
        "stain; gravel and a chain-link fence in the far background. Overcast "
        "late-afternoon daylight, soft and slightly cool, with the low sun "
        "grazing the steel panel edges; nothing glows, no indicator lamps lit, "
        "no light streaks. Shallow depth of field: the nearest enclosure face "
        "and its bolted seam are sharp, the second row and the lattice tower "
        "softening into gentle bokeh. Real lens blur, natural sensor noise, "
        "fine film grain, subtle vignette, believable weathering and paint "
        "chips, no CGI sheen, no perfect symmetry. Photorealistic, extremely "
        "high detail, authentic editorial stock photography, 16:9 landscape "
        "composition, wide horizontal framing. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic close editorial photograph, shot on an 85mm lens at "
        "f/2.0, real workshop light, not a render and not CGI: the open "
        "interior of a heavy industrial electrical distribution panel on a "
        "factory assembly bench. In the sharp focal plane, three thick tinned "
        "copper busbars run vertically through the frame, bolted at regular "
        "intervals through laminated insulators, with the hex heads of steel "
        "bolts catching hard specular highlights. To their right, a stack of "
        "grey moulded-case circuit breakers with plain unmarked black toggles "
        "clipped onto a steel rail, and a fan of control wiring in grey, white "
        "and black disappearing into a slotted plastic duct. The galvanised "
        "sheet-steel backplate behind them is dull and slightly scratched. "
        "Warm tungsten task lighting from a bench lamp on the left rakes across "
        "the copper, with cool daylight fill from a high window on the right; "
        "nothing emits its own light, no LEDs, no glow. Very shallow depth of "
        "field, the front busbar and the nearest breaker sharp, the rear of the "
        "enclosure falling into soft bokeh. Real macro-lens bokeh, natural "
        "sensor noise, faint dust motes, fine film grain, slight chromatic "
        "aberration at frame edges, subtle vignette, framing slightly "
        "off-centre. Photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition. " + NO_TEXT
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 60:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
