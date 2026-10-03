#!/usr/bin/env python3
"""Generate hero for focus-list-2026-10-03 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read covering four stocks
you'd read over a coffee. It is NOT about a single company, so the hero must
suit a calm weekend-reading moment rather than a company or a data center.

Scene chosen: a SMALL WOODEN DESK SET AGAINST A TALL BRIGHT WINDOW in a quiet
apartment, in warm late-afternoon autumn light. On the desk: a plain unmarked
ceramic mug of coffee, an open notebook with COMPLETELY BLANK pages and a plain
unbranded pen, a small stack of two closed hardback books with plain unmarked
spines, a slim laptop turned AWAY from the camera so only its plain back edge
and a soft unreadable blurred screen sliver show, and a small potted houseplant
in the out-of-focus background. Warm hard late-afternoon light falls in stripes
across the desk. Honest available-light photography.

Visual distinctness (the last three editions all used a tabletop with
coffee+notebook+pen+laptop, so this scene is deliberately different):
- 2026-09-26: indoor wooden KITCHEN table with a linen cloth, dried flowers /
  thyme, reading glasses and a face-down phone.
- 2026-09-19: a small round BALCONY table.
- 2026-09-16: a plain kitchen table.
This edition: a small wooden DESK pressed against a TALL BRIGHT WINDOW in a
quiet apartment, late-afternoon autumn light, with a stack of two closed plain
hardback books and a small potted houseplant in the blurred background.
Deliberately NO linen cloth, NO dried flowers/vase, NO reading glasses, NO
phone, NO newspaper and NO magazine (these are dropped so the frame reads as a
different room and so no text-bearing props are present).

Deliberately NOT: a trading floor, NOT a stock-ticker wall, NOT a data center /
server room / server aisle / cable run (banned), NOT digital art, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines / light trails, NOT
geometric patterns, NOT abstract art, NOT a chart graphic, NOT a futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at any edge.
- TEXT-FREE: a notebook, a coffee mug, book spines and a working screen are all
  magnets for lettering, so every letter, word, number, percentage, price, logo,
  brand name, watermark, UI element, icon and packaging label is explicitly
  forbidden. The notebook pages are completely blank white paper with nothing
  written or printed on them. The mug is plain unmarked ceramic. The two books
  are closed with completely plain unmarked spines and covers, no title, no
  author, no publisher mark. The laptop is turned AWAY so its back panel (plain,
  with no logo — Apple logos have leaked in before and must be rejected) faces
  the camera and its screen shows only a soft, featureless, unreadable blur, no
  chart, no axes, no UI, no numbers.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Generator note (2026-10-03): the usual FAL flux/schnell generator is LOCKED on
this box — both FAL keys ("User is locked. Reason: Exhausted balance.") return
HTTP 403, exactly as the previous day's onsemi hero documented. This script
therefore tries FAL flux/schnell first (as the proven template did) and, on
failure, falls back to the Google Gemini image model gemini-3-pro-image via the
key at /home/chino/video_output/.gemini_key (verified working 2026-10-03).
Everything downstream (16:9 center-crop, 1920x1080, JPEG q92 re-save, backup
mirror) is unchanged from the proven template.

Usage: cd /home/chino/thesignal && ATTEMPT=<n> \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-10-03-hero-20261003.py
"""
import base64
import json
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-10-03")
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
    "open notebook pages are pure blank white paper, completely empty and "
    "unwritten, showing nothing but paper and soft shadow. The coffee mug is "
    "a plain unmarked ceramic mug with no design, no logo and no text. The "
    "two closed hardback books have completely plain unmarked covers and "
    "spines with no title, no author and no publisher mark. The laptop is "
    "turned away from the camera with its smooth plain back panel facing the "
    "viewer, and the back panel carries no logo, no apple, no emblem, no "
    "sticker, no printing; the sliver of screen that shows is a soft, "
    "featureless, unreadable blurred wash with nothing on it, no interface, "
    "no icons, no chart, no numbers, no cursor. No phone anywhere, no "
    "smartphone anywhere. No illustration, no digital art, no cartoon, no 3D "
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
    "a few tiny specks on the desk, real-world clutter and small flaws, "
    "slightly uneven white balance drifting warm-to-cool across the frame, "
    "the highlights on the window clipping softly to pure white, the shadows "
    "lifting with true noise rather than being perfectly clean, a natural "
    "asymmetric hand-held tilt, and a slightly imperfect, unretouched "
    "documentary snapshot feel. Honest available-light exposure, not a lit "
    "set and not an HDR composite. Shallow depth of field from a wide "
    "aperture on a 50mm lens on a full-frame camera, real optical lens blur "
    "and creamy natural bokeh with slightly busy out-of-focus backgrounds, "
    "real texture in the wood grain and the paper, worn and lived-in objects "
    "with honest scuffs, dust and marks, natural slight over-exposure where "
    "the sunlight lands, some faint smudges on the mug and glass. No plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no immaculate "
    "cleanliness, no retouched hyper-clean digital look, no perfectly smooth "
    "computer-generated gradients, no patterned digital steam, no 3D "
    "visualisation, no digital illustration, no concept-art lighting, no "
    "video-game aesthetic, photorealistic, very high detail, professional "
    "editorial stock photography for a business newspaper, 16:9 landscape "
    "composition."
)

