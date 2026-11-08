#!/usr/bin/env python3
"""Generate hero for quantum-error-correction-explainer-2026 (fal flux/schnell).

Subject: how one logical qubit is encoded across many physical qubits inside a
dilution refrigerator held at near-absolute-zero temperatures.

MANDATORY SCENE: a quantum computing laboratory. Centre of frame: a tall
cylindrical dilution refrigerator cryostat — stacked circular gold-plated
copper plates, thin vertical rods, dense silver coax cabling looping between
stages — suspended inside an aluminium frame. A technician in a white lab coat
and blue nitrile gloves (seen from behind/side, unidentifiable, face not the
subject) adjusts a cable bundle at the base. Cold dim laboratory, out-of-focus
instrument racks and a plain wall behind.

Deliberately NOT: data center hallway / server aisle / rows of racks, neon or
glowing lines, holograms, abstract or digital art, charts on screens, text.

Rules:
- PHOTO-REALISTIC editorial stock photograph ONLY.
- TEXT-FREE: no legible letters/numbers/logos/brand names anywhere. Any
  instrument screen or panel in frame is dark and unreadable.
- Generate 1440x810, finalize 1536x864, hard cap 400KB.
- Hard cap: at most 3 FAL generations (ATTEMPT 1..3).

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
  scripts/gen-quantum-error-correction-hero-20261108.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "quantum-error-correction-explainer-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The image contains no readable text anywhere: no letters, no words, no "
    "numbers, no digits, no legible printed characters, no logos, no brand "
    "names, no manufacturer marks, no model plates, no engraved lettering, no "
    "stickers with writing, no serial labels, no signage, no wall signs, no "
    "watermark, no caption, no signature. Every instrument screen, monitor, "
    "panel and readout in the frame is completely dark or entirely blank and "
    "unreadable, showing no glyphs and no characters of any kind. Every metal "
    "surface, plate and plate edge in the frame is plain and unmarked. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no neon, "
    "no glowing lines, no glowing coils, no laser beams, no synthwave, no "
    "futuristic HUD overlays, no holograms, no augmented reality graphics, no "
    "abstract data visualisation, no charts on screens, no geometric light "
    "effects, no light painting, no data center hallway, no server aisle, no "
    "rows of server racks, no rows of blinking status LEDs."
)

PROMPTS = {
    # 1 — primary: dilution fridge centre frame, gloved technician at the base
    "1": (
        "Photo-realistic professional editorial stock photograph, landscape "
        "orientation, shot inside a real quantum computing laboratory. "
        "Dominating the centre of the frame, from just above the floor to "
        "near the top of the image, stands a large dilution refrigerator: a "
        "tall vertical cylindrical cryostat built as a stack of wide circular "
        "gold-plated copper plates, each disc slightly smaller than the one "
        "above it, spaced a hand's width apart down a central column. Between "
        "the plates run thin polished vertical rods and a dense curtain of "
        "silver semi-rigid coax cables, each cable bending in a smooth loop "
        "from a connector on one plate down to the plate below, dozens of them "
        "layered and crossing, catching small specular highlights along their "
        "smooth silver jackets. Fine toroidal copper coils and small machined "
        "brass fittings sit at some of the stages. The whole assembly hangs "
        "suspended inside a plain matte aluminium frame of square extrusion, "
        "the frame's vertical posts running up both sides of the frame, and "
        "the cryostat's lower stages disappear into a grey cylindrical "
        "vacuum can near the bottom. At the base of the apparatus, slightly "
        "right of centre, a technician is at work: a person in a crisp white "
        "cotton lab coat and blue nitrile gloves, seen from behind and "
        "side-on in three-quarter profile, only the back of the head, the "
        "shoulder and the forearms visible, the face turned away from the "
        "camera and completely unidentifiable. The gloved hands are gently "
        "guiding and dressing a bundle of silver cables into a connector at "
        "the lowest plate. Behind them the laboratory falls away into "
        "cold dim shadow: out-of-focus instrument racks, a bench and a plain "
        "painted concrete wall, everything soft and low contrast, no windows "
        "in frame. The light is cool muted fluorescent mixed with a faint "
        "grey window spill from off-frame left, falling softly down the gold "
        "plates and picking out the silver cables, deep shadow between the "
        "stages, restrained steel and gold and warm brass palette on a cold "
        "grey-green background. Shot on a full-frame camera with a 50mm lens "
        "at f/2.0, shallow depth of field — the near gold plates and the "
        "gloved hands sharp, the far side of the cryostat and the room "
        "behind melting into smooth bokeh, real optical blur, natural fine "
        "sensor grain, honest contrast, unretouched documentary realism, "
        "slightly imperfect handheld framing, no glossy CGI sheen. 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    # 2 — human scale forward: technician large in the left foreground, fridge behind
    "2": (
        "Unposed documentary photograph taken by a colleague with a DSLR in a "
        "working physics laboratory, landscape orientation, available light "
        "only, the kind of ordinary imperfect frame you get when someone "
        "photographs their co-worker mid-task. In the left third of the "
        "frame, close to the camera and cut off at the thigh, a researcher "
        "stands with their back to the lens: a real person in a slightly "
        "creased white cotton lab coat that hangs open over a plain grey "
        "shirt, the coat's collar bent, one sleeve pushed up to the elbow, "
        "fine creases and a faint ballpoint mark at the pocket. Both hands "
        "wear snug blue nitrile gloves, the fingers clearly shaped through "
        "the rubber, and they are holding and guiding a fat bundle of "
        "silver-jacketed coaxial cables into a connector at waist height. "
        "Only the back of their head with short dark hair and the line of "
        "one cheek are visible — the face is turned completely away from "
        "the camera and cannot be identified. Behind them and filling the "
        "centre and right of the frame, a dilution refrigerator stands on "
        "the floor: a tall cylindrical cryostat about two and a half metres "
        "high, a vertical stack of wide flat circular gold-plated copper "
        "discs of decreasing diameter descending down a central column, thin "
        "polished stainless rods between the discs, and a dense tangled "
        "curtain of dozens of silver semi-rigid coax cables looping in "
        "uneven arcs from connectors at the edge of each plate down to the "
        "plate below, the cables sagging slightly under their own weight, "
        "some bundled with small white cable ties, the whole assembly "
        "hanging inside a plain scuffed matte aluminium frame of square "
        "extrusion bolted at the joints. The lowest stage disappears into a "
        "dull brushed steel vacuum can. The gold plates are visibly worn: "
        "fingermarks, small tarnish patches and dull smudged areas where "
        "gloves have handled them, a few scratches, dust settled on the "
        "upper surfaces, none of it uniformly mirror-shiny. The room behind "
        "is a real lab, cold and dim and slightly untidy — a grey painted "
        "concrete block wall, a bench cluttered with coiled cables and a "
        "cardboard box, a dark unlit monitor standing blank, an instrument "
        "rack in shadow — all thrown well out of focus. Overhead fluorescent "
        "tubes and one weak grey spill light the scene unevenly, cool and a "
        "little green, hard highlight on the top plate and deep shadow "
        "underneath the discs, the white lab coat blown slightly bright at "
        "the shoulder. Muted desaturated palette of steel grey, dull tarnished "
        "gold and cold white, mixed colour temperature, faint greenish cast "
        "in the shadows. Shot on a full-frame camera with a 35mm lens at "
        "f/2.8 held at chest height, moderate depth of field — the "
        "technician's shoulders and gloves sharp, the far plates and the "
        "room softening, visible grain at high ISO, slight lens vignette, a "
        "touch of chromatic fringing on the bright cable highlights, "
        "slightly tilted handheld framing, unretouched and unstyled, no "
        "glossy CGI sheen, real photographic texture throughout. 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    # 3 — attempt 2 composition hardened: no plaques/nameplates, plain equipment
    "3": (
        "Unposed documentary photograph taken by a colleague with a DSLR in a "
        "working physics laboratory, landscape orientation, available light "
        "only, an ordinary imperfect handheld frame of someone working. In "
        "the left third of the frame, close to the camera and cut off at the "
        "thigh, a researcher stands with their back to the lens: a real "
        "person in a slightly creased white cotton lab coat hanging open over "
        "a plain grey shirt, collar bent, one sleeve pushed up, soft fabric "
        "creases and a faint ink smudge near the pocket, no badge and no "
        "embroidered patch on the coat. Both hands wear snug blue nitrile "
        "gloves, the fingers clearly shaped through the rubber, and they are "
        "holding and guiding a thick bundle of silver-jacketed coaxial "
        "cables into a connector at waist height. Only the back of their head "
        "with short dark hair and the edge of one cheek are visible — the "
        "face is turned fully away from the camera and cannot be identified. "
        "Behind them, filling the centre and right of the frame, stands a "
        "dilution refrigerator: a tall cylindrical cryostat about two and a "
        "half metres high, a vertical stack of wide flat circular "
        "gold-plated copper discs of decreasing diameter descending down a "
        "central column, thin polished stainless rods between the discs, and "
        "a dense tangled curtain of dozens of silver semi-rigid coax cables "
        "looping in uneven arcs from connectors at the rim of each plate "
        "down to the plate below, sagging slightly under their own weight, a "
        "few gathered with small plain cable ties, the whole assembly "
        "hanging inside a scuffed matte aluminium frame of square extrusion "
        "bolted at the joints, the lowest stage sinking into a dull brushed "
        "steel vacuum can. The gold plates are visibly worn — fingermarks, "
        "tarnish patches, dull smudged areas where gloves have handled them, "
        "a few fine scratches, dust settled on the upper surfaces, nothing "
        "uniformly mirror-shiny. The room behind is a cold dim real lab, "
        "slightly untidy: a plain bare grey painted concrete block wall with "
        "nothing mounted on it, a bench with a coil of cable and a plain "
        "cardboard box, and one closed white steel cabinet standing against "
        "the wall — that cabinet's front is entirely blank and smooth, with "
        "no plaque, no nameplate, no sticker, no badge and no marking of any "
        "kind on it, and the whole background is so far out of focus that "
        "its surfaces are only soft shapes of grey and white. Overhead "
        "fluorescent tubes and a weak grey spill light the scene unevenly, "
        "cool and a little green, a hard highlight on the top plate, deep "
        "shadow beneath the discs, the lab coat slightly blown out at the "
        "shoulder. Muted desaturated palette of steel grey, dull tarnished "
        "gold and cold white, mixed colour temperature, faint greenish cast "
        "in the shadows. Shot on a full-frame camera with a 35mm lens at "
        "f/2.8 held at chest height, moderate depth of field — the "
        "technician's shoulders and gloves sharp, the far plates and the "
        "room dissolving, visible high-ISO grain, slight lens vignette, a "
        "hint of chromatic fringing on the bright cable highlights, slightly "
        "tilted handheld framing, unretouched and unstyled, genuinely "
        "photographic, no glossy CGI sheen, no 3D render. 16:9 landscape "
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
