#!/usr/bin/env python3
"""Hero for coin-binance-hack-crypto-risk-repricing-2026 (fal flux/schnell).

Subject: Coinbase fell ~12% on Oct 30 2026 despite beating earnings, because a
~$6.3B hack at rival Binance repriced the whole crypto asset class. Bitcoin
~$86K -> ~$77K.

Scene: a real crypto exchange trading desk at night. Monitors glowing with
falling red price charts, two traders in shirtsleeves seen from behind, cold
blue monitor light, shallow depth of field, 35mm, natural grain.

NO data center / server racks, no neon / synthwave, no glowing geometric
lines, no abstract digital art, no 3D render, no text / numerals / logos /
legible values, no Bitcoin logo, no recognizable real person, no watermark.

Hard cap: 3 generations.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-coin-binance-hack-hero-20261030.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "coin-binance-hack-crypto-risk-repricing-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "Absolutely no text anywhere in the image: no words, no letters, no "
    "numerals, no tickers, no prices, no logos, no branding, no signage, no "
    "labels, no captions, no watermarks, no handwriting. The chart screens "
    "show only unreadable soft red and dark graph shapes with no axis numbers "
    "and no legible figures whatsoever. No data center, no server room, no "
    "server racks, no server aisle, no cable spaghetti. No neon, no synthwave, "
    "no glowing laser lines, no geometric patterns, no abstract digital art, "
    "no 3D render, no CGI, no crypto coin symbols, no bitcoin logo. No "
    "recognizable real person. Strictly photo-realistic editorial stock "
    "photography, natural film grain, true-to-life skin and fabric texture."
)

PROMPTS = {
    # 1: side-on across two desks, traders in shirtsleeves from behind
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "35mm lens at f/1.8 on a full-frame camera, handheld, eye level, "
        "slightly oblique to the desks. A cryptocurrency exchange trading "
        "floor late at night. In the near foreground, sharp focus on the backs "
        "and shoulders of two traders in rumpled white and pale grey dress "
        "shirtsleeves, one with his sleeves pushed up and a loosened dark tie, "
        "seated close together at a long black desk, leaning toward their "
        "screens; we see them from behind and slightly to the side, heads "
        "turned to the monitors, faces not visible at all. Three large matte "
        "monitors rise in front of them, blown into soft glowing bokeh, filled "
        "with dark red and maroon downward-sloping candlestick charts that are "
        "completely out of focus so only unreadable red colour and shape "
        "remains. Behind them, deeper into the room, a few more low desks and "
        "the vague silhouettes of three or four colleagues far out of focus, "
        "some standing. Cold blue-white monitor light is the only real source, "
        "rimming the traders' shoulders and hair, falling off into near "
        "blackness in the corners; a faint warm desk lamp glows far in the "
        "background. Empty coffee cups, a pen, a headset and scattered papers "
        "turned away from camera on the desk surface. Moody, tense, quiet, "
        "documentary realism, shot on 800-speed colour negative film, visible "
        "natural grain, slight highlight bloom, no HDR, no clarity boost. "
        + NO_TEXT
    ),
    # 2: over-the-shoulder single trader, wall of screens with red charts
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, 35mm lens "
        "wide open at f/2.0, camera behind and just above the shoulder of one "
        "trader, shallow depth of field. A crypto exchange trading desk at "
        "night: a man in his thirties in a white shirtsleeve, dark tie pulled "
        "loose, sits hunched forward at a black desk, seen from behind and "
        "slightly right, his face entirely hidden, one hand raised to his "
        "forehead, the other resting flat beside a keyboard. Directly ahead of "
        "him four horizontal monitors in a row glow with dark red, plunging "
        "candlestick price charts, defocused into soft crimson glow with no "
        "readable detail. Off to the right, out of focus, a female colleague "
        "in a slate shirt stands with arms folded looking at a separate "
        "screen, only her shoulder and silhouette readable. The room beyond is "
        "dark grey and shadowed, tall windows showing black night city with a "
        "scatter of blurred lights. Cold blue-white screen light on his neck, "
        "hair and the fabric of his shirt, deep shadows under the desk, the "
        "warm amber of a small desk lamp on the far left. Tense, silent, "
        "believable, documentary photojournalism, natural film grain, slight "
        "lens vignette, no post-processing gloss. "
        + NO_TEXT
    ),
    # 3: wider, the whole night floor, traders small in frame, red glow
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "35mm lens at f/2.8 from a standing position in the aisle of a "
        "cryptocurrency trading floor at two in the morning. A long bank of "
        "black desks recedes into soft focus toward a dark glass wall; at the "
        "nearest desks two traders in shirtsleeves are seen from behind and "
        "above, medium small in the frame, one leaning back with a hand on the "
        "back of his neck, the other still typing, both faces turned away and "
        "unreadable. Their monitors are angled away but cast a strong cold "
        "red-to-crimson glow that washes the desk surface, the keyboard and "
        "their forearms, the charts themselves pure defocused red shapes. "
        "Further down the aisle three more figures stand conversing quietly, "
        "silhouetted against the glow of their own desks. Everything else is "
        "dark: charcoal carpet, matte dividers, headset cables, a paper cup "
        "knocked over, an abandoned jacket over a chair back. Overhead lights "
        "are off, so the only illumination is the cold screen light and one "
        "distant warm office lamp, dust in the air, heavy shadow in the "
        "corners. Sombre, tense, unhurried realism, 800-speed colour negative "
        "film look, coarse natural grain, gentle falloff, no HDR. "
        + NO_TEXT
    ),
}


def load_fal_key():
    for path in ("/home/chino/hermes-workspace/studio-api/.env",
                 "/home/chino/video_output/.fal_real"):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
                if path.endswith(".fal_real") and line.strip():
                    raw = line.strip()
                    key = raw.split("|", 1)[1] if "|" in raw else raw
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path, seed=None):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if seed is not None:
        args["seed"] = int(seed)
    print("Generating with fal flux/schnell ...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    url = (result.get("images") or [{}])[0].get("url") or result.get("image")
    if not url:
        print("ERROR: no image url: %s" % result)
        sys.exit(1)
    print("Image URL: %s" % url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded %s size=%s bytes=%d" % (out_path, img.size, len(r.content)))
    return img


def save_capped(img, path):
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=%s" % ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT, os.environ.get("SEED") or None)
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img = img.convert("RGB")
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    save_capped(img, BACKUP)
    print("VERIFY %s dims=%dx%d bytes=%d" % (OUTPUT, W, H, os.path.getsize(OUTPUT)))


if __name__ == "__main__":
    main()
