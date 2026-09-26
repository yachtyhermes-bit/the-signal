#!/usr/bin/env python3
"""Generate hero for focus-list-2026-09-26 (fal flux/schnell).

Article: The Signal weekly "Focus List" weekend long read covering four stocks
you'd read over a coffee. It is NOT about a single company, so the hero must
suit a calm weekend-reading moment rather than a company or a data center.

Scene chosen: a CALM WEEKEND-READING MOMENT INDOORS — a wooden kitchen table in
warm autumn morning daylight with a mug of coffee, an open notebook with
COMPLETELY BLANK pages, a plain unbranded pen, and a laptop angled AWAY from the
camera so its screen is only a soft featureless unreadable blurred wash. Around
them: a linen cloth, a small vase of dried flowers / a sprig of thyme, a pair of
reading glasses, a phone lying face-down. Warm striped window light rakes across
the wood.

Visual distinctness: the previous edition (focus-list-2026-09-19) used a small
round BALCONY table with coffee, notebook, pen and laptop. This one is moved
INDOORS onto a wooden kitchen table, with a linen cloth, dried flowers/thyme,
reading glasses and a face-down phone, plus hard raking window light.

Deliberately NOT: a trading floor, NOT a stock-ticker wall, NOT a data center /
server room / server aisle / cable run (banned), NOT digital art, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines / light trails, NOT
geometric patterns, NOT abstract art, NOT a chart graphic, NOT a futuristic HUD.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at any edge (tabletop scenes attract hands —
  banned).
- TEXT-FREE: a notebook, a coffee mug and a working screen are all magnets for
  lettering, so every letter, word, number, percentage, price, logo, brand name,
  watermark, UI element, icon and packaging label is explicitly forbidden. The
  notebook pages are completely blank white paper with nothing written or
  printed on them. The mug is plain unmarked ceramic. The screen is a soft,
  featureless, unreadable wash of blurred colour — no chart, no axes, no labels,
  no interface, no cursor, no icons. The phone is face-down so nothing shows.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Shipped frame: PROMPTS["8"], the prop-first variant that finally rendered the
complete brief in one frame. Vision inspection of the shipped 1920x1080 file
(Gemini 2.5 Flash): TYPE photo, TEXT no legible text, LOGO none, SERVER_ROOM no,
PEOPLE/HANDS no, elements present = coffee mug, open blank notebook, pen,
laptop turned away with a soft unreadable screen, linen cloth, small vase of
dried flowers, reading glasses and a face-down phone, in warm raking window
light on a wooden kitchen table indoors. Notes from screening: ATTEMPT 1 put a
"JETSTREAM" wordmark on the mug (rejected); ATTEMPT 2/3 and most ATTEMPT 4/5/6
runs dropped the laptop (ATTEMPTS 4-5 keep the laptop but lose the small props,
ATTEMPT 6 wins the props but loses the laptop); several 4/5/8 runs put a
recognisable Apple logo on the laptop bezel (rejected). ATTEMPT 8 with the props
named first was the winner.

Usage: cd /home/chino/thesignal && ATTEMPT=8 \
  /home/chino/video-venv/bin/python3 scripts/gen-focus-list-2026-09-26-hero-20260926.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "focus-list-2026-09-26")
# ATTEMPT 8 is the frame that shipped (see docstring).
ATTEMPT = os.environ.get("ATTEMPT", "8")
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
    "printing, no newspaper, no magazine, no headlines, no book spines, no "
    "handwriting, no print, no legible writing or drawn marks of any kind "
    "anywhere in the image. The open notebook pages are pure blank white "
    "paper, completely empty and unwritten, showing nothing but paper and "
    "soft shadow. The coffee mug is a plain unmarked ceramic mug with no "
    "design, no logo and no text. The laptop screen is angled away from the "
    "camera, out of focus, and shows only a soft, featureless, blurred wash "
    "with nothing readable on it, no interface, no icons, no chart, no "
    "numbers, no cursor. The phone lies face-down on the table so its screen "
    "is completely hidden from view. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game still, no concept art, no "
    "matte painting, no neon, no synthwave colour, no glowing lines, no "
    "light trails, no abstract geometric art, no floating holographic "
    "elements, no wireframe, no dashboard, no data visualisation, no data "
    "center, no server room, no server racks, no server aisle, no cable "
    "run, no GPU racks, no robots."
)

COMMON = (
    "This is a quiet observational editorial still life, not a staged "
    "commercial product shot and not a hero render: the objects sit loosely "
    "off-centre, the framing is relaxed and a little careless, and foreground "
    "elements cut into the edges of the frame. Honest available-light "
    "exposure, not a lit set and not an HDR composite. Shallow depth of field "
    "from a wide aperture on a 50mm lens on a full-frame camera, real optical "
    "lens blur and creamy natural bokeh, unobtrusive film-like grain visible "
    "in the smooth mid-tones and shadows, a subtle lens vignette, slight "
    "sensor softness in the shadows, real texture in the wood grain and the "
    "fabric weave, worn and lived-in objects with honest scuffs and marks, "
    "asymmetric unidealised composition, a slight hand-held tilt, natural "
    "slight over-exposure where the sunlight lands, no plastic CGI sheen, no "
    "glossy render, no perfect symmetry, no immaculate cleanliness, no "
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial stock "
    "photography for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — the primary frame: wooden kitchen table, raking striped window light,
    #     mug of coffee, blank notebook, pen, laptop angled away, linen cloth,
    #     dried flowers, reading glasses, face-down phone.
    "1": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/1.8 on a full-frame camera from just above table height, of a "
        "quiet weekend-morning reading moment on a solid old wooden kitchen "
        "table indoors. Warm low autumn morning sunlight pours through a "
        "nearby window, casting long hard diagonal stripes of light and "
        "shadow across the grain of the wood and raking across the objects, "
        "so the tabletop is half brilliant warm gold and half soft deep "
        "shadow. The table is bare, worn oak with visible grain, a few light "
        "scratches and a faint ring mark, and a rumpled natural linen cloth "
        "is draped loosely across the left third of the frame, its weave "
        "clearly visible, edged with a soft shadow. Sharp and slightly "
        "off-centre to the right sits a plain unmarked stoneware ceramic mug "
        "of black coffee with a thin curl of steam rising into the light. "
        "To the left of it an open paper notebook lies flat on the wood with "
        "its pages completely blank, pure empty white paper catching the "
        "sunlight, its spine soft and slightly worn, and a plain simple pen "
        "with no branding lies diagonally across the open pages. A slim "
        "closed laptop sits behind and to the right of the notebook, angled "
        "away from the camera so only its pale back edge and a soft out-of-"
        "focus sliver of its screen are visible, the screen a completely "
        "unreadable featureless blurred wash. A small low glass vase holding "
        "a few dried flowers and a sprig of thyme stands at the back right "
        "of the frame, softly out of focus. A pair of thin metal reading "
        "glasses rests folded on the linen cloth, catching a tiny highlight "
        "of sun. A plain smartphone lies face-down on the bare wood at the "
        "front right, its dark screen completely hidden against the table. "
        "The background is a softly blurred kitchen interior: a warm plaster "
        "wall, the blurred edge of a window frame with a hint of autumn "
        "foliage outside, all in creamy shallow-focus bokeh. Nothing in the "
        "scene carries any writing of any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — closer, tighter crop on the notebook and mug with strong raking
    #     window-light stripes across the wood; laptop and vase pushed into
    #     the far bokeh, glasses in the foreground.
    "2": (
        "Photo-realistic editorial still-life photograph, shot on an 85mm "
        "lens at f/2 on a full-frame camera from slightly above and to the "
        "side, of an intimate weekend-reading scene on an old wooden kitchen "
        "table indoors. Hard, warm, low morning autumn sunlight slices "
        "through a window off to the left, throwing three or four crisp "
        "diagonal bands of brilliant golden light and deep shadow across the "
        "bare oak tabletop, lighting the exposed wood grain, its scratches "
        "and old water rings. In the sharp centre of the frame an open paper "
        "notebook lies flat, its pages completely blank and empty white, "
        "bright where the sun crosses it and falling into soft shadow at the "
        "edges, with a plain unbranded pen resting diagonally across the "
        "open spread. Just behind and right of the notebook, tack sharp, is "
        "a plain unmarked ceramic mug of coffee, dark surface, a thin wisp "
        "of steam in the light. A rumpled natural linen cloth is bunched to "
        "the left, its woven texture and a frayed edge catching the "
        "low sun. A pair of folded reading glasses rests in the near "
        "foreground, out of focus, their thin rims glinting. Beyond them the "
        "frame falls away into soft bokeh: the pale back of a slim laptop "
        "angled away from the camera so its screen shows only an unreadable "
        "featureless blurred wash, and a small glass vase of dried flowers "
        "and a sprig of thyme. A phone lies face-down on the wood in the "
        "lower right, screen hidden. The blurred background is a warm quiet "
        "kitchen: plaster wall, the indistinct bright edge of a window. "
        "Nothing in the scene carries any writing of any kind. No readable "
        "text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider room-context frame: the whole corner of the kitchen table seen
    #     from a little further back and higher, showing the full arrangement
    #     and a bigger pool of raking window light on the wood.
    "3": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera from standing eye-level looking "
        "down at an angle, of the corner of a wooden kitchen table indoors "
        "on a calm weekend morning. A wide low shaft of warm autumn sunlight "
        "comes in from a window on the left and falls in long hard-edged "
        "stripes of gold and shadow across the bare oak tabletop and the "
        "objects on it, with fine dust motes floating in the beam. Laid out "
        "loosely across the wood: a plain unmarked stoneware mug of black "
        "coffee with a faint plume of steam; an open paper notebook with "
        "completely blank pure white pages, a plain unbranded pen lying "
        "diagonally across them; a rumpled natural linen cloth folded and "
        "draped near the left edge, its weave in sharp relief in the "
        "raking light; a small glass vase of dried flowers and a sprig of "
        "thyme set back on the right, softly out of focus; a pair of thin "
        "metal reading glasses lying folded on the wood; and a plain "
        "smartphone resting face-down so its screen is entirely hidden. At "
        "the right of the frame, clearly visible behind the mug, an open "
        "slim laptop sits turned sharply away from the camera so only its "
        "pale back and a narrow sliver of the screen are in view, the screen "
        "a soft completely unreadable featureless blurred grey wash with "
        "nothing on it, no interface, no text. The wood grain, the linen "
        "weave, the ceramic and the dry "
        "petals all show honest real texture. The background is the softly "
        "blurred rest of a warm quiet kitchen: plaster wall, a blurred window "
        "with a hint of autumn trees outside, indistinct and out of focus in "
        "creamy bokeh. Nothing in the scene carries any writing of any kind. "
        "No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — laptop-forward: an open laptop turned fully away from the camera so
    #     its plain pale back dominates, with the notebook, mug, cloth, vase,
    #     glasses and face-down phone arranged around it on the sunlit wood.
    "4": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera from just above table height, of a "
        "calm weekend-morning reading moment on an old wooden kitchen table "
        "indoors. Warm low autumn morning sunlight comes through a window on "
        "the left and falls in long hard-edged diagonal stripes of gold and "
        "shadow across the bare oak tabletop, lighting the wood grain and "
        "fine dust motes drifting in the beam. Standing on the table and "
        "clearly the largest object in the frame is an open slim laptop "
        "computer, turned completely away from the camera so the viewer sees "
        "only its plain, smooth, pale grey aluminium back panel and the thin "
        "dark line of the hinge; the keyboard and the screen face away and "
        "are not visible, the back panel completely plain with no printing, "
        "no logo, no emblem, no sticker. Around and in front of it, laid out "
        "loosely on the sunlit wood: a plain unmarked stoneware ceramic mug "
        "of black coffee with a faint plume of steam; an open paper notebook "
        "with completely blank pure white unwritten pages, a plain unbranded "
        "pen lying diagonally across them; a rumpled natural linen cloth "
        "draped near the left edge, its weave in sharp relief in the raking "
        "light; a small glass vase holding dried flowers and a sprig of "
        "thyme set back on the right, softly out of focus; a pair of thin "
        "metal reading glasses lying folded on the wood; and a plain "
        "smartphone resting completely face-down so its screen is hidden. "
        "The wood grain, the linen weave, the ceramic and the dry petals all "
        "show honest real texture. The background is the softly blurred rest "
        "of a warm quiet kitchen: plaster wall, a blurred bright window with "
        "a hint of autumn foliage, out of focus in creamy bokeh. Nothing in "
        "the scene carries any writing of any kind. No readable text "
        "anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 5 — laptop at the right edge, half-open and angled away, its screen a
    #     soft unreadable wash; the reading scene (notebook, mug, cloth, vase,
    #     glasses, face-down phone) square in the frame on sunlit wood.
    "5": (
        "Photo-realistic editorial still-life photograph, shot on a 50mm lens "
        "at f/2 on a full-frame camera at a gentle downward angle, of a calm "
        "weekend-morning reading moment on an old wooden kitchen table "
        "indoors. Warm low autumn morning sunlight streams in from a window "
        "on the left, cutting long hard diagonal stripes of brilliant gold "
        "and deep shadow across the bare oak tabletop. At the right edge of "
        "the frame a slim open laptop stands on the table angled away from "
        "the camera at three-quarters, so its pale plain back and the top "
        "corner of its tilted screen are the only parts in view; the screen "
        "shows only a soft, featureless, completely unreadable blurred grey "
        "wash with nothing on it, no interface, no window, no icons, and the "
        "back is plain with no printing, no logo and no emblem. Square in "
        "the middle of the frame on the sunlit wood: an open paper notebook "
        "with completely blank pure white unwritten pages and a plain "
        "unbranded pen lying diagonally across them; a plain unmarked "
        "stoneware mug of black coffee with a thin curl of steam beside it; "
        "a rumpled natural linen cloth draped across the left of the table, "
        "its weave crisp in the light; a small glass vase of dried flowers "
        "and a sprig of thyme set back and softly out of focus; a pair of "
        "thin metal reading glasses folded on the wood; and a plain "
        "smartphone lying completely face-down so its screen is hidden. The "
        "background is the softly blurred rest of a warm quiet kitchen: "
        "plaster wall and the indistinct bright edge of a window, in creamy "
        "shallow-focus bokeh. Nothing in the scene carries any writing of "
        "any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 6 — every brief prop given its own explicit placement: reading glasses
    #     resting on the blank notebook, a phone face-down beside the mug, the
    #     mug standing on the linen cloth, dried flowers/thyme in a small vase,
    #     and the laptop turned away at the right — all in raking window light.
    "6": (
        "Photo-realistic editorial still-life photograph, shot on a 40mm lens "
        "at f/2.8 on a full-frame camera at eye level just above a wooden "
        "kitchen table indoors on a calm weekend morning. Warm low autumn "
        "sunlight comes through a window on the left and falls in long hard-"
        "edged diagonal stripes of gold and shadow across the bare oak "
        "tabletop, lighting the wood grain. In the middle of the frame an "
        "open paper notebook lies flat with completely blank pure white "
        "unwritten pages, and a pair of thin metal reading glasses rests "
        "folded on top of the open pages. A plain unmarked stoneware mug of "
        "black coffee with a faint wisp of steam stands on a rumpled natural "
        "linen cloth just to the left of the notebook, the cloth's woven "
        "texture and frayed edge crisp in the raking light. A plain "
        "smartphone lies completely face-down on the bare wood just in front "
        "of the mug, its dark screen hidden against the table. A plain "
        "unbranded pen lies diagonally "
        "across the notebook pages. Set back on the right of the frame, a "
        "small glass vase holds a few dried flowers and a sprig of thyme, "
        "softly out of focus. Behind it at the right edge an open slim "
        "laptop stands turned completely away from the camera so only its "
        "plain pale grey back is in view and its screen is not visible at "
        "all, the back plain with no printing, no logo, no emblem. The "
        "background is the softly blurred rest of a warm quiet kitchen: "
        "plaster wall and the indistinct bright edge of a window, out of "
        "focus in creamy bokeh. Nothing in the scene carries any writing of "
        "any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 7 — the full brief at once: the laptop stands large and turned away in
    #     the middle-background, with the glasses on the blank notebook, the
    #     mug on the linen cloth, a face-down phone, a pen and a vase of dried
    #     flowers/thyme in front of it, all in raking striped window light.
    "7": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera at eye level just above a wooden "
        "kitchen table indoors on a calm weekend morning. Warm low autumn "
        "sunlight comes through a window on the left and falls in long hard-"
        "edged diagonal stripes of gold and shadow across the bare oak "
        "tabletop, lighting the wood grain and the dust in the air. Standing "
        "upright in the middle-background of the table, large and clearly "
        "the main object, is an open slim laptop computer turned completely "
        "away from the camera: the viewer sees only its smooth plain pale "
        "grey back panel, the hinge edge and two thin black feet, while its "
        "keyboard and screen face away toward the window and are not visible "
        "at all. The back panel is completely plain with no printing, no "
        "logo, no emblem, no sticker, no reflection of any text. In front of "
        "the laptop on the sunlit wood: an open paper notebook with "
        "completely blank pure white unwritten pages, with a pair of thin "
        "metal reading glasses resting folded on top of the open pages and a "
        "plain unbranded pen lying diagonally across the paper; a plain "
        "unmarked stoneware mug of black coffee with a faint wisp of steam "
        "standing on a rumpled natural linen cloth to the left, the cloth's "
        "woven texture and frayed edge crisp in the raking light; a plain "
        "smartphone lying completely face-down on the bare wood in front of "
        "the mug with its dark screen hidden against the table; and a small "
        "glass vase holding a few dried flowers and a sprig of thyme set to "
        "the right, softly out of focus. The background is the softly "
        "blurred rest of a warm quiet kitchen: plaster wall and the "
        "indistinct bright edge of a window, out of focus in creamy bokeh. "
        "Nothing in the scene carries any writing of any kind. No readable "
        "text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 8 — prop-first ordering: the linen cloth, vase of dried flowers and
    #     face-down phone are named first so they survive, then the mug on the
    #     cloth, the blank notebook with glasses and pen, and the turned-away
    #     laptop at the right.
    "8": (
        "Photo-realistic editorial still-life photograph, shot on a 35mm lens "
        "at f/2.8 on a full-frame camera at eye level just above a wooden "
        "kitchen table indoors on a calm weekend morning, warm low autumn "
        "sunlight cutting hard diagonal stripes of gold and shadow across the "
        "bare oak tabletop. On the sunlit table there is a rumpled natural "
        "linen cloth with a visible woven texture and a frayed edge, and a "
        "small glass vase of dried flowers with a sprig of thyme beside it; a "
        "plain smartphone lies face-down on the bare wood with its screen "
        "hidden. A plain unmarked stoneware mug of black coffee with a faint "
        "wisp of steam stands on the linen cloth. Next to it an open paper "
        "notebook lies flat with completely blank pure white unwritten pages, "
        "a pair of thin metal reading glasses folded on top of the pages and "
        "a plain unbranded pen lying diagonally across the paper. Behind "
        "these, at the right of the frame and clearly visible, an open slim "
        "laptop stands turned completely away from the camera so only its "
        "smooth plain pale grey back panel and the hinge line are in view, "
        "its screen facing away and not visible at all, the back completely "
        "plain with no printing, no logo, no emblem, no sticker. The "
        "background is the softly blurred rest of a warm quiet kitchen: "
        "plaster wall and the indistinct bright edge of a window, out of "
        "focus in creamy bokeh. Nothing in the scene carries any writing of "
        "any kind. No readable text anywhere. "
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


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
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
    if not image_url:
        print(f"ERROR: Could not find image URL in result: {result}")
        sys.exit(1)
    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
    return img


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
