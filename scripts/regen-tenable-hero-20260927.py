#!/usr/bin/env python3
"""Regenerate hero for tenable-ai-vulnerability-flood-remediation-2026 (fal flux/schnell).

WHY (cron hero text-check 2026-09-27): the shipped hero was a SOC shot from behind
two analysts facing a wall of displays. Flux lettered the display panels with
gibberish ("Jusluls", random letter soup in both side panels). Screen-heavy scenes
are the single worst text-artifact risk at this level, so every attempt below is
built to remove readable displays from the frame at the source:

  1 — PRIMARY: the same room, but the camera is BEHIND the monitor bank. The frame
      is filled with the plain dark plastic BACKS of a row of monitors on arms,
      ventilation slots, matte rear panels, a deserted night ops room. No screen
      surface faces the lens at all, so there is nothing to letter.
  2 — Macro of an unlabelled fibre-optic patch panel: a dense field of fine
      coloured glass strands and clean connectors, no labels, no port numbers,
      gloved fingertips tidying one strand. Text-free by construction.
  3 — A lone analyst at night seen strictly from behind, every display ahead of
      them switched off or angled away, room in deep shadow with one warm lamp.
      (Person present, screen content excluded explicitly.)

Sector: ai (cybersecurity / AI-driven vulnerability remediation).
BANNED: neon, synthwave, glowing lines, digital art, 3D render, CGI, holograms,
HUD overlays, matrix rain, hooded hacker tropes, padlocks drawn on circuits,
circuit-board graphics, green code rain, text of any kind.
Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/regen-tenable-hero-20260927.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "tenable-ai-vulnerability-flood-remediation-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no digits, no serial numbers, no part "
    "numbers, no lot codes, no date codes, no port numbers, no patch-panel "
    "numbers, no cable labels, no cable ties with writing, no printed labels, "
    "no stickers, no barcode labels, no barcodes, no QR codes, no asset tags, "
    "no rack numbers, no cabinet labels, no equipment nameplates, no "
    "manufacturer names, no company names, no corporate logos, no brand "
    "names, no trademarks, no watermarks, no whiteboard writing, no "
    "whiteboard diagrams, no printed pages, no documents, no clipboards with "
    "writing, no handwritten markings, no screen content of any kind. "
    "ABSOLUTELY NO READABLE SCREEN OR DISPLAY ANYWHERE IN THE PICTURE: every "
    "monitor, display, panel, instrument, indicator and readout that appears "
    "in the frame is either switched off / powered down showing only a flat "
    "matte black or dark grey slab with no glow and no content, or is turned "
    "away from the camera so that only its plain unmarked rear plastic casing, "
    "its hinge, its stand or its mounting arm is visible with no screen "
    "surface facing the lens at all, or is thrown so far out of focus that it "
    "reads as a plain soft wash of dark colour like a defocused colour-field "
    "photograph. There are no user interfaces, no software windows, no "
    "dashboards, no terminals, no code, no tables, no charts, no graphs, no "
    "maps, no network diagrams, no lists, no toolbars, no menus, no icons, no "
    "cursors, no progress bars, no console output, no status lines, no "
    "placeholder text, no lorem-ipsum-like fake text, no scrambled or "
    "garbled lettering that only resembles words, no invented or misspelled "
    "brand names. Not a single legible character appears anywhere in the "
    "image. Also no signage, no wayfinding signs, no exit signs, no fire "
    "notices, no safety placards, no hazard tape lettering, no floor markings, "
    "no dial faces with numerals, no gauges, no meters, no clock faces, no "
    "lanyards with print, no ID badges with writing, no name badges, no "
    "pocket logos, no garment lettering, no handwritten notes, no sticky "
    "notes, no whiteboard, no notice board, no framed certificates, no "
    "graffiti, no legible writing of any kind on any surface or object. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no matrix rain, "
    "no falling green characters, no circuit-board graphics, no network "
    "diagram graphic, no glowing chip graphic, no futuristic HUD graphics, no "
    "hologram, no overlay elements, no augmented-reality graphics, no floating "
    "UI, no hooded figure, no hacker trope, no padlock graphic, no abstract "
    "logo, no data centre server room, no server rack rows, no server aisles, "
    "no long data-centre hallway, no cable-run composition, no computer screen "
    "with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light editorial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
    "visualisation, no digital illustration, no painting, photorealistic, "
    "very high detail, professional editorial stock photography, 16:9 "
    "landscape composition. "
)

PROMPTS = {
    # 1 — PRIMARY: behind the monitor bank. No screen surface faces the lens.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera from BEHIND a row of desk monitors "
        "inside a deserted security operations room at night, looking along "
        "the row of monitor backs toward the empty desks beyond. The camera "
        "sees only the REAR of the displays: four or five large flat monitors "
        "sit on long articulated arms and plain metal stands, and every one "
        "of them faces away from the camera, so the frame is filled with "
        "their plain matte dark grey rear casings — flat unmarked expanses of "
        "plastic with only a faint pattern of ventilation slots, a mounting "
        "bracket and a short white cable curving away underneath. Not one "
        "screen surface, not one glowing panel and not one pixel of display "
        "content is visible anywhere in the picture. Beneath and beyond the "
        "monitors, softly out of focus, is the empty analyst desk: a plain "
        "dark desk surface, an edge-on keyboard seen in shallow profile, a "
        "black mouse, a plain white ceramic mug and a closed matte black "
        "notebook with a blank unmarked cover — no paper, no documents, no "
        "printed matter anywhere. Two empty mesh-backed operator chairs are "
        "pushed neatly in, turned slightly away, receding down the row. The "
        "room is dark and quiet after hours: the ceiling is lost in shadow, "
        "the walls are a deep muted blue-grey, and the only light is a single "
        "warm desk lamp low in the middle distance plus a faint pool of cool "
        "light spilling from a doorway out of frame, so long soft shadows "
        "fall across the desk and the monitor casings carry gentle warm "
        "highlights along their top edges. Very shallow depth of field: the "
        "nearest monitor back and its stand crisp, the row of casings "
        "softening into the middle distance, the far end of the room melting "
        "into smooth dark bokeh. The feeling is the quiet after the alert "
        "flood — a room that has been worked hard and left for the night. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — Macro of an unlabelled fibre-optic patch panel. Text-free by construction.
    "2": (
        "A real macro photograph, not a render and not computer generated, "
        "shot on a 100mm macro lens at f/4 close up on a dense fibre-optic "
        "patch panel in a working network cabinet. The frame is filled with "
        "the panel face: rows of small clean optical connectors seated in "
        "plain unmarked metal and dark plastic housings, and from each one a "
        "fine flexible strand of glass fibre curves out and away, the strands "
        "in a tight rainbow of colours — aqua, orange, deep yellow, magenta, "
        "green and violet — sweeping across the frame in smooth parallel "
        "arcs, every one of them smooth and glossy and catching its own "
        "pin-sharp highlight. Two fingertips in a thin blue nitrile glove "
        "enter from the lower right and are captured mid-task, gently seating "
        "one aqua strand into its socket. The panel, the housings and the "
        "cabinet around them are completely plain and unmarked: no labels, no "
        "printed port numbers, no strips of tape with writing, no barcode "
        "tags, no cable ties with lettering, no manufacturer plate, no "
        "screened or stencilled lettering of any kind on any surface — just "
        "bare brushed metal, dark grey plastic and coloured glass. A single "
        "cool task light rakes in low from the upper left, so the strands "
        "throw soft coloured reflections across the brushed metal and the "
        "connector housings cast short hard shadows to the right; the "
        "background beyond the panel falls into soft dark blur with a faint "
        "warm amber hint of a distant indicator at the frame edge, unreadable "
        "and out of focus. Extremely shallow depth of field — a narrow band "
        "of connectors and the nearest strands is crisp while the rest of the "
        "panel and every other strand melts into creamy bokeh. Available-light "
        "editorial exposure, natural camera noise, visible fine film grain, "
        "subtle vignette, mild chromatic aberration on the brightest strand "
        "highlights, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — Lone analyst seen strictly from behind, every display dark or turned away.
    "3": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/1.8 on a full-frame camera at night in a dim security operations "
        "room, framing a lone analyst strictly from BEHIND. The person is a "
        "seated figure in a plain dark grey knit sweater, seen from the back "
        "and slightly to the left, cropped at the shoulders so no face and no "
        "hands are visible — their head is turned slightly down and away, and "
        "their arms are below the desk line, entirely hidden. The desk in "
        "front of them is in deep shadow and holds a plain white ceramic mug, "
        "a black mouse and a closed matte black notebook with a blank "
        "unmarked cover; no paper, no documents, no printed matter anywhere "
        "in the frame. The row of large monitors on the desk ahead of the "
        "analyst is dark and powered down: every display is either black and "
        "switched off showing only a flat matte dark surface with a single "
        "faint grey reflection of the room sliding across it, or angled away "
        "from the camera so only its plain rear casing shows — there is no "
        "readable content, no glow, no interface and no lettering on any "
        "screen anywhere in the picture. The room around them is quiet and "
        "almost black: dark walls, ceiling lost in shadow, a faint cool wash "
        "from an unseen doorway at the far right edge and one small warm pool "
        "of light on the desk from a low lamp behind the person, rimming "
        "their shoulder and the back of their head with soft warm light. "
        "Very shallow depth of field: the back of the analyst's head and "
        "shoulder and the mug on the desk crisp, the dark monitors behind "
        "softening, the room dissolving into deep smooth bokeh. The frame "
        "reads as a long night working a remediation queue — concentration, "
        "quiet, an empty room. No hands, no fingers, no wrists, no forearms, "
        "no arms and no elbows visible anywhere; nobody is touching their "
        "face; no extra limbs, no duplicated people, no disembodied limbs, no "
        "floating hands, no anatomically impossible anatomy. "
        + PHOTO_TAIL
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
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")


if __name__ == "__main__":
    main()
