#!/usr/bin/env python3
"""Hero for ktos-valkyrie-europe-cca-drone-2026 (Kratos U740 Valkyrie / XQ-58A
uncrewed jet combat aircraft — first European test flight with Airbus).

Scene: a single tailless jet-powered stealth UCAV on a damp asphalt runway at
first light on a Northern European airfield, low hangar + grass berm + birch/pine
treeline in morning mist behind, cold blue-grey dawn light with a low warm sun
on the horizon, wet asphalt reflecting the airframe. Long 200mm lens, low
three-quarter front angle, shallow depth of field, editorial aviation
photojournalism. Strictly photorealistic, no text/insignia, no people.
"""
import os
import sys
import shutil
import requests
from PIL import Image

SLUG = "ktos-valkyrie-europe-cca-drone-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080
SEED = 20261012

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no tail numbers, no roundels, no insignia, "
    "no watermarks, no signage. No people, no hands, no faces, no human figures, no silhouettes, "
    "no aircrew, no ground crew. No neon lights, no synthwave, no glowing laser lines, "
    "no digital fantasy effects, no 3D render sheen, no lens flares. "
    "Strictly photorealistic editorial photography."
)

PROMPT = (
    "Professional editorial aviation photograph shot on a 200mm telephoto lens at f/4 on a "
    "full-frame camera, shallow depth of field, of a single tailless jet-powered uncrewed "
    "combat aircraft rolling on a damp asphalt runway at first light on a Northern European "
    "airfield. The aircraft is a sleek matte-grey stealthy flying drone with a dorsal air "
    "intake behind the nose, absolutely no cockpit canopy and no propeller, clean swept-back "
    "wings and a V-tail, seen from a low three-quarter front angle so its long slender "
    "airframe fills the frame diagonally across the composition. The matte grey composite "
    "skin is plain and unmarked, faint panel lines and a dull operational finish, angular "
    "faceted forward fuselage, landing gear struts with tyres on the wet tarmac. Behind it "
    "in soft focus: a low grey airfield hangar, a tall hedgerow grass berm, and a line of "
    "birch and pine trees dissolving into morning mist. Cold blue-grey overcast dawn light "
    "with a low warm band of sun breaking through low on the horizon, wet asphalt on the "
    "runway reflecting the aircraft beneath it in a soft sheen. A few pieces of real "
    "unmarked ground equipment far in the background, out of focus. Realistic atmospheric "
    "haze, subtle film grain, muted cinematic colour grade, extremely high detail, 8k "
    "resolution, 16:9 landscape aspect ratio, documentary photojournalism. "
    + NO_TEXT
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
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)
    img = Image.open(OUTPUT)
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copyfile(OUTPUT, BACKUP)
    print("Saved", OUTPUT, Image.open(OUTPUT).size, os.path.getsize(OUTPUT))


if __name__ == "__main__":
    main()
