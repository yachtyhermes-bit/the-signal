#!/usr/bin/env python3
"""Generate hero for tenb-exposure-management-platform-margin-2026 (fal flux/schnell).

Subject: Tenable (NASDAQ: TENB) — exposure management / cybersecurity. The
discipline of inventorying everything an organisation owns and understanding
what of it is exposed.

Frame: PEOPLE AT WORK in a real office. NOT a data centre, NOT a server room,
NOT a server aisle, NOT racks of blinking lights.

Scene 1 (ATTEMPT=1): woman security analyst at her desk at dusk, over-shoulder,
two monitors out of focus.
Scene 2 (ATTEMPT=2): empty corporate workspace at night, one lit monitor turned
away from camera, coat on a chair.
Scene 3 (ATTEMPT=3): macro of a brass padlock and steel hasp on a worn wooden
door in an ordinary corridor.

BANNED: text/lettering/logos of any kind, neon, synthwave, glowing lines,
abstract digital art, geometric patterns, floating UI, dashboards overlaid on
hands, CGI look, data centre / server rooms.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
          scripts/gen-tenb-exposure-management-hero-20261028.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "tenb-exposure-management-platform-margin-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
W, H = 1536, 864  # 16:9

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no signage, no "
    "placards, no wall signs, no exit signs, no posters, no whiteboards with "
    "writing, no labels, no tags, no stickers, no decals, no name badges, no "
    "lanyards with printed names, no printed documents, no newspapers, no "
    "book covers with titles, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no watermarks, no "
    "barcodes, no QR codes, no legible writing of any kind anywhere in the "
    "image. Every computer monitor, laptop screen and phone display in the "
    "frame is either switched off, blank dark grey, or so softly out of "
    "focus that no content whatsoever is readable — absolutely no visible "
    "user interface, no menu bars, no window chrome, no code, no email, no "
    "spreadsheet, no chat, no thumbnails, no icons, no cursor and no "
    "recognisable application on any screen. Every surface, wall, desk and "
    "object is plain and unmarked. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no abstract geometric art, no floating "
    "holographic elements, no holograms, no overlay graphics, no wireframe, "
    "no glowing network mesh, no charts, no graphs, no dashboards, no data "
    "visualisation, no augmented-reality layers, no graphics superimposed "
    "over the scene, no data centre, no server room, no server racks, no "
    "server aisles, no cable runs, no GPU racks."
)

COMMON = (
    "Honest available-light exposure, true colour, shallow depth of field "
    "with real optical lens blur and creamy natural bokeh, subtle sensor "
    "noise at high ISO, very slight film grain, gentle lens vignette, faint "
    "chromatic fringing on high-contrast edges, a little motion softness in "
    "the foreground, imperfect and lived-in, no plastic CGI sheen, no "
    "glossy render, no perfect symmetry, no retouched hyper-clean digital "
    "look, an actual photograph taken on a real camera with a fast prime "
    "lens, photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — woman security analyst at her desk at dusk, over the shoulder.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens "
        "wide open at f/1.8 on a full-frame camera from just over the right "
        "shoulder of a woman security analyst seated at her desk in a real "
        "open-plan office at dusk. She is tack sharp and centred slightly "
        "left of frame, seen three-quarters from behind: a woman in her "
        "thirties with dark hair loosely tied back, wearing a plain charcoal "
        "knitted jumper, her shoulders relaxed, one hand resting on the "
        "desk beside a mouse, her head turned slightly toward the monitors. "
        "In front of her two large monitors stand side by side, angled away "
        "from the camera and thrown far out of focus so that their screens "
        "are nothing but soft glowing pale rectangles of cool blue-white "
        "light with no readable content at all. On the desk in the sharp "
        "near foreground: a shallow stack of plain unprinted papers, a "
        "black biro, a white ceramic coffee cup with visible coffee ring "
        "stains, a pair of reading glasses folded shut and a small potted "
        "succulent. A brass desk lamp with a dark green shade sits at the "
        "left of the monitors, switched on, throwing a warm pool of "
        "amber light across the desk surface and the side of her face and "
        "shoulder, while the room behind her falls into cool blue evening "
        "ambient light. Behind her, softly defocused, the tall windows of "
        "the office show a deep blue dusk sky and out-of-focus city lights "
        "as warm scattered bokeh points, with the skeletal shapes of "
        "distant buildings barely readable. Other empty desks with dark "
        "monitors recede into the blurred background. " + COMMON + NO_TEXT
    ),
    # 2 — empty corporate workspace at night, one lit monitor turned away.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera, standing in the aisle of an empty "
        "open-plan corporate office late at night. Rows of identical pale "
        "grey desks recede diagonally toward the back of the room, most of "
        "them dark and unused, their monitors black and switched off. In "
        "the mid-ground at the left of frame, a single monitor is still "
        "switched on and glowing, its back turned to the camera so only the "
        "plain matte plastic rear housing and the thin stand are visible, "
        "casting a cold white spill of light onto the desk surface and the "
        "carpet below it. A dark wool overcoat is slung over the back of one "
        "office chair nearby, and a canvas shoulder bag hangs from another. "
        "The desks carry ordinary lived-in clutter: a half-empty paper cup, "
        "a tangle of charging cables, a closed notebook, a set of keys, a "
        "wilted plant in a plain pot, a worn chair with a creased seat "
        "cushion. In the sharp near foreground a single desk edge and the "
        "arm of a chair are cropped and slightly out of focus. The far wall "
        "is plain painted plaster with no decoration, and the ceiling "
        "strip lights are mostly off, leaving only a couple of dim warm "
        "pools of light down the aisle. The whole room is quiet, depleted "
        "and slightly melancholy, lit by cold monitor glow against warm "
        "far-off ceiling light. " + COMMON + NO_TEXT
    ),
    # 3 — macro of a brass padlock on a worn wooden door.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, a tight close-up of a heavy "
        "solid brass padlock hanging closed through a blackened steel hasp "
        "on the door of an ordinary building in a plain corridor. The "
        "padlock fills the left-centre of the frame at a low three-quarter "
        "angle and is tack sharp: its body is dull tarnished brass with "
        "soft dark patina in the recesses, fine scratches and small dents "
        "from years of use, a thick chrome-steel shackle seated through the "
        "hasp, and a plain keyway with no engraving and no stamped marks of "
        "any kind on its face. The hasp is screwed into a worn painted "
        "wooden door frame with visible flat-head screws, the paint thickly "
        "built up and chipped at the edges, the timber grain raised and "
        "greasy where hands have pushed it. Behind, out of focus, the door "
        "itself is plain varnished wood with no notices, no plates, no "
        "numbers and no lettering. A hard raking side light comes from the "
        "upper right, throwing a long dramatic shadow from the padlock "
        "across the door and picking out the metal's micro-texture, while "
        "the corridor behind dissolves into warm dim falloff. " + COMMON
        + NO_TEXT
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
