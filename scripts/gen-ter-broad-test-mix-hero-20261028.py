#!/usr/bin/env python3
"""Generate hero for ter-broad-test-mix-2026 (fal flux/schnell).

Subject: Teradyne (NASDAQ: TER) — automated test equipment (ATE). The machines
that test AI accelerators, HBM/DRAM memory stacks, hard drives and networking
silicon. Q3 2026 was a record: revenue +70%, memory test and HDD / Integrated
Systems Test at all-time highs, robotics profitable.

Frame: a SEMICONDUCTOR TEST floor / test lab. NOT a data centre, NOT a server
room, NOT a fab lithography bay, NOT an assembly line.

Scene 1 (ATTEMPT=1): technician in a white bunny suit lowering a probe card
onto a mirror-polished 300mm wafer on a probe station, microscope above.
Scene 2 (ATTEMPT=2): robotic chip handler lowering a packaged chip into a test
socket on a green device interface board.
Scene 3 (ATTEMPT=3): macro of a probe card — radial field of fine tungsten
probe needles fanning from a circular PCB.

BANNED: text/lettering/logos of any kind, neon, synthwave, glowing lines,
abstract digital art, geometric patterns, data centre, server racks, CGI look.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
          scripts/gen-ter-broad-test-mix-hero-20261028.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ter-broad-test-mix-2026")
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
    # 1 — probe card lowered onto a 300mm wafer on a probe station.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/2.0 on a full-frame camera, inside a semiconductor test laboratory. "
        "At the centre of frame, tack sharp, a technician dressed in a white "
        "full-body bunny suit with hood, face mask and powder-free white "
        "gloves stands at a three-quarter angle, both gloved hands carefully "
        "lowering a circular probe card assembly down onto a wafer. Beneath "
        "the card, a mirror-polished 300mm silicon wafer sits flat on the "
        "dark precision stage of a probe station, its surface a smooth "
        "iridescent grey-blue sheen catching a soft broad highlight, divided "
        "into a plain unbroken grid of identical die with no lettering, no "
        "scribe marks and no printed codes anywhere. The probe card is a "
        "thick anodised dark circular carrier ring with a dense field of "
        "fine metallic needles facing down toward the wafer, hovering a "
        "hair's breadth above it. Above the wafer, the machined dark barrel "
        "and objective of a microscope leans in from the upper right, softly "
        "defocused. The prober stage and its cast aluminium chassis fill the "
        "lower frame with faint wear and honest machined texture, plain and "
        "unmarked. Behind, dissolving into warm haze, the shapes of other "
        "test equipment and instrument racks are blurred to soft pale grey "
        "and steel forms. Soft warm light rakes from the upper left, gentle "
        "shadow falloff on the right. " + COMMON + NO_TEXT
    ),
    # 2 — robotic handler placing a packaged chip into a test socket.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, at an automated test system "
        "inside a semiconductor test cleanroom. At the centre of frame, "
        "crisp and tack sharp, a precision pick-and-place handler arm has "
        "just descended: a slender machined aluminium vacuum nozzle holds a "
        "single small dark rectangular packaged chip a hair's breadth above "
        "an open test socket. The socket sits on a large flat green device "
        "interface board, its surface a wide unbroken field of deep "
        "bottle-green laminate carrying rows of fine gold contact pads and "
        "plain hardware, with no printing, no silkscreen, no etched "
        "lettering and no marked components anywhere. The socket itself is "
        "dark machined plastic with a fine lattice of gold spring pins "
        "glinting faintly inside. Around it, the test system is brushed "
        "stainless steel and pale grey machined aluminium with precise "
        "guide rails, a linear actuator, small servo motors and neat "
        "translucent pneumatic tubing, unmistakably real industrial hardware "
        "with faint wear on the metal and a warm reflection down its "
        "machined flank; no screen and no control panel faces the camera. "
        "In the sharp near foreground, partly cropped, a shallow anti-static "
        "tray holds rows of identical chips and a stainless steel vacuum "
        "tweezer rests beside it. In the mid-ground, softly blurred, a row "
        "of identical test systems recedes into warm cleanroom haze. "
        + COMMON + NO_TEXT
    ),
    # 3 — macro of a probe card, radial tungsten needles.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, a tight close-up of a probe "
        "card resting on a dark test bench in a semiconductor test lab. The "
        "card fills the lower two thirds of the frame at a low three-quarter "
        "angle: a circular printed circuit board of deep matte green-black "
        "laminate, its face plain and unmarked with no printing and no "
        "silkscreen, and from its centre a dense radial field of fine "
        "tungsten probe needles fans out and downward — dozens of hair-thin "
        "metallic needles with an unmistakable springy taper, each catching "
        "a tiny specular highlight, their tips converging toward the camera. "
        "One single needle at the front of the fan is tack sharp and in "
        "perfect focus, its polished tungsten tip visibly bent to a point, "
        "while the rest of the field falls off into creamy optical blur. A "
        "white-gloved fingertip, softly out of focus, steadies the edge of "
        "the board at the upper right. The machined metal housing ring "
        "around the board is brushed and faintly worn. Warm light rakes "
        "across the needles from the upper left with dark falloff behind, "
        "and the background dissolves into soft warm bokeh of bench "
        "equipment. " + COMMON + NO_TEXT
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
