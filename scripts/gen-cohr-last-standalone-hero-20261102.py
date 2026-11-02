#!/usr/bin/env python3
"""Generate hero for cohr-last-standalone-optics-2026 (fal flux/schnell).

Subject: Coherent Corp (NYSE: COHR) — the last large independent supplier of
AI data-center optics: indium phosphide lasers, EMLs, transceivers and the
optical fiber / photonics manufacturing chain behind AI interconnect.

Scene chosen (must be visually distinct from the 10/17 COHR hero, which was a
cleanroom technician holding an indium-phosphide wafer at an inspection
station — NOT repeated here):

  ATTEMPT 1 — an INDUSTRIAL OPTICAL FIBER DRAW TOWER: a tall draw furnace in a
  fiber plant, a hair-thin glass fiber being drawn downward from the molten tip
  of a glass preform, a technician in the background watching the draw,
  spooling machinery in soft focus.
  ATTEMPT 2 — macro of a polished optical fiber connector / ceramic ferrule on
  a precision bench.
  ATTEMPT 3 — wide photonics manufacturing floor with assembly benches and
  fiber spools.

Deliberately NOT a data-center hallway / server aisle / server racks. No
abstract or digital art, no neon or synthwave, no glowing geometric lines, no
fake charts, no text of any kind.

HARD CAP: 3 fal flux/schnell generations total for this article (ATTEMPT 1-3).
Never run a 4th attempt.

Rules:
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon,
  synthwave, CGI, 3D render, cartoon, glowing lines, light trails, HUD.
- TEXT-FREE: no letters, numbers, labels, logos, brand names, watermarks.
- FACES not clearly readable (hood/helmet, side/behind, out of focus).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-cohr-last-standalone-hero-20261102.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "cohr-last-standalone-optics-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no silkscreen text, no instrument "
    "display showing characters, no brand names, no logos, no watermark, no "
    "captions, no legible writing of any kind anywhere. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no synthwave, no "
    "glowing geometric lines, no light trails, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no charts, no "
    "graphs, no data visualization. Not a data-center hallway, no server "
    "aisle, no server racks, no rack of blinking lights, no cable runs "
    "through a building, no cloud-computing imagery."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 35mm lens at f/2.0, real available industrial light, not "
        "a render and not CGI: the inside of an optical fiber manufacturing "
        "plant, at the base of a tall fiber-draw tower. A vertical glass "
        "preform, a thick clear cylinder about the size of a forearm, hangs "
        "from the bottom of a cylindrical graphite draw furnace high in the "
        "frame; from its molten rounded tip a single hair-thin strand of glass "
        "fiber is being drawn downward, catching a thin thread of warm amber "
        "light where the furnace heat still glows on it, falling perfectly "
        "straight toward a coating cup and then a spinning take-up spool below. "
        "The tower is built from matte grey and stainless steel panels, "
        "insulated pipework, cable trays and dial gauges with plain unmarked "
        "faces, streaked with honest industrial grime and fine dust. In the "
        "middle distance, softly out of focus, a technician in a dark blue "
        "work jacket, hard hat and safety glasses stands at a control console "
        "watching the draw, seen from the side and behind so the face is not "
        "identifiable. To the right, blurred take-up machinery and large "
        "cardboard-free fiber spools wound with pale fiber. Cool neutral "
        "fluorescent plant lighting from above with the small warm glow of the "
        "furnace mouth as the only accent. Shallow depth of field: the preform "
        "tip and the first metre of drawn fiber are razor sharp, the tower and "
        "the technician melt into soft bokeh. Real optical lens blur, natural "
        "sensor noise, fine film grain, subtle vignette, tactile metal and "
        "glass texture, no plastic CGI sheen, no perfect symmetry. "
        "Photorealistic, extremely high detail, authentic editorial "
        "photography, 16:9 landscape composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "2": (
        "Photo-realistic macro editorial photograph shot on a 100mm macro lens "
        "at f/2.8, real camera optics, not a 3D render: extreme close-up on a "
        "precision optical bench in a fiber-optics assembly shop. The sharp "
        "focal point is a polished single-mode optical fiber connector — a "
        "cylindrical ceramic ferrule with a mirror-smooth chamfered end face, "
        "mounted in a spring-loaded metal housing, its white and grey strain-"
        "relief boot trailing off behind it, with a second identical connector "
        "lying beside it on a dark matte anti-static mat. The 125-micron glass "
        "core is just visible as a tiny bright point at the centre of the "
        "ferrule end face under a raking bench light. Around it, a scatter of "
        "precision tools: fine tweezers, a ceramic scribe, a small torque "
        "driver, a polishing puck with a disc of lapping film, and a short coil "
        "of bare glass fiber. Warm tungsten task light from the upper left "
        "rakes across the ceramic and metal, cool daylight fill from behind, "
        "honest specular highlights and real shadows. Deeply blurred "
        "background: out-of-focus stainless assembly equipment, a reel of "
        "fiber, a plain grey wall. Nothing in the frame emits light or glows: "
        "no light streaks, no lens flare, no illuminated cables, no glowing "
        "elements of any kind — only ordinary tungsten and daylight "
        "illumination on ordinary objects. The bench edge is chipped and worn, "
        "the anti-static mat carries real dust and a few stray cut fiber "
        "ends, the tools are used and slightly scratched, the framing is "
        "slightly off-centre and casual rather than a perfect product shot. "
        "Very shallow depth of field, sharp only on the ferrule end face and "
        "the first centimetres of the housing. Real "
        "macro-lens bokeh, natural sensor noise, faint dust motes, fine film "
        "grain, slight chromatic aberration at frame edges, subtle vignette, no "
        "plastic CGI sheen, no perfect symmetry. Photorealistic, extremely high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "3": (
        "Photojournalistic candid documentary photograph, shot on a Fujifilm "
        "X-T5 with a 23mm lens at f/4, available factory light, unretouched, "
        "not a render and not CGI: a wide eye-level view down the length of an "
        "ordinary working optical-fiber and photonics assembly floor. A long "
        "row of plain laminate-topped workbenches runs away from the camera on "
        "the left, each bench with a stereo microscope on an articulated arm, a "
        "small fusion-splicer box, a soldering iron in a holder, plastic parts "
        "bins and neatly coiled lengths of pale buff-coloured fiber; a few "
        "operators in dark blue work jackets and safety glasses sit or stand at "
        "the benches, small in the frame and seen from behind and in three-"
        "quarter profile at a distance, faces turned away and not identifiable. "
        "On the right, steel shelving holds matte grey plastic spools wound with "
        "dull fiber, cardboard boxes, labelled-free plain plastic cases and a "
        "coiled air hose. The room is unglamorous and slightly cluttered in a "
        "believable way: scuffed vinyl floor tiles, painted breeze-block walls, "
        "conduit and cable tray running along the ceiling, a wall clock with a "
        "blank white face, a fire extinguisher, a worn office chair pushed to "
        "one side. Flat cool overhead strip lighting mixed with a little warm "
        "afternoon daylight from high windows on the left; no coloured lighting, "
        "nothing in the room emits light or glows, no light streaks, no lens "
        "flare, no illuminated cable, no glowing elements of any kind. Honest "
        "wide-angle perspective with slight natural barrel distortion, "
        "believable clutter and asymmetry, real shadows, everyday dust and wear. "
        "Moderate depth of field: the nearest bench with its microscope and "
        "coiled fiber is in focus, the far end of the hall softening into haze. "
        "Real lens blur, natural sensor grain, faint chromatic aberration, "
        "realistic fabric, laminate and metal texture, no studio lighting, no "
        "neon, no glowing lines, no digital-art look. "
        "Photorealistic, extremely high detail, authentic editorial "
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
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
