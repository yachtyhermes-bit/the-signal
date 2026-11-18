#!/usr/bin/env python3
"""Generate hero for tencent-ai-capex-free-cash-flow-2026 (fal flux/schnell).

Subject: Tencent Q3 2026 results / the cost of AI infrastructure. Human,
street-level scene: a Chinese street-market vendor taking a QR/mobile payment
from a customer's phone at dawn. Deliberately NOT a data centre, NOT a server
aisle, NOT a cleanroom, NOT abstract/neon.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-tencent-ai-capex-hero-20261118.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "tencent-ai-capex-free-cash-flow-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "The scene contains no writing at all: no text, no letters, no numbers, "
    "no Chinese characters, no words, no signage, no shop signs, no price "
    "tags, no labels, no stickers, no branded packaging, no logos, no "
    "watermark, no captions, no legible phone interface, no readable screen "
    "content. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no synthwave, no glowing geometric lines, no light trails, "
    "no HUD graphics, no holograms, no abstract patterns, no charts or graphs. "
    "Not a data centre, no server room, no server racks, no server aisle, no "
    "cleanroom, no fab, no glowing fibre optics."
)


PROMPTS = {
    "1": (
        "Professional stock photograph, real documentary photograph, shot on a "
        "35mm lens at f/2 on a full-frame camera, 16:9 landscape, handheld, "
        "available early-morning light, not a render and not CGI: a busy "
        "outdoor street food market in a southern Chinese city just after "
        "sunrise. In the sharp focal plane at the centre-right of the frame, a "
        "middle-aged market vendor — a woman in a faded cotton apron over a "
        "plain work shirt, sleeves rolled, hair tied back, face partly turned "
        "away from camera and softly out of focus — stands behind a low "
        "stainless-steel stall counter piled with green vegetables and a few "
        "loose spring onions, one hand still resting on a worn wooden crate. "
        "In the near foreground left, a customer's hand and forearm reach into "
        "frame holding a plain dark smartphone out toward her at chest height, "
        "the phone tilted so its screen faces the vendor and away from the "
        "camera; the screen is just a soft pale wash of light with no legible "
        "content. Beside the vendor's hand on the counter sits a small plain "
        "matte plastic payment stand, unmarked, dulled with use. Steam rises "
        "faintly from a steel pot at the left edge. The vendor's stall is one "
        "of a receding row: pale canvas awnings, bare steel poles, stacked "
        "plastic crates, wet concrete underfoot with a dark puddle reflecting "
        "the sky, all softening into bokeh down the street. Early low morning "
        "sun rakes in from the right, warm gold on the vendor's shoulder and "
        "the vegetables, cool blue shadow filling the alley behind, thin haze "
        "in the air. Shallow depth of field with real optical bokeh, natural "
        "sensor noise, fine film grain, slightly off-centre casual framing, "
        "true-to-life muted colour, honest and unglamorous. " + NO_TEXT
    ),
    "2": (
        "Professional stock photograph, realistic documentary street "
        "photography, shot on a 50mm lens at f/2.2, 16:9 landscape, available "
        "dawn light: a small roadside breakfast stall on a narrow Chinese city "
        "street in the early morning. The frame is close and human-scaled. In "
        "the right half, a vendor in a plain grey sweater and a cloth apron "
        "leans slightly forward over a hot griddle, seen from the side at a "
        "three-quarter angle, face in soft shadow under a plain canvas awning "
        "and not clearly visible; his free hand holds a folded paper wrapper. "
        "In the left foreground, sharply in focus, a customer's hand holds up a "
        "smartphone at arm's length toward the vendor; the phone's screen is a "
        "flat pale glow with nothing readable on it, and a thin plain black "
        "cable dangles from the bottom edge. Between them on the counter, a "
        "small scuffed plastic payment terminal sits in a wire cradle, its "
        "body entirely plain dark grey with no markings. On the counter also: a "
        "stack of plain white paper cups, a steel tongs, a squeeze bottle, a "
        "crumpled cloth. Behind the vendor, the stall's back wall of pale "
        "stained plywood and a bare hanging bulb that is switched off. Beyond "
        "the awning edge, out of focus, the wet grey street and the blurred "
        "shapes of two passers-by walking away. Cool blue-grey pre-sunrise "
        "light with a warm spill from the griddle and a single shopfront lamp "
        "far behind, soft and diffuse, no strong contrast. Very shallow depth "
        "of field, real optical blur, natural sensor noise, fine grain, slight "
        "vignette, hand-held framing slightly off level, muted realistic "
        "colours. " + NO_TEXT
    ),
    "3": (
        "Professional stock photograph, photo-realistic editorial documentary "
        "photograph shot on an 85mm lens at f/1.8 on a full-frame camera, 16:9 "
        "landscape, available early-morning light: a tight, intimate view "
        "across a street-market counter in a Chinese city at dawn. The camera "
        "is close, at chest height, looking slightly down. In the lower left "
        "third, razor sharp, a customer's hand holds a plain black smartphone "
        "flat, screen up, angled away so only a soft pale glow reflects off "
        "the glass and the fingertips; the phone is otherwise featureless. In "
        "the centre right, softer, a vendor's weathered hand reaches across and "
        "rests two fingers lightly on the edge of the phone, the skin tanned "
        "and creased, a thin plain steel watch on the wrist, sleeve of a faded "
        "blue work shirt pushed up. Beneath the hands, the counter surface is "
        "scratched stainless steel, wet in patches, with a scatter of loose "
        "green beans and a single crumpled note-free paper receipt blank side "
        "up. Behind, melting into warm bokeh, the blurred mass of the vendor's "
        "torso in a grey apron, stacked woven baskets of produce, the pale "
        "canvas of the stall awning and the hazy blue-grey street beyond. Low "
        "warm sun comes in from behind the vendor at a shallow angle, rimming "
        "the hands and the phone edge in gold, deep soft shadow in the "
        "foreground, dust and steam hanging in the light. Extremely shallow "
        "depth of field, real optical bokeh with soft round highlights, "
        "natural sensor noise, fine film grain, subtle vignette, framing "
        "slightly off-centre and imperfect, honest muted colour, no CGI sheen. "
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
    print(f"Generating image with {os.environ.get('MODEL', 'fal-ai/flux/schnell')}...")
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get("STEPS", "4" if "schnell" in model else "28"))
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": steps,
        "enable_safety_checker": False,
    }
    if "schnell" not in model:
        args["guidance_scale"] = float(os.environ.get("GUIDANCE", "3.0"))
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe(model, arguments=args)
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT).convert("RGB")
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 55:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
