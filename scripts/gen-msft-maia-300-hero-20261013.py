#!/usr/bin/env python3
"""Generate hero for msft-maia-300-microsoft-custom-silicon-gigawatts-2026 (fal flux/schnell).

Subject: Microsoft's Azure Maia 300 — its own custom AI inference accelerator
(multi-chiplet, 288 GB HBM4, 950W, 96 accelerators per rack) — scaling to
multi-gigawatt Maia deployments starting 2027. Thesis: a hyperscaler designing
its own silicon instead of buying every GPU.

Scene chosen: an extreme close-up PRODUCT photograph of a large AI accelerator
chip package — ONE big square processor package sitting on a brushed-metal
anti-static tray. The organic substrate is visible with multiple smaller chiplets
bonded on top and rows of HBM memory stacks running along two edges. Soft studio
lighting, mixed cool white with a warm rim light, very shallow depth of field
(macro lens), clean neutral light-grey seamless background, glossy ceramic lid
with a subtle rainbow diffraction sheen on the silicon. 16:9 landscape.

Deliberately DISTINCT from recent heroes:
- NOT the 2026-10-13 MU/CXMT hero (cleanroom technician in a bunny suit holding
  a 300mm wafer) — no cleanroom, no person, no wafer.
- NOT a data-center aisle / server-rack corridor / server-room composition.
- NOT a dark tabletop macro of bare DRAM sticks.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: chip packages naturally carry silkscreen markings, so any legible
  marking — letters, numbers, part numbers, lot codes, logos, branding, QR
  codes, watermarks — is explicitly forbidden, and the output is verified.
- Generate 1440x810, finalize 1920x1080 center-crop JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-msft-maia-300-hero-20261013.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "msft-maia-300-microsoft-custom-silicon-gigawatts-2026")
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
    "trademarks, no watermark, no signature, no caption, no signature text, no "
    "ruler or measurement graduations, no letter-like or typography-like "
    "markings of any kind anywhere in the image. The chip lid, the organic "
    "substrate, the metal tray and every surface in the frame are entirely "
    "plain, bare and unmarked. No illustration, no digital art, no cartoon, no "
    "3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no futuristic HUD graphics, no overlay "
    "elements, no augmented-reality graphics, no server rack, no server aisle, "
    "no server room, no data-center hallway, no cable runs. "
    "Every small black chip and every memory stack is a uniform plain matte "
    "black surface with absolutely NO light-coloured specks, NO white dots, NO "
    "white or silver markings, NO tiny printed codes, NO small white letters or "
    "digits, NO speckles of writing on the dark chips, NO etched numbers and NO "
    "lettering of any size anywhere on any component or on the board. The dark "
    "chips are completely blank and clean."
)

PROMPTS = {
    "1": (
        "Photo-realistic macro product photograph of a large custom AI "
        "accelerator chip package, shot as a still-life stock photo. A single "
        "big square processor package rests flat on a brushed-metal "
        "anti-static tray, filling most of the frame. The package is a large "
        "square multi-chiplet module: a greenish-brown organic substrate with "
        "multiple smaller rectangular silicon dies bonded across its centre, "
        "and along two opposite edges run neat rows of identical darker "
        "HBM memory stacks, each a small flat slab set in its own recessed "
        "seal. The lid of the processor is a glossy ceramic that catches a "
        "faint iridescent rainbow diffraction sheen where the studio light "
        "grazes it. Soft professional studio lighting — a broad cool-white "
        "key light from the upper left with a subtle warm amber rim light "
        "grazing the far edge of the package. The background is a clean "
        "neutral light-grey seamless studio sweep, softly out of focus. "
        "Extremely shallow depth of field from a macro lens: the near chiplets "
        "and HBM stacks are tack sharp with fine realistic surface detail and "
        "micro-texture, while the far edge of the tray and the background "
        "dissolve into smooth creamy bokeh. Shot on a 100mm macro lens at "
        "f/2.8, real optical bokeh, honest exposure, natural fine sensor "
        "grain, subtle lens vignette, realistic material textures with no "
        "plastic CGI sheen, no perfect symmetry, no glossy render. "
        "Photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real close-up photograph taken with a macro lens, not a render and "
        "not computer generated: an extreme close-up of one large square AI "
        "accelerator chip package resting on a flat brushed-aluminium "
        "anti-static tray. The package is the whole subject — a broad square "
        "module whose lid is one smooth, unbroken sheet of dark glossy "
        "ceramic, plain and featureless, with a delicate iridescent rainbow "
        "diffraction shimmer of pale green, pink and violet sliding softly "
        "across it where the studio light grazes at a low angle. Around the "
        "lid only a slim rim of the organic package substrate shows at the "
        "edges. The package carries just a few large flat shapes: one wide "
        "central chiplet slab bonded under the lid edge and two long unbroken "
        "bands of recessed dark grey HBM memory blocks running down the left "
        "and right sides, each block smooth and completely blank. No small "
        "loose components, no scattered parts, no surface-mounted specks — "
        "only the few large clean elements of the package. Soft mixed studio "
        "lighting: a cool white softbox above and to the left, plus one small "
        "warm tungsten rim light skimming the far edge of the metal tray so "
        "the brushed metal catches a warm highlight. The backdrop is a plain "
        "light-grey seamless paper, far out of focus. Very shallow depth of "
        "field, everything but the nearest edge of the package melting into "
        "smooth creamy bokeh, fine natural film grain, subtle lens vignette, "
        "real optical blur, no plastic CGI sheen, no glossy render, no "
        "airbrushed plastic surfaces, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, honest documentary realism, "
        "photorealistic, high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "An authentic product still-life photograph of a large square AI "
        "accelerator chip package sitting on a brushed-metal anti-static "
        "tray, shot handheld with a macro lens as editorial stock photography "
        "— a real photograph, not a render and not computer generated. The "
        "single chip package is the hero: a big square processor module with "
        "a glossy ceramic lid that shows a delicate rainbow diffraction sheen "
        "of pale green, pink and violet where the studio light grazes the "
        "polished silicon. The organic substrate is visible around the lid, "
        "with multiple smaller rectangular chiplets bonded across the middle "
        "of the package and two orderly rows of stacked HBM memory packages "
        "flanking the chiplets along two sides, each stack a small dark slab. "
        "Soft studio lighting with a cool white key from one side and a warm "
        "rim light behind the opposite edge; a plain seamless light-grey "
        "backdrop softly blurred behind the tray. Macro-lens shallow depth of "
        "field: the package's nearest chiplets and the metal tray's brushed "
        "grain are tack sharp while the back of the package and the "
        "background fall into creamy bokeh. Natural fine sensor noise, "
        "slightly uneven real-world white balance, a thin cool haze, subtle "
        "vignette, imperfect honest framing, real optical blur, honest "
        "exposure. Absolutely not a 3D visualisation, not a glossy CGI "
        "render, no airbrushed plastic surfaces, no smooth digital sheen, no "
        "perfect symmetry, no digital illustration, no AI-generated look, "
        "photorealistic, high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "An authentic, slightly imperfect real-world macro photograph — shot "
        "handheld by a photographer with an 85mm macro lens wide open — of one "
        "large square AI accelerator chip package resting on a scratched "
        "brushed-metal anti-static tray in a studio. The package is a broad "
        "square module: its ceramic lid is a single smooth unbroken dark sheet "
        "with a faint soft iridescent rainbow diffraction shimmer running "
        "across it at a low grazing angle, and around the lid edge only a slim "
        "rim of the organic substrate shows. The package has just a few large "
        "plain shapes: one wide plain central chiplet slab and two long "
        "unbroken bands of recessed dark grey blank HBM memory blocks down the "
        "left and right sides. No small loose components, no scattered parts, "
        "no tiny surface-mounted specks. The brushed metal tray shows fine "
        "real hairline scratches and slight uneven tarnish, and a small stray "
        "fingerprint smudge near one corner. Soft directional studio light "
        "from the upper left with a warm amber rim light catching the far "
        "edge of the metal, a plain light-grey seamless backdrop far out of "
        "focus behind. Macro-lens shallow depth of field: only the nearest "
        "edge of the package and the metal's brushed grain are sharp, "
        "everything else is creamy natural bokeh. Heavy but natural sensor "
        "noise and real film grain in the shadows and midtones, slightly "
        "uneven real-world white balance, faint floating dust motes, a thin "
        "haze in the air, soft lens flare ghosting from the rim light, "
        "chromatic aberration on the high-contrast edges, subtle lens "
        "vignette, slightly crooked imperfect handheld framing, real optical "
        "blur, honest unretouched exposure. Absolutely not a 3D "
        "visualisation, not a glossy CGI render, no airbrushed plastic "
        "surfaces, no smooth digital sheen, no perfect symmetry, no pristine "
        "cleanroom-sterile look, no digital illustration, no AI-generated "
        "look, visibly a real camera photograph, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
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
