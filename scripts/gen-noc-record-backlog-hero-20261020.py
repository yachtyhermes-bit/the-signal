#!/usr/bin/env python3
"""Hero for noc-record-backlog-cash-conversion-2026 (fal flux/schnell).

Subject: Northrop Grumman's record backlog and cash conversion — the story of a
defense prime converting a book of funded orders into delivered aircraft and cash.
Sector: DEFENSE / AEROSPACE MANUFACTURING.

The story lives where the backlog physically sits: on the final-assembly line, in
an airframe that has been sold but not yet delivered. So the picture is the inside
of a large military aircraft final-assembly hangar at night: a single matte-grey
flying-wing stealth bomber airframe (B-21 style — broad blended delta, no tail,
angular faceted surfaces) on its landing gear, partially wrapped in pale
protective film, ringed by plain scaffolding and work platforms, lit by warm pools
from overhead hangar lamps, with a couple of distant coveralled technicians for
scale. Low three-quarter angle so the wing silhouette dominates.

Deliberately DISTINCT from recent heroes on this site:
- NOT a data-centre / server-room / server-aisle / GPU-rack / cable-run shot (banned).
- NOT a semiconductor cleanroom / wafer / lithography hero (AVGO, TSM, MU, MRVL).
- NOT a precision machine shop, NOT a trading floor, NOT a drone, NOT a rocket pad,
  NOT a satellite, NOT an aircraft in flight.
- NOT neon / synthwave / glow / HUD / geometric / digital art / CGI.

Rules: photo-realistic industrial documentary photography ONLY. The airframe is a
classified-platform assembly in progress, so it is entirely plain: no tail numbers,
no roundels, no insignia, no unit markings, no stencils, no safety placards, no
screens, no signage, no letters and no numerals anywhere in the frame.

Generate 1440x810, finalize 1600x900 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-noc-record-backlog-hero-20261020.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get(
    "SLUG", "noc-record-backlog-cash-conversion-2026"
)
ATTEMPT = os.environ.get("ATTEMPT", "3")
SEED = os.environ.get("SEED", "2026102003")  # optional fixed seed for reproducible re-rolls
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
# optional candidate override — writes to a scratch path instead of the real target
CAND = os.environ.get("CAND")
if CAND:
    OUTPUT = CAND
    BACKUP = CAND
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "The entire scene contains no legible lettering of any kind: no text, no "
    "letters, no words, no numbers, no digits, no numerals, no tail number, no "
    "serial numbers, no aircraft registration, no unit codes, no nose numbers, no "
    "painting or stencilled marks on the airframe, no roundels, no insignia, no "
    "national markings, no squadron badges, no stars and bars, no decals, no "
    "stickers, no paper tags, no tie-on labels, no asset tag, no barcodes, no QR "
    "codes, no datamatrix codes, no signage, no safety placards, no warning "
    "labels, no fire-point signs, no bay numbers, no posters, no whiteboards, no "
    "clipboards, no paper, no documents, no drawings, no charts, no screens, no "
    "monitors, no displays, no control panels, no user interface, no UI, no "
    "software windows, no icons, no dashboard, no readouts, no digital counter, "
    "no LED numerals, no ruler graduations, no scale ticks, no measurement "
    "markings, no hanging banners, no flags, no logos, no brand names, no "
    "trademarks, no watermarks, no captions, no signatures, no graffiti, no "
    "stencilling. The airframe skin is plain matte grey composite with nothing "
    "written anywhere on it; the protective film sheeting and the blank panel "
    "covers carry no printing of any kind; the scaffolding, work platforms and "
    "floor are plain unpainted metal and bare concrete. No close-up people, no "
    "visible faces, no identifiable individuals, no hands in the foreground — at "
    "most a couple of tiny distant workers in plain coveralls seen from behind, "
    "far out of focus, purely for scale. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no CGI sheen, no neon, no glowing lines, no "
    "light trails, no synthwave, no geometric patterns, no circuit graphics, no "
    "network diagram, no futuristic HUD, no hologram, no augmented-reality "
    "overlay, no data visualization, no data center, no server room, no server "
    "racks, no trading floor, no office, no desk, no rocket, no launch pad, no "
    "spacecraft, no aircraft in flight, no fighter jet in the sky, no drone, no "
    "radar dish, no antenna array, no satellite, no explosion, no fire, no smoke, "
    "no weapons, no missiles, no bombs, no open bomb bay."
)

REALISM = (
    "This is a real industrial documentary photograph taken on the assembly floor "
    "by an editorial photographer with available light, not a studio setup and not "
    "a rendering: honest uneven exposure with slightly blown highlights where the "
    "hangar lamps pool on the wing's upper skin, real high-ISO sensor noise and "
    "fine film grain, faint chromatic aberration along the sharp panel edges, "
    "subtle vignetting in the corners, scuffed and dust-marked concrete with "
    "faint tyre tracks, a few loose cable runs and small scattered workshop "
    "debris, and a softly imperfect out-of-focus background with real hangar "
    "clutter. Cool neutral grey-blue shadows against warm amber pools of hangar "
    "light, documentary reportage feel, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — low three-quarter, wing silhouette dominating, lamps pooling on the skin.
    "1": (
        "Photo-realistic editorial press photograph, a genuine documentary news "
        "picture shot on a 35mm lens at f/2 on a full-frame camera from a low "
        "three-quarter angle inside a vast military aircraft final-assembly hangar "
        "late at night. Dominating the frame, filling the centre and sweeping "
        "diagonally from the near lower right toward the far upper left, is a "
        "single large matte-grey flying-wing stealth bomber airframe: one broad "
        "blended delta wing with no tail, no vertical surfaces and no separate "
        "fuselage, its angular faceted upper skin built from large flat grey "
        "panels with crisp chamfered edges, shallow saw-tooth trailing edges and "
        "softly rounded leading edges. The aircraft sits on its own heavy dark "
        "landing gear on the smooth sealed concrete of the hangar floor, the long "
        "wing silhouette stretching wide across the composition and dwarfing "
        "everything around it. Loose sections of pale translucent protective film "
        "sheeting are draped and taped over parts of the airframe, wrinkling in "
        "the light, and a few blank flat grey protective covers are fitted over "
        "openings, all completely plain and unmarked. Simple galvanised steel "
        "scaffolding towers and plain wheeled work platforms stand alongside the "
        "wing in the middle distance, thin legs and flat decks, casting long soft "
        "shadows across the floor, with a coil of heavy cable and a low work "
        "lamp on the concrete. High above, rows of industrial hangar lamps deep in "
        "the roof trusses throw broad soft pools of warm light down onto the "
        "aircraft's upper surface, so the near wing glows warm grey and the "
        "shallow panel steps catch thin highlights, while the underside of the "
        "wing and the floor beneath fall into deep cool shadow. Far behind, the "
        "hangar's huge closed sliding doors read as a flat dark wall in soft "
        "blur. In the middle distance two technicians in plain pale grey coveralls "
        "stand with their backs to the camera, small and out of focus beside the "
        "wing, giving scale. Shallow depth of field — the near wing edge, the "
        "landing gear and the concrete sharp, the far wing tip and the doors "
        "dissolving into creamy haze. Real optical lens blur, natural camera "
        "noise, clearly visible fine film grain, subtle optical vignette, slightly "
        "off-level hand-held framing with the wing placed just off centre, no "
        "perfect symmetry, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + REALISM + " " + NO_TEXT
    ),
    # 2 — wider, further back, scaffolding lattice framing the airframe.
    "2": (
        "A real photograph taken on location inside a working military aircraft "
        "final-assembly hangar, not a render and not computer generated: a wide "
        "three-quarter shot on a 28mm lens at f/2.8 from standing height at the "
        "edge of the assembly floor, looking across at a large flying-wing "
        "stealth bomber airframe under construction at night. The camera is "
        "squarely inside the building: no sky, no daylight and no outdoors are "
        "visible anywhere in the frame — the top of the picture is filled by the "
        "hangar's dark roof structure and its lamps, the sides by the hangar's "
        "interior walls and columns, and the airframe stands on an indoor "
        "assembly floor littered with cable reels, trestles and offcuts of "
        "sheeting. The airframe is a work in progress, not a finished aircraft: a "
        "broad matte-grey blended delta wing with absolutely no vertical tail "
        "fin, no rudder, no cockpit canopy, no nose cone and no fuselage tube — "
        "just one continuous flat lifting body with a clean thin trailing edge, "
        "its unfinished skin a patchwork of large flat grey composite panels, "
        "dusty and grubby with handprints and taped seams, sitting low on its "
        "landing gear on bare sealed concrete and reaching from the left third "
        "of the frame across to the right edge, "
        "the far wing tip fading into shadow. Pale translucent protective film is "
        "part-wrapped over the centre section and one wing root, taped at the "
        "edges and creased where it has been pulled tight, and blank flat grey "
        "panel covers blank off two openings along the leading edge. In the near "
        "foreground on the left, slightly out of focus, a plain steel scaffolding "
        "tower rises out of frame, its vertical tubes and couplers catching a "
        "little light, and a low wheeled work platform with a bare plywood deck "
        "stands beside it; a second platform sits further back along the wing. "
        "The hangar is enormous and mostly dark: high roof trusses disappear into "
        "blackness overhead, and a sparse row of industrial lamps throws warm "
        "cones of light down onto the aircraft, leaving the aisles and the deep "
        "background in cool blue-grey shadow. The huge closed hangar doors at the "
        "back are a flat darkness with a thin seam of light along the floor. Two "
        "distant workers in plain coveralls, seen from behind and heavily out of "
        "focus, walk along the far side of the wing for scale. Very shallow depth "
        "of field — the near scaffolding tube and the wing's leading edge sharp, "
        "the aircraft's far half and the hangar already reduced to soft blur. Real "
        "optical blur, natural camera noise, visible fine film grain, subtle lens "
        "vignette, slightly off-centre hand-held framing, no CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + REALISM + " " + NO_TEXT
    ),
    # 3 — close along the wing upper surface, hangar lights pooling, technicians
    # tiny at the far end for scale.
    "3": (
        "Photo-realistic 35mm film scan, a real documentary press photograph taken "
        "on location, not a render and not computer generated, shot on a 35mm "
        "single-reflex camera with 400-speed colour negative film, hand-held, from "
        "a low angle just above the hangar floor, looking along the upper surface "
        "of a flying-wing stealth bomber airframe in final assembly at night. The "
        "camera is inside the hangar: black roof trusses and the undersides of "
        "lamps crowd the top of the frame, hangar columns and a concrete wall "
        "stand at the sides, and no sky or daylight appears anywhere. The "
        "airframe has no vertical tail fin at all, no rudder, no canopy, no nose "
        "cone and no fuselage tube — one continuous flat blended delta lifting "
        "body, its upper skin a single uniform shade of flat matte light-grey "
        "composite, dry and slightly dusty, with faint mottling, small "
        "handling scuffs and a few dull smudges, and thin recessed seam lines "
        "between the panels. The surface is completely bare: there is not a "
        "single painted mark, patch, black shape, stripe, badge, roundel or "
        "stencil on the whole upper wing, only the even grey skin and its seams. "
        "It is dead matte and does not reflect: the lamps above do not appear as "
        "sharp bright mirrors on the skin, only as broad soft areas of a slightly "
        "warmer grey where the light lands, and the panel seams read as fine "
        "darker lines. A sheet of pale translucent protective film is part-peeled "
        "and folded back across the mid wing, creased and taped at the loose "
        "edge, and a blank flat grey cover plate sits flush over one opening "
        "further along. Below the near leading edge, out of focus, the dark bulky "
        "shape of the main landing gear and a heavy tyre rest on the concrete, "
        "with dust and a faint tyre scuff on the floor. Far down the wing at the "
        "middle distance, small and soft, two workers in plain pale grey coveralls "
        "stand with their backs to the camera beside a plain steel work platform, "
        "clearly human and clearly tiny against the span of the aircraft, with "
        "scaffolding uprights breaking the darkness behind them. Very shallow "
        "depth of field — the near leading edge and the lifted corner of the film "
        "crisp, the wing's middle distance already softening, the far end and the "
        "two workers dissolved into soft hazy blur. Real optical lens blur, "
        "natural high-ISO colour noise, clearly visible coarse film grain, a "
        "little dust on the negative, mild halation around the lamps, subtle "
        "optical vignette, slightly off-level hand-held framing with the wing off "
        "centre, no perfect symmetry, no glossy sheen, no mirror reflections, "
        "photorealistic, documentary, 16:9 landscape composition. "
        + REALISM + " " + NO_TEXT
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
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    hermes_env = "/home/chino/.hermes/profiles/yachty/.env"
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if line.strip().startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    return None


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
    """Center-crop to 16:9, then resize to 1600x900."""
    img = img.convert("RGB")
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
