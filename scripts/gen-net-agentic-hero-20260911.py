#!/usr/bin/env python3
"""Generate hero for net-cloudflare-agentic-web-gatekeeper-2026 (fal flux/schnell).

Subject: Cloudflare (NYSE: NET) — the global edge-network / web-infrastructure
and security company. The article is about Cloudflare becoming the referee and
toll booth of the "agentic web": AI agents crawling, transacting and being
governed at the network edge, on top of a worldwide network of data centers.

Scene chosen: a network/telecom technician in a hard hat on a city ROOFTOP at
dusk, working on an opened rack of plain networking equipment with neat bundles
of fiber-optic patch cables, a softly blurred city skyline and warm dusk sky
behind — human at work, shallow depth of field.

Deliberately DISTINCT from recent heroes (chip-fab cleanroom, wafer macro,
cryostat, rocket pad, radar dish, jet-engine line, trading floor, container
port) and NOT a "data center long hallway / server aisle".

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/plaques/nameplates/decals/
  stencils/signage/screens/monitors/displays/UI/code/dashboards/whiteboards/
  paper documents/watermarks/captions anywhere.
- Equipment faces plain/scraped of any marking so no brand text can render.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-net-agentic-hero-20260911.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "net-cloudflare-agentic-web-gatekeeper-2026")
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
        "Photo-realistic editorial stock photograph of a telecommunications "
        "network technician in a plain white hard hat and a plain high-"
        "visibility work vest standing on the flat gravel rooftop of a city "
        "building at dusk, leaning over an open equipment rack cabinet of "
        "plain unmarked dark-grey networking switches, his hands gently "
        "routing a tidy bundle of thin fiber-optic patch cables, the thin "
        "glossy strands of the cables catching warm orange and soft cyan "
        "light and curving neatly between the plain polished metal ports, "
        "the opened rack cabinet door and rack rails smooth and free of any "
        "marking, behind him a softly blurred city skyline of glass towers "
        "and small blurred windows glowing warm and cool, a warm gradient "
        "dusk sky of amber, peach and deep blue with a few soft clouds, a "
        "blurred plain telecom antenna mast off to one side, gentle warm "
        "evening light raking across the scene, shallow depth of field with "
        "the technician's hands and the fiber patch cables crisply sharp "
        "while the city skyline melts into smooth bokeh, natural realistic "
        "skin tones, photorealistic, high detail, professional documentary "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Ultra-realistic stock photograph of a lone network engineer in a "
        "plain hard hat and plain work jacket crouching beside an opened "
        "outdoor telecom equipment rack on a rooftop terrace at twilight, "
        "carefully connecting smooth unmarked fiber-optic patch cords into "
        "the plain unmarked dark metal faceplate of the rack, bundles of "
        "thin jacketed fiber strands looping in loose tidy arcs, the metal "
        "cabinet panels completely smooth and unmarked, the rooftop deck "
        "plain grey gravel and concrete, in the blurred background a wide "
        "soft city skyline of towers with warm and cool lights and a deep "
        "orange-to-indigo dusk sky fading to dusk blue, a small blurred "
        "plain security camera and antenna on a pole out of focus, warm "
        "golden hour rim light on the worker's shoulders and the glossy "
        "fiber strands, very shallow depth of field with the patch panel "
        "and hands tack sharp and the skyline dissolved into soft bokeh, "
        "photorealistic, high detail, professional editorial photography, "
        "16:9 landscape composition. "
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
