#!/usr/bin/env python3
"""Hero image for ai-inference-token-economics-explainer-2026 via fal flux/schnell.

Subject: an evergreen explainer on AI inference economics -- what a model actually
sells (tokens), why per-token prices keep collapsing, and why that price collapse
drives MORE compute demand.
Physical subject: the accelerator hardware that serves inference -- ONE AI
accelerator module (GPU-class board with a large finned heatsink / vapor chamber
and HBM stacks beside the die).
Composition: close, side-lit macro documentary photograph of ONE unbranded AI
accelerator module lying on a dark anti-static workbench mat, fine tweezers and a
small calibrated measuring instrument out of focus beside it, shallow depth of
field, warm industrial bench lighting with soft cool window fill.
NOT a data-center corridor, NOT a symmetrical server aisle, NOT racks of any kind,
NOT a wafer/fab cleanroom, NOT a rocket, NOT people/hands/faces.
NO text, letters, numbers, logos, branding, watermarks or signage anywhere.
NO neon, synthwave, glowing lines, HUD overlays, holograms, digital art,
geometric patterns, charts or 3D-render sheen. Strictly photorealistic editorial
stock photography, 16:9 landscape.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "ai-inference-token-economics-explainer-2026"
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864  # exact 16:9 on flux's 16px grid, so the 1080p upscale is uniform
FINAL_W, FINAL_H = 1920, 1080
SEED = 770433

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no serial numbers, no model numbers, no symbols, no logos, no branding, "
    "no watermarks, no signage, no labels of any kind anywhere in frame. "
    "The board itself is completely plain and unbranded: no silkscreen printing, no white "
    "printed markings, no white label stickers, no adhesive labels, no tape, no barcode, "
    "no etched or printed part numbers, no printed symbols, glyphs or manufacturer marks on "
    "the PCB, the heatsink, the capacitors or any chip, no text on any packaging. "
    "No people, no hands, no fingers, no faces, no human figures, no silhouettes, no workers. "
    "No neon lights, no synthwave, no glowing lines, no light trails, no HUD overlays, "
    "no holograms, no digital or sci-fi effects, no 3D render sheen, no CGI look, no plastic "
    "surfaces, no perfectly clean showroom finish, no abstract art, no geometric patterns, "
    "no charts, no graphs. "
    "Not a data-centre corridor, not a symmetrical vanishing-point server aisle, "
    "not racks of any kind, not a wafer fab cleanroom, not a rocket, not a top-down aerial. "
    "Strictly photorealistic editorial stock photography, looks like a real camera photograph "
    "of real hands-off hardware on a bench. This is an actual photograph, not a 3D render, "
    "not a CGI model, not AI-generated digital art."
)

PROMPT = (
    "Close, side-lit macro documentary photograph of ONE unbranded AI accelerator module "
    "lying flat on a dark anti-static workbench mat, shot on a 100mm macro lens at f/4 on a "
    "full-frame camera, shallow depth of field. "
    "The board is a real GPU-class accelerator: a large finned aluminium heatsink and a "
    "polished copper vapour chamber dominate the frame, finely machined fins catching "
    "raking warm side light, visible micro-scratches, dust specks and light wear on the "
    "metal. Beside the die sit neat stacks of high-bandwidth memory chips on a dark matte "
    "circuit board, with gold edge connectors, tiny surface-mount capacitors, chokes, "
    "thick copper heat pipes and a matte black plastic shroud. "
    "In the soft out-of-focus foreground rest a pair of fine stainless tweezers and a small "
    "calibrated measuring instrument with a brushed metal body, blurred into bokeh. "
    "Warm industrial bench lighting rakes across the heatsink from the left with gentle "
    "shadow falloff, while a soft cool daylight fill from a window cools the highlights; "
    "the dark anti-static mat and dim blurred workshop background recede out of focus. "
    "Heavy, expensive, well-used engineering hardware under inspection, honest dust and "
    "wear, no glowing accents. "
    "Real reportage camera character: genuine digital sensor noise and fine film grain, "
    "natural optical vignetting, gentle chromatic aberration on the bright metal highlights, "
    "slightly imperfect handheld framing, realistic white balance, an unretouched "
    "documentary editorial stock photograph, extremely high detail, 16:9 landscape "
    "aspect ratio. "
    + NO_TEXT
)


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


def main():
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": SEED,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT)
    print(f"Saved: {OUTPUT} size={img.size} bytes={len(r.content)}")
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92)
        print(f"Upscaled to {FINAL_W}x{FINAL_H}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92)
    print(f"Copied to {BACKUP}")
    print("Done!")


if __name__ == "__main__":
    main()
