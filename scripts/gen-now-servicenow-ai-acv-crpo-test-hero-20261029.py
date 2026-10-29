#!/usr/bin/env python3
"""Hero for now-servicenow-ai-acv-crpo-test-2026 (fal flux/schnell).

Subject: ServiceNow beat on subscription revenue and raised FY guidance, but
the stock fell ~26% in one session -- worst day ever -- as Q4 cRPO growth
guidance decelerated to 18.5% and adjusted EPS missed by two cents. Theme:
enterprise software's AI monetization test. The market stopped paying for AI
promises and started demanding proof.

Scene: a late-afternoon enterprise software office. Dashboards exist but are
never readable; the human mood is "the quarter went sideways" -- quiet,
tired, contained disappointment rather than drama.

NO text anywhere (no letters, numerals, logos, signage, screen UI,
watermarks). NO data center / server room / rack aisle / cable spaghetti
(overused). No neon, no glowing lines, no geometric patterns, no abstract or
digital art, no 3D render. Strictly photo-realistic editorial photography.

SHIPPED: ATTEMPT=1. Wide 35mm shot of a man in a pale blue shirt standing at a
floor-to-ceiling glass wall over a grey city, cold paper cup abandoned on the
sill, the open-plan floor behind him in soft bokeh with two colleagues seated
and monitors turned away. Vision QA: no text/logos anywhere, photo-like, no
neon/racks. Minor known flaw: the defocused background figure's hand merges
into his jaw at 100%; invisible at display size.

Attempt history (hard cap 3):
  1 = window figure + floor bokeh. SHIPPED.
  2 = empty boardroom after the meeting, figure far off at the glass. Rejected:
      clear Apple logo on a closed laptop lid, merged fingers, waxy table.
  3 = empty dusk floor, one backlit silhouette at the glass. Rejected: Apple
      logo on a laptop (prompt said none) + blurred print on a sheet of paper.

Hard cap: 3 generations.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-now-servicenow-ai-acv-crpo-test-hero-20261029.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "now-servicenow-ai-acv-crpo-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864
MAX_BYTES = 500_000

NO_TEXT = (
    "Absolutely no text anywhere in the image: no words, no letters, no "
    "numerals, no logos, no branding, no signage, no posters, no labels, no "
    "captions, no screen text, no user interface elements, no document text, "
    "no handwriting, no watermarks, no glyphs. Every monitor and laptop screen "
    "is either dark, facing away from the camera, or so heavily defocused that "
    "it shows only soft diffuse colour with no readable or unreadable writing "
    "of any kind. No data center, no server room, no server racks, no server "
    "aisle, no cable spaghetti. No neon, no synthwave, no glowing lines, no "
    "laser effects, no abstract shapes, no geometric patterns, no 3D render, "
    "no CGI. Strictly photo-realistic editorial stock photography, natural "
    "film grain, true-to-life skin and fabric texture."
)

PROMPTS = {
    # 1: one person at the glass wall over the city, floor behind in bokeh
    "1": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "35mm lens at f/2.0 on a full-frame camera. A late-afternoon enterprise "
        "software office on the eighteenth floor. In sharp focus, a man in his "
        "early forties in a plain pale blue shirt with the sleeves rolled up "
        "stands with his back three-quarters to the camera at a floor-to-ceiling "
        "glass wall, one hand resting flat on the mullion, a paper cup of cold "
        "coffee forgotten on the low sill beside him, his shoulders slightly "
        "lowered, looking out over a dense grey city of mid-rise towers under a "
        "soft overcast late-day sky. Behind him, thrown far out of focus into "
        "smooth creamy bokeh, the open-plan floor: two colleagues sitting at "
        "desks with their monitors turned away from the camera, one leaning back "
        "with a hand over their eyes, a few empty chairs pushed back at odd "
        "angles, low felt divider panels and a scatter of notebooks lying closed. "
        "Cool blue-grey daylight from the window rakes across the carpet and "
        "mixes with warm overhead downlights reflected in the glass, gentle "
        "shadows, dust in the air. Quiet, deflated, documentary realism, no one "
        "looking at the lens. "
        + NO_TEXT
    ),
    # 2: the boardroom after the meeting broke up — empty, window figure far off
    "2": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "28mm lens at f/2.0 on a full-frame camera from the corner of a modern "
        "corporate boardroom, camera at table height and slightly tilted up. The "
        "meeting is over and everyone has gone: a long pale oak conference table "
        "runs away from the lens, six chairs pushed back and left at awkward "
        "angles, four closed matte-grey laptops flat on the table, one crumpled "
        "grey jacket slung over a chair back, a single half-empty water glass "
        "catching a highlight, a phone lying face-down. No paper, no folders, no "
        "documents anywhere. Far away at the head of the room, small in the frame "
        "and soft with distance, one person stands with their back fully to the "
        "camera at a floor-to-ceiling window, one hand on the mullion, looking "
        "down and out over a dense grey city in the late afternoon, too far away "
        "to read any detail of their face or hands. Long soft amber daylight from "
        "the windows lays diagonal bands across the empty table and the dark "
        "carpet, the far wall plain warm grey with no artwork, ceiling downlights "
        "off. Quiet, emptied, faintly deflated documentary realism, the abandoned "
        "room as the subject, natural film grain, true-to-life materials. "
        + NO_TEXT
    ),
    # 3: the floor emptied out at dusk, one silhouette at the glass
    "3": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "35mm lens at f/2.8 on a full-frame camera, standing eye level at one end "
        "of a modern software company's open-plan floor at dusk. Camera looks "
        "down a long pale carpeted aisle between two clusters of low desks toward "
        "a wide wall of floor-to-ceiling windows. Every monitor on the desks is "
        "switched off, dark grey and blank, angled away or seen edge-on; every "
        "chair is empty and pushed back at a slightly different angle; one grey "
        "wool coat is hung over a chair back, a ceramic mug and a pair of "
        "headphones sit on one desk, a single warm desk lamp is still on and "
        "spills an amber pool across the pale wood. There are no laptops, no "
        "paper, no documents, no whiteboard, and nothing printed anywhere on the "
        "furniture. At the far end, small in the frame and fully backlit by the "
        "bright dusk sky, a lone person stands with their back to the camera at "
        "the glass, entirely in silhouette, no facial features, no readable "
        "hands, just a dark quiet shape against the window with one arm hanging "
        "at their side. Outside the glass, a soft grey-blue city of mid-rise "
        "blocks under a fading overcast sky. Cool blue dusk from the windows "
        "against the single warm lamp, long soft shadows down the aisle, dust in "
        "the air, gentle highlight falloff in the corners, shot on 400-speed "
        "colour negative film, fine natural grain, slightly uneven exposure, "
        "unretouched documentary realism, no HDR, no clarity boost. "
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
    for q in (92, 90, 88, 86, 84, 82, 80):
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
