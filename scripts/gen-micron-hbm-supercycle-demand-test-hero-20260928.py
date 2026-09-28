#!/usr/bin/env python3
"""Generate hero for micron-hbm-supercycle-demand-test-2026 (fal flux/schnell).

Subject: Micron Technology (NASDAQ: MU) — the US memory maker whose DRAM /
NAND / HBM (high-bandwidth memory) is stacked next to every AI accelerator.
Article thesis: the memory supercycle meeting its first real demand test.

Scene chosen (the Writer's caption describes this exact photo): a PHOTOREAL
close-up inside an industrial memory-test area — a technician's gloved hands
seating a single bare memory module down into the gold-pinned test socket of
an industrial memory-test handler, under warm amber fab light, cool fill,
very shallow depth of field. One clear subject.

Deliberately DISTINCT from the two recent heroes that must not repeat:
  (1) 9/14 MU hero  = extreme macro of bare DRAM modules + polished HBM die
      stack on a dark matte surface (dark low-key studio product shot).
  (2) 9/27 AMD hero = a fab technician in a white bunny suit holding a 300mm
      wafer beside a lithography tool load port (person + wafer, cleanroom).
This one is a tight hands-and-hardware action shot on a test handler, amber
industrial light, no full face, no bunny suit portrait, no bare-wafer-in-hand.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/HUD.
- TEXT-FREE: memory PCBs, handlers and fab gear naturally carry printed
  markings, silkscreen part numbers, brand names, labels, barcodes, screen
  readouts and watermarks — all explicitly forbidden in the prompt.
- NO data-center hallway / server-aisle / rack composition (banned).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-micron-hbm-supercycle-demand-test-hero-20260928.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "micron-hbm-supercycle-demand-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no part numbers, no printed "
    "markings, no silkscreen lettering, no stencilled characters, no labels, "
    "no stickers, no barcodes, no QR codes, no warning decals, no "
    "country-of-origin stamps, no brand names, no manufacturer names, no "
    "company logos, no model designations, no readouts, no gauges with "
    "digits, no screens, no display panels, no dials, no signage, no "
    "watermark, no signature, no captions, no legible writing of any kind "
    "anywhere in the image. The equipment is plain unlabelled brushed metal "
    "and matte black plastic, the circuit board is plain unmarked green with "
    "bare gold contacts, everything perfectly clean and blank. No "
    "illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no holograms, no overlay elements, "
    "no augmented-reality graphics. Not a data-center hallway, no server "
    "aisle, no server racks, no rack of blinking network equipment, no cable "
    "runs, no rows of cabinets."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a tight over-the-shoulder close-up of a technician's gloved "
        "hands seating a single bare computer memory module down into the "
        "gold-pinned test socket of an industrial memory-test handler. Only "
        "the hands and forearms are in frame wearing clean plain white "
        "cleanroom gloves, no face and no full figure visible. The memory "
        "module is a plain unmarked green circuit board with bare gold "
        "contact fingers and plain black chip packages, held at a slight "
        "angle just above the open metal test socket, its gold edge already "
        "entering the socket jaws with tiny mechanical clamps on either side. "
        "The handler below and around the socket is matte black machined "
        "aluminium with brushed metal guide rails and small precision hex "
        "screws, softly out of focus. Warm amber industrial fab light rakes "
        "in from the upper right across the hands and the module, with a "
        "cool blue-white fill from the left, gentle amber-and-cool contrast. "
        "Very shallow depth of field: the near contact fingers of the module "
        "and the gloved fingertips are tack sharp, the socket jaws and the "
        "handler behind melt into smooth creamy bokeh, and the dark factory "
        "background dissolves into deep warm shadow with faint out-of-focus "
        "light bokeh only, no walls and no room readable. Shot on an 85mm "
        "lens at f/1.8, real optical bokeh, natural camera noise and very "
        "slight film grain, subtle lens vignette, honest realistic material "
        "textures on the gloves and metal, fine dust specks, professional "
        "moody editorial lighting, extremely detailed, photorealistic "
        "documentary technology photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph, shot on a fast prime lens, not computer "
        "generated: an authentic technology-industry press photo of the "
        "moment a bare memory module is pressed down into an industrial "
        "memory-test handler's test socket. Framed close on the action: a "
        "cleanroom-gloved hand from the right holds a plain unmarked green "
        "memory circuit board with bare gold contact fingers and plain black "
        "chip packages, easing its gold edge into the open gold-lined jaws "
        "of a heavy machined metal socket. The test handler beneath is matte "
        "black anodised aluminium with brushed steel rails, small screws and "
        "fine mechanical detail, thrown softly out of focus. Warm amber task "
        "lighting from the upper right bathes the hands and the metal in a "
        "golden glow while a cooler white light from the rear left rims the "
        "module edge, gentle warm-and-cool contrast. Very shallow depth of "
        "field, 85mm lens wide open: the gold fingers and gloved fingertips "
        "tack sharp, everything behind melting into soft creamy bokeh, the "
        "dark workshop interior falling away into deep underexposed shadow "
        "with only faint blurred highlights, no walls, no room, no racks. "
        "Honest available-style moody lighting, natural sensor noise, very "
        "slight film grain, fine dust and handling micro-marks on the metal, "
        "subtle vignette, real optical blur, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A real close-up photograph taken with a fast 85mm lens, not a "
        "render and not computer generated: a technician's cleanroom-gloved "
        "hands lower a single bare memory module into the open test socket "
        "of an industrial memory-test handler. The green circuit board is "
        "plain and unmarked with bare gold contact fingers and plain black "
        "chip packages; the socket is machined matte-black metal lined with "
        "gold spring pins, mounted on a heavy brushed-aluminium handler "
        "fixture. No face, no badge, no name tag, just the gloved hands and "
        "forearms entering frame from the upper left. Warm amber industrial "
        "light from the right and a cool white key from the left, warm "
        "highlights on the metal and cool shadow, gentle colour contrast. "
        "Extremely shallow depth of field: a narrow band of the module edge "
        "and gloved fingertips in crisp focus, the handler and the dark "
        "factory behind dissolving into smooth creamy bokeh, background a "
        "deep warm shadow with nothing readable in it, no room, no racks, no "
        "screens. Available-style underexposed moody lighting, natural "
        "camera noise and very slight film grain, faint dust particles, "
        "subtle lens vignette, real optical blur, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: a close, low-angle shot of a bare computer memory module "
        "being seated into the gold contact socket of an industrial "
        "memory-test handler at a chip factory. A cleanroom-gloved hand "
        "steadying the plain unmarked green circuit board with bare gold "
        "contact fingers and plain black chip packages, the module angled "
        "down into the open metal socket, mechanical clamp arms on each "
        "side. The handler body is matte black machined metal with brushed "
        "steel rails and fine fasteners, mostly out of focus. Warm amber fab "
        "light from the upper right, cool white fill from the left, soft "
        "warm highlights on gold and brushed metal. Very shallow depth of "
        "field on an 85mm lens at f/1.8: the module's gold edge and gloved "
        "fingertips tack sharp, the machine and the dark industrial "
        "background melting into creamy out-of-focus bokeh with faint warm "
        "light spots only, no walls, no racks, nothing else readable. "
        "Honest moody underexposed lighting, natural camera noise, slight "
        "film grain, fine dust and tooling marks on the metal, subtle "
        "vignette, real optical blur, no CGI look, no glossy render, no "
        "perfect symmetry, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a tight close-up of a technician's gloved hands lowering a "
        "single bare computer memory module EDGE-ON into the gold-pinned "
        "test socket of an industrial memory-test handler. The module is "
        "held nearly vertical and seen almost exactly edge-on, so only its "
        "thin edge and its row of bare gold contact fingers face the camera "
        "— the broad flat faces of the circuit board are turned away from "
        "the lens and are not visible in the frame. Only cleanroom-gloved "
        "fingertips and part of the glove are in frame, no face, no body, no "
        "badge. Below, the open machined matte-black socket jaws with tiny "
        "gold spring contacts and a brushed-aluminium handler plate with "
        "fine hex screws sit softly out of focus. Warm amber industrial fab "
        "light rakes in from the upper right across the gold fingers and the "
        "glove, soft cool white fill from the left, gentle amber-and-cool "
        "contrast, no light emitting from the equipment itself. Extremely "
        "shallow depth of field: a thin band of gold contact fingers and "
        "gloved fingertip tack sharp, everything else melting into smooth "
        "creamy bokeh, dark warm-shadow background with only faint blurred "
        "highlights, no walls, no room, no racks readable. Shot on an 85mm "
        "lens at f/1.8, real optical bokeh, natural camera noise and very "
        "slight film grain, subtle lens vignette, honest realistic glove and "
        "metal texture, fine dust specks, professional moody editorial "
        "lighting, extremely detailed, photorealistic documentary technology "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "7": (
        "A real photograph shot on a fast 85mm prime, not a render and not "
        "computer generated: an authentic semiconductor-industry press photo "
        "of the instant a bare memory module is seated down into an "
        "industrial memory-test handler socket. Framed tight and nearly "
        "edge-on to the module so the camera sees its thin side profile and "
        "its row of bare gold contact fingers only, the broad flat green "
        "faces of the board angled away and out of view. A cleanroom-gloved "
        "fingertip steadies the top of the module, the glove crisp and "
        "textured in the foreground. The socket is machined matte-black "
        "metal with tiny gold spring pins, mounted in a heavy "
        "brushed-aluminium handler fixture with fine fasteners, all thrown "
        "softly out of focus behind. Warm amber task light from the upper "
        "right gilds the gold contacts and the glove; a cool white fill from "
        "the left rims the module edge; gentle warm-and-cool contrast and no "
        "self-illuminated parts anywhere. Very shallow depth of field, 85mm "
        "wide open: the gold fingers and gloved fingertip tack sharp, "
        "everything behind melting into smooth creamy bokeh, the dark "
        "workshop interior falling into deep underexposed shadow with only "
        "faint blurred warm highlights, no walls, no room, no racks. Honest "
        "available-style moody lighting, natural sensor noise, very slight "
        "film grain, subtle vignette, real optical blur, no CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "8": (
        "A real close-up photograph taken with a fast 85mm lens, not a "
        "render and not computer generated: a gloved hand guiding a bare "
        "memory module edge-first into the open gold-lined test socket of an "
        "industrial memory-test handler. The camera looks along the thin "
        "edge of the module, so the frame shows the narrow board side and "
        "the bare gold contact fingers and almost nothing of the flat board "
        "surfaces. The socket is machined matte-black metal studded with "
        "tiny gold spring pins on a heavy brushed-aluminium fixture with "
        "fine screws, softly out of focus. Just cleanroom-gloved hands and "
        "forearms enter frame from the upper left, no face, no badge, no "
        "name tag. Warm amber industrial light from the right and a cool "
        "white key from the left, warm highlights on gold and metal, cool "
        "shadow, gentle colour contrast, nothing glowing on the machine. "
        "Extremely shallow depth of field: a narrow band of the module's "
        "gold edge and gloved fingertips in crisp focus, the handler and the "
        "dark factory behind dissolving into smooth creamy bokeh, background "
        "a deep warm shadow with nothing readable in it, no room, no racks, "
        "no screens. Available-style underexposed moody lighting, natural "
        "camera noise and very slight film grain, faint dust particles, "
        "subtle lens vignette, real optical blur, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "9": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: a low, tight angle on a memory module being pressed "
        "edge-first into the gold contact jaws of an industrial memory-test "
        "handler socket. Because the module is seen along its thin edge, the "
        "frame holds only the narrow side of the bare board and its row of "
        "gleaming gold contact fingers, plus a single cleanroom-gloved "
        "fingertip pressing the top corner down. The socket is heavy "
        "machined matte-black metal with fine gold spring contacts in a "
        "brushed-aluminium handler plate, softly out of focus. Warm amber "
        "fab light from the upper right, cool white fill from the left, soft "
        "warm highlights on gold and brushed metal, no glowing parts. Very "
        "shallow depth of field on an 85mm lens at f/1.8: the gold fingers "
        "and gloved fingertip tack sharp, the machine and the dark "
        "industrial background melting into creamy out-of-focus bokeh with "
        "faint warm light spots only, no walls, no racks, nothing else "
        "readable. Honest moody underexposed lighting, natural camera noise, "
        "slight film grain, fine dust and tooling marks on the metal, subtle "
        "vignette, real optical blur, no CGI look, no glossy render, no "
        "perfect symmetry, no digital illustration, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "10": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a close-up of a front-opening wafer carrier pod on a "
        "cleanroom workbench, its clear front door open and its internal "
        "slots filled with bare 300mm silicon memory wafers. Each bare wafer "
        "is plain mirror-polished grey-blue silicon with only a fine faint "
        "grid of rectangular die outlines, no printing of any kind on the "
        "wafer surfaces. The camera looks slightly down and along the stack "
        "of wafers so their thin polished edges catch the light in soft "
        "horizontal bands that recede into the dark. Bright cool cleanroom "
        "lighting from above and behind rims the wafer edges with a clean "
        "white glow while a warm amber accent light comes from the left, "
        "gentle cool-and-warm contrast, nothing self-illuminated. Very "
        "shallow depth of field on an 85mm lens at f/2: the nearest wafer "
        "edge tack sharp, the rest of the stack and pod melting into smooth "
        "creamy bokeh, the cleanroom background dissolving into a soft pale "
        "grey blur with no equipment readable, no walls, no racks, no "
        "screens. Honest realistic material texture, natural camera noise "
        "and very slight film grain, subtle vignette, fine dust motes in the "
        "air catching the light, professional editorial lighting, extremely "
        "detailed, photorealistic documentary semiconductor-industry "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "11": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a tight macro shot of a wafer-dicing operation cutting "
        "individual memory dies from a bare silicon wafer. A thin circular "
        "dicing blade with a fine abrasive rim bites into the plain "
        "mirror-polished grey silicon wafer, throwing a delicate arc of fine "
        "coolant water droplets and a small spray mist into the air, wet "
        "streaks glistening on the bare silicon surface beside the cut. The "
        "wafer shows only a faint grid of rectangular die outlines, fully "
        "plain and unmarked with no printing on its surface; the chuck "
        "beneath is matte black metal, softly out of focus. Cool white "
        "machine light from above makes the water spray sparkle while a warm "
        "amber accent light from the right edges the blade, gentle "
        "cool-and-warm contrast, nothing glowing. Very shallow depth of "
        "field on a 100mm macro lens at f/2.8: the blade edge and the cut "
        "line tack sharp with visible fine silicon texture and glinting "
        "water, the machine and the dark interior melting into smooth creamy "
        "bokeh, no walls, no racks, no panels readable. Honest realistic wet "
        "surfaces, natural camera noise and very slight film grain, subtle "
        "vignette, real optical blur, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "12": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a tight macro shot of a semiconductor wafer dicing saw "
        "cutting a bare 300mm memory wafer. The frame is dominated by the "
        "bare silicon wafer surface, which is a pale grey mirror, and the "
        "fine grid of hundreds of identical tiny rectangular chip dies is "
        "clearly visible across it, like a checkerboard of small pale "
        "squares separated by hair-thin lanes, completely plain and unmarked "
        "with no printing of any kind. A thin circular diamond dicing blade "
        "with a fine abrasive rim descends into a cut lane, and a delicate "
        "arc of clear coolant water droplets sprays up from the cut, mist "
        "and a thin wet trail glistening along the lane. Cool white machine "
        "light from above makes the water sparkle and reveals the subtle die "
        "grid, a warm amber accent light from the right edges the blade, "
        "gentle cool-and-warm contrast. Very shallow depth of field on a "
        "100mm macro lens at f/2.8: the blade edge, the cut lane and a few "
        "nearest dies tack sharp with fine silicon texture and glinting "
        "water, the far edge of the wafer and the dark machine interior "
        "melting into smooth creamy bokeh, no panels, no screens, no walls, "
        "no racks readable. Honest realistic wet silicon, natural camera "
        "noise and very slight film grain, subtle vignette, real optical "
        "blur, no plastic CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, "
        "extremely high detail, professional editorial stock photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "13": (
        "A real photograph taken with a macro lens, not a render and not "
        "computer generated: a close view of a bare 300mm memory wafer held "
        "on a matte black vacuum chuck in a semiconductor singulation tool, "
        "while a thin circular dicing blade with a fine abrasive rim cuts "
        "along one of the hair-thin lanes between the dies. The wafer is "
        "pale grey polished silicon whose surface is covered in a neat field "
        "of thousands of identical tiny rectangular dies arranged in a "
        "perfect grid, the grid clearly readable as a semiconductor wafer, "
        "with no printing, no text and no markings anywhere on the silicon. "
        "Fine coolant water sprays in a bright arc from the blade and runs "
        "in thin wet streaks along the cut, glistening under the light. Cool "
        "white machine light from the upper left and a warm amber accent "
        "from the right, gentle cool-and-warm contrast, nothing glowing. "
        "Extremely shallow depth of field: the blade tip, the cut lane and "
        "the nearest rows of dies in crisp focus with visible fine silicon "
        "texture and water droplets, everything else melting into smooth "
        "creamy bokeh, the dark tool interior a deep shadow with no panels, "
        "no screens, no racks readable. Honest realistic wet surfaces, "
        "natural camera noise and very slight film grain, faint dust, subtle "
        "lens vignette, real optical blur, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "14": (
        "Photo-realistic macro stock photograph taken with a real camera and "
        "a 100mm lens, not a render: a bare 300mm memory wafer seen at a low "
        "grazing angle on the matte black chuck of a dicing tool, its "
        "surface a pale grey mirror covered edge to edge in a flawless grid "
        "of thousands of identical tiny rectangular chip dies separated by "
        "hair-thin lanes, the die grid unmistakable, the silicon completely "
        "plain and unmarked with no text of any kind. A thin circular dicing "
        "blade with a fine abrasive rim is biting into one lane near the "
        "centre, spraying a delicate fan of clear coolant water droplets and "
        "fine mist into the dark air, wet streaks glistening along the cut "
        "and a few tiny droplets beading on the bare silicon beside it. Cool "
        "white machine light from above makes the water droplets sparkle and "
        "skims the die grid, a warm amber accent light from the right rims "
        "the blade and the droplet mist, gentle cool-and-warm contrast. Very "
        "shallow depth of field at f/2.8: the blade edge, cut lane and "
        "nearest droplets tack sharp, the wafer surface running smoothly out "
        "of focus into creamy bokeh, the surrounding tool lost in dark "
        "shadow with nothing readable in it, no panels, no screens, no "
        "walls, no racks. Honest realistic wet silicon and water, natural "
        "camera noise and very slight film grain, subtle vignette, real "
        "optical blur, no CGI sheen, no glossy render, no perfect symmetry, "
        "no digital illustration, photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "15": (
        "Photo-realistic macro stock photograph taken with a real camera and "
        "a 100mm lens, not a render: a bare 300mm memory wafer on the matte "
        "black vacuum chuck of a dicing saw, seen at a gentle angle so the "
        "round wafer edge curves across the frame. The wafer surface is pale "
        "grey polished silicon carrying a flawless grid of thousands of "
        "identical tiny rectangular dies separated by hair-thin lanes, the "
        "grid unmistakable and completely plain, with no printing, no text "
        "and no markings of any kind anywhere on the silicon. A thin "
        "circular dicing blade with a fine abrasive rim is cutting into one "
        "lane, throwing a bright delicate arc of clear coolant water "
        "droplets and fine mist into the air, thin wet streaks running along "
        "the cut and a row of tiny water beads glistening on the bare "
        "silicon beside it. The scene is lit only by soft cool white machine "
        "light from above, which makes the water sparkle and reveals the "
        "subtle die grid, with a faint warm neutral bounce from the right; "
        "nothing is self-illuminated, there is no glowing tip, no laser, no "
        "light emitted from the blade or the machine. Extremely shallow "
        "depth of field at f/2.8: the blade edge, the cut lane and the "
        "nearest water droplets tack sharp, the wafer surface running "
        "smoothly out of focus into creamy bokeh, the surrounding tool lost "
        "in dark shadow with nothing readable in it, no panels, no screens, "
        "no walls, no racks. Honest realistic wet silicon and water, natural "
        "camera noise and very slight film grain, subtle vignette, real "
        "optical blur, no CGI sheen, no glossy render, no perfect symmetry, "
        "no 3D visualisation, no digital illustration, photorealistic, "
        "extremely high detail, professional editorial stock photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "5": (
        "A genuine photograph, not a render and not computer generated: "
        "macro-close on the exact moment a plain unmarked green memory "
        "module with bare gold contact fingers and plain black chip packages "
        "is clamped down into the gold-pinned socket of an industrial "
        "memory-test handler. A gloved hand grips the top edge of the "
        "circuit board, clean plain white cleanroom glove, knit fabric "
        "texture and a faint crease visible at the wrist, no face and no "
        "body in frame. Machined matte-black metal socket jaws with tiny "
        "gold spring contacts, heavy brushed-aluminium handler plate below, "
        "fine hex screws, all softly out of focus behind the sharp module "
        "edge. Warm amber industrial light from the right grazing the gold "
        "contacts and the glove, cool white fill from the left, gentle "
        "amber-and-cool contrast. Extremely shallow depth of field, "
        "everything but a thin band of module edge and glove dissolved into "
        "smooth creamy bokeh, the dark factory interior a deep warm shadow "
        "with only faint blurred highlights, no walls, no room, no racks, "
        "no screens. Honest underexposed available-style lighting, natural "
        "camera noise and very slight film grain, tiny dust particles, "
        "subtle vignette, real optical blur, no plastic CGI sheen, no glossy "
        "render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, high detail, professional editorial "
        "stock photography, 16:9 landscape composition. "
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
