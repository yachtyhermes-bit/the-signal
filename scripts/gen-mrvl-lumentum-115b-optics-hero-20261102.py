#!/usr/bin/env python3
"""Generate hero for mrvl-lumentum-115b-optics-deal-2026 (fal flux/schnell).

Subject: Marvell buying Lumentum (~$115B) — the indium phosphide laser/photonics
layer that makes AI data-centre links move data as light.

Scene: OPTOELECTRONICS / PHOTONICS CLEANROOM, not a data centre.
  1) bunny-suit technician holding/inspecting a photonics wafer with visible
     laser diode dies, machined inspection equipment soft in the background.
  2) macro optical transceiver module on a workbench, fiber pigtails, laser die.
  3) cleanroom wafer-inspection station, gloved hands under a prober lens.

Rules: photo-realistic editorial stock photograph ONLY. No illustration, no
digital art, no neon, no glowing lines, no geometric patterns, no text/logos.
1440x810 generated -> 1920x1080 final, JPEG under 500KB.

Usage:
  ATTEMPT=1 OUT=/tmp/cand1.jpg /home/chino/video-venv/bin/python3 scripts/gen-mrvl-lumentum-115b-optics-hero-20261102.py
  FINALIZE_FROM=/tmp/cand1.jpg /home/chino/video-venv/bin/python3 scripts/gen-mrvl-lumentum-115b-optics-hero-20261102.py
"""
import os
import sys
import requests
from PIL import Image, ImageFilter

SLUG = "mrvl-lumentum-115b-optics-deal-2026"
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUT = os.environ.get("OUT", f"/tmp/mrvl_lite_cand_{ATTEMPT}.jpg")
FINAL = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no user interface, no software windows, "
    "no dashboards, no instrument readouts, no toolbars, no menus, no icons, "
    "no labels, no equipment nameplates, no model numbers, no serial "
    "numbers, no wafer scribe text, no die markings, no part numbers, no "
    "manufacturer logos, no brand names, no company names, no trademarks, "
    "no watermarks, no stickers, no barcodes, no QR codes, no printed "
    "signage, no safety signage, no warning labels, no wall posters, no "
    "badge lettering, no legible writing of any kind anywhere in the image. "
    "Any screen, monitor or instrument display in the frame is angled away, "
    "switched off, or so far out of focus that it shows only a soft flat "
    "wash of colour with nothing readable on it. All surfaces are plain and "
    "unmarked, all garments are plain and unbranded. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no glowing "
    "lines, no light trails, no synthwave, no geometric patterns, no circuit "
    "diagram, no network diagram, no graph graphic, no futuristic HUD "
    "graphics, no overlay elements, no augmented-reality graphics, no data "
    "center, no server room, no server racks, no server aisle, no rack "
    "hallway, no cable runs, no server lights, no GPU hardware."
)

