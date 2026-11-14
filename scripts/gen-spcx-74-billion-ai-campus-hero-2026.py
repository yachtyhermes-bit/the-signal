#!/usr/bin/env python3
"""Generate hero for spcx-74-billion-arizona-texas-ai-campus-2026 (fal flux/schnell).

Subject: a vast AI supercomputing campus under construction in the Arizona high
desert at golden hour — steel-framed, partially clad industrial halls, rows of
large dry-cooling units and transformers, high-voltage transmission pylons and
lines crossing the desert, distant mesas, graded dirt, a couple of construction
cranes, no people in the foreground.

  ATTEMPT 1 — Eye-level wide view from the graded dirt apron: two long
  steel-framed halls mid-construction (one skeleton, one partly clad in grey
  insulated panels), tower cranes above them, a row of big dry-cooling units
  and transformer bays in the middle distance, pylons marching off toward
  distant mesas, low gold sun.
  ATTEMPT 2 — Closer 50mm view walking the equipment yard: a long receding row
  of dry-cooling units and white transformer tanks in the foreground, the
  half-built halls behind, a crawler crane, pylons and lines stacked in the
  dusty gold air.
  ATTEMPT 3 — Long-lens 135mm elevated view from a nearby ridge: the whole
  campus layout spread across graded desert, halls, equipment yards, cranes,
  the transmission corridor crossing the frame, mesas on the horizon.

Deliberately NOT a data-center hallway / server aisle / server room / rows of
server racks. No abstract or digital art, no neon, no glowing lines, no
geometric patterns, no text, letters, numbers, logos or watermarks.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=2 /home/chino/video-venv/bin/python3 \
    scripts/gen-spcx-74-billion-ai-campus-hero-2026.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "spcx-74-billion-arizona-texas-ai-campus-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no site signs, no billboards, no labels, "
    "no banners, no flags, no painted markings, no unit numbers on equipment, "
    "no brand names, no company logos, no decals, no license plates, no "
    "watermark, no captions, no legible writing anywhere in the frame. This "
    "is a real landscape photograph of an industrial construction site, not "
    "an illustration, not digital art, not a cartoon, not a 3D render, not "
    "CGI, not a concept render: no neon, no synthwave palette, no glowing "
    "lines, no light trails, no holograms, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no geometric "
    "abstraction, no wireframe overlays, no data visualization, no "
    "science-fiction styling. This is absolutely not an interior: no data "
    "center hallway, no server aisle, no server room, no rows of server "
    "racks, no cabinets of blinking indicator lights, no cable trays, no "
    "raised floor, no ceiling, no corridor. The entire frame is outdoors "
    "under open desert sky."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 28mm wide lens at f/8, real late-afternoon available "
        "sunlight, not a render and not CGI: a vast AI data-center campus under "
        "construction in the Arizona high desert at golden hour, seen from "
        "eye level standing on the graded dirt apron at the edge of the site. "
        "The ground across the whole foreground is raw graded desert earth — "
        "pale tan and reddish-brown soil, compacted tire tracks, shallow "
        "scraped furrows, scattered gravel and a few small drifts of dust — "
        "stretching away from the camera toward the works. In the middle "
        "distance, slightly left of centre, two enormous long industrial "
        "halls stand side by side: the nearer one a bare steel skeleton of "
        "erect columns and roof trusses with grey steel decking partly laid, "
        "the further one already half clad in flat matte grey insulated wall "
        "panels with big blank openings where walls are still missing, both "
        "halls low and very wide and very long, warehouse-scale, their long "
        "flank walls receding in perspective. Two tall lattice-boom "
        "construction cranes rise above the rooflines, one yellow and one "
        "white, their jibs swung out over the steelwork, and a crawler crane "
        "sits lower near the halls with its boom half raised; no workers are "
        "visible anywhere in the frame. To the right of the halls, in the "
        "middle distance, sits an equipment yard: two long straight rows of "
        "big square dry-cooling units — grey finned heat-exchanger boxes the "
        "size of shipping containers, each with a large slow fan on top — "
        "arranged in ranks on concrete pads, and beyond them a fenced bay of "
        "white transformer tanks with steel radiators and porcelain bushings, "
        "linked by thin steel buswork. Behind everything, tall steel "
        "high-voltage transmission pylons march away to the right in a line "
        "across the open desert, six or seven of them receding into warm "
        "haze, with heavy cables sagging in long catenary curves between "
        "them and thin conductor lines crossing the pale sky. On the far "
        "horizon, low flat-topped desert mesas lie in layered bands of dusty "
        "violet and rose. The sun is low behind the camera to the left, warm "
        "gold light raking across the dirt and the steel, long soft shadows "
        "stretching to the right from every column and pylon, dust hanging "
        "in the air so the far pylons fade into warm haze; the sky is a "
        "clear desert gradient from pale hot gold near the horizon to a "
        "deeper dusty blue overhead, cloudless, nothing in the frame emits "
        "its own light, no lens flare, no glow. Deep depth of field: the "
        "near dirt is sharp, the halls and cranes sharp, the pylons and "
        "mesas softened only by real atmospheric haze. Natural sensor noise, "
        "fine film grain, subtle vignette, slightly off-centre casual "
        "framing, authentic editorial documentary feel, no plastic CGI sheen, "
        "no perfect symmetry. Photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition, wide horizontal framing. " + NO_TEXT
    ),
    "2": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 50mm lens at f/5.6, real late-afternoon available "
        "sunlight, not a render and not CGI: the equipment yard of a vast AI "
        "data-center campus under construction in the Arizona high desert at "
        "golden hour, seen at standing eye level from between the rows of "
        "plant. In the foreground, running from the lower right of the frame "
        "diagonally away toward the middle distance, a long receding row of "
        "large dry-cooling units: heavy grey steel heat-exchanger boxes with "
        "finned coil faces and big slow-turning fans under circular grilles "
        "on top, each about the size of a shipping container, bolted down in "
        "a neat line on a pale concrete pad, their steel flanks dusty and "
        "sun-bleached, casting long barred shadows across the pad to the "
        "right. Just beyond and left of them, three or four big white "
        "transformer tanks with vertical steel radiator fins and tall "
        "porcelain bushings stand inside a low fenced compound, thick cables "
        "and thin steel buswork looping between them. Beyond the yard, "
        "filling the middle of the frame, are the enormous half-built halls: "
        "one long low industrial building entirely framed in exposed steel "
        "columns and roof trusses with grey metal decking partly laid on "
        "top, and beside it another with long stretches of flat matte grey "
        "insulated wall panel already fixed while whole bays are still open "
        "to the sky, both buildings very wide, very long and low, their "
        "flank walls running off to the left in strong perspective. A tall "
        "crawler crane with a lattice boom stands beside the steel frame, "
        "and a second tower crane rises behind the clad hall, both still; no "
        "workers and no people are visible anywhere in the frame. Further "
        "left and behind, a line of steel high-voltage transmission pylons "
        "crosses the desert, their cables sagging in long curves against "
        "the sky, and low flat-topped mesas lie along the horizon in dusty "
        "rose and violet layers. The foreground ground is raw graded desert "
        "dirt, pale tan with reddish patches, tire ruts and loose gravel "
        "between the pads. The sun is low to the left and slightly behind "
        "the camera, throwing warm gold light across the equipment row and "
        "the white transformer tanks, rimming the pale steel edges, with "
        "long soft shadows reaching right and dust suspended in the air so "
        "the far pylons and mesas soften into warm haze; the sky is a clear "
        "desert gradient, pale gold to dusty blue, cloudless. Nothing in "
        "the frame emits its own light, no lens flare, no glow. Moderate "
        "depth of field: the nearest two cooling units and the pad are sharp, "
        "the transformer bay slightly softer, the halls and pylons softened "
        "by real atmospheric dust haze. Real optical lens rendering, natural "
        "sensor noise, fine film grain, gentle highlight roll-off, subtle "
        "vignette, framing slightly off-centre, authentic documentary feel, "
        "no plastic CGI sheen, no perfect symmetry. Photorealistic, "
        "extremely high detail, professional editorial stock photography, "
        "16:9 landscape composition, wide horizontal framing. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic editorial documentary photograph, shot on a full-frame "
        "camera with a 135mm telephoto lens at f/8 from a low ridge a "
        "kilometre away, real late-afternoon available sunlight, not a render "
        "and not CGI: the whole sprawling AI data-center campus under "
        "construction seen across the Arizona high desert at golden hour. "
        "The site fills the middle band of the frame as a wide arrangement of "
        "long low industrial buildings on graded desert ground: three or four "
        "very long, very wide warehouse-scale halls at different stages, one "
        "a bare steel skeleton of columns and roof trusses with grey decking "
        "partly laid, others partially clad in flat matte grey insulated wall "
        "panels with open bays, all of them spreading horizontally across the "
        "plain. Several construction cranes stand among them — two tall "
        "lattice tower cranes with jibs swung out and a crawler crane with "
        "its boom raised — and a crane barge of steel beams and stacked grey "
        "wall panels lies staged on the dirt nearby; no workers and no "
        "people are visible anywhere. Between and beside the halls, neat "
        "ranks of large grey dry-cooling units and white transformer tanks on "
        "concrete pads read as small blocks of equipment in ordered rows. "
        "The foreground and all the open ground is raw graded desert earth, "
        "pale tan and reddish, cut through by pale new access roads and "
        "compacted haul tracks that curve across the site, with dust rising "
        "in low drifting plumes from one of the work roads. Running through "
        "the right side of the frame and away to the horizon is a line of "
        "steel high-voltage transmission pylons with cables sagging in long "
        "catenaries, crossing the open desert toward low flat-topped mesas "
        "that lie along the far horizon in layered bands of dusty violet, "
        "rose and pale gold. The sun is low at the left, its warm gold light "
        "raking the landscape, lighting the long east-facing flanks of the "
        "halls and glinting on the steelwork, and stretching long soft "
        "shadows out to the right; thick warm haze and suspended desert dust "
        "compress the far distance so the mesas are pale and hazy. The sky "
        "is clear and cloudless, a smooth desert gradient from hot pale gold "
        "at the horizon to dusty blue overhead. Nothing in the frame emits "
        "its own light, no lens flare, no glow. Deep telephoto compression "
        "and real atmospheric haze, not bokeh; natural sensor noise, fine "
        "film grain, subtle vignette, slightly off-centre framing, "
        "authentic editorial documentary feel, no plastic CGI sheen, no "
        "perfect symmetry. Photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition, wide horizontal framing. " + NO_TEXT
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    with open("/home/chino/thesignal/.last_hero_prompt.txt", "a") as fh:
        fh.write(f"\n\n=== {SLUG} ATTEMPT {ATTEMPT} ===\n{prompt}\n")
    img = generate(prompt, OUTPUT)
    img = img.convert("RGB")
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 60:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
