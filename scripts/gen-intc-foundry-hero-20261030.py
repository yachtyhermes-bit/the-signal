#!/usr/bin/env python3
"""Generate hero for intc-server-growth-foundry-loss-2026 (fal flux/schnell).

Subject: Intel Q3 2026 earnings — data-centre/server CPU growth against a
still-loss-making foundry business.

Frame: a SEMICONDUCTOR FAB CLEANROOM. NOT a data centre, NOT a server room,
NOT a test floor, NOT an assembly line.

Scene 1 (ATTEMPT=1): technician in a white bunny suit holding a mirror-polished
300mm wafer up at a slight angle, iridescent die pattern, FOUPs and a
lithography tool blurred behind, warm yellow cleanroom light.
Scene 2 (ATTEMPT=2): macro of a wafer edge in a gloved hand, thin-film
interference colours, defocused cleanroom behind.
Scene 3 (ATTEMPT=3): wide cleanroom corridor, lithography scanner and wafer
handling robots under yellow light, lone bunny-suited figure walking away.

BANNED: text/lettering/logos of any kind, neon, synthwave, glowing lines,
abstract digital art, geometric patterns, data centre, server racks, CGI look.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
          scripts/gen-intc-foundry-hero-20261030.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "intc-server-growth-foundry-loss-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
W, H = 1536, 864  # 16:9

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no lot numbers, no serial numbers, no etched part markings on "
    "the dies or wafers, no signage, no placards, no warning labels, no "
    "safety posters, no labels, no tags, no stickers, no decals, no painted "
    "markings on machinery, no machine nameplates, no data plates, no asset "
    "tags, no inventory stickers, no illuminated indicator words, no brand "
    "names, no manufacturer names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no barcodes, no QR codes, no data-matrix "
    "codes, no wafer scribe lettering, no legible writing of any kind "
    "anywhere in the image. No silkscreen printing, no ink of any kind on "
    "any surface, no printed markings on the wafer or on the FOUP carriers, "
    "no lettering on the tiny components, no control panel, no keypad and no "
    "buttons visible in frame at all. Any display, monitor or machine readout "
    "is entirely blank, dark or softly out of focus with no readable content. "
    "Every surface, machine panel, carrier and wafer is plain and unmarked. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no overlay graphics, "
    "no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no data centre, no server room, no server racks, no "
    "server aisles, no cable runs, no GPU racks."
)

COMMON = (
    "Warm yellow cleanroom lighting from recessed ceiling fixtures with "
    "soft ambient fill, true colour, honest available-light exposure, "
    "depth of field that keeps the subject plane crisp and lets only the "
    "far background soften into natural optical blur, creamy bokeh where "
    "it occurs, subtle sensor noise, very slight film grain, gentle lens "
    "vignette, faint chromatic fringing on high-contrast edges, no plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no retouched "
    "hyper-clean digital look, an actual photograph taken on a real camera "
    "with a prime lens, photorealistic, very high detail, professional "
    "editorial stock photography, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — technician holding a mirror-polished 300mm wafer up to the light.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/2.0 wide open on a full-frame camera, inside a modern "
        "semiconductor fabrication cleanroom. At the centre of frame, tack "
        "sharp, a technician dressed in a white full-body bunny suit with "
        "hood, face mask and powder-free white gloves stands at a "
        "three-quarter angle and holds a single large mirror-polished 300mm "
        "silicon wafer up at a slight angle between both gloved hands, the "
        "way a person holds a record. The wafer fills a generous part of the "
        "frame as a perfect thin polished disc whose face is an iridescent "
        "rainbow of thin-film interference — soft bands of magenta, cyan, "
        "green and gold sliding across a fine unbroken grid of identical "
        "rectangular die, with one broad specular highlight sweeping across "
        "the polished surface and a clean dark rim at the very edge. The "
        "die grid is perfectly plain: no scribe lettering, no codes, no "
        "printed marks of any kind. The technician's hood, mask and gloves "
        "are soft matte white fabric and nitrile with visible real folds and "
        "honest creases, the mask covering nose and mouth, only the eyes "
        "visible above it. Behind the figure, thrown well out of focus into "
        "creamy bokeh, stand a rack of sealed translucent front-opening "
        "wafer carriers holding stacks of wafers, and the pale grey "
        "machined flank and dark window of a lithography scanner, its "
        "surfaces plain and unmarked. The floor is a polished epoxy grey "
        "with faint reflections. Soft warm light rakes from the upper left, "
        "gentle shadow falloff on the right. " + COMMON + NO_TEXT
    ),
    # 2 — macro of a wafer edge in a gloved hand.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, a tight close-up inside a "
        "semiconductor fabrication cleanroom. The frame is filled by the "
        "curved edge of a single large mirror-polished silicon wafer held at "
        "a low angle in a powder-free white-gloved hand, the gloved "
        "fingertips entering from the lower right and gripping the rim with "
        "visible real fabric texture and honest creases. The wafer edge "
        "sweeps across the frame as a thin bright arc of polished silicon, "
        "and the surface behind it glows with intense thin-film "
        "interference colours — iridescent magenta, teal, gold and violet "
        "banding sliding across a fine unbroken grid of identical "
        "rectangular die with no scribe lettering, no codes and no printed "
        "marks anywhere. A razor-thin specular highlight traces the very "
        "edge of the wafer and one die corner in the near field is tack "
        "sharp while the rest of the surface falls away into soft optical "
        "blur. No ring of tiny characters around the wafer perimeter, no "
        "curved lettering following the edge, no laser-scribe marks, no "
        "serial digits in the flat zone at the edge. "
        "Behind, far out of focus, the pale grey machinery of a "
        "cleanroom dissolves into warm yellow bokeh with the vague shape of "
        "a sealed wafer carrier. Warm light from the upper left. "
        + COMMON + NO_TEXT
    ),
    # 3 — wide cleanroom corridor, scanner and robots, lone figure walking away.
    "3": (
        "Photo-realistic documentary press photograph, shot on a 35mm lens at "
        "f/4 on a full-frame camera at chest height, looking straight down the "
        "length of a long wide semiconductor fabrication cleanroom bay under "
        "warm yellow-white ceiling light. The space reads unmistakably as a "
        "chip fab: a broad corridor with a light grey epoxy floor, pale "
        "powder-coated wall panels, sealed ceiling tiles and continuous "
        "recessed light panels running away in strong perspective toward a "
        "bright vanishing point at the far end, the far end softly hazed but "
        "still legible as architecture. Most of the frame is in reasonable "
        "focus, with only the last twenty metres softening. In the middle "
        "distance, a lone technician in a white full-body bunny suit with "
        "hood and mask walks away from the camera down the centre of the "
        "aisle, seen from behind, mid-stride, small in the frame, one arm "
        "relaxed at the side. On the right of the corridor stands a "
        "lithography scanner bay: a large rectangular pale grey machine with "
        "matte machined panels, a dark inset viewing window, an open load "
        "port and a small articulated wafer-handling robot arm beside it "
        "holding a translucent carrier of stacked wafers. On the left, a "
        "low metal rack holds several sealed front-opening wafer carriers, "
        "their translucent shells showing neat stacks of wafers inside. All "
        "machine panels, wall panels, floor and carriers are plain, matte "
        "and completely unmarked. The palette is muted and industrial — "
        "grey, bone white, aluminium and warm amber ceiling light — with no "
        "saturated magenta, purple, teal or rainbow lighting and no coloured "
        "neon bokeh anywhere. Ceiling lights reflect as soft vertical streaks "
        "on the polished floor. Honest industrial hardware, faint wear and "
        "dust on the metal, natural falloff into shadow at the frame edges. "
        + COMMON + NO_TEXT
    ),
}


def load_fal_key():
    env_paths = [
        "/home/chino/.hermes/profiles/yachty/.env",
        "/home/chino/thesignal/.env",
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
    if size > 400000:
        img.save(OUTPUT, "JPEG", quality=88, optimize=True)
        print("Re-saved under 400KB: %s bytes" % os.path.getsize(OUTPUT))
    if os.path.getsize(OUTPUT) > 400000:
        img.save(OUTPUT, "JPEG", quality=84, optimize=True)
        print("Re-saved again: %s bytes" % os.path.getsize(OUTPUT))


if __name__ == "__main__":
    main()
