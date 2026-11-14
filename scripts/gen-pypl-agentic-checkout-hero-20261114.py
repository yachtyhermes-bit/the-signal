#!/usr/bin/env python3
"""Generate hero for pypl-agentic-commerce-checkout-moat-2026 (fal flux/schnell).

Subject: PayPal (PYPL) and how AI agents are changing online checkout — the
payments button at the moment of sale. The image is a real, human contactless
payment moment: a customer tapping a phone on a card terminal at a small shop
counter. Warm available light, shoppers softly out of focus behind.

Rules:
- Photo-realistic professional stock photograph ONLY. No illustration, digital
  art, neon, synthwave, glowing lines, geometric patterns, abstract art.
- TEXT-FREE: no readable characters, no brand names, no logos, no signage.
- NO data center / server aisle / rack composition.
- Faces not the subject (turned away / out of focus), hands and terminal sharp.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-pypl-agentic-checkout-hero-20261114.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "pypl-agentic-commerce-checkout-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

CLEAN = (
    "Photo-realistic professional stock photograph. Realistic photo, shallow depth of field, "
    "professional lighting. Completely clean and unmarked: no text, no letters, no numbers, no "
    "words, no signage, no price tags, no menus, no labels, no brand names, no logos, no card "
    "network marks, no watermark, no signature, no caption. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no painting, no neon, no synthwave, no glowing lines, no "
    "light trails, no geometric patterns, no abstract shapes, no HUD overlays, no holograms, no "
    "charts or graphs. Not a data center, no server aisle, no server racks, no cable runs, no "
    "office interior, no cleanroom."
)

SUBJECT_1 = (
    "a customer standing at the counter of a small independent coffee shop, holding a plain "
    "dark smartphone flat against the top of a small black contactless card terminal on the "
    "counter, mid-tap, the terminal angled toward camera and its small screen softly lit with "
    "an unreadable glow. Seen from just behind and to the side of the customer's shoulder: the "
    "hand, phone edge and terminal are the sharp centre of the frame, the customer's face and "
    "shoulder turned away and falling out of focus. Behind them, two other customers wait "
    "softly blurred near a wooden counter, faces indistinct. The counter is warm dark wood with "
    "a few plain unmarked ceramic cups; a plain espresso machine sits softly out of focus to "
    "the left. Warm late-afternoon window light from the right, gentle falloff into warm shadow, "
    "nothing self-lit, no neon. Shot on a 50mm lens at f/2, tack sharp on the tap, creamy "
    "background blur, natural sensor noise, slight film grain, subtle vignette, honest wood, "
    "ceramic, glass and skin texture. 16:9 landscape composition."
)

SUBJECT_2 = (
    "a close-up photograph at a small boutique shop counter of one hand tapping a phone on a "
    "contactless payment terminal, and the shopkeeper's hand resting on the counter just beside "
    "it. The phone — plain, matte, screen dark — is pressed flat against the terminal's top "
    "panel; the terminal is plain black plastic with a small softly lit screen showing an "
    "unreadable glow. Both hands are the sharp subject, framed tight and slightly above counter "
    "level. The shopkeeper stands beyond the terminal, out of focus, only a soft blurred "
    "cardigan and shoulder visible, no face. Behind, a warmly lit boutique interior dissolves "
    "into blur: plain wooden shelving, folded fabric, a soft pool of daylight from a window at "
    "the left. Warm available light with cool daylight mixing, gentle shadows, nothing self-lit. "
    "Shot on an 85mm lens at f/1.8 from counter height, extremely shallow depth of field, "
    "razor-sharp on the two hands and the terminal, background turned to smooth bokeh, natural "
    "sensor noise, slight film grain, subtle vignette, realistic skin and plastic texture. 16:9 "
    "landscape composition."
)

SUBJECT_3 = (
    "a close, warm photograph at the counter of a small neighbourhood bakery: one customer's "
    "hand holds a black smartphone with its back pressed flat down onto the black contactless "
    "card terminal standing on the pale wooden counter, the phone resting directly on the "
    "terminal, the two devices touching, mid-tap. The phone and terminal are the crisp centre "
    "of the frame, the hand relaxed on the phone's edge, the customer's sleeve and turned-away "
    "shoulder soft at the left edge of the frame with the head out of focus. A plain paper bag "
    "of bread and a few softly blurred unwrapped loaves sit on the counter beside the terminal. "
    "Warm morning light comes through the shop window from the right, catching the pale wood and "
    "the paper bag, gentle falloff into warm shadow, nothing self-lit, no neon. Shot on a 50mm "
    "lens at f/2 from a three-quarter angle at counter height, tack sharp on the phone and "
    "terminal where they touch, smooth background blur, natural sensor noise, slight film "
    "grain, subtle vignette, realistic wood, paper, plastic, glass and skin texture. 16:9 "
    "landscape composition."
)

PROMPTS = {
    "1": "Professional stock photograph of " + SUBJECT_1 + " " + CLEAN,
    "2": "Professional stock photograph of " + SUBJECT_2 + " " + CLEAN,
    "3": "Professional stock photograph of " + SUBJECT_3 + " " + CLEAN,
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
    print("PROMPT: " + PROMPTS[ATTEMPT])
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = crop_to_16x9(img).convert("RGB")
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
