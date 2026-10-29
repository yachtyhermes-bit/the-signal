#!/usr/bin/env python3
"""Hero for hii-shipyard-labor-bottleneck-2026 (fal flux/schnell).

Subject: Huntington Ingalls Industries and the U.S. Navy shipbuilding labor
bottleneck -- welders, pipefitters and electricians are the constraint, not
steel or budget.

Scene: a cavernous enclosed shipbuilding hall with a huge grey submarine hull
section on keel blocks, gantry cranes overhead, scaffold towers, and a handful
of small workers in hard hats and welding shields. Industrial documentary
photography: dramatic overhead light, deep shadows, dust haze.

NO text anywhere (no letters, numerals, hull numbers, stencils, signage,
logos, watermarks). NO data center / server room / rack aisle. No neon, no
synthwave, no glowing lines, no geometric patterns, no abstract or digital
art, no 3D render. Strictly photo-realistic editorial photography.

Hard cap: 3 generations. ATTEMPT=1|2|3.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-hii-shipyard-labor-bottleneck-hero-2026.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "hii-shipyard-labor-bottleneck-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864
MAX_BYTES = 500_000

NO_BAD = (
    "Absolutely no text anywhere in the image: no words, no letters, no "
    "numerals, no digits, no painted hull numbers, no stencilled markings, no "
    "logos, no branding, no signage, no posters, no labels, no captions, no "
    "watermarks, no glyphs; any steel is plain and unmarked. No data center, no "
    "server room, no server racks, no rack aisle, no cable management trays. No "
    "neon, no synthwave, no glowing lines, no laser effects, no abstract shapes, "
    "no geometric patterns, no 3D render, no CGI, no digital illustration. "
    "Strictly photo-realistic editorial stock photography, real photographic "
    "optics, shallow depth of field, natural film grain, true-to-life steel, "
    "concrete and fabric texture, professional lighting, no HDR."
)

PROMPTS = {
    # 1: three-quarter view of the hull, workers small against the scale
    "1": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "35mm lens at f/2.2 on a full-frame camera, standing on the floor of a "
        "cavernous enclosed shipbuilding hall in a U.S. Navy shipyard. The "
        "subject fills the frame: an enormous curved section of a submarine "
        "pressure hull, matte primer-grey steel plate with visible weld seams, "
        "resting low on heavy timber keel blocks, its rounded flank running from "
        "the left foreground away into the dark rear of the hall. Steel "
        "scaffolding towers and temporary staging are clamped along its side, a "
        "tangle of orange power cables and hoses snakes across the stained "
        "concrete floor toward the camera, a red fire extinguisher and a stack "
        "of cut plate steel sit just off the keel blocks. In the middle "
        "distance, small against the hull and slightly soft with distance, four "
        "shipyard workers in scuffed yellow hard hats, dark fire-retardant "
        "coveralls and leather welding gloves are at work: one kneeling at a "
        "weld with a welding shield down, a single intense blue-white arc "
        "blooming and throwing hard light and long shadows across the steel, one "
        "climbing the scaffold with a tool bag on their shoulder, one coiling a "
        "hose, one walking away carrying a length of pipe. High above, two "
        "overhead gantry cranes span the hall from wall to wall, their hook "
        "blocks and heavy chains hanging still in the dark upper space. Cold "
        "grey daylight falls in dusty shafts from tall clerestory windows near "
        "the roof and mixes with warm sodium industrial floodlights high on the "
        "walls, deep black shadows pooled in the bays and behind the hull, dust "
        "and welding haze hanging in the air, quiet documentary realism, nobody "
        "looking at the lens. "
        + NO_BAD
    ),
    # 2: wider, deeper hall, hull broached from behind the blocks, more cranes
    "2": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "24mm lens at f/2.8 on a full-frame camera from a raised steel walkway "
        "inside a vast enclosed navy shipbuilding hall, looking down the length "
        "of the building. In the centre of the frame a massive grey submarine "
        "hull section sits on rows of timber keel blocks and steel cribbing, its "
        "unpainted primer-grey plates streaked with rust bloom and chalk marks "
        "worn away, open circular hatches and cut-outs revealing dark interior "
        "ribs; a forest of thin scaffold tubes and orange safety netting wraps "
        "its near side, and a tall mobile stair tower leans against the curve. "
        "Four gantry crane bridges span the hall overhead one behind the other, "
        "yellow-painted steel with trolleys and hook blocks, receding into "
        "shadow and haze. Small in the lower third of the frame, three workers "
        "in yellow hard hats and dark grey coveralls stand in a loose group on "
        "the floor beside a welding machine cart, one holding a grinder, one "
        "with a welding shield raised, their bodies dark shapes rimmed by the "
        "glare of a welding arc flaring low against the hull. Dramatic overhead "
        "lighting: hard-edged pools of white light from high bay lamps cut "
        "through dust and haze, the ceiling lost in blackness, deep shadows "
        "under the hull and between the keel blocks, cool blue-grey ambience "
        "against warm tungsten accents, faint lens flare from the arc, "
        "authentic industrial documentary feel, natural film grain, "
        "unretouched, no one looking at the camera. "
        + NO_BAD
    ),
    # 3: closer, low angle at the hull plate with workers at the weld line
    "3": (
        "Photo-realistic editorial stock photograph, horizontal 16:9, shot on a "
        "50mm lens at f/2.0 on a full-frame camera, low to the ground and close "
        "beside the curve of a submarine hull under construction inside a dim, "
        "cavernous shipyard hall. The grey steel plate sweeps across the frame "
        "from lower left to upper right, matte primer with faint rust staining, "
        "heavy weld beads and temporary stiffener bars welded along its surface, "
        "a wooden ladder and aluminium scaffold leaning against the curve at the "
        "right. In sharp focus at the left, one shipyard welder in a battered "
        "black welding shield, heavy leather jacket and gauntlets kneels on one "
        "knee, torch in hand, a blinding white-blue arc blooming at the joint "
        "and hard shadows raking away from it, sparks falling to the concrete. "
        "Behind, thrown into soft creamy bokeh, two more workers in yellow hard "
        "hats and reflective-striped coveralls walk along the base of the hull, "
        "and farther back the hall opens into darkness with two overhead gantry "
        "cranes hanging their chains high above and a distant column of hazy "
        "daylight from a high window. Dramatic overhead industrial lighting, "
        "deep black shadows swallowing the ceiling corners, dust motes "
        "glittering in the light beam, cool steel tones against the warm arc, "
        "shallow depth of field, authentic documentary realism, film grain. "
        + NO_BAD
    ),
}


def load_fal_key():
    for path in ("/home/chino/hermes-workspace/studio-api/.env",
                 "/home/chino/video_output/.fal_real"):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
                if path.endswith(".fal_real") and line.strip():
                    raw = line.strip()
                    key = raw.split("|", 1)[1] if "|" in raw else raw
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path, seed=None):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if seed is not None:
        args["seed"] = int(seed)
    print("Generating with fal flux/schnell ...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    url = (result.get("images") or [{}])[0].get("url") or result.get("image")
    if not url:
        print("ERROR: no image url: %s" % result)
        sys.exit(1)
    print("Image URL: %s" % url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded %s size=%s bytes=%d" % (out_path, img.size, len(r.content)))
    return img


def save_capped(img, path):
    for q in (92, 90, 88, 86, 84, 82, 80):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=%s" % ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT, os.environ.get("SEED") or None)
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img = img.convert("RGB")
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    save_capped(img, BACKUP)
    print("VERIFY %s dims=%dx%d bytes=%d" % (OUTPUT, W, H, os.path.getsize(OUTPUT)))


if __name__ == "__main__":
    main()
