#!/usr/bin/env python3
"""Generate hero for lrcx-september-quarter-memory-capex-2026 (fal flux/schnell).

Subject: Lam Research (LRCX) — deposition and etch process equipment. Etch tools
carve high-aspect-ratio holes in NAND, deposition tools build the stacked films
behind DRAM/HBM and leading-edge logic.

Scene chosen: the INTERIOR OF AN ADVANCED CHIP-FAB CLEANROOM — a deposition /
etch tool cluster of tall white and brushed-stainless cabinets with load ports,
a robotic wafer-handling arm holding a 300mm silicon wafer with faint rainbow
diffraction, and a technician in a full white bunny suit working at a plain
unmarked panel beside the cluster. Bright natural cleanroom light, shallow
depth of field, slightly wide 16:9 framing.

Deliberately NOT a data-center / server-room / server-aisle / rack / cable-run
composition (banned), NOT neon or synthwave, NOT glowing lines, NOT geometric
patterns, NOT abstract digital art, NOT illustration or 3D render.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: no letters/numbers/labels/logos/signage/screens/UI anywhere.
  Monitors are off, angled away, or far out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-lrcx-september-quarter-hero-20261021.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "lrcx-september-quarter-memory-capex-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no toolbars, no menus, no icons, no signage, "
    "no warning signs, no wall placards, no cabinet labels, no panel "
    "markings, no engraved lettering on the equipment, no dial faces with "
    "numbers, no gauges with numerals, no readouts, no charts, no arrows, "
    "no crosshairs, no alignment marks, no wafer flat markings, no die "
    "labels, no lettering scribed on the silicon wafers, no keyboard "
    "lettering, no name badges, no lanyards, no printed documents, no "
    "clipboards with writing, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no watermarks, no "
    "stickers, no barcodes, no QR codes, no handwriting, no legible writing "
    "of any kind anywhere in the image. Every monitor or display in the "
    "frame is switched off, angled away, or so far out of focus that it "
    "shows only a soft flat wash of dark colour with absolutely nothing "
    "readable or drawn on it. The cleanroom suit, gloves and boots are "
    "plain white and unmarked, the tool panels are plain brushed metal with "
    "only unlabelled blank buttons, and the walls are plain cleanroom panel "
    "with no writing on them. No illustration, no digital art, no cartoon, "
    "no 3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no circuit-board graphics, no "
    "network diagram, no graph graphic, no futuristic HUD graphics, no "
    "hologram, no overlay elements, no augmented-reality graphics, no data "
    "center, no server room, no server racks, no server aisles, no cable "
    "runs, no server lights, no GPU hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — medium-wide: tool cluster + robot arm with wafer + technician beside it.
    "1": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a 35mm lens at f/2.8 on a full-frame camera, inside an advanced "
        "semiconductor fabrication cleanroom. The subject is a deposition "
        "and etch tool cluster: a row of tall clean white and brushed "
        "stainless-steel process chambers with rounded corners, small wafer "
        "load ports with open cassette doors, and plain unmarked front "
        "panels, filling the left and centre of the frame and receding "
        "softly out of focus toward the back. In the sharp centre foreground "
        "a polished robotic wafer-handling arm, a slim articulated metal "
        "blade, extends from the open load port holding a single round "
        "300mm silicon wafer level and flat, its mirror face catching a "
        "faint rainbow diffraction of pale violet, cyan and warm gold across "
        "the fine unmarked grid of dies. To the right, a technician in a "
        "full plain white cleanroom bunny suit with a white hood and clear "
        "face shield stands at the tool, seen three-quarters from behind, "
        "one gloved hand resting near a plain blank control panel, calm and "
        "mid-task, not posing, softly out of focus. The cleanroom itself is "
        "bright and spotless: pale sealed wall panels, a white ceiling with "
        "flush diffuse light panels, a pale perforated raised floor with "
        "gentle reflections. Soft natural-looking diffuse cool-white light "
        "with a faint warm tint, honest shadows, no coloured gels. "
        "Photographic, very shallow depth of field, the wafer and the robot "
        "blade tack sharp and everything behind dissolving into creamy "
        "optical bokeh, real lens blur, natural camera noise, very slight "
        "film grain, subtle vignette, no CGI sheen, slightly wide 16:9 "
        "landscape framing, professional lighting. "
        + NO_TEXT
    ),
    # 2 — tighter: robot arm presenting the wafer, tool cluster behind.
    "2": (
        "Professional stock photograph, real photo not a render, shot on a "
        "50mm lens at f/2 inside a semiconductor fabrication cleanroom: a "
        "tight three-quarter view of a robotic wafer-handling arm inside the "
        "open load port of a deposition and etch tool. The arm's smooth "
        "polished stainless end-effector extends toward camera holding a "
        "300mm silicon wafer tilted slightly, its surface a soft iridescent "
        "wash of pale rose, cyan and silver diffraction over the faint "
        "unmarked grid of dies, absolutely nothing printed on it. Behind "
        "and around it, the bulk of the tool cluster: tall white painted "
        "chamber cabinets, brushed steel vacuum chamber lids, a round "
        "ceramic chamber window, thick grey gas lines and a plain blank "
        "panel, all rendered as soft out-of-focus planes of white and grey "
        "metal. Far left, blurred, the shoulder and white-hooded head of a "
        "cleanroom technician in a bunny suit leaning toward the tool. "
        "Bright diffuse cleanroom light from above and from a pale wall of "
        "light behind, soft natural falloff, gentle specular highlights on "
        "the metal, no coloured lighting. Photographic, extremely shallow "
        "depth of field with the wafer edge and the end-effector crisp and "
        "the tool dissolving into smooth creamy bokeh, real optical blur, "
        "natural camera noise, very slight film grain, subtle vignette, "
        "not CGI, slightly wide 16:9 landscape framing, professional "
        "lighting. "
        + NO_TEXT
    ),
    # 3 — wider aisle/bay view of the tool cluster with technician and wafer.
    "3": (
        "Professional stock photograph, documentary editorial photo, shot on "
        "a 28mm lens at f/4 from eye level inside a working semiconductor "
        "cleanroom: a wide view of a deposition and etch tool bay, a cluster "
        "of tall white and brushed stainless process tools with load ports "
        "and rounded chamber housings standing along a pale perforated "
        "raised floor, the white ceiling above carrying flush diffuse light "
        "panels. In the mid-ground a cleanroom technician in a full plain "
        "white bunny suit, hood and booties, stands side-on beside the "
        "nearest tool with both gloved hands near an open load port, "
        "attentive and mid-task, not posing. At the port a robotic arm "
        "presents a round 300mm silicon wafer, its mirror surface carrying a "
        "faint rainbow shimmer of violet and pale gold where the light "
        "grazes it, a second wafer visible in an open cassette beside it. "
        "Pale sealed wall panels, spotless surfaces, no signage anywhere, "
        "soft neutral cleanroom light with gentle shadows and subtle "
        "reflections on the polished floor. Photographic, moderate to "
        "shallow depth of field, the technician and the wafer sharp and the "
        "far tool bay softening into haze, real optical blur, honest "
        "available-light editorial exposure, natural camera noise, very "
        "slight film grain, subtle vignette, no CGI, no render, slightly "
        "wide 16:9 landscape framing, professional lighting. "
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
    img = img.convert("RGB")
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
    if size < 204800:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
