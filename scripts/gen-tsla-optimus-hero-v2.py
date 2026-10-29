#!/usr/bin/env python3
"""Hero candidates for tsla-optimus-humanoid-mass-production-2026 (fal flux/schnell).

Strategy note: 23 earlier generations of a *full humanoid robot* all failed the
"looks like CGI" check — flux/schnell's humanoid aesthetic is too clean. This
script leads with ENVIRONMENT and HUMAN PRESENCE (workers, dust, line fixtures,
car bodies) so the frame reads as a documentary factory photograph, with the
humanoid only as a distant/secondary subject.

Scene plan:
  1 — wide dusty assembly hall: workers walking past a line of empty stations,
      bare car bodies on an overhead conveyor, one large grey humanoid figure
      at a station in the middle distance, backlit.
  2 — close candid: a worker's gloved hands on the bare alloy forearm of a
      partly built humanoid limb standing on a workstand, machinery clutter.
  3 — bare steel car body on an assembly line with overhead conveyor and two
      workers, no robot at all (pure automotive-plant documentary).

Writes /tmp/tslahero/att<N>.jpg at 1920x1080. Prompts carry the shared
NO_TEXT / NO_DISPLAYS / PHOTO blocks below.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-tsla-optimus-hero-v2.py
"""
import os
import sys

import requests
from PIL import Image

OUTDIR = "/tmp/tslahero"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

PHOTO = (
    "An unposed available-light documentary photograph taken with a real camera "
    "on a real factory floor by a working photojournalist, not a render, not a "
    "3D visualisation and not a digital illustration: imperfect hand-held "
    "framing, uneven exposure, mild motion blur on anything moving, airborne "
    "dust lit by the lamps, scuffed painted steel, oil stains, scuff marks on "
    "the floor, taped joints, uneven paint, streaked grime and small asymmetric "
    "details everywhere. Natural camera noise and clearly visible fine film "
    "grain in the midtones and shadows, mild chromatic aberration on "
    "high-contrast edges, subtle optical vignette, honest highlight clipping "
    "under the factory lamps. No plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no clean plastic surfaces, no studio lighting, no "
    "product-shot emptiness, no floating elements. 16:9 landscape composition, "
    "professional editorial stock photography, photorealistic, very high detail. "
)

NO_TEXT = (
    "The scene is completely free of any lettering: no text, no letters, no "
    "words, no numbers, no digits, no serial numbers, no part numbers, no model "
    "numbers, no stamped or engraved markings, no labels, no sticker labels, no "
    "signage, no safety signs, no painted numbers on the floor, no floor "
    "markings with numbers, no hazard stripes with lettering, no warning signs, "
    "no placards, no manufacturer or company names, no brand names, no logos, "
    "no trademarks, no badges, no wordmarks, no emblems on clothing, no printed "
    "documents, no clipboards, no charts, no whiteboards, no watermarks, no "
    "handwriting, no legible writing of any kind anywhere in the frame. "
    "Machinery, tooling and the vehicles are plain unmarked metal and plastic "
    "with no printing on them. "
)

NO_DISPLAYS = (
    "There is not one lit or active screen anywhere in this photograph: no "
    "monitor with content, no glowing display, no lit control panel, no "
    "illuminated buttons, no status lights, no blinking indicator LEDs, no "
    "glowing digital numerals, no backlit gauges, no lit instrument windows. "
    "Every screen, panel and instrument face in frame is dead, dark, angled "
    "away or so far out of focus that it reads only as a flat dark rectangle of "
    "material. The only light in the image comes from the factory's own lamps "
    "and daylight through the roof, never from the equipment. "
)

