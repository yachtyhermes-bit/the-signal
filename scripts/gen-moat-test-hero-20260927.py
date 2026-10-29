#!/usr/bin/env python3
"""Generate hero for economic-moat-test-ai-durability-2026 (fal flux/schnell).

Subject: an evergreen explainer on ECONOMIC MOATS — what makes a business
durable, and how switching costs, network effects and scale create a chokepoint
that everyone else has to pay to cross. Sector: INVESTING / BUSINESS STRATEGY.

The story is a CHOKEPOINT YOU PAY TO CROSS, so the picture is a physical,
real-world chokepoint: a large cargo vessel held inside the concrete chamber of
a ship canal lock at golden hour — a human-scale infrastructure scene, NOT a
metaphor drawn on a screen, NOT a data center, NOT an abstract of "moats".

Scene set for the three attempts (all inside these bounds):
  1 — wide documentary frame from the quayside looking along the lock chamber:
      the cargo ship filling the left two-thirds of frame, the concrete lock
      wall running diagonally toward the foreground, a lock gate and bollards
      in the mid-ground, still water, low warm sun and long shadows.
  2 — tighter three-quarter crop from a deckhand's viewpoint at the waterline:
      the rust-streaked hull of the vessel close and towering, a heavy mooring
      bollard and mooring line sharp in the foreground, the lock gate behind.
  3 — high angle from above the lock: looking down at the vessel filling the
      narrow chamber between two concrete walls, chamber water and walkway,
      gates at the far end.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack /
cable-run composition (banned), NOT semiconductor cleanroom or wafers, NOT
neon / synthwave, NOT glowing lines, NOT geometric patterns, NOT digital art /
3D render / CGI / HUD overlay, NOT abstract, NOT satellite dishes, NOT
transmission-tower yards, NOT a trading floor, NOT a coffee-and-notebook desk
shot (all recently used on this site).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: ships, containers, locks and quaysides are wall-to-wall with hull
  names, IMO/registration numbers, port-of-registry lines, draught marks,
  container codes, depth gauges, safety placards and signage, so all lettering,
  numerals, logos, marks and dials are explicitly forbidden. Every visible
  surface is plain unmarked metal, weathered paint or bare concrete.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-moat-test-hero-20260927.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "economic-moat-test-ai-durability-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
SEED = os.environ.get("SEED")  # optional fixed seed for reproducible re-rolls
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
# optional candidate override — writes to a scratch path instead of the real target
CAND = os.environ.get("CAND")
if CAND:
    OUTPUT = CAND
    BACKUP = CAND
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene contains no legible lettering of any kind: no text, no "
    "letters, no words, no numbers, no digits, no numerals, no Roman numerals, "
    "no ship name on the hull, no vessel name, no boat name, no port of "
    "registry line, no IMO number, no registration number, no official number, "
    "no hull identification, no draught marks, no depth markings, no painted "
    "numbers on the ship, no tonnage marks, no load lines, no painted stripes "
    "of measurement, no container markings, no container serial codes, no "
    "container prefixes, no shipping-line names, no logos on containers, no "
    "flags with emblems, no pennants with writing, no funnels with lettering, "
    "no name boards, no bridge nameplates, no lifebuoys with any printing, no "
    "life rings with lettering, no safety placards, no warning signs, no "
    "noticeboards, no signage on the lock infrastructure, no lock signage, no "
    "gate numbering, no bollard numbering, no painted arrows or route markers, "
    "no depth gauges, no tide gauges, no water-level scales, no dials, no "
    "gauges, no meters, no instruments with readable faces, no clocks with "
    "numerals, no control panels with labelled buttons, no signs on posts, no "
    "high-visibility clothing with any printing or logo, no hard-hats with "
    "writing, no crew uniforms with embroidered names, no clothing logos, no "
    "brand names, no company names, no trademarks, no watermarks, no "
    "signatures, no captions, no graffiti, no stencilled marks of any kind, no "
    "barcodes, no QR codes, no license plates, no paper, no documents, no "
    "charts, no maps, no screens, no UI, no user interface, no software "
    "windows, no toolbars, no icons, no dashboard, no holograms, no projected "
    "data. Every surface is plain and unmarked: the ship's steel is bare "
    "weathered metal streaked with rust and salt bloom, the superstructure is "
    "plain painted steel with nothing written on it, the concrete lock walls "
    "are plain poured and stained concrete, the bollards are plain worn "
    "cast-iron, the mooring lines are plain twisted rope with no colour-coded "
    "tags, and the painted surfaces are faded and patchy but entirely blank. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit graphics, no network diagram, no word clouds, no "
    "futuristic HUD, no hologram, no overlay elements, no augmented-reality "
    "graphics, no data center, no server room, no server racks, no server "
    "aisles, no cable-run composition, no GPU hardware, no semiconductor "
    "cleanroom, no silicon wafer, no laboratory, no trading floor, no office, "
    "no desk, no spaceship, no space, no satellites."
)

PROMPTS = {
    # 1 — wide documentary frame from the quayside along the lock chamber.
    "1": (
        "Photo-realistic editorial press photograph, a genuine documentary "
        "news picture shot on a 35mm lens at f/2.8 on a full-frame camera from "
        "the quayside of a large ship canal lock at golden hour, low warm "
        "sunlight raking across the scene. The frame looks along the lock "
        "chamber: a big grey coastal cargo vessel sits held inside the "
        "chamber, its long hull and plain superstructure filling the left two "
        "thirds of the image and towering well above the quay, bare "
        "rust-streaked steel with salt bloom and no markings of any kind on "
        "its flanks. In front of the camera the massive concrete lock wall "
        "runs diagonally from the bottom-right corner up toward the vessel in "
        "the mid-ground, weathered and stained, with its plain stone coping "
        "edge catching the low sun. Along that wall in the mid-ground sit two "
        "heavy cast-iron mooring bollards, plain and worn, and beyond them a "
        "steel lock gate structure closes the chamber with plain riveted "
        "panels and a flat walkway across its top. The water inside the "
        "chamber is almost still, a dark green-brown surface reflecting a "
        "smear of warm sky and the dark bulk of the hull. In the right "
        "foreground a plain rusty mooring line lies coiled loosely on the wet "
        "concrete. Low sun behind the camera casts long raking shadows across "
        "the quay and lights the rivets and rust of the hull edge warmly; the "
        "sky beyond the lock is a pale washed dawn sky. Honest available-light "
        "editorial exposure, deep but gentle shadows, damp patches and drip "
        "stains on the concrete, faint scum line on the chamber wall, a few "
        "loose flecks of rust on the water. Moderate depth of field — the "
        "near concrete wall and bollards crisp, the far end of the vessel "
        "softening into creamy haze. Real optical lens blur, natural camera "
        "noise, clearly visible fine film grain, subtle optical vignette, mild "
        "chromatic aberration on high-contrast edges, slightly off-level "
        "hand-held framing with the vessel placed off centre, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — tighter three-quarter crop from a deckhand's viewpoint at the waterline.
    "2": (
        "A real photograph taken on location at a ship canal lock, not a "
        "render and not computer generated: a tighter three-quarter crop shot "
        "on an 85mm lens at f/2 from low on the quay at the waterline, as a "
        "deckhand would see it. The rust-streaked steel hull of a large cargo "
        "vessel rises close and towering right across the left and centre of "
        "the frame, its plating streaked with orange rust runs and dried salt, "
        "seams and rivet lines and weeping drainage stains all over it and "
        "absolutely no lettering, no name and no painted marks anywhere. In "
        "the sharp right foreground a single heavy cast-iron mooring bollard "
        "stands worn and rounded on the concrete edge, with a thick twisted "
        "mooring line lashed around it and stretching taut up and out of frame "
        "toward the ship. Behind the hull, across the chamber, the heavy "
        "riveted steel structure of a closed lock gate stands with its plain "
        "panels and horizontal beams, wet and dark. The water of the chamber "
        "lies between, flat and almost still, a dark olive-brown surface with "
        "a soft warm reflection of the sky and the hull, a few drifting "
        "flecks and a faint ripple near the concrete. Low golden-hour sun "
        "comes from behind the camera and grazes the bollard and the rope, "
        "picking out the fibres of the line, the pitted iron and every flake "
        "of rust on the hull, while the lock gate behind falls into cool "
        "shadow. Honest available-light editorial exposure, deep but gentle "
        "shadows, damp concrete, real texture everywhere. Very shallow depth "
        "of field — the bollard, the rope and the nearest hull plating crisp, "
        "the gate and the far water already reduced to soft blur. Real optical "
        "blur, natural camera noise, visible fine film grain, subtle lens "
        "vignette, slightly off-centre hand-held framing, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — high angle looking down into the lock chamber.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 from a high vantage point on "
        "the lock side, looking down at roughly forty-five degrees into the "
        "chamber of a large ship canal lock in low golden-hour light. Below "
        "the camera a long grey cargo vessel fills the narrow chamber almost "
        "wall to wall, its plain deck and hatch covers and its bare "
        "rust-streaked hull running diagonally across the frame from the "
        "lower-left to the upper-right, with nothing painted, written or "
        "marked on any surface of it, no name and no numbers. On either side "
        "of the hull the two massive concrete lock walls rise, plain and "
        "stained and streaked with old drip marks, with their worn stone "
        "coping and a narrow wet walkway running along the top of each, and a "
        "couple of plain cast-iron bollards and a coiled mooring line on the "
        "left walkway. The chamber water between wall and hull is flat and "
        "dark green-brown, holding a soft warm reflection of the sky, with "
        "slow small ripples and a faint band of foam near the hull. At the far "
        "end of the chamber the closed steel lock gate spans the gap, plain "
        "riveted panels with no markings, and beyond it the canal continues "
        "away toward a hazy low horizon under a pale washed dawn sky. Long "
        "shadows rake across the concrete from the low sun, honest "
        "available-light editorial exposure, wet patches and algae staining "
        "along the waterline on the walls, real grime and texture everywhere. "
        "Moderate depth of field with the near wall and deck crisp and the far "
        "gate softening into creamy haze; real optical blur, natural camera "
        "noise, visible fine film grain, subtle lens vignette, slightly "
        "off-kilter hand-held high framing, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if SEED:
        args["seed"] = int(SEED)
        print(f"  SEED={SEED}")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments=args,
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
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )


if __name__ == "__main__":
    main()
