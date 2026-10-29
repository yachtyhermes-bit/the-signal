#!/usr/bin/env python3
"""Generate hero for mrvl-ocp-open-rack-interconnect-2026 (fal flux/schnell).

Subject: Marvell Technology (MRVL) at OCP Global Summit 2026 — 3.2 Tbps 224G
protocol-aware retimer + 2nd-gen 1.6T AEC DSP for AI rack scale-up interconnect,
plus CXL memory expanders and an open hardware-security (HSM) standard.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room): a PHOTO-REALISTIC editorial stock photograph
of a high-speed optical/copper interconnect module on a lab test bench — a
QSFP-DD / OSFP style 800G/1.6T transceiver plugged into a signal-integrity test
board, copper DAC cables, a digital oscilloscope / BER test instrument blurred in
the background, shallow depth of field, professional lighting.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-mrvl-ocp-interconnect-hero-20261014.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "mrvl-ocp-open-rack-interconnect-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no part numbers, no serial numbers, no "
    "printed markings, no stencilled characters, no silkscreen text, no screen "
    "text, no instrument displays showing writing, no brand names, no "
    "manufacturer names, no logos, no watermark, no captions, no legible "
    "writing of any kind anywhere in the image. All equipment surfaces, test "
    "board silkscreen, connector bodies, oscilloscope and instrument panels are "
    "plain and unmarked. No people, no faces, no person in the scene. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no data-center hallway, no server aisle, no "
    "server racks, no cable runs through a building."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a high-speed optical and "
        "copper interconnect module being tested on an electronics signal-"
        "integrity lab bench. In the sharp foreground, an 800G-class QSFP-DD "
        "style optical transceiver module is seated in the cage of a green "
        "printed-circuit signal-integrity test board, its gold edge contacts and "
        "die-cast metal shell catching the light, a slim electrical connector "
        "and a short copper direct-attach twinaxial cable looping away from the "
        "board beside it. The board is populated with small surface-mount "
        "components, tiny capacitors and fine traces, resting on a matte dark "
        "workbench. Behind it, softly out of focus, sits a large digital "
        "sampling oscilloscope and a bit-error-rate test instrument stack, their "
        "screens glowing faintly and their front panels dissolving into smooth "
        "creamy bokeh. Cool neutral lab lighting from a softbox on the left with "
        "a gentle warm fill, honest reflections on the metal connector shell and "
        "the polished bench surface. Extremely shallow depth of field: the "
        "transceiver, its cage and the board traces are tack sharp while the "
        "instruments behind melt into bokeh. Shot on a 100mm macro lens at "
        "f/2.8, real optical blur, natural realistic material textures, subtle "
        "sensor noise and fine film grain, honest documentary realism, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph taken on a macro lens in an electronics "
        "signal-integrity test laboratory, not a render and not computer "
        "generated. A high-speed 1.6 terabit per second optical transceiver "
        "module in the OSFP form factor is plugged horizontally into the metal "
        "cage of a dense signal-integrity test board that fills the sharp "
        "foreground. The module's die-cast silver metal shell, its gold-plated "
        "edge connector and a small latching pull-tab are clearly visible; a "
        "pair of thick grey copper DAC cables curve out of adjacent ports and "
        "sweep across the table, fabric texture visible on their jackets. The "
        "green test board is covered in small surface-mount parts and fine "
        "copper traces. Farther back and completely out of focus, a tall "
        "oscilloscope with a softly glowing graticule screen and a racked "
        "bit-error-rate tester recede into smooth bokeh. Cool white lab light "
        "from overhead plus a soft warm accent, natural highlights on the "
        "polished metal. Very shallow depth of field focused on the transceiver "
        "shell and the nearest cable, everything behind blurred. Macro lens at "
        "f/2.8, real optical blur, subtle lens vignette, believable sensor noise "
        "in the shadows, honest imperfect realism, no glossy CGI sheen, no "
        "plastic render look, no digital illustration, photorealistic, high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A real photograph shot with a fast macro lens on a laboratory "
        "workbench, the work of a professional electronics photographer, not a "
        "3D visualisation and not an AI render. Tight three-quarter angle on a "
        "QSFP-DD style 800-gigabit optical transceiver docked in a signal-"
        "integrity test fixture: the flat metal package, the ribbed heat-sink "
        "lid, the gold contact edge and the small latching bail are rendered "
        "razor sharp, and pale light slides along the brushed metal. Beside the "
        "module, a short copper direct-attach twinaxial cable with a grey jacket "
        "and a shiny metal connector shell loops across the bench, and the "
        "modular test board beneath shows tiny resistors, capacitors and fine "
        "traces under a thin film of dust. Behind, blurred into heavy bokeh, the "
        "dark silhouette of a digital sampling oscilloscope with a faint glowing "
        "screen stands with a bit-error-rate test instrument, their outlines "
        "soft and out of focus. Cool neutral lab illumination with a soft warm "
        "practical in the far background, a low-key moody but honest look. "
        "Extremely shallow depth of field, sharp only on the transceiver and the "
        "near cable. Real macro-lens bokeh, faint dust motes, natural grain and "
        "sensor noise, slightly uneven real white balance, subtle vignette, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A genuine photograph shot on a macro lens by a professional electronics "
        "photographer on a laboratory workbench, not a render, not a 3D "
        "visualisation, not computer generated. Extreme close three-quarter view "
        "of an 800G-class QSFP-DD optical transceiver module seated in the metal "
        "cage of a green signal-integrity test board that fills the sharp lower "
        "foreground: the flat brushed metal package, a ribbed heat-sink lid, the "
        "gold-plated edge connector and a small latching bail are rendered razor "
        "sharp, with real specular highlights sliding along the metal and tiny "
        "machining marks and dust on its surface. A short thick grey copper "
        "direct-attach twinaxial cable curves out of an adjacent port and loops "
        "across the matte dark bench, its woven jacket texture and shiny metal "
        "connector shell clearly readable at an angle. The test board shows "
        "small surface-mount resistors and capacitors, fine copper traces, "
        "matte solder joints and a scatter of dust. Deep in the background and "
        "heavily out of focus, the dark unlit silhouette of a digital sampling "
        "oscilloscope stands with its screen turned off and dark, and a "
        "bit-error-rate test instrument beside it, both dissolved into smooth "
        "creamy bokeh with no glow. Soft cool daylight from a window on the "
        "left with a gentle warm practical bounce, honest natural shadows, "
        "low-key but clean. Extremely shallow depth of field, sharp only on the "
        "module and the near cable. Real macro-lens optical blur, faint dust "
        "motes in the air, natural sensor noise and fine film grain, slightly "
        "imperfect real-world exposure and white balance, subtle vignette, "
        "tactile realistic material textures, no plastic CGI sheen, no glossy "
        "render look, no airbrushed surfaces, no perfect symmetry, no digital "
        "illustration, no AI-generated look, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
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
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
