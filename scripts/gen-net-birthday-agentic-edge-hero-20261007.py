#!/usr/bin/env python3
"""Generate hero for net-birthday-week-agentic-edge-2026 (fal flux/schnell).

Subject: Cloudflare's "Birthday Week 2026" — Workers AI and new agentic
capabilities that push AI inference out of central clouds and into
Cloudflare's edge network, which spans hundreds of cities worldwide. Article
focus: AI at the edge / distributed low-latency inference; BTIG raised the
price target.

Task brief: PHOTO-REALISTIC, matching the article subject, but visually
DISTINCT from typical data-center imagery. Avoid abstract / digital / neon /
glowing lines / geometric patterns. Vary the scene.

Scene strategy — the "edge" is the opposite of a central data-center hall, so
the hero shows AI compute living in ordinary, real-world places at the edge of
a city or network:
  1 = a field engineer bringing a compact ruggedised edge-compute node online
      at a small hillside mast above a town at sunrise (rural edge, not a hall)
  2 = a compact fanless edge-AI appliance being wired up inside a small local
      shop's back room (edge AI in an everyday place, warm daylight)
  3 = a technician at a street-side fibre cabinet in a real city street at
      golden hour (edge of a cityscape, human-scale, candid)
Deliberately NOT a data-center hallway / server aisle / GPU rack / cable run.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon,
  synthwave, CGI, 3D render, cartoon, glowing lines, light trails, HUD,
  holograms, abstract patterns.
- TEXT-FREE / no legible text: no readable words, numbers, labels, logos,
  brand names, gibberish.
- FACES NOT clearly readable (turned away, in soft focus) or anonymous.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage:
  ATTEMPT=1 OUT=/tmp/net1.jpg /home/chino/video-venv/bin/python3 \
      scripts/gen-net-birthday-agentic-edge-hero-20261007.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "net-birthday-week-agentic-edge-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = os.environ.get(
    "OUT", f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
)
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is plain and unmarked: no text, no letters, no numbers, no "
    "codes, no serial numbers, no labels, no plaques, no nameplates, no decals, "
    "no stencils, no logos, no brand names, no signage, no screens, no monitors, "
    "no displays, no UI, no code, no dashboards, no whiteboards with writing, no "
    "paper documents, no watermarks, no captions, no garbled lettering. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "video-game look, no neon, no synthwave, no glowing holographic lines, no "
    "light trails, no futuristic HUD graphics, no augmented-reality overlays, no "
    "abstract digital patterns, no circuit-board graphics. Not a data-center "
    "hallway, no server aisle, no server racks, no GPU racks, no cable-run "
    "interior, no abstract cyberspace."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, shot on a full-frame camera "
        "with a 35mm lens at f/2.2, not a render and not CGI: at golden sunrise "
        "on a grassy hillside above a small distant town, a field network "
        "engineer in a plain high-visibility work jacket and a plain hard hat "
        "crouches beside a compact grey weatherproof street cabinet bolted to a "
        "low concrete plinth at the base of a slim metal communications mast. "
        "The cabinet door is open and inside sits a small ruggedised fanless "
        "edge-compute appliance with a finned aluminium heatsink and a neat coil "
        "of thin single-mode fibre-optic patch cable with a small blue connector "
        "coupler, which the engineer's gloved hands are carefully routing into "
        "the plain unmarked metal ports. No markings anywhere. The engineer is "
        "seen from behind and in three-quarter profile, face turned away so it "
        "is not identifiable. Behind, the landscape rolls away into soft mist: "
        "green fields, hedgerows, a scatter of distant rooftops catching the low "
        "warm light, a pale sunrise sky of peach and powder blue. Very shallow "
        "depth of field — the cabinet, appliance and fibre are razor sharp while "
        "the hillside melts into creamy optical bokeh; real lens blur, natural "
        "sensor noise, very slight film grain, subtle vignette, honest realistic "
        "textures on metal, fibre and fabric, no CGI sheen, no perfect symmetry, "
        "nothing self-lit, no neon. Photorealistic, extremely high detail, 8k, "
        "authentic editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic documentary stock photograph, real camera, 50mm lens at "
        "f/2.0, available daylight, not a render and not CGI: in the tidy little "
        "back room of a small neighbourhood shop, a compact fanless edge-AI "
        "appliance — a small plain rectangular box of matte dark-grey plastic and "
        "brushed metal with a finned heatsink, its surface a completely blank, "
        "smooth, unbranded shell with no printing, no badge, no logo, no brand "
        "lettering and no text of any kind — with a single short fibre-optic "
        "pigtail with a small blue connector coupler, sits neatly on a wooden "
        "shelf inside a plain open metal wall cabinet beside a coiled cable and a "
        "plain power brick. A person in a plain dark work shirt, seen from behind "
        "and to the side so the face is not visible, is gently pushing the small "
        "blue fibre connector into the port on the front of the appliance with "
        "one hand. The room is ordinary and lived-in: a wooden counter, a potted "
        "plant, plain painted walls, a frosted-glass door, a window letting in "
        "warm soft late-afternoon light that falls across the shelf, an "
        "out-of-focus kettle and cardboard boxes on a lower shelf. Everything is "
        "plain and free of any branding, wording or marks. Very shallow depth of "
        "field with the appliance and the connector hand tack sharp and the "
        "little room dissolving into warm bokeh; real optical lens blur, natural "
        "sensor noise, very slight film grain, subtle vignette, honest realistic "
        "textures on wood, metal and plastic, no studio lighting, no CGI look, "
        "no plastic sheen, no perfect symmetry, nothing self-lit, no neon. "
        "Photorealistic, extremely high detail, 8k, authentic editorial "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic candid press photograph, shot on a Fujifilm camera with "
        "a 35mm lens at f/2, real available light, unretouched, not a render and "
        "not CGI: on a real city street at golden hour, a telecommunications "
        "technician in a plain high-visibility vest and plain dark trousers "
        "kneels at a small opened grey pavement fibre-optic cabinet, connecting a "
        "neat coil of thin single-mode fibre-optic patch cable into the plain "
        "unmarked metal ports inside, one compact ruggedised edge-compute "
        "appliance resting on a small mat beside the cabinet. The technician is "
        "seen from behind and in three-quarter profile, face turned away and not "
        "identifiable. In the soft-blurred background a real modern city street "
        "recedes: tree-lined kerbs, parked cars, glass shopfronts and low-rise "
        "buildings, blurred pedestrians walking past, all bathed in warm low "
        "golden-hour sunlight raking long shadows across the pavement. Everything "
        "is plain, no signage or markings. Genuinely imperfect candid "
        "composition, very shallow depth of field with the cabinet, fibre and "
        "hands razor sharp and the street melting into creamy bokeh; real optical "
        "lens blur, natural sensor grain, faint chromatic aberration at the frame "
        "edges, subtle vignette, realistic textures on metal and asphalt, no "
        "studio lighting, no neon, no glowing lines, no perfect symmetry. "
        "Photorealistic, extremely high detail, authentic editorial photography, "
        "16:9 landscape composition. " + NO_TEXT
    ),
    "4": (
        "Raw, unposed documentary photograph, shot handheld on a 28mm lens at "
        "f/2.8 in soft overcast morning light, real photograph not a render: on a "
        "windswept grassy clifftop overlooking a grey sea, a lone field engineer "
        "in a plain orange high-visibility jacket and plain white hard hat stands "
        "beside a small grey roadside communications cabinet at the foot of a "
        "slender steel antenna mast. The plain featureless cabinet door is open "
        "and inside sits a compact fanless edge-computing appliance whose brushed "
        "metal housing is a completely blank, smooth, unbranded box with no "
        "printing, no badge, no logo, no brand lettering and no text of any kind, "
        "wired with a tidy coil of thin fibre-optic patch cable into unmarked "
        "metal ports. The housing and every surface carry absolutely no words, no "
        "letters, no numbers and no marks. The engineer is seen from behind and "
        "side-on, hood and hat hiding the face, not identifiable, one gloved hand "
        "steadying the cabling. Behind, the headland drops to a hazy grey-green "
        "sea, thin mist, coarse grass bent by wind and a pale overcast sky. The "
        "frame is honestly imperfect: slightly off-centre, natural motion, real "
        "available light with soft flat shadows, visible lens breathing and "
        "field curvature, strong natural film grain, subtle sensor noise, slight "
        "muted desaturated colour, a gentle vignette, faint chromatic aberration "
        "in the corners, no CGI cleanliness, nothing self-lit, nothing glowing, "
        "no perfect symmetry. Photorealistic, extremely high detail, authentic "
        "editorial photojournalism, 16:9 landscape composition. " + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial stock photograph, real camera, 85mm lens at "
        "f/2.0, warm available light, definitively a photograph and not a render: "
        "the quiet corner of a small-town communications hut, a simple concrete "
        "room with a plain painted wall and a single high window casting a shaft "
        "of warm morning light and dust motes. On a plain grey metal shelf unit "
        "sits a neat row of small cooling fins and a single compact edge-compute "
        "appliance, a plain blank rectangular box of scuffed matte aluminium with "
        "no printing, no badge, no logo, no brand name and no text of any kind, "
        "its surface marked only by honest wear and a soft dust film. Fanless, "
        "warm to the touch, with a single short fibre-optic patch cable and a "
        "small blue connector coupler looping neatly down to a plain unmarked "
        "patch panel of identical blank ports. A technician in a plain dark "
        "utility uniform stands half in frame at the left edge, seen from behind "
        "in soft focus, only a shoulder and arm visible, gently resting a hand "
        "near the appliance; the face is not visible. Coarse concrete floor, a "
        "coiled cable, an empty cardboard box, a plain metal toolbox, all free of "
        "any writing. Very shallow depth of field with the appliance and the "
        "fibre loop tack sharp, the wall, window and technician melting into warm "
        "creamy bokeh. Real optical lens blur, natural sensor noise, very slight "
        "film grain, subtle vignette, honest worn textures on aluminium, concrete "
        "and metal, no studio lighting, no plastic CGI sheen, no perfect "
        "symmetry, nothing self-lit, no neon, no glowing lines. Photorealistic, "
        "extremely high detail, 8k, authentic editorial photography, 16:9 "
        "landscape composition. " + NO_TEXT
    ),
    "6": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.2 in bright soft daylight, definitively a real photograph and not a "
        "render: a small, bright, tidy utility back room with plain pale walls "
        "and a large window. A person in a plain dark work jacket stands fully in "
        "frame, seen entirely from behind with their back to the camera so the "
        "face is never visible, reaching up with one hand to steady a small "
        "compact edge-computing appliance mounted on a plain grey metal shelf "
        "bracket. The appliance is a neat matte dark-grey rectangular box, "
        "fanless, with a finned aluminium heatsink on one face and a short, "
        "straight, glossy glass-like fibre-optic patch cable running cleanly out "
        "of a small rectangular port, smooth and taut, clearly a functional "
        "cable. Sunlight from the window falls brightly across the shelf and the "
        "appliance, which is crisply lit and clearly visible; the room is bright "
        "and airy with a plain workbench, a coiled spare cable and an empty shelf. "
        "Everything is plain and free of any branding, wording or marks. Shallow "
        "depth of field with the appliance and the person's hand tack sharp and "
        "the bright room softening into gentle bokeh; real optical lens blur, "
        "natural sensor noise, very slight film grain, subtle vignette, honest "
        "textures on painted wall, metal and plastic, no studio lighting, no CGI "
        "sheen, no plastic look, no perfect symmetry, nothing self-lit, no neon, "
        "no glowing lines. Photorealistic, extremely high detail, 8k, authentic "
        "editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "7": (
        "Photo-realistic press photograph, real camera, 50mm lens at f/2.5, warm "
        "available window light, not a render and not CGI: a close, slightly "
        "side-on view of a technician's hands gently guiding a thin, straight, "
        "glossy glass-like single-mode fibre-optic patch cord — smooth and taut, "
        "ending in a small neat rectangular plastic connector, clearly a "
        "functional cable and not fuzzy or frayed — into a small port on the "
        "front of a compact fanless edge-computing appliance. The appliance is a "
        "neat matte dark-grey rectangular box with a finned aluminium heatsink, "
        "resting on a plain wooden shelf in a tidy small back room beside a coil "
        "of the same fibre cable and a plain power supply brick. A person in a "
        "plain dark work jacket is only partly in frame at the edge, a shoulder "
        "and arm, seen from behind so the face is not visible. Warm late "
        "afternoon light enters from a nearby window, softly lighting the hands, "
        "the appliance and the shelf; the room behind is ordinary and lived-in, "
        "out of focus. Everything is plain and free of any branding, wording or "
        "marks. Very shallow depth of field with the hands, the connector, the "
        "fibre and the appliance razor sharp; real optical lens blur, natural "
        "sensor noise, very slight film grain, subtle vignette, honest realistic "
        "textures on metal, glass, wood and fabric, no studio lighting, no CGI "
        "look, no plastic sheen, no perfect symmetry, nothing self-lit, no neon, "
        "no glowing lines. Photorealistic, extremely high detail, 8k, authentic "
        "editorial photography, 16:9 landscape composition. " + NO_TEXT
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} OUT={OUTPUT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    # Mirror to backup only when writing the canonical slug path.
    if os.path.abspath(OUTPUT) == os.path.abspath(
        f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
    ):
        os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
        img.save(BACKUP, "JPEG", quality=92, optimize=True)
        print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
