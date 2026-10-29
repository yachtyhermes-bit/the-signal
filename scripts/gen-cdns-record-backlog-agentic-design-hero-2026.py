#!/usr/bin/env python3
"""Generate hero for cdns-record-backlog-agentic-design-2026 (fal flux/schnell).

Subject: Cadence Design Systems (CDNS) — electronic design automation (EDA)
software. Its tools are what engineers use to design AI chips and systems.
This is a chip-DESIGN-software story, NOT a data-center / fab / server story.

Scene ladder (vary the scene, max 3 attempts):
 1 — EDA design engineer at a wide-format multi-monitor workstation showing a
     chip layout + analog schematic, modern semiconductor design office.
 2 — Silicon bring-up / tape-out validation lab: engineer inspecting a wafer
     under a wafer-probe microscope, warm lab lighting.
 3 — Engineer at a very large wall-format display showing a dense schematic,
     reviewing with a colleague, dim design studio.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT abstract digital art, NOT neon/synthwave, NOT glowing
lines, NOT geometric-pattern art, NO text anywhere.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-cdns-record-backlog-agentic-design-hero-2026.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "cdns-record-backlog-agentic-design-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no code, no file names, no menu bars, "
    "no toolbars, no window titles, no tabs, no software user interface "
    "chrome, no icons, no dashboards, no charts, no graphs, no plots, no "
    "axes, no legends, no readouts, no gauges with numerals, no signage, no "
    "wall placards, no posters, no whiteboards with writing, no sticky notes "
    "with writing, no printed documents, no books or manuals with titles, no "
    "name badges, no lanyards, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no watermarks, no "
    "stickers, no barcodes, no QR codes, no handwriting, no legible writing "
    "of any kind anywhere in the image. Any screen in the frame shows ONLY "
    "pure geometric design geometry — unlabelled rectangles, hairline traces "
    "and thin uniform line networks — with nothing written, numbered or "
    "annotated on it. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no abstract geometric art, no floating holographic blocks, "
    "no augmented-reality overlay graphics, no circuit-board graphics "
    "superimposed on the room, no data center, no server room, no server "
    "racks, no server aisles, no cable runs, no server lights, no GPU "
    "hardware."
)

QUALITY = (
    " Real optical lens blur, honest available-light editorial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — EDA design engineer, wide multi-monitor workstation, chip layout + schematic.
    "1": (
        "Professional stock photograph of a semiconductor design engineer at "
        "an EDA workstation in a modern chip-design office, reviewing a "
        "processor floorplan on a wide-format display. Realistic photo, "
        "shallow depth of field, professional lighting. Shot on a 35mm lens "
        "at f/2.0 on a full-frame camera, from slightly behind and to the "
        "side of a man in his late thirties wearing a plain charcoal "
        "quarter-zip sweater, seated at a pale oak desk with one hand on a "
        "plain keyboard and the other resting near a mouse, mid-task and not "
        "posing, shoulders and hands sharp. In front of him two large "
        "monitors sit side by side, angled three-quarters toward the camera: "
        "the left screen is filled edge to edge with a dense chip floorplan "
        "— tightly packed solid rectangular blocks in muted slate blue, soft "
        "teal, dull olive and warm grey, crossed by hairline routing traces "
        "like an aerial view of an enormous city block layout in flat "
        "colour; the right screen shows a sparse analog schematic of thin "
        "uniform lines and small plain rectangles on a dark grey field. "
        "Nothing on either screen is written, labelled or annotated. The "
        "desk is uncluttered: a white ceramic mug, a small blank notebook, a "
        "thin stylus. Behind him the office is soft and modern — pale grey "
        "walls, a muted green plant out of focus at the frame edge, blurred "
        "silhouettes of other desks and other engineers, daylight through a "
        "large window in the far background. Warm natural key light from the "
        "window on the left, cool monitor glow filling the shadow side of "
        "his face, gentle falloff into the room, soft realistic shadows "
        "across the desk. Very shallow depth of field: the screens and his "
        "hands are tack sharp while the office behind melts into creamy "
        "bokeh."
        + QUALITY
        + NO_TEXT
    ),
    # 2 — silicon bring-up / tape-out validation lab, wafer under a probe microscope.
    "2": (
        "Professional stock photograph of a silicon validation engineer "
        "inspecting a processed wafer at a tape-out validation bench in a "
        "semiconductor lab. Realistic photo, shallow depth of field, "
        "professional lighting. Shot on an 85mm lens at f/1.8 on a "
        "full-frame camera. In the sharp centre of frame an engineer in her "
        "early thirties, plain navy button-up shirt with sleeves rolled, "
        "leans in profile over the bench with both hands on the focus knob "
        "of a wafer-probe microscope, absorbed and mid-task, not posing. "
        "Under the microscope objective a mirror-polished 300mm wafer rests "
        "on the dark stage, its surface a faint iridescent lattice of "
        "repeating tiny rectangular die patterns in soft teal, violet and "
        "steel catching a raking highlight at one edge. The microscope's "
        "black articulated arm, lens barrel and focus knobs are crisp in the "
        "mid-ground. Warm tungsten task lamp on the left plus soft diffuse "
        "daylight from a window at the back of the room, warm highlights "
        "along her face, hands and the wafer's polished edge, soft shadows "
        "under the bench equipment, a warm amber-to-grey tonal palette. The "
        "bench is plain and uncluttered: brushed-steel base plate, a plain "
        "anti-static mat, a sealed plain wafer carrier at the frame edge. "
        "The lab behind her is a soft wash of pale grey instrument "
        "housings, a fume-hood edge and window light, all far out of focus; "
        "every screen in the room is dark or angled away. Very shallow "
        "depth of field: the wafer, microscope front and her hands are tack "
        "sharp while the lab melts into creamy bokeh."
        + QUALITY
        + NO_TEXT
    ),
    # 3 — large wall-format schematic display, two engineers reviewing.
    "3": (
        "Professional stock photograph of two chip designers reviewing a "
        "large schematic on a wall-mounted display in a dim silicon design "
        "studio. Realistic photo, shallow depth of field, professional "
        "lighting. Shot on a 50mm lens at f/2.0 on a full-frame camera. A "
        "wide display fills much of the frame, showing a vast analog circuit "
        "schematic — thin uniform lines branching between small plain "
        "rectangles and rounded symbol shapes, drawn in pale grey and soft "
        "amber on a near-black field, dense at the centre and thinning "
        "toward the edges, purely geometric with nothing written or "
        "annotated. Two engineers stand three-quarters away from the camera "
        "in the mid-ground, a woman and a man in their thirties in plain "
        "dark sweaters, one gesturing toward a region of the drawing with an "
        "open hand while the other looks on, both mid-conversation and not "
        "posing, their silhouettes rimmed by the display's soft glow and "
        "sharp at the shoulders. Cool ambient light from the screen washed "
        "over the floor and their backs, a single warm ceiling downlight "
        "grazing the top of the frame, deep soft shadows behind them, a "
        "restrained cool-to-warm palette. The studio around them is dark and "
        "quiet: plain desks, a chair back, a matte grey wall, all out of "
        "focus. Very shallow depth of field: the schematics and the "
        "engineers' shoulders are tack sharp while the room melts into "
        "creamy bokeh."
        + QUALITY
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
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
