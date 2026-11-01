#!/usr/bin/env python3
"""Generate hero for ai-gpu-depreciation-accounting-explainer-2026 (fal flux/schnell).

Subject: how AI hardware is depreciated — the accounting useful life of GPUs and
servers, capex versus depreciation. The metaphor: an aging asset being costed
out on paper. Accounting meets hardware.

MANDATORY SCENE: a used data-center GPU accelerator card (large metal-shrouded
PCIe card with visible gold-finger connector and fans) lying flat on a plain
wooden desk beside a printed spreadsheet of asset schedules and a pair of
reading glasses. Natural window light raking across the desk, shallow depth of
field, muted neutral colours, slight dust on the card's shroud. Nothing else on
the desk.

Deliberately NOT: data center hallway / server aisle / rows of racks, neon or
glowing lines, holograms, abstract or digital art, charts on screens, text.

Rules:
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: no legible letters/numbers/logos/brand names anywhere. The printed
  sheet reads as a grid of blank cells and faint ruled lines only — out-of-focus
  so no glyph is resolvable.
- Generate 1440x810, finalize 1536x864, hard cap 400KB.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
  scripts/gen-gpu-depreciation-hero-20261101.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ai-gpu-depreciation-accounting-explainer-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The image contains no readable text anywhere: no letters, no words, no "
    "numbers, no digits, no legible printed characters, no logos, no brand "
    "names, no manufacturer marks, no part numbers on the circuit board, no "
    "silkscreen lettering, no stickers with writing, no serial labels, no "
    "watermark, no caption, no signature. The printed sheet in the frame is a "
    "softly out-of-focus page carrying only a faint grid of thin ruled lines "
    "and pale empty cells, its characters unresolvable and illegible. Every "
    "surface in the frame is plain and unmarked. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no glowing laser lines, "
    "no synthwave, no futuristic HUD overlays, no holograms, no augmented "
    "reality graphics, no abstract data visualisation, no charts on screens, "
    "no data center hallway, no server aisle, no rows of server racks, no "
    "blinking status LEDs."
)

PROMPTS = {
    # 1 — primary: GPU card flat on a wooden desk, spreadsheet + glasses, window light
    "1": (
        "Photo-realistic professional editorial stock photograph, shot at a "
        "low three-quarter angle across a plain oak wooden desk in a quiet "
        "office, landscape orientation. Lying flat in the centre of the frame: "
        "a single large used data-center GPU accelerator card — a heavy "
        "double-slot graphics card about a forearm's length, its entire top "
        "surface covered by a long matte brushed-aluminium and dark grey "
        "plastic shroud with two large black axial cooling fans, the fans' "
        "blades and central hubs clearly moulded, a few fine scratches and a "
        "light film of grey dust settled in the grooves and along the shroud "
        "edges, the shroud plain and completely unmarked with no printing, no "
        "badge and no logo. Its rear end shows the exposed gold-finger PCIe "
        "edge connector gripping the light as a strip of warm metal, and a "
        "bracket plate along one side. Just behind it and slightly to the "
        "right, a printed spreadsheet lies on the desk at a shallow angle: a "
        "single sheet of white paper covered by a faint even grid of thin "
        "pale grey ruled lines and empty cells, its type entirely "
        "out of focus and illegible, paper edges slightly curled. A pair of "
        "thin wire-frame reading glasses rests folded on the paper, one "
        "temple arm catching a fine specular line. Soft natural daylight "
        "rakes in from a window at the left of the frame, dropping a long "
        "soft-edged shadow off the card across the wood grain, warm on the "
        "lit end and cool grey in the shadow, muted neutral colour palette, "
        "no strong colours, honest wear in the desk surface, a faint ring "
        "mark and a few dust motes suspended in the beam. Shot on a "
        "full-frame camera with an 85mm lens at f/2.0, shallow depth of "
        "field — the nearest fan and the gold connector tack sharp, the "
        "paper and the far end of the card melting into smooth creamy "
        "bokeh, real optical blur, natural fine sensor grain, no glossy CGI "
        "sheen, unretouched documentary realism, slightly imperfect "
        "handheld framing. 16:9 landscape composition. " + NO_TEXT
    ),
    # 2 — wider desk view, card to the left, paperwork to the right
    "2": (
        "Photo-realistic editorial photograph of a work desk in a quiet "
        "office, landscape orientation, natural available light only. A used "
        "data-center GPU accelerator card lies flat on the plain light-wood "
        "desktop in the left half of the frame, seen from a slightly raised "
        "three-quarter angle: a long double-slot card in a matte grey metal "
        "and black plastic shroud with two large circular cooling fans, "
        "visible screw heads, a dust film in the deep fins at its edges, its "
        "exposed gold-finger edge connector at the near end catching a warm "
        "glint, the whole shroud plain and unprinted. To its right, a "
        "printed page of a spreadsheet sits square on the desk and on top of "
        "it a pair of thin round wire-frame reading glasses lies folded "
        "open, both lenses and the bridge plainly recognisable, one lens "
        "taking a soft rectangular window reflection; the page shows only a "
        "faint grid of thin ruled lines and pale empty cells, every "
        "character soft and unresolvable at this focus distance. Nothing "
        "else at all rests on the desk — no book, no mug, no keyboard, no "
        "cables, no box — the wood is otherwise completely clear, grain and a few "
        "fine scratches visible, surface fading to shadow at the frame "
        "edges. Late afternoon window light comes from the upper left, "
        "raking low across the desk at a shallow angle, stretching long soft "
        "shadows from the card and the glasses toward the lower right, "
        "dust motes drifting in the light shaft, the far wall falling into "
        "warm neutral shadow out of focus. Muted desaturated colours, "
        "grey-brown and cream. Shot on a full-frame camera with a 50mm lens "
        "at f/1.8 at close range, shallow depth of field focused on the "
        "card's near fan and connector, natural falloff and gentle vignette, "
        "fine film-like grain, true photographic texture, no retouching, "
        "candid and unstyled. 16:9 landscape composition. " + NO_TEXT
    ),
    # 3 — primary composition of attempt 1 hardened: card + glasses + empty grid
    "3": (
        "Photo-realistic professional editorial stock photograph, shot at a "
        "low three-quarter angle across a plain oak wooden desk in a quiet "
        "office, landscape orientation. Lying flat in the centre-left of the "
        "frame: a single large used data-center GPU accelerator card — a "
        "heavy double-slot graphics card about a forearm's length, its top "
        "surface covered by a long matte brushed-aluminium and dark grey "
        "plastic shroud carrying two large black axial cooling fans with "
        "finely moulded blades and plain central hubs, a film of fine grey "
        "dust settled in the grooves, along the screw recesses and on the "
        "shroud edges, a couple of faint handling scuffs, the shroud "
        "entirely plain with no printing, no sticker and no badge. Its rear "
        "end exposes the gold-finger PCIe edge connector as a strip of warm "
        "metal catching the light. Immediately to the right of the card, a "
        "single sheet of white printed paper lies on the desk at a shallow "
        "angle, its surface covered only by a faint even grid of thin pale "
        "grey ruled lines forming empty cells — every cell is completely "
        "blank, there is no index column, no row numbering, no digits and no "
        "type of any kind on the page. Resting diagonally across the paper, "
        "a pair of thin round wire-frame reading glasses, folded, both "
        "lenses intact and one temple arm throwing a fine shadow: they are "
        "held in focus and clearly recognisable. The desk around them is "
        "completely empty — no keyboard, no book, no mug, no cables, no "
        "notebook, nothing else at all — bare wood grain with a few fine "
        "scratches, falling away to shadow at the frame edges. Soft natural "
        "daylight rakes in low from a window at the left, dropping soft "
        "long shadows to the right and revealing the dust, warm at the lit "
        "end of the card and cool grey in the shadow, muted desaturated "
        "neutral palette, a few dust motes suspended in the beam. Shot on a "
        "full-frame camera with an 85mm lens at f/2.8, shallow depth of "
        "field — the near fan, the gold connector and the glasses all "
        "reasonably sharp while the far end of the card and the desk behind "
        "melt into smooth creamy bokeh, real optical blur, natural fine "
        "sensor grain, honest contrast, unretouched documentary realism, "
        "no CGI sheen, slightly imperfect handheld framing. 16:9 landscape "
        "composition. " + NO_TEXT
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