PROMPTS = {
    "1": (
        "Photo-realistic professional editorial photograph, shot on a 50mm "
        "lens at f/2.0 inside a real optoelectronics photonics cleanroom. "
        "Centred in the frame, a technician in a white cleanroom bunny suit, "
        "hood, hairnet and clear safety glasses holds a large round "
        "semiconductor wafer up at chest height in both white-gloved hands, "
        "turning it slightly toward the overhead light to inspect it. The "
        "wafer's mirror surface is sharp and clearly readable: a dense "
        "repeating grid of hundreds of tiny square indium phosphide laser "
        "diode dies in iridescent gold, green, violet and blue, each die "
        "separated by thin saw streets, the whole disc catching a soft broad "
        "highlight. The gloved hands and the wafer edge are tack sharp; the "
        "technician's hooded head, shoulders and suit sit just behind, "
        "slightly softer but clearly in focus, the face calm and partly "
        "obscured by the hood and glasses. Behind the technician the "
        "cleanroom falls into gentle soft-focus bokeh: a row of large "
        "machined stainless-steel wafer inspection and probe stations, "
        "brushed metal panels, a round inspection microscope on an "
        "articulated arm, a wafer prober with a black lens barrel, all "
        "smooth featureless anonymous equipment lit by cool white ceiling "
        "panels with faint warm amber accents. Clean, quiet, real industrial "
        "lighting, soft shadows, honest available-light editorial exposure, "
        "shallow depth of field with genuine optical blur, natural camera "
        "noise and very slight film grain, subtle lens vignette, no plastic "
        "CGI sheen, no glossy render, no perfect symmetry, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real macro photograph on a 100mm lens at f/4, not a render: an "
        "optical transceiver module on a clean matte workbench in a photonics "
        "lab. In the sharp foreground the small silver rectangular metal "
        "transceiver housing lies on its side, its cage opened, with a "
        "polished gold-plated edge connector and a tiny exposed laser diode "
        "chip glinting inside, a fine wire bond catching the light. Two "
        "black-jacketed single-mode fiber pigtails with yellow and blue "
        "strain-relief boots curl away from the module in soft arcs across "
        "the bench, their connectors resting on a plain white lint-free "
        "cloth. A gloved fingertip in a white nitrile glove rests on the "
        "module body, steadying it. Behind, melting into creamy bokeh, a "
        "soldering microscope, a small machined aluminium fixture and a rack "
        "of dark lab instruments with soft warm indicator glows, all "
        "unreadable and out of focus. Warm practical bench lamp light from "
        "the upper left, cool neutral fill, deep soft shadows. Extremely "
        "shallow depth of field, the module and fingertip pin sharp, real "
        "optical blur behind, honest available-light editorial exposure, "
        "natural camera noise and very slight film grain, subtle lens "
        "vignette, faint dust, no plastic CGI sheen, no glossy render, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine documentary-style photograph inside a semiconductor "
        "photonics cleanroom, wide three-quarter view. A technician in a "
        "white bunny suit and hood stands at a stainless wafer inspection "
        "station, both gloved hands holding the edge of a large round "
        "photonics wafer flat above a machined vacuum chuck, examining it "
        "under the objective lens of a black inspection microscope mounted "
        "on an articulated arm. The wafer's face shows a dense grid of tiny "
        "square laser diode dies in green, gold and violet iridescence, "
        "clearly visible and sharp. The technician's gloved hands, the wafer "
        "and the microscope objective are the sharp subject; the shoulders "
        "and hood are slightly softer. Around and behind, the cleanroom "
        "recedes into soft bokeh: pale stainless equipment cabinets, a "
        "wafer prober, a laminar-flow hood with a faint amber glow, smooth "
        "featureless machined surfaces, cool white ceiling lighting with "
        "warm accents on the metal. Clean modern industrial lab, calm, "
        "spacious, realistic lighting with soft shadows. Shallow depth of "
        "field, real optical blur, honest available-light editorial "
        "exposure, natural camera noise and very slight film grain, subtle "
        "lens vignette, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
}

# Attempt 4 = tuned variant of the cleanroom scene after attempt 1's flaws
# (translucent-looking wafer showing the tech's face through it, dies far too
# large/coarse, slight CGI sheen).
PROMPTS["4"] = (
    "An unretouched documentary photograph taken by a staff photographer on a "
    "full-frame DSLR with an 85mm lens at f/2.8, inside a working "
    "optoelectronics photonics cleanroom. A technician in a plain white "
    "cleanroom bunny suit, white hood, hairnet and clear safety glasses "
    "stands three-quarter to the camera and holds a large round silicon "
    "photonics wafer up at chest height, tilted slightly away from their "
    "face, in both white-gloved hands, examining the light glancing off its "
    "surface. The wafer is completely solid, opaque and mirror-finished, a "
    "sheet of polished metal that reflects only light and the blurred room, "
    "absolutely nothing visible through it, no transparency, no see-through "
    "glass. Its surface is covered edge to edge in a very fine, dense, "
    "microscopic repeating grid of hundreds of thousands of tiny square "
    "laser diode dies, so small they read as a fine woven texture of muted "
    "gold, olive green and violet with thin darker saw streets, the detail "
    "resolving only where the light rakes across it. The gloved hands, the "
    "wafer rim and the fine surface texture are pin sharp. The technician's "
    "hooded head and shoulders are just behind, softly but clearly in focus, "
    "face calm and partly hidden by the hood and glasses. Behind them the "
    "cleanroom recedes into smooth out-of-focus bokeh: a row of big machined "
    "stainless-steel wafer inspection stations and probe machines, brushed "
    "and anodised panels, a black inspection microscope on an articulated "
    "arm, plain featureless anonymous equipment under cool white ceiling "
    "panels with faint warm amber accents on the metal. Quiet real "
    "industrial lighting, soft directional shadows, honest available-light "
    "exposure, shallow depth of field with genuine optical blur, visible "
    "natural camera noise and slight film grain, subtle vignette, imperfect "
    "framing, no CGI sheen, no plastic skin, no glossy render, no perfect "
    "symmetry, no studio backdrop, photorealistic, very high detail, "
    "professional editorial stock photography, 16:9 landscape composition. "
    + NO_TEXT
)


def load_fal_key():
    for env_path in ("/home/chino/hermes-workspace/studio-api/.env",):
        if os.path.exists(env_path):
            for line in open(env_path):
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        raw = open(real_path).read().strip().split("\n")[0]
        key = raw.split("|", 1)[1] if "|" in raw else raw
        if key:
            os.environ["FAL_KEY"] = key
            return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating with fal flux/schnell ...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )
    url = None
    if result.get("images"):
        url = result["images"][0]["url"]
    elif result.get("output"):
        url = result["output"]
    elif result.get("image"):
        url = result["image"]
    if not url:
        print("ERROR: no image url:", result)
        sys.exit(1)
    print("URL:", url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path).convert("RGB")
    print(f"Downloaded {out_path} size={img.size} bytes={len(r.content)}")
    return img


