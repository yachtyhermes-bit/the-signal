#!/usr/bin/env python3
"""Generate hero for crwv-credit-default-risk-bond-selloff-2026 (fal flux/schnell).

Subject: the AI data-center debt selloff of Oct 14-15 2026 — CoreWeave (CRWV)
bond yields blowing past 16% and its credit default swaps past 1,000 basis points.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room / office cubicle farm with legible signage):
a PHOTO-REALISTIC editorial stock photograph of a fixed-income / credit trading
floor at a bank, seen from behind and slightly to the side of the desks — rows
of glowing monitors showing abstract blurred candlestick and line charts in red
and green, a trader's hand on a mouse, a desk phone, a stack of paper, shallow
depth of field, professional lighting, honest documentary realism.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks.
  Blurred abstract charts (shapes only, no legible characters) are fine.
- No identifiable faces: seen from behind, out of focus, or cropped out.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-crwv-credit-hero-20261015.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "crwv-credit-default-risk-bond-selloff-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no ticker symbols, no stock symbols, "
    "no price figures, no axis numbers, no printed markings, no stencilled "
    "characters, no screen text, no legible chart labels, no on-screen writing, "
    "no brand names, no manufacturer names, no bank names, no logos, no "
    "watermark, no captions, no legible writing of any kind anywhere in the "
    "image. All monitors show only abstract blurred shapes — soft red and green "
    "candlestick bodies and line-chart curves with no readable characters, "
    "numbers or words, everything smeared and out of focus. Desk phones, papers, "
    "keyboards, mice and badges are plain and unmarked. Any person is seen only "
    "from behind, as an out-of-focus silhouette, or cropped out of frame — no "
    "identifiable face, no portrait. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no holographic interface, no "
    "augmented-reality overlays, no data-center hallway, no server aisle, no "
    "server racks, no server room, no clean cubicle farm, no legible office "
    "signage."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a fixed-income and credit "
        "trading floor at a large bank, shot from behind and slightly to the "
        "side of a long row of desks receding into the distance. In the sharp "
        "near foreground a trader's hand rests on a computer mouse beside a "
        "scattered stack of paper and a desk phone, a slim keyboard catching "
        "the light. Ahead, rows of glowing monitors fill the room, their screens "
        "showing only soft, deeply out-of-focus abstract candlestick and line "
        "charts in warm red and cool green, every screen dissolving into smooth "
        "creamy bokeh with no readable characters at all. It is dusk: tall "
        "windows along the far wall hold a deep blue evening glow while small "
        "warm desk lamps pool amber light on the work surfaces, a mixed warm-and-"
        "cool balance with honest natural falloff. Shallow depth of field: the "
        "near mouse, hand, paper and keyboard are tack sharp while the desks and "
        "screens behind melt progressively into blur. Shot on a 50mm lens at "
        "f/1.8, real optical blur, natural material textures, subtle sensor "
        "noise and fine film grain, honest documentary realism, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph taken on a fast prime lens inside a "
        "bank's credit trading room, not a render and not computer generated. "
        "Tight over-the-shoulder macro framing from directly behind a seated "
        "trader whose dark, softly out-of-focus silhouette and the back of a "
        "shoulder fill the left of the frame, absolutely no face visible. The "
        "frame looks past the shoulder at a single large monitor filling the "
        "sharp centre-right, its screen glowing with abstract blurred candlestick "
        "and line shapes in red and green, no legible characters anywhere, the "
        "glassy panel reflecting a faint blur of the room. A hand rests on a "
        "computer mouse at the bottom edge, a desk phone and a small stack of "
        "paper sit on the matte desk surface beside it. Warm low-key practical "
        "lighting from nearby desk lamps mixes with the cool glow of the screen, "
        "faint ambient light from other desks far behind. Very shallow depth of "
        "field: the monitor bezel, mouse and near hand are sharp while the "
        "trader's shoulder and the deep background dissolve into heavy bokeh. "
        "50mm lens at f/1.4, real optical blur, subtle lens vignette, believable "
        "sensor noise in the shadows, honest imperfect realism, no glossy CGI "
        "sheen, no plastic render look, no digital illustration, photorealistic, "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine wide-angle photograph of a fixed-income trading floor at "
        "night, the work of a professional editorial photographer, not a 3D "
        "visualisation and not an AI render. A low-key, mostly dark room is lit "
        "almost entirely by the glow of dozens of monitors arranged in long rows "
        "of desks, their screens floating as soft panels of blurred red and green "
        "candlestick and line-chart shapes, no legible text or numbers on any "
        "screen. Dark unlit desks, low partitions, chairs and dark ceiling "
        "structure frame the scene; a couple of out-of-focus human silhouettes "
        "seen from behind sit deep in the rows, no faces visible. A single warm "
        "desk lamp provides a small amber practical in the mid-ground, deep "
        "shadows everywhere else, moody but honest and true to a real night "
        "trading room. Shallow depth of field with the near desks slightly soft "
        "and the middle rows sharp, the far wall melting into darkness. 24mm lens "
        "at f/2, real optical blur, natural grain and sensor noise in the deep "
        "shadows, slightly uneven real white balance, subtle vignette, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A genuine photograph shot on a macro lens by a professional editorial "
        "photographer at a bank's credit trading desk, not a render, not a 3D "
        "visualisation, not computer generated. Close three-quarter view angled "
        "down across a matte dark desk surface: a silver-edged computer mouse and "
        "part of a low-profile keyboard fill the sharp lower foreground, beside "
        "them a small curling paper trading ticket and a slim desk phone, all "
        "plain and completely unmarked, tiny dust and fine wear visible on the "
        "surfaces. Immediately behind, filling the upper frame and glowing "
        "softly, a large monitor shows only abstract blurred candlestick and "
        "line-chart shapes in warm red and cool green, heavily out of focus with "
        "no readable characters, its glass faintly reflecting the room. A "
        "trader's hand rests on the mouse, only the hand and part of a forearm "
        "in frame, no face and no identifiable person visible. Cool screen glow "
        "from above mixes with a gentle warm practical bounce from a desk lamp, "
        "honest natural shadows, low-key but clean. Extremely shallow depth of "
        "field, sharp only on the mouse, keyboard and ticket. Real macro-lens "
        "optical blur, faint dust motes, natural sensor noise and fine film "
        "grain, slightly imperfect real-world exposure and white balance, subtle "
        "vignette, tactile realistic material textures, no plastic CGI sheen, no "
        "glossy render look, no airbrushed surfaces, no perfect symmetry, no "
        "digital illustration, no AI-generated look, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
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
