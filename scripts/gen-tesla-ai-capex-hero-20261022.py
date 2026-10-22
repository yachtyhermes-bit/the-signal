#!/usr/bin/env python3
"""Generate hero for tesla-ai-capex-cut-optimus-terafab-2026 (fal flux/schnell).

Subject: Tesla Q3 2026 results. Capex for 2026 cut to about $20B while the
company promises a bigger 2027-2028 spending ramp on Optimus humanoid robots,
the Cybercab, and its own AI chip fab ("Terafab").

Scene: photo-realistic editorial photograph of a humanoid robot standing on an
automotive assembly line inside a brightly lit modern car factory — real steel
car bodies, concrete factory floor, workers blurred in the background.

Deliberately DISTINCT from recent heroes: no data center, no server aisle, no
chip macro, no boardroom, no abstract network graphic.

Rules: PHOTO-REALISTIC stock photograph only; no digital art / neon / glowing
lines / geometric patterns / text / logos. Generate 1440x810, finalize
1920x1080 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  SLUG=tesla-ai-capex-cut-optimus-terafab-2026 ATTEMPT=1 \
    /home/chino/video-venv/bin/python3 scripts/gen-tesla-ai-capex-hero-20261022.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "tesla-ai-capex-cut-optimus-terafab-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
PHOTO_DIR = os.environ.get("PHOTO_DIR", "/home/chino/thesignal/public/img/articles")
MIRROR_DIR = os.environ.get("MIRROR_DIR", "/home/chino/thesignal/img/articles")
BACKUP_DIR = os.environ.get("BACKUP_DIR", "/home/chino/thesignal/_backup_dist/img/articles")
OUTPUT = PHOTO_DIR + "/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no signage, no labels, no plates, no "
    "placards, no safety-sign lettering, no logos, no brand marks, no "
    "trademarks, no watermark, no signature. No illustration, no digital art, "
    "no cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no holographic graphics, no "
    "HUD overlays, no augmented-reality elements, no server rack, no server "
    "aisle, no data-center hallway, no abstract background, no sci-fi "
    "spaceship styling, no chrome fantasy armour."
)

ROBOT = (
    "a life-size humanoid robot of industrial design: matte light-grey and "
    "dark graphite composite panels over machined aluminium limbs, exposed "
    "precision joints at the elbows, wrists and knees, a smooth featureless "
    "head with a simple dark visor band instead of a face, two articulated "
    "five-fingered hands resting at its sides. It looks like a working "
    "prototype machine built for a factory, not a science-fiction character"
)


PROMPTS = {
    "1": (
        "A photo-realistic editorial stock photograph shot on a 35mm camera "
        "with a 50mm lens at f/2, available factory light only, professional "
        "photojournalism for a business magazine. " + ROBOT + ". It stands "
        "upright on the concrete floor of a modern automotive assembly line, "
        "body turned three-quarters toward the camera, head angled slightly "
        "toward the paint-shop end of the hall. Immediately behind it, bare "
        "unpainted steel car bodies hang from an overhead conveyor, their "
        "grey metal shells catching the light, seams and spot welds visible. "
        "A long row of industrial work stations, pneumatic tools, cable "
        "trays and yellow floor guide stripes recedes into the distance. Two "
        "assembly workers in navy uniforms and pale hard hats work at a "
        "bench far behind, softly out of focus. Lighting is bright, even, "
        "colour-neutral LED high-bay illumination with soft shadows on the "
        "polished concrete and a faint haze of workshop air. Shallow depth "
        "of field: the robot's forearm, torso panels and nearest steel body "
        "are tack sharp with honest brushed-metal texture, fine scratches "
        "and dust, while the conveyor, the workers and the far end of the "
        "plant dissolve into creamy optical bokeh. Real lens blur, visible "
        "fine film grain, subtle vignette, honest exposure with true blacks "
        "and clean highlights, slightly imperfect handheld framing. "
        "Photorealistic, very high detail, documentary realism, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched documentary photograph taken inside a "
        "brightly lit car factory with a 35mm lens at f/2.8 — visibly a real "
        "camera photograph, not a render. " + ROBOT + ". The robot stands at "
        "the edge of a moving assembly line, one arm slightly raised as if "
        "mid-task, its shadow falling across the grey concrete floor beside "
        "a strip of worn yellow safety paint. To its left a partially "
        "assembled electric car body — bare steel shell, open door apertures, "
        "no glass — sits on a steel conveyor skid. Overhead, rows of "
        "fluorescent and LED fixtures run the length of the hall; steel roof "
        "trusses, ducts and cable trays fill the upper frame. In the middle "
        "distance three workers in dark work clothes and pale helmets stand "
        "in conversation near a tool trolley, completely blurred. Cool "
        "neutral daylight-balanced light with warm highlights on the metal. "
        "Shallow depth of field: the robot's chest panel, shoulder and hand "
        "are sharp with honest material texture, everything behind it melts "
        "into soft bokeh. Visible film grain, slight lens flare at the "
        "ceiling lights, mild chromatic fringing at the frame edge, natural "
        "colour, candid off-centre composition. Photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    "3": (
        "A photo-realistic wide editorial photograph of a modern automotive "
        "plant floor, shot on a 35mm camera at f/4, natural industrial "
        "lighting, for a business magazine feature. " + ROBOT + ". It stands "
        "centred in a wide aisle between two assembly lines, facing the "
        "camera, feet planted on scuffed concrete with dark oil stains and "
        "faded floor markings. On both sides, rows of steel car-body shells "
        "and chassis frames on overhead conveyors recede in perspective "
        "toward a far wall of tall windows admitting pale overcast daylight. "
        "Robotic welding cells with their safety fencing sit further down "
        "the line, and a handful of workers in high-visibility vests move "
        "between the stations, all softly blurred. The air carries a faint "
        "haze; the light is bright, neutral and directional from the windows "
        "on the left. Shallow depth of field with the humanoid robot and the "
        "nearest steel body crisp, the long hall behind falling into smooth "
        "bokeh. Real optical blur, subtle film grain, slight vignette, "
        "honest contrast, documentary framing. Photorealistic, very high "
        "detail, 16:9 landscape composition. " + NO_TEXT
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
    seed = int(os.environ.get("SEED", "0"))
    arguments = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": steps,
        "enable_safety_checker": False,
    }
    if seed:
        arguments["seed"] = seed
    result = fal_client.subscribe(model, arguments=arguments)
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


def photo_finish(img, seed=11, grain=5.0, softness=0.7):
    """Adds the artefacts a real available-light frame carries so the file
    behaves like a photograph (borrowed from scripts/hero-photo-finish.py)."""
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
    vig = 1.0 - 0.14 * np.clip(dist / 1.42, 0, 1) ** 2
    arr *= vig[:, :, None]

    lum = rng.normal(0.0, grain, (h, w, 1))
    chroma = rng.normal(0.0, grain * 0.45, (h, w, 3))
    arr += lum + chroma

    arr[:, :, 1] *= 1.010
    arr[:, :, 2] *= 0.988
    arr = arr * 0.97 + 5.0
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
    for d in (MIRROR_DIR, BACKUP_DIR):
        os.makedirs(d, exist_ok=True)
        path = d + "/" + SLUG + ".jpg"
        img.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
        print("Mirrored to " + path)


if __name__ == "__main__":
    main()
