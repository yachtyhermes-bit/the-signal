#!/usr/bin/env python3
"""Generate hero for nvts-800v-ai-power-pivot-2026 (fal flux/schnell).

Subject: Navitas Semiconductor — small GaN/SiC power-semiconductor company
pivoting into AI data center power delivery with 800V DC architectures.

Scene chosen (NOT a data-center server aisle):
  ATTEMPT 1 — macro of a GaN half-bridge power stage on a copper heat
  spreader on a lab bench, microscope and tools soft in the background.
  ATTEMPT 2 — engineer in safety glasses probing a power converter board
  with an oscilloscope at a workbench.
  ATTEMPT 3 — silicon/gallium-nitride wafer inspected under cleanroom light.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-nvts-800v-ai-power-pivot-hero-20261104.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "nvts-800v-ai-power-pivot-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no silkscreen text, no brand names, "
    "no logos, no watermark, no captions, no legible writing of any kind "
    "anywhere. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no synthwave, no glowing lines, no light trails, no "
    "futuristic HUD graphics, no augmented-reality overlays, no abstract "
    "digital patterns, no charts, no graphs. Not a data-center hallway, no "
    "server aisle, no server racks, no rack of blinking lights, no "
    "cloud-computing imagery, no circuit-board-as-cityscape, no traces that "
    "glow or look like roads."
)

PROMPTS = {
    "1": (
        "Photo-realistic close-up editorial product photograph, shot on a "
        "full-frame camera with a 100mm macro lens at f/2.8, real available "
        "light in a power-electronics lab, not a render and not CGI: the sharp "
        "focal point is a wide-bandgap gallium nitride power semiconductor "
        "half-bridge module — an engineered block roughly the size of a "
        "matchbox, matte black moulded epoxy body with a flat exposed copper "
        "baseplate, thick tinned copper busbar tabs bent up at one end, and a "
        "row of fine aluminium bond wires visible where the lid is open, "
        "mounted with four screws onto a large machined copper heat spreader "
        "whose surface is warm-toned and lightly oxidised with faint "
        "machining marks. The module sits on a scuffed dark grey anti-static "
        "bench mat, with a small screwdriver, a pair of fine tweezers, a "
        "short length of red hookup wire and a few loose screws lying beside "
        "it. Warm tungsten task light rakes in from the upper left, cool "
        "daylight fill from a window behind, honest specular highlights on "
        "the copper and real soft shadows. Deeply blurred background: the "
        "dark barrel of a stereo microscope on its articulated arm and the "
        "soft shapes of hand tools and a bench power supply, all well out of "
        "focus. Slight scratches and dust on the bench, worn edges on the "
        "metal, framing slightly off-centre and casual rather than a perfect "
        "studio product shot. Very shallow depth of field, sharp only on the "
        "front edge of the module and the copper spreader beside it. Real "
        "macro-lens bokeh, natural sensor noise, fine film grain, faint "
        "chromatic aberration toward the corners, subtle vignette, no plastic "
        "CGI sheen, no perfect symmetry. Photorealistic, extremely high "
        "detail, authentic professional editorial stock photography, 16:9 "
        "landscape composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "2": (
        "Photojournalistic candid documentary photograph, shot on a full-frame "
        "camera with a 50mm lens at f/2.0, available light in a real "
        "electronics laboratory, unretouched, not a render and not CGI: an "
        "engineer in clear safety glasses and a dark short-sleeved shirt sits "
        "in three-quarter profile at an electronics workbench, bent slightly "
        "forward, both hands holding a fine oscilloscope probe steady against "
        "a green power-converter circuit board clamped in a bench vise. His "
        "face is turned down toward the board and partly away from the "
        "camera, softly lit and not clearly identifiable. The board carries "
        "large cylindrical electrolytic capacitors, black chunky inductors, a "
        "row of TO-247 power transistors bolted to an aluminium heatsink and "
        "thick copper busbar links. Its surface is plain unmarked dark green "
        "fibreglass laminate with no printed silkscreen lettering, no white "
        "reference designators and no markings of any kind. His hands are "
        "natural, with five correct fingers each, no distortion. "
        "To the right of frame, out of focus, the "
        "lit graticule of an oscilloscope showing only an unreadable blurred "
        "trace with no characters or numbers, a bench multimeter with a plain "
        "dark display, a soldering iron in its holder and a coil of solder. "
        "Warm tungsten bench lamp from the left, cool fluorescent ceiling "
        "light from above and behind, honest contrast and real shadows. "
        "Cluttered but believable bench: clipped component bags, a tub of "
        "assorted leads, an anti-static wrist strap, coffee ring on the "
        "laminate. Shallow depth of field focused on the hands and the probe "
        "tip touching the board. Real lens blur and bokeh, natural sensor "
        "noise, fine grain, slight vignette, realistic fabric, skin and metal "
        "texture, no studio lighting, no neon, no glowing lines. "
        "Photorealistic, extremely high detail, authentic editorial "
        "photography, 16:9 landscape composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with an 85mm lens at f/2.2 under cleanroom lighting, not a "
        "render and not CGI: close three-quarter view of a compound "
        "semiconductor wafer being handled with gloved hands inside a "
        "semiconductor cleanroom. The wafer — a mirror-polished disc of "
        "silver-grey gallium nitride on silicon — is held at a slight angle by "
        "two hands in white nitrile gloves, its surface catching the overhead "
        "light in a broad soft sheen with the fine rainbow diffraction of the "
        "thin-film layers just visible across it and the tiny repeating "
        "rectangles of the device die faintly readable as texture, not "
        "symbols. Behind it, deeply out of focus, the white and pale grey "
        "surfaces of wafer-handling equipment, a stainless inspection stage "
        "and the soft shape of a technician in a white cleanroom suit and "
        "hood seen from behind, face hidden. Cool neutral overhead cleanroom "
        "light with no coloured gels; nothing in the frame glows or emits "
        "light on its own, no light streaks, no lens flare. Fine dust-free "
        "surfaces, real reflections, a slight tilt in the framing, "
        "photographic rather than a perfect studio composition. Slightly "
        "uneven focus across the frame, a few real scratches and specks on "
        "the stainless stage, honest dirt on the floor tiles, imperfect "
        "white balance, the kind of ordinary imperfection a real press "
        "photographer's frame carries — not a clean computer render. "
        "Shallow depth "
        "of field sharp on the wafer's near edge and the gloved fingertips, "
        "the background dissolving into smooth bokeh. Natural sensor noise, "
        "fine film grain, faint chromatic aberration, subtle vignette, "
        "realistic metal and latex texture, no CGI sheen. Photorealistic, "
        "extremely high detail, authentic professional editorial stock "
        "photography, 16:9 landscape composition, wide horizontal framing. "
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    for q in (92, 88, 84, 80, 76):
        img.save(OUTPUT, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(OUTPUT)
        print(f"  q={q} -> {size} bytes")
        if size <= MAX_BYTES:
            break
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={os.path.getsize(OUTPUT)}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
