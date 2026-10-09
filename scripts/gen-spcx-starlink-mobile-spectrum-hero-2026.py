#!/usr/bin/env python3
"""Generate hero for spcx-starlink-mobile-spectrum-carrier-2026 (fal flux/schnell).

Subject: SpaceX (SPCX) buying a nationwide 800 MHz low-band spectrum portfolio
from Grain Management so its Starlink Mobile service can become a direct-to-phone
US mobile carrier.

Scene (mandatory, per task brief) — satellite-to-phone connectivity in RURAL
AMERICA, NOT a rocket pad, NOT a server room:
  a rural countryside at blue-hour dusk; in the foreground a person standing in
  a field or on a dirt road holding up a smartphone, seen from behind or in
  three-quarter profile; overhead in the twilight sky a bright train of Starlink
  satellites streaks across; a distant lone cell tower on the horizon. Warm dusk
  palette, real photographic depth of field.

Deliberately DISTINCT from recent SPCX Signal heroes (spcx-ai-compute-landlord):
those used a stainless-steel rocket on a launch pad / launch tower. This one has
NO rocket, NO launch pad, NO gantry — a grounded rural landscape instead.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/synthwave/
  glowing lines/geometric patterns/HUD/render/illustration/cartoon.
- TEXT-FREE: no letters/numbers/logos/brand names/signage/screens/displays/UI/
  watermarks/captions anywhere (phone screen must be turned away / not legible).
- Person seen from behind or three-quarter so the face is not clearly readable.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage:
    ATTEMPT=1 /home/chino/video-venv/bin/python3 \
        scripts/gen-spcx-starlink-mobile-spectrum-hero-2026.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "spcx-starlink-mobile-spectrum-carrier-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
MODEL = os.environ.get("MODEL", "fal-ai/flux/schnell")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, no "
    "codes, no labels, no signage, no street signs, no road markings with "
    "writing, no billboards, no posters, no plaques, no brand names, no logos, "
    "no watermarks, no captions. The smartphone in the person's hand is held "
    "away from the camera so its screen is turned away and shows no legible "
    "interface and no writing; no other screen, monitor or display appears "
    "anywhere. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no synthwave, no glowing lines, no light trails, no "
    "geometric patterns, no futuristic HUD or augmented-reality overlays, no "
    "abstract cyberspace. This is a real photograph of a real place."
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a lone person standing on a quiet "
        "rural dirt road at dusk in the American countryside, seen from behind "
        "in three-quarter view, holding a smartphone up toward the twilight "
        "sky as if catching a signal, their face turned away from the camera "
        "and not visible, wearing a plain jacket. The camera looks down the "
        "road over the person's shoulder at a wide flat landscape of rolling "
        "farm fields, fence posts, and a few distant trees, with an open sky "
        "above. High in the deepening blue-grey twilight a bright evenly-spaced "
        "train of small bright points of light streaks across the sky in a "
        "diagonal line, like a string of moving satellites. Far away on the "
        "horizon a single slender rural cell tower stands as a small dark "
        "silhouette against the afterglow. Warm dusk palette of soft orange "
        "and amber near the horizon fading up into deep blue, long soft "
        "shadows, faint ground mist. Realistic photo, shallow depth of field, "
        "professional lighting, the person and the near road crisp while the "
        "fields and horizon soften into gentle blur, natural film grain, "
        "photorealistic, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "Realistic photograph shot on a full-frame camera, 35mm lens at f/2, "
        "shallow depth of field, not a render: a young farmer standing alone "
        "in a wide open field at blue-hour dusk, seen in three-quarter profile "
        "from behind and to the side so their face is obscured, one arm raised "
        "holding a plain smartphone toward the sky. Around them tall grasses "
        "and a weathered wooden fence fade into the soft blur of evening, with "
        "a barn far off in the dim background. Overhead the sky is a warm "
        "gradient from amber at the horizon to deep indigo above, and across "
        "it runs a crisp diagonal chain of bright small satellite lights in a "
        "tidy line. A distant thin cell tower breaks the far horizon as a tiny "
        "silhouette. Warm golden-blue dusk light, soft haze, natural sensor "
        "noise, very slight film grain, authentic editorial photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Professional stock photograph of a solitary figure in a plain winter "
        "coat standing on a gravel country road at dusk, seen from directly "
        "behind, gazing up at the evening sky while holding a smartphone aloft, "
        "their back to the camera. The view opens onto gentle rural farmland "
        "with bare hedgerows and a low ridge, wrapped in soft twilight "
        "atmosphere. Stretching across the deepening blue sky above is a "
        "bright line of evenly spaced satellite lights trailing in a neat "
        "diagonal procession. On the far horizon a single distant cell mast "
        "rises as a slim dark shape. Warm amber and rose glow lingering at the "
        "horizon under a cool blue dome, long shadows across the road, ground "
        "haze catching the last light. Realistic photo, shallow depth of "
        "field, professional lighting, sharp foreground figure against a soft "
        "blurred landscape, natural grain, photorealistic, high detail, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "Photojournalistic documentary stock photograph taken on a real camera, "
        "85mm lens at f/2, unretouched, not CGI: a lone rural resident stands "
        "on an empty countryside lane at blue hour, seen in three-quarter "
        "profile facing away from the lens toward a broad open valley of farm "
        "fields, holding a smartphone up at arm's length toward the sky. The "
        "phone is angled away so its screen is not visible. Above, the "
        "twilight sky glows amber near the horizon and deepens to indigo "
        "overhead, and a bright train of small satellites arcs across it in a "
        "clean diagonal line of evenly spaced points. A single thin cell tower "
        "stands far off on the horizon as a tiny silhouette among the fields. "
        "Warm dusk light, soft mist low over the ground, natural film grain, "
        "faint lens vignette, honest available-light exposure, realistic skin "
        "and fabric texture, no studio lighting, shallow depth of field, "
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
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} MODEL={MODEL}")
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
