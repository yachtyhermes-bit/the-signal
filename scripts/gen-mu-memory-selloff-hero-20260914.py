#!/usr/bin/env python3
"""Generate hero for mu-memory-selloff-ai-slowdown-2026 (fal flux/schnell).

Subject: Micron Technology (NASDAQ: MU) — a memory-chip maker (DRAM / NAND /
HBM). Article thesis: memory stocks sold off today after AI leaders called for
a slower frontier-model pace, but Micron's DRAM/NAND/HBM business is
contracted and supply-tight.

Scene chosen (the Writer's caption describes this exact photo): an EXTREME
MACRO product photograph of advanced computer memory hardware — several bare
DRAM memory modules (green printed circuit boards with gold contact fingers)
lying on a dark matte surface, with one stack of polished mirror-like silicon
dies (a high-bandwidth-memory style stack) standing in the near foreground,
cool blue key light with a warm amber rim highlight on the metal edges, very
shallow depth of field, dark background dissolving into shadow. Must look like
a real photograph taken with a macro lens, editorial stock-photography quality.

Deliberately NOT a data-center hallway / server-aisle / rack composition, no
neon, no glowing lines, no HUD overlays, no 3D-render look, no people.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines.
- TEXT-FREE: memory PCBs naturally carry printed markings, so silkscreen
  lettering, part numbers, serial numbers, brand names, country-of-origin
  stamps and logos are explicitly forbidden. No watermark, no captions.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-mu-memory-selloff-hero-20260914.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "mu-memory-selloff-ai-slowdown-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The hardware is completely blank and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no part numbers, no printed "
    "markings, no silkscreen lettering, no stamped characters, no labels, no "
    "stickers, no barcodes, no QR codes, no white printed stripes with "
    "writing, no country-of-origin stamps, no brand names, no manufacturer "
    "names, no model designations referenced, no logos, no watermark, no "
    "captions, no legible writing of any kind anywhere in the image. The "
    "circuit boards are plain matte green with only unmarked gold contact "
    "fingers, plain unlabelled black chip packages and bare metallic traces, "
    "absolutely no printed characters on any surface. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no glowing "
    "lines, no light trails, no synthwave, no geometric patterns, no futuristic "
    "HUD graphics, no overlay elements, no augmented-reality graphics, no "
    "data-center hallway, no server aisle, no server racks, no cable runs, no "
    "computer screens."
)

PROMPTS = {
    "1": (
        "Photo-realistic extreme macro product photograph of advanced computer "
        "memory hardware resting on a dark matte charcoal surface. Several "
        "bare DRAM memory modules lie flat and slightly overlapping across the "
        "middle of the frame, showing plain unmarked green printed circuit "
        "boards with rows of gold contact fingers along one edge and plain "
        "black unlabelled memory chip packages soldered in neat rows. In the "
        "near foreground, standing upright and catching the light like a "
        "polished mirror, is a single stack of thin polished silicon dies — a "
        "tall rectangular high-bandwidth-memory style stack of gleaming "
        "silicon wafers bonded together, its edges mirror-bright and "
        "reflective. Cool blue key light rakes across the scene from one side "
        "while a warm amber rim highlight traces the metal edges and gold "
        "contacts of the modules and the stack. Very shallow depth of field: "
        "the front of the silicon stack is tack sharp with visible fine "
        "silicon texture, the DRAM modules behind it fall progressively into "
        "soft blur, and the dark background dissolves completely into deep "
        "shadow with no visible environment, no room, no racks and no walls. "
        "Shot on a 100mm macro lens at f/2.8, real optical bokeh, fine "
        "surface dust and micro-scratches, natural realistic material "
        "textures, moody low-key studio product lighting, dark and premium "
        "editorial look, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a macro lens, not a render: extreme "
        "close-up of computer memory chips on a dark matte table, styled as "
        "an authentic technology stock photo for a financial news article. "
        "Three plain green bare memory circuit boards with unmarked gold "
        "contact fingers rest on the dark surface at a slight angle, real "
        "soldered joints visible, thin matte-black rectangular chip packages "
        "in neat rows, a few faint specks of dust and tiny handling "
        "imperfections on the boards and the table. In the immediate "
        "foreground, standing on edge and catching the light, is a stack of "
        "thin stacked silicon dies — layered silicon with fine visible "
        "horizontal bonded layers on its side, its polished top face softly "
        "reflecting the light like dark silicon rather than like chrome. "
        "Cool blue-white light falls from the upper left and a warm amber "
        "edge light glints along the metal and gold surfaces, gentle "
        "cool-and-warm colour contrast. Extremely shallow depth of field "
        "melts everything except the near edge of the stack into smooth "
        "creamy bokeh, and the background is pure dark shadow with nothing "
        "visible in it — no room, no equipment, no racks. Moodily lit and "
        "underexposed at the edges, honest uneven real-world lighting, "
        "natural camera noise and very slight film grain, subtle lens "
        "vignette, real optical blur, no plastic CGI sheen, no perfect "
        "symmetry, no glossy render, no computer-generated look, no 3D "
        "visualisation, no digital illustration, photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A real close-up photograph taken with a macro lens, not a render and "
        "not computer generated: a single stack of thin stacked silicon dies "
        "stands on edge in the very near foreground, sharply in focus, "
        "layered silicon with fine visible horizontal bonded layers along its "
        "side and a polished dark grey-blue silicon top face that reflects "
        "the light only softly, like real silicon, not like chrome or metal. "
        "Behind it on a dark matte table, softly out of focus, lie two bare "
        "green memory circuit boards with unmarked gold contact fingers and "
        "plain bare matte-black chip packages, their green surfaces "
        "completely blank and plain right across, with no printed white "
        "characters, no stencilled codes and no markings of any kind on them, "
        "boards perfectly clean and blank as if plain unlabelled. Cool "
        "blue-white key light from the upper left and a warm amber rim light "
        "on the metal edges and gold contacts, gentle cool-and-warm contrast. "
        "Extremely shallow depth of field, everything but the near edge of "
        "the silicon stack dissolved into smooth creamy bokeh, background a "
        "pure dark shadow with nothing visible in it, no room, no racks, no "
        "equipment, nothing else present. Honest underexposed moody "
        "available-style lighting, faint dust particles, natural camera noise "
        "and very slight film grain, subtle lens vignette, real optical "
        "blur, no plastic CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "4": (
        "A real close-up photograph taken with a macro lens, not a render and "
        "not computer generated. In the very near foreground, standing on "
        "edge and sharply in focus, is a rectangular stack of thin polished "
        "silicon dies — a stack of bare silicon wafers bonded together, its "
        "side showing many fine horizontal layered edges of grey silicon with "
        "faint reflection, and its top face bare polished dark silicon "
        "reflecting the light only gently, like real silicon, not chrome and "
        "not metal. On the dark matte table behind it, softly out of focus, "
        "two bare memory circuit boards lie flat with blank plain green "
        "surfaces and unmarked gold contact fingers, their bare matte-black "
        "chip packages plain and unlabelled with no printed white characters, "
        "no stencilled codes and no markings of any kind on any surface. Cool "
        "blue-white key light from the upper left and a warm amber rim light "
        "along the metal edges and gold contacts, gentle cool-and-warm "
        "contrast. Extremely shallow depth of field, everything but the near "
        "edge of the silicon stack dissolved into smooth creamy bokeh, the "
        "background a pure dark shadow with nothing visible in it, no room, "
        "no racks, no equipment. Honest underexposed moody lighting, faint "
        "dust particles, natural camera noise and very slight film grain, "
        "subtle lens vignette, real optical blur, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "5": (
        "A real close-up photograph taken with a macro lens, not a render and "
        "not computer generated: a single stack of thin polished silicon dies "
        "stands on edge in the very near foreground, sharply in focus — a "
        "stack of bare grey silicon wafers bonded face to face, its side "
        "showing many fine horizontal layered edges, its top face bare "
        "polished silicon that reflects the light only softly, like real "
        "silicon, not like chrome or metal. Behind it on a dark matte table, "
        "softly out of focus, lie two bare green memory circuit boards with "
        "unmarked gold contact fingers and plain bare matte-black chip "
        "packages, their green surfaces completely blank and plain right "
        "across, with no printed white characters, no stencilled codes and no "
        "markings of any kind on them, boards perfectly clean and blank as if "
        "plain unlabelled. Cool blue-white key light from the upper left and "
        "a warm amber rim light on the metal edges and gold contacts, gentle "
        "cool-and-warm contrast. Extremely shallow depth of field, everything "
        "but the near edge of the silicon stack dissolved into smooth creamy "
        "bokeh, background a pure dark shadow with nothing visible in it, no "
        "room, no racks, no equipment, nothing else present. Honest "
        "underexposed moody available-style lighting, faint dust particles, "
        "natural camera noise and very slight film grain, subtle lens "
        "vignette, real optical blur, no plastic CGI sheen, no glossy render, "
        "no perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, high detail, professional editorial stock "
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
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
