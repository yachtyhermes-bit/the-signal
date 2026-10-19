#!/usr/bin/env python3
"""Generate hero for asts-europe-carrier-spectrum-bid-2026 (fal flux/schnell).

Subject: AST SpaceMobile (ASTS) — space-based cellular broadband that connects
directly to ordinary smartphones — and the European carrier alliance (Deutsche
Telekom, Orange, Telefonica, Vodafone) pursuing MSS spectrum alongside AST's
ground infrastructure.

Scene: ground-level, real-world telecom infrastructure. Three variants:
  A) rural cellular tower on a grassy hillside at golden hour
  B) satellite ground-station field with two white parabolic dishes at dusk
  C) rooftop macro-cell site on a city building at dawn

Deliberately DISTINCT from recent heroes (server halls, chip cleanrooms, SD-card
still lifes): no data center, no server aisle, no glowing lines/neon/synthwave,
no digital art, no abstract network globe, no CGI satellite renders, no text.

Rules: PHOTO-REALISTIC editorial stock photograph only. Generate 1440x810,
finalize 1600x900 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-asts-europe-carrier-hero-20261019.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "asts-europe-carrier-spectrum-bid-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no labels, no signage, no logos, no "
    "brand marks, no trademarks, no icons, no watermark, no signature, no "
    "banners, no printed or painted markings of any kind. No illustration, "
    "no digital art, no cartoon, no 3D render, no CGI, no matte painting, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no holographic or futuristic HUD graphics, no overlay "
    "graphics, no augmented-reality elements, no satellite rendered in "
    "space, no abstract network globe, no server rack, no server aisle, no "
    "data-center hallway, no circuit-board macro, no abstract background."
)

PROMPTS = {
    "1": (
        "A photo-realistic editorial stock photograph for a business "
        "magazine, shot on an 85mm lens at f/2.8 in warm golden-hour light, "
        "professional photojournalism, natural available light only. A "
        "lattice-steel rural cellular tower stands on a grassy hillside in "
        "the middle distance, its three white rectangular antenna panels "
        "mounted near the top and angled slightly downward, cabled neatly "
        "down the tower leg. The tower is in sharp focus with honest metal "
        "texture: galvanised grey steel, faint rust bloom at the bolt "
        "joints, thin grey antenna cables, a small equipment cabinet at the "
        "base half-hidden in tall dry summer grass. Golden low sun comes "
        "from behind and to the right, throwing a warm rim light down one "
        "edge of the tower and the panels while the near face stays in deep "
        "cool shadow. Far below and behind, farmland and the rooftops of a "
        "small town dissolve into soft out-of-focus shapes, a single pale "
        "road cutting through the fields, all creamy bokeh. Tall grass "
        "stems in the foreground bottom corner are softly blurred, catching "
        "bright gold highlights. Real optical blur, visible fine film "
        "grain, subtle vignette, slight chromatic fringing at the frame "
        "edge, honest exposure with true blacks and warm highlights, "
        "restrained off-centre composition with open sky on the left. "
        "Photorealistic, very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched documentary photograph shot on a 35mm "
        "lens at f/2, cold blue dusk light, visibly a real camera "
        "photograph, not a render. A satellite ground-station field on a "
        "wide gravel pad dusted with a thin layer of old snow and frozen "
        "puddles. Two large white parabolic dish antennas dominate the "
        "frame, their mottled white paint and grey support struts showing "
        "wear, both aimed low toward the horizon in the same direction. A "
        "technician in a bright hi-vis vest and dark trousers walks away "
        "from camera between the dishes, small and slightly out of focus, "
        "one hand at his side, casting a long shadow across the gravel. "
        "Behind the dishes a low chain-link perimeter fence and a flat, "
        "empty field recede into deep blue-grey dusk, with the faint "
        "orange smear of distant town lights on the horizon. The nearer "
        "dish and the gravel at its base are tack sharp with honest detail "
        "— chipped paint, frost crystals, tyre tracks in the frozen mud — "
        "while the second dish and the technician soften into shallow "
        "depth of field. Real optical blur, visible fine film grain, faint "
        "halation around the brightest highlights, subtle vignette, honest "
        "cool exposure, documentary off-centre composition. Photorealistic, "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A photo-realistic editorial stock photograph for a business "
        "magazine, shot on a 50mm lens at f/2 at first light, pale washed "
        "sky and thin morning haze, professional photojournalism. On the "
        "flat roof of a mid-rise city building, a cluster of white panel "
        "cellular antennas is mounted on a grey steel frame — four slim "
        "rectangular panels angled in different directions, black coaxial "
        "cables looping down to a small grey radio unit and a weatherproof "
        "junction box bolted to the parapet. The antennas and the parapet "
        "wall are in sharp focus with honest detail: faint grime and "
        "water-streak staining on the white radomes, galvanised bolts, a "
        "chalky patch of old sealant, gravel ballast and a shallow puddle "
        "reflecting the sky between the roof membrane seams. Behind and "
        "below, the city skyline is a soft band of pale grey-blue towers "
        "melting into haze, well out of focus, with no legible detail. "
        "Cool flat dawn light from the left with a faint warm tint near "
        "the horizon, low contrast, gentle shadows. Shallow depth of "
        "field, real optical blur, visible fine film grain, subtle "
        "vignette, restrained editorial composition with generous "
        "negative sky space on the right. Photorealistic, very high "
        "detail, 16:9 landscape composition. "
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get("STEPS", "28" if "dev" in model or "pro" in model else "4"))
    print("Generating image with " + model + " (steps=" + str(steps) + ")...")
    result = fal_client.subscribe(
        model,
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": steps,
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
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size) + "  bytes=" + str(len(r.content)))
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


def photo_finish(img, seed=23, grain=6.0, softness=0.9):
    """Borrowed from scripts/hero-photo-finish.py — adds the artefacts a real
    available-light frame carries so the file behaves like a photograph."""
    import numpy as np
    from PIL import ImageFilter

    rng = np.random.default_rng(seed)
    img = img.convert("RGB").filter(ImageFilter.GaussianBlur(softness))
    arr = np.asarray(img).astype(np.float32)

    r = np.roll(arr[:, :, 0], 1, axis=1)
    b = np.roll(arr[:, :, 2], -1, axis=1)
    arr[:, :, 0] = arr[:, :, 0] * 0.7 + r * 0.3
    arr[:, :, 2] = arr[:, :, 2] * 0.7 + b * 0.3

    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2.0, h / 2.0
    dist = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    vig = 1.0 - 0.22 * np.clip(dist / 1.42, 0, 1) ** 2
    arr *= vig[:, :, None]

    lum = rng.normal(0.0, grain, (h, w, 1))
    chroma = rng.normal(0.0, grain * 0.45, (h, w, 3))
    arr += lum + chroma

    arr[:, :, 1] *= 1.012
    arr[:, :, 2] *= 0.985
    arr = arr * 0.94 + 9.0
    arr = np.clip(arr, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    if os.environ.get("FINISH", "1") == "1":
        img = photo_finish(img)
        print("Applied photographic finishing pass")
    img.convert("RGB").save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: " + OUTPUT + "  dimensions=" + str(img.size) + "  bytes=" + str(size))
    if size < 51200:
        img.convert("RGB").save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT)) + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.convert("RGB").save(BACKUP, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + BACKUP)


if __name__ == "__main__":
    main()
