#!/usr/bin/env python3
"""Generate hero for zs-investor-day-arr-ambition-cyber-valuation-gap-2026 (fal flux/schnell).

Subject: Zscaler (ZS) — enterprise cloud-security / zero-trust company. At its
2026 Investor Day Zscaler raised its long-term ARR ambition while the stock's
valuation sits far below the security-software peer group — an ambition-vs-
valuation gap.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room / transceiver on a lab bench / factory
assembly floor / bank trading floor): a PHOTO-REALISTIC editorial stock
photograph of ENTERPRISE NETWORK SECURITY AT WORK — employees walking through
modern access-control turnstiles / security gates in a bright glass-and-steel
corporate office lobby, one person's hand holding an access badge near a reader,
shallow depth of field, professional lighting, faces not prominent (seen from
side/back or gently out of focus).

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks,
  no legible badges, no signage, no legible screens.
- No identifiable face: seen from side/back or gently out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-zs-investor-day-arr-ambition-hero-20261015.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "zs-investor-day-arr-ambition-cyber-valuation-gap-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no printed markings, no stencilled "
    "characters, no screen text, no legible ID badge, no card-holder writing, "
    "no name badges, no brand names, no manufacturer names, no company names, "
    "no logos, no watermark, no captions, no legible writing of any kind "
    "anywhere in the image. All badges, card holders, turnstile bodies, badge "
    "readers, displays and access-control panels are plain and unmarked with no "
    "readable characters, numbers or symbols. No illustration, no digital art, "
    "no cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no futuristic HUD graphics, "
    "no overlay elements, no augmented-reality graphics, no glowing scanning "
    "beams, no data-center hallway, no server aisle, no server racks, no cable "
    "runs through a building. No prominent face, no portrait, no front-facing "
    "identifiable person: people are seen from behind or from the side, or "
    "gently out of focus."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of employees walking "
        "through modern access-control security turnstiles in a bright "
        "glass-and-steel corporate office lobby. In the soft-focus foreground a "
        "person's hand holds a plain unmarked access badge up close to a slim "
        "brushed-metal badge reader mounted on the turnstile, the badge and the "
        "reader catching clean daylight. Ahead, a few people in business "
        "attire pass through the waist-high glass speed gates, one seen from "
        "behind and one from the side in gentle motion blur, none facing the "
        "camera. The lobby is airy and bright: a tall glazed curtain wall, "
        "steel mullions, a polished stone floor with soft reflections, a ficus "
        "plant and a minimal reception counter dissolving into creamy bokeh far "
        "behind. Clean cool daylight floods in from the glass wall with a warm "
        "ambient fill, honest natural shadows. Shallow depth of field: the hand, "
        "badge and reader are reasonably sharp while the turnstiles and people "
        "fall away into smooth realistic bokeh. Shot on a 50mm lens at f/2, real "
        "optical blur, natural material textures, subtle sensor noise and fine "
        "film grain, honest documentary realism, no glossy CGI sheen, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph taken on a wide lens in the bright "
        "entrance lobby of a modern glass-and-steel corporate office building, "
        "not a render and not computer generated. Waist-height glass speed-gate "
        "turnstiles stand across the frame with slim brushed-metal bodies and "
        "clear glass wings. In the near foreground, deliberately softly out of "
        "focus, a commuter's hand lifts a plain unmarked proximity card toward "
        "the dark reader panel of the gate. Behind the gates, employees in "
        "smart business dress stream through, most seen from behind or in "
        "three-quarter profile, a couple gently blurred by motion, no one facing "
        "the camera. Tall glazed walls and steel columns frame the space, "
        "daylight pouring across a polished terrazzo floor, distant lounge "
        "seating and a plant dissolving into creamy bokeh. Cool clean daylight "
        "from the left with a warm practical bounce, honest natural shadows and "
        "reflections. Shallow depth of field on the badge-and-reader foreground, "
        "background smoothly blurred. 35mm lens at f/2, real optical blur, "
        "believable sensor noise in the shadows, slightly imperfect real-world "
        "exposure and white balance, subtle vignette, tactile realistic "
        "textures, no plastic render look, no digital illustration, no "
        "AI-generated look, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine photograph shot by a professional corporate photographer at "
        "the security checkpoint of a bright modern office tower, not a 3D "
        "visualisation and not an AI render. Modern access-control turnstiles "
        "with brushed stainless-steel pedestals and glass barrier wings line the "
        "lobby. In the sharp-ish foreground, seen from the side, a person's hand "
        "presses a plain unmarked white access card against the dark glossy "
        "reader on the gate, fingertips and the card's blank surface clearly "
        "readable. Through the gates a small queue of employees in business "
        "attire moves into the building, all viewed from behind or the side, "
        "faces turned away or softly out of focus. The lobby behind is open and "
        "light-filled: floor-to-ceiling glass, slim steel mullions, a wide "
        "polished concrete floor reflecting the daylight, blurred seating and "
        "greenery far back. Bright cool daylight with a gentle warm fill, honest "
        "natural contrast, no artificial glow. Shallow depth of field, "
        "background falling off into smooth real bokeh. 50mm lens at f/2.2, real "
        "optical blur, natural grain and sensor noise, slightly uneven real "
        "white balance, subtle vignette, honest imperfect realism, no airbrushed "
        "surfaces, no perfect symmetry, no glossy CGI sheen, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A real photograph made by a documentary photographer inside the "
        "daylit entrance hall of a contemporary glass-and-steel corporate "
        "headquarters, not a render, not CGI. The dominant subject is a row of "
        "modern access-control security gates: low stainless-steel pedestals "
        "with glass swinging barrier panels, one of them open as people pass "
        "through. Close in the foreground and gently out of focus, a woman's "
        "hand holds a plain unmarked access badge against the gate's reader, the "
        "plastic card blank and featureless. Beyond the gates employees walk "
        "away into the building, all seen from behind or from the side, motion "
        "soft, faces not visible or heavily blurred. The lobby is bright and "
        "airy: a great glazed wall with steel framing, abundant daylight, a "
        "polished stone floor with soft reflections, a reception desk and a "
        "potted tree blurred deep in the background. Natural daylight dominant "
        "with a soft warm practical bounce, honest realistic shadows. Shallow "
        "depth of field focused on the badge-and-hand, the rest dissolving into "
        "creamy bokeh. 35mm lens at f/1.8, real optical blur, faint dust in the "
        "air, natural sensor noise and fine film grain, slightly imperfect "
        "exposure, subtle vignette, tactile realistic material textures, no "
        "plastic CGI sheen, no digital art, no illustration, no AI-generated "
        "look, photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
