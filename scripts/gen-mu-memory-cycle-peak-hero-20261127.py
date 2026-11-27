#!/usr/bin/env python3
"""Generate hero for mu-memory-cycle-peak-trendforce-2027-2026 (fal flux/schnell).

Subject: Micron Technology — US DRAM/HBM/NAND maker at the centre of the
"has the AI memory cycle peaked?" debate. Scene must read as a chip-fab /
silicon-wafer story, NOT a data centre: extreme close-up of a patterned
300mm wafer in a cleanroom with a bunny-suited operator soft in the bokeh.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-mu-memory-cycle-peak-hero-20261127.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "mu-memory-cycle-peak-trendforce-2027-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "The scene contains no writing at all: no text, no letters, no numbers, "
    "no words, no signage, no labels, no stickers, no equipment badges with "
    "lettering, no brand names, no manufacturer logos, no watermark, no "
    "captions, no overlay. No illustration, no digital art, no cartoon, no "
    "3D render, no CGI, no neon, no synthwave, no glowing geometric lines, "
    "no light trails, no futuristic graphics, no holograms, no abstract "
    "digital patterns, no charts or graphs. Not a data centre, no server "
    "room, no server racks, no server aisle, no glowing fibre optics, no "
    "computer screens."
)

PROMPTS = {
    "1": (
        "Professional editorial stock photograph, realistic photo, shot on "
        "100mm macro at f/2.8, 16:9 landscape, available light. Extreme "
        "close-up of a 300 millimetre silicon wafer held at a slight angle "
        "in the left-of-centre of the frame, filling the left half of the "
        "image. The wafer is densely patterned with rows and rows of "
        "rectangular DRAM memory dies, each die a grid of tiny mirror-like "
        "circuit blocks, the array catching a soft rainbow iridescence "
        "across its surface. The wafer rests on the black-gloved fingertips "
        "of a technician whose hand is just visible at the lower edge, "
        "slightly soft. The dies nearest the camera are tack sharp; the far "
        "edge of the wafer and everything behind it falls into creamy "
        "shallow-depth-of-field bokeh. Behind, well out of focus in the "
        "upper right, the blurred pale shape of an operator in a white "
        "full-body cleanroom bunny suit with hood and face mask, standing "
        "beside fab equipment. The cleanroom around them is pale grey and "
        "cool white, with soft overhead light panels rendered as gentle "
        "bokeh. Cool neutral industrial lighting, low contrast, muted "
        "natural colour, honest micro-scratches and a little dust on the "
        "wafer surface, realistic specular highlights, calm documentary "
        "mood, nothing dramatic. Real optical blur, sensor noise, fine film "
        "grain, subtle vignette. " + NO_TEXT
    ),
    "2": (
        "Professional editorial stock photograph, realistic photo, "
        "documentary style, shot on 85mm at f/2, 16:9 landscape, available "
        "light. Close three-quarter view of a patterned silicon wafer lying "
        "flat on a dark grey ceramic vacuum chuck, positioned just left of "
        "centre and occupying the lower two-thirds of the frame. The "
        "polished surface shows a dense regular array of rectangular memory "
        "die sites, fine scribe lines between them, and the faint "
        "holographic sheen of thin-film layers. A few die sites catch a "
        "sharp soft highlight; the pattern recedes into blur toward the "
        "wafer edge. In the soft background upper right, deeply out of "
        "focus, an engineer in a white cleanroom coverall with the hood up "
        "stands in profile facing away, one gloved hand near a matte grey "
        "machine housing. The fab interior is pale grey walls and cool "
        "white ceiling light panels reduced to soft bokeh circles. Shallow "
        "depth of field, real optical blur, sensor noise, fine grain, "
        "subtle vignette, unglamorous believable industrial realism, "
        "muted cool colour. " + NO_TEXT
    ),
    "3": (
        "Professional stock photograph, realistic photo, shot on 50mm at "
        "f/2.8, 16:9 landscape. Tighter environmental portrait of a wafer "
        "inspection bench inside a bright semiconductor cleanroom. In the "
        "sharp left-of-centre foreground, the edge and upper face of a "
        "silicon wafer are visible at an oblique angle, revealing the "
        "repeating rectangular grid of DRAM memory dies with their fine "
        "metallisation, tiny bond pads and bright thin-film reflections. "
        "The wafer is held above a matte grey inspection stage by a "
        "stainless steel edge grip. Two thirds of the frame behind it is "
        "soft, milky bokeh: pale grey machinery, a cool white ceiling "
        "panel, and the blurred white bunny-suited figure of a fab operator "
        "standing a few metres back, face obscured by the hood and mask. "
        "Cool neutral light, low contrast, natural muted colour, slight "
        "haze, honest dust specks, calm documentary realism. Very shallow "
        "depth of field with real optical bokeh, sensor noise, fine film "
        "grain, subtle vignette. " + NO_TEXT
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    print(f"Generating image with {model}...")
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
