#!/usr/bin/env python3
"""Generate hero for nand-flash-supercycle-explainer-2026 (fal flux/schnell).

Subject: NAND flash memory — the storage chips inside solid-state drives — and
how AI data centres are consuming enormous amounts of it.

Scene chosen: MACRO PHOTOGRAPH OF AN OPENED SOLID-STATE DRIVE ON A WORKBENCH,
its bare NAND flash packages and controller visible on the green circuit
board, warm professional lighting, shallow depth of field, anti-static mat and
precision tweezers softly out of focus.

Deliberately NOT: data-center hallway, server aisle, racks, neon, glowing
lines, abstract or digital art, geometric patterns, illustration, render.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: chips carry no printed markings/part numbers/logos, PCB has no
  silkscreen lettering, no labels, no stickers, no brand names.
- Generate 1536x864 (16:9), finalize 1920x1080, identical bytes to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/generate-nand-flash-supercycle-explainer-2026-hero.py
"""

import os
import shutil
import sys

import requests

SLUG = os.environ.get("SLUG", "nand-flash-supercycle-explainer-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
W, H = 1536, 864            # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

OUTPUT1 = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
OUTPUT2 = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
PROMPT_DUMP = "/tmp/nand_flash_hero_prompt.txt"

NO_TEXT = (
    "Absolutely no lettering anywhere in the scene: no text, no letters, no "
    "words, no numbers, no part numbers, no serial numbers, no date codes, no "
    "laser-etched markings on the chips, no printed markings of any kind on "
    "the chip packages, no silkscreen lettering on the circuit board, no "
    "capacitor printing, no connector labels, no stickers, no adhesive labels, "
    "no barcodes, no QR codes, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no vendor marks, no "
    "watermarks, no captions, no signage, no readable writing of any kind. "
    "Every chip package has a completely blank, smooth, uniform matte-black "
    "moulded surface with no text and no marking whatsoever. The green "
    "circuit board is clean and unlabelled. No illustration, no digital art, "
    "no cartoon, no painting, no 3D render, no CGI, no neon, no glowing lines, "
    "no light trails, no synthwave, no geometric patterns, no futuristic HUD "
    "graphics, no hologram, no overlay graphics, no abstract shapes, no data "
    "center, no server room, no server racks, no server aisle, no hallway of "
    "racks, no cable-run composition."
)

PROMPTS = {
    # 1 — the brief: macro of an opened SSD on a workbench.
    "1": (
        "Professional macro stock photograph, a genuine camera photograph and "
        "not a render, shot on a 100mm macro lens at f/4 on a full-frame DSLR: "
        "an opened solid-state drive lies on a grey anti-static workbench mat, "
        "its aluminium enclosure slid open and lying to one side, revealing "
        "the green printed circuit board inside. The board fills the centre of "
        "the frame at a shallow three-quarter angle: several large rectangular "
        "black NAND flash memory packages sit in a neat row, their flat matte "
        "surfaces catching soft highlights, and a smaller square controller "
        "chip sits among them, alongside a row of tiny silver surface-mount "
        "capacitors and resistors and fine gold contact traces running across "
        "the green solder mask. A fine metal precision tweezer rests on the "
        "mat in the near foreground, softly out of focus, and a second drive "
        "screwed shut sits further back, melting into blur. Warm professional "
        "lighting from a single soft key light above and to the left rakes "
        "across the chips, picking out the slight texture of the moulded "
        "packages and the sheen of the solder joints, with gentle warm "
        "reflections on the aluminium edge and soft natural shadows in the "
        "gaps between components. Extremely shallow depth of field: the middle "
        "row of NAND packages is tack sharp and everything in front of and "
        "behind it dissolves into creamy bokeh. Real optical lens blur, honest "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photo-realistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition, top-down but slightly "
        "angled view of real hardware. "
        + NO_TEXT
    ),
    # 2 — lower angle, tighter on the chip row and controller.
    "2": (
        "A real close-up photograph of electronic hardware, not a render and "
        "not computer generated, shot on a 90mm macro lens at f/3.5: an opened "
        "solid-state drive on an anti-static mat, viewed from a low angle "
        "almost level with the board so the black memory packages stand proud "
        "above the green surface. In the sharp centre of the frame three "
        "large rectangular NAND flash memory chips are arranged side by side, "
        "their blank matte-black moulded tops plain and unmarked, with a "
        "smaller square controller package just behind them and a scatter of "
        "tiny silver capacitors and resistors between. Fine copper traces and "
        "vias thread across the solder mask. A pair of steel tweezers and the "
        "edge of the drive's aluminium cover sit in the foreground, heavily "
        "defocused. Warm directional light from a softbox at the upper left "
        "grazes the tops of the chips and throws short soft shadows, giving "
        "the plastic a gentle satin sheen and a warm amber cast across the "
        "bench. Very shallow depth of field, the front chip edge razor sharp "
        "and the rest of the board falling away into smooth bokeh. Real "
        "optical lens blur, honest editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photo-realistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — wider bench scene: opened drive plus tools, still hardware-led.
    "3": (
        "A genuine documentary photograph of a repair bench, not a render and "
        "not computer generated, shot on a 50mm lens at f/2.8 with a close "
        "focus: an opened solid-state drive lies disassembled on a grey "
        "anti-static mat, its two aluminium halves apart and the green circuit "
        "board exposed between them. The bare NAND flash memory packages and "
        "the controller chip are clearly visible as flat black rectangles in a "
        "row across the board, with fine traces and small silver components "
        "around them. Precision tweezers, a small screwdriver and a few tiny "
        "screws are scattered on the mat around the drive, softly out of "
        "focus in the foreground and to the sides. Warm professional bench "
        "lighting from a single lamp above casts soft pools of amber light and "
        "gentle shadows, the metal enclosure edges glinting faintly. Shallow "
        "depth of field focused on the exposed board, the surrounding bench "
        "tools and the far edge of the mat dissolving into creamy bokeh. Real "
        "optical lens blur, honest available-light editorial exposure, natural "
        "camera noise, very slight film grain, subtle lens vignette, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photo-realistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
}

# Attempt 4 — final fallback: plain-surface emphasis, silkscreen explicitly denied.
PROMPTS["4"] = (
    "Professional macro product photograph of computer hardware, a genuine "
    "camera photograph and not a render, shot on a 100mm macro lens at f/5.6 "
    "from directly above: the exposed circuit board of an opened solid-state "
    "drive fills the whole frame on a warm grey workbench surface. A row of "
    "four large black NAND flash memory packages dominates the centre of the "
    "frame, each one a perfectly plain, smooth, matte black moulded rectangle "
    "with a completely bare top face and nothing printed on it at all, and a "
    "smaller square controller package sits at the end of the row. The green "
    "solder mask around them is clean, uniform and completely unmarked, with "
    "no white silkscreen printing, no reference designators, no pad labels, no "
    "outlines and no writing of any kind anywhere on the board. Fine copper "
    "traces and vias thread between the components and tiny silver "
    "surface-mount capacitors and resistors sit in neat rows. Warm soft "
    "directional light from the upper left rakes across the flat chip tops, "
    "giving the matte plastic a gentle satin sheen and casting short soft "
    "shadows beside every component. Shallow depth of field: the middle chips "
    "are tack sharp and the far edge of the board and the workbench dissolve "
    "into creamy bokeh. Real optical lens blur, honest editorial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
    "visualisation, no digital illustration, photo-realistic, very high "
    "detail, professional editorial stock photography, 16:9 landscape "
    "composition. "
    + NO_TEXT
    + " CRITICAL: every visible surface is plain, blank and unmarked — zero "
      "printed characters, zero numbers, zero silkscreen, zero engraved or "
      "etched markings, zero labels, zero stickers anywhere in the image."
)

# Attempt 5 — workshop realism: used hardware, imperfections, natural falloff.
PROMPTS["5"] = (
    "An ordinary working photograph, the kind a technician takes on a bench "
    "with a camera, definitely not a product render and not computer "
    "generated, shot on a 60mm macro lens at f/8 with a modest aperture so "
    "the depth of field is natural rather than extreme: an opened solid-state "
    "drive lies half out of its aluminium shell on a worn grey anti-static "
    "mat, the green circuit board angled towards the camera. Three plain "
    "matte-black NAND flash memory packages sit in a row on the board, their "
    "flat top faces bare and completely unmarked, with a small square "
    "controller chip beside them, a scatter of tiny silver surface-mount "
    "components and fine copper traces crossing the green solder mask. The "
    "hardware is genuinely used, not new out of the box: faint fingerprints "
    "and a little dust on the chip tops, a hairline scratch on the aluminium "
    "shell, a few specks on the mat, a loose screw and the tip of a steel "
    "tweezer sitting slightly out of focus in the near foreground. Warm "
    "practical light from an ordinary desk lamp to the left, slightly uneven, "
    "falling off towards the right of the frame, with a soft shadow from the "
    "tweezers and a dull reflection on the metal edge. Modest depth of field "
    "with natural optical falloff, the middle of the board sharp and the near "
    "foreground and far bench edge softly blurred. Photographic texture: real "
    "lens blur, visible fine sensor noise, slight chromatic softness at the "
    "frame edges, mild vignetting, uneven white balance, no studio polish, no "
    "glossy sheen, no perfect symmetry, no CGI look, no 3D visualisation, no "
    "digital illustration, photo-realistic, high detail, documentary "
    "editorial photography, 16:9 landscape composition. "
    + NO_TEXT
    + " CRITICAL: every visible surface is plain, blank and unmarked — zero "
      "printed characters, zero numbers, zero silkscreen, zero engraved or "
      "etched markings, zero labels, zero stickers anywhere in the image."
)


# Attempt 6 — ordinary handheld bench snapshot, off-centre, 35mm, real clutter.
PROMPTS["6"] = (
    "A real, unposed snapshot photograph taken handheld on a workbench, not a "
    "render, not CGI, not a stock studio product shot: shot on a 35mm lens at "
    "f/2.8 from just above bench height, the framing loose and off-centre, "
    "the drive sitting low and left of frame rather than dead centre, the "
    "horizon of the bench slightly tilted. An opened solid-state drive lies "
    "there with its top shell prised off and set aside, the green circuit "
    "board exposed: a row of plain matte-black rectangular NAND flash memory "
    "packages with completely bare unmarked tops, a smaller square controller "
    "package, rows of tiny silver capacitors and resistors, fine copper "
    "traces. Around it on a worn grey anti-static mat: a small screwdriver, "
    "four loose screws, a strip of thermal pad, the tip of a steel tweezer "
    "and the corner of a laptop just clipping the frame edge, most of it "
    "softly out of focus. The hardware is used and a bit dusty, with faint "
    "fingerprints on the chip faces and light scuffs on the aluminium. "
    "Lighting is a single warm desk lamp from the left, uneven and falling "
    "off into shadow on the right side of the frame, with soft shadows behind "
    "the components and a dull highlight on the metal. Shallow depth of field "
    "in the ordinary photographic way, the near part of the board sharp and "
    "the rest of the bench melting away. Real optics: slight highlight bloom, "
    "soft corners, visible sensor noise in the shadows, honest color. No "
    "studio lighting, no perfect symmetry, no glossy CGI sheen, no 3D "
    "visualisation, no digital illustration, no product-render polish, "
    "photo-realistic, documentary editorial photography, 16:9 landscape "
    "composition. "
    + NO_TEXT
    + " CRITICAL: every visible surface is plain, blank and unmarked — zero "
      "printed characters, zero numbers, zero silkscreen, zero engraved or "
      "etched markings, zero labels, zero stickers anywhere in the image."
)


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as fh:
            for line in fh:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        with open(real_path) as fh:
            raw = fh.read().strip().split("\n")[0]
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
    model = os.environ.get("MODEL", "fal-ai/flux/schnell")
    steps = int(os.environ.get(
        "STEPS", "28" if "dev" in model or "pro" in model else "4"))
    print("Generating image with " + model + " (steps=" + str(steps) + ") ...")
    gen_args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": steps,
        "enable_safety_checker": False,
    }
    guidance = os.environ.get("GUIDANCE")
    if guidance and "schnell" not in model:
        gen_args["guidance_scale"] = float(guidance)
        print("guidance_scale=" + guidance)
    seed = os.environ.get("SEED")
    if seed:
        gen_args["seed"] = int(seed)
        print("seed=" + seed)
    result = fal_client.subscribe(model, arguments=gen_args)
    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]
    if not image_url:
        print("ERROR: no image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    from PIL import Image

    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size)
          + "  bytes=" + str(len(r.content)))
    return img


def crop_to_16x9(img):
    from PIL import Image

    target_ratio = FINAL_W / FINAL_H
    w, h = img.size
    cur = w / h
    if cur > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT1)
    img = crop_to_16x9(img)
    img.save(OUTPUT1, "JPEG", quality=94, optimize=True)
    size = os.path.getsize(OUTPUT1)
    if size < 102400:
        img.save(OUTPUT1, "JPEG", quality=98, optimize=True)
        size = os.path.getsize(OUTPUT1)
    print("Saved final hero: " + OUTPUT1 + "  dimensions=" + str(img.size)
          + "  bytes=" + str(size))
    os.makedirs(os.path.dirname(OUTPUT2), exist_ok=True)
    shutil.copy2(OUTPUT1, OUTPUT2)
    print("Mirrored to " + OUTPUT2)

    from PIL import Image

    for p in (OUTPUT1, OUTPUT2):
        v = Image.open(p)
        print("VERIFY " + p + " dimensions=" + str(v.size[0]) + "x"
              + str(v.size[1]) + " bytes=" + str(os.path.getsize(p)))
    with open(PROMPT_DUMP, "w") as fh:
        fh.write(prompt)


if __name__ == "__main__":
    main()
