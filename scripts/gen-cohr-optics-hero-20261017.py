#!/usr/bin/env python3
"""Generate hero for cohr-optics-selloff-sold-out-capacity-2026 (fal flux/schnell).

Subject: Coherent Corp (NYSE: COHR) — indium phosphide (InP) lasers, EMLs,
optical transceivers and co-packaged-optics components that move data between
AI servers. The story is AI OPTICAL INTERCONNECT / photonics manufacturing,
not data centers as buildings.

Scene chosen (per task brief, must be visually distinct from recent heroes):
a PHOTONICS / LASER MANUFACTURING scene — a cleanroom technician in a bunny
suit inspecting a glowing indium-phosphide wafer under amber-lit inspection
equipment on a precision optical bench. Shallow depth of field, professional
lighting, cinematic but documentary in feel.

Deliberately NOT a data-center hallway / server aisle / server racks / cable
runs. No abstract or digital art, no neon or synthwave, no glowing geometric
lines, no fake charts.

Rules:
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon,
  synthwave, CGI, 3D render, cartoon, glowing lines, light trails, HUD.
- TEXT-FREE: no letters, numbers, labels, logos, brand names, watermarks.
- FACES not clearly readable (visor/hood, side/behind, out of focus).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-cohr-optics-hero-20261017.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "cohr-optics-selloff-sold-out-capacity-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no silkscreen text, no instrument "
    "reading showing characters, no brand names, no logos, no watermark, no "
    "captions, no legible writing of any kind anywhere. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no synthwave, no "
    "glowing geometric lines, no light trails, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no charts, no "
    "graphs, no data visualization. Not a data-center hallway, no server "
    "aisle, no server racks, no rack of blinking lights, no cable runs "
    "through a building."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with an 85mm lens at f/2, real available light, not a render "
        "and not CGI: inside a semiconductor photonics fabrication cleanroom, a "
        "laser-diode manufacturing area. In the sharpest focus in the centre of "
        "frame, a gloved hand in a white cleanroom glove holds a thin "
        "indium-phosphide semiconductor wafer with fine tweezers above the "
        "stainless-steel stage of an optical inspection station. The wafer is a "
        "mirror-like disc, faintly iridescent in pale gold and violet where the "
        "light catches the epitaxial thin films, its surface divided into a "
        "fine grid of tiny laser-diode dies. A low amber-tinted inspection "
        "lamp throws a narrow warm pool of light across the wafer and the "
        "polished stage, while the rest of the room stays in cool neutral "
        "cleanroom white. Behind and slightly above, a technician in a full "
        "white cleanroom bunny suit, hood and safety glasses leans over a "
        "binocular inspection microscope, seen from behind and in three-quarter "
        "profile so the face is turned away and not identifiable. On the bench "
        "beside the stage sit a black wafer carrier cassette, a small tray of "
        "gold-plated optical submounts and a short coil of thin single-mode "
        "fiber-optic pigtail. Very shallow depth of field: the wafer, the "
        "tweezers and the gloved fingertips are razor sharp while the "
        "microscope, the technician and the white cleanroom walls dissolve into "
        "smooth creamy bokeh. Real optical lens blur, honest available-light "
        "exposure, natural sensor noise, fine film grain, subtle vignette, "
        "tactile realistic textures on metal, glass and fabric, no plastic CGI "
        "sheen, no perfect symmetry, faint dust and machining marks. "
        "Photorealistic, extremely high detail, authentic editorial "
        "photography, 16:9 landscape composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "2": (
        "Photo-realistic macro editorial photograph shot on a 100mm macro lens "
        "at f/2.8, real camera optics, not a 3D render: extreme close-up on a "
        "precision optical assembly bench of a photonics components lab. The "
        "sharp focal point is a gold-plated optical transceiver module — a "
        "small rectangular metal housing with finely machined edges, tiny "
        "gold-plated pins and a polished gold-plated lid — seated in a machined "
        "fixture, with a flat fiber-optic ribbon cable of twelve thin strands "
        "plugged into its front port, the ribbon curving away across the bench. "
        "A fine gold bond wire and a miniature indium-phosphide laser diode die "
        "are visible at the open end of the housing under a small bench light. "
        "The bench is matte dark grey with a scatter of precision tools: fine "
        "tweezers, a tiny torque driver, a ceramic-tipped probe. Warm "
        "tungsten-amber task light from the upper left rakes across the gold "
        "plating, with cool daylight fill from behind, honest specular "
        "highlights and real shadows. Deeply blurred background: out-of-focus "
        "stainless lab equipment, a reel of optical fiber, a plain white wall. "
        "Very shallow depth of field, sharp only on the transceiver's front "
        "port and the first centimetres of the ribbon. Real macro-lens bokeh, "
        "natural sensor noise, faint dust motes, fine film grain, slight "
        "chromatic aberration at the frame edges, subtle vignette, no plastic "
        "CGI sheen, no perfect symmetry. Photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape composition, "
        "wide horizontal framing. "
        + NO_TEXT
    ),
    "3": (
        "Photojournalistic candid documentary photograph, shot on a Fujifilm "
        "X-T5 with a 56mm lens at f/1.8, available cleanroom light, unretouched, "
        "not a render and not CGI: a laser-diode fabrication cleanroom. A "
        "technician in a white bunny suit, hairnet and safety glasses stands at "
        "a stainless-steel inspection bench, seen from the side and slightly "
        "behind, leaning in to examine a small indium-phosphide laser diode bar "
        "mounted in a copper submount beneath a low amber inspection lamp that "
        "casts a warm glow over the work area. The tiny gold-coated diode "
        "facet catches a pinpoint of warm light. Both gloved hands rest on the "
        "bench, one holding fine tweezers; the face is turned away behind the "
        "hood and glasses and is not identifiable. On the bench: a black wafer "
        "cassette, a magnifier on a boom arm, a short loop of single-mode fiber "
        "with a small connector, and a row of identical machined modules on a "
        "clean mat. The room behind is bright diffuse cleanroom white — plain "
        "walls, ceiling panels, a laminar-flow hood and a second operator in "
        "soft blur far down the bench. Genuinely imperfect candid framing, very "
        "shallow depth of field with the diode bar and the technician's hands "
        "sharp and everything else melting into creamy bokeh. Real lens blur, "
        "natural sensor grain, faint chromatic aberration, realistic fabric and "
        "metal texture, no studio lighting, no neon, no glowing lines. "
        "Photorealistic, extremely high detail, authentic editorial "
        "photography, 16:9 landscape composition, wide horizontal framing. "
        + NO_TEXT
    ),
    "4": (
        "Photo-realistic editorial press photograph taken on a real camera with "
        "a 35mm lens at f/2.2, wide horizontal composition, not computer "
        "generated: the interior of a photonics manufacturing cleanroom where "
        "indium-phosphide laser wafers are processed. Across the middle of the "
        "frame, a polished stainless-steel inspection bench holds an open "
        "wafer-inspection machine, its amber-ringed illuminator glowing softly "
        "over a vacuum chuck. A technician in a full white cleanroom bunny suit "
        "and hood stands at the machine seen from behind and in three-quarter "
        "profile, both gloved hands guiding a thin iridescent wafer onto the "
        "chuck with a vacuum wand; the face is hidden by the hood so it is not "
        "identifiable. Warm amber light from the inspection head falls on the "
        "wafer and the gloves, contrasting with the cool white cleanroom "
        "ambience of the rest of the room. To the right, softly out of focus, a "
        "black wafer cassette rack and a cart of sealed component trays; to the "
        "left, a second inspection station with a binocular microscope. Very "
        "shallow depth of field with the technician's hands, the wafer and the "
        "chuck sharp, and the room and the machinery behind melting into creamy "
        "bokeh. Real optical blur, natural sensor noise, fine film grain, "
        "honest real-world white balance, subtle vignette, believable dust and "
        "machining marks, no CGI sheen, no glossy render look, no perfect "
        "symmetry. Photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
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
