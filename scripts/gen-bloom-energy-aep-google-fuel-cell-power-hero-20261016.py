#!/usr/bin/env python3
"""Generate hero for bloom-energy-aep-google-fuel-cell-power-2026 (fal flux/schnell).

Subject: Bloom Energy solid-oxide fuel cells powering Google's Cheyenne, Wyoming
data center — AEP's $4B / 702 MW project.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room / cable runs through a building). It must ALSO
be distinct from the earlier Bloom Energy hero which showed fuel-cell modules on a
concrete pad right next to a glass data-center building at golden hour. So this
frame goes OUT ONTO THE OPEN PRAIRIE: a wide documentary-style photograph of a
compact fuel-cell power plant on the high plains at dusk — rows of large
stainless-steel solid-oxide fuel-cell power modules on concrete pads, a low
transformer yard and steel transmission lattice towers leading away to the
horizon, a big dramatic Wyoming sky, faint distant silhouette of wind turbines on
the ridge, a thin plume of heat-haze above the modules. Slightly low camera angle,
35mm look, shallow depth of field, natural warm-and-cold dusk light.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks.
- No people, no faces, no hands anywhere in the frame.
- NOT a data-center hallway, NOT a server aisle, NOT a server room interior.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-bloom-energy-aep-google-fuel-cell-power-hero-20261016.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "bloom-energy-aep-google-fuel-cell-power-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no part numbers, no serial numbers, no "
    "printed markings, no stencilled characters, no silkscreen text, no screen "
    "text, no instrument displays showing writing, no brand names, no "
    "manufacturer names, no company names, no logos, no watermark, no captions, "
    "no legible writing of any kind anywhere in the image. All equipment "
    "surfaces, panels, cabinets and containers are plain and unmarked. No "
    "people, no faces, no person in the scene, no hands in the frame, no "
    "figures. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no data-center hallway, no server aisle, no "
    "server racks, no server room, no cable runs through a building, no "
    "interior corridor."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, wide documentary style, of "
        "a compact fuel-cell power plant standing on the open high-plains "
        "prairie at dusk. In the middle distance, long orderly rows of large "
        "stainless-steel solid-oxide fuel-cell power modules — tall brushed "
        "metal cabinets a few metres high, plain and unmarked — sit in neat "
        "ranks on pale concrete pads, their flat tops and faint exhaust stacks "
        "catching the last cold blue light while a thin plume of heat-haze and "
        "faint warm vapour shimmers above them. To the right, a low transformer "
        "yard of grey steel boxes and switchgear stands behind a chain-link "
        "fence, and beyond it the slender steel lattice towers of a "
        "transmission line march away toward the horizon, the conductors sagging "
        "in long graceful curves. On the distant ridge across the plain, a faint "
        "pale silhouette of white wind turbines turns against the sky. The sky "
        "dominates the upper half of the frame: a vast dramatic Wyoming dusk, "
        "deep cold blue overhead fading to a band of muted orange and rose "
        "along the horizon, with long low stratus clouds. Slightly low camera "
        "angle, shot on a 35mm lens at f/4, shallow depth of field so the "
        "nearest fuel-cell modules are crisp and the towers, turbines and ridge "
        "melt into soft distance haze. Natural warm-and-cold dusk light, honest "
        "industrial realism, wide-open prairie grass and gravel in the "
        "foreground, subtle sensor noise and fine film grain, no glossy CGI "
        "sheen, photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph shot on a fast lens out on the open "
        "plains at twilight, not a render and not computer generated. The view "
        "is a wide establishing shot of a utility-scale solid-oxide fuel-cell "
        "generating station: parallel banks of large stainless-steel power "
        "modules in plain unmarked metal enclosures stand on rectangular "
        "concrete pads across the mid-ground, evenly spaced like a tidy "
        "industrial orchard, each with a short ventilation stack and a faint "
        "thread of warm shimmering heat-haze rising and dissolving into the cool "
        "air. In front of them the ground is prairie grass, pale gravel and a "
        "concrete service driveway curving away. Past the modules on the left, a "
        "compact transformer yard of grey steel tanks, radiators and gantry "
        "frames hums quietly behind a wire fence, and three tall steel lattice "
        "transmission towers stride off toward the low horizon carrying heavy "
        "sagging power lines. Far away on the ridge line, thin white wind "
        "turbines stand as faint pale sentinels against the dusk. The enormous "
        "high-plains sky fills the frame — cold indigo above, a soft glowing "
        "gradient of amber and dusky pink at the horizon, clouds streaked and "
        "layered. Camera is low and close to the grass for a slightly upward "
        "industrial perspective, 35mm look, gentle depth of field, believable "
        "optical blur, natural warm-and-cold dusk colour, honest working "
        "textures of brushed steel, weathered concrete and dry grass, subtle "
        "vignette, real sensor noise, no perfect symmetry, no airbrushed "
        "surfaces, no plastic render look, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine photograph shot on a 35mm lens by a professional industrial "
        "photographer standing low on the prairie at dusk, not a 3D "
        "visualisation and not an AI render. The frame looks across a compact "
        "fuel-cell power plant toward the horizon: ranks of tall stainless-steel "
        "solid-oxide fuel-cell cabinets, plain brushed-metal boxes without any "
        "markings, sit on pale concrete pads in clean perspective rows, the "
        "nearest ones sharp and richly detailed with visible panel seams, "
        "fasteners and faint weathering, and a delicate wavering plume of hot "
        "air rising above their short exhaust stacks. Between the rows runs a "
        "gravel service lane with bundled conduit and a low steel railing. On "
        "the right of the frame a low transformer yard of grey switchgear, "
        "bushing insulators and steel frames stands behind a chain-link fence, "
        "and beyond it the tapered steel lattice masts and curving catenary "
        "conductors of a transmission line lead the eye far off toward the "
        "flattened horizon. A handful of distant white wind turbines turn slowly "
        "on the far ridge, faint and pale in the haze. Above it all, an immense "
        "sweeping sky of layered clouds glows with cold blue at the zenith and "
        "warm amber light along the receding horizon. Slightly low camera angle, "
        "shallow depth of field focused on the near fuel-cell modules while the "
        "towers and ridge soften into gentle bokeh, natural warm-and-cold dusk "
        "light, honest dust and grain, believable real-world exposure and white "
        "balance, tactile textures of stainless steel, galvanised lattice, "
        "weathered concrete and prairie grass, no glossy CGI sheen, no neon, no "
        "glowing lines, photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A real photograph, wide establishing shot, shot on a fast prime lens at "
        "dusk by an editorial photographer on the high plains, not a render and "
        "not computer generated. A modest solid-oxide fuel-cell generating "
        "plant is seen across open grassland: rows of big stainless-steel "
        "fuel-cell modules in plain unmarked rectangular enclosures stand evenly "
        "on concrete slabs, receding in neat perspective, and a thin ribbon of "
        "warm heat haze trembles above each unit and fades into the cooling air. "
        "A compact outdoor transformer yard of grey steel boxes, cooling fins "
        "and insulators sits to one side behind a low wire fence, humming under "
        "the deepening sky. Steel lattice transmission towers, tall and slender, "
        "walk away across the plain in a straight line, their heavy conductors "
        "sagging in long lithe curves that catch the last pale light, leading "
        "the eye to the distant horizon. Tiny pale wind turbines dot a far "
        "ridge, barely more than silhouettes. Most of the picture is that "
        "enormous high-desert sky: cold slate blue high up melting into a wide "
        "band of muted orange, rose and pale gold near the horizon, with long "
        "soft cloud layers stretching across it. The camera sits low among the "
        "grass, looking slightly up and out toward the wires, a 35mm field of "
        "view, shallow depth of field keeping the nearest fuel-cell modules "
        "sharp and letting the towers, turbines and horizon dissolve into "
        "grainy haze. Natural warm-and-cold dusk light, honest sensor noise and "
        "fine film grain, slightly imperfect real exposure and white balance, "
        "believable textures of brushed steel, weathered concrete, prairie grass "
        "and gravel, subtle vignette, no glowing lines, no neon, no geometric "
        "patterns, no HUD graphics, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
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
