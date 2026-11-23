#!/usr/bin/env python3
"""Generate hero for anthropic-ipo-ai-lab-economics-2026 (fal flux/schnell).

Subject: Anthropic's record IPO (ticker ANT, Nasdaq, 19 Nov 2026) and the
market's verdict on AI-lab economics — a public-listing / trading-floor story.

MANDATORY SCENE: a modern stock-exchange trading floor on a listing day —
a wide, slightly elevated view across rows of desks and pale glowing monitor
walls, traders as soft out-of-focus silhouettes seen from behind (no faces),
warm overhead light against cool screen glow, one figure in the middle
distance standing and looking up at a large blank glowing display, shallow
depth of field.

Rules:
- PHOTO-REALISTIC professional stock photograph ONLY. No digital art, no
  CGI/3D-render look, no neon, no synthwave, no glowing lines, no geometric
  patterns, no abstract art, no illustration.
- TEXT-FREE: no letters/numbers/logos/tickers/signage. Every screen and every
  sign is plain, blank, or blurred beyond legibility.
- NOT a chip / data-center / server-rack / hallway / cleanroom scene.
- No human faces (seen from behind, soft out of focus silhouettes only).
- Generate 1440x810, finalize 1536x864 center-crop, JPEG under 400KB.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-anthropic-ipo-hero-2026.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "anthropic-ipo-ai-lab-economics-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "Absolutely no text anywhere in the frame: no letters, no words, no "
    "numbers, no digits, no tickers, no stock symbols, no prices, no charts "
    "or graphs, no scrolling market data, no captions or subtitles, no logos, "
    "no brand names, no illuminated signage, no banners, no badges or lanyard "
    "printing, no watermark. Every computer monitor and every wall display is "
    "entirely blank, showing only soft pale glowing white-blue light, plain "
    "and featureless, and any screen further back in the room is blurred past "
    "legibility into abstract pale glow. No digital art, no illustration, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no synthwave, "
    "no geometric patterns, no abstract art, no sci-fi, no data center, no "
    "server racks, no server aisle, no cleanroom, no long empty hallway."
)

PROMPTS = {
    # 1 — the brief, literally: wide slightly elevated view across the floor
    "1": (
        "Photo-realistic professional editorial stock photograph of a modern "
        "stock exchange trading floor on a listing day, shot wide and slightly "
        "elevated from a mezzanine vantage point looking down and across the "
        "room: long rows of dark desks recede in perspective, each desk "
        "carrying banks of thin monitors whose screens are blank and glowing "
        "a pale cool white-blue, the light from the screens washing softly "
        "across desk surfaces and pooling into pale walls of monitor glow "
        "that tile the middle of the room. Traders sit at the desks and stand "
        "between the rows as soft out-of-focus silhouettes seen from behind "
        "and from the side, shoulders and heads readable only as dark shapes "
        "against the screen light, no faces visible anywhere, several of them "
        "in shirtsleeves with dark jackets slung over chair backs. In the "
        "middle distance one figure stands alone, still and upright, back to "
        "the camera, head tilted up, looking at a large blank glowing display "
        "panel mounted high on the far wall, that panel a smooth featureless "
        "rectangle of pale light. Warm tungsten overhead light from a coffered "
        "ceiling falls in soft pools along the near rows, cool blue screen "
        "glow rises from the desks below, the two light temperatures mixing "
        "in the mid-ground. Shallow depth of field: the near desks and a "
        "monitor bezel at the lower left are slightly soft, the standing "
        "figure and the large display are the sharpest part of the frame, and "
        "the far rows dissolve into gentle bokeh. Realistic micro-texture on "
        "desk laminate, chair fabric, monitor plastic and floor carpet, fine "
        "sensor grain, unretouched natural color, muted palette of charcoal "
        "grey, warm amber and pale cool white. Shot on a full-frame camera "
        "with a 35mm lens at f2.0 from a raised position, 16:9 landscape "
        "composition, documentary realism, no staging. " + NO_TEXT
    ),
    # 2 — tighter: the standing figure and the blank display, room behind in bokeh
    "2": (
        "Photo-realistic professional editorial stock photograph of a stock "
        "exchange trading floor on a listing morning, a medium-wide view from "
        "slightly above and behind the room: the focus is on a single trader "
        "standing in the middle distance, seen from behind in three-quarter "
        "view, one hand resting on the back of a chair, head lifted, "
        "motionless, watching a very large blank display panel set into the "
        "far wall that glows a soft even white. He wears a dark suit jacket "
        "and a light shirt, the fabric catching a rim of warm overhead light "
        "along his shoulder, his face entirely turned away and out of sight. "
        "Behind and around him rows of low dark desks run away toward the "
        "back of the hall, each desk crowded with thin monitors showing only "
        "flat pale blue-white glow, no readable content, the monitors "
        "repeating and blurring into soft bokeh as the rows recede. Other "
        "traders appear as dark indistinct silhouettes at the desks, backs "
        "turned, never a face. Warm amber light from recessed ceiling "
        "fixtures above mixes with the cool screen light below, soft shadows "
        "under the desks, a grey carpet floor. Shallow depth of field with "
        "the standing figure and the display's lower edge crisp and "
        "everything nearer and farther falling off gently, realistic "
        "micro-texture in clothing weave and monitor plastic, fine sensor "
        "grain, unretouched natural color, restrained palette of dark "
        "charcoal, warm amber and pale cool white. Shot on a full-frame "
        "camera with an 85mm lens at f1.8, 16:9 landscape composition, "
        "documentary photojournalism realism. " + NO_TEXT
    ),
    # 3 — refined: documentary/news-still texture to kill any CG look, no lit strips
    "3": (
        "Photo-realistic documentary news photograph, taken as a still from a "
        "television report inside the trading floor of a large modern exchange "
        "on the morning of a high-profile public listing: a wide view from a "
        "raised walkway looking out and down across the hall. Rows of dark "
        "desks with ribbed grey worktops stretch away in perspective, each "
        "workstation fitted with a bank of slim monitors angled toward the "
        "traders. Not one monitor shows readable content: every screen is "
        "blank and emitting only a flat pale cool-white glow, dozens of soft "
        "luminous rectangles repeating down the room and dimming into gentle "
        "blur, so the middle of the floor reads as a wall of pale light "
        "against a plain unlit dark ceiling with ordinary recessed downlights, "
        "no illuminated strips, no LED accent bars, no light lines on ceiling "
        "or walls. Traders are at the desks as soft out-of-focus shapes seen "
        "from behind, shoulders and heads dark against the screen light, a few "
        "standing in the aisle with their backs to the lens, no face visible "
        "on any person. In the middle distance one man stands still, back to "
        "the camera, head tilted up, watching a large blank display panel hung "
        "high above the desks, a smooth unbroken field of pale glowing white. "
        "Warm tungsten overhead pockets mix with cool blue screen light rising "
        "off the desks, mild haze in the air, some bloated highlights where "
        "the downlights flare into the lens and faint veiling glare across the "
        "frame. The near foreground is cluttered and slightly soft: the dark "
        "plastic bezel of a monitor at the left edge, a coffee cup, a coiled "
        "cable, a chair back. Shallow depth of field, imperfect asymmetrical "
        "framing with a slightly tilted horizon, visible high-ISO sensor noise "
        "in the shadows, mild corner softness and faint chromatic fringing at "
        "the edges, dust and smudges on the glass. Muted unretouched color, "
        "documentary realism, ordinary mixed indoor light. Shot on a full-frame "
        "camera with a 35mm lens at f2.2, 16:9 landscape composition. " + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
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


def crop_to_ratio(img):
    """Center-crop to 16:9 then resize to 1536x864."""
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


def save_under_cap(img, path):
    """Save JPEG, stepping quality down until under MAX_BYTES."""
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        print(f"  q={q} -> {size} bytes")
        if size < MAX_BYTES:
            return size
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_ratio(img)
    size = save_under_cap(img, OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Mirrored to {BACKUP}  bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
