#!/usr/bin/env python3
"""Generate hero for etf-review-shld-2026-09-30 (fal flux/schnell).

Article: "The ETF Review: SHLD — Global X Defense Tech ETF" — a passive,
rules-based fund that buys defence-technology companies. So the picture must
read as a sober editorial / financial still life, NOT as a defence-contractor
advert: nothing military, no insignia, no hardware, no flags, no camouflage.

Scene chosen (deliberately different from the recent heroes):
A low, three-quarter, eye-level desk still life on a dark oak desk in soft
natural window light from one side — a small plain matte olive-green canvas
drawstring pouch, a simple unbranded matte brass ruler, and a short roll of
completely blank unmarked paper standing beside them. Shallow depth of field,
honest available-light exposure, real lens blur behind, quiet and unhurried.
Quiet, tactile and completely unlabelled: reads "a rules-based basket of
things held together" without a single word or soldier in frame.

Deliberately NOT a repeat of the most recent heroes:
- The previous ETF Review hero (etf-review-spmo-2026-09-23) was two stacks of
  blank cream card stock plus a brass paperweight on dark walnut, TOP-DOWN in
  raking morning light. This one is side-on / three-quarter and uses neither
  card stacks nor a paperweight.
- Recent daily heroes used coffee mugs, laptops, notebooks, pens, reading
  glasses and phone-adjacent desk scenes. None of those appear here: no mug,
  no cup, no notebook, no ledger, no laptop, no pen, no glasses, no phone.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts of
  any kind anywhere in frame or at the frame edges.
- TEXT-FREE: cloth and paper are magnets for fake lettering, so every letter,
  word, number, percentage, price, ticker, logo, brand name, watermark,
  barcode, label, ruled line and print pattern is explicitly forbidden; every
  surface is completely blank and unprinted.
- No military insignia, weapons, ammunition, flags or camouflage.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92 (re-save q98 if
  under 85KB), mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-etf-review-shld-hero-20260930.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etf-review-shld-2026-09-30")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no body parts of "
    "any kind anywhere in the frame or at the edges of the frame. No text, "
    "no letters, no words, no numbers, no digits, no prices, no percentages, "
    "no currency symbols, no dollar signs, no ticker symbols, no charts, no "
    "graphs, no axis labels, no brand names, no company names, no fund names, "
    "no catalogue numbers, no measurement marks or ruler graduations, no "
    "rulers, no tape measure, no measuring instrument, no numerical scale, "
    "no measurement ticks, no hash marks, no small tick marks along any edge "
    "of any object, no unit abbreviations such as CM or INCH, no serial "
    "numbers, no part numbers, "
    "logos, no trademarks, no monograms, no watermarks, no signatures, no "
    "barcodes, no QR codes, no packaging labels, no tags, no stickers, no "
    "stamps, no seals, no newspaper, no magazine, no headlines, no book "
    "spines, no titles, no handwriting, no print, no printed marks, no "
    "printed fabric, no printed paper, no engraved marks, no embossed marks, "
    "no ruled lines, no lined paper, no grid, no woven-in lettering, no "
    "legible or illegible writing and no drawn marks of any kind anywhere in "
    "the image. Every surface in the picture is completely blank and "
    "unprinted: the olive-green canvas pouch is plain matte unlabelled cloth "
    "with absolutely no text, no logo, no tag and no print or woven pattern "
    "of any kind, reading only as cloth weave and soft shadow; the brass "
    "rod is a plain smooth featureless solid unbranded cylinder of matte "
    "brass with no numbers, no graduations, no ticks, no scale, no marks, no "
    "engraving and no lettering of any kind, never a ruler and never a "
    "measuring instrument; the rolled paper is completely blank unmarked "
    "white paper with nothing written, printed, stamped or embossed on it "
    "and clean blank unprinted edges. There is no readable or unreadable "
    "typography anywhere on any surface. No illustration, no digital art, no "
    "cartoon, no calligraphy, no typographic pattern, no 3D render, no CGI, "
    "no neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no chart graphics, no futuristic HUD graphics, no hologram, "
    "no floating overlay elements, no augmented reality graphics, no data "
    "center, no server room, no server racks, no cable runs, no server "
    "lights, no trading floor, no ticker screen, no stock chart display, no "
    "military insignia, no rank stripes, no badges, no weapons, no guns, no "
    "rifles, no ammunition, no shells, no grenades, no helmets, no uniforms, "
    "no flags, no camo, no camouflage pattern, no military hardware, no "
    "drones, no missiles, no vehicles."
)

PROMPTS = {
    # 1 — low three-quarter, eye-level: olive canvas pouch, plain matte brass
    # ruler, short roll of blank paper on dark oak, soft window light from
    # the left, deep creamy bokeh behind.
    "1": (
        "Photo-realistic editorial stock photograph, not a render and not "
        "computer generated, shot at eye level in a low three-quarter view on "
        "a 50mm lens at f/2.0 on a full-frame camera, looking slightly down "
        "and across a tidy dark oak desk in a quiet empty room with nobody "
        "present. Resting on the desk are three quiet, tactile, completely "
        "unlabelled objects: a small plain matte olive-green canvas "
        "drawstring pouch sitting on the left with its soft cloth body gently "
        "slumped and its simple drawstring lightly closed, a plain unbranded "
        "matte brass ruler lying flat across the desk in front of it, a "
        "smooth featureless strip of brushed brass with no marks and no "
        "numbers, and just behind them a short roll of completely blank "
        "unmarked white paper standing on end, its opening turned away so "
        "only the plain rolled outer surface and clean blank edge are "
        "visible. The three objects sit naturally at slightly different "
        "angles, close together but not touching, with calm empty desk around "
        "them. Soft natural window light falls in low and warm from the left, "
        "quiet overcast daylight through an unseen window, wrapping gently "
        "around the cloth pouch and laying one long soft shadow to the right "
        "across the oak. The desk is dark oak with a fine matte grain, and "
        "behind the objects the room dissolves into smooth creamy "
        "out-of-focus daylight and shadow. Shallow depth of field, the cloth "
        "of the pouch and the brass ruler crisply sharp nearest the camera "
        "and the paper roll already softening, real optical lens blur, honest "
        "available light editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, calm unhurried financial "
        "editorial mood, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — tighter, slightly higher angle on the same trio, window light from
    # the right, more negative space, cloth weave and brass texture dominant.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close view from a slightly raised three-quarter angle, shot "
        "on an 85mm lens at f/1.8, of a quiet desk still life on a dark oak "
        "desk in an empty room with no one in frame. Three plain unlabelled "
        "objects: a small matte olive-green canvas drawstring pouch on the "
        "right, its plain unprinted cloth softly creased and slightly "
        "slumped with the drawstring gathered loosely at its neck, a simple "
        "unbranded matte brass ruler lying at a slight diagonal in front of "
        "it, a smooth featureless brass strip with no engraving, no ticks "
        "and no numbers, and on the left a short upright roll of completely "
        "blank unmarked white paper, plain unprinted surface and clean blank "
        "edge facing the camera. The objects are grouped loosely with small "
        "gaps and honest natural placement, never arranged in a perfect line. "
        "Warm low late-afternoon window light comes in from the right, "
        "softly grazing the cloth weave of the pouch and catching the matte "
        "brass, casting one soft long shadow to the left across the dark oak "
        "grain. The background behind the objects falls away into an "
        "out-of-focus wash of quiet warm daylight and blurred dark wood. "
        "Extremely shallow depth of field with the cloth and the brass edge "
        "sharp and real optical blur everywhere else, honest editorial "
        "exposure, natural camera noise, very slight film grain, subtle lens "
        "vignette, sober calm mood, no plastic CGI sheen, no glossy render, "
        "no perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — low three-quarter view across the desk: olive canvas pouch, plain
    # matte brass rod lying flat, short roll of blank paper lying flat beyond
    # them, soft diffused daylight from the left, matte worn wood, no hard
    # window-pane shadows. Ruler deliberately dropped (flux draws graduations
    # and unit markings on any ruler-shaped object, twice proven on attempts
    # 1 and 2).
    "3": (
        "An ordinary unretouched 35mm film photograph, scanned straight from "
        "the negative with its natural grain, not a render and not computer "
        "generated and not a digital illustration, shot hand-held from a low "
        "three-quarter angle just above the surface of a dark oak desk on a "
        "35mm lens at f/2.8, in a quiet empty room with nobody present. The "
        "desk is clearly a desk: its softly worn rounded front edge crosses "
        "the lower part of the frame, the oak is matte, slightly scuffed and "
        "dull with age and honest wear marks, and behind it a plain dark "
        "plaster wall falls away out of focus. On the desk lie three small "
        "completely unlabelled objects: a plain matte olive-green canvas "
        "drawstring pouch with a soft slumped body of plain unprinted woven "
        "cloth and a simple cotton cord closure, lying flat on the desk in "
        "front of it a single plain smooth matte brass rod, a simple "
        "featureless solid cylindrical bar of dull warm brushed brass with no "
        "markings, no scale, no ticks, no numbers and no engraving of any "
        "kind, not a ruler and not a measuring instrument, and beyond them a "
        "short roll of completely blank unmarked white paper lying flat on "
        "the desk showing only its plain rolled outer surface and clean "
        "blank edge. The objects sit small and quiet in the lower left of "
        "frame, loosely grouped and natural, with a large calm expanse of "
        "bare matte oak around them and never arranged in a perfect line. "
        "Soft diffused overcast daylight falls in from the left through an "
        "unseen window, gentle and even with no hard focused window-pane "
        "shapes, softly modelling the dull texture of the cloth and the matte "
        "brass and leaving one soft diffuse shadow to the right. The far end "
        "of the desk and the wall behind dissolve into smooth creamy "
        "out-of-focus daylight and shadow. Moderate shallow depth of field "
        "with the pouch and the brass rod crisp and the paper roll and the "
        "desk edge softening, real optical blur, honest available light "
        "exposure with visible 35mm film grain throughout, matte surfaces "
        "with no gloss or sheen, subtle lens vignette, unhurried sober "
        "financial editorial mood, empty room with no human figure and no "
        "hands, no plastic CGI sheen, no glossy render, no hyper-real "
        "cleanliness, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
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
    if size < 87040:  # <85KB
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")

    # Folded-in verification
    for p in (OUTPUT, BACKUP):
        im = Image.open(p)
        print(f"VERIFY {p}  dims={im.size}  bytes={os.path.getsize(p)}")


if __name__ == "__main__":
    main()
