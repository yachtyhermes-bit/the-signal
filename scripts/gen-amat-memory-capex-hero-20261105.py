#!/usr/bin/env python3
"""Generate hero for amat-memory-capex-test-2026 (fal flux/schnell).

Subject: Applied Materials (NASDAQ: AMAT) — semiconductor fabrication equipment:
deposition, etch, ion implant, CMP tools sold into memory and logic fabs.

Scene chosen: a SEMICONDUCTOR CLEANROOM / FAB BAY, never a data center.

  ATTEMPT 1 — technician in a white full-body cleanroom suit and hood loading a
  300mm silicon wafer into an advanced deposition/etch tool; load port and wafer
  cassette in sharp focus, mirrored wafer catching amber bay lighting, stainless
  chamber and cable bundles, overhead wafer-transport track in soft bokeh.
  ATTEMPT 2 — robotic transfer arm holding one mirror-polished 300mm wafer in a
  fab bay, technician silhouetted behind glass.
  ATTEMPT 3 — extreme close-up of a wafer cassette holding a stack of 300mm
  wafers, amber-lit fab corridor behind.

Deliberately NOT a data-center hallway / server aisle / server racks. No digital
art, neon, synthwave, glowing lines, geometric abstraction, text, logos.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-amat-memory-capex-hero-20261105.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amat-memory-capex-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
REPO_COPY = f"/home/chino/thesignal/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no labels, no stickers, no barcodes, no "
    "part numbers, no printed markings, no silkscreen text, no display showing "
    "characters, no brand names, no logos, no watermark, no captions, no "
    "legible writing of any kind anywhere. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no synthwave, no glowing "
    "geometric lines, no light trails, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no charts, no "
    "graphs, no data visualization. This is a semiconductor wafer fabrication "
    "cleanroom, not a data center: no server aisle, no server racks, no rack "
    "of blinking lights, no computer room, no corridor of black cabinets. "
    "Surfaces are bare and unmarked: no control panel with digits, no small "
    "black display screens, no digital readouts, no part numbers stamped into "
    "metal, no bottles, no spray cans, no containers with labels, no gaffer "
    "tape with writing, no clipboard, no paperwork."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 35mm lens at f/2.0, real available cleanroom light, not a "
        "render and not CGI: inside a semiconductor wafer fabrication cleanroom. "
        "In the foreground, in sharp focus, the load port of a large stainless "
        "steel deposition tool: a matte brushed-steel front panel with a recessed "
        "wafer transfer opening, a black anodised load-port plate, and an open "
        "front-opening wafer pod holding a stack of mirror-polished 300mm "
        "silicon wafers, their surfaces reflecting the room in faint rainbow "
        "diffraction. A technician in a white full-body cleanroom coverall with "
        "a white hood, face mask and blue nitrile gloves stands at the tool, "
        "turned three-quarters away from camera, gloved hands lifting a single "
        "mirror-finish 300mm wafer by its edge toward the load port; the wafer "
        "catches a soft amber reflection of the bay lighting across its polished "
        "face. Behind the tool, out-of-focus, stainless steel process chambers, "
        "thick corrugated cable bundles in dark grey sleeving, pneumatic tubing "
        "and a dense manifold of valves, and above them an overhead track for "
        "automated wafer transport receding into the shallow depth of field. "
        "Floor is a pale grey epoxy cleanroom floor with faint scuffing; walls "
        "are white honeycomb cleanroom panels with a dark grilled air return. "
        "Warm amber-tinted bay lighting from ceiling panels mixed with cool "
        "white task light, soft and diffuse, no glare, nothing emitting its own "
        "light, no LED strips, no status lamps lit. Very shallow depth of field: "
        "the load port, the wafer stack and the gloved hands are razor sharp, "
        "the technician, chambers and overhead track melt into soft bokeh. Real "
        "optical lens blur, natural sensor noise, fine film grain, subtle "
        "vignette, honest metal and polymer texture, slightly off-centre casual "
        "framing, no plastic CGI sheen, no perfect symmetry. Photorealistic, "
        "extremely high detail, authentic editorial stock photography, 16:9 "
        "landscape composition, wide horizontal framing. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 50mm lens at f/2.2, real available cleanroom light, not a "
        "render and not CGI: a semiconductor fabrication bay seen through the "
        "thick glass of a cleanroom window. Just inside the glass, in sharp "
        "focus, a robotic wafer transfer arm of pale grey machined aluminium "
        "extends from a stainless steel deposition tool, its end effector "
        "holding a single mirror-polished 300mm silicon wafer perfectly level; "
        "the wafer is a flawless silver-grey mirror disc with a faint "
        "iridescent sheen, its surface so reflective that it mirrors the amber "
        "ceiling lights and the white panels of the bay as a pale, soft, "
        "distorted reflection; the disc is perfectly smooth, absolutely "
        "unmarked, with no radial brushing, no concentric grooves, no "
        "engraving, no gold or brass tint, reading unmistakably as polished "
        "silicon. Behind the arm, "
        "softly out of focus, a technician in a white full-body cleanroom suit, "
        "hood and face mask stands beside the tool watching the transfer, "
        "silhouetted against the bright bay, face not identifiable. Further back, "
        "a row of tall stainless steel process tools with dark grilled vents "
        "and ribbed cable bundles along their bases, an overhead monorail track "
        "for automated wafer transport running across the top of the frame, and "
        "a pale grey epoxy floor with faint reflections. Faint dust specks and "
        "smeared fingerprint haze on the window glass in the foreground add "
        "honest optical imperfection. Warm amber ceiling lighting, soft and "
        "diffuse with cool white fill, nothing emits its own light, no LED "
        "strips, no lit indicators. Shallow depth of field: the wafer and the "
        "robot end effector are razor sharp, the technician and the far tools "
        "fall into gentle bokeh. Real lens blur, natural sensor noise, fine film "
        "grain, subtle vignette, believable brushed steel and anodised aluminium "
        "texture, slightly off-centre framing, no CGI sheen, no perfect "
        "symmetry. Photorealistic, extremely high detail, authentic editorial "
        "stock photography, 16:9 landscape composition, wide horizontal "
        "framing. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic editorial photograph, shot on a full-frame camera with "
        "a 100mm macro lens at f/2.5, hand-held, available cleanroom light, on "
        "Kodak Portra 400 film, not a render and not CGI: an extreme close-up "
        "inside a working semiconductor wafer fabrication cleanroom, at the load "
        "port of a deposition tool. In the sharp focal plane, a white moulded "
        "polymer wafer cassette stands open, its shelf teeth holding a vertical "
        "stack of 300mm silicon wafers viewed almost edge-on from slightly "
        "below, so the discs read as a receding row of thin bright ellipses. "
        "Each wafer face is a flawless dark mirror that reflects the room as a "
        "soft inverted image with one thin hard specular highlight sliding "
        "along its curved edge; the wafer edges are matte grey, roughly a "
        "millimetre thick, with a barely visible flat notch on the nearest "
        "disc. The discs are glassy and perfectly smooth, never brushed, never "
        "radial, never golden. The cassette sits on a black anodised load-port "
        "plate with two polished steel locating pins and a machined hinge, and "
        "the plate meets the brushed stainless steel front of the tool, which "
        "carries real wear: faint handling scuffs, a smear of fingerprint oil, "
        "a hairline scratch, small dust specks settled in the panel seams. In "
        "the soft background bokeh, a cleanroom corridor recedes in warm amber "
        "light, its white honeycomb wall panels and ceiling luminaires reduced "
        "to soft glowing rectangles, with the blurred white shape of a "
        "technician in a cleanroom coverall walking away. Warm amber ambient "
        "light from the corridor with a cool white fill from the left, gentle "
        "and diffuse, slightly overexposed in the highlights like film, nothing "
        "emitting its own light, no LED strips, no lit indicator lamps. Very "
        "shallow depth of field, real macro lens bokeh with visible cat's-eye "
        "shaping, natural sensor noise, fine film grain, faint dust motes "
        "floating in the air, slight chromatic aberration at the frame edges, "
        "subtle vignette, framing slightly off-centre and casual, no CGI sheen, "
        "no perfect symmetry. Photorealistic, extremely high detail, "
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 60:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")
    os.makedirs(os.path.dirname(REPO_COPY), exist_ok=True)
    shutil.copy(OUTPUT, REPO_COPY)
    print(f"Mirrored to {REPO_COPY}")


if __name__ == "__main__":
    main()
