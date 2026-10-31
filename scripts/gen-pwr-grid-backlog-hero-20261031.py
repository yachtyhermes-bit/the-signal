#!/usr/bin/env python3
"""Generate hero for pwr-grid-backlog-capex-panic-2026 (fal flux/schnell).

Subject: Quanta Services — North America's largest electrical-infrastructure
contractor. Record Q3 revenue (+57% YoY), record $63.7B backlog, raised 2026
guidance across every metric, while the AI trade sold off on hyperscaler capex
fears. The picture is the physical bottleneck: building the high-voltage
transmission grid that AI data centers plug into.

MANDATORY SCENE: a real-world photograph of high-voltage TRANSMISSION LINE
construction — steel lattice towers / monopoles being erected or strung across
open countryside, conductors and wires visible, ideally a utility crew, bucket
truck or lattice-boom crane at work. Golden hour or overcast daylight, wide
landscape composition, professional editorial photography, shallow depth of
field.

Deliberately NOT: data center / server room / server aisle / racks, neon or
glowing lines, abstract or digital art, geometric patterns, sci-fi, text,
logos, watermarks, CGI look.

Rules:
- PHOTO-REALISTIC stock photograph ONLY.
- TEXT-FREE: no letters/numbers/logos/brand names/signs/vehicles lettering.
- Generate 1440x810, finalize 1536x864 center-crop.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-pwr-grid-backlog-hero-20261031.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "pwr-grid-backlog-capex-panic-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, "
    "no signage, no labels, no logos, no brand names, no decals, no stencils, "
    "no license plates, no truck lettering, no warning placards, no screens, "
    "no watermark, no caption, no illustration, no digital art, no cartoon, "
    "no 3D render, no CGI, no neon, no glowing lines, no geometric patterns, "
    "no abstract art, no sci-fi."
)

PROMPTS = {
    # 1 — primary pick: lattice towers under construction, crew + crane, golden hour
    "1": (
        "Photo-realistic professional editorial photograph, wide landscape, of "
        "high-voltage transmission line construction across open rolling "
        "countryside at golden hour: a tall steel lattice transmission tower "
        "half-erected in the middle distance, its bare galvanized steel arms "
        "reaching skyward, with a second completed tower further out, heavy "
        "aluminum conductors strung between them in deep catenary curves, a "
        "lattice-boom crane and a bucket truck parked on a dirt access track at "
        "the tower base with three workers in hard hats and high-visibility "
        "vests and harnesses working at ground level, one worker small in "
        "silhouette, dry golden grass and scrub in the foreground, distant "
        "hills and soft haze on the horizon, low warm sunlight raking from "
        "camera right with long shadows across the field, warm rim light on the "
        "steel, shallow depth of field with the nearest tower base sharp and "
        "the far towers softening into atmospheric haze, shot on a full-frame "
        "camera at 70mm f4, natural color, fine sensor grain, unretouched "
        "documentary realism, 16:9 landscape composition. " + NO_TEXT
    ),
    # 2 — overcast: stringing conductors with a tensioner between towers
    "2": (
        "Photo-realistic documentary stock photograph, wide landscape, of a "
        "high-voltage transmission line stringing operation in flat overcast "
        "daylight: two rows of grey steel lattice towers marching away across "
        "green and brown farmland toward a low grey horizon, fresh conductors "
        "being pulled through the stringing blocks on the nearest tower, a "
        "hydraulic conductor tensioner trailer and a reel trailer with large "
        "wooden cable drums standing on a gravel work pad in the foreground, "
        "two utility linemen in hard hats, harnesses and high-visibility vests "
        "standing beside the equipment watching the pull, muddy tire tracks and "
        "flattened grass, low green hedgerows and a distant treeline, soft "
        "diffuse grey sky with no direct sun, muted natural color, shallow "
        "depth of field with the cable drum and nearest lineman tack sharp and "
        "the tower line dissolving into soft haze, shot on a 35mm lens at f4, "
        "candid press wire photograph taken by a working photojournalist, "
        "visible high-ISO sensor grain, natural lens falloff and mild "
        "chromatic fringing at the frame edges, imperfect handheld framing, "
        "true-to-life weathered materials and dirt, dull realistic color "
        "straight out of camera, no retouching, no color grading, "
        "unretouched photojournalism, 16:9 landscape composition. " + NO_TEXT
    ),
    # 3 — monopole erection, crane lift, golden hour, realism-hardened
    "3": (
        "Photo-realistic editorial photograph, wide landscape, real camera "
        "picture, of a single tall tubular steel transmission monopole being "
        "erected in open countryside at late golden hour: the smooth grey "
        "galvanized pole standing vertical with its cross-arms and insulators "
        "fitted at the top, a heavy crawler crane with its lattice boom angled "
        "up and rigging cables still attached near the base as the lift "
        "finishes, a utility crew of four in hard hats, harnesses and "
        "high-visibility vests standing well back on a dirt work pad, a "
        "flatbed truck loaded with steel pole sections parked to one side, an "
        "existing power line running away toward distant hills in the "
        "background, warm low orange sunlight behind the pole throwing long "
        "shadows toward the camera, dust in the air catching the light, dry "
        "grass field in the foreground, extremely detailed real-world "
        "texture: gravel and mud underfoot, scuffed painted steel, rust "
        "bloom, frayed rope, denim and canvas seams, sweat and dust on the "
        "workers, shallow depth of field with the crew and crane base sharp "
        "and the pole top soft, shot on a full-frame DSLR at 85mm f2.8, RAW "
        "file with visible fine sensor grain, natural ungraded color, "
        "documentary realism, this is a genuine photograph not a painting and "
        "not an illustration, 16:9 landscape composition. " + NO_TEXT
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
