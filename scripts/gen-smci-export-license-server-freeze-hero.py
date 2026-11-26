#!/usr/bin/env python3
"""Hero for smci-export-license-server-freeze-2026 (fal flux/schnell) — LOADING DOCK.

Subject: Super Micro (SMCI) and the new US AI-server export licence freeze —
hardware manufactured, paid for, and now stuck waiting on export paperwork.

Scene: a FREIGHT LOADING DOCK at an electronics manufacturing plant at dusk. Two
or three shrink-wrapped, palletized server racks on wooden pallets on the concrete
dock, a forklift partly in frame, an open roll-up door with daylight behind it, a
worker in a hi-vis vest and hard hat holding a clipboard with the paperwork turned
away from camera.

Hard negatives: no data-centre hallway, no aisle of server racks, no neon, no
glowing lines, no digital/abstract art, no geometric patterns, no text/logos.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-smci-export-license-server-freeze-hero.py
"""
import os
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "smci-export-license-server-freeze-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1").strip()
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
MAX_BYTES = 400_000


def load_fal_key():
    for path in ("/home/chino/hermes-workspace/studio-api/.env",
                 "/home/chino/video_output/.fal_real"):
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                for line in f:
                    s = line.strip()
                    if s.startswith("FAL_KEY="):
                        key = s.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            os.environ["FAL_KEY"] = key
                            return key
                    elif path.endswith(".fal_real") and s and "|" not in s:
                        os.environ["FAL_KEY"] = s
                        return s
        except OSError:
            continue
    return os.environ.get("FAL_KEY")


NO_TEXT = (
    "Absolutely no legible writing anywhere: no text, no words, no letters, no numbers, no digits, "
    "no serial plates, no labels, no decals, no signage, no brand marks, no company logos, no watermarks. "
    "Any clipboard, form, document, placard, pallet tag or signage in the frame is turned away from the "
    "camera, flipped to its blank reverse, or thrown fully out of focus, so nothing is readable. "
    "No illustration, no digital art, no abstract art, no 3D render, no CGI, no video-game look, "
    "no neon, no glowing lines, no light trails, no geometric patterns, no HUD graphics."
)

PHOTO = (
    "Real lens, real sensor: natural motion blur where hands move, uneven dust and scuffs on the "
    "concrete, creased stretch-wrap plastic catching a highlight, cracked and dirty paint on the dock "
    "edge, clutter that no art director arranged, soft highlight rolloff, visible photographic grain, "
    "no computer-render smoothness, no plastic-looking surfaces, no impossibly clean geometry."
)

NO_DATACENTER = (
    "This is an outdoor industrial freight dock, not a data centre and not an assembly line: no long "
    "hallway, no corridor, no aisle lined with server racks, no cold-aisle blue lighting, no glass-walled "
    "machine room, no conveyor line of technicians. The setting is the exterior concrete loading bay of "
    "an electronics plant with dock bumpers, pallets and a roll-up door."
)

