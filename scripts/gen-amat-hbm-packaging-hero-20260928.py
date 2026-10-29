#!/usr/bin/env python3
"""Generate hero for amat-hbm-packaging-memory-capex-cycle-2026 (fal flux/schnell).

Subject: Applied Materials (NASDAQ: AMAT) — the semiconductor-equipment maker
whose deposition / etch / CMP / ion-implant tools (and now advanced packaging
and hybrid bonding) are the chokepoint behind AI memory (HBM) supply.
Article thesis: the equipment capex cycle behind the AI memory build-out.

Scene chosen: a semiconductor fab CLEANROOM interior — an engineer in a full
white bunny-suit handling a FOUP (front-opening unified pod) of silicon wafers
beside a large wafer-processing tool, warm amber-tinged cleanroom glow plus
cool white machine light, shallow depth of field.

Deliberately DISTINCT from the recent heroes that must not repeat:
  (1) memory-article macro of a bare silicon wafer with dicing coolant (Micron,
      today) — this one is NOT a wafer macro.
  (2) data-center / server aisle, offshore wind, rocket launch pad,
      office-productivity scene.
This one is a human/tool cleanroom documentary moment, no macro.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/HUD.
- TEXT-FREE: fab gear naturally carries printed markings, brand names, labels,
  barcodes, screen readouts and watermarks — all explicitly forbidden.
- NO data-center hallway / server-aisle / rack composition (banned).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-amat-hbm-packaging-hero-20260928.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amat-hbm-packaging-memory-capex-cycle-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no "
    "numbers, no codes, no serial numbers, no part numbers, no printed "
    "markings, no silkscreen lettering, no stencilled characters, no labels, "
    "no stickers, no barcodes, no QR codes, no warning decals, no HAZMAT "
    "legends, no country-of-origin stamps, no brand names, no manufacturer "
    "names, no company logos, no model designations, no instrument readouts, "
    "no gauges with digits, no screens, no display panels, no dials, no "
    "signage, no wall signs, no badges, no name tags, no watermark, no "
    "signature, no captions, no legible writing of any kind anywhere in the "
    "image. The machinery is plain unlabelled brushed stainless steel and "
    "matte grey panelwork, the pods and carriers are plain unbranded plastic, "
    "everything perfectly clean and blank. No illustration, no digital art, "
    "no cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no futuristic HUD graphics, "
    "no holograms, no overlay elements, no augmented-reality graphics, no "
    "charts, no graphs, no diagrams. Not a data-center hallway, no server "
    "aisle, no server racks, no rack of blinking network equipment, no cable "
    "runs, no rows of cabinets, no office, no people in street clothes."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: an interior view of a modern semiconductor fabrication "
        "cleanroom. A single engineer dressed head to toe in a full white "
        "cleanroom coverall with hood, face mask, safety glasses and white "
        "gloves stands at the load port of a large enclosed wafer-processing "
        "tool, holding a wafer carrier pod of silicon wafers with both hands "
        "and lowering it onto the tool's open load port. The engineer is seen "
        "in profile from a few metres away, one clear subject, facing the "
        "machine. The tool is a big plain stainless-steel and grey-panel "
        "enclosed cabinet with a recessed load-port opening, thin metal "
        "framing and no markings at all. The cleanroom around it is bright "
        "and pale: a white ceiling with soft luminous panels, a cream "
        "epoxy floor with a faint reflection, plain unmarked wall panels and "
        "a glass window into the next bay, all softly out of focus. Warm "
        "amber-tinged overhead cleanroom light fills the room and gives the "
        "white coverall and pale surfaces a gentle golden cast, with a cool "
        "white machine light glowing from the tool's load port and rimming "
        "the pod; gentle warm-and-cool contrast, nothing else self-lit. Very "
        "shallow depth of field on an 85mm lens at f/2: the engineer's "
        "gloved hands, the pod and the load-port mouth are tack sharp, the "
        "tool body and the cleanroom ceiling and floor melt into smooth "
        "creamy bokeh, nothing readable in the background. Natural camera "
        "noise and very slight film grain, subtle lens vignette, honest "
        "realistic fabric and brushed-metal texture, fine dust-free crisp "
        "clean air, professional documentary semiconductor-industry "
        "photography, extremely detailed, photorealistic, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph, shot on a fast prime lens, not computer "
        "generated: an authentic semiconductor-industry press photo inside a "
        "wafer fab cleanroom. One technician in a full white bunny suit — "
        "coverall, hood, mask, goggles and white gloves — stands beside a "
        "large wafer-processing machine, both hands lifting a front-opening "
        "wafer pod of stacked bare silicon wafers and guiding it into the "
        "machine's loading bay. The technician is framed from the waist up, "
        "seen three-quarters from behind and to the side so the face is not "
        "the subject; the pod of wafers is the brightest thing in the frame "
        "and the wafer edges catch the light in thin pale lines. The machine "
        "is a tall plain enclosed tool of brushed stainless steel with matte "
        "grey doors, a recessed dark load-port mouth and plain unmarked "
        "operator panel, softly out of focus. Cleanroom interior behind: pale "
        "white ceiling panels, soft luminous ceiling light, a plain wall and "
        "a window, all dissolving into a bright blur. Warm amber-tinged "
        "ceiling light washes the white suit and the pale room with a golden "
        "tint while a cool white light from inside the tool's load port "
        "rims the pod, gentle warm-and-cool contrast, nothing else glowing. "
        "Shallow depth of field at f/2 on an 85mm lens: the gloved hands and "
        "the wafer pod tack sharp, the tool and the background melting into "
        "smooth creamy bokeh with no readable detail. Natural sensor noise, "
        "very slight film grain, subtle vignette, realistic fabric, glove and "
        "metal texture, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, extremely high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: two cleanroom workers in full white bunny suits at an "
        "inspection station inside a semiconductor fab, one leaning slightly "
        "forward over a matte grey inspection bench examining a bare silicon "
        "wafer held up in gloved hands, the other standing just behind at a "
        "large plain enclosed wafer tool. Seen from the side at medium "
        "distance, one clear subject, faces covered by masks and hoods. The "
        "wafer in the gloved hands is a plain pale grey mirror disc, blank, "
        "catching a soft warm highlight along its edge, no printing on it. "
        "The bench and the tool are plain unlabelled brushed stainless and "
        "matte grey panel with a recessed dark opening, softly out of focus. "
        "The cleanroom is bright and pale: white ceiling with luminous "
        "panels, cream epoxy floor with a faint sheen, plain unmarked wall "
        "panels. Warm amber-tinged overhead cleanroom light bathes the white "
        "suits and the pale room with a golden cast, cool white light from "
        "the tool's opening balances the frame, gentle warm-and-cool "
        "contrast, nothing self-illuminated. Very shallow depth of field on "
        "an 85mm lens at f/2: the gloved hands and the wafer tack sharp, the "
        "bench, the tool and the far cleanroom melting into smooth creamy "
        "bokeh with nothing readable, no signage, no screens. Natural camera "
        "noise and very slight film grain, subtle lens vignette, honest "
        "realistic texture on suit and steel, crisp clean air, professional "
        "documentary semiconductor-industry photography, extremely detailed, "
        "photorealistic, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a wide-ish but shallow-focus view down a semiconductor "
        "cleanroom bay. In the near foreground, seen from the side, an "
        "engineer in a full white cleanroom coverall, hood, mask and gloves "
        "is closing the clear front door of a wafer carrier pod seated in the "
        "load port of a big enclosed wafer-processing tool, one gloved hand "
        "on the pod handling handle. The pod's clear shell shows the stacked "
        "edges of bare silicon wafers as thin pale lines inside. The tool is "
        "a large plain brushed-stainless and matte grey cabinet with a "
        "recessed load-port niche and completely blank panels. Beyond, the "
        "cleanroom recedes out of focus: white luminous ceiling, pale floor, "
        "another opaque tool and a plain wall, all unreadable in the blur. "
        "Warm amber-tinged ceiling light fills the bay and tints the white "
        "suit and pale surfaces gold, while a cool white glow from the "
        "tool's load port rims the pod and the engineer's gloved arm; gentle "
        "warm-and-cool contrast, no other light source. Very shallow depth "
        "of field on an 85mm lens at f/2: the gloved hand, the pod door and "
        "the pod's wafer edges tack sharp, everything else in creamy smooth "
        "bokeh with nothing readable, no signage, no screens, no text. "
        "Natural camera noise, very slight film grain, subtle lens vignette, "
        "realistic plastic, glove and steel texture, no CGI look, no glossy "
        "render, no perfect symmetry, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "A genuine photograph, not a render and not computer generated: a "
        "semiconductor fab cleanroom at work. Framed medium-close from the "
        "side, a lone engineer in a full white bunny suit with hood, mask, "
        "goggles and white gloves stands at a large plain wafer-processing "
        "tool, both gloved hands steadying a wafer carrier pod against the "
        "tool's open load port as it seats into place. The pod is a plain "
        "unbranded pale plastic shell and its clear front shows the stacked "
        "rims of bare silicon wafers as delicate pale arcs inside. The tool "
        "is a tall brushed-stainless cabinet with matte grey doors and a "
        "dark recessed port opening, no labels anywhere. Behind, the "
        "cleanroom blurs out: luminous white ceiling panels, pale cream "
        "floor, plain wall, a hint of another machine, nothing readable. "
        "Warm amber-tinged overhead light wraps the white suit and the pale "
        "room in a soft golden haze, a cool white light from the tool port "
        "chisels the engineer's shoulder and the pod edge, gentle "
        "warm-and-cool contrast, no other light emitted. Extremely shallow "
        "depth of field on an 85mm lens wide open: the gloved hands, the pod "
        "and the load-port mouth tack sharp, everything else melting into "
        "smooth creamy bokeh with no text and no detail readable. Natural "
        "camera noise and very slight film grain, subtle vignette, honest "
        "realistic glove, plastic and brushed-metal texture, no plastic CGI "
        "sheen, no glossy render, no perfect symmetry, no 3D visualisation, "
        "no digital illustration, photorealistic, high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "7": (
        "A real close-up photograph taken with a fast 85mm lens, not a "
        "render and not computer generated: inside a bright semiconductor "
        "cleanroom, an engineer in a full white cleanroom suit — hood, face "
        "mask, safety glasses, white gloves — guides a front-opening wafer "
        "pod of bare silicon wafers into the load port of a large enclosed "
        "wafer tool, seen at medium-close range from a three-quarter angle. "
        "The pod is plain unbranded translucent plastic and the polished "
        "wafer edges inside catch the light as fine pale lines; the tool is "
        "brushed stainless steel and matte grey with a deep dark port niche "
        "and blank panels. The cleanroom recedes out of focus behind: white "
        "luminous ceiling, pale floor, a plain unmarked wall. Warm "
        "amber-tinged ceiling lighting gives the whole cleanroom a soft "
        "golden cast, and a cool white light from the tool opening rims the "
        "engineer's arm and the pod, gentle warm-and-cool colour contrast, "
        "nothing else emitting light. Very shallow depth of field: the "
        "gloved hands, the pod and the port mouth tack sharp while the tool "
        "and the room dissolve into creamy bokeh with nothing readable, no "
        "signage, no screens, no text. Natural camera noise, very slight "
        "film grain, subtle lens vignette, realistic fabric, plastic and "
        "metal texture, fine detail, no CGI sheen, no glossy render, no "
        "perfect symmetry, no digital illustration, photorealistic, "
        "professional documentary semiconductor-industry photography, 16:9 "
        "landscape composition. "
        + NO_TEXT
    ),
    "8": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera at medium distance inside a semiconductor fab cleanroom: an "
        "engineer in a full white coverall suit with hood, mask and white "
        "gloves stands beside a long row of large enclosed wafer-processing "
        "tools, turning with a wafer carrier pod of bare silicon wafers "
        "carried carefully in both hands. The engineer is seen from behind "
        "and to the side, walking away down the bay, one clear subject, the "
        "bright pod and its thin wafer edges the focal point. The tools are "
        "plain brushed stainless steel and matte grey front panels, "
        "completely unlabelled, with dark recessed load-port niches, "
        "running away down the bay and melting into blur. The cleanroom is "
        "bright and pale: white luminous ceiling, cream epoxy floor with a "
        "faint reflection, plain unmarked walls. Warm amber-tinged overhead "
        "light washes the white suit and the pale corridor with a golden "
        "tint, cool white light spills from the tools' ports in soft glows, "
        "gentle warm-and-cool contrast. Shallow depth of field on an 85mm "
        "lens at f/2: the gloved hands and the pod tack sharp, the row of "
        "tools and the ceiling dissolving into smooth creamy bokeh with "
        "nothing readable, no signage, no screens, no text anywhere. "
        "Natural camera noise, very slight film grain, subtle vignette, "
        "realistic fabric and brushed-metal texture, no CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, extremely high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "9": (
        "A real photograph, not a render: a semiconductor fab cleanroom "
        "where an engineer in a full white bunny suit, hood, mask, goggles "
        "and gloves leans over a matte grey inspection bench, holding a bare "
        "300mm silicon wafer up in both gloved hands and examining it under "
        "the light. Framed medium-close in profile from the side, one clear "
        "subject, face covered. The wafer is a plain pale grey mirror disc "
        "with a soft warm highlight sweeping across its polished face and no "
        "printing of any kind. Behind, a large plain enclosed wafer tool in "
        "brushed stainless steel and blank matte grey panels is softly out "
        "of focus, and the cleanroom recedes: white luminous ceiling, pale "
        "floor, plain unmarked wall. Warm amber-tinged overhead cleanroom "
        "light bathes the white suit and the pale room with a golden cast, "
        "a cooler white light from the tool's port balances the frame, "
        "gentle warm-and-cool contrast, nothing self-illuminated. Extremely "
        "shallow depth of field on an 85mm lens at f/2: the gloved hands and "
        "the wafer tack sharp, the bench, the tool and the room melting into "
        "creamy bokeh with nothing readable, no signage, no screens, no "
        "text. Natural camera noise and very slight film grain, subtle lens "
        "vignette, honest realistic glove, suit and polished-silicon "
        "texture, crisp clean air, professional documentary "
        "semiconductor-industry photography, extremely detailed, "
        "photorealistic, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "10": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a semiconductor fab cleanroom interior seen from a slightly "
        "elevated angle, the whole bay pale and luminous. An engineer in a "
        "full white cleanroom coverall with hood, mask and gloves stands at "
        "a big enclosed wafer-processing tool, one gloved hand on the tool's "
        "operator panel, the other holding a wafer carrier pod of bare "
        "silicon wafers at hip height, a single clear human subject in the "
        "middle of the frame. The tool is a large plain cabinet of brushed "
        "stainless steel and matte grey panel with a deep dark load-port "
        "niche and entirely blank surfaces. The cleanroom around it: white "
        "luminous ceiling panels, a cream epoxy floor with a soft "
        "reflection, plain unmarked wall panels, everything clean and "
        "empty. Warm amber-tinged overhead light floods the bay and tints "
        "the white suit and the pale surfaces golden, cool white light from "
        "the tool opening rims the engineer and the pod, gentle "
        "warm-and-cool contrast, nothing else emitting light. Very shallow "
        "depth of field on an 85mm lens at f/2: the engineer, the pod and "
        "the tool's load port tack sharp, the ceiling and floor and the far "
        "end of the bay melting into smooth creamy bokeh with nothing "
        "readable, no signage, no screens, no text. Natural camera noise, "
        "very slight film grain, subtle vignette, realistic suit, plastic "
        "and steel texture, no CGI look, no glossy render, no perfect "
        "symmetry, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
