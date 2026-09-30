#!/usr/bin/env python3
"""Generate hero for jbl-ai-infrastructure-assembly-margin-2026 (fal flux/schnell).

Subject: Jabil Inc (JBL), a giant contract manufacturer / electronics
manufacturing services company that physically assembles AI data-center
hardware — rack-scale server systems, power and cooling, networking gear —
for hyperscalers, in a global network of over 100 sites.

Scene chosen: a modern electronics MANUFACTURING / ASSEMBLY FLOOR — a bright,
clean, high-ceilinged assembly hall with workers in anti-static coats, ESD
wrist straps and hairnets, several large sheet-metal server rack enclosures on
a line, cabling harnesses, an overhead gantry or conveyor, workbenches and
plain unmarked tote bins, shallow depth of field, professional industrial
lighting. Factory floor, people at work.

Deliberately DISTINCT from the recent Signal heroes that must not repeat:
  (1) data-center long hallway / server aisle / rack-row interior (banned)
  (2) rocket launch pad (banned)
  (3) aircraft carrier deck (banned)
  (4) trading floor (banned)
  (5) retail payment terminal (banned)
  (6) semiconductor fab cleanroom interior (banned)
  (7) desert laser-weapon truck (banned)
  (8) ship canal lock (banned)
  (9) AI compute campus exterior at dusk (banned)
  (10) a hand holding anything (banned)

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/HUD.
- TEXT-FREE: factory floors naturally carry signage, hazard labels, part
  numbers, screen content and brand logos — ALL explicitly forbidden.
  Tote bins, walls, panels and enclosures must read as plain blank surfaces.
- NO data-center long hallway / server aisle / rack interior composition.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-jbl-ai-infra-hero-20260930.py
Optional: SEED=... ATTEMPT=... (best-effort reproducibility)
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "jbl-ai-infrastructure-assembly-margin-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
SEED = os.environ.get("SEED", "").strip()  # optional: pin the fal seed
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no "
    "numbers, no digits, no codes, no serial numbers, no part numbers, no "
    "printed markings, no stencilled characters, no warning decals, no "
    "painted words, no labels, no stickers, no barcodes, no QR codes, no "
    "safety signage, no hazard signs, no exit signs, no wall signs, no "
    "billboards, no posters, no brand names, no manufacturer names, no "
    "company logos, no tote contents, no bin labels, no screen, no computer "
    "monitor, no display panel, no digital readout, no instrument text, no "
    "signage of any kind anywhere in the image, no watermark, no signature, "
    "no captions, no legible writing anywhere. The tote bins, walls, "
    "workbenches and equipment are entirely plain and unbranded: plain "
    "unmarked grey plastic bins, blank pale walls, blank flat metal panels, "
    "plain unmarked metal enclosures, plain coloured cleanroom jackets with "
    "no lettering. No illustration, no digital art, no cartoon, no anime, no "
    "3D render, no CGI, no video-game look, no plastic toy look, no neon, no "
    "synthwave, no glowing lines, no light trails, no geometric patterns, no "
    "futuristic HUD graphics, no holograms, no overlay elements, no "
    "augmented-reality graphics, no charts, no graphs, no diagrams, no "
    "infographic, no title text, no typography. Not a data-center hallway, "
    "no server aisle, no row of server cabinets, no rack of blinking network "
    "equipment, no computer room, no office interior, no rocket launch pad, "
    "no aircraft carrier deck, no trading floor, no retail store, no "
    "semiconductor fab cleanroom, no surgical cleanroom, no laboratory, no "
    "warehouse shelf aisle, no hand holding anything."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a modern electronics manufacturing and final-assembly floor "
        "inside a bright, clean, high-ceilinged industrial hall. The camera "
        "looks down a working assembly line in shallow depth of field: in "
        "the mid-ground two workers in plain pale-blue anti-static coats, "
        "hairnets, safety glasses and ESD wrist straps lean over a long "
        "workbench fastening a large open sheet-metal server rack enclosure "
        "upright on a low wheeled fixture. Along the line behind them stand "
        "several more tall grey-green steel rack enclosures at different "
        "stages, some with their blank side and front panels open, "
        "revealing empty bays and neatly dressed black cabling harnesses "
        "routed in clean bundles. An overhead gantry rail carries a "
        "suspended hoist above the line; a pale conveyor and plain unmarked "
        "grey plastic tote bins sit on the workstations. Far down the hall, "
        "softly out of focus, more workers in the same pale coats work at "
        "benches under broad banks of diffused ceiling light. Smooth light "
        "grey epoxy floor, pale walls, sheer clean surfaces. The workers "
        "are ordinary real people of varied appearance, mid-task, natural "
        "posture, not posing. Shot on a 35mm lens at f/2.0 from eye level, "
        "available factory light plus soft ceiling fluorescents, shallow "
        "depth of field with the nearest rack sharp and the far end of the "
        "hall falling into gentle blur. Natural camera noise, subtle film "
        "grain, honest realistic sheet metal, painted floor and fabric "
        "texture, slightly imperfect real-world clutter, no CGI sheen, no "
        "glossy render, no perfect symmetry, no digital illustration, "
        "photorealistic, extremely detailed, professional industrial "
        "documentary photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A genuine photograph, not a render and not computer generated: the "
        "interior of a large bright modern electronics assembly plant, "
        "photographed in a wide three-quarter view along a server-rack "
        "build line. In the sharp foreground a tall unfinished grey steel "
        "rack enclosure stands on a wheeled build stand, its side panel "
        "removed and an empty bay frame exposed, with clean black cable "
        "harnesses hanging neatly inside and a coiled power cord bundled at "
        "its base. Two assembly workers in pale anti-static coats, hairnets "
        "and ESD wrist straps work beside it, one kneeling to fit a plain "
        "metal panel, one standing to route a harness; both are ordinary "
        "people seen mid-task. Behind them the line recedes into soft blur: "
        "more rack enclosures, a low conveyor carrying plain unmarked grey "
        "tote bins, workbenches with hand tools, and further workers as "
        "small soft shapes in the distance. Above the line runs an overhead "
        "gantry rail and a suspended hoist under a high ceiling of exposed "
        "structure and broad diffused light panels. Light grey epoxy floor, "
        "pale clean walls, everything utterly blank and unmarked. Shot on a "
        "35mm lens at f/2.2, eye-level standing viewpoint, broad soft "
        "industrial lighting with gentle shadows, shallow depth of field "
        "and smooth tonal falloff to the far end of the hall. Natural "
        "sensor noise, subtle grain, realistic brushed metal, matte painted "
        "steel and fabric texture, believable working clutter, no CGI look, "
        "no glossy render, no perfect symmetry, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: a high-ceilinged, bright and spotlessly clean electronics "
        "manufacturing floor, the kind of hall where large computer "
        "hardware is assembled by hand. Four workers in pale blue anti-"
        "static coats, hairnets and ESD wrist straps populate the mid-"
        "ground, bent over workbenches and a partially built tall sheet-"
        "metal rack enclosure, threading cabling harnesses and bolting "
        "blank metal panels; they are ordinary real people in natural "
        "mid-task postures, and the nearest worker is the sharpest thing in "
        "the frame. Rows of plain grey plastic tote bins and hand tools sit "
        "along the benches. Several more large rack enclosures on wheeled "
        "stands stand at intervals down the line, their flat blank panels "
        "unmarked grey steel. An overhead gantry beam crosses the top of "
        "the frame with a hoist trolley and hanging chain, below broad "
        "banks of diffused ceiling luminaires. Deep clean perspective down "
        "the hall to a softly blurred far wall and further figures. Smooth "
        "pale grey floor, plain light walls with no signage or boards "
        "anywhere. Shot on a 35mm lens at f/2.0, standing eye-level "
        "viewpoint, soft even industrial light with warm neutral colour, "
        "shallow depth of field giving a real camera look. Natural noise, "
        "very slight film grain, subtle vignette, honest metal, paint and "
        "fabric texture, no plastic render look, no perfect symmetry, no "
        "digital illustration, photorealistic, extremely high detail, "
        "professional documentary industrial photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "4": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a modern assembly-hall interior where workers build large "
        "computer hardware, framed over the shoulder of the production "
        "line with strong shallow depth of field. In the right foreground, "
        "crisply in focus, a worker in a pale anti-static lab coat, "
        "hairnet, safety glasses and blue ESD wrist strap plugs a black "
        "cable harness into the open bay of a tall grey steel rack "
        "enclosure mounted on a wheeled assembly stand; the worker's "
        "hands and the enclosure's blank metalwork carry the sharpest "
        "detail. To the left, softly out of focus, the line stretches back "
        "through the bright hall: more rack enclosures, plain grey tote "
        "bins on benches, a low conveyor, an overhead gantry rail with a "
        "suspended hoist, and several other workers in pale coats bent "
        "over their benches under wide diffused ceiling lights. High "
        "ceilings, pale clean walls, smooth light grey epoxy floor, all "
        "completely blank with no signs, labels or screens. Natural "
        "working atmosphere, believable clutter of tools and coiled "
        "cables, real people mid-task rather than posing. Shot on a 35mm "
        "lens at f/2.0, eye-level standing viewpoint, soft directional "
        "industrial light modelling the metal and the fabric of the coats. "
        "Natural sensor noise, subtle film grain, realistic sheet metal, "
        "matte plastic and fabric texture, no CGI sheen, no glossy render, "
        "no perfect symmetry, no digital illustration, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "5": (
        "A real photograph, shot on a real camera, not computer generated: "
        "a wide view of a bright, clean, modern electronics manufacturing "
        "and assembly hall with a high exposed ceiling. A long line of "
        "assembly stations runs from the sharp foreground into soft blur "
        "at the back of the hall. On the near stations, two workers in "
        "pale blue anti-static coats, hairnets and ESD wrist straps are "
        "building a large open sheet-metal server rack enclosure, one "
        "holding a blank side panel in place while the other drives a "
        "fastener; both are ordinary real people, absorbed in the task. "
        "Neat black cabling harnesses drape from the enclosure frame and "
        "coil onto the bench beside clear plain tote bins and hand tools. "
        "Several more tall grey steel rack enclosures stand along the line "
        "on wheeled stands, flat blank panels facing the camera. An "
        "overhead gantry rail with a suspended hoist crosses above the "
        "benches, and banks of diffused luminaires light the whole hall "
        "evenly from the high ceiling. More workers appear small and "
        "softly out of focus in the distance. Smooth pale grey floor, "
        "clean blank walls, no signage or displays of any kind. Shot on a "
        "35mm lens at f/2.2, standing eye-level viewpoint, generous soft "
        "industrial light, shallow depth of field with a genuine "
        "photographic falloff into the distance. Natural camera noise, "
        "very slight film grain, subtle lens vignette, honest realistic "
        "brushed metal, matte paint, plastic and fabric texture, no "
        "plastic CGI look, no perfect symmetry, no digital illustration, "
        "photorealistic, extremely high detail, professional documentary "
        "industrial photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: the busy assembly floor of a contract electronics "
        "manufacturer, shot from a low three-quarter angle along a build "
        "line so the near rack enclosure looms large and everything behind "
        "it melts into shallow-focus blur. In the foreground a tall grey "
        "steel sheet-metal server rack enclosure stands open on a wheeled "
        "build stand, its blank side panel leaned against the bench, "
        "exposing an empty bay frame and a carefully dressed bundle of "
        "black cabling harnesses. Two workers in pale anti-static coats, "
        "hairnets, safety glasses and ESD wrist straps work on it "
        "together, one crouched low with a hand tool, one standing; they "
        "are real, ordinary people mid-task. Behind and above them the "
        "hall opens up: a high ceiling with exposed structure and long "
        "diffused light panels, an overhead gantry rail with a suspended "
        "hoist, a low conveyor with plain unmarked grey tote bins, more "
        "racks and more workers reduced to soft blurred shapes deep in the "
        "frame. Smooth light grey epoxy floor, plain pale walls, nothing "
        "printed or written anywhere. Shot on a 35mm lens at f/2.0, low "
        "stable perspective, soft industrial light with gentle contrast "
        "and warm neutral colour. Natural sensor noise, subtle film grain, "
        "realistic sheet metal, matte plastic and fabric texture, "
        "believable working clutter, no CGI sheen, no glossy render, no "
        "perfect symmetry, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "7": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a bright high-ceilinged assembly hall in a modern "
        "electronics factory, seen from a slightly elevated viewpoint "
        "looking along a row of build stations. Nearest to camera and "
        "sharpest in focus, a large grey sheet-metal server rack enclosure "
        "sits open on a wheeled stand, its interior empty bays criss-"
        "crossed by neatly routed black cabling harnesses tied in tidy "
        "bundles; a worker in a pale anti-static coat, hairnet and ESD "
        "wrist strap kneels beside it, fitting a blank metal panel. A "
        "second worker stands at the bench behind, coiling a cable beside "
        "plain unmarked grey tote bins and hand tools. The line recedes "
        "into soft blur with more rack enclosures and more workers in pale "
        "coats, and an overhead gantry rail with a suspended hoist spans "
        "the width of the hall beneath a high ceiling of exposed beams and "
        "broad diffused lighting panels. Smooth pale grey epoxy floor, "
        "clean blank walls, no signage, boards or screens anywhere. "
        "Ordinary real people of varied appearance, natural mid-task "
        "postures, never posing. Shot on a 35mm lens at f/2.2 from eye "
        "level, soft even industrial light, shallow depth of field with "
        "clean receding perspective and smooth tonal falloff. Natural "
        "camera noise, very slight film grain, subtle lens vignette, "
        "honest realistic brushed metal, matte paint, plastic and fabric "
        "texture, no CGI look, no glossy render, no perfect symmetry, no "
        "digital illustration, photorealistic, extremely high detail, "
        "professional documentary industrial photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "8": (
        "A genuine photograph, not a render: a modern electronics "
        "manufacturing hall during a working shift, captured in a natural "
        "documentary style with shallow depth of field. In the mid-ground "
        "and tack sharp, three workers in pale blue anti-static coats, "
        "hairnets and ESD wrist straps gather around a partially built "
        "tall grey steel rack enclosure on a wheeled fixture, one holding "
        "a loose blank metal panel, one guiding a black cable harness into "
        "an open bay, one steadying the frame; they are real, ordinary "
        "people working, caught mid-movement and not looking at the "
        "camera. Around them the bright hall is filled with the apparatus "
        "of assembly: workbenches with hand tools, coils of cable, plain "
        "unmarked grey tote bins, and several more large rack enclosures "
        "with flat blank grey panels standing along the line. Above, a "
        "high ceiling of pale structure carries long diffused light panels "
        "and an overhead gantry rail with a suspended hoist. Further back "
        "the hall dissolves into soft blur with small distant figures at "
        "benches. Smooth light grey epoxy floor, plain blank pale walls, "
        "nothing written or labelled anywhere in the scene. Shot on a 35mm "
        "lens at f/2.0, eye-level viewpoint, soft even industrial lighting "
        "with warm neutral balance and depth-defining falloff. Natural "
        "sensor noise, subtle film grain, subtle vignette, realistic sheet "
        "metal, matte plastic, painted floor and fabric texture, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no "
        "digital illustration, no infographic, photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
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
    arguments = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if SEED:
        arguments["seed"] = int(SEED)
        print(f"Using pinned SEED={SEED}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=arguments)
    print(f"fal seed: {result.get('seed')}")
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
