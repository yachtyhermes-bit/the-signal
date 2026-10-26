#!/usr/bin/env python3
"""Generate hero for spcx-apollo-gpu-lease-financing-2026 (fal flux/schnell).

Subject: SpaceX (SPCX) financing ~$40B of Nvidia AI chips through a master
finance lease with an Apollo-managed entity — a rocket company paying for GPUs
the way airlines pay for aircraft.

Scene (mandatory, per task brief): an orbital launch site / launch pad with a
tall steel launch tower at golden hour. NOT a data center corridor, NOT a
server aisle. Visually distinct from recent heroes (memory, cloud software,
process control, networking, power, defense).

Rules:
- PHOTO-REALISTIC stock photograph only. No digital art/neon/synthwave/
  glowing lines/geometric patterns/HUD/render/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/signage/screens/UI/
  watermarks anywhere.
- 16:9 landscape, final 1536x864 JPEG.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 \
        scripts/gen-spcx-apollo-gpu-lease-hero-2026.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "spcx-apollo-gpu-lease-financing-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
MODEL = os.environ.get("MODEL", "fal-ai/flux/schnell")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
RAW = f"/home/chino/thesignal/tmp/{SLUG}-raw-attempt{ATTEMPT}.jpg"
W, H = 1536, 864
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, no "
    "codes, no labels, no signage, no billboards, no posters, no plaques, no "
    "brand names, no logos, no mission patches, no watermarks, no captions, "
    "no screens or displays anywhere. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no synthwave, no glowing lines, "
    "no geometric patterns, no futuristic HUD overlays, no abstract "
    "cyberspace. This is a real photograph of a real place."
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a tall steel orbital rocket launch "
        "tower standing over a concrete launch pad at golden hour, with a "
        "slender white launch vehicle vertical beside the tower, its access "
        "arms folded back, thin white vapor venting from the vehicle and "
        "drifting across the pad. The camera stands low on the approach road "
        "looking up at the tower so it reads monumental against the sky, "
        "with service structures, water deluge pipes and cable trays in "
        "silhouette around the base. Warm low sun behind the tower throws a "
        "long amber rim light along the steelwork and floods the coastal "
        "scrub and marsh grass in the foreground with gold, while the sky "
        "above fades from pale peach at the horizon to soft blue overhead. "
        "Realistic photo, shallow depth of field, professional lighting, the "
        "near grass and concrete crisp while the tower's upper reaches and "
        "the far horizon soften into gentle haze, natural film grain, "
        "photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Realistic photograph, not a render: a wide view of an orbital launch "
        "complex at blue hour, a lattice steel launch tower with a white "
        "rocket on the pad catching the last warm sunlight on its upper "
        "stages while floodlights have just come on at the base, casting a "
        "soft warm glow on the concrete apron. Thin cryogenic vapor spills "
        "down the side of the vehicle and pools low around the pad. The frame "
        "is shot with a long lens from a distance across flat coastal marsh, "
        "so the tower and rocket sit compressed against a deep indigo sky "
        "with a band of orange afterglow behind them, and a few dark "
        "palm-and-scrub silhouettes frame the lower edge. Realistic photo, "
        "shallow depth of field, professional lighting, natural film grain, "
        "photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Professional stock photograph of an empty orbital launch pad at the "
        "end of the day, a tall open-truss launch tower of galvanized steel "
        "rising beside a horizontal integration hangar with its massive door "
        "open, revealing only dark interior. The pad surface is weathered "
        "concrete with scorch marks, ringed by low service buildings and "
        "tanker trailers, and a single access road leads toward the tower. "
        "Golden hour side light rakes across the structures, stretching long "
        "shadows over the concrete and lighting the dust in the air; the sky "
        "is a clear gradient from warm gold at the horizon to deep blue "
        "overhead. Realistic photo, shallow depth of field, professional "
        "lighting, natural film grain, photorealistic, high detail, 16:9 "
        "landscape composition. "
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


def generate(prompt, out_path, model=MODEL):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print(f"Generating image with {model}...")
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "enable_safety_checker": False,
    }
    if "schnell" in model:
        args["num_inference_steps"] = 4
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe(model, arguments=args)
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
    img = Image.open(out_path).convert("RGB")
    print(f"Downloaded raw: {out_path}  size={img.size}  bytes={len(r.content)}")
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
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} MODEL={MODEL}")
    img = generate(prompt, RAW)
    img = crop_to_16x9(img)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")


if __name__ == "__main__":
    main()
