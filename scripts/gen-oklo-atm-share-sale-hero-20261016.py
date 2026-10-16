#!/usr/bin/env python3
"""Hero for oklo-atm-billion-dollar-share-sale-2026 via fal flux/schnell.

Subject: Oklo (nuclear / AI power) — $1B at-the-market share sale and the cost of
capital for pre-revenue AI-power companies. Capital-intensive reactor hardware that
is not yet producing revenue.

Scene chosen (varied from recent heroes): a large cylindrical small modular reactor
vessel module strapped to a multi-axle heavy-haul trailer in the laydown yard of an
industrial nuclear construction site at dusk. NOT a fabrication-floor centrepiece
(NuScale hero already used that), NOT a data-centre / server-room aisle.

Rules: photo-realistic stock photography ONLY. No text/logos/watermarks, no people,
no neon/synthwave/glow/geometric/abstract/render looks.

Usage: SEED=1234 python3 scripts/gen-oklo-atm-share-sale-hero-20261016.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = "oklo-atm-billion-dollar-share-sale-2026"
SEED = int(os.environ.get("SEED", "20261016"))
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810          # 16:9 generation size
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no numbers, "
    "no codes, no serial numbers, no barcodes, no labels, no plaques, no nameplates, "
    "no decals, no stencils or stenciled writing, no markings of any kind, no logos, "
    "no brand names, no signage, no posters, no screens, no monitors, no displays, "
    "no UI, no charts, no watermark, no captions. "
    "No people, no hands, no faces, no human figures, no silhouettes, no body parts. "
    "No illustration, no digital art, no cartoon, no 3D render, no neon, no glowing "
    "lines, no glowing sci-fi lines, no geometric patterns, no abstract art, no synthwave, "
    "no lens flare, no bokeh lights. Not a server room, not a data-centre aisle, "
    "not an interior corridor."
)

VARIANT = os.environ.get("VARIANT", "2")

WIDE_INTRO = (
    "Professional stock photograph of a small modular nuclear reactor vessel module on a "
    "heavy-haul transport trailer in the gravel laydown yard of a nuclear power station "
    "under construction, at dusk, shot on a full-frame DSLR with a 35mm lens from a "
    "natural standing eye level about thirty metres away. "
    "The whole low-bed multi-axle trailer and its load are visible, sitting in the centre "
    "of the frame and filling roughly half the frame width, with a broad expanse of gravel "
    "yard in the foreground and a wide open dusk sky above, leaving generous empty space "
    "on all sides for cropping. "
)

VARIANTS = {
    "2": WIDE_INTRO + (
        "The load is a massive matte grey steel cylindrical pressure vessel about ten metres "
        "long with machined flanged end caps, thick bolted pipe nozzles, welded lifting lugs "
        "and circumferential seam rings, resting in a heavy steel transport saddle and secured "
        "to the trailer deck with thick tensioned chain binders. "
        "Around the yard: graded earth and gravel, stacked steel reinforcement bundles, a "
        "half-built steel containment structure and a tall lattice tower crane in the softly "
        "blurred background, a high-voltage substation with transformers and transmission "
        "pylons to one side. "
        "Late dusk with low warm sunlight raking in from the side against cool blue shadow "
        "ambient light, faint atmospheric haze, muted steel grey, rust brown and dusty earth "
        "tones, tall site floodlight poles just beginning to glow. "
        "Candid documentary construction-industry photography, realistic and slightly "
        "imperfect, natural ambient light and natural colour, gentle film grain, the module "
        "sharp and the background falling gently out of focus. "
        "16:9 landscape aspect ratio. " + NO_TEXT
    ),
}

PROMPT = VARIANT_PROMPT = VARIANTS[VARIANT]

LEGACY_PROMPT = (
    "Professional stock photograph of a large cylindrical small modular nuclear reactor "
    "vessel module strapped down on a multi-axle heavy-haul transport trailer at an "
    "industrial construction site at dusk. "
    "The reactor module is a massive matte grey steel pressure vessel, roughly ten metres "
    "long, with machined flanged end caps, thick bolted pipe nozzles, welded lifting lugs "
    "and circumferential seam rings, resting horizontally in a heavy steel transport "
    "saddle and secured to the trailer deck with thick tensioned chains and ratchet "
    "binders; the trailer is a low-bed multi-axle rig with rows of heavy wheels and "
    "a tractor unit at the front. "
    "The setting is a gravel laydown yard of an unfinished nuclear power station: graded "
    "earth and gravel, steel reinforcement bar bundles, a half-built steel containment "
    "structure and a tall lattice tower crane in the softly blurred background, a "
    "high-voltage substation with transformers and transmission pylons off to one side. "
    "Late dusk, low warm sunlight raking from the side with cool blue shadow ambient "
    "light, faint atmospheric haze, muted steel grey, rust brown and dusty earth tones, "
    "a few tall site floodlight poles just beginning to glow. "
    "Subject centred with generous space around it for cropping, shot on a 35mm lens on "
    "a full-frame camera, shallow depth of field with the module crisply sharp and the "
    "background falling gently out of focus. "
    "Extremely high detail, 8k, documentary industrial photography, "
    "16:9 landscape aspect ratio. " + NO_TEXT
)


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


def main():
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal-ai/flux/schnell (seed={SEED})...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": SEED,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT).convert("RGB")
    print(f"Downloaded: {OUTPUT} size={img.size} bytes={len(r.content)}")

    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT} dimensions={img.size} bytes={size}")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Copied to {BACKUP} bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
