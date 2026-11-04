#!/usr/bin/env python3
"""Generate hero for crwv-midterm-permitting-risk-2026 (fal flux/schnell).

Subject: the 2026 US midterm elections putting data-center permitting and
siting risk in play for CoreWeave (CRWV) and the AI buildout.

Scene (must be DISTINCT from a server room / data-center aisle — overused):
an aerial / elevated photograph of a very large data-center construction site
on open Texas ranchland or scrubland in late-afternoon light: steel frame
buildings under construction, cranes, rows of cooling units, a high-voltage
transmission tower and lines cutting across the frame, dirt access road in
the foreground. Realistic, medium depth of field, professional lighting,
slight haze. Photographic, documentary, editorial.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/infographic/CGI.
- TEXT-FREE: no writing, letters, numbers, logos, signage, watermarks.
- No identifiable faces.
- Generate 1440x810, finalize 1536x864 (16:9), JPEG under 400KB.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-crwv-midterm-permitting-risk-hero-20261104.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "crwv-midterm-permitting-risk-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1536, 864

NO_TEXT = (
    "The photograph contains no writing of any kind: no text, no letters, no "
    "numbers, no words, no signage, no billboards, no placards, no labels, no "
    "stencilled markings, no painted characters on equipment or containers, no "
    "brand names, no company names, no manufacturer logos, no vehicle livery, "
    "no watermark, no caption, no legible writing anywhere in the frame. All "
    "construction equipment, trailers, containers and vehicles are plain and "
    "unmarked. "
    "This is a real photograph taken by a documentary photographer on a "
    "professional camera, not a 3D render, not CGI, not a video-game "
    "environment, not an architectural visualization, not a drone simulation, "
    "not digital art, not an illustration, not a matte painting. No neon, no "
    "glowing lines, no light trails, no synthwave colour grading, no geometric "
    "patterns, no infographic overlays, no HUD graphics, no text callouts, no "
    "server aisle, no server room interior, no rack hallway, no clean-room "
    "interior, no sci-fi styling."
)

PROMPTS = {
    "1": (
        "Aerial documentary photograph taken from a light aircraft or "
        "helicopter at about four hundred feet, looking down at a very large "
        "hyperscale data-center construction site spread across open central "
        "Texas ranchland. Late afternoon sun sits low and warm, raking across "
        "the site from the left and throwing long soft shadows behind every "
        "structure, with a faint atmospheric haze thickening toward the "
        "horizon. In the foreground a pale caliche dirt access road curves in "
        "from the bottom of the frame, tyre tracks and dust visible, a white "
        "unmarked pickup truck small on the road for scale. Beyond it, several "
        "long rectangular steel-frame buildings stand at different stages of "
        "construction: bare skeletons of dark grey girders and open roof "
        "trusses, some half-clad with pale metal wall panels, one nearly "
        "complete. Two crawler cranes and a lattice-boom crawler crane rise "
        "above the frames, booms angled across the pale sky, and a cluster of "
        "long white cooling units and fin-fan condensers is staged in neat rows "
        "on a gravel pad to the right. A tall steel high-voltage transmission "
        "tower stands in the mid-ground with its lines strung out and sweeping "
        "diagonally across the frame, cables catching a thin line of warm "
        "light. The surrounding land is dry scrub and pasture, dull olive and "
        "tan, with a few distant live oaks and a stock tank. Realistic "
        "medium depth of field with the near road and dirt sharp and the far "
        "site softening slightly in the haze, honest natural colour, dusty "
        "earth tones, professional editorial stock photography, genuine "
        "texture in the dirt and steel, subtle sensor noise, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "A grainy 35mm film photograph, an aerial shot taken from a small "
        "Cessna by a newspaper photographer covering a construction boom, "
        "looking down at a hyperscale data-center site being built on flat dry "
        "Texas scrubland. The horizon is slightly tilted and the framing is "
        "off-centre and imperfect, the way a real in-flight shot comes out. "
        "Across the lower half of the frame runs a rutted unpaved caliche haul "
        "road, pale dusty gravel with dark braided tyre ruts and a fine haze of "
        "suspended dust drifting over it, the ground beside it churned brown "
        "and uneven with scattered debris, pipe spools and mud. Three long "
        "low steel-framed halls sit mid-frame in different stages of build: "
        "exposed grey I-beam columns, open roof purlins, unpacked bundles of "
        "conduit, half-hung pale metal wall panels, dark open ends. A tall "
        "crawler crane with a long lattice boom lifts a roof truss at the left, "
        "a smaller cherry picker and a flatbed truck with no markings sit near "
        "the right, and long rows of white industrial condenser units are "
        "staged crookedly on gravel. A big steel transmission tower stands in "
        "the upper left with its conductors sagging away across the landscape "
        "toward a smaller tower in the far distance. Late afternoon low warm "
        "sun, deep long shadows, dust and humidity haze dulling the horizon, "
        "dry mesquite and dead grass in the untouched margins, a wire fence "
        "line. Flat honest documentary exposure, slightly faded colours, real "
        "dirt and rust and dust, uneven ground detail, imperfect real-world "
        "clutter, film grain and sensor noise, subtle vignette, no glossy "
        "finish, no symmetry, no computer-generated smoothness, photorealistic "
        "press photograph, high detail, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Grainy 35mm documentary aerial photograph, shot from a small plane by "
        "a working press photographer, looking down at an enormous AI "
        "data-center campus being built on open Texas ranch land in late "
        "afternoon light. Slightly tilted horizon, off-centre framing, the "
        "imperfect look of a real in-flight shot through a scratched window. "
        "A wide unpaved caliche road fills the bottom third of the frame, "
        "packed pale dust with deep dark tyre ruts and scattered gravel, "
        "running diagonally toward the site. Just beyond it the steel skeleton "
        "of a very long single-storey data hall stretches across the frame, "
        "grey I-beam columns and open roof trusses throwing long shadows across "
        "bare concrete slabs, stacks of pale metal wall panels and pipe spools "
        "laid crookedly beside it. A second completed hall with pale ribbed "
        "cladding stands behind, and long neat rows of white rooftop cooling "
        "units and fin-fan condensers line the right side on a gravel yard. Two "
        "crawler cranes with red lattice booms work the steel, one lifting a "
        "truss, plus a concrete pump truck and a few small excavators, all "
        "plain and unmarked. A tall grey steel high-voltage transmission tower "
        "rises prominently in the right mid-ground, its thick power cables "
        "strung diagonally across the whole frame toward a second tower in the "
        "distance, silhouetted against a hazy warm sky. Surrounding ground is "
        "dry olive scrub, cactus and patches of bare tan earth, a wire ranch "
        "fence running along the edge. Low warm late-afternoon sun, long deep "
        "shadows, dust haze softening the distance, flat honest documentary "
        "exposure, real dirt and rust, film grain and sensor noise, subtle "
        "vignette, no glossy finish, no symmetry, no computer-generated "
        "smoothness, photorealistic press photograph, very high detail, 16:9 "
        "landscape composition. "
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
    """Center-crop to 16:9, then resize to FINAL_W x FINAL_H."""
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
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img).convert("RGB")
    quality = 90
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True, progressive=True)
    size = os.path.getsize(OUTPUT)
    while size > 400_000 and quality > 70:
        quality -= 5
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True, progressive=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")
    with open(f"/tmp/crwv_midterm_prompt_{ATTEMPT}.txt", "w") as f:
        f.write(prompt)


if __name__ == "__main__":
    main()