PROMPTS = {
    # 1 — the primary frame: small wooden desk against a tall bright window,
    #     warm late-afternoon striped autumn light, blank notebook + pen, mug,
    #     two plain closed hardbacks, laptop turned away, potted houseplant.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera from just above desk height, of a "
        "calm weekend-reading moment at a small wooden desk set against a "
        "tall bright window in a quiet apartment, in warm late-afternoon "
        "autumn light. Low golden late-afternoon sunlight comes through the "
        "tall window and falls in long hard stripes of warm light and soft "
        "shadow across the bare wood of the small desk and across the objects "
        "on it, with fine dust motes drifting in the beams. The desk is a "
        "narrow worn wooden plank-top desk pushed right up against the tall "
        "window frame, its surface honest and lived-in with faint marks and a "
        "soft sheen of daylight. Centred slightly right sits a plain unmarked "
        "stoneware ceramic mug of black coffee, a thin curl of steam rising "
        "into the light. To its left an open paper notebook lies flat on the "
        "desk with its pages completely blank, pure empty white paper "
        "catching the sun, and a plain simple unbranded pen lies diagonally "
        "across the open pages. At the back right of the desk stands a small "
        "stack of two closed hardback books with completely plain unmarked "
        "covers and spines, no title, no author, no printing, slightly "
        "soft in focus. A slim laptop rests closed on the desk turned "
        "completely away from the camera so only its smooth plain back edge "
        "and a soft out-of-focus sliver of its screen are visible, the screen "
        "and its back panel entirely plain with no logo. In the out-of-focus "
        "background a small potted green houseplant in a plain unmarked pot "
        "stands on the windowsill, its leaves soft and blurred against the "
        "bright window. Nothing in the scene carries any writing of any "
        "kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — tighter: desk corner in the foreground, tall window filling the back
    #     with blown-out bright daylight, hard striped light on the notebook.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on an 85mm "
        "lens at f/2 on a full-frame camera from slightly above and to the "
        "side, of an intimate weekend-reading desk in a quiet apartment. A "
        "small wooden desk corner fills the lower frame, pushed against a "
        "tall bright window that fills the background with soft blown-out "
        "daylight; warm hard late-afternoon autumn sun slants through the "
        "glass and lays three or four crisp diagonal stripes of gold and "
        "shadow across the worn plank top. In the sharp centre an open paper "
        "notebook lies flat, its pages completely blank and empty white, with "
        "a plain unbranded pen resting diagonally on the open spread. Just "
        "behind it, tack sharp, a plain unmarked ceramic mug of coffee, dark "
        "surface, a thin wisp of steam in the light. To the right, a small "
        "stack of two closed hardback books with completely plain unmarked "
        "spines rests on the wood. Beyond them a slim laptop sits turned away, "
        "its plain back edge toward the camera and only a soft unreadable "
        "featureless blurred sliver of screen showing, no logo anywhere. A "
        "small potted houseplant stands blurred in the far background against "
        "the bright window. Nothing in the scene carries any writing of any "
        "kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider room-context: the whole small desk and the tall window seen a
    #     little further back and higher, stripes of light on the floor and desk.
    "3": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera from standing eye level looking down "
        "at an angle, of the corner of a quiet apartment where a small wooden "
        "desk stands against a tall bright window on a calm late afternoon in "
        "autumn. A wide shaft of warm late-afternoon sun comes through the "
        "tall window and falls in long hard-edged stripes of gold and shadow "
        "across the desk top and onto the floorboards, with fine dust motes "
        "in the beam. Laid out loosely across the wood: a plain unmarked "
        "stoneware mug of black coffee with a faint plume of steam; an open "
        "paper notebook with completely blank pure white pages and a plain "
        "unbranded pen lying diagonally across them; a small stack of two "
        "closed hardback books with completely plain unmarked covers and "
        "spines set back on the right, softly out of focus; and a slim laptop "
        "turned sharply away from the camera so only its plain pale back edge "
        "and a narrow sliver of its screen are in view, the screen a soft "
        "completely unreadable featureless blurred wash with nothing on it, "
        "no interface, no text, and the back plain with no logo. A small "
        "potted green houseplant stands blurred in the background on the "
        "windowsill against the bright glass. The wood grain, the paper, the "
        "ceramic and the plant leaves all show honest real texture. Nothing "
        "in the scene carries any writing of any kind. No readable text "
        "anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — laptop-forward: the laptop dominates, turned fully away so its plain
    #     pale back panel faces the camera, with the reading props around it.
    "4": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera from just above desk height, of a "
        "calm weekend-reading moment at a small wooden desk against a tall "
        "bright window in a quiet apartment. Warm low late-afternoon autumn "
        "sunlight comes through the tall window and falls in long hard-edged "
        "diagonal stripes of gold and shadow across the bare wooden desk top, "
        "lighting the wood grain and dust motes in the beam. Standing on the "
        "desk and clearly the largest object in the frame is a slim laptop "
        "computer turned completely away from the camera so the viewer sees "
        "only its plain, smooth, pale grey back panel and the thin dark line "
        "of the hinge; the keyboard and the screen face away and almost all of "
        "them are hidden, only a soft out-of-focus unreadable sliver of screen "
        "showing, the back panel completely plain with no printing, no logo, "
        "no apple, no emblem, no sticker. Around and in front of it, laid out "
        "loosely on the sunlit wood: a plain unmarked stoneware ceramic mug of "
        "black coffee with a faint plume of steam; an open paper notebook with "
        "completely blank pure white unwritten pages and a plain unbranded pen "
        "lying diagonally across them; and a small stack of two closed "
        "hardback books with completely plain unmarked spines, softly out of "
        "focus. A small potted green houseplant stands blurred in the "
        "background against the bright tall window. The wood grain, the paper, "
        "the ceramic and the leaves all show honest real texture. Nothing in "
        "the scene carries any writing of any kind. No readable text "
        "anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 5 — the two books are the anchor prop, stacked on the desk with the mug
    #     resting beside them under the tall window and hard striped light.
    "5": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/2 on a full-frame camera at a gentle downward angle, of a calm "
        "weekend-reading desk in a quiet apartment against a tall bright "
        "window. Warm low late-afternoon autumn sunlight streams in through "
        "the tall window and cuts long hard diagonal stripes of brilliant gold "
        "and deep shadow across the worn wooden desk top. In the middle of the "
        "frame a small stack of two closed hardback books rests on the wood, "
        "their covers and spines completely plain and unmarked, no title, no "
        "author, no printing, one book sitting slightly askew on the other. "
        "Beside the books a plain unmarked stoneware mug of black coffee with "
        "a thin curl of steam. To the left an open paper notebook lies with "
        "completely blank pure white unwritten pages and a plain unbranded pen "
        "lying diagonally across them. At the right edge of the frame a slim "
        "laptop stands turned away from the camera at three-quarters, its "
        "plain pale back edge toward the viewer and only the top corner sliver "
        "of its screen in view, the screen a soft, featureless, completely "
        "unreadable blurred grey wash with nothing on it, no interface, no "
        "window, no icons, and the back plain with no logo. A small potted "
        "green houseplant stands blurred in the background on the "
        "windowsill against the bright glass. Nothing in the scene carries "
        "any writing of any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 6 — plant-first prop ordering so the houseplant survives, then the mug,
    #     the blank notebook with pen, the plain closed books, the turned-away
    #     laptop — all under the tall bright window in raking stripes.
    "6": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera at eye level just above a small "
        "wooden desk in a quiet apartment pressed against a tall bright "
        "window, warm low late-afternoon autumn sunlight cutting hard "
        "diagonal stripes of gold and shadow across the bare wooden desk top. "
        "In the softly out-of-focus background a small potted green houseplant "
        "in a plain unmarked pot stands on the windowsill against the bright "
        "tall window. On the sunlit desk there is a plain unmarked stoneware "
        "mug of black coffee with a faint wisp of steam; an open paper "
        "notebook lying flat with completely blank pure white unwritten pages "
        "and a plain unbranded pen lying diagonally across the paper; and a "
        "small stack of two closed hardback books with completely plain "
        "unmarked covers and spines, no title, no author, no printing. Behind "
        "these, at the right of the frame and clearly visible, a slim laptop "
        "stands turned completely away from the camera so only its smooth "
        "plain pale grey back panel and the hinge line are in view, its screen "
        "facing away and almost all hidden with only a soft unreadable "
        "featureless blurred sliver showing, the back completely plain with no "
        "printing, no logo, no apple, no emblem, no sticker. Nothing in the "
        "scene carries any writing of any kind. No readable text anywhere. "
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
    """Try the proven FAL flux/schnell path first; fall back to Gemini.
    Both FAL keys are locked (HTTP 403) on this box as of 2026-10-03."""
    fal_ok = True
    try:
        import fal_client
        key = load_fal_key()
        if not key:
            fal_ok = False
            print("WARN: FAL_KEY not found — skipping FAL")
    except Exception as e:  # noqa: BLE001
        fal_ok = False
        print(f"WARN: FAL unavailable ({type(e).__name__}) — skipping FAL")
    if fal_ok:
        try:
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
    target_ratio = FINAL_W / FINAL_H  # 16/9
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
