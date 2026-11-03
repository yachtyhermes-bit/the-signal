#!/usr/bin/env python3
"""Hero for meta-first-bond-sale-ai-debt-2026 (fal flux/schnell).

Subject: Meta tapping the corporate bond market for $20B+ to fund AI
infrastructure — the moment a mega-cap tech borrower goes to the credit
markets.

Scene: a bank bond trading / debt underwriting desk at blue hour. Traders at
multi-monitor desks, bond price ladders glowing green and red as soft bokeh,
one trader in sharp focus reading a printed term sheet on paper. Moody
blue-hour trading-floor lighting, shallow depth of field.

NO text, no logos, no readable screens, no data-center interior, no server
aisle, no neon, no digital art, no CGI look.

HARD CAP: 3 fal flux/schnell generations (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-meta-bond-sale-hero-20261103.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "meta-first-bond-sale-ai-debt-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "Absolutely no legible text anywhere in the image: no readable words, no "
    "letters, no headlines, no signage, no labels, no brand names, no logos, "
    "no corporate marks, no watermarks, no captions, no signatures. All "
    "monitor content is soft blurred columns of light and colour only, with "
    "no recognisable characters or tickers; the printed document in the "
    "photograph shows only faint grey tabular rows and blank ruled lines that "
    "stay out of focus and unreadable. Not an illustration, not digital art, "
    "not a 3D render, not CGI, not matte painting, no neon, no synthwave, no "
    "glowing light trails, no geometric patterns, no abstract shapes, no data "
    "visualization graphics, no HUD overlays, no collage, no split screen. Not "
    "a data center, not a server room, not a server aisle, not server racks. "
    "Strictly photo-realistic editorial stock photography with true-to-life "
    "materials, real lens optics, natural film grain and honest atmospheric "
    "haze."
)

PROMPTS = {
    # 1: medium-wide down the aisle of desks, one trader reading paper
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "full-frame camera with a 50mm lens wide open at f/1.8, from standing "
        "eye level in a large investment bank bond trading floor late in the "
        "day. One trader in his forties sits at a broad black desk in the left "
        "third of the frame, in sharp focus: white shirt sleeves rolled to the "
        "forearm, loosened dark tie, reading a printed document held in both "
        "hands, head tilted down in concentration, a pen between his fingers. "
        "On the desk in front of him, a keyboard, a cold cup of coffee, a "
        "spiral-bound printed document, a desk phone with a coiled cord and "
        "two black monitors on articulated arms, their screens turned slightly "
        "away so they read only as soft glowing grids of pale green and red "
        "cells falling quickly out of focus. Rows of identical desks recede "
        "behind him to the right, each with its own cluster of monitors "
        "emitting dim green and amber light, a handful of other traders "
        "reduced to blurred shoulders and the backs of chairs, nobody's face "
        "identifiable. Cool overhead lighting from a low luminous ceiling "
        "mixes with the warm spill of desk lamps, so the room sits in a moody "
        "blue-grey half light with pools of amber on the desktop surfaces. "
        "Behind the desks, a wall of dark glass windows shows the last of the "
        "evening sky and a scatter of out-of-focus city lights. Shallow depth "
        "of field, the background dissolving into soft bokeh circles of green "
        "and red, clean falloff on the trader's near shoulder. Natural sensor "
        "noise, fine film grain, gentle vignette, matte low-contrast colour "
        "grade, no HDR. Photorealistic, extremely high detail, authentic "
        "documentary editorial photography. " + NO_TEXT
    ),
    # 2: tighter over-the-shoulder three-quarter on the trader and his paper
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, full-frame "
        "camera, 85mm lens at f/1.4, three-quarter over-the-shoulder view of a "
        "bond trader at his desk on a bank trading floor at blue hour. The "
        "trader, a woman in her late thirties with short dark hair, a pale "
        "grey shirt and a headset resting around her neck, fills the right "
        "half of the frame in crisp focus, angled toward the left, studying a "
        "printed term sheet she holds up in one hand while her other hand "
        "rests flat on the desk beside a stack of printed pages. Her "
        "expression is intent and tired, brow slightly furrowed, lips parted "
        "as if mid-thought; a strand of hair has come loose. The paper in her "
        "hand is lit from above and slightly in front, its surface a soft "
        "grey-white with faint rows of tabular figures that blur into "
        "illegibility toward the top edge. In the near foreground, out of "
        "focus and running along the bottom of the frame, the edge of a "
        "second desk with a black keyboard, a wired mouse, a lanyard and a "
        "paper cup. Directly behind her, two large monitors stand at an angle, "
        "their screens showing dense price ladders as columns of softly "
        "blurred green, teal and red blocks, bright enough to rim-light the "
        "side of her face and hair in cool cyan; a third smaller screen sits "
        "lower with a pale wash of blue. Farther back the trading floor falls "
        "away into darkness dotted with more glowing screens and the blurred "
        "silhouettes of two colleagues standing and talking, their voices "
        "implied only by posture. Moody low-key lighting, deep shadows, cool "
        "blue ambient from the ceiling panels, warm amber kicker from a desk "
        "lamp at the left edge. Extremely shallow depth of field, background "
        "rendered as creamy bokeh discs, natural skin texture with visible "
        "pores and fine wrinkles, real fabric folds, faint lens flare from a "
        "monitor edge, fine film grain, subtle vignette, restrained colour. "
        "Photorealistic, extremely high detail, authentic editorial "
        "photojournalism. " + NO_TEXT
    ),
    # 3: wide, room-scale, one lit desk island in a dark floor
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "full-frame camera with a 35mm lens at f/2, from a slightly elevated "
        "position at the end of a bank bond trading floor after the close. The "
        "room is large and mostly dark, arranged in long islands of desks "
        "running away from the camera, each desk a slab of pale grey laminate "
        "crowded with two, three, sometimes four flat monitors on tall arms. "
        "One desk island in the middle-left of the frame is still occupied and "
        "lit: a single trader in a white shirt with sleeves rolled up sits "
        "with his back half turned, hunched over a printed document spread "
        "flat on the desk, one hand pressed to his forehead, the other "
        "steadying the pages, a desk lamp throwing a warm cone of light across "
        "the paper and his forearms so the paper glows warm cream against the "
        "cool room. His monitors throw pale green and red light onto his shirt "
        "and the desktop, their content reduced at this distance to soft grids "
        "of coloured rectangles. All around him the other desks are empty or "
        "nearly so, a few monitors left on showing dim blue standby glow, "
        "chairs pushed back at odd angles, jackets hung over chair backs, "
        "scattered paper, a plastic water bottle catching a highlight. The "
        "ceiling above is a grid of recessed panels, most of them switched "
        "off, a few still burning cold white and creating long soft shadows "
        "down the aisles. In the far background a wall of dark glass shows the "
        "blue hour sky over a city, and a scatter of distant window lights "
        "blurs into bokeh. Moody low-key blue-hour exposure, deep shadow, "
        "pockets of warm tungsten and cool screen glow, believable "
        "institutional wear on carpet and desk edges. Natural atmospheric "
        "perspective, slight haze in the room, natural sensor noise, fine film "
        "grain, gentle vignette, no HDR, no saturation push. Photorealistic, "
        "extremely high detail, authentic editorial architectural photography "
        "of a working financial floor. " + NO_TEXT
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
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=%s (hard cap 1-3)" % ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT, os.environ.get("SEED") or None)
    if img.size != (W, H):
        resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
        img = img.resize((W, H), resample)
    img = img.convert("RGB")
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    save_capped(img, BACKUP)
    print("VERIFY %s dims=%s bytes=%d" % (OUTPUT, img.size, os.path.getsize(OUTPUT)))


if __name__ == "__main__":
    main()
