#!/usr/bin/env python3
"""Generate hero for the NFLX attention/decoupling article (fal flux/schnell).

Subject: a viewer alone in a living room at night in front of a large glowing
television — the attention the company is no longer directly paid for.

Scene variety: deliberately NOT a data center / server room / rack aisle /
office / boardroom. Domestic interior, warm lamp + cool screen light.

  ATTEMPT 1 — wide, three-quarter rear view: person on a sofa, big TV glowing,
              phone face up on the armrest, darkness around.
  ATTEMPT 2 — closer side view of the sofa and the viewer's profile in
              silhouette, screen light only, plant and floor lamp.
  ATTEMPT 3 — over-the-shoulder from behind the sofa, focus on the bright
              screen with soft abstract colour only, viewer soft.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-nflx-attention-decoupling-hero-2026.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "nflx-margin-ladder-attention-decoupling-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
REPO_COPY = f"/home/chino/thesignal/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image contains absolutely no readable writing: no text, no letters, "
    "no numbers, no words, no subtitles, no captions, no channel logos, no "
    "brand marks, no user-interface menus, no app tiles, no signage, no "
    "posters with legible lettering, no book spines with titles, no "
    "watermark. The television screen shows only a soft, blurred, abstract "
    "photographic image of colour and light — for example a dim landscape or "
    "faces at a distance — never any interface, grid of thumbnails, menu, "
    "title card or written content. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no synthwave, no glowing lines, "
    "no light trails, no futuristic HUD graphics, no augmented-reality "
    "overlays, no abstract digital patterns, no charts, no graphs, no data "
    "visualization. This is a domestic living room, not a workplace: no "
    "server room, no server aisle, no server racks, no laptops, no office "
    "desks, no whiteboards, no conference table, no data centre of any kind."
)

STYLE = (
    "Photo-realistic editorial photograph, shot on a full-frame camera with a "
    "35mm lens at f/2, natural available light only, not a render and not "
    "CGI, looks like a real photograph taken by a human on assignment: "
)

TAIL = (
    " Night interior: the only light sources are the large television and one "
    "warm shaded floor lamp off to the side, so the room falls into deep, "
    "believable shadow with cool blue-white spill from the screen across the "
    "furniture and the viewer, mixing with warm amber lamplight. Real optical "
    "lens blur, shallow but honest depth of field, natural sensor noise at "
    "high ISO, fine film grain, subtle vignette, believable skin and fabric "
    "texture, believable wool, cotton and wood grain, slightly off-centre "
    "casual framing, slight handheld tilt, no CGI sheen, no perfect symmetry, "
    "authentic editorial reportage. Photorealistic, extremely high detail, "
    "16:9 landscape composition, wide horizontal framing. "
)

PROMPTS = {
    "1": STYLE + (
        "a quiet modern living room at night, seen from behind and slightly to "
        "the left of a low grey linen sofa. One person sits on the sofa, a "
        "woman in her thirties in an oversized knit sweater and soft trousers, "
        "seen from three-quarters behind, knees drawn up, head resting back "
        "against the sofa, face turned away from camera and not visible. She "
        "holds a mug in one hand. Directly in front of her a large flat-screen "
        "television on a low oak media console fills the middle of the frame, "
        "glowing softly with an out-of-focus abstract image of muted colour and "
        "light. A smartphone lies face down on the sofa arm beside her. To the "
        "right a warm-shaded floor lamp casts a pool of amber light over a "
        "stack of two books with plain unmarked covers, a ceramic bowl and a "
        "small potted plant with broad leaves. Behind the television the wall "
        "is a plain deep grey-green with a faint plaster texture; a single "
        "framed canvas hangs there, abstract and unreadable in the gloom. A "
        "wooden side table, a folded throw blanket over the back of the sofa, "
        "a rug of woven wool on a wooden floor. The back of the sofa, the mug "
        "and the nearest part of the rug are sharp; the viewer's shoulders, the "
        "screen's glow and the far wall fall into gentle bokeh."
    ) + TAIL + NO_TEXT,
    "2": STYLE + (
        "candid documentary photograph made on 35mm colour negative film, "
        "scanned, visible fine grain, slightly uneven natural white balance, "
        "an ordinary un-posed late-evening moment in an ordinary apartment. "
        "Camera at seated eye level, looking across the room from the side: a "
        "man in his forties in a plain grey t-shirt and dark jeans is curled "
        "into the corner of a deep fabric sofa, seen in near-silhouette in "
        "profile against the light of a large television just off-frame to the "
        "left, which throws a cool blue-white wash across one side of his face "
        "and shoulder while the rest of him stays in shadow, features soft and "
        "not identifiable. His bare feet are up on the sofa cushion, one arm "
        "behind his head. A remote control with plain blank buttons rests on "
        "the cushion beside him next to a folded pair of glasses. In the "
        "foreground, softly out of focus, the corner of a low wooden coffee "
        "table with a half-finished glass of water, a small stack of coasters "
        "and a closed paperback with a plain unmarked cover. Mid-ground a tall "
        "leafy houseplant in a terracotta pot, a floor lamp with a linen shade "
        "switched on and throwing warm light up the wall, and a window behind "
        "it showing only black night with faint reflections of the room's "
        "lamplight on the glass. Plain plastered walls in a warm off-white, a "
        "wooden floor with a worn woven rug. The nearest sofa fabric and the "
        "man's hands are sharp; the table clutter and the far wall are soft."
    ) + TAIL + NO_TEXT,
    "3": STYLE + (
        "candid documentary photograph, over-the-shoulder view from just "
        "behind the back of a fabric sofa in a darkened living room at night, "
        "camera at roughly seated head height and slightly to the right. The "
        "out-of-focus shoulder and back of the head of a person sitting up on "
        "the sofa occupy the lower-left foreground, hair and shoulder soft and "
        "unreadable, face turned to the screen and not visible. Beyond them a "
        "large wall-mounted flat-screen television is the brightest object in "
        "the frame, filling the middle third, its picture a soft blurred "
        "abstract field of muted colour, gentle highlights and deep shadow "
        "with no shapes that resolve into anything. A slim soundbar sits on a "
        "low wooden shelf below it, a small unmarked black game controller "
        "beside it, and a short row of vinyl records leans in a plain wooden "
        "crate, their spines turned away so nothing is legible. The screen's "
        "cool light spills onto the wall and the ceiling above it and catches "
        "the edge of a curtain to the left; a warm table lamp out of frame to "
        "the right adds a low amber glow across the arm of the sofa and the "
        "floorboards. A knit blanket is crumpled on the sofa seat, a mug on "
        "the floor beside it. Honest interior detail: visible wood grain, "
        "slight scuffs on the skirting board, a power cable trailing to the "
        "wall. The television shell and the crate of records are sharp; the "
        "foreground shoulder and the room's corners blur away."
    ) + TAIL + NO_TEXT,
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
    os.makedirs(os.path.dirname(REPO_COPY), exist_ok=True)
    shutil.copy(OUTPUT, REPO_COPY)
    print(f"Mirrored to {REPO_COPY}")


if __name__ == "__main__":
    main()
