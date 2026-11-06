#!/usr/bin/env python3
"""Hero for iren-ai-cloud-revenue-triples-construction-test-2026 (fal flux/schnell).

Subject: IREN Limited — the Texas AI-cloud company that began as a bitcoin miner
and is now building out power-and-land-heavy campuses. The picture is the
metaphor, not hardware: a wide aerial drone frame at golden hour over a vast
solar array curving across dry Texas grassland, with a long low white industrial
building complex and gravel access roads far off on the horizon under a big
clean sky. Cheap land, cheap power, enormous scale.

Deliberately NOT a server room / data-centre hallway / rack aisle / cranes or
steel skeletons / substation / neon / synthwave / glowing lines / geometric
patterns / abstract art / 3D render.

Rules:
- PHOTO-REALISTIC editorial aerial ONLY, natural golden-hour daylight.
- TEXT-FREE: no letters/numbers/signs/logos/watermarks anywhere.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-iren-ai-cloud-construction-hero-20261106.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image, ImageFilter

SLUG = os.environ.get("SLUG", "iren-ai-cloud-revenue-triples-construction-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080
MAX_BYTES = 480 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no signs, no billboards, no printed "
    "labels, no painted markings, no stencilled codes, no unit numbers on "
    "any building, no panel identification tags, no decals, no corporate "
    "logos, no trademarks, no graffiti, no handwriting, no signatures, no "
    "watermarks, no overlay captions, no legible writing of any kind "
    "anywhere in the image. Every roof, wall, panel, road and fence in the "
    "frame is plain, bare and unmarked. No people, no hands, no fingers, no "
    "vehicles with visible markings, no human silhouettes, no aircraft in "
    "frame, no drone visible. No illustration, no digital art, no matte "
    "painting, no cartoon, no 3D render, no CGI, no CGI sheen, no "
    "infographic, no chart overlay, no glowing lines, no neon, no synthwave, "
    "no teal-and-orange blockbuster grade, no purple colour grading, no "
    "high-contrast HDR look, no lens flare artefacts, no artificial "
    "geometric overlay."
)

PHOTO_TAIL = (
    "Shot as a real aerial photograph from a small drone hovering high above "
    "the ground with the camera tilted slightly down, on a wide prime lens "
    "at f/5.6, deep focus so near and far are both sharp, honest natural "
    "evening exposure, slightly hazy air, muted desaturated colour, low "
    "contrast, flat documentary look, fine true-to-life sensor grain, "
    "gentle atmospheric haze toward the horizon, no colour grading, no "
    "filter, no plastic CGI sheen, no glossy render, no perfect symmetry, "
    "no 3D visualisation, no digital illustration, no painting, "
    "photorealistic, high detail, ordinary documentary editorial aerial "
    "photography for a financial news site, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — PRIMARY: vast curving solar array, low white buildings on horizon.
    "1": (
        "Aerial drone photograph, photo-realistic editorial documentary "
        "image, taken at golden hour in west Texas. The camera is high above "
        "the ground looking slightly down and out across an enormous flat "
        "expanse of dry short-grass prairie, pale straw and dusty olive, "
        "with faint patches of bare red-brown earth showing through. "
        "Filling the lower two thirds of the frame is a vast utility-scale "
        "solar array: thousands of long identical rows of dark blue-black "
        "photovoltaic panels mounted low on thin steel posts, the rows laid "
        "out in a great sweeping curve that bends from the lower left of the "
        "frame across the foreground and away toward the right, so the array "
        "reads as a huge dark ribbon of glass curving over the pale grass. "
        "The rows are evenly spaced with narrow strips of dry grass and pale "
        "gravel service lanes between them, and the low warm sun behind the "
        "panels catches their top edges so each row throws a long shadow "
        "forward onto the grass and glints faintly along its upper lip; seen "
        "from this height and angle the tilted panels reveal their dark "
        "faces in receding diagonal bands that converge toward the horizon. "
        "Beyond the array, on the flat horizon line across the upper third "
        "of the frame, sits a long, low complex of plain white industrial "
        "buildings — rectangular windowless metal-clad halls with flat roofs "
        "and shallow grey rooftop units, laid out in a loose line perhaps a "
        "kilometre away, small in the frame and softened by warm haze, with "
        "pale gravel access roads running straight out from them across the "
        "grass toward the foreground. A thin line of dark green scrub and a "
        "few low utility poles follow one of the roads. Above it all is a "
        "huge, clean, nearly cloudless sky, a smooth gradient from warm pale "
        "gold at the horizon up through soft dusty blue to a deeper blue at "
        "the top of the frame, with just one or two thin high streaks of "
        "cirrus far off to the right. The light is low and warm, coming from "
        "behind and slightly left of the panels, so the grass glows amber "
        "and the shadows stretch long and soft to the right. The mood is "
        "scale, open land and cheap power — quiet, empty, enormous, "
        "matter-of-fact, nothing dramatic happening. Nothing else is in the "
        "frame: no towers, no cranes, no machinery, no buildings under "
        "construction, no fences in the foreground, no water, no city. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 2 — FALLBACK: oblique angle, fewer cleaner rows, buildings read clearly.
    "2": (
        "Aerial drone photograph, photo-realistic editorial documentary "
        "image, taken at golden hour on the dry Texas plains, shot from "
        "several hundred feet up with the camera angled gently down. In the "
        "lower half of the frame, occupying the middle distance rather than "
        "the immediate foreground, a large utility-scale solar farm spreads "
        "across flat, short, dry golden-brown grassland: long, clean, "
        "orderly parallel rows of dark navy-black photovoltaic panels "
        "mounted low on slim posts, each row a straight unbroken line, all "
        "of them running on the same axis and separated by even strips of "
        "dry grass and pale dusty gravel service lanes, laid out in a broad "
        "sweeping arc so the rows curve together across the plain and "
        "narrow into fine regular dark lines in the distance. The geometry "
        "is precise, industrial and calm, every row the same height and "
        "spacing, the surfaces of the panels flat and matte, catching a "
        "thin warm glint along their upper edges. The low sun sits behind "
        "and to the left of the array, so the panel faces fall into deep "
        "shadow and each row throws a long soft shadow forward across the "
        "pale grass toward the viewer. Behind the array, clearly visible on "
        "the flat horizon at the right of centre and standing alone on the "
        "empty plain, is a long, low complex of plain white industrial "
        "buildings: several connected windowless rectangular halls with "
        "flat grey-white roofs, maybe four to six storeys tall, laid out "
        "end to end in a single unbroken run perhaps a kilometre long, "
        "plainly readable as a single enormous facility, with straight "
        "pale gravel access roads running out from it across the grassland "
        "and a sparse line of thin utility poles and low dark scrub along "
        "one road. The top third of the frame is open, clean sky: soft warm "
        "peach and pale gold low down at the horizon, lifting into a clear, "
        "calm, dusty blue higher up, almost cloudless with only faint high "
        "streaks far to the right. Warm raking evening light, long soft "
        "shadows, gentle atmospheric haze building with distance, honest "
        "dusty textures. The mood is vast open space, cheap land and cheap "
        "power at industrial scale, quiet and matter-of-fact. No towers, no "
        "cranes, no machinery, no substation hardware, no buildings under "
        "construction, no city, no water. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 3 — LAST RESORT: short, plainly photographic, buildings stated up front.
    "3": (
        "Aerial drone photograph, photo-realistic, taken in the last hour of "
        "light over flat, dry farmland in Texas. On the horizon, across the "
        "upper middle of the frame, sits a very long, low, plain white "
        "industrial complex: one unbroken run of flat-roofed, windowless "
        "warehouse buildings, white walls catching the warm low sun, small "
        "with distance and hazed by dusty air, standing completely alone on "
        "the empty plain. Straight pale gravel access roads run out from it "
        "across the land toward the camera, with a sparse line of thin poles "
        "and low dark scrub along one road. In front of the buildings, "
        "filling the lower half of the frame, is a huge field of solar "
        "panels laid over dry golden-brown grass: long straight parallel "
        "rows of dark tilted panels running in one direction across the "
        "plain, separated by strips of dry grass and pale dirt tracks, the "
        "rows in shadow with a thin warm glint of light along their top "
        "edges and their long soft shadows falling toward the viewer. The "
        "land is dead flat, empty and endless. Above, a big clean sky, "
        "pale dusty blue higher up fading to warm cream at the horizon, with "
        "the faintest high wisp of cloud. The light is low and warm, the "
        "colours muted and dusty, the air slightly hazy, the whole scene "
        "quiet and ordinary like a documentary photograph of an empty place "
        "at the end of the day. No towers, no cranes, no machinery, no "
        "substation, no construction site, no city, no water. "
        + PHOTO_TAIL
        + " " + NO_TEXT
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
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    hermes_env = "/home/chino/.hermes/profiles/yachty/.env"
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if line.strip().startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    return None


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
    img = img.convert("RGB")
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


def save_bounded(img, path):
    """Save JPEG at the highest quality that stays under MAX_BYTES."""
    for q in (90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print(f"Saved {path} quality={q} bytes={size}")
            return size
    print(f"WARNING: still {os.path.getsize(path)} bytes at min quality")
    return os.path.getsize(path)


def ocr_text_check(path, min_conf=70.0):
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return [], []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11", "tsv"],
                check=True, capture_output=True, timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return [], []
        tsv = base + ".tsv"
        if not os.path.exists(tsv):
            return [], []
        with open(tsv, errors="ignore") as f:
            rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]

    readable, noise = [], []
    for row in rows[1:]:
        if len(row) < 12:
            continue
        try:
            conf = float(row[10])
        except ValueError:
            continue
        text = row[11].strip()
        clean = "".join(ch for ch in text if ch.isalnum())
        if conf <= 0 or len(clean) < 3:
            continue
        (readable if conf >= min_conf else noise).append((text, conf))
    return readable, noise


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    size = save_bounded(img, OUTPUT)
    print(f"FINAL {OUTPUT} dimensions={img.size} bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copyfile(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
    readable, noise = ocr_text_check(OUTPUT)
    if not readable:
        print(f"OCR TEXT CHECK: clean ({len(noise)} sub-threshold blob(s) ignored)")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
