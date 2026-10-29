#!/usr/bin/env python3
"""Generate hero for ftnt-security-appliance-margin-miss-2026 (fal flux/schnell).

Subject: Fortinet (NASDAQ: FTNT) — the cybersecurity company behind FortiGate
firewalls. Q3 2026 earnings: revenue and EPS beat, but hardware gross margin
slipped, and the stock fell ~22-25%. The story is the appliance business —
the box that gets sold, shipped, racked and renewed — not the silicon story
we ran on Sept 12.

SHIPPED: ATTEMPT=3 (third and final allowed generation). A photo-realistic,
low-angle documentary photograph near the floor of a bright empty warehouse:
an open plain unprinted cardboard carton on grey concrete with three brand-new
matte-black 1U rack-mount network security appliances, one still in plastic
wrap leaning half out of the box, long warm late-afternoon daylight raking
through the open dock door, dust in the air, shallow depth of field. The
"refresh shipment" idea — the appliance business rather than the silicon.

Attempt history (hard cap 3):
  1 = technician racking an appliance in a bright closet. Rejected: readable
      port text ("USER WLAN") on adjacent rack gear + malformed gloved fingers.
  2 = tight bezel/connector macro on a grey wall. Rejected: neon-leaning warm/
      cool contrast read as futuristic render, garbled glyphs beside the ports.
  3 = warehouse carton + appliances. SHIPPED after removing one faint
      letterform on the top unit's silver panel via a local texture clone
      (verified: tesseract clean at psm 3/4 on a 2x upscale, vision QA reports
      no readable text at display size).

Deliberately NOT: a data center hallway / server aisle / rack row, a SOC
monitor wall, a bare PCB macro of a chip (that was the Sept 12 hero), a
chip-fab cleanroom, a silicon wafer macro, or any rocket/drone/space imagery.

Rules:
- PHOTO-REALISTIC stock photograph ONLY. No digital art/illustration/cartoon/
  3D render/neon/glowing lines/geometric patterns/abstract art.
- TEXT-FREE: no letters/numbers/logos/brand names/labels/serial plates/
  signage/screens/monitors/UI/code/dashboards/paper/watermarks anywhere.
- Generate 1440x810, finalize 1920x1080 center-crop.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-ftnt-margin-miss-hero-20261029.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ftnt-security-appliance-margin-miss-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely smooth, plain and unmarked: no text, no "
    "letters, no numbers, no serial numbers, no barcodes, no etched or "
    "engraved markings, no labels, no stickers, no plaques, no nameplates, "
    "no decals, no stencils, no logos, no brand names, no model names, no "
    "signage, no posters, no screens, no monitors, no displays, no laptops, "
    "no phones, no tablets, no keyboards with writing, no UI, no computer "
    "interfaces, no code, no dashboards, no whiteboards with writing, no "
    "paper documents, no cardboard printing, no tape with writing, no "
    "watermark, no captions, no illustration, no digital art, no cartoon, "
    "no 3D render, no neon, no glowing lines, no geometric patterns, no "
    "abstract art."
)

PROMPTS = {
    # (a) technician racking an appliance — primary pick
    "1": (
        "Photo-realistic professional stock photograph, low three-quarter "
        "angle, of a technician's hands in plain blue nitrile gloves guiding "
        "one plain matte-black 1U rack-mount network security appliance along "
        "its metal rail into a shallow open equipment chassis inside a small "
        "bright corporate wiring closet, the appliance front bezel smooth and "
        "unmarked with a neat row of tiny green and amber status LEDs and two "
        "empty square port openings, a bundle of thin fiber patch cables with "
        "small clear LC connectors draped softly out of focus in the "
        "foreground, matte grey perforated metal panels and plain plastic "
        "cable managers in the softly blurred background, warm late-afternoon "
        "daylight spilling through an open door from camera left and mixing "
        "with cool bounce light from the pale wall, gentle soft shadows, "
        "shallow depth of field with the appliance edge and the gloved "
        "fingertips tack sharp and the background dissolving into smooth "
        "creamy bokeh, natural realistic materials and skin texture, "
        "photorealistic, high detail, shot on a 50mm lens at f2.0, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    # (c) front bezel macro, no hands, single appliance, plain background
    "2": (
        "Photo-realistic close-up stock photograph, low three-quarter angle, "
        "of one plain matte-black rack-mount enterprise network security "
        "appliance filling most of the frame, its front bezel completely "
        "smooth, featureless and unmarked apart from a single neat horizontal "
        "row of small round status LEDs lit soft green and amber, two square "
        "fiber port openings on the right with one clear slim fiber connector "
        "already seated and its thin cable curving away, the other ports open "
        "and dark, plain brushed aluminium rack ears at the edges, the entire "
        "appliance surface free of any printed legends, port labels or "
        "iconography, behind it only a plain out-of-focus painted grey wall "
        "with no other equipment, no rack of other devices, warm natural "
        "window light from camera left raking across the matte finish along "
        "with the faintest cool fill from the right, dust on the metal, very "
        "shallow depth of field with the front edge of the bezel and the "
        "seated connector razor sharp, shot on a full-frame camera at 85mm "
        "f2.0, subtle sensor noise and natural lens falloff, unretouched "
        "documentary realism, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # (b) unpacking a refresh shipment, no hands, no people
    "3": (
        "Photo-realistic documentary stock photograph, low camera angle near "
        "the floor, of an open plain unprinted brown corrugated cardboard box "
        "standing on a smooth grey concrete floor with three brand-new plain "
        "matte-black 1U rack-mount network security appliances still in their "
        "clear plastic wrap stacked beside it, one appliance leaning against "
        "the box edge half out of the carton turned so only its blank smooth "
        "side and blank rear vents face the camera, no people, no hands, no "
        "visible human anywhere in the frame, all surfaces smooth and free of "
        "printing, soft warm late-afternoon daylight pouring in from a wide "
        "open warehouse door behind and laying long gentle shadows across the "
        "concrete, a plain pale grey wall and a bare metal shelving upright "
        "far out of focus behind, dust motes drifting in the light, shallow "
        "depth of field with the nearest appliance edge and cardboard flap "
        "tack sharp and the warehouse beyond melting into smooth creamy "
        "bokeh, shot on a full-frame camera at 35mm f1.8, natural film grain "
        "and true-to-life materials, slightly uneven exposure, unretouched "
        "editorial realism, 16:9 landscape composition. "
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
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
