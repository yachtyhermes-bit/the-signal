#!/usr/bin/env python3
"""Generate hero for orcl-credit-default-swap-ai-debt-2026 (fal flux).

Subject: Oracle's AI data-center buildout debt load and the widening stress in
its credit-default swaps.

Scene: a vast data-center construction site at dusk — steel framing, cranes,
cooling pipes, half-finished halls stretching into the distance, warm work
lights — professional editorial stock photograph.

Rules: PHOTO-REALISTIC stock photograph only. NO interior server aisle, NO
glowing hallway, NO abstract/neon/digital art, no text or lettering anywhere.
Generate 1440x810, finalize 1920x1080 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-orcl-credit-default-swap-ai-debt-hero-20261019.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "orcl-credit-default-swap-ai-debt-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no labels, no signage, no logos, no brand "
    "marks, no trademarks, no watermark, no signature, no construction hoarding "
    "lettering, no safety placards with readable words. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no concept art, no neon, "
    "no glowing lines, no light trails, no synthwave, no geometric patterns, "
    "no holographic or futuristic HUD graphics, no overlay graphics, no "
    "abstract background, no interior server aisle, no server racks, no long "
    "glowing corridor, no sci-fi architecture."
)

PROMPTS = {
    "1": (
        "A photo-realistic editorial stock photograph for a business magazine, "
        "shot on a 35mm DSLR with a tilt-shift lens at f/5.6 from a slightly "
        "elevated vantage point, professional architectural photojournalism, "
        "available light plus site work lamps, 16:9 landscape composition. "
        "The subject is an enormous data-center construction site at dusk: a "
        "vast half-built campus of long rectangular halls stretching away "
        "toward a low horizon, most of them still open steel skeletons with "
        "exposed roof trusses and grey concrete slab floors, a few already "
        "clad in pale silver-grey metal panels. In the near foreground a "
        "bundle of thick galvanised cooling pipes and ductwork lies on the "
        "dirt beside a concrete pad, with rebar bundles, plywood sheets and a "
        "stack of steel beams. Tall lattice tower cranes rise above the frames "
        "at intervals, their jibs silhouetted against the fading sky, and a "
        "mobile boom crane with a telescopic arm stands mid-frame. Orange and "
        "white work lights on tripods and on the crane masts throw warm pools "
        "of amber light over the steelwork and the pale concrete, while the "
        "sky behind is a deep blue-grey dusk with the faintest amber band at "
        "the horizon and a few thin clouds. Dust haze softens the distant "
        "halls, making successive rows of steel frames fade from crisp dark "
        "metal into pale silhouettes. Shallow depth of field: the cooling "
        "pipes and the dirt in the immediate foreground are tack sharp with "
        "honest surface texture — rust bloom, mud, scratches on the metal — "
        "and the far halls fall into soft atmospheric blur. Real optical "
        "blur, visible fine film grain, subtle vignette, honest exposure with "
        "true blacks and warm highlights, slight halation around the work "
        "lamps, candid imperfect framing, a few distant tiny worker figures in "
        "hi-vis vests for scale. Photorealistic, very high detail, natural "
        "colour, no stylisation. "
        + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched documentary photograph of a colossal "
        "AI data-center under construction at blue hour, taken on a full-frame "
        "camera with a 24mm lens at f/4, professional editorial stock "
        "photography, 16:9 landscape. Low camera position on a gravel access "
        "road between two enormous unfinished buildings: on the left a long "
        "steel frame with bare columns and open bays, on the right a "
        "partially clad hall with silver metal wall panels and a row of dark "
        "louvred cooling intakes. Overhead runs a thick insulated chilled-water "
        "pipe run on steel supports, its white lagging catching warm light. "
        "Two crawler cranes and one tall tower crane stand against the dusk "
        "sky; the tower crane has small red aviation lights at its tip. The "
        "site is lit by warm sodium work lamps on tall poles, throwing pools of "
        "amber light across the gravel, the concrete and the steel, with cool "
        "deep blue shadow filling the gaps between them. The sky is a smooth "
        "gradient from dusty amber at the horizon to deep indigo overhead, "
        "with a thin crescent moon. Distant rows of half-finished halls recede "
        "in haze toward the horizon so the scale reads as industrial sprawl. "
        "Shallow depth of field: the gravel, the pipe lagging and a coil of "
        "black cable in the foreground are sharp with gritty real texture, "
        "the far structures melting into soft blur. Real optical blur, visible "
        "film grain, mild lens flare from a work lamp at the frame edge, "
        "subtle chromatic fringing, honest exposure, a couple of tiny "
        "silhouetted workers walking between the buildings for scale. "
        "Photorealistic, high detail, natural muted colour, documentary "
        "realism, no stylisation. "
        + NO_TEXT
    ),
    "3": (
        "A photo-realistic editorial stock photograph of a gigantic data-center "
        "construction site at dusk seen from a distance across bare earth, "
        "shot with a long lens on a tripod, compressed perspective, warm work "
        "lights against a cold blue sky, 16:9 landscape. Rows of long "
        "unfinished halls with exposed steel roof trusses and grey concrete "
        "walls recede into the distance, a forest of tower cranes above them, "
        "stacks of precast concrete panels and coiled cooling pipe laid out on "
        "the site. Foreground: a chain-link fence line and muddy tyre tracks "
        "with a single portable site light tower glowing warm amber. Haze "
        "compresses the far halls into pale layered silhouettes. Shallow depth "
        "of field with the foreground fence and light tower sharp and the site "
        "beyond softening into atmospheric blur. Real optical blur, visible "
        "film grain, subtle vignette, honest exposure, true blacks, warm "
        "highlights. Photorealistic, very high detail, documentary realism. "
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
    model = os.environ.get("MODEL", "fal-ai/flux/dev")
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


def photo_finish(img, seed=17, grain=4.5, softness=0.7):
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
    vig = 1.0 - 0.20 * np.clip(dist / 1.42, 0, 1) ** 2
    arr *= vig[:, :, None]

    lum = rng.normal(0.0, grain, (h, w, 1))
    chroma = rng.normal(0.0, grain * 0.45, (h, w, 3))
    arr += lum + chroma

    arr[:, :, 1] *= 1.008
    arr[:, :, 2] *= 0.988
    arr = arr * 0.96 + 7.0
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
    if size < 102400:
        img.convert("RGB").save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT)) + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.convert("RGB").save(BACKUP, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + BACKUP)


if __name__ == "__main__":
    main()