def crop_to_16x9(img):
    w, h = img.size
    target = FINAL_W / FINAL_H
    cur = w / h
    if cur > target:
        nw = int(h * target)
        left = (w - nw) // 2
        img = img.crop((left, 0, left + nw, h))
    elif cur < target:
        nh = int(w / target)
        top = (h - nh) // 2
        img = img.crop((0, top, w, top + nh))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def save_jpeg(img, path, max_bytes=500 * 1024):
    """Save JPEG trying descending quality until under max_bytes."""
    for q in (92, 88, 84, 80, 76, 72, 68, 64):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= max_bytes:
            print(f"  saved {path} q={q} bytes={size}")
            return size
    print(f"  WARNING: {path} still {os.path.getsize(path)} bytes at q=64")
    return os.path.getsize(path)


def finish(img):
    """Light photographic finishing: mild tone lift, sharpen, fine grain."""
    from PIL import ImageEnhance
    import numpy as np
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
    arr = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(7)
    noise = rng.normal(0.0, 3.2, arr.shape[:2])[:, :, None]
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def finalize(src):
    img = Image.open(src).convert("RGB")
    img = crop_to_16x9(img)
    img = finish(img)
    os.makedirs(os.path.dirname(FINAL), exist_ok=True)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    size = save_jpeg(img, FINAL)
    save_jpeg(img, BACKUP)
    print(f"FINAL {FINAL} dims={img.size} bytes={size}")
    print(f"BACKUP {BACKUP} bytes={os.path.getsize(BACKUP)}")
    assert os.path.getsize(FINAL) == os.path.getsize(BACKUP), "mirror size mismatch"


if __name__ == "__main__":
    if os.environ.get("FINALIZE_FROM"):
        finalize(os.environ["FINALIZE_FROM"])
    else:
        if ATTEMPT not in PROMPTS:
            print("no prompt for ATTEMPT", ATTEMPT)
            sys.exit(1)
        generate(PROMPTS[ATTEMPT], OUT)
