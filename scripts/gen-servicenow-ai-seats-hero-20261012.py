#!/usr/bin/env python3
"""Hero for servicenow-agentic-ai-seat-model-rerate-2026.

Subject: ServiceNow -- enterprise workflow platform (IT service desk, HR,
security ops) now pitching AI agents as the new unit of work. Article angle:
do AI agents replace per-seat software?

Scene (commit to option b): a real operations floor, people at desks in warm
practical lighting, shallow depth of field on a single worker reviewing a case
queue on a monitor whose screen content is blurred and entirely text-free.

NO text of any kind anywhere (no letters, numerals, logos, signage, screen UI
text, watermarks). NO data center, no server racks, no server aisle, no cable
spaghetti, no neon/glowing lines, no abstract shapes, no 3D render look.
Strictly photorealistic editorial stock photography.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "servicenow-agentic-ai-seat-model-rerate-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NEGATIVE = (
    "Absolutely no text anywhere in the image: no words, no letters, no numerals, "
    "no logos, no branding, no signage, no posters, no labels, no captions, no screen "
    "UI text, no interface elements, no document text, no handwriting, no watermarks, "
    "no glyphs, no symbols. Every monitor and screen displays only soft blurred "
    "out-of-focus colour with no readable or unreadable writing of any kind, all "
    "screens turned away or heavily defocused. No data center, no server room, "
    "no server racks, no server aisle, no cable spaghetti. No neon, no synthwave, "
    "no glowing laser lines, no digital fantasy effects, no abstract shapes, no "
    "geometric patterns, no 3D render look, no CGI. Strictly photorealistic "
    "editorial stock photography, natural film grain, warm human tones."
)

PROMPT = (
    "Professional stock photograph of a real enterprise operations floor in the "
    "early evening, shot on an 85mm lens at f/2.0 on a full-frame camera, shallow "
    "depth of field. In sharp focus in the foreground, a single office worker in "
    "smart-casual business attire sits at a tidy modern desk, leaning in and "
    "reviewing a case queue on a large desktop monitor; the monitor's screen is "
    "heavily blurred and softly glowing with diffuse colour only, turned slightly "
    "away from the lens so its contents are completely unreadable. Behind them in "
    "soft bokeh, rows of colleagues at neighbouring desks work at their terminals "
    "in a warm open-plan office, under warm practical lighting from ceiling "
    "pendants and desk lamps, with cool dusk light through large windows far behind. "
    "Muted warm amber and teal colour grade, wood and fabric textures, subtle film "
    "grain, extremely high detail, realistic photo, professional lighting, candid "
    "documentary workplace photography, 16:9 landscape aspect ratio. " + NEGATIVE
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


def gen(seed, out):
    import fal_client
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": seed,
    })
    url = None
    if result.get("images"):
        url = result["images"][0]["url"]
    elif result.get("image"):
        url = result["image"]
    if not url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    img = Image.open(out)
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(out, "JPEG", quality=92)
    print(f"saved {out} size={Image.open(out).size} bytes={os.path.getsize(out)}")


if __name__ == "__main__":
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261012
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/servicenow_hero_1.jpg"
    gen(seed, out)
