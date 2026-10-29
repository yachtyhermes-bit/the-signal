#!/usr/bin/env python3
"""Generate hero for arm-qualcomm-licensing-verdict-2026 (fal flux/schnell).

Subject: Arm Holdings (NASDAQ: ARM) — a semiconductor CPU architecture licensing
company. Article thesis: a Delaware jury found Arm breached its licensing
agreement with Qualcomm, and what that verdict says about Arm's
licensing / royalty business model (Arm sells architectural designs + royalties,
it does not sell finished chips).

Scene chosen: a PHOTO-REALISTIC editorial stock photograph of a bare processor
silicon die being inspected in a semiconductor lab. A macro close-up of a thin
silicon die / small wafer fragment held point-to-point in fine laboratory
tweezers above an anti-static work surface, with a probe-station / microscope
lens softly out of focus behind it. Fine bond-pad detail on the die, metallic
and dark in tone, professional directional lab lighting, very shallow depth of
field. 16:9 landscape.

Deliberately DISTINCT from recent heroes (all BANNED for this job):
- NOT a data-center aisle / server-rack corridor / server-room composition.
- NOT the 2026-10-13 MSFT Maia 300 hero (big square chip package still-life on
  a metal tray) — no single large sealed package on a tray.
- NOT the 2026-10-13 MU/CXMT hero (cleanroom technician in a bunny suit holding
  a 300mm wafer) — no person, no full round 300mm wafer held up.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: dies and lab gear naturally carry markings, so any legible
  marking — letters, numbers, lot codes, logos, signage, screen text,
  watermarks — is explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-arm-qualcomm-licensing-verdict-hero-20261013.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "arm-qualcomm-licensing-verdict-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image is completely free of any writing: no text, no letters, no "
    "numbers, no words, no digits, no part numbers, no serial numbers, no lot "
    "codes, no batch codes, no date codes, no QR codes, no barcodes, no "
    "datamatrix codes, no silkscreen printing, no laser-etched markings, no "
    "engraved characters, no stencilled characters, no labels, no stickers, no "
    "tags, no painted markings, no stamped symbols, no brand names, no "
    "manufacturer names, no product names, no logos, no logotypes, no "
    "trademarks, no watermark, no signature, no caption, no ruler or "
    "measurement graduations, no letter-like or typography-like markings of "
    "any kind anywhere in the image. The silicon die, the tweezers, the lab "
    "bench and every surface in the frame are entirely plain, bare and "
    "unmarked. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no glowing lines, no light trails, no synthwave, no "
    "geometric patterns, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no server rack, no server aisle, no server "
    "room, no data-center hallway, no cable runs."
)

PROMPTS = {
    "1": (
        "Photo-realistic macro stock photograph of a bare silicon processor die "
        "being inspected in a semiconductor laboratory, shot as professional "
        "editorial photography. A thin square semiconductor die — bare "
        "polished silicon with a fine grid of tiny metallic bond pads and "
        "delicate microscopic circuit regions across its surface — is held "
        "point-to-point in a pair of slim stainless-steel laboratory tweezers, "
        "gently pinching one corner of the die. The die is the hero of the "
        "frame, angled slightly toward the camera so its mirror-flat polished "
        "surface catches a soft sheen. Behind it, far out of focus, is the "
        "dark grey body and thin cabling of a probe station / optical "
        "microscope assembly on a matte anti-static work surface. Soft "
        "directional professional laboratory lighting — a cool white key light "
        "from the upper left with a faint warm rim light grazing the far edge "
        "of the tweezers. Extremely shallow depth of field from a macro lens: "
        "the near edge of the die and the tweezer tips are tack sharp with "
        "fine realistic surface micro-texture, while the microscope behind "
        "and the bench dissolve into smooth creamy bokeh. Shot on a 100mm "
        "macro lens at f/2.8, real optical bokeh, honest exposure, natural "
        "fine sensor grain, subtle lens vignette, realistic material "
        "textures with no plastic CGI sheen, no perfect symmetry, no glossy "
        "render. Photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "An authentic real-world macro photograph, not a render and not "
        "computer generated: an extreme close-up of a single bare silicon "
        "die held in fine laboratory tweezers for inspection in a "
        "semiconductor lab. The thin rectangular chip of polished silicon "
        "fills the centre of the frame, tilted just off the horizontal, its "
        "surface an unbroken mirror-expanse of dark grey and faint silver "
        "with delicate miniature circuit textures and a neat row of tiny "
        "metal bond pads along one edge. The slim steel tweezers grip the "
        "die's corner; beyond it, heavily blurred, sits the matte body of an "
        "optical microscope / probe station. Soft cool-white laboratory "
        "lighting from above with a subtle warm highlight skimming the metal "
        "of the tweezers. Very shallow depth of field: only the nearest "
        "portion of the die and the tweezer tips are sharp, everything else "
        "melting into smooth creamy bokeh. Natural fine film grain, slightly "
        "uneven real-world white balance, subtle lens vignette, real optical "
        "blur, no plastic CGI sheen, no airbrushed surfaces, no perfect "
        "symmetry, honest documentary realism, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A professional laboratory still-life stock photograph, shot handheld "
        "with a macro lens as editorial photography — a real photograph, not "
        "a render and not computer generated. A bare silicon semiconductor "
        "die, thin and square with rounded corners, is suspended between the "
        "fine points of a pair of laboratory tweezers above a matte dark-grey "
        "anti-static bench. The die's polished surface shows fine micro-"
        "engineering detail and faint shallow iridescence where the light "
        "grazes at a low angle, and its edges are thin and crisp. The tweezers "
        "are brushed stainless steel. In the softly blurred background sits "
        "the dark silhouette of an inspection microscope with gently out-of-"
        "focus controls. Soft directional studio lighting with a cool white "
        "key from one side and a warm rim light behind the opposite edge. "
        "Macro-lens shallow depth of field: the die and tweezer tips are tack "
        "sharp while the bench and microscope fall into creamy bokeh. Natural "
        "fine sensor noise, slightly uneven real-world white balance, a thin "
        "cool haze, subtle vignette, imperfect honest framing, real optical "
        "blur, honest exposure. Absolutely not a 3D visualisation, not a "
        "glossy CGI render, no airbrushed plastic surfaces, no digital sheen, "
        "no perfect symmetry, no digital illustration, no AI-generated look, "
        "photorealistic, high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "An authentic, slightly imperfect real-world macro photograph, shot "
        "handheld by a photographer with an 85mm macro lens wide open, of a "
        "bare silicon processor die being examined with fine tweezers in a "
        "semiconductor laboratory. The thin square chip of polished silicon "
        "rests at a shallow angle between the slim steel points of the "
        "tweezers, its mirror-like surface carrying delicate microscopic "
        "circuit patterns and a border of tiny flat metal bond pads, all "
        "plain and completely unmarked. The matte dark anti-static work "
        "surface below shows a few fine real dust specks and slight uneven "
        "wear, with the blurred grey mass of a probe station behind. Soft "
        "directional lab light from the upper left with a warm amber rim "
        "light catching the edge of the tweezers. Macro-lens shallow depth of "
        "field: only the nearest edge of the die and the metal of the "
        "tweezers are sharp; everything else is creamy natural bokeh. Heavy "
        "but natural sensor noise and real film grain, faint floating dust "
        "motes, a thin haze in the air, chromatic aberration on the "
        "high-contrast edges, subtle lens vignette, slightly crooked "
        "imperfect handheld framing, real optical blur, honest unretouched "
        "exposure. Absolutely not a 3D visualisation, not a glossy CGI "
        "render, no airbrushed plastic surfaces, no digital sheen, no perfect "
        "symmetry, no digital illustration, no AI-generated look, visibly a "
        "real camera photograph, photorealistic, high detail, professional "
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