PROMPTS = {
    # A — wide: pallets waiting on the dock, forklift to the side, open door
    "1": (
        "Professional editorial stock photograph, shot on a full-frame DSLR with a 35mm lens at f/2.8, "
        "of a freight loading dock at an electronics manufacturing plant at dusk. Three shrink-wrapped, "
        "palletized server racks stand on wooden pallets on the stained concrete apron, the clear "
        "stretch-wrap reflecting the last flat daylight, aluminium rack edges just visible through the "
        "plastic film. A forklift sits partly in frame at the left edge, its mast cropped by the border. "
        "Behind them a big roll-up door is open onto the dim plant interior with pale daylight spilling "
        "out across the floor, dock bumpers and a scuffed steel edge plate in the foreground. Overcast "
        "blue-hour sky above the roofline, sodium work lamps just starting to glow along the canopy. "
        "Shallow depth of field with the nearest pallet tack-sharp, muted industrial palette of grey "
        "concrete, rusty orange wrap and cold dusk blue, honest grime, mild sensor noise, subtle film "
        "grain. Photorealistic, extremely high detail, candid industrial photojournalism, 16:9 landscape "
        "composition. " + NO_DATACENTER + " " + PHOTO + " " + NO_TEXT
    ),
    # B — worker with clipboard and hi-vis vest in the mid-ground
    "2": (
        "Candid press photograph taken on a real camera, 50mm lens wide open at f/2, harsh mixed dusk "
        "light with visible sensor noise: a warehouse worker in a scuffed high-visibility yellow vest "
        "and a dusty white hard hat stands on a stained concrete freight dock at dusk, holding a "
        "clipboard at chest height with the paperwork turned away from the lens, its back blank, while "
        "he looks toward two shrink-wrapped palletized server racks waiting beside a half-raised "
        "roll-up door. The pallets sit on splintered wooden bases, cloudy stretch-wrap creased and "
        "reflective over brushed aluminium cabinet frames, strapping tape hanging loose; a forklift "
        "sits out of focus behind them, grey daylight bleeding past the door frame and rimming the "
        "worker's shoulder and the brim of his helmet. Foreground concrete is wet in patches with tyre "
        "scuffs, a coil of plastic strapping and a crushed cardboard box dropped on the ground, dock "
        "bumper scuffed black. Handheld framing slightly off-level, focus falling off fast behind the "
        "worker's hands, colour natural and unbalanced rather than graded, film-like grain across the "
        "shadows, tiny blown highlights on the plastic film. This must look like it was shot by a "
        "photographer standing on the dock, not made by a computer: expect imperfect edges, dust, "
        "fingerprints, uneven exposure and no clean digital sheen. Photorealistic, high detail, "
        "16:9 landscape composition. " + NO_DATACENTER + " " + PHOTO + " " + NO_TEXT
    ),
    # C — closer, low angle on the shrink-wrapped racks at the dock edge
    "3": (
        "Authentic editorial press photograph, 35mm lens at f/4, overcast dusk outside an electronics "
        "plant's freight dock. In the mid-ground three server cabinets stand on bare wooden pallets, "
        "wrapped in dull, dusty, heavily creased stretch-wrap that has lost its shine — the plastic is "
        "matted with grit and finger marks, sagging between the cabinet corners, strapping tape dulled "
        "and frayed. A worker in a high-visibility yellow vest and white hard hat stands with his back "
        "half turned to the lens, face not visible, head tilted down as he holds a clipboard low against "
        "his body with the paper side toward himself so only the blank grey back of the board shows. "
        "Behind the pallets a roll-up steel door stands half open with flat grey daylight beyond, and "
        "the rear corner of a forklift is cropped by the right edge of the frame, thrown far out of "
        "focus. Bare concrete apron with dried salt streaks, oil stains, a dead leaf, and a dock bumper "
        "scuffed to black rubber in the foreground; exposed steel canopy overhead cutting a hard "
        "diagonal shadow line across the pallets. Underexposed by a third of a stop, natural "
        "unmanipulated colour, matte surfaces throughout, real optical falloff at the corners, fine "
        "even film grain, gentle highlight bloom on the daylight through the door. Nothing in the frame "
        "is glossy, polished or clean. No cardboard boxes anywhere in the frame. Photorealistic, high "
        "detail, 16:9 landscape composition. " + NO_DATACENTER + " " + PHOTO + " " + NO_TEXT
    ),
}


def main():
    if ATTEMPT not in PROMPTS:
        raise SystemExit(f"ERROR: ATTEMPT must be one of {sorted(PROMPTS)}")
    key = load_fal_key()
    if not key:
        raise SystemExit("ERROR: FAL_KEY not found")

    import fal_client

    args = {
        "prompt": PROMPTS[ATTEMPT],
        "image_size": "landscape_16_9",
        "num_inference_steps": 4,
        "num_images": 1,
        "enable_safety_checker": True,
    }
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)

    image_url = None
    if isinstance(result, dict):
        imgs = result.get("images") or []
        if imgs:
            image_url = imgs[0].get("url")
    if not image_url:
        raise SystemExit(f"ERROR: no image URL in result: {str(result)[:300]}")
    print("Image URL:", image_url)

    r = requests.get(image_url, timeout=180)
    r.raise_for_status()

    tmp = f"/tmp/smci-export-hero-raw-{ATTEMPT}.jpg"
    with open(tmp, "wb") as f:
        f.write(r.content)

    img = Image.open(tmp).convert("RGB")
    # center-crop to 16:9, then resize to 1920x1080
    w, h = img.size
    target = 1920 / 1080
    if w / h > target:
        nw = int(h * target)
        img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w / target)
        img = img.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    img = img.resize((1920, 1080), Image.LANCZOS)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76):
        img.save(OUTPUT, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(OUTPUT)
        if size <= MAX_BYTES:
            break
    print(f"Saved: {OUTPUT} {img.size} q={q} bytes={size}")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=q, optimize=True, progressive=True)
    print(f"Backup: {BACKUP} bytes={os.path.getsize(BACKUP)}")


if __name__ == "__main__":
    main()
