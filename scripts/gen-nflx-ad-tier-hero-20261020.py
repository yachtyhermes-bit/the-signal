#!/usr/bin/env python3
"""Generate hero for nflx-q3-print-ad-tier-repricing-2026 (fal flux/schnell).

Subject: Netflix (NFLX) ahead of its Q3 2026 earnings print — the ad-supported
tier, engagement, and the 2026 de-rating of the multiple.

Scenes: consumer-media photography, not infrastructure. A living room at dusk
with a glowing textless television; an advertising/creative studio desk; a
film/television production soundstage.

Deliberately DISTINCT from recent heroes: no data-center hallway, no server
aisle, no silicon die/chip macro, no circuit board, no neon/synthwave, no
glowing lines, no geometric patterns, no digital art, no boardroom.

Rules: PHOTO-REALISTIC stock photograph only; no digital art / neon / glowing
lines / geometric patterns / text / logos. Generate 1440x810, finalize
1600x900 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-nflx-ad-tier-hero-20261020.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "nflx-q3-print-ad-tier-repricing-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no labels, no serial numbers, no "
    "logos, no brand marks, no trademarks, no icons, "
    "no watermark, no signature. Every screen, monitor and slate in the "
    "frame is completely blank and unmarked — it shows only soft abstract "
    "light and colour with no printing of any kind, no barcodes, no "
    "stickers. There is no user interface, no app menus, no menu bars, no "
    "tiles, no thumbnails, no grids of content, no playback controls, no "
    "standby indicators. No packaging, no retail boxes, "
    "no printed paper, no manuals, no box art, no signage anywhere. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no holographic or futuristic HUD graphics, no overlay graphics, no "
    "augmented-reality elements, no server rack, no server aisle, no "
    "data-center hallway, no circuit-board macro, no abstract background."
)

PROMPTS = {
    "1": (
        "A photo-realistic editorial photograph for a business magazine, "
        "shot on a 35mm lens at f/2 with available light only, on 35mm film, "
        "professional photojournalism. A cozy modern living room at dusk, "
        "seen from behind and slightly to the side of a low grey linen sofa. "
        "One adult sits on the sofa facing away from the camera, shoulders "
        "relaxed, holding a small black remote loosely in one hand; only the "
        "back of the head, the shoulder line and the arm are visible, softly "
        "out of focus. On the wall ahead a large slim-bezel television "
        "glows with a soft, completely abstract blue-white picture — drifting "
        "pale light and gentle colour gradients only, no image content, no "
        "interface of any kind. The screen is the brightest thing in the "
        "room and throws a cool wash over the sofa back and the pale wall "
        "behind it. A warm floor lamp with a linen shade at the right of "
        "frame spills amber light across a side table, a ceramic mug and the "
        "arm of the sofa, while cool blue evening light comes through a "
        "window at the left and catches the curtain edge. Muted mid-century "
        "furnishing, oak floorboards, a wool throw folded over the sofa back. "
        "Shallow depth of field with the television and the room's far wall "
        "soft and the lamp and side table sharper in the foreground; real "
        "optical blur, visible fine film grain, subtle vignette, honest "
        "exposure with true blacks and warm specular highlights, relaxed "
        "slightly off-centre composition with negative space on the left. "
        "Photorealistic, very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A photo-realistic editorial photograph for a business magazine, "
        "shot on an 85mm lens at f/1.8, available light with a little "
        "softbox spill, professional photojournalism of a working advertising "
        "and creative studio. A worn wooden studio desk seen at a low "
        "three-quarter angle. In the near foreground a thick black script "
        "binder lies open on the desk, its pages blank and unprinted, the "
        "rings of the spine catching a thin highlight. Beside it a matte "
        "black film slate lies face up, its surface entirely blank with no "
        "writing of any kind. A cup of coffee gone cold, a scatter of "
        "pencils and a folded pair of reading glasses sit just out of focus "
        "at the edge of frame. Behind the desk a large softbox spills a "
        "gentle white light from the upper left across the binder and the "
        "wood, while two warm practical lamps in the background fill the "
        "rest of the frame with amber. An out-of-focus television monitor "
        "stands at the back of the room showing only abstract soft colour, "
        "no picture content, no interface. Scuffed desk surface with honest "
        "scratches, dust in the light, visible paper fibre on the binder "
        "pages. Very shallow depth of field: the slate face and the near "
        "edge of the binder are tack sharp while the monitor and lamps "
        "dissolve into creamy bokeh. Real optical blur, visible fine film "
        "grain, subtle vignette, slight halation around the practicals, "
        "honest neutral exposure, restrained off-centre composition with "
        "generous negative space on the right. Photorealistic, very high "
        "detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A photo-realistic editorial photograph for a business magazine, "
        "shot on a 50mm lens at f/2.2 with available set lighting, "
        "professional on-set photojournalism. The interior of a working film "
        "and television production soundstage: a black-painted stage floor "
        "stretches away from the camera, a large cinematic lighting rig hangs "
        "overhead with black diffusion frames and barn doors flared open, "
        "and a professional cinema camera sits on a wheeled dolly at "
        "mid-frame, its matte box and follow-focus visible, cables coiled "
        "loosely on the floor beside it. Far in the background, out of focus "
        "and small in frame, the silhouettes of three or four crew members "
        "stand near a set wall in dark work clothes. Hazy atmospheric light "
        "beams cut diagonally through the air from the rig, thick with dust, "
        "picking out the edges of the diffusion frames and the camera body "
        "with a warm tungsten glow; a cooler blue fill comes from off-frame "
        "right and rims the dolly's metal frame. Scuffed floorboards with "
        "gaffer-tape marks lead the eye in. Shallow depth of field with the "
        "camera and dolly sharp and the crew and rig softening into haze. "
        "Real optical blur, honest visible grain, subtle vignette, gentle "
        "bloom around the lamps, honest exposure with deep blacks and warm "
        "highlights, cinematic but documentary in feel — clearly a real "
        "photograph taken on set, not a render. Photorealistic, very high "
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
