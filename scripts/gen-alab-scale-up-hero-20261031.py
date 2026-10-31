#!/usr/bin/env python3
"""Generate hero for alab-scale-up-connectivity-cash-test-2026 (fal flux/schnell).

Subject: Astera Labs (ALAB) — connectivity silicon and cable modules that link
AI accelerators inside a rack: PCIe retimers, Scorpio fabric switches, Aries
Smart Cable Modules, and the new Aries 7 PCIe 7 portfolio spanning copper and
optical. Thesis: the connectivity layer inside the AI rack.

MANDATORY SCENE: a close, shallow-depth-of-field photograph of high-speed
copper cable harnesses and connector ends being inspected at a test bench —
macro focus on the metal connector shell, densely packed twinax pairs and
strain-relief boots, a technician's nitrile-gloved hands slightly out of focus
in the background, cool white bench lighting, realistic metal and plastic
textures.

Deliberately NOT: data center aisle / server room / server racks as subject,
neon, glowing lines, synthwave, abstract or digital art, geometric patterns,
charts rendered as art, text, logos, watermarks, CGI look.

Rules:
- PHOTO-REALISTIC stock photograph ONLY.
- TEXT-FREE: no letters/numbers/logos/brand names/markings on shells or bench.
- Generate 1440x810, finalize 1536x864 center-crop.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-alab-scale-up-hero-20261031.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "alab-scale-up-connectivity-cash-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, "
    "no labels, no printed markings on the connector shells or the bench, "
    "no logos, no brand names, no part numbers, no signage, no screens, "
    "no watermark, no caption, no illustration, no digital art, no cartoon, "
    "no 3D render, no CGI, no neon, no glowing lines, no synthwave, "
    "no geometric patterns, no abstract art, no charts, no sci-fi, "
    "no server racks, no data center aisle."
)

PROMPTS = {
    # 1 — primary pick: extreme macro on one connector shell end, twinax fanning out
    "1": (
        "Photo-realistic professional product-lab stock photograph, extreme "
        "close-up with very shallow depth of field, of a high-speed copper "
        "cable connector end resting on a brushed stainless steel test bench: "
        "the rectangular die-cast metal connector shell in sharp macro focus "
        "at the front, its stamped metal cage, tiny solder joints and "
        "alignment pins visible at the mating edge, a gold-plated contact "
        "array recessed inside the mouth of the shell, a thick black "
        "strain-relief boot behind it with molded ribs, and dozens of "
        "densely packed thin twinax wire pairs fanning out of the back of "
        "the boot, individually insulated in tight parallel lines of grey, "
        "blue and natural silver, held in a bundle by a small black cable "
        "comb, the copper braid shield slightly frayed at the transition, "
        "faint scuffs and handling marks on the metal, fine dust on the "
        "bench surface. In the softly blurred background a technician's "
        "hands in pale blue nitrile gloves hover over a second connector, "
        "completely out of focus, only pale blue shapes and a suggestion of "
        "motion. Cool neutral white bench lighting from the upper left, "
        "crisp specular highlights along the metal edges, gentle falloff to "
        "a dark neutral background, cold grey and steel tones with a hint "
        "of warm skin color lost in the bokeh. Shot on a full-frame camera "
        "with a 100mm macro lens at f2.8, 1:1 magnification, tack-sharp "
        "focus plane on the connector mouth, creamy blurred foreground and "
        "background, realistic micro-texture on plastic and metal, fine "
        "sensor grain, unretouched natural color, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    # 2 — wider bench: harness bundle + connector ends laid out, gloved hands mid-frame
    "2": (
        "Photo-realistic professional stock photograph, close-up with "
        "shallow depth of field, of several high-speed copper cable harness "
        "assemblies laid out on a light grey industrial test bench: three "
        "black-jacketed cable modules with rectangular metal connector "
        "shells at the near end, strain-relief boots and molded plastic "
        "collars, the cable jackets splitting open into tight bundles of "
        "twisted twinax pairs wrapped in foil and braided shield, small "
        "black cable ties holding the bundle, connector shells showing "
        "machined aluminium edges, faint fingerprints and handling wear. "
        "In the mid-ground, out of focus, a technician wearing pale blue "
        "nitrile gloves holds one connector up between thumb and forefinger "
        "to inspect its mating face, torso cropped, only gloved hands and "
        "dark sleeve visible. A grey anti-static mat under the cables, a "
        "blurred probe fixture and a matte black instrument housing at the "
        "far edge of the frame, no readable screens. Cool white overhead "
        "bench lighting, soft directional shadows, subtle reflection of the "
        "light on the steel bench, muted realistic color palette of black, "
        "grey, aluminium and pale blue. Shot on a full-frame camera at "
        "85mm f2.0, natural bokeh, realistic material texture, fine sensor "
        "grain, documentary lab realism, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — alternative: signal-integrity probe fixture on board, gloved hand, instrument bokeh
    "3": (
        "Photo-realistic professional engineering-lab stock photograph, "
        "close-up with shallow depth of field, of a signal-integrity probing "
        "setup on a bench: in sharp focus a green printed circuit board with "
        "a dense high-speed edge connector and a metal probing fixture "
        "clamped over it, fine gold-tipped probe needles touching test pads, "
        "a short high-frequency coaxial cable with a small metal connector "
        "running out of frame, tiny surface-mount components and solder "
        "pads sharply resolved, faint flux residue and handling marks. "
        "Slightly behind, a technician's hand in a pale blue nitrile glove "
        "steadies the probe fixture, fingers softly out of focus, and at the "
        "edge of the frame a blurred dark instrument chassis and a matte "
        "grey bench surface with a coiled cable, no readable display "
        "content, no charts, no glowing screen. Cool white bench lighting "
        "from above with a soft shadow under the fixture, neutral color, "
        "metallic highlights on the probe tips. Shot on a full-frame camera "
        "with a 100mm macro lens at f2.8, extremely detailed real-world "
        "texture, fine sensor grain, unretouched natural color, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
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


def crop_to_ratio(img):
    """Center-crop to 16:9 then resize to 1536x864."""
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def save_under_cap(img, path):
    """Save JPEG, stepping quality down until under MAX_BYTES."""
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        print(f"  q={q} -> {size} bytes")
        if size < MAX_BYTES:
            return size
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_ratio(img)
    size = save_under_cap(img, OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Mirrored to {BACKUP}  bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
