#!/usr/bin/env python3
"""Hero for app-applovin-ad-engine-decoupling-2026 (fal flux/schnell).

Subject: AppLovin — the mobile advertising / AI ad-targeting engine. The picture
is the metaphor, not a product: a person's hands cradling a phone in a warm
cafe at dusk, the screen throwing soft coloured light onto their fingers, the
room behind them dissolving into warm bokeh. A single glowing rectangle in the
middle of an ordinary evening.

Deliberately NOT a data-centre hallway / server rack / neon / synthwave / CGI /
3D render / abstract art / dashboard screenshot.

Rules:
- PHOTO-REALISTIC editorial photography ONLY, warm dusk interior light.
- TEXT-FREE: no letters/numbers/icons/UI/logos on the screen or anywhere.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-app-applovin-ad-engine-decoupling-hero-20261105.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "app-applovin-ad-engine-decoupling-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "Strictly no lettering anywhere in the image: no text, no letters, no "
    "words, no numbers, no digits, no icons, no user-interface elements, no "
    "buttons, no menus, no notification badges, no app icons, no logos, no "
    "brand names, no trademarks, no signage, no price tags, no subtitles, no "
    "captions, no watermarks, no handwriting, no legible writing of any kind. "
    "The phone screen shows only soft, undefined washes of colour and light — "
    "no readable content at all. No facial features in focus, no eye contact "
    "with the camera. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no CGI sheen, no infographic, no chart overlay, no "
    "glowing lines, no neon, no synthwave, no cyberpunk, no purple or teal "
    "colour grading, no high-contrast HDR look."
)

PHOTO_TAIL = (
    "Real optical lens blur with creamy out-of-focus falloff, honest natural "
    "exposure, fine true-to-life sensor grain, subtle optical vignette, "
    "true-to-life colour, warm neutral tones, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no 3D visualisation, no digital "
    "illustration, no painting, photorealistic, extremely high detail, "
    "professional editorial stock photography for a technology news site, "
    "16:9 landscape composition, shallow depth of field, shot at f/1.8."
)

PROMPTS = {
    # 1 — PRIMARY: hands and phone in a warm cafe at dusk, screen glow only.
    "1": (
        "Professional stock photograph, photo-realistic editorial shot on an "
        "85mm lens at f/1.8 on a full-frame camera, tight three-quarter "
        "framing. In the sharp foreground, a pair of ordinary adult hands "
        "hold a plain modern smartphone upright and slightly tilted toward "
        "the lens, both thumbs resting loose against the lower edges of the "
        "device, the fingers relaxed and natural with visible knuckles, "
        "short clean nails and a little honest skin texture, no jewellery. "
        "The phone has a dark matte case and a slim dark bezel, its glass "
        "face turned up toward the person holding it, and the screen is a "
        "soft blurred bloom of warm colour — gentle gradients of amber, "
        "rose and pale jade with no defined shapes, no interface, no words, "
        "nothing readable at all — spilling a smooth wash of coloured light "
        "across the fingers and the base of the thumbs. The hands are lit "
        "mainly by that screen glow from below, warm and low, with a small "
        "cool rim of dusk light from a window behind picking out the top "
        "edges of the fingers and the crown of the phone. Behind the hands "
        "the scene falls away completely out of focus: the warm interior of "
        "a small cafe at dusk, a dark wooden table edge just under the "
        "wrists, the suggestion of a ceramic cup, and past it a window with "
        "the last blue-grey evening light outside and round amber pendant "
        "lamps inside blossoming into wide soft bokeh circles. The "
        "background is deep and quiet — burnt umber, warm shadow, one or two "
        "muted teal highlights — so the lit phone and the hands around it "
        "are the only crisp, bright thing in the frame. Palette of warm "
        "amber, dark wood brown, dusky blue and soft rose. The mood is "
        "quiet, absorbed, everyday — someone scrolling in the last hour of "
        "the day. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 2 — FALLBACK: closer, front-lit by the screen only, dim warm cafe interior.
    "2": (
        "Professional stock photograph, photo-realistic editorial shot on a "
        "50mm lens at f/1.8 on a full-frame camera at chest height, "
        "candid and close. A person's two hands, seen from the front and "
        "slightly above, hold a plain dark smartphone low in front of them "
        "at waist height, sitting at a dark wooden table in a small cafe "
        "after sunset, the thumbs poised over the screen, the fingers "
        "curving around the back of the device, skin real and unretouched "
        "with fine creases, short fingernails and a plain dark knit sleeve "
        "cuff at the wrist in view. The phone's screen is turned up and is "
        "the closest and brightest light in the whole frame: a soft diffuse "
        "bloom of saturated colour — warm coral, deep gold and a cool mint "
        "wash bleeding into one another with no defined edges, no "
        "interface, no icons, no words — and the light from it falls "
        "directly onto the fingers, the backs of the thumbs and the lower "
        "palm, painting them in warm amber and rose, so the hands are "
        "clearly lit and fully visible rather than a silhouette, with the "
        "fine texture of the skin readable. Beyond the hands and the near "
        "edge of the dark wooden tabletop everything is out of focus and "
        "much dimmer: the shadowed warm interior of the cafe, the soft "
        "round shapes of two empty chairs, a small white ceramic cup "
        "blurred at the table edge, and far off toward the upper right a "
        "cluster of round amber pendant lamps blossoming into wide creamy "
        "bokeh against deep brown shadow, plus the faintest cool blue hint "
        "of a distant window high in the background — nothing bright enough "
        "to silhouette the hands. Palette of warm amber, rose, dark walnut "
        "brown, off-white ceramic and a whisper of dusky blue. The mood is "
        "quiet, absorbed, everyday — a person alone with a screen in the "
        "last hour of the evening. "
        + PHOTO_TAIL
        + " " + NO_TEXT
    ),
    # 3 — LAST RESORT: wider cafe table, phone lying face-up, hands entering.
    "3": (
        "Professional stock photograph, photo-realistic editorial shot on a "
        "35mm lens at f/2 on a full-frame camera from a low angle across a "
        "dark wooden cafe table at dusk. A plain dark smartphone lies "
        "face-up on the table in the middle of the frame, its screen glowing "
        "with a soft undefined bloom of warm amber, rose and pale green "
        "colour that fades out at the edges — no interface, no icons, no "
        "words, nothing readable — and that glow pools on the polished wood "
        "around it and catches along the rim of a small white ceramic "
        "espresso cup just behind it. A person's hand enters the frame from "
        "the right foreground, out of focus and soft, one finger reaching "
        "toward the edge of the phone, the rest of the hand and forearm "
        "falling away into blur; a plain dark sleeve cuff is just visible. "
        "The far side of the cafe is completely out of focus: dark warm "
        "walls, the soft shapes of empty chairs, and a window at dusk with "
        "cool blue-grey light and round amber lamps blooming into wide "
        "creamy bokeh. The phone and the little stretch of lit tabletop are "
        "the only sharp things in the image. Palette of warm amber, dark "
        "walnut brown, off-white ceramic, dusky blue. The mood is still and "
        "intimate — an ordinary evening table, one screen left glowing. "
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
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def save_bounded(img, path):
    """Save JPEG at the highest quality that stays under MAX_BYTES."""
    for q in (93, 91, 89, 87, 85, 82, 79, 76, 73, 70):
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
    with open(f"/tmp/{SLUG}-prompt-{ATTEMPT}.txt", "w") as f:
        f.write(prompt)
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
