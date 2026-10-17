#!/usr/bin/env python3
"""Generate hero for panw-ai-labs-security-budget-2026 (fal flux/schnell).

Subject: Palo Alto Networks, cybersecurity platform consolidation, and AI labs
entering the security market. Sector = cyber / enterprise software, so the scene
is PEOPLE AT WORK in a bright modern office — expressly NOT a data center,
server room, server aisle or rack hallway.

Rules:
- PHOTO-REALISTIC stock photograph ONLY. No digital art/neon/render/geometric
  patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD/matrix rain.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks, no
  legible screen content.
- No prominent identifiable face; the person is seen from behind/side or at an
  angle, colleagues softly out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop (16:9).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-panw-ai-labs-security-budget-2026-hero-20261017.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "panw-ai-labs-security-budget-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no whiteboard writing, no "
    "post-it notes with writing, no screen text, no code visible on screens, "
    "no logos, no brand names, no company names, no watermarks, no captions, "
    "no readable writing of any kind anywhere in the image. Every laptop is a "
    "generic unbranded model with a completely plain matte grey or silver lid: "
    "no logo, no apple-shaped mark, no bitten-apple symbol, no emblem, no "
    "sticker and no marking of any kind on any laptop lid or phone. Laptop and "
    "monitor screens are turned away, softly out of focus, or show only a "
    "plain indistinct glow with no legible characters. No illustration, no "
    "digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no glowing lines, no "
    "light trails, no synthwave, no geometric patterns, no futuristic HUD "
    "graphics, no overlay elements, no augmented-reality graphics, no "
    "cybersecurity iconography, no padlock icons, no shields, no circuit "
    "board patterns, no binary code rain, no matrix effect. Absolutely no "
    "data center, no server room, no server aisle, no server racks, no "
    "cable trays, no raised floor with racks. No prominent face, no portrait, "
    "no front-facing identifiable person."
)

PROMPTS = {
    "1": (
        "Professional editorial stock photograph of a cybersecurity analyst "
        "at work in a bright modern corporate office. In the mid-ground a "
        "person in a light blue business-casual shirt sits at a pale wooden "
        "desk, seen from behind and slightly to the side so the face is not "
        "visible, leaning toward an open laptop; their hands rest on the "
        "keyboard. A notebook, a coffee mug and a pair of glasses sit on the "
        "desk. Two colleagues work at desks further back, softly out of focus, "
        "one standing and talking to the other. Floor-to-ceiling windows fill "
        "the left of the frame with bright soft daylight, green trees visible "
        "outside, and the office interior is calm and airy with light grey "
        "walls, pale wood and a few green plants. Shallow depth of field, shot "
        "on a 50mm lens at f/2 on a full-frame camera, real optical blur, "
        "natural skin and fabric texture, honest daylight white balance, "
        "subtle sensor noise and fine film grain, documentary realism, very "
        "high detail, photorealistic, professional corporate stock "
        "photography, 16:9 landscape composition with the subject centred and "
        "no important content at the extreme edges. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken by a corporate photographer inside a bright "
        "open-plan office of a modern software company, not a render and not "
        "computer generated. Three people are at work: in the foreground, "
        "seen over the shoulder from behind, a woman with her hair tied back "
        "in a dark blazer sits at a white desk working on a laptop; beyond "
        "her, two colleagues in shirts stand near a glass partition talking, "
        "one gesturing, both pleasantly blurred by the lens. Large windows on "
        "the right side flood the room with soft natural morning light, "
        "casting gentle shadows across the desk and a small potted plant. "
        "Light oak furniture, muted grey and white interior, a few books and "
        "a water bottle on the desk. Shallow depth of field, 35mm lens at "
        "f/2.2 on a full-frame camera, real optical bokeh, believable natural "
        "contrast, slight imperfection in exposure, subtle vignette, tactile "
        "realistic textures, no plastic CGI sheen, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition with the subject centred. "
        + NO_TEXT
    ),
    "3": (
        "Candid documentary-style office photograph: a small cyber security "
        "team in a bright modern workplace. A man in a checked shirt, viewed "
        "from the side and behind at a three-quarter angle so his face is "
        "mostly hidden, sits at a long shared desk focused on a laptop, one "
        "hand on the trackpad. Next to him a colleague in a grey sweater is "
        "half-turned, mid-conversation, softly out of focus. Behind them tall "
        "windows with daylight and blurred city greenery, plus a glass "
        "meeting room with two distant figures. Warm neutral interior, light "
        "wood, white desks, a couple of plants, papers and a mug. Shot on a "
        "full-frame camera with an 85mm lens at f/1.8, very shallow depth of "
        "field, creamy real optical background blur, natural window light, "
        "honest skin tones, fine grain and light sensor noise, slightly "
        "imperfect real-world framing, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape composition "
        "with clear space around the subject. "
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
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img).convert("RGB")
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
