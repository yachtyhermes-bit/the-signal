#!/usr/bin/env python3
"""Generate hero for mu-cxmt-dram-density-race-2026 (fal flux/schnell).

Subject: Micron Technology (NASDAQ: MU) — a US memory-chip maker (DRAM / NAND /
HBM). Article thesis: China's CXMT is claiming a denser "4F2" DRAM design, and
what that means for the memory supply cycle / memory pricing.

Scene chosen (the Writer's caption describes this exact photo): a
PHOTO-REALISTIC editorial stock photograph inside a semiconductor wafer-fab
cleanroom. A technician in a white cleanroom bunny suit, hood and mask (face
not identifiable, seen from behind / three-quarter back) holds up and inspects
a large polished 300mm silicon wafer with both gloved hands; the wafer's mirror
surface reflects the pale cleanroom light and shows a faint diffraction rainbow
sheen. Cool white/blue cleanroom lighting, a hint of amber safety light in the
far background, rows of process equipment and piping softly out of focus behind.
Shallow depth of field focused on the wafer and gloved hands. 16:9 landscape.

Deliberately DISTINCT from the recent 9/14 Micron hero (which was a dark macro
of bare DRAM modules + a silicon die stack on a black table) and NOT a
data-center hallway / server-aisle / rack composition.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: cleanrooms and fab equipment naturally carry printed markings, so
  signage, screen text, equipment labels, wafer-lot codes, letters, numbers,
  logos and watermarks are explicitly forbidden. No captions.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-mu-cxmt-dram-density-hero-20261013.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "mu-cxmt-dram-density-race-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no lot codes, no serial numbers, no "
    "part numbers, no printed markings, no stencilled characters, no screen "
    "text, no monitor displays with writing, no brand names, no manufacturer "
    "names, no logos, no watermark, no captions, no legible writing of any "
    "kind anywhere in the image. All cleanroom surfaces, equipment panels, "
    "wafer surfaces and suit fabrics are plain and unmarked. No illustration, "
    "no digital art, no cartoon, no 3D render, no CGI, no neon, no glowing "
    "lines, no light trails, no synthwave, no geometric patterns, no futuristic "
    "HUD graphics, no overlay elements, no augmented-reality graphics, no "
    "data-center hallway, no server aisle, no server racks, no cable runs."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph inside a semiconductor "
        "wafer fabrication cleanroom. A technician wearing a full white "
        "cleanroom bunny suit, white hood and white face mask — face not "
        "identifiable, seen from behind and slightly to one side, "
        "three-quarter back view — stands holding up a large polished 300mm "
        "silicon wafer with both white-gloved hands, inspecting it at eye "
        "level. The wafer is a perfect circular mirror disc, tilted toward the "
        "camera, its flawless polished surface reflecting the pale cleanroom "
        "light with a faint diffraction rainbow sheen shimmering across it in "
        "soft arcs. Cool white and pale blue cleanroom lighting floods the "
        "room from above, with a single small amber safety light glowing in "
        "the far background. Behind the technician, rows of stainless-steel "
        "process equipment with pipes and venting recede into the distance, "
        "softly out of focus. Shallow depth of field: the wafer and the "
        "gloved hands holding it are tack sharp with visible fine surface "
        "reflections, while the technician's shoulders, the equipment and the "
        "room behind dissolve into smooth creamy bokeh. Shot on a 50mm lens at "
        "f/2.0, real optical bokeh, natural realistic material textures, "
        "authentic cleanroom atmosphere with a slight cool haze, honest "
        "documentary lighting, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a fast prime lens, not a render and not "
        "computer generated: a cleanroom technician in a full white bunny "
        "suit, hood and face mask is photographed from behind and to one side "
        "so the face is not visible, standing at a wafer inspection station "
        "and lifting a large circular 300mm silicon wafer up to the light with "
        "both white-gloved hands. The wafer is the focal point — a bare "
        "polished mirror-finish silicon disc, its surface catching the cool "
        "white overhead cleanroom light and diffracting it into a soft pale "
        "rainbow band across the mirror, the technician's white-gloved fingers "
        "gripping the thin wafer edge. Cool blue-white cleanroom illumination, "
        "a faint amber glow from a safety lamp deep in the background, rows of "
        "stainless process tools, gas panels and piping stretching away and "
        "rendered in soft blur. Extremely shallow depth of field, everything "
        "but the wafer and the gloves melted into smooth creamy bokeh, a thin "
        "cool haze in the air, natural camera noise and very slight film "
        "grain, subtle lens vignette, real optical blur, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, honest documentary realism, photorealistic, "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A real documentary photograph taken by a professional photographer in "
        "a semiconductor wafer fabrication cleanroom, not a render and not "
        "computer generated. Strictly from BEHIND in a three-quarter back "
        "view, a worker in a white cleanroom bunny suit, white hood and white "
        "face mask — back of the hood toward the camera, no face and no eyes "
        "visible at all — stands with both arms raised, holding a bare "
        "polished 300mm silicon wafer up in front of them and inspecting it "
        "between two white-gloved hands. The wafer is a flawless circular "
        "mirror disc tilted toward the camera, and across its mirror-polished "
        "surface a clear iridescent diffraction rainbow shimmers — soft pale "
        "green, pink, violet and gold fringes fanning outward across the "
        "reflective silicon like a thin-film interference sheen, the cleanroom "
        "lights mirrored sharply in the disc. Cool white and pale blue "
        "overhead cleanroom lighting, with one small amber safety lamp glowing "
        "far down the bays behind. The room stretches away in rows of blank "
        "stainless-steel process tools, gas panels, ducts and piping, all "
        "rendered softly out of focus. Shallow depth of field: the wafer and "
        "the gloved hands are tack sharp while the technician's back and the "
        "entire room fall into smooth creamy bokeh. Shot handheld on a "
        "full-frame camera with an 85mm lens at f/2.0, heavy natural sensor "
        "noise and fine film grain in the shadows, slightly uneven real-world "
        "white balance, faint dust motes and a thin cool haze in the air, "
        "subtle lens vignette, real optical blur, imperfect honest framing. "
        "Absolutely not a 3D visualisation, not a glossy CGI render, no "
        "airbrushed plastic surfaces, no smooth digital sheen, no perfect "
        "symmetry, no digital illustration, no AI-generated look, "
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
