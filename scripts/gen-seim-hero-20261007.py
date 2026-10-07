#!/usr/bin/env python3
"""Generate hero image for etf-review-seim-2026-10-07 using fal flux/schnell.

Subject: SEI QiM U.S. Large Cap Momentum Active ETF (SEIM) deep dive.
Theme: A disciplined, quiet quantitative investment desk or study scene.
Per brief:
- ONE hero image via FAL flux/schnell, photo-realistic, 16:9.
- Scene must fit a fund deep-dive and must NOT look like any recent hero:
  e.g. a neat stack of plain unmarked booklets and a coffee cup on a wooden table in soft morning light,
  or a tidy desk with a calculator, a notebook and a tablet showing an abstract unreadable chart.
- NO people, NO hands or body parts, NO text, lettering, logos or numbers anywhere in frame,
  NO data-center hallway, NO neon/synthwave, NO abstract art.
"""
import os
import sys
import requests
from PIL import Image

SLUG = "etf-review-seim-2026-10-07"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no watermarks. "
    "Any papers or notebooks are blank or show soft, completely unreadable light pencil sketches. "
    "Any tablet or screen displays only an abstract, soft gradient or smooth blurry graphic with no legible text or digits. "
    "No people, no hands, no faces, no human figures, no silhouettes. "
    "No neon lights, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Strictly photorealistic editorial still life."
)

PROMPT = (
    "Professional editorial still life photograph, shot on a 50mm f/2.0 lens on a full-frame camera, "
    "natural soft morning window light from the side with gentle real shadows. "
    "On a beautiful solid dark walnut desk sits a neat stack of two plain unbranded matte linen notebooks, "
    "a ceramic stoneware coffee mug with dark coffee, a sleek brass stylus resting beside the books, "
    "and a slim tablet lying flat with its display softly reflecting the morning window light. "
    "In the background, a small textured ceramic vase with dried olive branches sits in soft, warm bokeh. "
    "Clean, balanced, contemplative composition, rich organic textures of matte paper, glazed ceramic, "
    "brushed brass, and natural wood grain. Authentic depth of field, subtle film grain, "
    "extremely high detail, 8k resolution, documentary photography, 16:9 landscape aspect ratio. "
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
    args = {
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": 420815,
    }
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "image" in result:
        image_url = result["image"]
        
    if not image_url:
        print(f"ERROR: Could not get image url: {result}")
        sys.exit(1)
        
    print(f"Downloading from {image_url}...")
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)
        
    img = Image.open(OUTPUT)
    print(f"Saved initial image: {OUTPUT} size={img.size} bytes={len(r.content)}")
    
    # Resize / upscale to standard 1920x1080
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92)
        print(f"Upscaled to {FINAL_W}x{FINAL_H}")
        
    # Copy to _backup_dist
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92)
    print(f"Copied to {BACKUP}")
    print("Done!")

if __name__ == "__main__":
    main()
