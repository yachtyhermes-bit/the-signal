#!/usr/bin/env python3
"""Generate hero for akam-anthropic-cloud-compute-deal-2026 (fal flux/schnell).

Subject: Akamai Technologies landed an $11.6B, seven-year commitment from
Anthropic to run Anthropic's CPU workloads on Akamai Cloud — the largest
contract in Akamai's history. Akamai built the CDN that made the web fast:
tens of thousands of servers in thousands of locations close to users,
caching content so it never has to travel far. That same distributed edge is
what it is now selling as cloud compute.

Frame: THE FIBER PLANT OF AN EDGE NETWORK — the physical connectivity at the
edge, NOT a data center.

Scene 1 (ATTEMPT=1): a technician's gloved hands patching aqua and orange
fiber-optic patch cords into a dense, orderly optical patch panel inside a
compact edge / colocation cabinet, with a small handheld optical power meter
on the shelf beside it.

Scene 2 (ATTEMPT=2): a close-up of an open fiber-optic splice tray with
fusion-spliced strands coiled in neat loops, a gloved hand holding a fusion
splicer above it.

Deliberately NOT (banned): no long data-center hallway, no server aisle, no
server racks, no GPU racks, no glowing neon, no synthwave, no light trails,
no abstract / geometric digital art, no charts or screens full of data.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: telecom gear invites silkscreens, port numbers, part codes,
  brand names and cable labels, so all lettering, numerals, signage and
  logos are explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-akam-anthropic-hero-20260925.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "akam-anthropic-cloud-compute-deal-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no port numbers, no channel numbers, no circuit IDs, no lot "
    "numbers, no serial numbers, no etched part markings on the hardware or "
    "the connectors, no markings on the patch cords, no colour-code legends, "
    "no signage, no placards, no warning labels, no safety posters, no "
    "labels, no tags, no stickers, no decals, no painted markings on "
    "equipment, no words on push buttons or switches, no START or STOP "
    "legends, no button lettering, no control-panel instructions, no "
    "machine nameplates, no data plates, no asset tags, no inventory "
    "stickers, no equipment identification plates, no illuminated indicator "
    "words, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no trademarks, no watermarks, no signatures, no "
    "barcodes, no QR codes, no data-matrix codes, no hatching IDs, no "
    "graffiti, no handwriting, no documents, no clipboards with writing, no "
    "label printers, no legible writing of any kind anywhere in the image. "
    "No silkscreen printing, no ink of any kind on any surface, no printed "
    "markings on the panels, no lettering on the tiny connectors, no control "
    "panel, no keypad and no buttons are visible in frame at all. Any "
    "display, monitor, HMI panel or instrument readout is entirely blank, "
    "dark or softly out of focus with no readable content at all. Every "
    "surface, cabinet panel, shelf, panel face and connector housing is "
    "plain and unmarked, carrying no lettering, no numerals and no logos at "
    "all. No illustration, no digital art, no cartoon, no 3D render, no CGI, "
    "no neon, no glowing lines, no light trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no artificial overlay "
    "graphics, no augmented-reality graphics, no wireframe, no charts, no "
    "graphs, no dashboards, no data visualisation, no screens full of data, "
    "no data center, no server room, no server racks, no server aisles, no "
    "GPU racks."
)

COMMON = (
    "Natural available light, mostly soft daylight from above and from an "
    "open doorway at the side, with faint cool reflection off the metal and "
    "softer warm fill from a nearby room. Shallow depth of field with real "
    "optical lens blur and creamy natural bokeh, honest available-light "
    "exposure, true colour, natural camera noise, very slight film grain, "
    "subtle lens vignette, slight sensor softness in the shadows, no plastic "
    "CGI sheen, no glossy render, no perfect symmetry, no retouched "
    "hyper-clean digital look, no 3D visualisation, no digital illustration, "
    "an actual photograph taken on a real camera, not a rendering, handheld "
    "with a slightly imperfect framing, uneven corner illumination, faint "
    "chromatic fringing on high-contrast edges, a few dust motes drifting in "
    "the air, photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — gloved hands patching fiber patch cords into a dense optical patch
    #     panel inside a compact edge / colocation cabinet.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/2.0 on a full-frame camera, inside a compact edge-network and "
        "colocation cabinet where fiber-optic patch cords are being "
        "installed by hand. At the centre of frame, crisp and tack sharp, a "
        "technician's two hands in thin grey work gloves are plugging a "
        "pair of fiber-optic patch cords into a dense, orderly vertical "
        "optical patch panel: the cords are bright aqua-teal and orange, "
        "their slim round jackets smooth and slightly glossy, each ending "
        "in a small dark metal-and-plastic connector gripped between "
        "finger and thumb and sliding home with a faint real specular "
        "glint along its edge. The patch panel itself is a long rectangle "
        "of dark machined metal and matte plastic filled with dozens upon "
        "dozens of small identical connector ports in perfect rows, each "
        "one plain and unmarked, an unbroken field of quiet industrial "
        "repetition with no printing, no numbers and no labels anywhere on "
        "it, fine wear and a little dust in the crevices of the metal. The "
        "aqua and orange cords sweep away from the live ports in gentle "
        "controlled arcs, looping down out of the bottom of the frame and "
        "coiling loosely to one side, layered over a few already-installed "
        "orange strands that hang in soft curves and fall gently out of "
        "focus toward the edges. On the shelf beside the panel to the "
        "right, slightly behind the plane of focus and softly blurred, a "
        "small handheld optical power meter lies flat on the metal, a "
        "palm-sized dark handset with a plain blank face and a short stub "
        "of patch cord fitted into its side, its surface unmarked with no "
        "lettering and no readable display. The cabinet interior around "
        "the hands is dim grey metal and shadow with faint cool highlights "
        "on the frame edges, and beyond the open cabinet door the "
        "background dissolves into a soft warm-grey blur of an ordinary "
        "equipment room. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — close-up of an open fiber splice tray with fusion-spliced strands,
    #     a gloved hand holding a fusion splicer above it.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 100mm macro "
        "lens at f/2.8 on a full-frame camera, close in over an open "
        "fiber-optic splice tray on a workbench. The tray fills the lower "
        "half of the frame, tack sharp in the plane of focus: a shallow "
        "moulded dark plastic tray with neat curved channels and small "
        "clips, holding several coiled loops of bare fiber-optic strand "
        "and jacketed aqua-teal and orange patch cord wound in tidy "
        "overlapping circles, the thin glass strands catching long slender "
        "specular highlights along their length, a few fusion-spliced "
        "joints sitting in the protective sleeves visible as small "
        "transparent cylindrical beads among the loops, every surface "
        "plain and unmarked with no printing, no numbers and no labels. "
        "Above the tray, held between the thumb and forefinger of a hand "
        "in a thin grey work glove, enters a small dark handheld fusion "
        "splicer seen from the side, its machined metal body and tiny "
        "alignment groove just above the strands, poised a few centimetres "
        "above the tray and slightly soft as it falls outside the plane of "
        "focus. Around the tray the workbench surface is worn grey "
        "laminate with fine scratches and a scatter of tiny dust and "
        "clippings, a small pair of precision strippers and a lint-free "
        "wipe lying softly out of focus at the left edge of frame, and the "
        "background beyond dissolves into warm-grey workshop haze. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wide edge-site establishing view: orderly fiber cross-connect
    #     racks at the edge of a network, cords carpeting between panels.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera, a wide establishing view standing "
        "inside a compact edge and colocation site, looking at a short row "
        "of optical fiber cross-connect frames. The nearest frame stands "
        "large at the right of the frame, tack sharp: a pale grey metal "
        "open frame packed tightly with a tall stack of dark optical patch "
        "panels, every panel filled with dense rows of small identical "
        "connector ports, plain and unmarked, and a living curtain of aqua "
        "and orange fiber-optic patch cords sweeping between the panels in "
        "long graceful vertical loops, tens of them crossing and layering "
        "into a soft orderly thicket of colour that catches narrow "
        "highlights along each smooth jacket. Behind it one more identical "
        "frame recedes toward the far wall, smaller and softer, its cords "
        "still faintly readable as warm colour, then the room dissolves "
        "into gentle haze. In the sharp near foreground, partly cropped by "
        "the bottom of the frame, the edge of a plain workbench holds a "
        "loose coil of aqua patch cord and a small dark handheld optical "
        "power meter with a blank face, both falling softly out of focus. "
        "Above, a plain industrial ceiling with surface-mounted conduit "
        "and a few soft strip lights, and the plain concrete floor below "
        "holds faint grey reflections. Quiet, ordinary, working "
        "telecommunications space, clean and orderly, with daylight "
        "spilling through an open doorway at the left of frame. "
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
