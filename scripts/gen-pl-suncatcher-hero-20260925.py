#!/usr/bin/env python3
"""Generate hero for planet-labs-google-suncatcher-orbital-ai-2026 (fal flux/schnell).

Subject: Planet Labs (PL) built the prototype spacecraft for Google's Project
Suncatcher — the first in-orbit test of Google TPU AI compute hardware, riding
a SpaceX Falcon 9 rideshare (Transporter-18) on 1 Oct 2026. The spacecraft,
named MVP, is roughly refrigerator-sized, carries four Google TPUs, and runs on
about a kilowatt of solar power. The long-term idea: solar-powered satellites
running AI compute in orbit, in clusters linked by lasers.

Frame: SPACE / ORBITAL HARDWARE — a real spacecraft photographed in orbit.
This is deliberately NOT a data center, NOT a server aisle, NOT a cleanroom
(except as the ATTEMPT=2 fallback), and NOT a launch pad.

Scene 1 (ATTEMPT=1): a small, compact satellite spacecraft in orbit above
Earth — curved Earth limb with atmosphere glow and sunlit cloud tops below,
the spacecraft's deployed solar arrays catching hard sunlight, dark space
above. Photographed like a real orbital press photo.

Scene 2 (ATTEMPT=2): alternate orbital framing — the spacecraft seen from a
lower/side angle with the terminator line and a bright crescent of sunlit
Earth, solar wings edge-on, deep space and faint stars behind.

Scene 3 (ATTEMPT=3): FALLBACK — the small satellite under final assembly in a
cleanroom: technicians in white cleanroom suits, spacecraft bus on a stand,
solar array panels, thermal blankets, bench equipment, warm practical light.

Deliberately NOT (banned, per repo regen lessons): no data-center hallway, no
server aisle, no server racks, no cable runs, no GPU rack. No digital art, no
3D-render/CGI look, no neon/synthwave, no glowing lines or light trails, no
geometric patterns, no abstract art, no holograms or HUD overlays. No text of
any kind anywhere (no logos, no lettering, no numerals, no signage, no screen
UI, no mission patches, no flags, no watermarks). No humans in the orbital
scenes; the cleanroom fallback may have out-of-focus suited technicians only.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: spacecraft invite mission patches, flag decals, part numbers and
  agency lettering, so all lettering, numerals, logos and signage are
  explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

SHIPPED: ATTEMPT=7 (high-bay integration, human-centred), 6th roll of that
prompt. Note for future space-sector heroes: flux/schnell essentially never
returns a "photo" verdict for isolated orbital hardware. 13 rolls across
ATTEMPTs 1/2/4/6 (spacecraft above Earth, terminator framing, no-fill raw-sun
lighting, through-a-window framing) all passed text/logo/server-room checks but
were scored render/CGI by scripts/vision_inspect.py — schnell smooths
featureless black space and evenly rim-lights the bus. Re-rolling does not fix
it; changing genre does. The cleanroom/high-bay scene with prominent suited
technicians (the amkor-proven composition) passed as "photo" on 5 of 8 rolls,
but flux sprinkles shipping stickers ("FRAGILE", "TOP") and brand logos onto
crates, so this prompt explicitly bans cartons, packing tape and stickers as
objects. Control check: 3 of 4 recent shipped heroes score "photo", so the
verdict is discriminating, not blanket-flagged.

Usage: ATTEMPT=7 /home/chino/video-venv/bin/python3 scripts/gen-pl-suncatcher-hero-20260925.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "planet-labs-google-suncatcher-orbital-ai-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no mission "
    "patches, no insignia, no emblems, no flags, no national flags, no "
    "agency logos, no sponsor logos, no sponsor decals, no corporate logos, "
    "no trademarks, no brand names, no manufacturer names, no company "
    "names, no serial numbers, no part numbers, no asset tags, no stencilled "
    "codes, no identification plates, no nameplates, no engraved or etched "
    "markings on the spacecraft body or solar panels, no painted markings on "
    "any hardware, no signage, no placards, no labels, no stickers, no "
    "decals, no warning notices, no instrument lettering, no antenna "
    "lettering, no screen content, no user interface, no display readouts, "
    "no keyboards, no watermarks, no signatures, no copyright marks, no "
    "barcodes, no QR codes, no datamatrix codes, no handwritten markings, no "
    "graffiti, no documents, no clipboards with writing, no legible writing "
    "of any kind anywhere in the image. All spacecraft structure, solar "
    "arrays, thermal blankets, instrument housings, fasteners, wiring and "
    "connectors are plain, bare and completely unmarked. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no synthwave, "
    "no glowing lines, no light trails, no laser beams, no geometric "
    "patterns, no abstract art, no circuit-board graphics, no network "
    "diagrams, no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no futuristic HUD graphics, no holograms, no overlay "
    "elements, no augmented-reality graphics, no artificial graphics in "
    "space, no data center, no server room, no server racks, no server "
    "aisles, no cable runs, no GPU racks."
)

COMMON = (
    "Strong directional unfiltered sunlight from one side and deep shadow on "
    "the other, hard specular highlights clipped on bare metal, honest "
    "available-light exposure, true colour, natural camera noise, very slight "
    "film grain, subtle lens vignette, slight sensor softness in the shadows, "
    "no plastic CGI sheen, no glossy render, no perfect symmetry, no "
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, an actual photograph taken on a real camera, not a "
    "rendering, handheld with a slightly imperfect framing, uneven corner "
    "illumination, faint chromatic fringing on high-contrast edges, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — small spacecraft in orbit above Earth, hard sunlight, cloud tops below.
    "1": (
        "Professional stock photograph of a small, compact satellite "
        "spacecraft in low Earth orbit, photographed like a real orbital "
        "press photograph, shot on a 50mm lens at f/2.8 from a nearby "
        "spacecraft. The satellite occupies the right half of frame, tack "
        "sharp: a boxy rectangular spacecraft body the size of a domestic "
        "refrigerator, wrapped in crinkled silver-gold multilayer thermal "
        "insulation that catches the hard sunlight in bright metallic "
        "creases, with plain bare aluminium structural rails along its "
        "edges, small round thruster nozzles, a squat cylindrical antenna "
        "mast and a cluster of short blunt-tipped helical antennas on its "
        "upper face, every surface plain, unmarked and free of any lettering "
        "or insignia. Two long flat solar array wings are deployed on "
        "slender booms on either side, their dark blue-black photovoltaic "
        "cell faces glossy and semi-reflective, one wing angling toward the "
        "camera and raking light across its panel seams with a harsh "
        "specular streak, the other wing edge-on and catching only a thin "
        "bright rim. Below and filling the lower third of the frame is the "
        "curved limb of the Earth, softly out of focus, sunlit cloud tops in "
        "white and pale cream drifting over a deep blue ocean, with a thin "
        "luminous band of atmosphere glowing pale cyan-white along the "
        "horizon curve, the terminator falling away into darkness at the "
        "lower left. Above the satellite the frame opens into near-black "
        "space with a faint dusting of dim stars and one soft starfield "
        "bloom, deep and clean. The composition is a candid orbital "
        "documentary frame with the spacecraft slightly off-centre and one "
        "solar wing cropped by the edge of frame, the Earth limb melting "
        "into creamy optical bokeh beneath it, no lens flare other than one "
        "small honest streak. Realistic photo, shallow depth of field, "
        "professional lighting. " + COMMON + NO_TEXT
    ),
    # 2 — alternate orbital framing: terminator crescent, wings edge-on, deep space.
    "2": (
        "Professional stock photograph of a small satellite spacecraft in "
        "orbit, shot on an 85mm lens at f/2.0 as a real orbital press "
        "photograph from close range. The spacecraft sits in the left third "
        "of frame with the frame's eye at its lower flank, tack sharp: a "
        "compact bus about the size of a refrigerator, its plain riveted "
        "aluminium and composite panels half in brilliant sunlight and half "
        "in black shadow, wrapped in places with crinkled gold and silver "
        "thermal blanket that glints hard where the sun catches a fold, a "
        "small sensor package and a flat shielded panel on its sunlit face, "
        "short latching mechanisms and tidy laced wiring harnesses along one "
        "side, everything bare, plain and carrying no lettering, no insignia "
        "and no markings of any kind. Both solar array wings are seen almost "
        "edge-on as two thin bright blades of light extending to the right, "
        "their cell faces dark with a narrow strip of specular reflection "
        "running along each panel edge, thin shadows cast by the booms "
        "falling across the spacecraft flank. Behind and below, the Earth "
        "appears only as a huge soft crescent of sunlit atmosphere along the "
        "very bottom of the frame — a luminous pale blue-white arc of air "
        "glow over a sliver of sunlit cloud, everything below that in "
        "velvety darkness, deeply out of focus. The upper two thirds of the "
        "frame is black space with a sparse scatter of faint real stars, "
        "gentle sensor noise visible in the black and a soft vignette "
        "pulling the corners down. Slightly off-level handheld framing with "
        "the horizon arc skewed against the frame edge. Realistic photo, "
        "shallow depth of field, professional lighting. " + COMMON + NO_TEXT
    ),
    # 3 — FALLBACK: spacecraft under final assembly in a cleanroom.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2.0 on a full-frame camera, inside a satellite integration "
        "cleanroom during final assembly of a small spacecraft. In the "
        "centre of frame, tack sharp, a compact rectangular spacecraft bus "
        "about the size of a refrigerator rests on a low plain metal "
        "integration stand, its bare machined aluminium panels, plain "
        "fastener rows and partially laced wiring harness all clean and "
        "completely unmarked, one face still wrapped in loose silver "
        "multilayer thermal blanket with a soft crinkled sheen, a stubby "
        "antenna mast folded flat along its top and a flat shielded "
        "equipment panel on one side. Nearby, leaning in a shallow cradle on "
        "the bench to the right, a large rectangular unframed solar array "
        "panel shows its dark blue-black cell face and fine grid of seams "
        "under the lights, entirely plain and unlettered. On the bench in "
        "the sharp near foreground, partly cropped by frame, sit a plain "
        "aluminium tool tray, a torque driver and a coiled length of laced "
        "cable, with soft warm reflections on the steel bench top. In the "
        "mid-ground behind the spacecraft, out of focus and rendered only as "
        "soft shapes, two technicians in white full-body cleanroom suits "
        "with hoods, face masks and gloves lean over a bare workbench and a "
        "piece of test equipment, seen from behind and in three-quarter "
        "view, mid-task, faces turned away and not identifiable. The "
        "cleanroom recedes into warm haze with the pale flanks of more "
        "integration stands and a plastic-sheeted wall beyond. Warm "
        "yellow-white overhead cleanroom lighting rakes across the top of "
        "the spacecraft from the upper left with dark falloff toward the "
        "back of the room. Realistic photo, shallow depth of field, "
        "professional lighting. " + COMMON + NO_TEXT
    ),
    # 4 — orbital, re-rolled with heavy real-camera defect cues. Added after
    #     ATTEMPT 1 and 2 both passed text/scene/logo checks but were scored
    #     "render/CGI" by vision inspection: flux lighting for isolated space
    #     hardware comes back evenly rim-lit and studio-clean, which reads as a
    #     render. This variant removes fill light altogether and demands the
    #     defects a real orbital exposure actually has.
    "4": (
        "A real documentary photograph taken by a photojournalist on a real "
        "camera, not a render and not computer generated, shot on an 85mm lens "
        "wide open at f/1.8 from a nearby spacecraft window, of a small "
        "satellite spacecraft against the Earth below. The spacecraft fills "
        "the centre-right of frame, tack sharp in the plane of focus: a "
        "compact boxy bus about the size of a refrigerator, its plain bare "
        "machined aluminium frame and composite side panels entirely "
        "unlabelled and unmarked, partially draped in crinkled silver and gold "
        "multilayer thermal blanket whose folds throw hard black shadows, with "
        "a stubby folded antenna mast, a small cylindrical sensor housing, "
        "plain bolted flanges and a tidy laced wiring harness visible along "
        "one flank. Two long solar array wings extend left and right on thin "
        "booms, their dark blue-black cell faces glossy and semi-reflective, "
        "fine panel seams running across them, one wing catching a single "
        "harsh specular streak of raw unfiltered sunlight. The lighting is "
        "brutal and completely uncontrolled: one face of the spacecraft is "
        "blown out by direct sunlight with clipped hot highlights on the bare "
        "metal, the rest falls into near-black shadow with crushed dense "
        "blacks, there is no fill light of any kind, no rim light, no studio "
        "lighting, no even illumination, and the shadow side shows visible "
        "ISO noise, sensor grain and a couple of faint hot pixels. Below and "
        "behind it, softly out of focus and slightly overexposed, the curved "
        "limb of the Earth rolls away with sunlit white cloud tops and deep "
        "blue ocean, a thin luminous pale cyan band of atmosphere glowing "
        "along the horizon curve, and the terminator dropping into darkness "
        "toward the lower left corner. The upper part of the frame is black "
        "space with heavy visible sensor noise, a few dim stars and no "
        "gradient wash. Slightly crooked handheld framing with the horizon "
        "tilted a degree or two off level and the spacecraft a little "
        "off-centre, faint chromatic fringing on the high-contrast limb edge, "
        "soft optical blur melting the Earth into creamy bokeh, honest "
        "available-light exposure, subtle lens vignette, uneven corner "
        "illumination, mild camera shake. Realistic photo, shallow depth of "
        "field, professional lighting. " + COMMON + NO_TEXT
    ),
    # 5 — FALLBACK re-rolled: satellite high-bay integration scene with the
    #     full real-camera defect list and no screens anywhere. Modelled on the
    #     amkor packaging hero (the repo's proven "photo"-passing cleanroom
    #     composition): warm practical light, glossy floor reflections, real
    #     tools in the sharp foreground, out-of-focus suited technicians.
    "5": (
        "A real documentary photograph taken by a photojournalist on a real "
        "camera, not a render and not computer generated, shot on a 35mm lens "
        "at f/2.0 on a full-frame camera, inside a spacecraft integration "
        "high bay during the final build of a small satellite. In the sharp "
        "left foreground, partly cropped by the frame, sits a steel "
        "workbench carrying real used hardware: a scuffed aluminium tool "
        "tray, loose socket drivers and a torque wrench with worn chrome, a "
        "coil of laced cable held by a plain cable tie, a folded anti-static "
        "bag and a roll of plain grey tape, all of it marked up with genuine "
        "grime, fingerprint smudges and scuffs, no lettering anywhere. "
        "Beyond it in the centre mid-ground stands the spacecraft itself on "
        "a low plain steel integration stand: a compact boxy bus about the "
        "size of a refrigerator, some panels bare brushed aluminium with "
        "visible fastener rows and laced wiring harnesses, other faces "
        "loosely draped in crinkled silver multilayer thermal blanket that "
        "creases and buckles in the work light, one large rectangular solar "
        "array panel leaning vertically in a shallow padded cradle beside "
        "it showing its dark blue-black cell face and fine seams, all plain "
        "and completely unmarked. Standing at the spacecraft, seen from "
        "behind and in three-quarter view, are two workers in white "
        "full-body cleanroom suits with hoods, face masks and gloves, one "
        "with both gloved hands on a blanket edge taping it down, the other "
        "kneeling to a bolted bracket, both mid-task with faces turned away "
        "and not identifiable. The high bay recedes behind them into warm "
        "haze with the pale flanks of more integration stands, a coiled "
        "hose on the floor, a pallet of plain crated parts and a "
        "plastic-sheeted partition, all dissolving into creamy bokeh. There "
        "is not a single screen, monitor, display, panel computer, laptop, "
        "tablet or control panel anywhere in the frame. Warm practical work "
        "lighting from high overhead fixtures with uneven mixed colour "
        "temperature, hot pools and dull corners, honest shadows, the worn "
        "epoxy floor holding soft greasy reflections of the stand legs and "
        "a few scattered dust motes drifting in the light shafts. Slightly "
        "crooked handheld framing, visible ISO grain in the shadows, natural "
        "camera noise, very slight film grain, soft lens flare from one "
        "high lamp, faint chromatic fringing on high-contrast edges, "
        "imperfect and unretouched, no plastic CGI sheen, no glossy render, "
        "no perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # 6 — orbital, re-rolled through a spacecraft window: glass reflections and
    #     a blurred foreground structure anchor it as a real photograph. Added
    #     after six orbital/cleanroom rolls all came back "render/CGI"; schnell
    #     smooths featureless black space, and foreground occlusion plus window
    #     artefacts are the strongest available photographic cues in orbit.
    "6": (
        "A real documentary photograph taken by an astronaut on a real camera, "
        "not a render and not computer generated, shot handheld on a 50mm lens "
        "at f/1.8 through the thick glass window of a spacecraft, looking out "
        "at a small satellite in orbit above the Earth. In the near foreground "
        "and completely out of focus, framing the shot at the left and top of "
        "frame, sit the layered scratch-marked glass of the window itself with "
        "a couple of real internal glass reflections ghosted across the "
        "centre, flanked by a blurred piece of the window's surrounding "
        "structure and a soft dark cable loop. Beyond the glass, tack sharp in "
        "the centre of frame, hangs a small compact satellite spacecraft: a "
        "boxy bus about the size of a refrigerator, its plain bare machined "
        "aluminium panels and riveted frame entirely unmarked, wrapped across "
        "much of its sunward face in crinkled silver-gold multilayer thermal "
        "blanket that buckles and folds under hard raw sunlight, small plain "
        "thruster nozzles and a folded antenna mast along its upper edge, "
        "laced wiring harnesses running neatly along one flank, no markings, "
        "no insignia, no lettering on any surface. Two long solar array wings "
        "extend from it, their dark blue-black cell faces glossy with fine "
        "seams, one wing raking into a harsh specular streak of sunlight, "
        "both casting thin hard shadows across the spacecraft body. Its "
        "lighting is entirely raw unfiltered sun: one face blown out white "
        "with clipped highlights, the rest crushed into dense black shadow "
        "with no fill light at all. Below the spacecraft the curved limb of "
        "the Earth rolls away, sunlit white cloud tops and deep blue ocean "
        "slipping into a thin luminous pale cyan band of atmosphere along the "
        "horizon and then into darkness at the terminator, the whole planet "
        "surface softened by real optical defocus. The upper part of the "
        "frame is black space with faint sensor noise and a sparse scatter of "
        "dim stars. Slightly crooked handheld framing, the horizon tilted a "
        "degree or two off level, uneven corner illumination, subtle lens "
        "vignette, faint chromatic fringing on the bright limb edge, mild "
        "sensor grain and a little camera shake, honest available-light "
        "exposure, no studio lighting, no rim light, no even illumination, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    # 7 — FALLBACK, human-centred: technicians actively working the spacecraft in
    #     a high bay. Amkor (the repo's proven "photo" pass) is carried by the
    #     workers, so here the suited crew is prominent in frame rather than the
    #     hardware being the sole hero.
    "7": (
        "A real documentary photograph taken by a photojournalist on a real "
        "camera, not a render and not computer generated, shot on a 35mm lens "
        "at f/2.0 on a full-frame camera, inside a spacecraft integration high "
        "bay during the final build of a small satellite. The frame is carried "
        "by two workers caught mid-task, prominent in the centre mid-ground: "
        "one in a white full-body cleanroom suit with hood, face mask, safety "
        "glasses and white gloves, leaning in with both gloved hands "
        "smoothing and pressing down the edge of a crinkled silver multilayer "
        "thermal blanket across the flank of a compact boxy spacecraft bus "
        "about the size of a refrigerator that stands on a low plain steel "
        "integration stand, the blanket creasing and buckling under their "
        "hands; the second worker crouches lower beside the stand with a "
        "gloved hand on a plain bolted bracket, mid-turn away from the camera "
        "with their face hidden, plain unmarked white suit, no name badge, no "
        "lanyard, no lettering anywhere on any garment. The spacecraft behind "
        "them is plain bare machined aluminium with visible fastener rows and "
        "laced wiring harnesses, and a large rectangular solar array panel "
        "leans vertically in a padded cradle to the right showing its dark "
        "blue-black cell face and fine panel seams, all of it unmarked. In "
        "the sharp left foreground, partly cropped by frame, a steel bench "
        "holds real used hand tools on a scuffed tray, a coil of laced cable "
        "and a folded anti-static bag, all grimy and fingerprinted. The bay "
        "recedes into warm haze with more integration stands, a coiled hose "
        "on the floor and a plastic-sheeted partition dissolving into creamy "
        "bokeh behind them. There is no screen, monitor, laptop, tablet or "
        "control panel anywhere in the frame. There are no cardboard boxes, "
        "no shipping cartons, no packing crates, no wooden pallets with "
        "goods, no packing tape, no tape of any colour, no red or white "
        "striped tape, no adhesive labels, no shipping labels, no warning "
        "stickers, no decals and no placards anywhere in the frame, and every "
        "single object, panel and surface in the picture is completely bare, "
        "plain and unmarked with nothing printed, stuck, taped or written on "
        "it. Warm practical overhead work lighting with mixed colour "
        "temperature, hot pools and dull corners, "
        "honest shadows, dust motes drifting in the light shafts, the worn "
        "epoxy floor holding soft greasy reflections. Slightly crooked "
        "handheld framing, visible ISO grain in the shadows, natural camera "
        "noise, slight film grain, soft lens flare, faint chromatic fringing, "
        "imperfect unretouched available light, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # 8 — orbital via the framing real orbital photography actually uses: a long
    #     lens, the Earth filling the frame, the spacecraft small and hard-lit
    #     against an overexposed limb with sun glint and haze.
    "8": (
        "A real documentary photograph taken by a photojournalist on a real "
        "camera, not a render and not computer generated, shot from a nearby "
        "spacecraft on a long 200mm lens at f/4, of a small satellite "
        "spacecraft flying high above the Earth. The Earth dominates the "
        "lower two thirds of the frame, filling it edge to edge and slightly "
        "overexposed: an enormous curved sweep of sunlit cloud tops in white "
        "and pale grey over deep blue ocean, a brilliant specular sun glint "
        "burning a white highlight off the water in the lower right, a broad "
        "hazy pale cyan-white band of atmosphere along the limb curve, and "
        "the surface detail softened by real atmospheric haze and optical "
        "defocus so it reads naturally soft and low-contrast with a faint "
        "dull brown-grey tint in the shadowed parts of the cloud. Against "
        "that huge bright backdrop, small in the upper middle of frame and "
        "tack sharp, drifts a compact boxy satellite spacecraft about the "
        "size of a refrigerator: bare machined aluminium and composite "
        "panels with visible fastener rows, part of its sunward face draped "
        "in crinkled silver-gold multilayer thermal blanket folding hard "
        "under a raw sun that blows out one side of the body into clipped "
        "white highlights while the rest falls into dense black shadow with "
        "absolutely no fill light, small plain thruster nozzles and a folded "
        "antenna mast along its upper edge, laced wiring harnesses along one "
        "flank, and two long solar array wings extending from it, their dark "
        "blue-black cell faces glossy with fine seams, one wing catching a "
        "hard specular streak of light. Every surface of the spacecraft is "
        "plain and completely unmarked, and the upper band of the frame above "
        "it is black space with heavy visible sensor noise and a sparse "
        "scatter of dim stars. Slightly crooked handheld framing with the "
        "horizon tilted a degree or two off level, strong natural lens "
        "vignette, uneven corner illumination, faint chromatic fringing "
        "along the bright limb, visible ISO grain in the shadows, a little "
        "camera shake, honest available-light exposure, no studio lighting, "
        "no rim light, no even illumination, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. " + NO_TEXT
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
    img = img.convert("RGB")
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
    print(f"MD5 {os.popen('md5sum ' + OUTPUT).read().strip()}")


if __name__ == "__main__":
    main()
