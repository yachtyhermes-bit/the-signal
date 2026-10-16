#!/usr/bin/env python3
"""Generate hero for vrns-proofpoint-ai-data-security-acquisition-2026 (fal flux/schnell).

Subject: Varonis Systems (VRNS), a data-security software company, being acquired by
Proofpoint (owned by Thoma Bravo) for $6.3B in cash — a cybersecurity consolidation /
AI data-security story.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room / glass office lobby with access-control turnstiles
(Zscaler, Oct 15) / fuel-cell power scene):
a PHOTO-REALISTIC editorial stock photograph of PROTECTING CORPORATE RECORDS —
a person in business casual working among color-coded file folders, ring binders and
archive boxes in a bright modern office, or a worker's hands sorting plain labeled
folders with an access badge resting on the desk. Warm natural window light, shallow
depth of field, shot on a full-frame camera.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks,
  no legible labels, no legible badge text, no readable screens.
- No identifiable face: seen from side/back or gently out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-vrns-proofpoint-hero-20261016.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "vrns-proofpoint-ai-data-security-acquisition-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "printed markings, no stencilled characters, no screen text, no legible "
    "folder tabs, no legible paper headings, no legible ID badge, no name "
    "badges, no brand names, no manufacturer names, no company names, no "
    "logos, no watermark, no captions, no legible writing of any kind "
    "anywhere in the image. All folders, binders, boxes, papers, tab dividers "
    "and any badge present are plain and unmarked with no readable characters, "
    "numbers or symbols. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no neon, no glowing lines, no light trails, no synthwave, "
    "no geometric patterns, no futuristic HUD graphics, no overlay elements, "
    "no augmented-reality graphics, no data-center hallway, no server aisle, "
    "no server racks, no cable runs through a building, no glowing computer "
    "screens, no monitors displaying content. No prominent face, no portrait, "
    "no front-facing identifiable person: any person is seen from behind or "
    "from the side, hands only, or gently out of focus."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a person in business "
        "casual working among color-coded file folders, ring binders and "
        "cardboard archive boxes in a bright modern office records area. In "
        "the soft-focus foreground we see only a pair of hands sitting at a "
        "light wooden desk, sorting plain folders from an open archive box, "
        "with a slim unmarked plastic access badge resting on the desk beside "
        "a mug of coffee. Rows of neatly shelved binders and stacked document "
        "boxes recede into creamy bokeh behind, a couple of them warm red, "
        "blue and green but completely plain and unlabelled. Warm natural "
        "daylight pours through a tall nearby window, casting soft honest "
        "shadows and highlighting the texture of the paper and fabric. "
        "Shallow depth of field, shot on a 50mm lens at f/2 on a full-frame "
        "camera, real optical blur, natural material textures, subtle sensor "
        "noise and fine film grain, honest documentary realism, no glossy CGI "
        "sheen, photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph taken on a full-frame camera in a "
        "bright, tidy corporate records room of a modern office, not a render "
        "and not computer generated. The focus is a person's hands placing a "
        "plain manila folder into an open cardboard archive box on a pale "
        "wooden desk. Around the box, neat stacks of color-coded ring binders "
        "and shelved document files — warm red, teal and grey but entirely "
        "plain and blank — fill the frame. A simple unmarked access card and "
        "lanyard lie on the desk. Warm afternoon daylight streams in from a "
        "window to the left, casting long gentle shadows and a soft golden "
        "warmth across the paper and wood. In the background, softly out of "
        "focus, the shoulder and back of a colleague in a light shirt reaching "
        "for a shelf, not facing the camera. Shallow depth of field, 35mm lens "
        "at f/2, real optical blur, believable sensor noise in the shadows, "
        "slightly imperfect real-world exposure and white balance, subtle "
        "vignette, tactile realistic textures, no plastic render look, no "
        "digital illustration, no AI-generated look, photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine photograph shot by a professional corporate photographer "
        "in a bright modern office filing and records room, not a 3D "
        "visualisation and not an AI render. A worker in business casual, seen "
        "from behind and slightly to the side so the face is not visible, "
        "stands at a low shelf organising rows of plain color-coded archive "
        "boxes and lever-arch binders. Their hands hold one unmarked folder "
        "mid-sort. On the desk beside them sits a small pile of documents, a "
        "paper tray, and a plain white access badge with no writing. Warm "
        "natural window light floods the room from the right, honest natural "
        "contrast, soft realistic shadows, a faint dust haze in the air. "
        "Shallow depth of field focused on the hands and folders, everything "
        "behind melting into smooth real bokeh. 50mm lens at f/2.2 on a "
        "full-frame camera, real optical blur, natural grain and sensor noise, "
        "slightly uneven white balance, subtle vignette, honest imperfect "
        "realism, no airbrushed surfaces, no glossy CGI sheen, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A real photograph made by a documentary photographer in the bright "
        "records area of a contemporary corporate office, not a render, not "
        "CGI. The dominant subject is a light wooden worktable covered with "
        "color-coded file folders, lever-arch binders and an open archive box, "
        "all plain and unmarked. A person's hands, business-casual shirt "
        "sleeves rolled up, sort the folders; a plain access badge on a lanyard "
        "lies to one side. Tall shelving full of blank labeled-free document "
        "boxes and binders stands softly out of focus behind. Warm daylight "
        "pours in through a large window, catching the texture of the paper, "
        "cardboard and desk surface, with honest natural shadows and a gentle "
        "golden glow. Shallow depth of field, 35mm lens at f/1.8 on a "
        "full-frame camera, real optical blur, faint dust in the air, natural "
        "sensor noise and fine film grain, slightly imperfect exposure, subtle "
        "vignette, tactile realistic material textures, no plastic CGI sheen, "
        "no digital art, no illustration, no AI-generated look, photorealistic, "
        "very high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
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
