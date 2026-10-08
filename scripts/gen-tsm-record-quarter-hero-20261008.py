#!/usr/bin/env python3
"""Hero image for tsm-record-quarter-ai-foundry-bottleneck-2026 via fal flux/schnell.

Subject: TSMC (TSM) — the article's thesis is that TSMC posts a record quarter on AI demand,
but the real story is foundry capacity: advanced-node wafer supply is the bottleneck everyone
else is queuing behind.
Theme: an extreme-ultraviolet (EUV) lithography tool inside a semiconductor cleanroom —
the exact machine that gates advanced-node capacity.
Distinct from the other semiconductor heroes (chip close-ups, wafer dicing floor,
server racks, data-center aisles).
NO people, NO hands or body parts, NO text/lettering/numbers/logos anywhere in frame.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "tsm-record-quarter-ai-foundry-bottleneck-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no watermarks, no signage, no flags. "
    "No people, no hands, no faces, no human figures, no silhouettes, no technicians. "
    "No neon lights, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Strictly photorealistic editorial photography."
)

PROMPT = (
    "Professional editorial photograph shot on a 35mm lens on a full-frame camera inside a modern "
    "semiconductor cleanroom under even cool white ceiling light. "
    "A massive extreme-ultraviolet lithography machine dominates the frame: a sealed white and "
    "stainless-steel enclosure with precision optical columns, cable bundles, and pneumatic lines "
    "routed into its side, mounted on a heavy vibration-isolated granite base. "
    "Glossy epoxy floor with a faint mirror reflection, brushed aluminium equipment banks and "
    "yellow-tinted safety glazing receding in soft focus toward a bright clean corridor. "
    "Faint haze of filtered air counterflow drifts through the frame. "
    "Desaturated cool industrial palette of white, steel grey, and faint amber accents, "
    "authentic depth of field, subtle film grain, extremely high detail, 8k resolution, "
    "documentary semiconductor manufacturing photography, 16:9 landscape aspect ratio. "
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

    print(f"Generating hero for {SLUG} via fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": 20261008,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT)
    print(f"Saved: {OUTPUT} size={img.size} bytes={len(r.content)}")
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92)
        print(f"Upscaled to {FINAL_W}x{FINAL_H}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92)
    print(f"Copied to {BACKUP}")
    print("Done!")


if __name__ == "__main__":
    main()
