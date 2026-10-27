#!/usr/bin/env python3
"""Generate hero for amkr-advanced-packaging-ai-backend-2026 (fal flux/schnell).

Subject: Amkor Technology — OSAT (outsourced semiconductor assembly and test).
Advanced packaging: organic substrates, die attach, flip chip, 2.5D interposers
carrying HBM stacks, panel-level processing, final test. This is the back-end
step between the fab and the AI accelerator.

Frame: a PACKAGING / ASSEMBLY cleanroom. NOT a data centre, NOT a server room,
NOT a front-end lithography bay.

Scene 1 (ATTEMPT=1): technician in a white bunny suit and gloves holding a
substrate strip of chip packages up to the light at a bench.
Scene 2 (ATTEMPT=2): pick-and-place head placing a die onto an organic
substrate panel on a packaging line.
Scene 3 (ATTEMPT=3): macro of a finished AI accelerator package — central die
ringed by HBM stacks on a substrate, package lid lifted away.

BANNED: text/lettering/logos of any kind, neon, synthwave, glowing lines,
abstract digital art, geometric patterns, data centre, server racks, CGI look.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
          scripts/gen-amkr-advanced-packaging-hero-20261027.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amkr-advanced-packaging-ai-backend-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
W, H = 1536, 864  # 16:9

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no lot numbers, no serial numbers, no etched part markings on "
    "the dies or substrates, no signage, no placards, no warning labels, no "
    "safety posters, no labels, no tags, no stickers, no decals, no painted "
    "markings on machinery, no machine nameplates, no data plates, no asset "
    "tags, no inventory stickers, no illuminated indicator words, no brand "
    "names, no manufacturer names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no barcodes, no QR codes, no data-matrix "
    "codes, no wafer scribe lettering, no legible writing of any kind "
    "anywhere in the image. No silkscreen printing, no ink of any kind on "
    "any surface, no printed markings on the substrate, no lettering on the "
    "tiny components, no control panel, no keypad and no buttons visible in "
    "frame at all. Any display, monitor or machine readout is entirely "
    "blank, dark or softly out of focus with no readable content. Every "
    "surface, machine panel, tray and substrate is plain and unmarked. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no overlay graphics, "
    "no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no data centre, no server room, no server racks, no "
    "server aisles, no cable runs, no GPU racks."
)

COMMON = (
    "Warm neutral cleanroom lighting from recessed ceiling fixtures with "
    "soft ambient fill, true colour, honest available-light exposure, "
    "shallow depth of field with real optical lens blur and creamy natural "
    "bokeh, subtle sensor noise, very slight film grain, gentle lens "
    "vignette, faint chromatic fringing on high-contrast edges, no plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no retouched "
    "hyper-clean digital look, an actual photograph taken on a real camera "
    "with a fast prime lens, photorealistic, very high detail, professional "
    "editorial stock photography, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — technician holding a substrate strip of packages up to the light.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/2.0 on a full-frame camera, inside a semiconductor packaging and "
        "assembly cleanroom. In the centre of frame, tack sharp, a technician "
        "dressed in a white full-body bunny suit with hood, face mask and "
        "powder-free white gloves holds a long narrow rectangular strip of "
        "organic package substrate up in both hands at chest height, "
        "examining it against the light. The strip is a flat bar of matte "
        "green-grey laminate carrying a neat row of six identical finished "
        "chip packages: each a small square with a smooth mirror-polished "
        "silicon die in the middle, faintly iridescent slate grey, "
        "surrounded by a plain dark moulded body, edges razor straight, the "
        "substrate surface one unbroken uniform tone with no printing, no "
        "etched lettering and no marked components anywhere. The gloved "
        "fingertips grip the strip at its extreme ends so the whole row of "
        "packages sits unobstructed across the middle of the frame, "
        "catching long soft highlights along their polished faces. The "
        "technician's hooded head is turned in three-quarter view away from "
        "the camera, only the smooth white fabric of the hood and the "
        "shadowed curve of the mask visible, face unidentifiable. Behind "
        "them, out of focus and rendered only as soft pale grey and steel "
        "shapes, the cleanroom bench holds a stack of black slotted "
        "carrier magazines, a shallow anti-static tray and the dark hood of "
        "an inspection microscope, dissolving into warm haze. Soft warm "
        "light rakes from the upper left, gentle shadow falloff on the "
        "right. " + COMMON + NO_TEXT
    ),
    # 2 — pick-and-place head placing a die on an organic substrate panel.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, at a panel-level advanced "
        "packaging line inside a semiconductor assembly cleanroom. At the "
        "centre of frame, crisp and tack sharp, a precision pick-and-place "
        "toolhead has just descended onto a large flat organic packaging "
        "panel clamped on a heated stage: a slender machined aluminium "
        "nozzle holds a single small mirror-bright silicon die a hair's "
        "breadth above its landing site. The panel beneath is a wide "
        "rectangular field of polished green-grey laminate carrying a plain "
        "grid of smooth square die sites and fine rows of soft solder "
        "bumps, its surface one uniform unbroken tone with no printing, no "
        "etched lettering, no marked components and no silkscreen anywhere, "
        "dust-free and gleaming under the light. Around the toolhead, the "
        "machine body is pale grey and stainless steel with brushed "
        "aluminium rails, small servo motors and neat translucent pneumatic "
        "tubing, unmistakably real industrial hardware with faint wear on "
        "the metal and a warm reflection down its machined flank; no screen "
        "and no control panel faces the camera. In the sharp near "
        "foreground, partly cropped, two open flat trays hold rows of "
        "finished large packages with exposed central dies ringed by memory "
        "stacks, a stainless steel vacuum tweezer resting beside them. In "
        "the mid-ground, softly blurred, a row of identical machines "
        "recedes into warm cleanroom haze. " + COMMON + NO_TEXT
    ),
    # 3 — macro of a finished AI accelerator package, lid lifted away.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, a tight three-quarter "
        "close-up of a single finished advanced AI accelerator package "
        "resting on a sheet of black anti-static foam on a cleanroom "
        "bench. The package fills the lower two thirds of the frame: a "
        "large square organic substrate of matte green-grey laminate, and "
        "at its centre a smooth mirror-polished silicon interposer die that "
        "catches a soft broad highlight across its plain iridescent grey "
        "face. Ringed tightly around the central die sit eight separate "
        "rectangular high-bandwidth memory stacks of thin stacked dies, "
        "their edges softly defined, faces a milky gloss. A brushed "
        "stainless steel package lid, its inner face plain and unmarked, is "
        "held slightly raised above the package at the upper right by a "
        "white-gloved hand whose fingers and wrist fall softly out of focus "
        "into the background. The laminate between the components is a wide "
        "unbroken uniform tone with no printing, no serial marks, no "
        "lettering and no marked components anywhere. Warm cleanroom light "
        "rakes across the top of the package from the upper left with dark "
        "falloff behind it, and the background dissolves into soft warm "
        "bokeh of bench equipment. " + COMMON + NO_TEXT
    ),
}


def load_fal_key():
    env_paths = [
        "/home/chino/.hermes/profiles/yachty/.env",
        "/home/chino/hermes-workspace/studio-api/.env",
    ]
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.strip().startswith("FAL_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
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
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + str(image_url))
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: %s  size=%s  bytes=%s" % (out_path, img.size, len(r.content)))
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT).convert("RGB")
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: %s  dimensions=%s  bytes=%s" % (OUTPUT, img.size, size))
    if size > 2000000:
        img.save(OUTPUT, "JPEG", quality=85, optimize=True)
        print("Re-saved under 2MB: %s bytes" % os.path.getsize(OUTPUT))


if __name__ == "__main__":
    main()
