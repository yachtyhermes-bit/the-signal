#!/usr/bin/env python3
"""Generate hero for visa-agentic-payments-network-moat-2026 (fal flux/schnell).

Subject: Visa (NYSE: V) — the payments network that is building the identity and
trust layer for AI agents that buy things. Article thesis: the moat is the
guarantee (authorization, fraud scoring, chargebacks, dispute arbitration), and
Visa is turning that into the protocol layer for machine payments.

Scene chosen: a city transit station fare-gate line at evening rush hour — the
contactless tap that Visa's network clears 900 million times a day. Human,
documentary, kinetic, and deliberately NOT a data centre.

Deliberately DISTINCT from recent Signal heroes that must not repeat:
  (1) crcl-stablefx (20260926): retail checkout close-up at a counter.
  (2) crwv-credit (20260929): AI data-centre campus under construction at dusk.
  (3) amat-hbm-packaging (20260928): semiconductor fab cleanroom interior.
  (4) amkor-packaging (20260924): die-attach machine / package macro.
  (5) cifr-barber-lake (20260926): transmission tower / substation at dusk.
  (6) pl-suncatcher (20260925): spacecraft in orbit.
  (7) moat-test (20260927): ship canal lock at golden hour.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph ONLY. No digital art, neon, render, cartoon,
  CGI, glowing lines, geometric patterns, HUD, illustration.
- TEXT-FREE: transit stations are full of signage, advertising, destination
  boards and route numbers — all explicitly forbidden.
- FACES NOT VISIBLE: seen from behind, out of focus, motion-blurred.
- NO data-centre hallway / server aisle / rack composition (banned).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-visa-agentic-hero-20260929.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "visa-agentic-payments-network-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no numbers, no "
    "digits, no signage, no station names, no advertising posters, no billboards, no route "
    "numbers, no destination boards, no departure screens, no timetables, no maps, no arrows, "
    "no warning labels, no safety notices, no brand names, no logos, no company marks, no "
    "ticket machines, no payment terminal branding, no card logos, no printed words anywhere, "
    "no watermark, no signature, no captions. All panels, walls, pillars and floors are plain "
    "and unmarked: bare brushed steel, plain grey concrete, plain painted metal, plain dark "
    "glass. No illustration, no digital art, no cartoon, no 3D render, no CGI, no video-game "
    "look, no neon, no synthwave, no glowing lines, no light trails, no geometric patterns, "
    "no futuristic HUD graphics, no holograms, no augmented-reality overlays, no charts, no "
    "graphs, no diagrams. Not a data-center hallway, no server aisle, no server racks, no "
    "cable runs, no rack of network equipment, no cleanroom, no office interior."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a render: the fare-gate "
        "line of a big-city transit station at evening rush hour, shot from just behind the "
        "queue. The dominant foreground subject is a single bare hand holding a plain "
        "smartphone flat against the dark reader disc on top of a fare gate, the disc faintly "
        "lit, the phone screen dark and blank. The gate itself is plain brushed stainless "
        "steel with a blank dark glass panel and no markings of any kind. Behind that one "
        "sharp hand, a compressed line of commuters recedes into shallow focus: the backs of "
        "heads, shoulders in plain coats and jackets, one person in a plain coat reaching "
        "toward the next gate, every face turned away from camera and softly out of focus, "
        "with motion blur on the nearest of them from the long exposure. The floor is plain "
        "grey concrete with soft reflections of the reader lights, and the ceiling above is "
        "plain ribbed metal with a row of simple unlit luminaires. Warm-white station lighting "
        "from above and behind, cool light spilling from the reader discs, nothing else "
        "self-lit, no neon. Shot on a 50mm lens at f/2 from a standing eye-level viewpoint "
        "half a step behind the queue: the hand and the reader disc tack sharp, the crowd "
        "smoothly blurred behind, strong one-directional perspective down the gate line. "
        "Natural sensor noise, very slight film grain, subtle lens vignette, honest realistic "
        "steel, glass and concrete texture, photorealistic, extremely detailed, professional "
        "documentary photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "A real photograph, shot on a real camera, not computer generated: a commuter tapping "
        "a phone on a contactless reader at a city transit fare gate during the evening rush, "
        "photographed from behind and slightly to the side of their shoulder so no face is "
        "visible. The hand and the phone held against the lit reader disc are the sharp focal "
        "point in the left foreground; the gate is plain unmarked brushed steel with a blank "
        "dark glass side panel. Beyond the gate a blurred tide of commuters moves away from "
        "camera through a plain concrete concourse, all seen from behind, shoulders and backs "
        "only, faces turned away and lost in motion blur from the slow shutter. Above them a "
        "plain ribbed metal ceiling with simple unlit light fittings; beneath, plain grey "
        "concrete polished by hundreds of thousands of footsteps, catching long soft "
        "reflections of the reader lights and the warm overhead lighting. Cool light from the "
        "reader discs, warm-white light from the ceiling, gentle contrast, nothing else "
        "self-lit, no neon and no glowing lines. Shot on a 35mm lens at f/2 with the near hand "
        "tack sharp and the concourse falling into soft blur, honest documentary framing, "
        "natural sensor noise, slight film grain, subtle vignette, realistic steel, glass and "
        "concrete textures, no CGI sheen, no perfect symmetry, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph taken with a real camera: an overhead "
        "view looking down onto a row of plain contactless fare gates in a busy city transit "
        "station at rush hour. One traveller in the foreground, seen from directly above and "
        "behind so the face is hidden, holds a dark smartphone flat on the glowing reader of "
        "the nearest gate; that phone, hand and reader are the crisp centre of the frame. The "
        "gate row recedes diagonally across the frame as plain unmarked brushed-steel "
        "housings with blank dark panels. Around them a scattered crowd of commuters crosses "
        "the plain grey concrete floor in every direction, all seen from above with faces "
        "hidden by angle, hats and motion blur, some sharp, most drawn into soft movement "
        "streaks. Polished concrete carries soft smears of reflected light; the ceiling is out "
        "of frame. Even warm-white overhead lighting with cool light from the reader discs and "
        "nothing else emitting light, no neon, no glowing lines, no light trails. Shot on a "
        "35mm lens at f/4 from a raised viewpoint looking down at roughly forty-five degrees, "
        "the near tap tack sharp and the crowd softening with distance and motion. Natural "
        "sensor noise, very slight film grain, subtle vignette, realistic steel, glass and "
        "polished concrete texture, no CGI look, no digital illustration, photorealistic, "
        "extremely high detail, professional editorial photography, 16:9 landscape "
        "composition. " + NO_TEXT
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


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
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
