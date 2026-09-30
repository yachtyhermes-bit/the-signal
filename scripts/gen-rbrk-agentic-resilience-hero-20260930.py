#!/usr/bin/env python3
"""Generate hero for rbrk-agentic-cyber-resilience-moat-2026 (fal flux/schnell).

Article: Rubrik (RBRK) — enterprise cyber resilience. The company keeps an
immutable, recoverable copy of a company's data (and now its AI agents'
actions), so that when an autonomous agent or a ransomware crew destroys
production data, the business can be rebuilt.

Scene chosen (deliberately new and distinct from recent heroes):
A quiet enterprise records archive room. A heavy open steel records-room /
vault door stands in the left third of the frame, and behind it run neat
shelved rows of identical plain unbranded archive boxes. ONE box has been
pulled out and rests open on a bare steel table in the foreground — the copy
you can rebuild from. Soft directional daylight from one side, shallow depth
of field, matte textures, no gloss, slight film grain, calm and serious.

Deliberately NOT a repeat of the most recent heroes:
- Recent heroes used a desk still life (dark oak desk, olive canvas pouch,
  brass rod, blank paper roll) and before that coffee mugs, laptops,
  notebooks, pens, reading glasses. None of those appear here.
- Explicitly excluded per brief: data centre, server room, server racks,
  cable runs, laptop, desk still life, glowing screens, trading floor.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at the frame edges.
- TEXT-FREE: archive boxes and shelving are the strongest magnets for fake
  lettering (labels, label holders, barcodes, file numbers), so every letter,
  word, number, logo, brand name, watermark, barcode, label, sign, plaque,
  stencil and print pattern is explicitly forbidden; every box face, shelf
  edge, wall and surface is completely blank.
- No illustration, digital art, CGI/render look, neon, glowing lines,
  holograms, HUD graphics, geometric patterns, abstract art.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.
- Three ATTEMPT prompts so a re-run can escape a bad render (person appearing,
  fake text on boxes, render-y look).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-rbrk-agentic-resilience-hero-20260930.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "rbrk-agentic-cyber-resilience-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no legs, no body "
    "parts of any kind anywhere in the frame or at the edges of the frame, "
    "an entirely deserted empty room with nobody in it. No text, no letters, "
    "no words, no numbers, no digits, no codes, no file numbers, no dates, "
    "no catalogue numbers, no serial numbers, no part numbers, no "
    "abbreviations, no brand names, no company names, no logos, no "
    "trademarks, no monograms, no watermarks, no signatures, no stamps, no "
    "barcodes, no QR codes, no labels, no label holders, no label frames, no "
    "index cards, no plackets, no packaging labels, no tags, no stickers, no "
    "seals, no signs, no plaques, no notices, no rules, no headlines, no "
    "book spines, no titles, no handwriting, no print, no printed marks, no "
    "printed paper, no engraved marks, no embossed marks, no stencilled "
    "marks, no painted marks, no ruled lines, no grid, no writing of any "
    "kind, legible or illegible, and no drawn marks anywhere in the image. "
    "Every archive box is a completely plain unbranded blank box: plain "
    "matte board with absolutely no label, no label holder, no printed "
    "rectangle, no writing, no barcode, no number, no logo and no print or "
    "no pattern of any kind on any face, top, end or flap, no attached white "
    "or pale rectangle, no card pocket, no adhesive label shape, no paper "
    "insert and no label-sized lighter patch anywhere on any box, reading "
    "only as "
    "board texture, seam and soft shadow; the boxes are all identical and "
    "indistinguishable apart from their lighting. The steel vault door, the "
    "shelving uprights, the shelf edges and the steel table are plain "
    "featureless brushed metal with no stencilling, no stamped numbers, no "
    "engraved marks, no rivet lettering and no signage of any kind, and no "
    "stamped or cast or engraved number, letter or mark of any kind on any "
    "hinge, hinge leaf, hinge pin, bolt, latch, latch plate, handle, knob or "
    "screw head. The "
    "walls and floor are plain bare surfaces with no signage, no posters, no "
    "wayfinding marks and no markings. There is no readable or unreadable "
    "typography anywhere on any surface. No illustration, no digital art, no "
    "cartoon, no calligraphy, no typographic pattern, no 3D render, no CGI, "
    "no CGI sheen, no neon, no glowing lines, no light trails, no synthwave, "
    "no geometric patterns, no chart graphics, no futuristic HUD graphics, "
    "no hologram, no floating overlay elements, no augmented reality "
    "graphics, no data centre, no server room, no server racks, no cable "
    "runs, no server lights, no glowing screens, no monitors, no laptop, no "
    "trading floor, no ticker screen."
)

PROMPTS = {
    # 1 — wide three-quarter editorial view of the records room: heavy open
    # steel vault door on the LEFT third, shelved rows of identical plain
    # blank archive boxes receding behind it, one open blank box on a bare
    # steel table in the foreground, soft directional daylight from the left.
    "1": (
        "Photo-realistic editorial stock photograph, not a render and not "
        "computer generated, shot at eye level in a wide three-quarter view "
        "on a 35mm lens at f/2.8 on a full-frame camera, looking across a "
        "quiet empty enterprise records archive room where nobody is "
        "present. In the left third of the frame stands a heavy steel "
        "records-room vault door, swung open on its hinges towards the "
        "camera so we see its thick plain brushed-steel slab and its simple "
        "featureless steel locking bolts and round handle, a dull matte "
        "industrial door with no markings of any kind. Behind the open "
        "doorway, running away from the camera on the right two thirds of "
        "the frame, are neat metal shelving units carrying long rows of "
        "identical plain unbranded archive boxes, row after row of the same "
        "blank matte grey-beige board box with a plain lid and a simple "
        "lift-off top, every single box completely blank and identical with "
        "no label holder, no label, no writing and no pattern anywhere on "
        "it, softly lit and receding into quiet out-of-focus distance. In "
        "the foreground, lower centre, on a bare brushed-steel work table "
        "with a plain matte scratched surface, rests one single archive box "
        "of the same kind, pulled out from the shelf, its plain lid lifted "
        "off and set down flat beside it, its open interior showing only "
        "empty blank board and soft shadow, the one copy you can rebuild "
        "from. Soft directional daylight falls in low and cool from the left "
        "through an unseen high window, raking across the shelving and the "
        "open box on the table and laying one long soft shadow to the right "
        "across the bare concrete floor. Shallow depth of field with the "
        "open box on the steel table and the steel door edge crisply sharp "
        "in front and the shelving rows already dissolving into smooth "
        "creamy out-of-focus daylight, real optical lens blur, honest "
        "available light editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, matte surfaces with no "
        "gloss and no sheen, calm serious unhurried mood, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — closer, lower angle: the open blank box on the steel table
    # dominates the foreground, the open steel vault door and its blank
    # shelving loom behind, warmer daylight from the right.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close view from a low three-quarter angle just above the "
        "surface of a bare steel work table, shot on a 50mm lens at f/2.0, "
        "inside a quiet empty records archive room with no one in frame. "
        "Dominating the foreground, slightly right of centre, is a single "
        "plain unbranded archive box of matte grey-beige board, pulled out "
        "and resting on the bare brushed-steel table, its plain featureless "
        "lid lifted off and laid flat beside it and its open interior "
        "showing only clean blank board, folded seams and soft shadow, "
        "absolutely no label, no label holder, no writing, no number, no "
        "barcode and no logo anywhere on it. Behind and to the left, filling "
        "the left side of the frame slightly out of focus, stands a heavy "
        "open steel records-room vault door swung towards us, a thick plain "
        "matte brushed-metal slab on simple hinge leaves and plain steel "
        "locking bolts, with no markings of any kind: its hinges are simple "
        "smooth bare unmarked metal with absolutely no stamped, cast or "
        "engraved number or letter on them and the door face is a plain "
        "blank slab. Beyond the open doorway, soft and "
        "out of focus down the right side of the frame, neat metal shelving "
        "holds long uniform rows of identical completely blank archive "
        "boxes receding away from the camera into quiet blurred distance, "
        "every box the same plain unmarked board with a simple lid. Warm "
        "low late-afternoon daylight comes in from the right through an "
        "unseen window, softly grazing the bare steel of the table and "
        "catching the open cardboard edge of the box, casting one soft long "
        "shadow to the left across the matte table and the bare floor. "
        "Extremely shallow depth of field with the open box crisp and real "
        "optical blur everywhere else, honest editorial exposure, natural "
        "camera noise, very slight film grain, subtle lens vignette, matte "
        "textures with no gloss, sober calm mood, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — 35mm film look, widest and quietest: the shelf wall of identical
    # blank boxes fills the right, the open steel vault door stands open on
    # the left, the open box on the steel table sits small in the lower
    # frame, even diffused daylight, heavy grain, deliberate escape hatch if
    # attempts 1-2 render people or fake labels.
    "3": (
        "An ordinary unretouched 35mm film photograph, scanned straight from "
        "the negative with its natural grain, not a render and not computer "
        "generated and not a digital illustration, shot hand-held from a "
        "wide three-quarter angle at chest height on a 35mm lens at f/2.8 in "
        "a quiet empty records archive room in a plain commercial building, "
        "with nobody present and no human figure anywhere in the frame. On "
        "the left side of the frame a heavy steel records-room vault door "
        "stands open, a plain thick matte brushed-steel slab on simple "
        "hinges with plain steel locking bolts and a simple featureless "
        "round handle, unmarked and industrial. On the right, filling the "
        "middle and right of the frame, is a run of plain grey metal "
        "shelving loaded with long rows of identical plain uncoded archive "
        "boxes of blank grey-beige board, every box the same and completely "
        "unmarked with no label, no label holder, no writing, no number and "
        "no print on any face, their uniform rows receding into slightly "
        "out-of-focus distance. In the lower left foreground a bare "
        "brushed-steel work table stands with a plain matte scuffed "
        "surface, and on it one single archive box of the same blank kind "
        "has been pulled out and opened, its plain lid off and resting flat "
        "beside it, the open interior showing only empty blank board and "
        "shadow. Soft diffused overcast daylight falls evenly from the left "
        "through an unseen high window, gentle and flat with no hard focused "
        "window-pane shapes, softly modelling the matte board, the dull "
        "brushed steel and the bare painted wall, and leaving one soft "
        "diffuse shadow to the right. The far end of the room dissolves "
        "into smooth out-of-focus pale daylight and shadow. Moderate "
        "shallow depth of field with the steel door edge and the open box "
        "fairly crisp and the shelving rows softening, real optical blur, "
        "honest available light exposure with visible 35mm film grain "
        "throughout, matte surfaces with no gloss or sheen, subtle lens "
        "vignette, unhurried sober editorial mood, empty room with no human "
        "figure and no hands, no plastic CGI sheen, no glossy render, no "
        "hyper-real cleanliness, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
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
    if size < 87040:  # <85KB
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")

    # Folded-in verification
    for p in (OUTPUT, BACKUP):
        im = Image.open(p)
        print(f"VERIFY {p}  dims={im.size}  bytes={os.path.getsize(p)}")


if __name__ == "__main__":
    main()
