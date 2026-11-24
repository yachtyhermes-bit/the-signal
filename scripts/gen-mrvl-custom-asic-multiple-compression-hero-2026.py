#!/usr/bin/env python3
"""Generate hero for mrvl-custom-asic-multiple-compression-2026 (fal flux/schnell).

Subject: Marvell Technology (MRVL) — fabless custom AI accelerator programs and
optical interconnect silicon being repriced (multiple compression on
program-based custom silicon). NOT a product launch.

Scene rules: photonics lab / bench bench work, NOT a data centre, NOT a server
room / server aisle. Photo-realistic editorial stock photograph only.

  1) macro: optical transceiver module + fiber ribbon held in a technician's
     gloved hand over a workbench, shallow DOF.
  2) silicon photonics die on a probe station under cleanroom lighting, gloved
     hands adjusting a probe card.
  3) fabless chip designer's lab bench: packaged ASIC in a test socket, soft
     oscilloscope trace on a screen behind it.

No text/logos/watermark, no illustration/digital art/neon/glow/geometrics.
1536x864 generated -> 1536x864 final, JPEG under 400KB.

Usage:
  ATTEMPT=1 OUT=/tmp/mrvlc_cand1.jpg /home/chino/video-venv/bin/python3 \
      scripts/gen-mrvl-custom-asic-multiple-compression-hero-2026.py
  FINALIZE_FROM=/tmp/mrvlc_cand1.jpg /home/chino/video-venv/bin/python3 \
      scripts/gen-mrvl-custom-asic-multiple-compression-hero-2026.py
"""
import os
import sys
import requests
from PIL import Image, ImageFilter

SLUG = "mrvl-custom-asic-multiple-compression-2026"
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUT = os.environ.get("OUT", f"/tmp/mrvlc_cand_{ATTEMPT}.jpg")
FINAL = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no user interface, no software windows, "
    "no dashboards, no instrument readouts, no toolbars, no menus, no icons, "
    "no labels, no equipment nameplates, no model numbers, no serial "
    "numbers, no die markings, no part numbers, no manufacturer logos, no "
    "brand names, no company names, no trademarks, no watermarks, no "
    "stickers, no barcodes, no QR codes, no printed signage, no safety "
    "signage, no warning labels, no wall posters, no badge lettering, no "
    "legible writing of any kind anywhere in the image. Any screen, monitor "
    "or instrument display in the frame is angled away or so far out of "
    "focus that it shows only a soft flat wash of colour with nothing "
    "readable on it. All surfaces are plain and unmarked, all garments are "
    "plain and unbranded. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no circuit diagram, no network "
    "diagram, no graph graphic, no futuristic HUD graphics, no overlay "
    "elements, no augmented-reality graphics, no data center, no server "
    "room, no server racks, no server aisle, no rack hallway, no cable runs, "
    "no blinking server lights, no GPU hardware, no warehouse of computers."
)

PROMPTS = {
    # (a) macro optical transceiver + fiber ribbon in a gloved hand, workbench
    "1": (
        "Professional stock photograph of a macro shot on a 100mm macro lens "
        "at f/3.5: a technician's white nitrile-gloved hand holding a small "
        "silver optical transceiver module over a matte stainless workbench "
        "in a fibre-optics lab, a short ribbon of twelve fine single-mode "
        "fibres fanning out of its gold connector in a graceful arc and "
        "resting loosely across the gloved fingers. The module's polished "
        "metal housing, the gold edge contacts and the individual fibre "
        "strands are tack sharp; the bench surface and the lab behind melt "
        "into creamy bokeh — a soldering microscope stand, a coil of black "
        "jacket cable, a machined aluminium fixture, all anonymous and out "
        "of focus. Warm practical bench lamp from the upper left, cool "
        "neutral fill, soft long shadows, shallow depth of field with "
        "genuine optical blur, honest available-light exposure, natural "
        "camera noise and very slight film grain, subtle lens vignette, "
        "no CGI sheen, no glossy render, photorealistic, very high detail, "
        "16:9 landscape composition. " + NO_TEXT
    ),
    # (b) silicon photonics die on a probe station, gloved hands on probe card
    "2": (
        "Professional stock photograph of a silicon photonics chip die "
        "mounted on a machined vacuum chuck of a wafer probe station inside "
        "a cleanroom, photographed from a low three-quarter angle on an "
        "85mm lens at f/2.8. In the sharp foreground two hands in white "
        "gloves rest on the edge of a black probe card, one gloved finger "
        "steadying a fine needle probe touching the die. The die itself is "
        "an iridescent square of polished silicon, a few centimetres across, "
        "its surface catching a soft rainbow sheen of teal, violet and gold "
        "from the overhead light, fine optical waveguides catching the "
        "raking light as faint texture. Behind, softly out of focus, the "
        "probe station's black lens barrel, an articulated arm and brushed "
        "stainless panels recede into bokeh under cool white ceiling panels "
        "with a faint amber accent. Quiet real industrial lighting, soft "
        "directional shadows, shallow depth of field, genuine optical blur, "
        "honest available-light exposure, natural camera noise and very "
        "slight film grain, subtle vignette, no CGI sheen, no glossy render, "
        "photorealistic, very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # (c) designer's lab bench: packaged ASIC in test socket + scope trace
    "3": (
        "Professional stock photograph of an electronics engineer's lab "
        "bench in a small fabless chip design office, shot on a 50mm lens at "
        "f/2.2. In the sharp foreground a large square packaged ASIC with a "
        "silver heat spreader sits clamped in a black spring-loaded test "
        "socket on a green evaluation board, its fine gold pins and the "
        "socket's machined contacts clearly visible; a bundle of thin grey "
        "probe leads loops away from the board across a plain anti-static "
        "mat. Just behind it, slightly out of focus, a bench oscilloscope "
        "shows a soft blurry green waveform on its dark screen, no numbers "
        "and no text legible, only a gentle smeared glow of a trace. A "
        "white-gloved hand rests near the board holding a fine probe. The "
        "background falls into warm soft bokeh: a bench power supply, a coil "
        "of cable, a stack of plain anti-static trays, all unmarked. Warm "
        "desk lamp light from the right, cool fill from a window, soft "
        "shadows, shallow depth of field with genuine optical blur, honest "
        "available-light exposure, natural camera noise and slight film "
        "grain, subtle vignette, no CGI sheen, no glossy render, "
        "photorealistic, very high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
}


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
    print(f"Generating with fal flux/schnell at {W}x{H} ...")
    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": {"width": W, "height": H},
                "num_inference_steps": 4,
                "enable_safety_checker": False,
            },
        )
    except Exception as e:
        print("generate() failed:", e)
        raise
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
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def save_jpeg(img, path, max_bytes=MAX_BYTES):
    """Save JPEG trying descending quality until under max_bytes."""
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 72, 68, 64, 60):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= max_bytes:
            print(f"  saved {path} q={q} bytes={size}")
            return size
    print(f"  WARNING: {path} still {os.path.getsize(path)} bytes at q=60")
    return os.path.getsize(path)


def finish(img):
    """Light photographic finishing: mild tone lift, sharpen, fine grain."""
    from PIL import ImageEnhance
    import numpy as np
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=50, threshold=3))
    arr = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(7)
    noise = rng.normal(0.0, 2.8, arr.shape[:2])[:, :, None]
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
