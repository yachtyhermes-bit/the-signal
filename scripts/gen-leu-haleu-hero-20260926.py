#!/usr/bin/env python3
"""Generate hero for leu-centrus-haleu-chokepoint-ai-power-2026 (fal flux/schnell).

Subject: Centrus Energy (NYSE: LEU) — the only licensed HALEU (high-assay
low-enriched uranium) production facility in the western world, at Piketon,
Ohio, scaling from demonstration to commercial uranium enrichment to fuel the
next generation of advanced nuclear reactors that will power AI data centres.
Theme: the nuclear fuel cycle; heavy industry; uranium enrichment.
NOT a data centre. NOT an abstract tech render.

Frames chosen (photo-realistic editorial stock only):
  1 — a vast industrial enrichment hall interior: long rows of tall grey
      cylindrical gas-centrifuge machines receding to a vanishing point, a
      spotless painted floor, overhead pipes and cable trays, one worker in
      white coveralls and a hairnet walking away from the camera.
  2 — a close low-angle shot of a heavy brushed-steel uranium hexafluoride
      (UF6) transport cylinder resting on a cradle, a technician in white
      coveralls and gloves inspecting the valve with a gloved hand, shallow
      depth of field.
  3 — a worker in white coveralls and safety glasses in the foreground, out of
      focus, looking down a long industrial plant aisle of centrifuge machines,
      cool overhead lighting, slight haze.
  4 — a tighter, closer view of the centrifuge cascade itself: a dense cluster
      of machine heads, pipework and valve manifolds in the mid-frame with a
      worker's gloved hand and forearm on a valve wheel in the near foreground.

Deliberately NOT (banned): no data centre, no server racks, no server aisles,
no glowing cable runs, no neon / synthwave colour, no abstract digital art, no
geometric patterns, no glowing lines, no holograms, no robots, no charts /
graphs / dashboards, no 3D render / CGI / video-game look, no yellow radiation
trefoil symbols with writing, no nuclear cooling towers, no readable text of
any kind. Distinct from recent Signal heroes (Texas data-centre construction
site with substation and transmission towers, contactless card tap at a shop
counter, kitchen table still life, ground-based laser weapon on a military
truck, rocket launch pad, cleanroom packaging line).

Rules (per repo regen lessons):
- PHOTO-REALISTIC documentary photojournalism ONLY: available industrial light,
  real sensor noise, long-lens shallow depth of field, imperfect handheld
  framing, worn and grimy metal, genuine textures. No CGI sheen.
- TEXT-FREE: industrial plant equipment, cylinders, drums, machine nameplates
  and hazard placards all invite lettering and numbers, so every surface is
  explicitly unmarked and every placard and notice board explicitly blank.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-leu-haleu-hero-20260926.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "leu-centrus-haleu-chokepoint-ai-power-2026")
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
    "codes, no machine nameplates, no printed tags on valves or pipework, no "
    "instrument gauges with numerals, no hazard placards with writing, no "
    "danger signs with words, no warning labels, no radiation trefoil "
    "symbols with writing, no site signage, no billboards, no posted "
    "notices, no branding anywhere, no brand names, no manufacturer names, "
    "no corporate logos, no trademarks, no watermarks, no signatures, no "
    "graffiti, no handwriting, no documents, no clipboards with writing, no "
    "paperwork, no newspapers, no magazines, no labels, no tags, no "
    "stickers, no decals, no licence plates, no vehicle markings, no "
    "coveralls with printed logos or lettering, no name patches, no hard "
    "hats with stickers, decals or writing, no hairnets with printed "
    "branding, no legible writing of any kind anywhere in the image. Every "
    "signboard, placard and notice board in the scene is completely blank "
    "and unlettered, every instrument face is plain and unmarked, and every "
    "piece of equipment, every cylinder, every machine and every pipe is "
    "plain and unmarked. There is no data centre, no server room, no server "
    "racks, no server aisles, no cable runs, no GPU racks, no racks of any "
    "kind, no glowing lines, no light trails, no neon, no synthwave colour, "
    "no abstract geometric digital art, no floating holographic elements, no "
    "wireframe, no charts, no graphs, no dashboards, no data visualisation, "
    "no robots, no drones, no lasers, no holograms, no nuclear cooling "
    "towers, no illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no video-game still, no concept art, no matte painting."
)

COMMON = (
    "This is unposed documentary photojournalism caught in a single "
    "unrehearsed moment, not a staged commercial shot and not a hero render: "
    "the subject sits off-centre, the framing is loose and a little careless, "
    "and foreground elements cut into the edges of the frame. Honest "
    "available-light exposure under real industrial lighting, not a lit set "
    "and not an HDR composite. Shallow depth of field from a wide aperture "
    "on a long-ish lens on a full-frame camera, real optical lens blur and "
    "creamy natural bokeh falling off into the far distance, unobtrusive "
    "film-like grain visible in the mid-tones and the smooth metal, faint "
    "chromatic fringing on the high-contrast edges of bright metal against "
    "the light, a subtle lens vignette, slight sensor softness in the "
    "shadows, real atmospheric haze hanging in the air of the hall, dust in "
    "the light beams and scuff marks on the floor, worn industrial surfaces "
    "with real grime, greasy hand-prints, scuffed paint, dull brushed "
    "stainless steel gone matte with age, chipped coating and faint water "
    "staining, fine cobwebs and dust on the overhead pipework and cable "
    "trays, asymmetric unidealised composition, a slight hand-held tilt, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, no immaculate "
    "showroom cleanliness, no retouched hyper-clean digital look, no 3D "
    "visualisation, no digital illustration, no concept-art lighting, no "
    "video-game aesthetic, photorealistic, very high detail, professional "
    "editorial stock photography for a business newspaper, 16:9 landscape "
    "composition."
)

PROMPTS = {
    # 1 — vast enrichment hall interior: long rows of tall grey cylindrical
    #     gas-centrifuge machines receding to a vanishing point, spotless
    #     painted floor, overhead pipes and cable trays, one worker in white
    #     coveralls and a hairnet walking away from camera.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 50mm lens at "
        "f/2.8 on a full-frame camera held at chest height just inside the "
        "door of a vast industrial uranium enrichment hall, of long rows of "
        "tall grey cylindrical gas-centrifuge machines standing in perfect "
        "process order and receding to a vanishing point deep in the "
        "distance. Each machine is a smooth vertical grey metal cylinder "
        "about two and a half metres tall on a low dark base, cased in matte "
        "painted sheet steel with a plain domed top cap, a heavy flanged "
        "joint at its middle and plain unmarked pipework running into its "
        "top and base; the surfaces are plain and completely unmarked with "
        "no nameplates, no stencilled codes, no printed labels and no "
        "numbers of any kind. The rows march away in perspective down the "
        "left and right of the frame, a wide central aisle between them "
        "paved in spotless smooth pale grey painted floor with a faint "
        "reflected sheen and a single scuff of dust. Above, the ceiling is a "
        "reticulated grid of grey steel cable trays, lagged insulated pipes, "
        "ducting and small bore tubing bundled in neat parallel runs, "
        "faintly dusted and cobwebbed where the light does not reach, all "
        "plain and unmarked. Cool white overhead industrial lighting falls "
        "in soft pools down the hall, the far end of which dissolves into "
        "gentle haze and shadow in the depth of field. The sharp subject in "
        "the mid-distance is a single worker in plain white coveralls and a "
        "white hairnet, seen from behind and slightly to the side, walking "
        "away from the camera down the central aisle between the machines, "
        "their coveralls plain and unmarked with no logos, no name patches "
        "and no lettering anywhere, their face not visible. Nothing in the "
        "scene carries any writing of any kind. No readable text anywhere, "
        "no signage, no placards, no data centre, no server racks, no "
        "glowing lines, no neon. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — close low-angle shot of a heavy brushed-steel UF6 transport cylinder
    #     on a cradle, technician in white coveralls and gloves inspecting the
    #     valve, shallow depth of field.
    "2": (
        "Photo-realistic editorial stock photograph, shot on an 85mm lens at "
        "f/2 on a full-frame camera from a low vantage point close to the "
        "floor, of a heavy brushed-steel uranium hexafluoride transport "
        "cylinder resting horizontally on a low steel cradle in the corner "
        "of an industrial nuclear fuel plant. The cylinder fills the lower "
        "half of the frame at a shallow angle, a thick welded steel pressure "
        "vessel about a metre in diameter with strongly domed ends, a dull "
        "brushed and slightly oxidised grey-silver surface, faint circular "
        "grinding marks, small patches of surface staining and dust caught "
        "in the crevices, heavy rolled-steel lifting trunnions welded to its "
        "shoulders, thick bolted flanges, and a squat unprotected valve "
        "assembly at its end with a plain hexagonal gland nut and a small "
        "plain handwheel. Every surface is completely plain and unmarked: no "
        "stencil codes, no painted numbers, no stamped serial numbers, no "
        "rating plates, no placards with writing, no hazard diamonds with "
        "words. Kneeling beside the cylinder in the sharp middle distance, a "
        "technician in plain white coveralls and white cotton gloves leans in "
        "and inspects the valve with a bare gloved hand, one hand resting "
        "flat on the cylinder shoulder and the other turning the plain "
        "handwheel, their face partly turned away and unidentifiable, their "
        "coveralls and gloves completely unmarked with no lettering, no "
        "logos and no name patches. Behind and above them the plant falls "
        "away into soft focus: the dull grey lower bodies of tall cylindrical "
        "machines, a run of lagged pipework and a steel floor grating, lit "
        "by cool overhead industrial light with the faintest haze in the air. "
        "The floor is bare sealed concrete, worn and chalky with wheel "
        "tracks. Nothing in the scene carries any writing of any kind. No "
        "readable text anywhere, no signage, no placards, no data centre, no "
        "server racks, no glowing lines, no neon. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — worker in white coveralls and safety glasses in the foreground, out
    #     of focus, looking down a long industrial plant aisle of centrifuge
    #     machines, cool overhead lighting, slight haze.
    "3": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/1.8 on a full-frame camera from just behind a worker, of a long "
        "industrial process aisle inside a nuclear enrichment plant. In the "
        "near foreground, huge and well out of focus, the back of the head, "
        "shoulder and upper arm of a worker in plain white coveralls fill the "
        "left third of the frame, cropped by the left and bottom edges: "
        "their coveralls are plain and completely unmarked with no logos, no "
        "name patches and no lettering, and the side of their plain safety "
        "glasses just catches the light as their head is turned away. Beyond "
        "them the image goes tack sharp down a long straight aisle running "
        "from the lower right of the frame to a bright vanishing point deep "
        "in the hall: on both sides of the aisle stand tall grey cylindrical "
        "gas-centrifuge machines in long process rows, smooth matte painted "
        "steel casings about two and a half metres tall on low dark bases, "
        "each with a plain domed cap and plain flanged joints, connected by "
        "slender unmarked pipework running in continuous manifolds along the "
        "tops of the rows; the machines are entirely plain with no "
        "nameplates, no codes, no printed labels and no numbers. Above, "
        "close-set rows of grey cable trays, insulated pipes and ducting run "
        "the length of the ceiling, faintly dusty and cobwebbed, unmarked. "
        "Cool overhead industrial lighting makes regular soft pools on the "
        "smooth pale grey painted floor and hangs slight blue-grey haze in "
        "the air deeper into the hall, so that the far end of the aisle "
        "fades gently into light. The floor is painted and spotless with a "
        "single faint dust scuff. Nothing in the scene carries any writing of "
        "any kind. No readable text anywhere, no signage, no placards, no "
        "data centre, no server racks, no glowing lines, no neon. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — tighter view of the centrifuge cascade: dense cluster of machine
    #     heads, pipework and valve manifolds in the mid-frame with a worker's
    #     gloved hand on a valve wheel in the near foreground.
    "4": (
        "Photo-realistic editorial stock photograph, shot on a 135mm lens at "
        "f/2.8 on a full-frame camera, looking along the top of a cascade of "
        "uranium enrichment gas-centrifuge machines inside an industrial "
        "plant. In the near foreground, large and softly out of focus, the "
        "white-sleeved forearm and white-gloved hand of a worker rest on a "
        "plain steel valve handwheel mounted on a manifold pipe, cropped by "
        "the bottom right corner of the frame, the plain white coverall "
        "sleeve completely unmarked. Just beyond it, tack sharp in the middle "
        "distance, a dense cluster of the machines themselves: the domed "
        "matte grey steel tops of tall cylindrical centrifuge units packed in "
        "close process rows, joined by a lattice of slender unmarked "
        "stainless pipework, small bolted flange joints, plain blank "
        "instrument covers and neat runs of bundled cable and thin-bore "
        "tubing sweeping in long parallel curves away to the right and "
        "receding out of focus to the left; the machines and all their "
        "fittings are entirely plain and unmarked with no nameplates, no "
        "stencilled codes, no printed tags, no labels and no numbers of any "
        "kind. The surfaces are worn and real: dull brushed stainless steel "
        "gone matte with age, faint greasy hand-prints around the valve, "
        "tiny dust deposits along the pipe runs, slight scuffing on the "
        "painted machine collars. Cool overhead industrial light rakes "
        "across the metal from the top left, with slight haze in the air and "
        "soft shadows falling between the machine rows, and the far side of "
        "the hall fading into gentle blur. Nothing in the scene carries any "
        "writing of any kind. No readable text anywhere, no signage, no "
        "placards, no data centre, no server racks, no glowing lines, no "
        "neon. "
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
