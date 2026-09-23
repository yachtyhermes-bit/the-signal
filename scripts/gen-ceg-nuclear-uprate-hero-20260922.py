#!/usr/bin/env python3
"""Generate hero for ceg-nuclear-uprates-ai-power-premium-2026 (fal flux/schnell).

Subject: Constellation Energy (CEG) — America's largest nuclear fleet owner — and
the new pattern of hyperscalers (Google) paying a premium subscription for extra
megawatts squeezed out of EXISTING reactors via 'uprates': targeted equipment
upgrades to turbines, pumps, motors and cooling systems (Georgia Power's Vogtle
and Hatch). AI data centers need firm, carbon-free power around the clock.

Scene chosen (ATTEMPT=1): INTERIOR OF A NUCLEAR PLANT TURBINE HALL DURING AN
UPGRADE OUTAGE — a colossal low-pressure steam turbine with its casing open and
a massive multi-ton rotor lifted onto a service stand, polished steel turbine
blades catching the light, a technician in a plain hard hat and coveralls
inspecting a blade row at a walkway railing, overhead gantry crane rails, tall
industrial lighting, polished concrete floor, enormous scale and depth.

Why it is visibly different from recent heroes on this site:
- BANNED data-center server halls / server aisles / GPU racks: not present.
- GNRC 9/17 (data-center standby generator yard at dusk): this is indoors, no
  generator enclosures, no dusk sky, no exhaust stacks.
- PWR 9/12 (high-voltage grid / substation): no lattice towers, no transformers,
  no overhead lines — this is a machine hall.
- older CEG 8/23 (nuclear plant at dusk beside a data center): no exterior, no
  cooling towers, no dusk, no data center anywhere in frame.
- Google Finland nuclear (9/13: nuclear plant + cold climate): no snow, no
  boreal forest, no exterior at all.
- NRG 9/18 (demand-response control scene): no control room, no desks, no
  operators at screens — this is the physical machine itself under maintenance.

ATTEMPT=2 alternative: exterior ground-level view of a containment dome and
reactor service building from a plant access road at blue hour, worker on a wet
concrete apron, no data center in frame.
ATTEMPT=3 alternative: reactor refueling-outage scene — open reactor vessel
inside containment with the vessel head lifted clear above it on a crane.
ATTEMPT=4 alternative: exterior outage laydown yard at blue hour with a heavy
mobile crane lifting a slung, wrapped turbine component past a turbine-hall
flank (added during this run — see note above PROMPTS["4"]).

SHIPPED: ATTEMPT=1 (turbine hall), fifth render. Flux/schnell is stochastic and
the first four turbine-hall rolls were scored "render/CGI" by the vision check
(scripts/vision_inspect.py) despite passing the text/scene checks; the fifth
roll passed as an authentic photograph with the correct subject (worker
inspecting a bladed turbine rotor on a platform). Site baseline for that check
is ~4 of 5 shipped heroes passing, so the flag was treated as a real signal.
Variants 2 and 4 also passed as photographs and can be used if a reshoot is
needed without repeating a composition.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: turbine halls and nuclear plants are wall-to-wall with nameplates,
  tag numbers, warning placards and control displays, so all lettering, numbers,
  UI, logos and brand names are explicitly forbidden. Any display in frame is
  dark / switched off / out of focus.
- No tight close-ups of faces (mid-ground or turned-away workers only).
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-ceg-nuclear-uprate-hero-20260922.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ceg-nuclear-uprates-ai-power-premium-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "user interface, no software windows, no dashboards, no machine control "
    "screens showing content, no control panel displays, no digital readouts, "
    "no toolbars, no menus, no icons, no signage, no warning signs, no "
    "placards, no danger notices, no safety stickers, no turbine nameplates, "
    "no equipment labels, no engraved or stamped lettering on the turbine "
    "casing, rotor, blades, pipework or crane, no cabinet labels, no panel "
    "markings, no dial faces with numbers, no gauges with numerals, no dials, "
    "no meters, no charts, no arrows, no crosshairs, no alignment marks, no "
    "lettering on the concrete floor or steel walkways, no railing banners, no "
    "keyboard lettering, no name badges, no lanyards, no hard-hat lettering, "
    "no printed documents, no clipboards with writing, no brand names, no "
    "manufacturer names, no company names, no corporate logos, no trademarks, "
    "no watermarks, no stickers, no barcodes, no QR codes, no datamatrix "
    "codes, no handwritten markings, no graffiti, no license plates, no "
    "legible writing of any kind anywhere in the image. Every display or "
    "control screen in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with "
    "absolutely nothing readable or drawn on it, like an out-of-focus colour "
    "field photograph, not a screen with content. The turbine casing, rotor, "
    "blade rows, bearing pedestals, pipework, valves, gantry crane, walkway "
    "railings and concrete floor are plain and unmarked, and the worker's "
    "coveralls and hard hat are plain unmarked solid colours. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center server room, no server "
    "racks, no server aisles, no cable-run composition, no server lights, no "
    "GPU hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — turbine hall interior, casing open, rotor on a service stand.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 24mm lens at "
        "f/4 on a full-frame camera, inside a nuclear power station's turbine "
        "hall during an upgrade outage. Filling the frame is a colossal "
        "low-pressure steam turbine, its heavy steel outer casing split open "
        "and lifted clear, revealing a massive multi-ton rotor resting on a "
        "purpose-built service stand: long rows of steel turbine " 
        "blades fan out along the rotor in crisp repeating ranks, their "
        "machined flanks catching the light under a fine film of grime, the "
        "curved stators of the lower casing still seated in the machine pit "
        "beneath, bolted flanges and thick bearing pedestals plain and "
        "unmarked. The scale is enormous — the rotor is longer than a bus and "
        "the hall ceiling disappears far above. In the sharp mid-ground, "
        "standing at a steel walkway railing above the rotor and seen mostly "
        "from behind and the side, is a single maintenance technician in "
        "plain dark navy coveralls and a plain white hard hat, one gloved "
        "hand on the railing, head angled down toward the blade row as if "
        "inspecting it, unposed and mid-task, their face not visible. Above "
        "them run the overhead gantry crane rails and a heavy travelling "
        "crane trolley, softened by depth of field. The polished concrete "
        "floor carries subtle reflections, a few plain hand tools and a coil "
        "of cable sit on a low service platform at the right edge, and deep "
        "in the background the far end of the hall dissolves into warm haze "
        "under tall industrial lamp clusters. Warm-neutral industrial "
        "lighting with cool grey daylight spilling from high clerestory "
        "windows, honest shadows pooling in the machine pit. Moderate depth "
        "of field: the near blade rows and the technician crisp, the far hall "
        "melting into creamy bokeh. This is a real, unretouched, hand-held "
        "documentary press photograph taken by a human photojournalist on "
        "assignment — visibly a photograph, never a render: the surfaces are "
        "worn and imperfect, the turbine casing carries scuffed faded paint, "
        "greasy streaks, rust bloom, dust film and hand smudges, the blade "
        "rows have fine grime rather than mirror polish, the concrete floor "
        "is stained and patched, and the light is uneven, mixed in colour "
        "temperature, with hot spots and dull corners. Slightly crooked "
        "handheld framing, a trace of camera shake, visible ISO grain in the "
        "shadows, mild sensor noise, faint chromatic fringing on "
        "high-contrast edges, soft lens flare from the lamp cluster, real "
        "optical lens blur, honest available-light editorial exposure, subtle "
        "lens vignette, no plastic CGI sheen, no glossy render, no video-game "
        "or visualisation look, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, no AI-generated look, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    # 2 — exterior: containment dome + reactor service building at blue hour.
    "2": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 35mm lens at f/5.6 from ground level on a "
        "nuclear power station access road at blue hour. Dominating the right "
        "of frame is the smooth pale-grey concrete containment dome of a "
        "pressurised water reactor, its curved shell rising far above the "
        "camera with faint vertical weathering streaks, and beside it the "
        "blocky mass of a reactor service building with plain windowless "
        "flanks and flat panel doors, also unmarked. In the left mid-ground, "
        "sharp and unposed, a plant worker in plain dark coveralls and a "
        "plain white hard hat walks away from the camera along a wide "
        "concrete apron between painted kerb lines, one hand in a pocket, "
        "their back to the lens, throwing a long soft shadow. Wet asphalt in "
        "the foreground catches weak reflections of the plant's cool white "
        "floodlights and a single warm sodium lamp, and a low steel guard "
        "rail and a plain chain-link fence line the road edge. Above, the sky "
        "is a deep indigo band with the last faint amber afterglow low on the "
        "horizon behind the dome. No other buildings, no cooling towers, no "
        "data center anywhere in frame. Moderate depth of field with the "
        "worker, kerbs and dome base crisp and the far fence softening into "
        "haze, real optical blur, honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, subtle lens vignette, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — refueling outage: open reactor vessel, head lifted on a crane.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 24mm lens at "
        "f/4 inside a reactor containment building during a refuelling "
        "outage. In the centre of the frame the vast cylindrical reactor "
        "vessel stands open, its dark interior visible as a deep recess, and "
        "above it — suspended on a heavy overhead polar crane — hangs the "
        "enormous domed steel reactor vessel head, lifted clear and held in "
        "the air, its thick studded flange ring and massive bolts plain and "
        "unmarked. Thick structural steelwork, shielded platform decks and "
        "rounded concrete containment walls frame the scene, with a curved "
        "steel liner panelled in plain unmarked plates and a heavy plain "
        "chain hoist rigging the suspended head. On a steel grating platform "
        "at mid-height, seen from behind and slightly above in the "
        "mid-ground, two outage workers in plain pale coveralls and plain "
        "white hard hats stand at a railing, one leaning on it looking down "
        "toward the open vessel, neither turning toward the camera and no "
        "faces visible. Cold blue-white work lighting floods down from high "
        "lamps onto the vessel head and the platform, deep shadows fall away "
        "into the containment's lower levels, and the enormous vertical "
        "scale of the space is obvious from the sheer drop below the "
        "platform. Moderate depth of field: the suspended head and the "
        "workers crisp, the far containment wall and lower levels dissolving "
        "into shadow and haze. Real optical lens blur, honest available-light "
        "editorial exposure, natural camera noise, very slight film grain, "
        "subtle lens vignette, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
}

# Variant 4 — added after ATTEMPT=1 and 3 (turbine-hall and reactor-vessel
# interiors) both passed the text/scene checks but were scored as looking
# render-like by vision inspection, while the exterior blue-hour variant 2 read
# as a genuine photograph. Variant 4 keeps the "uprate / outage work" subject in
# an exterior setting without repeating the dusk-nuclear-plus-data-center
# framing of the earlier CEG hero: a heavy crane lift over a plant laydown yard.
PROMPTS["4"] = (
    "Photo-realistic editorial press photograph, shot on a 28mm lens at f/4 "
    "from ground level in a nuclear power station's outdoor outage laydown "
    "yard at blue hour, during a maintenance outage. Filling the left of "
    "frame is the long windowless flank of a vast turbine hall, built from "
    "plain pale concrete panels with a run of thick large-diameter steam "
    "pipes carried on squat roller supports along its base, everything plain "
    "and completely unmarked. In the sharp centre mid-ground, a heavy "
    "telescopic mobile crane stands levelled on its outriggers on a wide "
    "concrete pad, its plain unmarked boom raised, and from its hook block a "
    "large cylindrical machine component is slung in heavy fabric lifting "
    "straps and held a few metres clear of the ground, turning very slowly, "
    "its surface wrapped and plain. Two maintenance workers in plain dark "
    "coveralls and plain white hard hats walk together beside the suspended "
    "load, seen mostly from behind and in profile, small in the frame, one "
    "steadying a tag line, neither turning toward the camera and no faces "
    "visible. In the background, softened well out of focus, a curved "
    "containment shell and a plain service building with a few scaffolding "
    "frames leaning against it rise against the sky. Wet stained concrete "
    "underfoot holds shallow puddles that catch weak reflections of the yard "
    "lights, and a low steel guard rail and a stretch of plain chain-link "
    "fence edge the pad. Cool indigo blue-hour ambient light with a couple of "
    "warm sodium work lamps and their soft flare, the last faint amber band "
    "low on the horizon behind the containment shell. No other buildings, no "
    "cooling towers and no data center anywhere in frame. Moderate depth of "
    "field with the crane, load and workers crisp and the far shell and fence "
    "softening into haze, real optical blur, honest available-light editorial "
    "exposure, natural camera noise, very slight film grain, subtle lens "
    "vignette, no plastic CGI sheen, no glossy render, no perfect symmetry, "
    "no 3D visualisation, no digital illustration, photorealistic, very high "
    "detail, professional editorial stock photography, 16:9 landscape "
    "composition. "
    + NO_TEXT
)


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
    img = img.convert("RGB")
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
    print(f"MD5 {os.popen('md5sum ' + OUTPUT).read().strip()}")


if __name__ == "__main__":
    main()
