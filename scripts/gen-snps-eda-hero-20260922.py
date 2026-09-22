#!/usr/bin/env python3
"""Generate hero for snps-eda-ai-chip-design-toll-2026 (fal flux/schnell).

Subject: Synopsys (SNPS) — the EDA software company. Its design tools, verification
and silicon IP are what every AI chip is designed with. This is a chip-DESIGN story,
NOT a data-center / fab-manufacturing / server story.

Scene chosen: a semiconductor DESIGN ENGINEER at a large monitor showing a complex
chip floorplan / layout, hands on the keyboard, in a modern office. The screen is
covered by the chip floorplan itself (interlocking blocks of coloured area and
hairline routing) — no text, no labels, no charts, no dashboards.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT a cleanroom or wafer-inspection tool, NOT abstract digital
art, NOT a 3D render, NOT neon / synthwave, NOT glowing lines, NOT geometric
patterns, NOT a chart or graph on the screen.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: software screens are full of menus, labels and numbers, so all
  lettering, numbers, UI chrome, logos and brand names are explicitly forbidden.
  The only thing visible on the monitor is the layout geometry itself.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-snps-eda-hero-20260922.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "snps-eda-ai-chip-design-toll-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no code, no file names, no menu bars, "
    "no toolbars, no window titles, no tabs, no software user interface "
    "chrome, no icons, no cursors with labels, no dashboards, no charts, no "
    "graphs, no plots, no axes, no legends, no readouts, no gauges with "
    "numerals, no signage, no wall placards, no posters, no whiteboards with "
    "writing, no sticky notes with writing, no printed documents, no books "
    "or manuals with titles, no name badges, no lanyards, no brand names, no "
    "manufacturer names, no company names, no corporate logos, no trademarks, "
    "no watermarks, no stickers, no barcodes, no QR codes, no handwriting, no "
    "legible writing of any kind anywhere in the image. The large monitor "
    "shows ONLY the chip layout itself: an arrangement of solid coloured "
    "rectangular blocks and very fine hairline routing traces packed tightly "
    "edge to edge, a dense mosaic of geometric area only — nothing is written, "
    "labelled, numbered, annotated or highlighted on it, it is purely a "
    "colour-and-texture field of layout geometry, not a chart, not a graph "
    "and not a dashboard. The keyboard is plain and its keys carry no "
    "lettering. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no glowing lines, no light trails, no synthwave, no "
    "abstract geometric art, no floating holographic blocks, no artificial "
    "overlay graphics, no augmented-reality graphics, no circuit-board "
    "graphics superimposed on the room, no data center, no server room, no "
    "server racks, no server aisles, no cable runs, no server lights, no GPU "
    "hardware, no cleanroom, no bunny suit, no wafer-inspection tool."
)

PROMPTS = {
    # 1 — design engineer at a large monitor showing a chip floorplan, modern office.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera, of a semiconductor design engineer at "
        "work at their desk in a modern office. In the sharp centre of frame "
        "a large desktop monitor is angled three-quarters toward the camera, "
        "and its screen is filled edge to edge with the intricate floorplan "
        "of a processor chip: a dense, tightly packed mosaic of solid "
        "rectangular blocks in muted slate blue, soft teal, dull olive and "
        "warm grey, criss-crossed by hairline routing traces and rows of tiny "
        "uniform logic cells, layer over layer, like an aerial view of an "
        "enormous city block layout rendered in flat colour. The layout is "
        "complex and busy but purely geometric colour — nothing is written or "
        "annotated on it. In front of the monitor, seen from the side and "
        "slightly behind, a woman in her thirties wearing a plain dark "
        "knit sweater sits turned toward the screen, both hands resting on a "
        "plain keyboard on a pale wooden desk, one hand lifted mid-keystroke, "
        "her expression focused and calm, mid-task, not posing. Her face is "
        "in near-profile, softly lit by the monitor's glow from the front and "
        "by daylight from a window on the left, and her figure is sharp from "
        "shoulders to hands. The desk is uncluttered: a plain white ceramic "
        "mug, a small plain notebook with blank pages, a thin stylus, a "
        "second smaller monitor behind turned away from the camera with its "
        "screen dark. The office behind her is soft and modern: pale grey "
        "walls, a warm oak desk surface, a muted green potted plant out of "
        "focus at the edge of frame, blurred silhouettes of other desks and "
        "daylight through a large window in the far background. Warm natural "
        "key light from the window on the left with cool monitor glow "
        "filling the shadow side of her face, gentle falloff into the room, "
        "soft realistic shadows across the desk, subtle colour harmony "
        "between the warm daylight and the cool screen. Very shallow depth "
        "of field: the monitor layout and her hands are tack sharp while the "
        "office behind melts into creamy bokeh. Real optical lens blur, "
        "honest available-light editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — two engineers at a lab bench examining a silicon die under a microscope, warm lab light.
    "2": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens at "
        "f/1.8 on a full-frame camera, of two semiconductor engineers working "
        "together at a laboratory bench in a warm-lit lab. In the sharp "
        "centre of frame, on the bench in front of them, a bare silicon die "
        "about two centimetres square lies on a plain white tray, its "
        "mirror-polished surface catching a soft iridescent sheen of "
        "teal and violet where the light rakes across it, held at its corner "
        "by a pair of fine stainless-steel tweezers in a gloved hand. An "
        "inspection microscope on a black articulated arm leans in from the "
        "right above the die, its lens barrel and focus knobs crisp in the "
        "mid-ground. The two engineers, a man and a woman both in their "
        "thirties in plain grey and navy button-up shirts with no badges, "
        "lean over the bench side by side in profile to the camera, heads "
        "close together, absorbed in what they are examining, one with a "
        "hand resting on the microscope's focus knob, mid-task and not "
        "posing. Warm tungsten bench lighting from an adjustable task lamp "
        "on the left plus soft diffuse daylight from a window at the back of "
        "the room, gentle warm highlights along their faces, hands and the "
        "die, soft shadows under the bench equipment, a warm amber-to-grey "
        "tonal palette. The bench surface is plain and uncluttered: a "
        "brushed-steel base plate, a plain white tray, a small plain "
        "anti-static mat, a plain grey cable sweeping out of focus toward "
        "the frame edge. The lab behind them is a soft wash of pale grey "
        "cabinets, instrument housings and window light, all far out of "
        "focus; every screen or display in the room is dark, switched off or "
        "angled away. Very shallow depth of field: the die, tweezers and "
        "microscope front are tack sharp while the two engineers and the lab "
        "behind melt into creamy bokeh. Real optical lens blur, honest "
        "available-light editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
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
