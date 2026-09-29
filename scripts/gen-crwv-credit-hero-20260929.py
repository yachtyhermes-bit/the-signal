#!/usr/bin/env python3
"""Generate hero for crwv-ai-compute-credit-residual-value-2026 (fal flux/schnell).

Subject: CoreWeave (NASDAQ: CRWV) — the AI "neocloud" that buys GPUs with debt
and rents compute to AI labs. Article thesis: AI compute has become its own
credit-financed asset class (chip-backed loans, GPU residual values, hyperscale
build-out financing).

Scene chosen: an EXTERIOR at dusk — a vast purpose-built AI compute campus
UNDER CONSTRUCTION on a flat industrial site. Long low warehouse-scale
buildings with banks of louvered cooling, tower cranes and steel still going up
on one end, a floodlit concrete apron, high-voltage transmission pylons and a
substation at the edge of frame, long-exposure dusk sky, wet asphalt
reflections. No people, or one or two small distant silhouetted workers.
One strong subject, deep perspective, documentary industrial photography.

Deliberately DISTINCT from the recent Signal heroes that must not repeat:
  (1) cifr-barber-lake (20260926): a bitcoin-miner transmission-tower /
      substation dusk scene — this one is a whole BUILDING SCALE campus under
      construction, with the pylons only as a small edge-of-frame element.
  (2) moat-test (20260927): a ship canal lock at golden hour.
  (3) amat-hbm-packaging (20260928): a semiconductor fab CLEANROOM interior.
  (4) amkor-packaging (20260924): die-attach machine / package macro.
  (5) pl-suncatcher (20260925): a spacecraft in orbit.
  (6) crcl-stablefx (20260926): a retail checkout close-up.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/HUD.
- TEXT-FREE: construction sites naturally carry signage, crane numbers, vehicle
  livery, safety decals and warning boards — all explicitly forbidden.
- NO data-center long hallway / server aisle / rack interior composition
  (banned). This is an exterior, building-scale architectural view.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-crwv-credit-hero-20260929.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "crwv-ai-compute-credit-residual-value-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no "
    "numbers, no digits, no codes, no serial numbers, no part numbers, no "
    "printed markings, no stencilled characters, no painted words, no labels, "
    "no stickers, no barcodes, no QR codes, no warning decals, no hazard "
    "boards, no safety signage, no site hoarding posters, no billboards, no "
    "brand names, no manufacturer names, no company logos, no crane "
    "identification marks, no vehicle livery, no lorry lettering, no unit "
    "numbers, no plant tags, no screen, no display panel, no digital readout, "
    "no signage of any kind anywhere in the image, no watermark, no signature, "
    "no captions, no legible writing anywhere. All buildings, plant, cranes "
    "and vehicles are entirely plain and unbranded: bare concrete, plain "
    "corrugated metal cladding, plain grey steel, plain unmarked white and "
    "grey cabins. No illustration, no digital art, no cartoon, no 3D render, "
    "no CGI, no video-game look, no neon, no synthwave, no glowing lines, no "
    "light trails, no geometric patterns, no futuristic HUD graphics, no "
    "holograms, no overlay elements, no augmented-reality graphics, no charts, "
    "no graphs, no diagrams. Not a data-center hallway, no server aisle, no "
    "server racks, no rack of blinking network equipment, no cable runs, no "
    "rows of cabinets, no cleanroom, no office interior, no rocket launch pad, "
    "no wind turbines."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a vast purpose-built AI compute campus UNDER CONSTRUCTION on "
        "a flat industrial site at dusk. The dominant subject is a long, low "
        "warehouse-scale data-centre building stretching away in strong "
        "one-point perspective, its flanks clad in plain ribbed grey metal "
        "with long banks of louvered cooling intakes running the full length "
        "of the wall like dark horizontal gills, completely unmarked. At the "
        "far end of the same building, steel frame and open floor decks are "
        "still going up: a lattice of bare I-beams and scaffolding topped by "
        "one tall tower crane, its jib silhouetted against the afterglow. The "
        "ground is a wide floodlit concrete apron, still wet, holding long "
        "smears of the building's lights and the dusk colour, with faint "
        "painted-out lane markings just visible as sheen. At the very edge of "
        "frame, far behind the building, stand two high-voltage lattice "
        "transmission pylons carrying cables away into the dusk, small and "
        "secondary, with a low unlit substation compound beneath them. The "
        "sky is a long-exposure twilight gradient — deep blue at the top "
        "melting to a band of dull orange at the horizon — with high streaked "
        "cloud smeared by the exposure. No people, or at most two small "
        "distant silhouetted workers in hi-vis near the far corner of the "
        "building, tiny in the frame. Cool white floodlights and a few warm "
        "amber safety lights lift the concrete and the building's underside, "
        "nothing else self-lit, no neon, no glowing lines. Shot on a 35mm lens "
        "at f/8 from a low, stable, long-lens perspective: the near corner of "
        "the building and the wet apron tack sharp, depth carried by the "
        "receding louvre banks and pylons. Natural camera noise and very "
        "slight film grain, subtle lens vignette, honest realistic concrete, "
        "wet asphalt and ribbed-metal texture, professional documentary "
        "industrial photography, extremely detailed, photorealistic, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph, shot on a real camera, not computer generated: an "
        "authentic industrial press photo of a giant AI compute campus rising "
        "out of a flat site at blue hour. The frame is dominated by one long "
        "low data-centre hall seen from a three-quarter angle, its plain grey "
        "metal facade broken only by an unbroken horizontal band of dark "
        "louvered cooling vents, and by the raw steel skeleton still open at "
        "the near end where two tower cranes lean over the unfinished roof "
        "deck, jibs crossing the sky. Below, a broad wet concrete apron runs "
        "the length of the frame, mirroring the cold white work lights in "
        "long vertical streaks. Far off at the right-hand edge, a line of "
        "high-voltage lattice pylons marches away across the flat land toward "
        "a small transformer substation, unlit and secondary. Twilight sky, "
        "deep indigo overhead fading to a compressed band of burnt orange at "
        "the horizon, thin cloud streaked by the long exposure. One clear "
        "subject, deep perspective, the whole industrial landscape empty of "
        "people or at most a pair of tiny distant worker silhouettes in hi-"
        "vis. Cold white floodlight on the concrete, warm amber glow spilling "
        "from inside the open steel frame, nothing else emitting light, no "
        "neon and no glowing lines. Natural camera noise, slight film grain, "
        "subtle vignette, realistic wet asphalt, scaffold steel and concrete "
        "texture, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: a purpose-built AI data-centre campus at dusk, seen along "
        "the flank of a single enormous low warehouse-scale building. The "
        "whole facade is a rhythmic repetition of dark louvered cooling banks "
        "and plain grey cladding, blank and unmarked, marching into the "
        "distance in deep perspective. At the far end the building is still "
        "under construction: bare steel columns, open floor plates and a "
        "scaffolded core, with a tower crane and a smaller mobile crane "
        "outlined against the last light, their jibs black against a band of "
        "orange sky. In the foreground a wet concrete service apron, floodlit "
        "cold white, carries long reflections of the building's lights and "
        "the dusk. At the extreme left edge, out of focus in the distance, "
        "two lattice transmission pylons and a low electrical substation sit "
        "on the flat horizon. Long-exposure twilight: deep blue above, dull "
        "orange at the horizon, thin cloud smeared across the frame. No "
        "people, or one or two small distant silhouetted workers in hi-vis "
        "far down the apron. Cold white floodlights on the concrete, warm "
        "amber light deep in the open steel frame, gentle warm-and-cool "
        "contrast, nothing else self-lit. Shot on a 35mm lens at f/8, low "
        "stable viewpoint: sharp near corner and wet apron, smooth recession "
        "into distance. Natural camera noise, very slight film grain, subtle "
        "lens vignette, honest realistic concrete, wet asphalt and ribbed "
        "metal texture, no CGI look, no glossy render, no perfect symmetry, "
        "no digital illustration, photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "4": (
        "A genuine photograph, not a render and not computer generated: a "
        "huge AI compute campus under construction on flat open land, framed "
        "wide from a low vantage point at dusk. One long low data-centre hall "
        "occupies the middle distance, its plain grey ribbed metal walls "
        "carrying a continuous band of dark louvered cooling openings along "
        "the full length, entirely blank. To its right the site is unfinished: "
        "a steel skeleton of columns and beams, stacked grey cladding panels, "
        "scaffolding and a tower crane whose jib reaches over the frame, all "
        "silhouetted against the afterglow. The foreground is a wide wet "
        "concrete apron with long floodlit reflections and faint lane sheen. "
        "Far at the left edge, a line of high-voltage lattice pylons and a "
        "small unlit substation recede along the horizon, deliberately small "
        "and secondary. Dusk sky: deep blue above, a compressed dull orange "
        "band low down, high cloud streaked by a long exposure. No people, or "
        "at most two small distant hi-vis silhouettes near the construction "
        "end. Cold white floodlight washes the concrete, warm amber glow from "
        "inside the open steel frame, nothing else glowing, no neon, no light "
        "trails. Shot on a 35mm lens at f/8 with deep focus: crisp wet "
        "concrete and steel in the foreground, the long building receding "
        "cleanly to the horizon. Natural sensor noise, very slight film "
        "grain, subtle vignette, realistic metal, concrete and asphalt "
        "texture, no plastic CGI sheen, no glossy render, no 3D "
        "visualisation, no digital illustration, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a solitary, enormous AI compute building almost complete on "
        "a flat industrial site, photographed at last light. The building is "
        "very long and very low, its plain grey metal flank defined by three "
        "even tiers of dark louvered cooling banks that run its entire length "
        "and disappear to a vanishing point, giving strong one-point "
        "perspective, all surfaces blank and unmarked. Beyond it in the "
        "distance the next phase is still raw construction: a steel frame "
        "with open floor decks, a stair core and two tower cranes standing "
        "against the dusk, jibs angled, all silhouette. The site apron in the "
        "foreground is wet floodlit concrete, dark and gleaming, carrying the "
        "long doubled reflection of the building's cold white lights. At the "
        "far right edge, small on the horizon, high-voltage lattice pylons "
        "carry power cables away to a low substation compound. Long-exposure "
        "twilight sky: deep blue turning to a thin band of orange at the "
        "horizon, cloud drawn into soft streaks. Empty site, no people, or "
        "one or two tiny distant silhouetted workers in hi-vis at the corner "
        "of the building. Cold white floodlights and a faint warm amber glow "
        "from the unfinished block, gentle warm-and-cool contrast, nothing "
        "else self-lit. Shot on a 35mm lens at f/8, low stable perspective: "
        "sharp near asphalt and building corner, deep receding perspective. "
        "Natural camera noise, very slight film grain, subtle lens vignette, "
        "honest realistic wet concrete, asphalt and ribbed metal texture, no "
        "CGI look, no glossy render, no perfect symmetry, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "documentary industrial photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "A real photograph, not a render: the exterior of a purpose-built AI "
        "data centre at dusk, seen straight on down its own facade. An "
        "enormous low warehouse-scale building fills the frame, plain grey "
        "ribbed cladding with a single continuous horizontal band of dark "
        "louvered cooling vents that runs dead straight to the vanishing "
        "point, every surface completely unmarked. Small unlit rooftop "
        "cooling plant and plain air-handling units sit along the roofline, "
        "just visible against the sky. At the near end, a section is still "
        "under construction — bare steel columns, open joists, a half-fixed "
        "cladding panel edge — with a tower crane rising above it, silhouette "
        "only. The foreground is a wide wet concrete apron, floodlit cold "
        "white, its reflections stretched long across the frame by the low "
        "light. Distant at the left edge, small and fully secondary, HV "
        "lattice pylons and a substation run away toward the horizon. "
        "Twilight sky, long-exposure smooth: deep blue high, a dull orange "
        "seam at the horizon, soft streaked cloud. No people in frame, or a "
        "couple of tiny distant hi-vis silhouettes. Cold white floodlights on "
        "concrete and cladding, a faint warm amber interior glow at the open "
        "construction bay, nothing else emitting light, no neon, no glowing "
        "lines. Shot on a 35mm lens at f/8, low and level: crisp ribbed metal "
        "texture near to camera, clean deep recession. Natural camera noise, "
        "very slight film grain, subtle vignette, realistic concrete, wet "
        "asphalt, painted steel and ribbed cladding texture, no plastic CGI "
        "sheen, no glossy render, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "7": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera at dusk: a colossal AI compute campus on a flat site seen "
        "from an elevated but distant vantage, so the whole complex reads in "
        "one view. A long, low, plain grey data-centre hall with continuous "
        "dark louvered cooling banks fills the mid-frame; beside it, the next "
        "block is a raw steel skeleton still rising, with scaffolding, "
        "stacked cladding sheets and two tower cranes leaning over it, all "
        "black silhouettes against the afterglow. To the right, a low unlit "
        "substation compound and two high-voltage lattice pylons send cables "
        "away across the empty land, small and secondary in the frame. The "
        "foreground is a broad wet concrete site apron, floodlit cold white, "
        "with long reflections and faint tyre sheen. Long-exposure twilight "
        "sky: deep indigo at the top, a band of muted orange at the horizon, "
        "cloud smeared into soft horizontal streaks. One clear subject, deep "
        "perspective, no people, or at most two tiny distant silhouetted "
        "workers in hi-vis at the far edge of the apron. Cold white "
        "floodlights on the concrete, a warm amber glow from the open steel "
        "frame, gentle warm-and-cool contrast, no neon and nothing else "
        "self-lit. Shot on a 35mm lens at f/8: sharp wet concrete and "
        "cladding in the near frame, deep clean recession into the horizon. "
        "Natural camera noise, very slight film grain, subtle lens vignette, "
        "honest realistic metal, concrete and asphalt texture, no CGI look, "
        "no glossy render, no perfect symmetry, no digital illustration, "
        "photorealistic, extremely high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "8": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a purpose-built AI compute campus under construction, seen "
        "at dusk from ground level beside a wet floodlit apron. One very "
        "large component of it dominates the frame: a long, low "
        "warehouse-scale data-centre building with plain ribbed grey metal "
        "cladding and a deep continuous run of dark louvered cooling banks, "
        "entirely blank and unmarked, receding in strong perspective toward "
        "the distance. Behind and above it at the far end, a steel frame is "
        "half-built with a tower crane standing over the open deck, jib and "
        "rigging rendered as clean black silhouette against the last of the "
        "light. The wet concrete apron in the foreground reflects the "
        "building's cold white floodlights in long broken streaks, with soft "
        "sheen where lane markings would be. At the extreme right edge, small "
        "on the flat horizon, two lattice transmission pylons and a low "
        "substation stand in the haze. Long-exposure twilight: deep blue "
        "overhead fading to dull orange at the horizon, thin cloud pulled "
        "into streaks. No people, or at most two small distant silhouetted "
        "workers in hi-vis far down the building line. Cold white floodlights "
        "and a faint warm amber glow deep in the open construction bay, "
        "gentle warm-and-cool contrast, nothing else self-lit, no neon. Shot "
        "on a 35mm lens at f/8, low stable perspective: sharp near concrete "
        "and cladding, deep clean depth into the dusk. Natural camera noise, "
        "very slight film grain, subtle vignette, honest realistic wet "
        "asphalt, painted steel and ribbed metal texture, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, high detail, professional "
        "documentary industrial photography, 16:9 landscape composition. "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
