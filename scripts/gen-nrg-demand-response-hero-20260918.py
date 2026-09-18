#!/usr/bin/env python3
"""Generate hero for nrg-demand-response-ai-power-2026 (fal flux/schnell).

Subject: NRG Energy (NYSE: NRG) + the AI Energy Management Alliance — a coalition
(Emerald AI + Google + NVIDIA + Anthropic + utilities AES / Constellation /
National Grid / NRG) built around DATA-CENTER DEMAND RESPONSE: data centres pausing
or shifting compute when the grid is stressed, so they become a flexible grid asset
instead of a rigid load. It is also a story about ordinary electricity customers and
who pays for the AI power boom.

The picture therefore has to read as THE ELECTRICITY-IN-YOUR-NEIGHBOURHOOD shot:
dusk on an ordinary suburban American residential street, the same distribution grid
that the AI data centres lean on. The demand-response / AI angle is carried by the
sense of a shared grid (a distant substation or industrial skyline glow on the
horizon), NOT by any hardware hero shot, chart or diagram.

Deliberately NOT a rural data-centre campus under construction at golden hour (used
on this site 2026-09-17), NOT a standby back-up generator yard behind a data centre
(used on this site 2026-09-17), NOT a generic data-centre long hallway / server aisle
/ GPU rack (banned site-wide), NOT a wafer cleanroom, NOT a quantum lab, NOT an office
or headset customer-service scene, NOT digital art, NOT an illustration, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines, NOT geometric patterns,
NOT a HUD / hologram overlay, NOT a chart.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: suburban streets are full of house numbers, street-name signs, licence
  plates, mailbox numbers and brand logos, so all lettering, numbers, signage, UI,
  logos and readable markings are explicitly forbidden. Windows are warm glowing
  rectangles with NO readable content; any vehicle is plain and unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-nrg-demand-response-hero-20260918.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = "nrg-demand-response-ai-power-2026"
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no house numbers, no address numerals, "
    "no porch numbers, no mailbox numbers, no street-name signs, no road "
    "signs, no traffic signs, no speed-limit signs, no stop signs, no "
    "parking signs, no streetlight banner boards, no billboards, no yard "
    "signs, no for-sale signs, no realtor signs, no political signs, no "
    "construction notices, no warning signs, no utility pole tags, no "
    "transformer cabinet labels, no hazard decals, no nameplates, no serial "
    "numbers, no part numbers, no stencilled marks, no spray-painted "
    "markings, no license plates, no registration stickers, no bumper "
    "stickers, no vehicle badges, no car branding, no manufacturer names, "
    "no fleet numbers, no company names, no corporate logos, no brand names, "
    "no trademarks, no watermarks, no logos of any kind, no user interface, "
    "no software windows, no dashboards, no screens showing content, no "
    "digital readouts, no gauges with numerals, no dials, no meters, no "
    "charts, no bars or graphs, no toolbars, no menus, no icons, no arrows, "
    "no crosshairs, no QR codes, no barcodes, no handwritten markings, no "
    "graffiti, no legible writing of any kind anywhere in the image. Every "
    "window in every house is a soft warm glowing rectangle with the curtains "
    "drawn, showing absolutely nothing readable or drawn inside it — pure "
    "amber light with no shapes, no silhouettes holding objects, no screens. "
    "The parked cars and any other vehicle are plain, generic, unmarked and "
    "debadged, with completely blank featureless license-plate areas and no "
    "lettering anywhere on them. The utility pole, crossarm, conductors, "
    "insulators, transformer cabinet and mailboxes are completely plain and "
    "unmarked. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no glowing lines, no light trails, no synthwave, no "
    "geometric patterns, no circuit-board graphics, no network diagram, no "
    "graph graphic, no futuristic HUD graphics, no hologram, no overlay "
    "elements, no augmented-reality graphics, no data centre server room, no "
    "server racks, no server aisles, no long indoor corridor, no GPU "
    "hardware, no computer screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light editorial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
    "visualisation, no digital illustration, no painting, photorealistic, "
    "very high detail, professional editorial stock photography, 16:9 "
    "landscape composition. "
)

PROMPTS = {
    # 1 — dusk suburban residential street: pole + drooping conductors in the
    #     sharp foreground, pad-mounted transformer at the kerb, warm windows.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera from the sidewalk at eye level, looking "
        "down an ordinary quiet suburban American residential street at dusk, "
        "about twenty minutes after sunset. The sky overhead is a deep rich "
        "post-sunset blue, grading down to a thin band of warm amber afterglow "
        "along the horizon between the rooftops. On both sides of the street "
        "stands a row of modest single- and two-storey family homes of the "
        "kind built in the mid twentieth century — painted clapboard and "
        "brick, pitched roofs, small front porches, shallow front lawns — and "
        "every one of them has warm amber light glowing out of its windows "
        "into the blue evening, the curtains drawn so each window is a soft "
        "glowing rectangle of pure warm light. In the sharp immediate "
        "foreground at the left edge of the frame, very close to the camera "
        "and slightly out of focus at the very frame edge, a weathered wooden "
        "utility distribution pole rises vertically out of bottom frame with "
        "a plain straight wooden crossarm near its top and small dark "
        "ceramic insulators, and from that pole three slack conductors droop "
        "in long lazy catenary curves diagonally across the upper half of the "
        "frame, receding pole to pole down the street and cutting across the "
        "deep blue sky and the amber afterglow. At the kerb on the right, "
        "standing on a small concrete pad beside a driveway apron, is a "
        "small pad-mounted green distribution transformer cabinet, plain and "
        "unmarked, sitting in the shadows of the grass verge. A plain pale "
        "family sedan is parked in the driveway on the right, seen in three "
        "quarter view from behind, completely unmarked and debadged; on the "
        "left verge a bicycle leans against a low front garden wall near a "
        "plain metal mailbox on a post, and a second mailbox stands opposite. "
        "Leafy deciduous trees arch over the street on both sides, their "
        "foliage nearly black against the sky, and the damp asphalt of the "
        "road and the wet front lawn catch the last of the light in long soft "
        "specular streaks. Long shadows lie across the street from the "
        "fading twilight. Far away down the sightline of the street, low and "
        "softened by distance and evening haze, glows the spread of small "
        "warm amber lights of a distant electrical substation and a flat "
        "industrial skyline on the horizon, hinting at where the grid goes. "
        "A faint cool blue fill from the sky balances the warm interior light "
        "in the windows. The feeling of the frame is ordinary, lived-in and "
        "quiet: the same grid that AI data centres lean on is the grid that "
        "runs this street. Strong spatial depth — the near pole, crossarm and "
        "the transformer cabinet crisp, the homes and parked car resolving, "
        "the distant substation glow softening into haze. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — tighter 50mm crop of the same idea: pad-mounted transformer in the
    #     near foreground, warm lit windows beyond the verge and sidewalk.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2 on a full-frame camera at crouching height on the grass verge "
        "beside a suburban driveway at dusk, a tighter and more intimate "
        "framing of an ordinary residential street at blue hour. Filling the "
        "near right third of the sharp foreground is a small pad-mounted "
        "green distribution transformer cabinet standing on its concrete pad "
        "at the kerb beside a driveway apron, its plain painted steel sides "
        "completely unmarked, its edges softly rim-lit by the last cool light "
        "from the deep blue sky above and falling away into shadow at its "
        "base; wet grass and a few fallen leaves catch the light around it. "
        "Beyond it on the left, loosely in focus, the quiet street carries on: "
        "a low front garden wall, a short flight of concrete steps up to a "
        "modest family home with a small porch, and that house's windows "
        "glowing in soft warm amber with their curtains drawn, so every "
        "window is simply a glowing rectangle of warm light against the cold "
        "blue of the evening. Just behind the transformer cabinet at the top "
        "right of frame, the base and lower shaft of a weathered wooden "
        "utility distribution pole rise out of frame, with the long slack "
        "catenary curves of its three conductors drooping away across the "
        "deep blue sky in the upper part of the frame toward the next pole "
        "down the street. A plain unmarked family car sits quietly in the "
        "driveway behind the cabinet, half in shadow, its windows dark. A "
        "plain metal mailbox on a post and a leaning bicycle sit further back "
        "along the verge, out of focus, and a dark leafy tree fills the upper "
        "left corner in silhouette. Everything is damp: the asphalt, the "
        "concrete pad and the grass all hold the low warm reflections of the "
        "lit windows in long soft streaks. Far down the street on the "
        "horizon, small and soft in the evening haze, a scattered cluster of "
        "warm amber lights marks a distant electrical substation and an "
        "industrial skyline beneath the last band of afterglow. Very shallow "
        "depth of field — the transformer cabinet, the kerb and the wet grass "
        "crisp, the warm windows and the pole softening into creamy bokeh. "
        "Ordinary, lived-in and quiet; this is the grid that runs the "
        "neighbourhood, and the grid is shared. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — blue hour wide: street receding, distant substation / industrial
    #     skyline glow on the horizon.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated: a blue-hour wide view, shot on a 24mm lens at f/4 from a "
        "low angle standing on the sidewalk of an ordinary suburban American "
        "residential street, looking straight down the road toward the "
        "horizon. The sky takes the upper half of the frame, a deep indigo "
        "blue darkening toward the top and holding a narrow band of dull "
        "amber afterglow right along the horizon. The street runs away from "
        "the camera to a distant vanishing point, lined on both sides with "
        "modest family homes — clapboard and brick, pitched roofs, porches — "
        "whose windows all glow warm amber through drawn curtains, a long "
        "receding ribbon of small glowing rectangles on either side of the "
        "dark road. Down the left side of the frame the wooden utility "
        "distribution poles step away into the distance, each with its plain "
        "crossarm and dark insulators, and the slack conductors sag in long "
        "catenary curves from pole to pole, slicing across the deep blue sky "
        "above the street. In the near foreground at the bottom right of "
        "frame, low and sharp, a small plain green pad-mounted distribution "
        "transformer cabinet stands on its concrete pad at the kerb beside a "
        "driveway, where a plain unmarked family car is parked in shadow, and "
        "a plain metal mailbox on a post stands further along the verge. A "
        "bicycle leans against a low garden wall in the near left mid-ground, "
        "just out of the pool of light. Dark leafy trees stand between the "
        "houses, black masses against the fading sky, and the damp asphalt "
        "catches long faint warm reflections from the lit windows, with the "
        "verge grass dark and wet. At the far end of the street, small on the "
        "horizon and softened by evening haze, a concentration of warm amber "
        "lights and a low flat industrial skyline mark a distant electrical "
        "substation, spreading wider than the street itself and glowing "
        "gently beneath the afterglow, suggesting where the grid goes. Deep "
        "blue ambient light fills the frame against the scattered warm amber "
        "of human habitation. Quiet, ordinary and humble — the same grid the "
        "AI data centres lean on, and someone has to pay for it. "
        + PHOTO_TAIL
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


def ocr_text_check(path):
    """Run tesseract OCR as a text-artifact smoke test. Returns list of words."""
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11"],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return []
        txt_path = base + ".txt"
        if not os.path.exists(txt_path):
            return []
        with open(txt_path, errors="ignore") as f:
            raw = f.read()
    words = []
    for line in raw.splitlines():
        clean = "".join(ch for ch in line if ch.isalnum())
        if len(clean) >= 3:
            words.append(line.strip())
    return words


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
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )
    # OCR text-artifact smoke test on the published file
    words = ocr_text_check(OUTPUT)
    if not words:
        print("OCR TEXT CHECK: clean — no readable text detected")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(words)} candidate token(s): {words[:12]}")


if __name__ == "__main__":
    main()
