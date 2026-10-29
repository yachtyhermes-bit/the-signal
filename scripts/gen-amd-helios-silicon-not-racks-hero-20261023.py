#!/usr/bin/env python3
"""Generate hero for amd-helios-silicon-not-racks-2026 (fal flux/schnell).

Subject: AMD (Advanced Micro Devices) ramping Instinct MI400-series accelerators
and licensing the Helios rack-scale design to customers / ODMs rather than
selling finished racks. The story is silicon content and manufacturing
partners, not data-centre construction.

Scene chosen: A CLOSE-UP ON A SEMICONDUCTOR PACKAGING / ASSEMBLY BENCH — a
technician's gloved hands lifting a large AI accelerator module out of a black
antistatic tray on a stainless steel workbench, the multi-die package with its
gold interposer and stacked memory dies visible in sharp macro detail.

Deliberately NOT a data-centre hallway / server aisle / rack (banned site-wide),
NOT a server room, NOT a chiller plant, NOT neon / synthwave / glowing lines /
geometric patterns, NOT digital art, NOT 3D render or CGI, NOT abstract,
NOT a circuit-board graphic overlay.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial photograph ONLY.
- TEXT-FREE: no letters/numbers/labels/logos/signage/screens/UI anywhere.
  The package substrate and lid carry NO laser-etched or printed markings,
  no part numbers, no lot codes, no die markings, no QR / 2D matrix codes.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-amd-helios-silicon-not-racks-hero-20261023.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amd-helios-silicon-not-racks-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "lot codes, no date codes, no model numbers, no stencilled markings, no "
    "laser-etched markings, no etched lettering on the silicon, no die "
    "markings, no printed markings on the package substrate, no colour-code "
    "dots arranged as characters, no equipment nameplates, no asset tags, no "
    "warning signs, no safety posters, no bench labels, no cabinet labels, "
    "no monitor screens, no digital readouts, no control screens, no user "
    "interface, no dashboards, no software windows, no labels on trays, no "
    "printed paper, no clipboards with writing, no signage of any kind, no "
    "brand names, no manufacturer names, no company names, no corporate "
    "logos, no trademarks, no watermarks, no stickers, no decals, no "
    "barcodes, no QR codes, no two-dimensional matrix codes, no fiducial "
    "text, no handwriting, no graffiti, no legible writing of any kind "
    "anywhere in the image. The accelerator module is a completely unbranded "
    "engineering sample: its metal stiffener frame, its package substrate "
    "and its lid are plain bare metal and plain matte laminate with no "
    "etching, no engraving, no silk-screen print and no identification "
    "marks of any kind. Every silicon die face in the image is completely "
    "bare: a plain polished mirror surface with no etched characters, no "
    "die codes, no laser-scribe lettering, no wafer lot text, no tiny "
    "printed marks of any kind — only plain smooth reflective silicon and "
    "plain gold-plated trace. The technician wears plain gloves, a plain sleeve "
    "and plain clothing in solid colours with no printed patches, no "
    "embroidered names and no wordmarks. The antistatic tray, the tweezers, "
    "the vacuum pick-up tool and every instrument on the bench are plain "
    "unmarked metal and plain dark plastic with no printed legends and no "
    "branding. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no neon, no glowing lines, no light trails, no synthwave, no "
    "geometric patterns, no circuit-board graphic, no network diagram, no "
    "graph graphic, no futuristic HUD graphics, no hologram, no overlay "
    "elements, no augmented-reality graphics, no data center, no server "
    "room, no server racks, no server aisles, no cable runs, no server "
    "lights, no computer screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light industrial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, "
    "true-to-life colour, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no 3D visualisation, no digital illustration, no "
    "painting, photorealistic, very high detail, professional editorial "
    "stock photography, 16:9 landscape composition, professional lighting. "
)

PROMPTS = {
    # 1 — PRIMARY: 85mm macro, gloved hands lifting an AI accelerator module
    #     out of a black antistatic tray on a stainless workbench.
    "1": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a Nikon 85mm macro lens at f/2.8 on a full-frame camera, framed "
        "tight and low over a stainless steel assembly workbench in a "
        "semiconductor packaging and test facility. The subject fills the "
        "centre of the frame: a large AI accelerator module — a rectangular "
        "multi-die package roughly the size of a small book, its stiffener "
        "frame in brushed bare aluminium, its substrate a dark matte "
        "laminate — being lifted clear of a black carbon-filled antistatic "
        "tray. Two hands in thin pale grey nitrile cleanroom gloves cradle "
        "the module by its opposite edges, fingertips spread and pressing "
        "gently, thumbs braced on the near edge, the gloves creased and "
        "slightly powdery at the knuckles, a plain pale grey sleeve cuff "
        "entering the frame at the upper left. The module is tilted toward "
        "camera so its underside and edge catch the light: a dense array of "
        "solder bumps and a warm gold-plated interposer ring run along the "
        "visible edge, and on the upper face a row of stacked memory dies "
        "sits beside the main compute die, their polished silicon edges "
        "catching thin highlights, the die surfaces a deep mirror-dark "
        "violet-grey with faint iridescent diffraction along the bevels. "
        "Fine detail is everywhere at this distance: the matte black "
        "antistatic tray with its shallow moulded pockets and soft "
        "moulded ribs, one empty pocket where the module was lifted from, "
        "the brushed grain of the stainless bench top running left to "
        "right across the lower frame, a scatter of tiny dust specks and a "
        "single loose screw well out of focus in the near foreground. Warm "
        "industrial task lighting comes from a bench lamp above and to the "
        "left, a soft amber-white pool of light falling across the gloved "
        "hands and the gold interposer with a gentle falloff into the "
        "shadowed right side of the frame, honest specular highlights and "
        "no coloured gels. Behind, thrown far out of focus into smooth "
        "planes of dark grey and warm brown, the indistinct shapes of a "
        "bonding machine housing and a reel of tape, dissolving into creamy "
        "bokeh with nothing readable in it. Photographic, extremely shallow "
        "depth of field with the near edge of the package, the gold "
        "interposer and the gloved fingertips tack sharp and the background "
        "melting away. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — FALLBACK A: tighter top-down macro on the open package itself,
    #     lid removed, interposer and stacked dies exposed, gloved hand at edge.
    "2": (
        "Professional stock photograph, real photo not a render and not "
        "computer generated, shot on a 100mm macro lens at f/4 from directly "
        "above a stainless steel workbench in a semiconductor assembly "
        "laboratory. The frame is filled by a single large AI accelerator "
        "package lying in a black antistatic tray, its lid removed and set "
        "aside out of focus at the upper right: a rectangular multi-die "
        "assembly on a dark matte laminate substrate, the main compute die "
        "at the centre surrounded by a neat ring of eight smaller stacked "
        "high-bandwidth memory dies, all of them polished mirror-dark "
        "silicon with faint violet and green diffraction along their "
        "bevels, a thin warm gold-plated interposer trace running between "
        "the dies and the substrate edge, and a fine lattice of copper "
        "micro-bumps visible along one exposed flank. A border of tiny "
        "surface-mount capacitors and resistors lines two edges of the "
        "substrate, each a minute plain ceramic block with a bright tinned "
        "solder fillet, entirely unmarked. In the lower left of the frame a "
        "single hand in a thin pale grey nitrile cleanroom glove rests "
        "against the tray edge, two fingertips just touching the substrate "
        "corner, the glove creased at the knuckles. The tray around the "
        "package is matte black antistatic moulding with shallow ribs and a "
        "soft dusty sheen, and beyond it the brushed stainless bench top "
        "runs out of frame. Warm benchtop task light from the upper left "
        "rakes low across the assembly, lighting the gold trace and the die "
        "bevels with warm amber specular glints and leaving the near right "
        "corner in deep soft shadow. Photographic, shallow depth of field "
        "with the centre dies, the gold interposer and the nearest "
        "capacitors razor sharp, the far tray edge and background falling "
        "into creamy bokeh. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — FALLBACK B: wider bench view, technician at the assembly station
    #     with the module under a bonder, hands working, warm shop light.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated: a medium close view shot on a 50mm lens at f/2 from "
        "slightly above bench height along a semiconductor packaging and "
        "assembly workstation. A technician in a plain pale blue cleanroom "
        "smock, plain white hairnet and thin pale grey nitrile gloves stands "
        "at the bench, seen three-quarters from the side and slightly from "
        "behind so the face is turned away and mostly hidden, both hands "
        "working at a large accelerator module seated in a black antistatic "
        "tray on the brushed stainless bench: one gloved hand steadying the "
        "package edge, the other guiding a slim plain metal vacuum pick-up "
        "tool toward a stacked memory die, mid-motion and intent, not "
        "posing. The package itself is a rectangular multi-die module with a "
        "brushed aluminium stiffener frame, a dark matte laminate substrate "
        "and a row of polished silicon dies along its open face catching the "
        "light, entirely unmarked. Around it on the bench sit a plain "
        "stainless steel tweezers, a small dark plastic parts bin with a "
        "hinged plain lid, a coil of fine wire and a folded lint-free cloth, "
        "all unmarked and softly lit. Above the bench a low matte grey "
        "extractor hood and a plain bench lamp throw a warm amber-white pool "
        "of task light down onto the work surface, and the rest of the room "
        "falls away behind into soft cool shadow: the blurred pale grey "
        "cabinets of bonding and inspection equipment, a plain wall, and a "
        "distant colleague in the same plain smock moving through the far "
        "background as a soft shape. Clean, precise, quietly industrious "
        "mood, honest mixed available light with no coloured gels and no "
        "atmospheric theatrics. Photographic, moderate depth of field with "
        "the hands, the tool and the module crisp and the room softening "
        "into bokeh, real optical blur, honest exposure, natural camera "
        "noise, very slight film grain, subtle vignette, no CGI, no render. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 4 — THIRD PASS: module held at a steep angle showing its UNDERSIDE
    #     contact array; no flat die face toward camera (die lids invite
    #     hallucinated part-number lettering).
    "4": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a Nikon 85mm macro lens at f/2.8 on a full-frame camera, framed "
        "close and low over a stainless steel assembly workbench in a "
        "semiconductor packaging and test facility. A technician's two hands "
        "in thin pale grey nitrile cleanroom gloves hold a large AI "
        "accelerator module tilted steeply away from camera at about "
        "forty-five degrees, turning its UNDERSIDE toward the lens: a wide "
        "rectangular land-grid array of hundreds of tiny gold-plated contact "
        "pads laid out in neat dense rows and columns across a dark matte "
        "laminate substrate, every pad a minute warm golden square with a "
        "soft specular glint, the array filling the centre of the frame and "
        "receding in clean perspective. Along the near edge of the package "
        "the side profile is visible: the thickness of the dark laminate "
        "substrate, the bright machined edge of a brushed aluminium "
        "stiffener ring, and beneath it the shadowed suggestion of stacked "
        "silicon dies seen edge-on, only their thin polished bevels catching "
        "light — no die face is turned toward the camera anywhere in the "
        "frame. The gloved fingers grip the module by two opposite corners, "
        "fingertips pressing into the substrate edge, thumbs braced "
        "underneath, the nitrile creased and slightly powdery at the "
        "knuckles, a plain pale grey sleeve cuff entering at the upper "
        "right. Below the hands, filling the lower third of the frame, the "
        "module's black carbon-filled antistatic tray sits on the bench: "
        "matte moulded plastic with shallow pockets and soft ribs, one empty "
        "pocket where the part was lifted from, a faint powdery sheen on its "
        "surface. The brushed grain of the stainless bench runs across the "
        "bottom edge of the frame, and a single loose screw and a scatter of "
        "tiny dust specks lie well out of focus in the near foreground. Warm "
        "industrial task light from a bench lamp above and to the left rakes "
        "across the gold pad array, lighting it with warm amber highlights "
        "and leaving the right side of the package and the tray in deep soft "
        "shadow, honest available-light exposure and no coloured gels. "
        "Behind, thrown far out of focus into smooth planes of dark grey and "
        "warm brown, the indistinct mass of a die bonder housing and a reel "
        "of carrier tape dissolve into creamy bokeh with nothing readable in "
        "it. Photographic, extremely shallow depth of field: the nearest "
        "rows of gold pads, the substrate edge and the gloved fingertips "
        "tack sharp, the far edge of the package and the background melting "
        "away. "
    ),
    # 5 — FOURTH PASS: as 4 but the package reads as thick and rigid, both
    #     hands in frame, and the antistatic tray is clearly visible in the
    #     near foreground.
    "5": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a Nikon 85mm macro lens at f/2.8 on a full-frame camera, framed "
        "low and close across a stainless steel assembly workbench in a "
        "semiconductor packaging and test facility. Two hands in thin pale "
        "grey nitrile cleanroom gloves hold a large, thick, rigid AI "
        "accelerator package — a slab about the size of a paperback book and "
        "clearly two centimetres thick, heavy and stiff, not flexible — "
        "lifting it clear of a black carbon-filled antistatic tray that sits "
        "in the sharp foreground at the lower left, its shallow moulded "
        "pockets and soft ribs plainly visible, one empty pocket where the "
        "part was lifted from. The left hand grips the near corner from "
        "below, fingers curled under the substrate with the glove creased at "
        "the knuckles; the right hand steadies the far corner, thumb braced "
        "on the top face, a plain pale grey sleeve cuff at the frame edge. "
        "The package is turned so its side and top are seen at a steep "
        "angle: a dark matte laminate substrate edge, a bright machined "
        "brushed aluminium stiffener ring running around the perimeter, and "
        "on the visible top face a band of stacked memory dies seen almost "
        "edge-on, their polished silicon bevels catching thin warm "
        "highlights, together with one corner of a wide gold-plated contact "
        "array whose tiny square pads recede away from the lens in clean "
        "perspective. No broad flat die face is presented to camera. Warm "
        "industrial task light from a bench lamp above and to the left rakes "
        "across the metal ring and the gold pads, throwing warm amber "
        "highlights and a soft falloff into the shadowed right of the frame, "
        "honest available-light exposure with no coloured gels. The brushed "
        "grain of the stainless bench runs across the bottom of the frame, "
        "with a single loose screw and a scatter of dust specks well out of "
        "focus at the very near edge. Behind, thrown far out of focus into "
        "smooth planes of dark grey and warm brown, the indistinct mass of a "
        "die bonder housing and a reel of carrier tape dissolve into creamy "
        "bokeh with nothing readable in it. Photographic, shallow depth of "
        "field: the tray pocket, the near substrate edge, the aluminium ring "
        "and the gloved fingertips tack sharp, the far corner of the package "
        "and the background melting away. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 6 — FIFTH PASS: same no-die-face approach as 4, but the package is
    #     presented almost edge-on so its thickness dominates and only a
    #     narrow foreshortened band of contacts is visible.
    "6": (
        "Professional stock photograph, photo-realistic editorial image shot "
        "on a Nikon 85mm macro lens at f/2.8 on a full-frame camera, framed "
        "low across a stainless steel assembly workbench in a semiconductor "
        "packaging and test facility. Two hands in thin pale grey nitrile "
        "cleanroom gloves lift a large, heavy, thick AI accelerator package "
        "almost edge-on to the lens — a rigid slab like a thick hardback "
        "book, its cut edge filling the centre of the frame, clearly two "
        "centimetres of dark matte laminate substrate with a bright machined "
        "brushed aluminium stiffener ring bolted along its perimeter, the "
        "ring's fine tooling marks catching warm light. Behind that edge, "
        "foreshortened almost to nothing, a narrow band of the module's "
        "underside shows a few rows of tiny gold-plated contact pads "
        "receding steeply away, and above it the thin polished bevels of "
        "stacked silicon dies are just visible side-on as a row of fine "
        "bright lines in shadow — no broad flat face of any chip is turned "
        "toward the camera. The left hand curls under the near corner, the "
        "glove creased and slightly powdery at the knuckles and a bead of "
        "sweat-free cleanroom dust on one fingertip; the right hand steadies "
        "the far corner out of focus, a plain pale grey sleeve cuff at the "
        "upper edge. Beneath the hands the black carbon-filled antistatic "
        "tray sits on the bench in the near foreground, matte moulded "
        "plastic, its shallow ribs plain and empty. The brushed grain of the "
        "stainless bench and one loose screw lie well out of focus along the "
        "bottom edge. Warm industrial task light from a bench lamp above and "
        "to the left rakes along the aluminium ring and the near cut edge, "
        "warm amber highlights rolling into deep soft shadow on the right, "
        "honest available-light exposure, no coloured gels. Behind, thrown "
        "far out of focus into smooth planes of dark grey and warm brown, "
        "the indistinct mass of a die bonder housing and a reel of carrier "
        "tape dissolve into creamy bokeh with nothing readable in it. "
        "Photographic, extremely shallow depth of field with the near cut "
        "edge, the aluminium ring and the gloved fingertips tack sharp. "
        + PHOTO_TAIL
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
    img = img.convert("RGB")
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def ocr_text_check(path, min_conf=70.0):
    """Run tesseract OCR as a text-artifact smoke test.

    psm 11 (sparse text) on photographic texture emits low-confidence garbage
    on high-frequency detail (glove creasing, brushed metal, solder bumps).
    A genuine artifact is a multi-character token at high confidence.
      - `readable`: >=3 alnum chars AND mean confidence >= min_conf -> real risk
      - `noise`:    everything else
    Returns (readable, noise) lists of (text, conf) tuples.
    """
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return [], []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11", "tsv"],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return [], []
        tsv_path = base + ".tsv"
        if not os.path.exists(tsv_path):
            return [], []
        with open(tsv_path, errors="ignore") as f:
            rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]

    readable, noise = [], []
    for row in rows[1:]:
        if len(row) < 12:
            continue
        try:
            conf = float(row[10])
        except ValueError:
            continue
        text = row[11].strip()
        clean = "".join(ch for ch in text if ch.isalnum())
        if conf <= 0 or len(clean) < 3:
            continue
        if conf >= min_conf:
            readable.append((text, conf))
        else:
            noise.append((text, conf))
    return readable, noise


def main():
    if os.environ.get("CHECK_ONLY") == "1":
        for p in (OUTPUT, BACKUP):
            if not os.path.exists(p):
                print(f"ERROR: missing {p}")
                sys.exit(1)
            v = Image.open(p)
            print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
        readable, noise = ocr_text_check(OUTPUT)
        if not readable:
            print(
                f"OCR TEXT CHECK: clean — no readable text detected "
                f"({len(noise)} sub-threshold texture blob(s) ignored)"
            )
        else:
            print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")
        return

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
    if size < 204800:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
    readable, noise = ocr_text_check(OUTPUT)
    if not readable:
        print(
            f"OCR TEXT CHECK: clean — no readable text detected "
            f"({len(noise)} sub-threshold texture blob(s) ignored)"
        )
    else:
        print(f"OCR TEXT CHECK: WARNING {len(readable)} readable token(s): {readable[:12]}")


if __name__ == "__main__":
    main()
