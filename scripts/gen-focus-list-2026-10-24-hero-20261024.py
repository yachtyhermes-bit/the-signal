#!/usr/bin/env python3
"""Generate hero for focus-list-2026-10-24 (fal flux/schnell, Gemini fallback).

Article: The Signal weekly "Focus List" weekend long read — four stocks read over
a weekend, not a single company story. The hero must suit a calm reading moment
rather than a company, a data center or a trading floor.

Scene chosen for THIS edition: a RAINY-DAY WINDOW SEAT IN A QUIET HOUSE, cool
grey-blue overcast light. A deep cushioned bench under a tall rain-streaked
window, a folded wool throw, a plain unmarked ceramic mug on the sill, a closed
plain notebook, and a closed laptop lying flat with its smooth plain lid up.
Cool, soft, diffuse daylight — deliberately NOT warm.

Visual distinctness (every recent edition used a tabletop in warm daylight):
- 2026-10-10: bright MORNING kitchen table, warm soft daylight, mug + blank
          notebook + pen + laptop turned away.
- 2026-10-03: small wooden DESK against a tall bright window, late-afternoon
          autumn striped light, two plain hardbacks, potted houseplant.
- 2026-09-26: indoor wooden KITCHEN table with a linen cloth, dried flowers,
          reading glasses and a face-down phone.
- 2026-09-19: a small round BALCONY table.
This edition: NO table at all. A window SEAT with a rain-streaked pane, cool
overcast grey-blue light, a folded wool throw. No warm sunlight, no pen, no
hardbacks, no houseplant, no phone, no newspaper, no magazine.

Deliberately NOT: a trading floor, NOT a stock-ticker wall, NOT a data center /
server room / server aisle / cable run (banned), NOT digital art, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines / light trails, NOT
geometric patterns, NOT abstract art, NOT a legible chart graphic, NOT a
futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at any edge.
- TEXT-FREE: every letter, word, number, percentage, price, logo, brand name,
  watermark, UI element, icon and packaging label is forbidden. Notebook pages
  blank. Mug plain. Laptop lid plain with no logo.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Usage: cd /home/chino/thesignal && ATTEMPT=<n> \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-10-17-hero-20261017.py
"""
import base64
import json
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-10-24")
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
    "percentages, no currency symbols, no dollar signs, no ticker symbols, "
    "no charts with axis labels, no readable graph, no brand names, no "
    "company names, no logos, no trademarks, no watermarks, no signatures, "
    "no barcodes, no QR codes, no packaging labels, no stickers, no mug "
    "printing, no newspaper, no magazine, no headlines, no book titles, no "
    "book-spine text, no printed book covers, no handwriting, no print, no "
    "legible writing or drawn marks of any kind anywhere in the image. The "
    "closed notebook has a completely plain unmarked cover with no title and "
    "no printing of any kind. The coffee mug is a plain unmarked ceramic mug "
    "with no design, no logo and no text. The closed laptop lid is a smooth "
    "plain pale grey panel with no logo, no apple, no emblem, no sticker, no "
    "writing. No phone anywhere, no smartphone anywhere, no tablet screen "
    "showing anything. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no video-game still, no concept art, no matte painting, "
    "no neon, no synthwave colour, no glowing lines, no light trails, no "
    "abstract geometric art, no floating holographic elements, no wireframe, "
    "no dashboard, no data visualisation, no data center, no server room, no "
    "server racks, no server aisle, no cable run, no GPU racks, no robots."
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
    "slightly uneven white balance, the bright window clipping softly to pure "
    "white, the shadows lifting with true noise rather than being perfectly "
    "clean, a natural asymmetric hand-held tilt, and a slightly imperfect, "
    "unretouched documentary snapshot feel. Honest available-light exposure, "
    "not a lit set and not an HDR composite. Shallow depth of field from a "
    "wide aperture on a 35mm lens on a full-frame camera, real optical lens "
    "blur and creamy natural bokeh with slightly busy out-of-focus "
    "backgrounds, real texture in the wool, the cotton cushion, the paper and "
    "the glaze of the mug, worn and lived-in objects with honest scuffs and "
    "marks. No plastic CGI sheen, no glossy render, no perfect symmetry, no "
    "immaculate cleanliness, no retouched hyper-clean digital look, no "
    "perfectly smooth computer-generated gradients, no 3D visualisation, no "
    "digital illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial stock "
    "photography for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — primary: a plain covered front PORCH at first light in autumn.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera from a low three-quarter angle, of a "
        "quiet covered wooden porch at first light on an ordinary autumn "
        "morning. A weathered painted wooden bench runs along a clapboard "
        "wall under the porch roof, its paint chalky and worn through at the "
        "edges. On the bench sits a plain unmarked stoneware mug of coffee "
        "with a thin curl of steam, a closed notebook with a completely plain "
        "unmarked cover, a slim closed laptop lying flat with its smooth "
        "plain pale grey lid facing up and no logo, and a folded woollen "
        "blanket in muted rust brown. Two dry fallen leaves rest on the "
        "boards. Low cool morning daylight rakes in from the left across the "
        "floorboards, long soft shadows, a blurred garden and bare branches "
        "far behind in shallow focus. Early autumn, ordinary, lived-in, "
        "nothing staged. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — tighter on the bench, mug the anchor, porch boards in the foreground.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera at bench height, of a bare wooden "
        "porch early on an autumn morning. The sharp foreground is a worn "
        "painted plank bench, where a plain unmarked stoneware mug of coffee "
        "sits on a small wooden offcut, faint steam rising into the cool "
        "air, the glaze showing honest crazing and one small chip at the "
        "rim. Behind it, leaning against the clapboard wall, a closed "
        "notebook with a completely plain unmarked slightly scuffed cover "
        "and a slim closed laptop lying flat with its smooth plain pale grey "
        "lid up and no logo. A folded rust-brown woollen blanket softens the "
        "right edge of the frame, one loose thread visible. Cool morning "
        "light, dappled and soft through the porch posts, a blurred leafless "
        "tree beyond. Nothing staged, nothing tidy. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider: the whole porch, the step and the path beyond.
    "3": (
        "Photo-realistic editorial still-life photograph, shot on a 24mm lens "
        "at f/4 on a full-frame camera from standing height a few steps away, "
        "of a plain farmhouse front porch on an overcast autumn morning. A "
        "chalky painted wooden bench sits against the clapboard wall beneath "
        "the porch roof, a folded rust-brown woollen blanket draped over one "
        "end, a plain unmarked stoneware mug of coffee on the seat, a closed "
        "notebook with a completely plain unmarked cover beside it, and a "
        "slim closed laptop lying flat with its smooth plain pale grey lid up "
        "and no logo. Dry leaves are scattered across the boards and the top "
        "step. The porch posts frame a soft blurred path and a leafless "
        "tree, all grey-green and quiet, flat diffuse daylight with no sun "
        "and no warm glow. "
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
    """Fallback generator: Google Gemini image model (image is returned inline)."""
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
    """Try FAL flux/schnell first; fall back to Gemini on failure/lock."""
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
    """Center-crop to 16:9, then resize to 1920x1080."""
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
