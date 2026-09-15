#!/usr/bin/env python3
"""Generate hero for lumentum-laser-chokepoint-ai-optics-2026 (fal flux/schnell).

Subject: Lumentum Holdings — photonics / laser manufacturer. Indium phosphide
laser chips and the optical engines inside 800G/1.6T AI datacenter links, plus
optical circuit switches.

Scene chosen: the LIGHT-MAKING layer, NOT the data centre. Three candidate
compositions, one per ATTEMPT:
  1) photonics cleanroom macro — bunny-suit technician holding a gold-mirrored
     indium phosphide laser wafer with a vacuum wand, amber lithography light.
  2) laser test bench — gloved engineer coupling a lens mount to a die on a
     black optical breadboard, red laser spot, oscilloscope blurred behind.
  3) fiber-optic manufacturing bench — gloved hands coiling and inspecting
     single-mode fiber whose cleaved ends catch a warm point of light.

Deliberately NOT a data-center / server-room / server-aisle / rack-hallway
composition (overused on this site). No neon, no glowing lines, no HUD
overlays, no 3D-render look, no geometric patterns, no synthwave, no digital art.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: wafers carry scribe marks, benches carry labels, scopes carry
  readouts, so all lettering, numbers, barcodes and UI are explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-lite-laser-hero-20260915.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "lumentum-laser-chokepoint-ai-optics-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no user interface, no software windows, "
    "no dashboards, no instrument readouts, no oscilloscope trace labels, no "
    "toolbars, no menus, no icons, no file labels, no bin labels, no tape "
    "labels, no equipment nameplates, no model numbers, no serial numbers, "
    "no wafer scribe text, no die markings, no part numbers, no manufacturer "
    "logos, no brand names, no company names, no trademarks, no watermarks, "
    "no stickers, no barcodes, no QR codes, no printed signage, no safety "
    "signage, no warning labels, no charts, no wall posters, no badge "
    "lettering, no lanyards, no legible writing of any kind anywhere in the "
    "image. Any screen, monitor or instrument display in the frame is angled "
    "away, switched off, or so far out of focus that it shows only a soft "
    "flat wash of colour with absolutely nothing readable or drawn on it, "
    "like an out-of-focus colour field photograph, not a display with "
    "content. All surfaces are plain and unmarked, all garments are plain "
    "and unbranded, and the wafers, dies and fibres carry only plain mirror "
    "surfaces and unmarked metal. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no circuit diagram, no "
    "network diagram, no graph graphic, no futuristic HUD graphics, no "
    "overlay elements, no augmented-reality graphics, no data center, no "
    "server room, no server racks, no server aisle, no rack hallway, no "
    "cable runs, no server lights, no GPU hardware, no screen with text."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial industrial stock photograph, a tight macro "
        "detail shot inside a semiconductor photonics cleanroom. In the near "
        "foreground and tack sharp, a technician's gloved hands in white "
        "cleanroom gloves hold a small round indium phosphide laser wafer "
        "with a stainless vacuum wand, the wafer's surface a flawless "
        "iridescent gold and green mirror catching the overhead light, its "
        "edge catching a thin bright rim of reflection. The hands and the "
        "wand are crisp, the wafer occupies a large part of the frame. The "
        "technician's white bunny-suit hood, shoulders and pale face shield "
        "sit just behind the hands, softly out of focus, only the rounded "
        "white shape and the curve of the hood clearly readable. Behind "
        "them, dissolving into deep creamy bokeh, the cleanroom stretches "
        "away: rows of stainless-steel lithography and deposition machines "
        "with flat brushed-metal panels and soft amber and warm-white "
        "indicator glows, all smooth and featureless. The room is bathed in "
        "the warm amber-yellow light of cleanroom photolithography "
        "safelights, warm gold highlights rimming the wafer, the gloves and "
        "the machine edges against a shadowed room. Very shallow depth of "
        "field at macro range, the wafer and gloves pin sharp while "
        "everything beyond melts into smooth heavy bokeh, real optical blur, "
        "honest available-light editorial exposure, natural camera noise and "
        "very slight film grain, subtle lens vignette, faint dust in the "
        "air, no plastic CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a 100mm macro lens at f/2.8, not a render "
        "and not computer generated: a photonics laser test bench in a dim "
        "laboratory, shot at close range across a matte black optical "
        "breadboard. In the sharp foreground, a gloved engineer's fingers in "
        "white lint-free gloves turn a small knurled brass lens mount, "
        "aligning it above a tiny square laser die sitting on a small "
        "unmarked metal fixture, with a single hair-thin optical fibre "
        "curving away toward the back of the bench. A small intense red "
        "laser spot glows at the coupling point, throwing a faint warm red "
        "bloom across the fingertips and the brushed metal, the light "
        "physically reflected in the polish of the mount. Around it on the "
        "black bench surface lie plain unmarked patch cords, a small "
        "stainless screwdriver and a plain metal tweezer, all softly lit. In "
        "the blurred background, a bench oscilloscope and a rack of lab "
        "equipment stand as dark anonymous shapes with soft warm indicator "
        "glows and display panels that are blank, dark and completely "
        "unreadable, out of focus to smooth flat washes of light. The lab is "
        "dark and quiet, lit only by a warm practical lamp above the bench "
        "and the small red laser spot, deep shadows filling the corners. "
        "Extremely shallow depth of field holding the fingers, the lens "
        "mount and the die crisp while the bench and instruments melt into "
        "creamy bokeh, real optical blur, honest available-light editorial "
        "exposure, natural camera noise and very slight film grain, subtle "
        "lens vignette, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine documentary-style photograph, not a render and not "
        "computer generated, of an optical fibre manufacturing bench, "
        "composed as a close editorial frame. In the sharp near foreground, "
        "two hands in white lint-free cleanroom gloves carefully coil and "
        "inspect a loose bundle of single-mode optical fibres, the glass "
        "hair-thin strands looping in gentle arcs between the fingers, "
        "translucent and catching the light, their cleaved ends glowing as "
        "tiny warm points of light where the lamp catches them. The gloves, "
        "the fingertips and the nearest fibres are tack sharp, showing the "
        "fine texture of the glove and the smooth glass. On the plain matte "
        "bench below sit a small stainless steel spool, a plain metal "
        "cleaving tool and a folded white lint-free cloth, all unmarked. "
        "Behind the hands the bench falls away into beautiful smooth bokeh: "
        "a white cleanroom wall, the soft blurred bulk of a fibre draw "
        "tower and a coiling machine as pale featureless shapes, everything "
        "beyond the hands dissolved into creamy blur with no writing and no "
        "detail legible anywhere. The lighting is warm and practical from a "
        "bench lamp above and slightly behind, rimming the gloves and the "
        "fibre bundle with a soft warm highlight against a cool neutral "
        "background. Very shallow depth of field at macro range, real "
        "optical blur, honest available-light editorial exposure, natural "
        "camera noise and very slight film grain, subtle lens vignette, "
        "faint dust in the air, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
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
