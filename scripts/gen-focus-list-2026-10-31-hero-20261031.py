#!/usr/bin/env python3
"""Generate hero for focus-list-2026-10-31 (fal flux/schnell, Gemini fallback).

Article: The Signal weekly "Focus List" weekend long read — four stocks read over
a weekend, not a single company story. The hero must suit a calm reading moment.

Scene chosen for THIS edition: a deep WINDOW SILL AT BLUE HOUR in a quiet upstairs
room, cool blue-violet dusk light outside, blurred city rooftops far beyond the
glass. A plain unmarked mug, a closed notebook with a blank cover, a slim closed
laptop lying flat with a plain pale-grey lid, and a folded grey wool throw at the
edge of the sill. Deliberately NOT warm daylight, NOT a table, NOT a porch.

Visual distinctness (recent editions):
- 2026-10-24: covered front PORCH, chalky bench, warm low morning light.
- 2026-10-17: unknown/other.
- 2026-10-10: bright MORNING kitchen table, mug + blank notebook + pen.
- 2026-10-03: small wooden DESK against a tall bright window, autumn light.
- 2026-09-26: indoor wooden KITCHEN table with a linen cloth.
This edition: a WINDOW SILL at dusk, no table, no desk, no bench, no porch.

Rules: PHOTO-REALISTIC editorial only. NO people, no hands, no body parts.
TEXT-FREE: no letters, numbers, charts, logos, labels, watermarks anywhere.
NOT: data center, server room, neon/synthwave, 3D render, digital art, HUD.

Usage: cd /home/chino/thesignal && ATTEMPT=<n> \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-10-31-hero-20261031.py
"""
import base64
import json
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-10-31")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no legs, no body "
    "parts of any kind anywhere in the frame or at the edges of the frame. "
    "No text, no letters, no words, no numbers, no digits, no prices, no "
    "percentages, no currency symbols, no ticker symbols, no charts with "
    "axis labels, no readable graph, no brand names, no company names, no "
    "logos, no trademarks, no watermarks, no signatures, no barcodes, no QR "
    "codes, no packaging labels, no stickers, no mug printing, no newspaper, "
    "no magazine, no headlines, no book titles, no book-spine text, no "
    "printed book covers, no handwriting, no print, no legible writing or "
    "drawn marks of any kind anywhere in the image. The closed notebook has "
    "a completely plain unmarked cover. The mug is plain unmarked stoneware "
    "with no design, no logo and no text. The closed laptop lid is a smooth "
    "plain pale grey panel with no logo, no apple, no emblem, no sticker, no "
    "writing, no glowing keyboard. No phone anywhere, no smartphone anywhere, "
    "no tablet screen showing anything. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game still, no concept art, no "
    "matte painting, no neon, no synthwave colour, no glowing lines, no "
    "light trails, no abstract geometric art, no floating holographic "
    "elements, no wireframe, no dashboard, no data visualisation, no data "
    "center, no server room, no server racks, no server aisle, no cable run, "
    "no GPU racks, no robots."
)

