#!/usr/bin/env python3
"""Generate hero for lhx-orbital-jamming-space-control-weapons-2026 (fal flux/schnell).

Subject: L3Harris Technologies (LHX) and the US Space Force's newly-acknowledged
ON-ORBIT space-control weapons. L3Harris built the Meadowlands ground-based
satellite jamming system (predecessor: the Counter Communications System) and
also builds space-based missile-tracking satellites. Sector: DEFENSE SPACE /
counter-space ground infrastructure.

Scene chosen: A SATELLITE-TRACKING GROUND STATION AT DUSK — large parabolic
tracking dish antennas on concrete pedestals at a remote desert site, one dish
seen in profile mid-track against a deep blue-grey sky, a defense technician in
plain work clothing walking the site, low warm work lights, desert scrub and
mountains on the horizon.

Deliberately NOT a data-center / server aisle / GPU rack scene (banned), NOT a
high-voltage substation or transformer bank (banned), NOT a generator yard
(banned), NOT an optics or laser lab (banned), NOT a wafer/photomask cleanroom
(banned), NOT a quantum cryostat lab (banned), NOT an office or desk scene
(banned), NOT a trading floor (banned). NOT abstract art, NOT digital art,
NOT a 3D render / CGI, NOT neon / synthwave, NOT glowing lines, NOT geometric
patterns, NOT HUD or hologram overlays, NOT text or lettering of any kind.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: antenna sites are littered with equipment labels, warning placards,
  hazard tape and control signage, so all lettering, numbers, UI, logos and
  brand names are explicitly forbidden. Any control display in frame is blank /
  dark / switched off / out of focus.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-lhx-space-control-hero-20260918.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "lhx-orbital-jamming-space-control-weapons-2026")
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
    "placards, no danger notices, no safety stickers, no hazard tape with "
    "writing, no antenna nameplates, no equipment labels, no engraved or "
    "stamped lettering on the dish structures or pedestals, no cabinet "
    "labels, no panel markings, no dial faces with numbers, no gauges with "
    "numerals, no dials, no meters, no charts, no arrows, no crosshairs, no "
    "alignment marks, no lettering on the concrete, no fence banners, no "
    "keyboard lettering, no name badges, no lanyards, no hard-hat lettering, "
    "no printed documents, no clipboards with writing, no brand names, no "
    "manufacturer names, no company names, no corporate logos, no trademarks, "
    "no watermarks, no stickers, no barcodes, no QR codes, no datamatrix "
    "codes, no handwritten markings, no graffiti, no license plates, no "
    "legible writing of any kind anywhere in the image. Every display or "
    "control screen in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with "
    "absolutely nothing readable or drawn on it, like an out-of-focus colour "
    "field photograph, not a screen with content. The antenna dishes, "
    "pedestals, support struts, cable runs and the worker's plain clothing "
    "are plain and unmarked. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit-board graphics, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no hologram, no overlay elements, "
    "no augmented-reality graphics, no data center server room, no server "
    "racks, no server aisles, no GPU hardware, no computer screen with text."
)

PROMPTS = {
    # 1 — dusk wide: remote tracking station, dish array in profile mid-track,
    #     technician walking the pad, desert scrub + mountains on the horizon.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera, of a remote satellite-tracking ground "
        "station at dusk. In the sharp mid-ground two very large parabolic "
        "tracking antenna dishes stand on heavy poured-concrete pedestals: "
        "the nearest dish is seen in profile, tilted steeply up and to the "
        "right mid-track, its deep ribbed concave face catching the last warm "
        "light while its smooth white back shell falls into shadow; thick "
        "steel support struts and a fat bundled cable run loop down to the "
        "concrete pedestal below it. The structures are entirely plain and "
        "unmarked - no nameplates, no labels, no lettering of any kind. "
        "Walking the cracked concrete apron between the pedestals away from "
        "the camera is a single defense technician seen from behind: a plain "
        "dark work jacket over work trousers, a plain unmarked cap, hands at "
        "their sides, mid-stride, neither turning nor posing, their figure "
        "crisp in the mid-ground. Low warm work lights on short poles throw "
        "soft amber pools onto the concrete and rim the technician's "
        "shoulders. Beyond the site, low desert scrub and a dark ridge of "
        "mountains sit on the horizon under a deep blue-grey sky with the "
        "last band of amber afterglow low behind the ridge. Moderate depth "
        "of field: the nearest dish and the technician crisp, the second "
        "dish and the mountain line softening into haze. Real optical lens "
        "blur, honest available-light editorial exposure, natural camera "
        "noise, very slight film grain, subtle lens vignette, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — 50mm: technician small in frame at the base of a huge dish, looking up.
    "2": (
        "A genuine photograph taken on site at a satellite-tracking ground "
        "station, not a render and not computer generated: a 50mm lens at "
        "f/4, blue hour. The frame is dominated by a single enormous "
        "parabolic tracking antenna dish on its concrete pedestal, seen from "
        "below and to one side so that the dish sweeps across the upper two "
        "thirds of the image, tilted up toward the deep indigo sky, its "
        "smooth pale back shell and the dark silhouette of its ribbed "
        "support struts reading clean against the fading light. At the base "
        "of the pedestal, small in frame and sharp, stands a defense "
        "technician in a plain dark work jacket and plain cap, head tipped "
        "back looking up along the dish's line of sight, one hand on the "
        "pedestal edge, unposed and unlit except by the ambient dusk and a "
        "single warm work lamp flaring low in the frame. The pedestal, "
        "struts, dish panels, ladders and hand rails are completely plain "
        "and unmarked - no nameplates, no stencilled numbers, no hazard "
        "placards, no lettering anywhere. Around the base, cracked concrete "
        "apron with a coil of heavy black cable and a few tufts of desert "
        "scrub pushing through the joints; further off, out of focus, the "
        "pale silhouette of another dish and a low equipment shelter against "
        "the mountain line. Honest blue-hour ambient light with the last "
        "amber on the horizon behind the dish, shadows pooling under the "
        "pedestal. Moderate depth of field with the technician and the near "
        "pedestal edge crisp and the dish rim and background softening, real "
        "optical blur, honest editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 3 — wide site establishing shot: several dishes on pedestals across the
    #     apron, technician mid-ground, mountains and desert scrub on horizon.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/5.6 from a low angle across the "
        "apron of a remote satellite-tracking ground station at dusk. "
        "Receding left to right across the frame in a loose line are three "
        "large parabolic tracking antenna dishes, each on its own wide "
        "poured-concrete pedestal: the nearest on the right is seen in "
        "profile mid-track, tilted high against a deep blue-grey sky, its "
        "concave face dark with the smooth pale back shell catching the last "
        "warm light; the middle dish faces away and the far dish is reduced "
        "to a soft pale silhouette near the horizon. Heavy steel struts, "
        "cable runs and plain steel ladders descend to each pedestal, all "
        "entirely plain with no nameplates, no labels, no stencilled "
        "numbers and no lettering of any kind. In the mid-ground walks a "
        "defense technician in plain dark work clothing and a plain "
        "unmarked cap, seen from the side and slightly behind, mid-stride "
        "with hands relaxed, small in the frame against the concrete. Short "
        "poles carry low warm work lights whose amber pools slide across the "
        "cracked concrete apron, and thin desert scrub bushes sit at the "
        "edge of the pad. Beyond the site, low desert scrub stretches to a "
        "dark ridge of mountains on the horizon under a deep blue-grey sky "
        "with the last band of amber afterglow low behind the ridge. Wide "
        "honest available-light editorial exposure, the near dish and the "
        "technician crisp and the far dishes and mountain line melting into "
        "haze, real optical blur, natural camera noise, very slight film "
        "grain, subtle lens vignette, no plastic CGI sheen, no glossy "
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
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )


if __name__ == "__main__":
    main()
