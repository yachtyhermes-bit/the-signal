#!/usr/bin/env python3
"""Regenerate hero for smr-nuscale-nuclear-licensing-moat-ai-power-2026.

Reason: the previous hero contained GARBLED / HALLUCINATED text — a wall sign
reading "NOSTE"/"NO3TE" and a monitor-plus-whiteboard sign that three separate
vision passes read as three different non-words ("Sophiat" / "Industrial
Automation Solutions", "Svenskt Kärnbränslehantering", "Cunnian / Sclution").
Every model run agreed the lettering was not real.

Scene brief: precision manufacturing of an advanced small modular reactor (SMR)
pressure-vessel module inside an industrial nuclear fabrication facility —
matching the published caption/alt text.

Hard rules for every attempt:
- PHOTO-REALISTIC editorial photograph only: no CGI, 3D render, illustration,
  cartoon, neon, synthwave, HUD, holograms, glowing lines.
- NO SCREENS, MONITORS, DISPLAYS, CONTROL PANELS, WHITEBOARDS, SIGNAGE, PLACARDS,
  POSTERS, LABELS, TAGS, STENCILS, GAUGES, DRAWINGS OR DATA PLATES anywhere.
- NO legible text at all: no words, letters, numbers, glyphs, code, logos, brand
  names, company marks — and no garbled pseudo-lettering either.
- Faces not clearly identifiable (seen from behind / in profile / out of focus).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-smr-nuscale-hero-20261006.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "smr-nuscale-nuclear-licensing-moat-ai-power-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any writing or marking whatsoever: no text, no words, "
    "no letters, no numbers, no digits, no glyphs, no characters, no code, no captions, no labels, "
    "no tags, no stickers, no decals, no stencilled markings, no placards, no signage, no posters, "
    "no notices, no paperwork, no documents, no clipboards, no whiteboards, no charts, no gauges, "
    "no data plates, no engraved markings, no brand names, no company logos, no watermarks, no "
    "signatures, and no garbled or pseudo-lettering of any kind. There are no screens of any sort "
    "in the frame — no monitors, no displays, no control panels, no terminals, no instrument "
    "readouts, no touch panels, no tablets, no laptops, no phones; every surface is plain and bare. "
    "Not an illustration, not digital art, not a cartoon, not a 3D render, not CGI, not a "
    "video-game look; no neon, no synthwave, no glowing holographic lines, no light trails, no "
    "futuristic HUD graphics, no augmented-reality overlays."
)

PROMPTS = {
    "1": (
        "Professional editorial stock photograph, shot on a full-frame camera with a 35mm lens at "
        "f/2.8, real available light, not a render: inside a spotless heavy-fabrication hall where "
        "advanced small modular reactor pressure vessels are built. The sharp subject filling the "
        "centre of frame is an enormous polished cylindrical stainless-steel reactor vessel shell, "
        "roughly three metres in diameter, lying horizontal in a set of heavy steel turning rollers. "
        "Its surface is brushed and mirror-bright, ringed by machined weld seams and a thick bolted "
        "flange collar at the near end, with a cluster of plain smooth coolant nozzles. To the right "
        "of the cylinder an engineer in a white hard hat, clear safety glasses and a pale grey "
        "coverall stands with their back three-quarters to the camera, one gloved hand resting flat "
        "on the steel, inspecting the surface — the face is turned away and not visible. The hall "
        "behind is honest and industrial: pale grey epoxy floor with faint painted walkway stripes, "
        "blue-grey steel columns, overhead gantry beams, warm-white high-bay lamps with soft flares, "
        "the far end of the building dissolving into gentle haze. Shot at f/2.8 with shallow depth of "
        "field: the vessel surface and the engineer's gloved hand tack sharp, the hall behind melting "
        "into creamy bokeh. Realistic textures — brushed steel, painted concrete, fabric, matte "
        "plastic; natural sensor noise, very slight film grain, subtle vignette, no CGI sheen, no "
        "perfect symmetry. Photorealistic, extremely high detail, 8k resolution, authentic editorial "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic documentary press photograph taken on a real camera, 50mm lens at f/2, "
        "shallow depth of field, not computer generated: a clean nuclear-grade machining bay where a "
        "large cylindrical pressure-vessel module for a small modular reactor is being finished. The "
        "frame is filled diagonally by the huge matte-grey painted steel shell, seen in three-quarter "
        "close view, its curved flank catching a long soft highlight from a window on the left; a "
        "thick machined flange with a circle of evenly spaced plain bolt holes sits at the near end, "
        "and short smooth pipe stubs project from the curve. A fine spray of coolant mist hangs in the "
        "air near the surface. In the soft-focus background a machinist in a dark work jacket and "
        "white hard hat stands in profile at the far side of the shell, head down, absorbed in the "
        "work, face not identifiable, holding a plain hand tool. The bay is plain and real: sealed "
        "pale-grey epoxy floor, ribbed steel wall panels in muted blue-grey, overhead crane rail, "
        "warm-white industrial lighting with gentle falloff into shadow, daylight from tall windows "
        "on the left as the dominant key light. Nothing self-lit, no neon, no glowing lines. Honest "
        "realistic texture on steel, paint, fabric and concrete; natural sensor noise, very slight "
        "film grain, subtle vignette, no plastic CGI sheen, no perfect symmetry. Photorealistic, "
        "extremely high detail, 8k resolution, authentic editorial photography, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic editorial stock photograph shot on a real camera, 24mm wide lens at f/4, not "
        "a render: the interior of a vast, immaculately clean nuclear fabrication hall photographed "
        "straight down the axis of an enormous hollow stainless-steel reactor pressure-vessel casing "
        "that recedes toward the viewer in strong circular perspective. The camera looks slightly up "
        "into the open end of the giant cylinder; concentric rings of machined steel, an inner liner "
        "and a ring of plain smooth bolt bosses frame a dark, deep interior that fades to black at "
        "the centre. The outer skin of the cylinder is brushed bright steel with clean circumferential "
        "weld bands and no markings whatever. At the left edge of frame, out of focus, the shoulders "
        "and back of an engineer in a white hard hat and light coverall are visible, leaning in to "
        "inspect the rim of the vessel, seen from behind so the face is hidden. Behind and around it "
        "the hall is enormous and honest: glossy pale-grey floor, tall steel columns, gantry cranes "
        "high overhead, warm-white high-bay lighting with soft lens flares, distant machinery "
        "dissolving into gentle atmospheric haze. Wide-angle perspective, deep focus on the cylinder "
        "rim with the far hall softly hazed, natural sensor noise, very slight film grain, subtle "
        "vignette, realistic steel and concrete texture, no CGI sheen, no perfect symmetry. "
        "Photorealistic, extremely high detail, 8k resolution, authentic editorial photography, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    "4": (
        "Photojournalistic candid documentary photograph shot on a Fujifilm X-T5 with a 23mm lens at "
        "f/2, real available light, unretouched, not a render and not CGI: a modern precision "
        "engineering facility where the thick stainless-steel shell of a small modular reactor is "
        "welded and ground to a flawless finish. In the sharp foreground the curved grey steel wall of "
        "the vessel sweeps across the bottom third of the frame, catching a soft sheen; a welder in a "
        "leather apron, dark sleeves and a white hard hat works at the curved seam, seen from behind "
        "and to the side so the face is not identifiable, one gloved hand guiding a plain welding "
        "torch, a soft glow at the arc but no harsh light. Behind them, in soft focus, a colleague in "
        "a pale coverall carries a plain steel bar; the hall stretches away with gantry beams, "
        "scaffold-like steel platforms and large windows flooding everything with cool soft daylight. "
        "The scene is richly textured and human: worn painted floors, tidy coiled cables, plain "
        "steel trestles, a white cloth bundle, realistic fabric, leather and steel surfaces, faint "
        "dust in the air. Genuinely imperfect candid composition, natural sensor grain, faint "
        "chromatic aberration at the frame edges, subtle motion blur on one passing figure, no studio "
        "lighting, no neon, no glowing lines, no perfect symmetry. Photorealistic, extremely high "
        "detail, authentic editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial press photograph shot on a 35mm lens at f/2.2 on a full-frame "
        "camera, not a render: a vertically framed industrial portrait of an advanced small modular "
        "reactor pressure-vessel module in a clean assembly hall. The tall matte-grey painted steel "
        "cylinder stands upright on a heavy steel base plate, occupying the centre of the frame; its "
        "surface is smooth and even, marked only by clean circumferential weld bands and a few plain "
        "smooth nozzle bosses — nothing written, stencilled or attached to it anywhere. Two riggers in "
        "white hard hats, dark navy work jackets and gloves stand at the left beside the base, seen "
        "from behind and in three-quarter rear profile with heads lowered over a plain chain sling, "
        "faces not identifiable. The hall around them is honest and industrial: pale grey epoxy floor, "
        "blue-grey ribbed steel walls, yellow gantry crane rail high above, warm-white high-bay lamps "
        "with soft flares, a hint of another seated figure far down the hall out of focus. Warm "
        "industrial lighting with real falloff and soft realistic shadows, nothing self-lit, no neon. "
        "Honest realistic texture on painted steel, fabric, gloves and concrete; natural sensor noise, "
        "very slight film grain, subtle vignette, no CGI sheen, no perfect symmetry. Photorealistic, "
        "extremely high detail, 8k resolution, authentic editorial photography, 16:9 landscape "
        "composition. " + NO_TEXT
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
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
