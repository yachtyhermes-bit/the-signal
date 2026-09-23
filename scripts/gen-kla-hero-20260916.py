#!/usr/bin/env python3
"""Generate hero for kla-process-control-ai-chip-inspection-moat-2026 (fal flux/schnell).

Subject: KLA Corporation — process control / wafer inspection and metrology.
Its machines check every layer of every wafer inside a chip fab, which is the
business "moat" the article is about.

Scene chosen: INSIDE A SEMICONDUCTOR CLEANROOM — a wafer-inspection tool stage
holding a round patterned silicon wafer under the optical inspection head, the
fine repeating chip pattern catching the light, with a cleanroom engineer in a
full white bunny suit and hood standing beside the tool, gloved hand near a
plain unmarked control panel.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT a nuclear power plant, NOT an office or headset
customer-service scene, NOT a technician holding a gold-mirrored indium
phosphide laser wafer, NOT digital art, NOT a 3D render, NOT neon / synthwave,
NOT glowing lines, NOT geometric patterns, NOT abstract.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: fabs are full of labels, monitors, panel markings and signage, so
  all lettering, numbers, UI, logos and brand names are explicitly forbidden.
  Any monitor in frame is blank / dark / out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-kla-hero-20260916.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "kla-process-control-ai-chip-inspection-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no toolbars, no menus, no icons, no signage, "
    "no warning signs, no wall placards, no cabinet labels, no panel "
    "markings, no engraved lettering on the equipment, no dial faces with "
    "numbers, no gauges with numerals, no dials, no readouts, no charts, no "
    "arrows, no crosshairs, no alignment marks, no wafer flat markings, no "
    "die labels, no lettering scribed on the silicon wafer itself, no "
    "keyboard lettering, no name badges, no lanyards, no printed documents, "
    "no clipboards with writing, no brand names, no manufacturer names, no "
    "company names, no corporate logos, no trademarks, no watermarks, no "
    "stickers, no barcodes, no QR codes, no datamatrix codes, no handwriting, "
    "no legible writing of any kind anywhere in the image. Every monitor or "
    "display in the frame is switched off, angled away, or so far out of "
    "focus that it shows only a soft flat wash of dark colour with absolutely "
    "nothing readable or drawn on it, like an out-of-focus colour field "
    "photograph, not a screen with content. The cleanroom suit, gloves and "
    "boots are plain white and unmarked, the tool panels are plain brushed "
    "metal with only unlabelled blank buttons and a plain unmarked rotary "
    "knob, and the walls are plain cleanroom panel with no writing on them. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center, no server room, no server "
    "racks, no server aisles, no cable runs, no server lights, no GPU "
    "hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — wafer-inspection tool stage + wafer + engineer beside the tool.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2 on a full-frame camera, of the inside of a working semiconductor "
        "cleanroom during process control. The subject is a wafer-inspection "
        "tool: in the sharp centre of frame a round, mirror-polished silicon "
        "wafer sits flat on a brushed-metal inspection stage, held on a "
        "circular vacuum chuck, with an optical inspection head — a smooth "
        "dark anodised housing with a downward-facing lens barrel — "
        "suspended just above it on a precision gantry arm. The wafer's finely "
        "patterned surface of repeating rectangular chips catches the "
        "light, its surface a mosaic of faint interlocking rectangles and "
        "fine lines that shimmer with a subtle iridescent bloom where the "
        "light grazes it; the die pattern is a texture of light and colour "
        "only, with absolutely nothing written on it. Standing beside the "
        "tool, slightly behind the wafer and softly out of focus, is a "
        "cleanroom engineer in a full white bunny suit: an unmarked white "
        "coverall, a white hood that covers the head and neck, a clear face "
        "shield over a soft plain mask, yellow-gloved hands, one of them "
        "reaching toward a plain unlabelled control panel on the tool's side "
        "with blank buttons. Their posture is calm and attentive, mid-task, "
        "not posing. The tool itself is clean white and brushed stainless "
        "steel with a load port, a small blank dark monitor turned away from "
        "camera and switched off, and clean geometric panelling. The "
        "cleanroom around them is bright and spotless: pale sealed wall "
        "panels, a white ceiling with flush light panels, a grated raised "
        "floor. Soft diffuse cool-white cleanroom light with a faint warm "
        "amber tint falling across the wafer, giving gentle shadows under "
        "the gantry and a soft glow along the engineer's hood. Very shallow "
        "depth of field: the wafer surface and the inspection head are tack "
        "sharp while the engineer and the cleanroom wall behind melt into "
        "creamy bokeh. Real optical lens blur, honest available-light "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — close crop: gloved hands holding a wafer up to the light.
    "2": (
        "A genuine photograph taken in a semiconductor fab, not a render and "
        "not computer generated: a tight close crop, shot on a 100mm macro "
        "lens at f/2.8, of yellow-gloved hands in a cleanroom carefully "
        "holding a round silicon wafer up to the light for inspection. The "
        "wafer fills much of the frame, tilted toward the camera so its "
        "mirror-like surface catches the light at a raking angle: across it "
        "spreads the delicate repeating pattern of identical rectangular "
        "chips, a fine mosaic of faint interlocking rectangles and hairline "
        "gaps that flares into soft bands of violet, teal and warm gold where "
        "the light diffracts off the surface — pure iridescent light and "
        "texture, with nothing written, engraved or printed on the wafer. "
        "The white-gloved fingertips grip the wafer's edge gently by its "
        "rim, and the fabric of a white cleanroom sleeve is visible at the "
        "left edge of frame. Behind the wafer, thrown far out of focus, the "
        "dark bulk of an inspection or metrology tool: a smooth anodised "
        "housing, a blurred lens barrel, a soft glow of instrument light, "
        "the cleanroom wall a pale wash of light behind it. Soft cleanroom "
        "lighting from above and slightly behind, so the wafer glows "
        "translucent around its rim and the fingers are lit from the top "
        "with gentle falloff. Extremely shallow depth of field — the near "
        "rim of the wafer and the fingertips crisp, the far edge of the "
        "wafer softening, the background dissolving into heavy creamy "
        "bokeh. Honest editorial exposure, natural camera noise, very "
        "slight film grain, real optical blur, subtle lens vignette, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — wide low-angle down a small-bay cleanroom aisle, technician walking away.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 from a low angle inside a "
        "semiconductor cleanroom: a wide view straight down a narrow "
        "small-bay fab aisle lined on both sides with wafer inspection and "
        "metrology tools. The tools are tall clean white and brushed "
        "stainless-steel cabinets with rounded corners, load ports, small "
        "dark blank monitor panels turned away from camera or switched off, "
        "and flat unmarked front panels; the aisle floor is a pale perforated "
        "raised-floor grid and the ceiling is a white grid carrying flat "
        "flush light panels that run away toward a vanishing point in warm "
        "cleanroom light. Walking away from the camera down the middle of "
        "the aisle, seen from behind, is a single cleanroom technician in a "
        "full plain white bunny suit with a white hood and white booties, "
        "mid-stride, arms relaxed, neither turning nor posing, their figure "
        "in sharp focus in the mid-ground and the far end of the aisle "
        "softening into haze. Along the left-hand tool a round silicon wafer "
        "sits on a stage beneath a small inspection head, its patterned "
        "surface holding a pale pool of light. Pale sealed wall panels, no "
        "signage anywhere, a faint cool-warm mix of cleanroom light with "
        "gentle reflections on the polished floor and soft shadows under "
        "the tool cabinets. Moderate depth of field with the nearest tool "
        "edge crisp and the far end of the corridor melting into soft blur, "
        "real optical blur, honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, subtle lens vignette, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
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
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
