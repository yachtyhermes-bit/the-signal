#!/usr/bin/env python3
"""Generate hero for asml-record-quarter-2030-order-horizon-2026 (fal flux/schnell).

Subject: ASML Holding (NASDAQ: ASML) — the Dutch company that builds
extreme-ultraviolet (EUV) lithography scanners, the multi-hundred-million-dollar
machines every leading-edge AI chip is printed on. Article thesis: a record Q3
2026 quarter and a customer order book that now stretches years out (an order
horizon running to 2030).

Scene chosen (the Writer's caption describes this exact photo): a huge EUV
lithography SCANNER standing in a semiconductor fab bay, photographed from a
distance so the machine dominates the frame — a small worker in a white
cleanroom bunny suit, seen from behind (face not identifiable), walking beside
it for scale, dwarfed by the machine. Cool white and pale blue cleanroom light,
a warm amber safety glow, polished light-grey flooring with a soft reflection,
the long machine body with its panels and service frame receding into shallow
focus. Documentary engineering photography. 16:9 landscape.

Deliberately DISTINCT from recent heroes: NOT a data-center hallway / server
aisle / server racks / cable runs; NOT the 10/13 Micron close-up of a hand
holding up a silicon wafer; NOT the 9/17 ASML hero of a gloved hand holding a
photomask; NOT abstract art, digital art, neon, synthwave, glowing lines,
geometric patterns, HUD overlays, 3D renders or CGI looks.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: fab equipment naturally carries printed markings, so signage,
  screen text, equipment labels, placards, letters, numbers, logos and
  watermarks are explicitly forbidden. No captions.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-asml-record-quarter-2030-order-horizon-hero-20261014.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "asml-record-quarter-2030-order-horizon-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no lot codes, no serial numbers, no "
    "part numbers, no printed markings, no stencilled characters, no screen "
    "text, no monitor displays with writing, no brand names, no manufacturer "
    "names, no logos, no watermark, no captions, no legible writing of any "
    "kind anywhere in the image. All cleanroom surfaces, machine panels, "
    "equipment housings and suit fabrics are plain and unmarked. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no futuristic HUD graphics, no overlay elements, no augmented-reality "
    "graphics, no data-center hallway, no server aisle, no server racks, no "
    "cable runs."
)

PROMPTS = {
    "1": (
        "Photo-realistic documentary engineering stock photograph inside a "
        "semiconductor fabrication cleanroom bay. The subject is an enormous "
        "extreme-ultraviolet lithography scanner — a very large multi-panel "
        "industrial machine, many metres long and several metres tall, made of "
        "smooth pale grey and white machine housings with a dark service frame, "
        "hinged access panels and a heavy structural steel base. It stands "
        "squarely in the centre of the frame and dominates it, the whole "
        "machine visible, its long body receding away from the camera in "
        "perspective. Beside the machine, small and dwarfed by it for scale, a "
        "single worker in a full white cleanroom bunny suit with hood and face "
        "mask, seen strictly from behind, walks along the machine — no face, no "
        "eyes visible at all. The floor is polished light-grey epoxy resin with "
        "a soft mirror reflection of the machine and the worker in it. Cool "
        "white and pale blue cleanroom light floods from above, and a single "
        "warm amber safety glow spills from the far end of the bay. More "
        "unspecified process equipment lines the sides, softly out of focus. "
        "Shot from a distance on a 35mm lens at f/4, the machine and worker "
        "reasonably sharp, the far end of the bay dissolving into smooth "
        "natural bokeh. Natural realistic material textures, honest "
        "documentary lighting, slight cool haze in the air, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a wide lens, not a render and not computer "
        "generated: a colossal extreme-ultraviolet lithography scanner machine "
        "occupying a cleanroom bay, photographed from far enough back that the "
        "entire machine fits in the frame and towers over everything. It is a "
        "long rectangular high-tech industrial tool built from large blank "
        "white and light-grey side panels, a dark ribbed service frame along "
        "the top, dark cable-free structural trusses and a broad flat base, its "
        "smooth housing catching a soft sheen from the overhead lights. A lone "
        "cleanroom worker in a white bunny suit, white hood and white mask is "
        "photographed strictly from behind, walking beside the machine's flank "
        "and looking tiny beside it — a human figure included only to give a "
        "sense of the machine's scale. Polished light-grey cleanroom flooring "
        "reflects the machine and the worker faintly. Cool white and pale blue "
        "overhead illumination, one small warm amber safety lamp glowing deep "
        "at the end of the aisle, other indistinct fab tools and blank wall "
        "panels lining both sides and rendered in soft blur. Moderate depth of "
        "field, very slight film grain and natural sensor noise, faint dust "
        "motes and a thin cool haze, subtle lens vignette, slightly uneven real "
        "white balance, imperfect honest framing. Absolutely not a 3D "
        "visualisation, not a glossy CGI render, no airbrushed plastic "
        "surfaces, no smooth digital sheen, no digital illustration, no "
        "AI-generated look, no data center, no server room, photorealistic, "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A real documentary photograph taken by a professional industrial "
        "photographer standing well back in a semiconductor fab cleanroom, not "
        "a render and not computer generated. A vast extreme-ultraviolet "
        "lithography scanner fills the bay: an immense pale grey and white "
        "panel-housed machine with a dark structural service frame, its long "
        "body stretching away into the depth of the picture, access covers and "
        "structural ribs plainly visible, no markings of any kind on any "
        "surface. Photographed from a distance so the machine is the hero of "
        "the frame and reads as monumental. For scale, one small worker in a "
        "white cleanroom bunny suit, hood and mask — strictly a back view, no "
        "face and no eyes visible — walks beside the machine, tiny next to it. "
        "The floor is polished light-grey epoxy with a soft wet-look reflection "
        "of the machine's base and the worker's legs. Cool white and pale blue "
        "cleanroom lighting from above, a low warm amber safety glow at the far "
        "end of the bay, unmarked blank process tools and wall panels receding "
        "into shallow focus on both sides. Moderate depth of field so the "
        "machine stays readable while the far background melts away, natural "
        "sensor noise and fine film grain, faint airborne dust, subtle cool "
        "haze, restrained lens vignette, real optical character. Not a 3D "
        "visualisation, not a glossy CGI render, no plastic surfaces, no "
        "digital sheen, no perfect symmetry, no illustration, no AI-generated "
        "look, photorealistic, high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
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
