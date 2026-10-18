#!/usr/bin/env python3
"""Generate hero for meta-capex-bill-ai-payback-2026 (fal flux/schnell).

Subject: Meta Platforms Q3 2026 earnings (Wed Oct 21). The angle is the AI
capital-spending bill ($130-145B guided for 2026) against the advertising
machine that pays for it — the feed is the cash register.

Scene: photo-realistic editorial photograph of a person in a warm-lit cafe at
dusk, holding a phone, scrolling a social feed; screen glow on the face,
shallow depth of field. Alternative: smart glasses on a table beside a phone.

Deliberately DISTINCT from recent heroes: no data-center hallway, no server
aisle, no chip macro, no boardroom, no abstract globe/network graphic.

Rules: PHOTO-REALISTIC stock photograph only; no digital art / neon / glowing
lines / geometric patterns / text / logos. Generate 1440x810, finalize
1920x1080 center-crop JPEG q92, mirror to _backup_dist.

Usage:
  SLUG=meta-capex-bill-ai-payback-2026 ATTEMPT=1 \
    /home/chino/video-venv/bin/python3 scripts/gen-meta-capex-hero-20261018.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "meta-capex-bill-ai-payback-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no captions, no usernames, no hashtags, no app "
    "interface labels, no notification badges with digits, no logos, no brand "
    "marks, no trademarks, no watermark, no signature. No signage of any kind "
    "anywhere: no storefront lettering, no lit signs, no neon signs, no menu "
    "boards, no chalkboards, no posters, no books, no magazines, no "
    "newspapers, no printed paper of any kind. No readable content on the "
    "phone screen at all — the screen is a soft out-of-focus wash of pale "
    "light with only vague unreadable shapes. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no glowing lines, no "
    "light trails, no synthwave, no geometric patterns, no holographic or "
    "futuristic HUD graphics, no overlay graphics, no augmented-reality "
    "elements, no server rack, no server aisle, no data-center hallway, no "
    "abstract background."
)

PROMPTS = {
    "1": (
        "A photo-realistic editorial stock photograph shot on 35mm film with a "
        "fast prime lens at f/1.8, available light only, professional "
        "photojournalism for a business magazine. A woman in her early "
        "thirties sits alone at a bare round cafe table in the late evening, "
        "a single small espresso cup and saucer the only other object on the "
        "tabletop. Nothing else lies on the table — no paper, no packaging, "
        "no phone accessories. She holds a black smartphone in both hands at "
        "chest height, thumbs mid-scroll, head tilted slightly down toward "
        "the screen. The pale glow of the phone screen lights the lower half "
        "of her face and the undersides of her fingers while warm amber "
        "tungsten light from cafe pendant lamps rakes across her hair and "
        "shoulder from the left. Behind her, the cafe interior falls into "
        "deep creamy bokeh — blurred hanging bulbs, the soft dark shapes of "
        "other tables and seated silhouettes, and a window fogged at the "
        "edges showing the blue dusk street outside, all dissolved into "
        "shapeless glow. Shallow depth of field: her hands and the phone are "
        "tack sharp with honest skin texture, visible pores and fine fabric "
        "detail, everything else softly blurred. Real optical blur, visible "
        "film grain, subtle vignette, slightly imperfect handheld framing, "
        "candid unposed expression, honest exposure with true blacks and "
        "warm highlights, faint halation around the light sources. "
        "Photorealistic, very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "An authentic, unretouched candid photograph taken on a city street "
        "at dusk with a 50mm lens at f/1.4, available light only — visibly a "
        "real camera photograph, not a render. A man in a dark wool coat "
        "stands at the corner of a wet stone pavement, leaning his shoulder "
        "against a plain dark brick wall, looking down at the black "
        "smartphone he holds in one hand, his other hand in his pocket. The "
        "phone's pale screen casts a soft glow onto his cheek, jaw and the "
        "collar of his coat while the last blue-grey daylight from the "
        "after-sunset sky rim-lights his hair and shoulder. Around him the "
        "street is out of focus: warm amber light spilling from an "
        "unlettered shop window onto wet cobblestones, the blurred headlights "
        "of passing traffic as soft glowing discs, a bare tree branch "
        "silhouetted at the top corner. No shop signs, no lettering, no "
        "posters anywhere. Shallow depth of field — his face, the phone and "
        "the hand holding it are tack sharp with honest skin texture and "
        "visible coat fibres, the street melting into smooth bokeh. Real "
        "optical blur, visible film grain, slight lens flare from a "
        "streetlight at the frame edge, subtle chromatic fringing, honest "
        "exposure, candid off-centre composition. Photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A photo-realistic editorial still-life photograph for a business "
        "magazine, shot on a macro lens at a shallow aperture. On a warm "
        "walnut cafe table beside a white ceramic cup of coffee sits a pair "
        "of dark-framed smart glasses, folded, their lenses catching a soft "
        "reflection of the room. Just behind and slightly to the left lies a "
        "black smartphone face-down, its edge gleaming. A person's blurred "
        "hand rests at the very edge of the frame, out of focus. Late "
        "afternoon window light rakes across the table from the left in warm "
        "amber, with cool blue dusk light filling the shadows and a faint "
        "coffee-cup shadow falling across the wood grain. Very shallow depth "
        "of field: the glasses and the table grain immediately around them "
        "are tack sharp with honest micro-texture and a little dust, while "
        "the cup, the phone and the background dissolve into creamy bokeh. "
        "Real optical blur, natural fine grain, subtle vignette, honest "
        "exposure, relaxed imperfect composition. Photorealistic, very high "
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


def photo_finish(img, seed=11, grain=6.0, softness=0.9):
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
