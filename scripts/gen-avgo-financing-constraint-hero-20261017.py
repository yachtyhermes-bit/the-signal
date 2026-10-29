#!/usr/bin/env python3
"""Hero for avgo-financing-constraint-casino-2026 (fal flux/schnell).

Subject: Broadcom (AVGO) — designs custom AI accelerators (XPUs) for a handful of
giant customers; the CEO warned that CAPITAL, not chips, is now the binding
constraint on the AI buildout.

Scene chosen: an extreme macro product-photography shot of a finished custom AI
accelerator package and a 300mm wafer resting on the inspection stage of a
semiconductor cleanroom, lit by the warm amber/yellow cleanroom ambience with the
die surface catching the light.

Deliberately DISTINCT from recent heroes:
- NOT a data-centre / server-rack aisle / server-room corridor (used recently).
- NOT a bunny-suited technician holding a wafer (MU/CXMT hero).
- NOT a studio tray product shot on seamless grey (MSFT Maia 300 hero).

Rules: photo-realistic stock photography ONLY. No text/logos/watermarks, no people,
no neon/synthwave/glow/geometric/abstract/render looks.

Usage: SEED=1234 VARIANT=1 /home/chino/video-venv/bin/python3 scripts/gen-avgo-financing-constraint-hero-20261017.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "avgo-financing-constraint-casino-2026")
SEED = int(os.environ.get("SEED", "20261017"))
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810          # 16:9 generation size
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "Every surface is completely plain and unmarked: no text, no letters, no numbers, "
    "no words, no digits, no codes, no serial numbers, no part numbers, no lot codes, "
    "no barcodes, no QR codes, no datamatrix codes, no silkscreen printing, no "
    "laser-etched characters, no engraved characters, no labels, no stickers, no "
    "plaques, no nameplates, no decals, no stencils or stenciled writing, no markings "
    "of any kind, no logos, no brand names, no signage, no posters, no screens, no "
    "monitors, no displays, no UI, no charts, no ruler graduations, no watermark, no "
    "captions, no signature. The ceramic package, the wafer surface, the carrier and "
    "the stage are entirely bare. "
    "No people, no hands, no faces, no human figures, no silhouettes, no body parts. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI look, no neon, "
    "no glowing lines, no glowing sci-fi lines, no abstract art, no synthwave, no lens "
    "flare, no bokeh lights, no HUD graphics, no overlay graphics. Not a server room, "
    "not a data-centre aisle, not a server rack, not an interior corridor."
)

VARIANT = os.environ.get("VARIANT", "1")

REALISM = (
    "This is a real press photograph taken inside a working factory by an editorial "
    "photographer with available light, not a studio setup and not a rendering: uneven "
    "exposure with slightly blown highlights on the metal, real high-ISO sensor noise and "
    "fine film grain, faint chromatic aberration on the sharp edges, slight vignetting in "
    "the corners, a few specks of dust on the metal, tiny scratches and machining marks, "
    "and a softly imperfect out-of-focus background with visible real-world clutter. "
    "Muted natural colour, documentary reportage feel, 16:9 landscape aspect ratio. "
)

STAGE = (
    "Professional stock photograph, close-up shot on a 50mm lens at a natural low "
    "three-quarter viewing angle, of an open wafer carrier and a finished custom AI "
    "accelerator chip package sitting on a stainless-steel inspection bench inside a "
    "semiconductor cleanroom. The subject group sits in the centre of the frame and fills "
    "roughly half the frame width, with generous space around it for cropping. "
    "Warm amber and yellow-orange cleanroom lighting, the soft yellow-tinted light of a "
    "photolithography area, raking across the subject so the silicon surface catches it "
    "and shows a faint iridescent rainbow diffraction sheen. "
)

STAGE_WIDE = (
    "Professional stock photograph of a semiconductor cleanroom interior, shot on a 35mm "
    "lens from a natural standing eye level, centred on a stainless-steel wafer inspection "
    "station where an open wafer carrier holds a stack of 300mm silicon wafers and a "
    "finished custom AI accelerator chip package sits on the bench beside it. The "
    "inspection station fills roughly the centre half of the frame, with cleanroom wall "
    "panels, a softly blurred tool housing and empty floor space around it leaving "
    "generous room for cropping. The whole room is bathed in warm amber and yellow-orange "
    "light, the yellow-tinted lighting of a photolithography bay, with the wafers' mirror "
    "faces catching soft iridescent bands of green, violet and gold. "
)

VARIANTS = {
    "1": STAGE + (
        "The subject is a large square processor package about the size of a coffee mug "
        "footprint: a matte ceramic and organic substrate body with a thin metallised lid, "
        "a dense perimeter fence of tiny gold bond pads and fine wire bonds catching small "
        "specular highlights, and a large central silicon die visible through the lid "
        "opening, its microscopic transistor and interconnect detail just resolving as "
        "very fine texture rather than legible shapes. Beside it, slightly out of focus in "
        "the middle distance, the curved edge of a 300mm silicon wafer rests in an open "
        "wafer carrier, its mirror-polished surface reflecting the warm amber light in "
        "soft bands. Brushed steel stage surface with a few fine handling scratches and a "
        "faint dust-free sheen; plain brushed metal framework around the frame edges "
        "softly blurred. " + REALISM + NO_TEXT
    ),
    "2": STAGE + (
        "The subject is a 300mm silicon wafer standing almost upright in an open wafer "
        "carrier slot on the inspection stage, seen at a raking low angle so the round "
        "silhouette of the wafer fills the centre of the frame, its mirror-polished face "
        "covered in the dense fine grid of identical die rectangles catching the amber "
        "light as soft iridescent bands of green, violet and gold. The wafer's polished "
        "bevel edge glints along its curve. A finished ceramic chip package rests on the "
        "brushed steel stage in the near foreground, slightly out of focus, showing its "
        "substrate, gold bond pads and a dark polished lid. Plain machined metal carrier "
        "with soft rounded edges, no markings. " + REALISM + NO_TEXT
    ),
    "3": STAGE + (
        "The subject is a finished custom AI accelerator package standing on its ceramic "
        "substrate on the inspection stage, photographed almost edge-on at table height: "
        "a thick square package with a machined metal stiffener ring, a dark polished lid "
        "with a faint iridescent sheen, and rows of tiny gold contact pads along the "
        "visible substrate edge. Behind and above it, out of focus, the soft amber glow of "
        "cleanroom ceiling light panels and the blurred edge of a wafer handling tool. The "
        "brushed steel stage reflects a soft warm pool of light beneath the package. "
        + REALISM + NO_TEXT
    ),
    "4": STAGE_WIDE + (
        "The open carrier is a plain black machined plastic cassette with soft rounded "
        "edges, its wafers standing in neat parallel slots and their mirror faces layered "
        "with pale reflected light. The chip package beside it is a thick square substrate "
        "with a dark polished lid and a fine perimeter row of gold contact pads. The bench "
        "is plain brushed stainless steel; the cleanroom ceiling above shows flat pale "
        "light panels and the blurred top edge of a sealed tool enclosure. " + REALISM + NO_TEXT
    ),
    "5": STAGE + (
        "The subject is a single 300mm silicon wafer lying flat and slightly tilted on the "
        "brushed steel inspection bench, photographed close up at a low angle so the round "
        "disc curves across the centre of the frame, its mirror-polished face covered in "
        "the dense fine repeated grid of identical die rectangles that catch the amber "
        "light as soft iridescent bands of green, violet and gold. Beside it on the bench, "
        "partly out of focus, a black wafer carrier cassette is open on its side. A narrow "
        "band of the bench's brushed metal shows fine machining scratches. " + REALISM + NO_TEXT
    ),
    "6": (
        "Professional stock photograph, medium shot on a 50mm lens at a natural low "
        "three-quarter viewing angle, inside a semiconductor cleanroom bathed in warm "
        "amber and yellow-orange photolithography-bay light. In the dead centre of the "
        "frame, an open black wafer carrier cassette holds a stack of 300mm silicon wafers "
        "at a slight angle, their mirror-polished faces layered with soft iridescent "
        "reflections of green, violet and gold from the warm overhead light, and a "
        "finished square custom AI accelerator chip package with a brushed metal lid and a "
        "gold contact-pad perimeter sits on the plain brushed stainless-steel inspection "
        "bench directly in front of it. The two objects occupy only the middle third of "
        "the image: they are completely inside the frame with a wide even margin of empty "
        "brushed metal bench and softly blurred cleanroom wall panel all around them on "
        "the left, right, top and bottom. The equipment behind is far out of focus. "
        "Symmetrical centred composition, wide breathing room, nothing cropped at the "
        "edges. " + REALISM + NO_TEXT
    ),
}

PROMPT = VARIANTS[VARIANT]


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


def main():
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating hero for {SLUG} via fal-ai/flux/schnell (seed={SEED}, variant={VARIANT})...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
        "prompt": PROMPT,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
        "seed": SEED,
    })
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    img = Image.open(OUTPUT).convert("RGB")
    print(f"Downloaded: {OUTPUT} size={img.size} bytes={len(r.content)}")

    if img.size != (FINAL_W, FINAL_H):
        img = img.resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT} dimensions={img.size} bytes={size}")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Copied to {BACKUP} bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
