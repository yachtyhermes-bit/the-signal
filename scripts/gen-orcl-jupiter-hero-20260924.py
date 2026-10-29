#!/usr/bin/env python3
"""Generate hero for orcl-force-majeure-jupiter-2026 (fal flux/schnell).

Subject: Oracle (ORCL) sent a reported 'force majeure' notice to the developer of
Project Jupiter — a 2.45 GW AI data-center campus on 1,400 acres in Doña Ana
County, New Mexico (part of Stargate, with OpenAI). The trigger is power and
infrastructure: the 17-mile, 400 MMcf/d 'Green Chile' gas pipeline (Energy
Transfer) was denied permits twice by the New Mexico State Land Office and
slipped ~6 months to Feb 1, 2027. The campus was to be powered by Bloom Energy
fuel cells.

Frame: DESERT-SCALE ENERGY INFRASTRUCTURE + a STALLED CONSTRUCTION PROJECT.

Scene 1: a corridor of steel lattice high-voltage transmission towers marching
across flat New Mexico desert scrubland at golden hour, with distant
survey / earthmoving activity and an unpaved access road.

Scene 2: a large-diameter steel natural-gas pipeline right-of-way under
construction through desert scrub, with excavators and staged pipe sections
alongside the open trench.

Deliberately NOT a data-center composition (banned): no long server aisle, no
server racks, no GPU racks, no cable runs, no cleanroom, no hallway of racks.
NOT neon / synthwave, NOT glowing lines or light trails, NOT abstract geometric
digital art, NOT a chart / graph / dashboard, NOT a 3D render or CGI look.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: infrastructure scenes invite stencilled numbers, placards and
  brand names, so all lettering, numerals, signage, labels and logos are
  explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-orcl-jupiter-hero-20260924.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "orcl-force-majeure-jupiter-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no painted markings, no signage, no billboards, no road signs, "
    "no route markers, no mile posts, no warning placards, no hazard "
    "diamonds, no safety posters, no labels, no tags, no plates, no decals, "
    "no stickers, no bumper stickers, no painted stencils on machinery, no "
    "brand names, no manufacturer names, no company names, no utility names, "
    "no corporate logos, no trademarks, no watermarks, no signatures, no "
    "barcodes, no QR codes, no graffiti, no handwriting, no documents, no "
    "clipboards with writing, no building numbers, no legible writing of any "
    "kind anywhere in the image. Every piece of equipment, every vehicle, "
    "every tower leg, every pipe section, every cone and every surface is "
    "plain and unmarked, carrying no lettering, no numerals and no logos at "
    "all. No illustration, no digital art, no cartoon, no 3D render, no CGI, "
    "no neon, no glowing lines, no light trails, no synthwave, no abstract "
    "geometric art, no floating holographic elements, no artificial overlay "
    "graphics, no augmented-reality graphics, no charts, no graphs, no "
    "dashboards, no data visualisation, no screens at all, no data center, no "
    "server room, no server racks, no server aisles, no cable runs, no "
    "computing hardware."
)

PROMPTS = {
    # 1 — transmission-tower corridor marching across New Mexico desert at golden hour.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 70-200mm "
        "telephoto lens at f/5.6 on a full-frame camera, of a long corridor "
        "of steel lattice high-voltage transmission towers receding in a "
        "straight line across flat high-desert scrubland in southern New "
        "Mexico at golden hour. The nearest tower stands at the left third "
        "of frame, tall and crisply detailed, its open steel lattice "
        "structure, bolted angle-iron bracing and two long tapered "
        "cross-arms carrying thick bundled conductors that sag away in "
        "gentle catenary curves toward the horizon; behind it a further "
        "seven or eight identical towers diminish one after another toward "
        "the vanishing point, each smaller and hazier than the last, "
        "compressing in the long lens into a rhythmic row of dark vertical "
        "forms against the sky. Below them the ground is dry Chihuahuan "
        "desert: pale tan gravel, cracked caliche hardpan, low tufts of "
        "grey-green creosote bush and scattered mesquite and ocotillo, "
        "weathered into an even, gently rolling plain that runs unbroken to "
        "a distant low mountain ridge on the horizon. Just right of the "
        "tower line a wide unpaved caliche access road runs dead straight "
        "toward the horizon, its graded surface and faint tyre ruts "
        "catching warm light, and far away along it, small and half "
        "dissolved in haze and heat shimmer, a yellow earthmoving machine "
        "and a parked flatbed truck sit at the edge of freshly scraped "
        "ground with a low mound of turned earth beside them — distant "
        "evidence of stalled construction work, tiny in the frame, not the "
        "subject. Late low sun from the right side of frame rakes across "
        "the scene, throwing long soft shadows from every bush and tower "
        "leg toward the camera, rimming the steel lattice in warm amber "
        "and lifting dust into the air; the sky is a clear gradient from "
        "pale warm yellow near the horizon to soft dusty blue overhead with "
        "a few thin high clouds. Muted desert palette of tan, ochre, dusty "
        "olive and faded steel grey. Shot with honest available-light "
        "exposure, deep but natural depth of field keeping the near tower "
        "tack sharp and the distant towers softly hazed by atmosphere, "
        "real optical lens rendering, natural camera noise, very slight "
        "film grain, subtle lens vignette, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, no dramatic fantasy sky, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 2 — large-diameter gas pipeline right-of-way under construction through desert scrub.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/4.0 on a full-frame camera, of a large-diameter steel natural-gas "
        "pipeline right-of-way under construction across flat desert "
        "scrubland in southern New Mexico in low warm late-afternoon light. "
        "The camera stands low and slightly off to the side of the trench, "
        "looking straight down the right-of-way corridor as it runs off to "
        "the horizon in a dead-straight line: a long open trench cut into "
        "pale tan caliche soil, its near wall sharp and crumbling at the "
        "lip, filled with a row of long heavy dark steel pipe sections "
        "already laid end to end, their bare cylindrical surfaces catching "
        "a dull warm specular gleam along the top edge, each joint ringed "
        "by a raw welded band and supported on timber skids and sandbags, "
        "with loose backfill, pale spoil and freshly disturbed earth heaped "
        "along the near side of the cut. Staged on the cleared ground "
        "alongside the trench, out of focus in the near foreground, lie "
        "three more long unpainted steel pipe sections resting on wooden "
        "dunnage, their open bores dark circles facing the camera, and a "
        "short length of lifting sling hung from a bare crane hook. "
        "Further down the right-of-way, mid-ground and softly blurred, a "
        "tracked excavator with its boom and bucket lowered sits parked "
        "beside the trench next to a second idle digging machine and a "
        "wheeled side-boom pipeline tractor, all plainly painted in faded "
        "construction yellow, sitting still and unattended as though work "
        "has stopped. The surrounding land is dry Chihuahuan desert: pale "
        "gravel hardpan, low grey-green creosote and rabbitbrush bushes "
        "flanking the cleared corridor, a few mesquite, and a low ridge of "
        "distant hills on the horizon. Low golden sun from the left side of "
        "frame rakes across the ground, throwing long soft shadows from "
        "each bush and pipe section, warming the steel and the dust, with "
        "the sky a soft gradient from warm pale gold near the horizon to "
        "dusty blue overhead with thin streaked clouds. Muted palette of "
        "tan, ochre, dry olive and weathered steel grey. Very shallow to "
        "natural depth of field: the near pipe sections and trench lip are "
        "tack sharp while the excavators and the far end of the corridor "
        "melt into soft atmospheric haze. Real optical lens blur, honest "
        "available-light editorial exposure, natural camera noise, very "
        "slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
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


if __name__ == "__main__":
    main()
