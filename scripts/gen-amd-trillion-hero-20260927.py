#!/usr/bin/env python3
"""Generate hero for amd-trillion-dollar-ai-rerate-2026 (fal flux/schnell).

Subject: AMD (Advanced Micro Devices) has crossed a $1 trillion market cap for
the first time — one of four US chipmakers in the trillion-dollar club, riding
the AI accelerator buildout (Instinct MI450 data-centre GPUs, EPYC server CPUs,
gigawatt-scale deals with OpenAI / Meta / Anthropic).

Sector: semiconductors. Scene guidance: chip fab cleanroom / silicon wafer.

Frames chosen (photo-realistic editorial stock only):
  1 — fab cleanroom interior: a technician in a white bunny suit seen from
      behind/side at a slight angle, carrying a gleaming 300mm silicon wafer
      with an iridescent rainbow die pattern, beside an open FOUP and the
      brushed-metal housing of a lithography tool, cool white overhead light
      and a faint yellow litho-bay glow deep in the background.
  2 — tight macro of a single 300mm wafer held in a gloved hand at a shallow
      angle, dies catching violet / blue / gold diffraction, ceiling bokeh.
  3 — wide cleanroom aisle from behind a rack of FOUPs on a wafer transport
      system, technician walking away in the middle distance.

Deliberately NOT (banned): no illustration / digital art, no CGI sheen, no
neon / synthwave, no glowing lines, no abstract geometric art, no holograms,
no wireframe, no charts / graphs / dashboards, no data visualisation, no
server room, no server racks, no server aisles, no cable runs, no robots,
no drones, no lasers, and no readable text of any kind. Wafer die grids are
fine as geometry but must carry no readable characters.

Rules (per repo regen lessons):
- PHOTO-REALISTIC documentary photojournalism ONLY: available light, real
  sensor noise, long-lens shallow depth of field, imperfect handheld framing,
  worn and real textures. No CGI sheen.
- TEXT-FREE: cleanrooms invite equipment stencils, lot codes, hazard placards
  and brand marks, so every surface, wafer and machine is explicitly unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-amd-trillion-hero-20260927.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amd-trillion-dollar-ai-rerate-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no ticker "
    "symbols, no stock tickers, no stencilled codes, no engraved equipment "
    "numbers, no serial numbers, no part numbers, no painted identification "
    "codes, no wafer lot codes, no batch codes, no date codes, no hazard "
    "placards with writing, no danger signs with words, no warning labels, "
    "no cleanroom signage, no bay signs, no door signs, no posted notices, "
    "no branding anywhere, no brand names, no manufacturer names, no "
    "corporate names, no corporate logos, no trademarks, no watermarks, no "
    "signatures, no graffiti, no handwriting, no documents, no clipboards "
    "with writing, no paperwork, no labels, no tags, no stickers, no decals, "
    "no screen displays with writing, no readouts with digits, no lettering "
    "on the bunny suit, no printed marks on the hood or mask, no lettering "
    "on gloves or sleeves, no legible writing of any kind anywhere in the "
    "image. Every surface, every wafer and every machine is plainly and "
    "completely unmarked: the silicon wafers carry only plain repeating "
    "rectangular die grid geometry with no readable characters anywhere on "
    "them, and the equipment housings are bare brushed metal with no plates "
    "and no engraving. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no video-game still, no concept art, no matte painting, "
    "no neon, no synthwave colour, no glowing lines, no light trails, no "
    "abstract geometric art, no floating holographic elements, no wireframe, "
    "no charts, no graphs, no dashboards, no data visualisation, no data "
    "centre, no server room, no server racks, no server aisles, no cable "
    "runs, no GPU racks, no racks of any kind, no robots, no drones, no "
    "lasers, no holograms."
)

COMMON = (
    "This is unposed documentary photojournalism caught in a single "
    "unrehearsed moment, not a staged commercial shot and not a hero render: "
    "the subject sits off-centre, the framing is loose and a little careless, "
    "and foreground elements cut into the edges of the frame. Honest "
    "available-light exposure, not a lit set and not an HDR composite. "
    "Shallow depth of field from a wide aperture on a long lens on a "
    "full-frame camera, real optical lens blur and creamy natural bokeh, "
    "unobtrusive film-like grain visible in the smooth mid-tones and the "
    "highlights, faint chromatic fringing on the high-contrast edges of "
    "bright metal, a subtle lens vignette, slight sensor softness in the "
    "shadows, real atmospheric haze in the depth of the room, fine airborne "
    "particles catching the light, worn and real textures with faint scuffs "
    "and handling marks on every surface, asymmetric unidealised composition, "
    "a slight hand-held tilt, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no immaculate retouched perfection, no 3D "
    "visualisation, no digital illustration, no concept-art lighting, no "
    "video-game aesthetic, photorealistic, very high detail, professional "
    "editorial stock photography for a business newspaper, 16:9 landscape "
    "composition."
)

PROMPTS = {
    # 1 — PRIMARY: cleanroom technician with a wafer beside an open FOUP and
    #     a lithography tool housing, cool overhead light, yellow bay glow.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 70-200mm lens "
        "at 135mm and f/2.8 on a full-frame camera from about ten feet away "
        "at chest height, of the interior of a semiconductor fabrication "
        "cleanroom. The main subject, tack sharp and slightly left of centre, "
        "faces away from the camera turned three-quarters to the side so only "
        "the back and side of the head and shoulders are visible: a "
        "technician sealed in a plain white bunny suit — a hood covering the "
        "head and ears, a white face mask, clear safety goggles, and white "
        "nitrile gloves — leaning slightly forward as they hold up and carry "
        "a gleaming 300mm silicon wafer in both gloved hands at waist height, "
        "the wafer's polished face tipped toward the light so its surface "
        "catches a broad iridescent rainbow sheen of violet, blue, teal, gold "
        "and pink diffraction across a fine repeating grid of plain "
        "rectangular die patterns that carry no readable characters of any "
        "kind. Their unbranded white suit is completely plain with no "
        "lettering. Immediately to the right of the technician stands an open "
        "front-opening unified pod — a pale grey plastic FOUP with its lid "
        "off and empty slot shelves visible inside — resting on the bare "
        "brushed-metal load port housing of a semiconductor lithography "
        "tool, a large matte grey machine body with rounded panels, thin "
        "seams, small polished stainless fasteners and a faint scuff of "
        "handling wear, its surface plain and completely unmarked with no "
        "plates, no screens, no stencilled codes and no labels. The floor is "
        "smooth seamless pale grey epoxy, polished and faintly reflective, "
        "with the soft blurry reflection of the technician's legs pooling "
        "beneath them. Overhead, long rows of cool white diffuse cleanroom "
        "lighting panels recede away from the camera down the length of the "
        "room, and far in the deep out-of-focus background a narrow "
        "lithography bay glows with a faint warm yellow-light strip beside "
        "pale grey wall panels and the blurred dark silhouettes of more "
        "equipment, all hazy and soft. The depth of field is shallow so the "
        "background melts into soft bokeh while the wafer and the gloved "
        "hands stay pin sharp. The room is quiet, austere and industrial, lit "
        "only by its own ceiling lighting. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — ALT: tight macro of a single 300mm wafer held in a gloved hand at a
    #     shallow angle, iridescent diffraction, cleanroom ceiling bokeh.
    "2": (
        "Photo-realistic editorial stock photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera from inches away, of a single "
        "300mm silicon wafer held at a shallow angle in a pair of white "
        "nitrile-gloved hands in a semiconductor cleanroom. The wafer fills "
        "most of the frame, tilted so the polished face catches a strong "
        "broad iridescent diffraction sweep of violet, deep blue, cyan, gold "
        "and rose pink across a dense fine repeating grid of plain "
        "rectangular die patterns, with a bright specular sheen sliding over "
        "the mirror-smooth surface and the wafer's crisp circular edge "
        "bright against the background. No readable characters appear "
        "anywhere on the wafer: only plain geometric die rectangles. The "
        "gloved fingers holding the wafer's edge are sharp and detailed, "
        "with faint creases and powder dust on the white nitrile and a plain "
        "unbranded cuff with no lettering. Behind the wafer, far out of "
        "focus, are the soft blurred bokeh spheres of overhead cleanroom "
        "ceiling lighting panels and the pale grey depth of the room. The "
        "lighting is cool, soft and diffuse with a slightly warm glint in "
        "the specular highlight. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — ALT: wide cleanroom aisle from behind a rack of FOUPs on a wafer
    #     transport system, technician walking away, real industrial scale.
    "3": (
        "Photo-realistic editorial stock photograph, shot on a 24mm wide lens "
        "at f/4 on a full-frame camera held at chest height, of a long wide "
        "aisle inside a semiconductor fabrication cleanroom seen from behind "
        "a rack of wafer pods. In the near foreground, cropped by the bottom "
        "and left edges of the frame and softly out of focus, sits a "
        "wafer transport system: a low pale grey overhead-track style rack "
        "carrying a neat row of front-opening unified pods, matte grey and "
        "pale translucent plastic carriers with dark thin seams and small "
        "polished metal handles, all perfectly plain and unmarked with no "
        "stencilled codes, no labels, no tags and no lettering. Beyond the "
        "rack the room opens into a long straight aisle flanked by rows of "
        "large matte grey semiconductor process tools with rounded panel "
        "forms, small status lamps glowing softly, thin panel seams and "
        "brushed stainless trim, their housings bare and completely unmarked. "
        "In the middle distance a single technician in a plain white bunny "
        "suit, hood and face mask walks directly away from the camera down "
        "the centre of the aisle, small in the frame, seen only from behind, "
        "their suit entirely unbranded with no lettering. The floor is "
        "seamless polished pale grey epoxy with soft faint reflections of the "
        "ceiling lights and the room's structure. Overhead, long parallel "
        "rows of cool white diffuse lighting panels run the full length of "
        "the aisle and recede to a vanishing point, with far equipment and "
        "wall panels dissolving into pale grey haze at the end of the room. "
        "The scale is real industrial scale — a vast, austere, quiet "
        "high-technology factory interior. No readable text anywhere. "
        + COMMON
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
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