COMMON = (
    "This is a quiet observational editorial still life, not a staged "
    "commercial product shot and not a hero render: the objects sit loosely "
    "off-centre, the framing is relaxed and a little careless, and foreground "
    "elements cut into the edges of the frame. It is a real, actual camera "
    "photograph, not a computer image and not an AI render: there is visible "
    "sensor noise and fine film-like grain in the shadows and midtones, a "
    "trace of chromatic aberration on high-contrast edges, a little dust and "
    "a few tiny specks on the fabric, real-world clutter and small flaws, "
    "slightly uneven white balance, the dusk sky outside the glass clipping "
    "softly, the shadows lifting with true noise rather than being perfectly "
    "clean, a natural asymmetric hand-held tilt, and a slightly imperfect, "
    "unretouched documentary snapshot feel. Honest available-light exposure, "
    "not a lit set and not an HDR composite. Shallow depth of field from a "
    "wide aperture on a 35mm lens on a full-frame camera, real optical lens "
    "blur and creamy natural bokeh with slightly busy out-of-focus "
    "backgrounds, real texture in the wool, the paper and the glaze of the "
    "mug, worn and lived-in objects with honest scuffs and marks. No plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no immaculate "
    "cleanliness, no retouched hyper-clean digital look, no perfectly smooth "
    "computer-generated gradients, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial stock "
    "photography for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — primary: deep window sill at blue hour, rooftops blurred beyond glass.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.0 on a full-frame camera from a low three-quarter angle, of a "
        "deep painted wooden window sill in a quiet upstairs room at blue "
        "hour on an autumn evening. Through the tall old window the last "
        "cold blue-violet light of dusk sits over a blur of city rooftops, "
        "chimneys and a single faint lit window far away, all soft and out "
        "of focus. On the chipped white-painted sill, in no tidy arrangement, "
        "sit a plain unmarked stoneware mug of tea with a thin curl of steam, "
        "a closed notebook with a completely plain unmarked cloth cover, and "
        "a slim closed laptop lying flat with its smooth plain pale grey lid "
        "facing up and no logo. A folded grey wool throw is bunched against "
        "the right edge of the frame, one loose thread catching the light. "
        "The room behind is almost dark, the only light coming from the "
        "window and a faint warm spill across the floorboards. Cool, quiet, "
        "lived-in, nothing staged, nothing tidy. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — tighter: mug and notebook sharp, window glass and dusk beyond.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera at sill height, of a broad stone "
        "window ledge in an old house at dusk. The sharp foreground is the "
        "cool grey stone, where a plain unmarked stoneware mug of tea sits "
        "with faint steam rising and honest crazing in the glaze, a closed "
        "notebook with a completely plain unmarked scuffed cover leans "
        "against the window frame, and a slim closed laptop lies flat with a "
        "smooth plain pale grey lid and no logo. Beyond the old glass, a "
        "softly blurred evening sky, deep blue going to violet, with the dark "
        "shapes of rooftops and television aerials out of focus. A folded "
        "grey wool blanket softens the left edge. Cold blue dusk light on the "
        "objects, a single warm lamp glow reflected faintly in the glass. "
        "Nothing staged, nothing tidy. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider: the whole room corner, window, sill and floor.
    "3": (
        "Photo-realistic editorial still-life photograph, shot on a 24mm lens "
        "at f/4 on a full-frame camera from standing height across a dim "
        "upstairs room at dusk, of a tall sash window with a deep painted "
        "sill. On the sill, a plain unmarked stoneware mug, a closed notebook "
        "with a completely plain unmarked cover, and a slim closed laptop "
        "lying flat with a smooth plain pale grey lid and no logo. A folded "
        "grey wool throw is draped over the end of the sill and a worn "
        "wooden chair back cuts into the right of the frame. The room is in "
        "cool shadow, floorboards fading into darkness, and beyond the glass "
        "a blurred blue-violet evening over dark rooftops. Flat ambient dusk "
        "light with no sun and no warm glow. "
        + COMMON
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


def load_gemini_key():
    path = "/home/chino/video_output/.gemini_key"
    if os.path.exists(path):
        with open(path) as f:
            key = f.read().strip()
            if key:
                return key
    return os.environ.get("GEMINI_API_KEY")


GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-pro-image")


def generate_gemini(prompt, out_path):
    key = load_gemini_key()
    if not key:
        print("ERROR: Gemini key not found")
        sys.exit(1)
    print(f"Generating image with Gemini {GEMINI_MODEL}...")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "imageConfig": {"aspectRatio": "16:9"},
            "responseModalities": ["IMAGE"],
        },
    }
    r = requests.post(
        url,
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=240,
    )
    r.raise_for_status()
    j = r.json()
    try:
        parts = j["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError):
        print(f"ERROR: no parts in Gemini result: {json.dumps(j)[:400]}")
        sys.exit(1)
    for p in parts:
        inline = p.get("inlineData") or p.get("inline_data")
        if inline and inline.get("data"):
            data = base64.b64decode(inline["data"])
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(data)
            img = Image.open(out_path)
            print(f"Downloaded: {out_path}  size={img.size}  bytes={len(data)}")
            return img
    print(f"ERROR: no image in Gemini result: {json.dumps(j)[:400]}")
    sys.exit(1)


def generate(prompt, out_path):
    fal_ok = True
    try:
        import fal_client  # noqa: F401
        key = load_fal_key()
        if not key:
            fal_ok = False
            print("WARN: FAL_KEY not found — skipping FAL")
    except Exception as e:  # noqa: BLE001
        fal_ok = False
        print(f"WARN: FAL unavailable ({type(e).__name__}) — skipping FAL")
    if fal_ok:
        try:
            import fal_client
            print("Generating image with fal flux/schnell...")
            result = fal_client.subscribe(
                "fal-ai/flux/schnell",
                arguments={
                    "prompt": prompt,
                    "image_size": {"width": W, "height": H},
                    "num_inference_steps": 4,
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
            if image_url:
                print(f"Image URL: {image_url}")
                r = requests.get(image_url, timeout=120)
                r.raise_for_status()
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "wb") as f:
                    f.write(r.content)
                img = Image.open(out_path)
                print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
                return img
            print(f"WARN: no image URL in FAL result: {result}")
        except Exception as e:  # noqa: BLE001
            print(f"WARN: FAL generation failed ({type(e).__name__}): {str(e)[:200]}")
    print("Falling back to Gemini image generation...")
    return generate_gemini(prompt, out_path)


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
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