PROMPTS = {
    # 1 — wide dusty assembly hall, workers, bare car bodies, distant humanoid at a station.
    "1": (
        "Wide available-light documentary photograph inside a large automotive "
        "assembly hall, shot hand-held on a 35mm lens at f/4, ISO 1600, from "
        "shoulder height down the length of the plant. Concrete floor covered in "
        "tire scuff marks, oil stains and a fine layer of dust; overhead runs a "
        "heavy steel conveyor rail from which three bare unpainted steel car "
        "bodies hang on hooks, bodies in white with visible spot welds, panel "
        "gaps and no paint. Along the right side stands a row of empty assembly "
        "stations: steel workstands, coiled black cable looms with tie-wrapped "
        "ends, control pedestals painted a plain flat grey with unlit blank "
        "faces, and half-built steel fixtures wrapped in shipping foam. Two "
        "workers in scuffed hi-vis vests, hard hats and safety glasses walk "
        "away from the camera in the middle distance, slightly motion-blurred, "
        "one carrying a torque tool. In the middle distance at the second "
        "station stands a large humanoid robot of human height and proportions, "
        "plain matte grey and bare alloy construction with a boxy torso, thick "
        "articulated arms hanging at its sides, heavy braced legs and a plain "
        "blank rounded head with no face and nothing lit on it; its shoulder "
        "cover is missing so bare machined steel and an exposed actuator show, "
        "and it is partly in shadow with factory dust settled on its shoulders. "
        "Bright high-bay lamps along the roof, hard shadows falling across the "
        "floor, a soft haze of suspended dust in the light beams, strong "
        "perspective depth with the hall receding into industrial darkness. "
        + PHOTO
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 2 — close candid: worker's gloved hands on a partly built humanoid limb on a workstand.
    "2": (
        "Close candid available-light documentary photograph on the floor of an "
        "automotive plant, shot hand-held on a 50mm lens at f/2.0 at close range "
        "over a workstand. The frame is filled by the bare machined alloy "
        "forearm and hand structure of a large humanoid robot resting across a "
        "wooden-topped workstand: polished stainless tube, exposed actuator "
        "cylinders, black fingerless cable sleeves, a wrist joint with visible "
        "bolts and a small smear of grease. In the sharp foreground, a worker's "
        "hands in well-worn tan work gloves grip the forearm and feed a black "
        "cable loom through a machined gland with a slim hand tool, knuckles and "
        "a frayed cuff of a grey work jacket entering the frame; fingertips are "
        "grimy and the bench beneath is messy with a tin of bolts, a roll of "
        "tape, a used rag and metal swarf. Everything is scratched, dusty and "
        "used rather than new: fine scratches on the alloy, dust in the pores of "
        "the metal, fingerprint smears and lint on the surfaces. Behind, well "
        "out of focus, the pale grey mass of line equipment and a partly built "
        "car body dissolve into soft industrial bokeh. Mixed warm tungsten "
        "work-lamp light from the left and cool daylight from the roof. "
        "Extremely shallow depth of field, the gland, the tool and the gloved "
        "fingertips tack sharp, everything behind melting into creamy blur. "
        + PHOTO
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 3 — no robot: bare car body on the line with workers (pure plant documentary).
    "3": (
        "Available-light documentary photograph inside an automotive stamping "
        "and assembly plant, shot hand-held on a 28mm lens at f/5.6, three-"
        "quarter angle from floor level. Dominating the left half of the frame "
        "is a bare unpainted steel car body on a chain conveyor, spot welds, "
        "door apertures, unpainted seam sealer and handling dents all visible, "
        "with an overhead rail and hanging hooks above it. Two workers in blue "
        "coveralls, hard hats, safety glasses and worn gloves crouch and lean "
        "against the body, one running a pneumatic tool along the rocker panel "
        "with a short burst of dust and a few sparks, the other holding a "
        "rubber-tipped steady bar; their faces are turned away and one is "
        "slightly motion-blurred. Steel pressings are stacked on a plain wooden "
        "pallet at the lower right, strapped with frayed blue banding. The floor "
        "is stained concrete with tire tracks, rubber marks and scattered swarf; "
        "the plant behind recedes into dust and darkness with high-bay lamps "
        "throwing hard light and long shadows across the hall. "
        + PHOTO
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 4 — empty cleared assembly bay, no people at all (the line Tesla is converting).
    "4": (
        "Available-light documentary photograph of a cleared section of an "
        "automotive assembly plant, shot hand-held on a 28mm lens at f/5.6 from "
        "standing eye level, no people anywhere in the frame. A long line of "
        "empty assembly stations runs away from the camera: stripped steel "
        "workstands, bare grey steel fixtures with mounting plates and bolt "
        "holes, coiled black cable looms tied off with tape hanging from the "
        "stations, and a heavy overhead conveyor rail with a row of empty "
        "hanging hooks and chain. On the stained concrete floor lie a coiled air "
        "hose, a scattering of small metal offcuts, a half-collapsed cardboard "
        "box and a stack of worn wooden pallets; the concrete is scuffed, "
        "cracked, patched and marked with dark rubber streaks. In the right "
        "foreground lies a partially unbolted machined alloy bracket beside a "
        "loose bundle of grey cable connected to nothing. High in the roof the "
        "big industrial lamps burn hot, throwing shafts of light through "
        "suspended dust and haze that drifts across the hall; the far end of the "
        "plant dissolves into gloom. Everything is used, grimy and slightly "
        "crooked. "
        + PHOTO
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 5 — distant backlit humanoid in a dim plant, workers as faceless silhouettes.
    "5": (
        "Available-light documentary photograph shot into the light inside a "
        "dim large industrial plant, hand-held on a 50mm lens at f/2.8, ISO "
        "3200, exposure set for the bright high-bay lamps so the whole hall "
        "reads dark and the machinery nearest the light is almost a silhouette. "
        "In the middle distance stands the partially built frame of a large "
        "humanoid machine of human height and proportions, seen from behind and "
        "slightly to one side: a boxy bare steel torso, two thick articulated "
        "arms hanging at its sides, heavy braced legs, and a plain blank rounded "
        "head block with nothing lit on it. Its shoulder and back covers are "
        "missing, exposing machined steel joints, actuator cylinders and a loom "
        "of black cables taped off in a bundle; factory dust has settled "
        "unevenly on its upper surfaces and one hand rests flat on a steel "
        "workstand. Around it, out of focus and far back, two workers walk away "
        "as unreadable dark silhouettes with no visible faces, one pushing an "
        "empty sack barrow. The floor between camera and machine is bare stained "
        "concrete with tire tracks and a shallow smear of light; cables and "
        "hoses trail across it. Hard glare from the lamp bank, heavy atmospheric "
        "haze, deep blacks, visible grain. "
        + PHOTO
        + NO_TEXT
        + NO_DISPLAYS
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


def crop_to_16x9(img):
    w, h = img.size
    target = FINAL_W / FINAL_H
    cur = w / h
    if cur > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur < target:
        new_h = int(w / target)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def main():
    attempt = os.environ.get("ATTEMPT", "1")
    if attempt not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={attempt}")
        sys.exit(1)
    import fal_client

    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"att{attempt}.jpg")
    print(f"Generating ATTEMPT={attempt} -> {out}")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPTS[attempt],
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )
    url = None
    if result.get("images"):
        url = result["images"][0]["url"]
    elif result.get("output"):
        url = result["output"]
    elif result.get("image"):
        url = result["image"]
    if not url:
        print(f"ERROR: no image url in {result}")
        sys.exit(1)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    img = crop_to_16x9(Image.open(out))
    img.save(out, "JPEG", quality=92, optimize=True)
    print(f"Saved {out} {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
