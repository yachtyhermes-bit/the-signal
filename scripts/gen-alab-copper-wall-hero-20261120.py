#!/usr/bin/env python3
"""Generate hero for alab-copper-wall-de-rating-2026 (fal flux/schnell).

Subject: Astera Labs (ALAB) — AI rack connectivity silicon: PCIe retimers,
Scorpio fabric switches, Aries smart cable modules and the copper signal
conditioning that carries the links inside a rack. Thesis: copper connectivity
content per rack, and what a ~54% repricing does to that story.

MANDATORY SCENE (deliberately NOT the previous ALAB hero, which was a cold
grey macro of one connector shell on stainless steel with pale blue gloves):
a WIDE three-quarter view of an electro-mechanical assembly bench in a
cleanroom — a harness routing board with steel pegs carrying a dense bundle of
shielded copper twinax cables, connector ends fanned out at the near edge, and
a retimer board held in a metal inspection fixture at mid-frame. Warm task-lamp
light against cool room fill, copper/orange cable tones against a matte white
bench, dark slate ESD gloves at the frame edge, shallow depth of field.

Rules:
- PHOTO-REALISTIC stock photograph ONLY. No digital art, no neon, no CGI look.
- TEXT-FREE: no letters/numbers/logos/markings on boards, shells or bench.
- No human faces. Hands only, and only as soft out-of-focus shapes.
- Generate 1440x810, finalize 1536x864 center-crop, JPEG under 400KB.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-alab-copper-wall-hero-20261120.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "alab-copper-wall-de-rating-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, "
    "no labels, no silkscreen printing, no printed markings on the circuit "
    "board, the connector shells or the bench, no logos, no brand names, "
    "no part numbers, no signage, no screens, no watermark, no caption, "
    "no illustration, no digital art, no cartoon, no 3D render, no CGI, "
    "no neon, no glowing lines, no synthwave, no geometric patterns, "
    "no abstract art, no charts, no sci-fi, no server racks, "
    "no data center aisle, no long hallway."
)

PROMPTS = {
    # 1 — cleanroom harness bench, wide three-quarter view, copper-dominant
    "1": (
        "Photo-realistic professional industrial stock photograph, wide "
        "three-quarter view across a cleanroom electro-mechanical assembly "
        "bench, shallow depth of field with the focus plane on the cable "
        "harness in the middle distance: a white laminate harness routing "
        "board stands slightly angled on the bench, studded with rows of "
        "small polished steel routing pegs, and a dense bundle of shielded "
        "high-speed copper twinax cables is laced between them in sweeping "
        "parallel runs, the copper conductors a warm reddish orange inside "
        "semi-translucent insulation, silver braided shields and foil wraps "
        "catching the light, black heat-shrink breakouts and small cable "
        "combs holding the bundle together, a few cable ends terminated in "
        "short rectangular die-cast metal connector shells fanned out and "
        "resting on the bench at the near edge, slightly soft. Behind the "
        "harness a green-grey printed circuit board sits clamped in a "
        "brushed aluminium inspection fixture, its fine gold edge contacts "
        "and rows of tiny surface-mount components just resolvable, the "
        "board surface bare and unprinted. At the left edge of the frame a "
        "technician's hands in dark slate grey anti-static gloves hold one "
        "cable end up to the light, fingers softly out of focus, only hands "
        "and a dark sleeve visible, no face. Warm amber task-lamp light "
        "raking in from the upper right, cool neutral daylight fill from "
        "the left, soft shadows under the board, a matte white bench "
        "surface with faint scuffs, copper orange and steel grey and warm "
        "white palette, realistic micro-texture on plastic and metal, fine "
        "sensor grain, unretouched natural color, documentary factory "
        "realism. Shot on a full-frame camera with an 85mm lens at f2.2, "
        "16:9 landscape composition. " + NO_TEXT
    ),
    # 2 — macro: cable connector mating into a server tray backplane cage
    "2": (
        "Photo-realistic professional industrial stock photograph, extreme "
        "close-up macro with very shallow depth of field, of a high-speed "
        "copper cable assembly being mated into a connector cage on a "
        "server tray backplane: the rectangular die-cast metal connector "
        "shell is caught half-inserted, angled into the mating opening of "
        "the cage, in tack-sharp focus, with its machined aluminium edges, "
        "tiny alignment key and the faint contact wipe marks on the metal "
        "clearly visible, a black molded strain-relief boot behind it, and "
        "behind that a dense fan of shielded twinax wire pairs spreading "
        "out of the jacket, warm copper conductors glimpsed under "
        "semi-translucent insulation, silver braid and foil wrap, held in "
        "a tight bundle by two small black cable combs. The connector cage "
        "is set into the edge of a sheet-metal chassis wall with visible "
        "screw heads and a folded sheet-metal lip, the wall running "
        "diagonally out of the frame. Other ports of the same backplane "
        "row repeat into soft bokeh to the right, a second cable curving "
        "out of focus at the left. Warm amber task light from upper right "
        "raking along the sheet metal, cool neutral fill from the left, "
        "crisp specular highlights on the shells, gentle falloff into a "
        "dark warm grey background, fine dust and handling scuffs on the "
        "metal. Palette of brushed aluminium, black plastic, warm copper "
        "orange and amber. Shot on a full-frame camera with a 100mm macro "
        "lens at f2.8, 1:1 magnification, realistic micro-texture, fine "
        "sensor grain, unretouched natural color, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    # 3 — refined pick: same backplane mating macro, black-jacketed twinax (no orange
    #     fiber look), copper only at the stripped braid and contact tips
    "3": (
        "Photo-realistic professional industrial stock photograph, extreme "
        "close-up macro with very shallow depth of field, of a high-speed "
        "copper cable assembly being mated into a connector cage on a "
        "server tray backplane: the rectangular die-cast metal connector "
        "shell is caught half-inserted, angled into the mating opening of "
        "the cage, in tack-sharp focus, with its machined aluminium edges, "
        "tiny alignment key and faint contact wipe marks on the metal "
        "clearly visible, a black molded strain-relief boot with ribs "
        "behind it, and behind that a dense fan of shielded wires spreading "
        "out of the jacket, every wire individually insulated in matte "
        "black and dark grey, a tightly twisted pair construction, the "
        "silver braided shield cut back and folded over the boot ferrule "
        "with a glimpse of bare warm copper strands at the exposed tips, "
        "held in a tight bundle by two small black cable combs. The "
        "connector cage is set into the edge of a dark grey sheet-metal "
        "chassis wall with visible screw heads and a folded sheet-metal "
        "lip, the wall running diagonally out of the frame. Other ports of "
        "the same backplane row repeat into soft bokeh to the right, a "
        "second black cable curving out of focus at the left. Warm amber "
        "task light from the upper right raking along the sheet metal, "
        "cool neutral fill from the left, crisp specular highlights on the "
        "shells and the braid, gentle falloff into a dark warm grey "
        "background, fine dust and handling scuffs on the metal. Palette "
        "of brushed aluminium, black plastic, dark grey and a small accent "
        "of warm copper. Shot on a full-frame camera with a 100mm macro "
        "lens at f2.8, 1:1 magnification, realistic micro-texture, fine "
        "sensor grain, unretouched natural color, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
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


def crop_to_ratio(img):
    """Center-crop to 16:9 then resize to 1536x864."""
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


def save_under_cap(img, path):
    """Save JPEG, stepping quality down until under MAX_BYTES."""
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        print(f"  q={q} -> {size} bytes")
        if size < MAX_BYTES:
            return size
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_ratio(img)
    size = save_under_cap(img, OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Mirrored to {BACKUP}  bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
