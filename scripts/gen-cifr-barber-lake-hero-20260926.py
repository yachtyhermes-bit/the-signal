#!/usr/bin/env python3
"""Generate hero for cifr-barber-lake-twenty-year-ai-lease-2026 (fal flux/schnell).

Subject: Cipher Digital (NASDAQ: CIFR, formerly Cipher Mining) — a bitcoin miner
that pivoted into building industrial-scale AI/HPC data centres on Texas power
sites, and just extended its Barber Lake data-centre lease in Colorado City,
Texas from 10 years to 20 years, lifting contracted revenue above $9 billion.
Theme: mining sites becoming AI campuses, West Texas power, land and megawatts.

Frames chosen (photo-realistic editorial stock only):
  1 — high-voltage substation / lattice transmission towers at the edge of a vast
      industrial site under construction on the West Texas plains at golden hour,
      with a partly built low industrial building and a construction crane in the
      middle distance.
  2 — close low-angle shot of a massive grey transformer bank with thick cables
      and ceramic insulators against a dusk sky, dust in the air.
  3 — wide landscape of the construction site from a distance, transmission lines
      marching across the horizon, out-of-focus high-vis workers in the foreground.

Deliberately NOT (banned): no data centre server room, no server racks, no server
aisles, no glowing cable runs, no neon / synthwave colour, no abstract digital
art, no geometric patterns, no glowing lines, no holograms, no robots, no
charts / graphs / dashboards, no 3D render / CGI / video-game look, no readable
text of any kind. Distinct from recent Signal heroes (laser weapon on a truck,
payment terminal at a shop counter, rocket launch pad, wind farm).

Rules (per repo regen lessons):
- PHOTO-REALISTIC documentary photojournalism ONLY: available light, real sensor
  noise, long-lens shallow depth of field, imperfect handheld framing, worn and
  dusty metal, genuine textures. No CGI sheen.
- TEXT-FREE: substations, switchyards, transformers, equipment stencils, vehicle
  markings and site signage all invite lettering and numbers, so every surface is
  explicitly unmarked and every signboard explicitly blank.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-cifr-barber-lake-hero-20260926.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "cifr-barber-lake-twenty-year-ai-lease-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no ticker "
    "symbols, no stock tickers, no stencilled codes, no engraved equipment "
    "numbers, no serial numbers, no part numbers, no painted identification "
    "codes, no pole numbers, no hazard placards with writing, no danger "
    "signs with words, no warning labels, no site signage, no billboards, "
    "no road signs, no highway markers, no mileage markers, no distance "
    "markers, no county line signs, no gate signs, no fence placards, no "
    "posted notices, no branding anywhere, no brand names, no manufacturer "
    "names, no utility company names, no co-op names, no corporate logos, "
    "no trademarks, no watermarks, no signatures, no graffiti, no "
    "handwriting, no documents, no clipboards with writing, no paperwork, "
    "no newspapers, no magazines, no labels, no tags, no stickers, no "
    "decals, no licence plates, no vehicle markings, no painted numbers on "
    "machinery or truck doors, no hi-vis vests with printed logos or "
    "lettering, no hard hats with stickers, decals or writing, no legible "
    "writing of any kind anywhere in the image. Every signboard, placard "
    "and notice board in the scene is completely blank and unlettered, and "
    "every piece of equipment, every tower, every transformer and every "
    "vehicle is plain and unmarked. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game still, no concept art, no "
    "matte painting, no neon, no synthwave colour, no glowing lines, no "
    "light trails, no abstract geometric art, no floating holographic "
    "elements, no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no data centre, no server room, no server racks, no "
    "server aisles, no cable runs, no GPU racks, no racks of any kind, no "
    "robots, no drones, no lasers, no holograms."
)

COMMON = (
    "This is unposed documentary photojournalism caught in a single "
    "unrehearsed moment, not a staged commercial shot and not a hero render: "
    "the subject sits off-centre, the framing is loose and a little careless, "
    "and foreground elements cut into the edges of the frame. Honest "
    "available-light exposure, not a lit set and not an HDR composite. "
    "Shallow depth of field from a wide aperture on a long lens on a "
    "full-frame camera, real optical lens blur and creamy natural bokeh, "
    "unobtrusive film-like grain visible in the smooth sky and mid-tones, "
    "faint chromatic fringing on the high-contrast edges of bright metal "
    "against the sky, a subtle lens vignette, slight sensor softness in the "
    "shadows, real atmospheric haze on the horizon, airborne dust and grit "
    "catching the light, worn weathered surfaces with real rust, pitting, "
    "chipped paint, sunscreen fade, bird lime on the steelwork and wind-"
    "driven grime on every object, asymmetric unidealised composition, a "
    "slight hand-held tilt, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no immaculate cleanliness, no retouched hyper-clean "
    "digital look, no 3D visualisation, no digital illustration, no "
    "concept-art lighting, no video-game aesthetic, photorealistic, very "
    "high detail, professional editorial stock photography for a business "
    "newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — high-voltage switchyard / transmission towers at the edge of a vast
    #     industrial site under construction on the West Texas plains, golden
    #     hour, crane and partly built low building in the middle distance.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 70-200mm lens "
        "at 135mm and f/4 on a full-frame camera from a low vantage point at "
        "a fenceline, of a high-voltage electrical substation and two tall "
        "steel lattice transmission towers standing at the edge of a vast "
        "industrial construction site on the open West Texas plains at golden "
        "hour. The substation occupies the left two-thirds of the frame, "
        "slightly off-centre and tack sharp: a gravel switchyard of pale "
        "crushed caliche stone, banks of grey ribbed transformers with cooling "
        "fins and rusty drip stains, squat steel gantries carrying heavy "
        "corrugated aluminium busbar tubes, tall stacked porcelain and "
        "ceramic insulators glistening dull white in the low sun, and thick "
        "steel-cored aluminium conductor cables dipping in catenaries between "
        "the structures, all of it plainly unmarked with no stencilled codes, "
        "no equipment numbers, no placards with writing. Behind the yard, two "
        "tall steel lattice transmission towers rise against the sky, their "
        "worn galvanised angles and rivets catching the golden light, "
        "insulator strings hanging in dark chains from their crossarms. In "
        "the middle distance across open scrubland of low mesquite, dry "
        "grass and red dirt, a partly built low industrial building stands: a "
        "long steel-framed hall with grey corrugated metal cladding half "
        "fixed in place, open bays showing dark structural steel inside, "
        "still wrapped in white vapour-barrier sheeting, and a single tall "
        "tower crane standing over it with its jib angled across the sky. "
        "The horizon is flat, open and hazy for miles; the sky is dramatic, "
        "with a band of layered cloud catching a dusty orange and pink glow "
        "and deep blue overhead. In the near foreground, softly out of focus "
        "and cropped by the bottom of the frame, a chain-link fence line, "
        "clumps of dry weeds and a coil of unused black cable lie on the "
        "ground. Nothing in the scene carries any writing of any kind. No "
        "readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — close low-angle shot of a massive grey transformer bank with thick
    #     cables and ceramic insulators against a dusk sky, dust in the air.
    "2": (
        "Photo-realistic editorial stock photograph, shot on a 28mm wide lens "
        "at f/5.6 on a full-frame camera held very low and tilted up, of a "
        "massive grey power transformer bank in an outdoor electrical "
        "switchyard at dusk on the West Texas plains. Three huge grey "
        "oil-filled transformers dominate the frame, filling almost the whole "
        "image and rising steeply away from the camera in perspective: heavy "
        "riveted steel tanks with rows of vertical cooling fins, thick "
        "porcelain ceramic insulator bushings topped with brass caps, "
        "painted olive-green radiators gone chalky and faded, rust weeping "
        "down from every bolt head and weld seam, and dirt and dried dust "
        "caked in the crevices and drip trays. Thick steel-cored aluminium "
        "cables and bare copper conductors sweep down and out of the top of "
        "the frame in heavy arcs, and blocky steel gantry members cross the "
        "upper corners of the image. The transformer bodies are plainly "
        "unmarked: absolutely no stencilled numbers, no painted codes, no "
        "rating plates with writing, no hazard placards with words. The sky "
        "behind is deep dusk blue with the last dusty afterglow low on the "
        "horizon, and fine airborne caliche dust hangs in the air, catching "
        "the light and softening the distant structures into silhouettes. "
        "The foreground is a rough gravel switchyard surface, out of focus, "
        "with a few loose stones, a coiled length of rope and the corner of a "
        "concrete foundation slab cutting into the bottom of the frame. No "
        "people are visible. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wide landscape of the construction site seen from a distance with
    #     transmission lines marching across the horizon, out-of-focus
    #     high-vis workers in the near foreground.
    "3": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera from waist height on a dirt track, of a "
        "huge industrial construction site spread across the flats of the "
        "West Texas plains, with a line of steel lattice transmission towers "
        "marching away across the horizon. In the sharp middle distance a "
        "broad cleared and graded pad of pale caliche gravel carries the "
        "early frame of a large industrial power building: structural steel "
        "columns and roof trusses, grey corrugated cladding stacked on the "
        "ground, concrete foundations with protruding rebar, an articulated "
        "boom lift and a crawler crane parked at rest, stacked shipping "
        "containers and a tall portable light mast, an electrical switchyard "
        "with gantries and transformer banks off to the right, and a fine "
        "haze of dust drifting over all of it from the graded ground. To the "
        "left a row of maybe eight steel lattice transmission towers recedes "
        "to a vanishing point in the heat haze, each carrying heavy "
        "conductor catenaries and dark strings of ceramic insulators, and a "
        "second parallel line of shorter wooden distribution poles runs "
        "along the dirt access road toward the site. The land is flat and "
        "empty out to a pale hazy horizon, low mesquite scrub and dry grass "
        "in dull green and straw, red dirt, a barbed wire fence line. The "
        "sky is a big dramatic West Texas sky, high streaked cirrus over "
        "warm afternoon light low in the west. In the near foreground, well "
        "out of focus and cropped by the bottom edge of the frame, stand the "
        "backs and shoulders of two construction workers in plain dark "
        "coveralls with hard hats, turned away from the camera, their faces "
        "unidentifiable and unlit, one of them with a rolled plan tube under "
        "arm; their workwear is plain with no lettering, no logos and no "
        "printed words anywhere. No readable text anywhere in the scene, no "
        "site signage, no billboards, no licence plates. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — construction-forward but back-lit golden hour: a partly built
    #     industrial building with a crane AND a transmission line, so the
    #     "AI campuses under construction on Texas power land" idea is legible
    #     while keeping strong photographic cues (backlight, haze, grain).
    "4": (
        "Photo-realistic editorial stock photograph, shot on a 135mm lens at "
        "f/4 on a full-frame camera hand-held from the edge of a dirt access "
        "road, of a large industrial construction site on the West Texas "
        "plains at the last hour of golden-hour light. The low sun sits just "
        "off the left edge of the frame behind the structures, so the scene is "
        "strongly back-lit: long dark shadows rake toward the camera across "
        "the graded ground, the dusty air between camera and subject glows "
        "with warm haze and soft lens flare, and every metal edge catches a "
        "thin bright rim of sunlight. In the sharp middle distance stands a "
        "partly built low industrial building: a long steel structural frame "
        "of columns, beams and roof trusses half clad in grey corrugated "
        "metal sheeting, with open bays showing the dark skeleton inside, "
        "pallets of still-wrapped cladding on the ground, concrete "
        "foundations with protruding rebar, and a tall lattice-boom crawler "
        "crane standing beside it with its jib angled across the sky. To the "
        "right of the building, an electrical yard under construction: two "
        "steel gantries, a bank of grey ribbed transformers on a concrete pad, "
        "coiled conductor drums and heavy cables on the gravel, all plainly "
        "unmarked with no stencilled numbers, no codes and no placards with "
        "writing. Further off to the right a line of steel lattice "
        "transmission towers carries heavy catenary cables away toward the "
        "vanishing point in the heat haze. In the near foreground, out of "
        "focus and cut by the bottom edge of the frame, a weathered ranch "
        "fence of grey sun-bleached posts and sagging wire crosses the shot "
        "with dry grass and cow-parsley stalks in front of it. The land is "
        "flat, empty and hazy to the horizon; the sky above is a deep warm "
        "gradient of orange and dusty rose into slate blue, streaked with "
        "thin high cloud. The whole frame is grainy and slightly soft with "
        "genuine atmospheric depth. No readable text anywhere, no site "
        "signage, no billboards, no vehicle markings, no licence plates. "
        + COMMON
        + NO_TEXT
    ),
    # 5 — ATTEMPT 1's composition (substation + lattice towers, golden hour,
    #     proven photo-real) but with the construction promoted to the dominant
    #     mid-frame element so "AI campus being built on a Texas power site"
    #     is unmistakable. Everything else kept identical to prompt 1.
    "5": (
        "Photo-realistic editorial stock photograph, shot on a 70-200mm lens "
        "at 135mm and f/4 on a full-frame camera from a low vantage point at "
        "a fenceline, of a huge industrial site under construction beside a "
        "high-voltage electrical substation on the open West Texas plains at "
        "golden hour. The single dominant subject, sharp and centred in the "
        "middle of the frame, is a large low industrial building halfway "
        "through construction: a long steel structural skeleton of bare grey "
        "columns, beams and roof trusses, only part of it clad in grey "
        "corrugated metal sheeting, open bays exposing the dark steelwork "
        "inside, bays still hung with white vapour-barrier membrane flapping "
        "slightly in the wind, stacked pallets of wrapped cladding panels and "
        "a concrete foundation slab with protruding rebar littering the "
        "ground around it, and a tall yellow-grey lattice-boom crawler crane "
        "standing right beside it with its jib raised high and angled across "
        "the sky above the roofline. To the left of the building, occupying "
        "the left third of the frame and tack sharp, an operating high-voltage "
        "substation: a gravel switchyard of pale crushed caliche stone, banks "
        "of grey ribbed transformers with cooling fins and rusty drip stains, "
        "squat steel gantries carrying heavy corrugated aluminium busbar "
        "tubes, tall stacked porcelain insulators glistening dull white in the "
        "low sun, and thick steel-cored aluminium conductors dipping in "
        "catenaries between the structures, all plainly unmarked with no "
        "stencilled codes, no equipment numbers and no placards with writing. "
        "Behind and to the right of the building, two tall steel lattice "
        "transmission towers rise against the sky with insulator strings "
        "hanging in dark chains, their worn galvanised angles and rivets "
        "catching the golden light. Across the graded caliche pad between the "
        "structures sit the ordinary marks of a working site: a parked "
        "articulated boom lift, two stacked shipping containers, a coiled "
        "reel of black cable on the gravel, and a low haze of dust drifting "
        "from the graded ground. The horizon is flat, open and hazy for miles; "
        "the sky is dramatic, with a band of layered cloud catching a dusty "
        "orange and pink glow and deep blue overhead. In the near foreground, "
        "softly out of focus and cropped by the bottom of the frame, a "
        "chain-link fence line, clumps of dry weeds and a coil of unused "
        "black cable lie on the ground. Nothing in the scene carries any "
        "writing of any kind. No readable text anywhere, no site signage, no "
        "billboards, no vehicle markings, no licence plates. "
        + COMMON
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
