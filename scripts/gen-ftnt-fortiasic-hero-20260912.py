#!/usr/bin/env python3
"""Generate hero for ftnt-fortiasic-fortios-ai-firewall-moat-2026 (fal flux/schnell).

Subject: Fortinet (NASDAQ: FTNT) — the cybersecurity company that designs
its own security silicon (FortiASIC: NP7 network processor, CP9 content
processor, SP5 security processor) and runs a single operating system
(FortiOS) across firewalls, SASE, endpoint and cloud. The article is about
why that custom-silicon edge matters as AI data centers, encrypted traffic
and agentic AI workloads land on enterprise firewalls. The story is the
silicon and the board — hardware engineering, not a data center.

Scene chosen: a PHOTOREALISTIC MACRO PHOTOGRAPH of an enterprise
network-security appliance's printed circuit board lying on a technician's
workbench — a large square custom network-processor chip at the center
under plain heatsink fins, dense gold circuit traces radiating outward, and
the blurred hands of an electronics engineer holding a fine test probe in
the soft background. Shallow depth of field, warm neutral bench lighting,
professional stock-photography look.

Deliberately NOT a data center hallway, server aisle or rack row, cable
spaghetti, a rack of blinking switches, a security operations center with
monitors, a chip-fab cleanroom or a bare silicon wafer macro (those were
recent heroes on this site).

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere. The circuit board carries NO
  silkscreen lettering of any kind.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-ftnt-fortiasic-hero-20260912.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ftnt-fortiasic-fortios-ai-firewall-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no "
    "letters, no numbers, no codes, no serial numbers, no etched or engraved "
    "markings, no labels, no plaques, no nameplates, no decals, no stencils, "
    "no stenciled writing, no markings of any kind, no logos, no brand names, "
    "no signage, no posters, no screens, no monitors, no displays, no video "
    "walls, no laptops, no phones, no tablets, no keyboards with writing, no "
    "UI, no computer interfaces, no code, no dashboards, no whiteboards with "
    "writing, no paper documents, no notebooks, no books with titles, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, no "
    "3D render, no neon, no glowing lines, no geometric patterns."
)

PROMPTS = {
    "1": (
        "Photo-realistic macro stock photograph of an enterprise network-"
        "security appliance's green printed circuit board lying flat on a "
        "plain smooth technician's workbench, a large square custom network-"
        "processor chip centered in frame beneath plain unmarked aluminium "
        "heatsink fins, hundreds of dense gold-plated copper circuit traces "
        "fanning radially outward from the chip across the immaculate bare "
        "board to neat rows of small capacitors, resistors and smooth "
        "unmarked connector sockets, the board entirely free of any printing "
        "or silkscreen lettering, in the soft blurred background the out-of-"
        "focus hands of an electronics engineer in a plain unmarked work "
        "coat holding a fine steel test probe toward the board, warm neutral "
        "overhead bench lighting with gentle soft shadows and a subtle warm "
        "highlight on the heatsink fins, very shallow depth of field with "
        "the chip and the nearest gold traces tack sharp and the engineer "
        "and background dissolved into smooth creamy bokeh, natural "
        "realistic textures, photorealistic, high detail, professional "
        "hardware-engineering stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic close-up macro photograph, shot on a 100mm macro "
        "lens, of one single large square network-processor chip mounted on "
        "a green printed circuit board on a workbench, the chip capped by "
        "plain unmarked machined aluminium heatsink fins, fine gold-plated "
        "copper traces radiating outward in clean parallel fan patterns "
        "across the smooth bare glossy board surface, the board carrying "
        "absolutely no printed or silkscreen lettering and its few small "
        "components plain, smooth and completely unmarked, a blurred out-of-"
        "focus engineer in a plain unlabelled work coat holding a slim steel "
        "test probe in the warm background, warm neutral tungsten bench "
        "light falling softly across the board with a faint warm reflection "
        "on the metal fins, extremely shallow depth of field with a crisp "
        "sharp plane across the chip and its immediate traces while "
        "everything behind falls into smooth soft bokeh, clean dust-free "
        "surface, natural realistic materials, photorealistic, high detail, "
        "professional product-engineering photography, 16:9 landscape "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
