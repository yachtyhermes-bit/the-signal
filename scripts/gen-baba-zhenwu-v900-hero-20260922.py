#!/usr/bin/env python3
"""Generate hero for baba-zhenwu-v900-ai-chip-stack-2026 (fal flux/schnell).

Subject: Alibaba's T-Head "Zhenwu V900" AI accelerator — China's self-designed
AI silicon, a large multi-die accelerator package. The story is the hardware
itself and, behind it, the supply-chain / self-sufficiency question.

The picture therefore has to read as a MACRO EDITORIAL LAB INSPECTION PHOTOGRAPH
OF THE CHIP ITSELF: a large multi-die AI accelerator package sitting on a matte
dark lab inspection bench, a rectangular silicon package with a lid, the
multi-die construction visible along the exposed interposer edge (small silicon
dies set into a larger carrier with fine copper routing), rows of tiny solder
bumps along one cut edge, and a slender metal inspection microlens / probe head
entering the frame from the upper right at a steep angle. It is a photograph of
a physical object under task lighting — the subject carries the story by itself.

Deliberately NOT a data centre / server room / server aisle / server rack
(banned site-wide, already used repeatedly), NOT a person in a cleanroom suit,
NOT gloved hands holding a circuit board, NOT hard-drive platters, NOT a
neon / synthwave / glowing-lines / geometric-pattern abstract digital image,
NOT a HUD / hologram / chart / graph, NOT an illustration, NOT a 3D render,
NOT CGI.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial macro photograph ONLY.
- TEXT-FREE: flux loves to laser-etch text onto chip surfaces, package lids,
  PCBs and probe bodies, so all lettering is explicitly forbidden EVERYWHERE —
  no lot codes, no part numbers, no die markings, no "AI"-style glyphs, no
  laser-etched serials, no branding, no logos, no watermarks. Every surface in
  the frame is plain and unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-baba-zhenwu-v900-hero-20260922.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = "baba-zhenwu-v900-ai-chip-stack-2026"
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "There is absolutely no lettering anywhere in this photograph: no text, "
    "no letters, no words, no numbers, no digits, no punctuation on any "
    "surface, on any object, at any depth. The silicon is completely "
    "unmarked: there is no laser-etched text on any chip die, no etched "
    "lettering on the silicon, no mask markings, no die corner lettering, "
    "no alignment glyphs that read as characters, no lot codes, no batch "
    "codes, no part numbers, no serial numbers, no date codes, no fab "
    "markings, no stepper marks, no fiducials that read as letters, no "
    "silkscreen printing, no white legend printing, no reference designator "
    "labels, no printed labels, no etched branding, no manufacturer name, "
    "no company name, no corporate logo, no wordmark, no symbol, no glyph, "
    "no icon, no barcode, no QR code, no data matrix mark, no dot-matrix "
    "marking, no ink stamp, no engraved writing, no scratched or scribed "
    "characters anywhere on the chip package, the lid, the interposer, the "
    "carrier substrate, the copper routing, the solder bumps, the probe "
    "body, the microlens barrel, the tweezers or the bench. The package lid "
    "is a plain unmarked slab with no printed or engraved marking of any "
    "kind on its face or its edges. The probe head and its metal barrel are "
    "plain brushed metal with no engraved text, no printed scale, no ring "
    "markings, no knurling that reads as type, and no brand name. The bench "
    "is plain matte dark material with no tape labels, no masking-tape "
    "writing, no sticky notes, no printed sheet, no paper, no notebook, no "
    "clipboard, no ruler with numerals, no measuring scale, no printed "
    "graduations, no dial with numerals, no gauge face, no meter, no digital "
    "readout, no seven-segment display, no status indicator with characters, "
    "no chart, no graph, no diagram, no plotted curve, no axes, no legend, "
    "no data table, no spreadsheet, no software window, no user interface, "
    "no toolbar, no menu, no browser tab, no code, no terminal window, no "
    "written note, no handwriting, no signature, no signature marks, no "
    "graffiti, no watermark, no corner mark, no signature box, no caption, "
    "no border text, no logo anywhere, no legible lettering of any kind "
    "anywhere in the image at all. Nothing in the frame is a screen and "
    "nothing in the frame displays any content. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no neon, no glowing lines, no "
    "light trails, no synthwave, no geometric pattern overlay, no circuit-"
    "board graphic, no network diagram, no graph graphic, no futuristic HUD "
    "graphics, no hologram, no overlay elements, no augmented-reality "
    "graphics, no floating interface elements. No data centre, no server "
    "room, no server racks, no server aisle, no long indoor tech corridor, "
    "no cleanroom, no cleanroom bunny suit, no person in a protective suit, "
    "no laboratory worker, no gloves, no gloved hands, no bare hands, no "
    "fingers, no hand holding a circuit board, no human figure, no people "
    "anywhere in the frame, no hard-drive platters, no spinning disk, no "
    "wafer on a pedestal, no robot arm."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light editorial exposure, "
    "natural camera sensor noise, very slight film grain, subtle lens "
    "vignette, no plastic CGI sheen, no glossy render, no perfect symmetry, "
    "no 3D visualisation, no digital illustration, no painting, "
    "photorealistic, very high detail, professional editorial stock "
    "photography, macro lens rendering, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — PREFERRED: macro three-quarter view of the bare multi-die package on
    #     the dark inspection bench, probe head entering from the upper right.
    "1": (
        "Photo-realistic editorial macro photograph, an extreme close-up shot "
        "on a 100mm macro lens at f/4 on a full-frame camera, camera set low "
        "and angled down at roughly thirty-five degrees across a matte dark "
        "grey laboratory inspection bench with a very fine, faintly dusty "
        "micro-texture and a soft diffuse sheen. The single subject filling "
        "the sharp centre of the frame is a large rectangular multi-die AI "
        "accelerator chip package about the size of a matchbox, an engineering "
        "sample with its protective lid still on, resting squarely on the "
        "bench with nothing under it and nothing around it. The package is a "
        "flat squared slab with a brushed, slightly bead-blasted metal lid "
        "that is completely plain and unmarked, its beveled edges catching a "
        "thin cold highlight, and beneath the lid a dark greenish-grey "
        "laminate carrier substrate whose cut edge is clearly visible in "
        "focus along the lower-left side: the multi-die construction is "
        "exposed there, showing three or four small rectangular silicon dies "
        "of slightly different sizes set down into the larger carrier, their "
        "tile-like seams and the fine copper routing traces fanning out "
        "between them in hair-thin lines under a faint warm bronze of "
        "exposed metal, all of it a real physical object seen under "
        "raking light rather than any kind of graphic or diagram. Along the "
        "nearest cut edge of the substrate runs a single dense row of "
        "hundreds of tiny solder bumps, each one a bright micro-sphere "
        "smaller than a grain of salt, arrayed in perfect staggered rows "
        "like a metallic comb, the near end of that row falling softly out "
        "of focus as it recedes. From the upper right corner of the frame, "
        "entering steeply at a sharp angle, comes a slender brushed-steel "
        "inspection microlens barrel with a tiny dark glass objective at its "
        "tip, hovering just above and slightly to the right of the package, "
        "held steady and tilted toward the exposed die seams — the probe "
        "head and the tip of the lens barrel are the closest objects to the "
        "camera on that side and stay crisp, while the shaft of the barrel "
        "runs out of the frame entirely and the rest of the instrument is "
        "never shown. Cool focused task lighting rakes low across the bench "
        "from the upper left, hard-edged and clinical, grazing the lid so "
        "that its brushed texture and a few faint fingerprints of handling "
        "come up, throwing the trailing solder bumps and the die seams into "
        "fine micro-shadow, and letting the far right of the bench fall into "
        "deep clean darkness. Shallow depth of field with creamy smooth "
        "bokeh behind the package: only the near cut edge, the row of solder "
        "bumps and the lens tip are truly sharp, the die seams stay almost "
        "sharp, the lid softens toward its far corner, and the bench "
        "dissolves into an even untextured dark falloff with one or two "
        "small, entirely defocused bright specular points where lab light "
        "catches something far away. Faint dust-free still lab atmosphere, "
        "no smoke, no haze, no motion. The frame reads as the hardware at the "
        "centre of the story — real silicon, real metal, a real instrument "
        "over it, the physical fact of a chip. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — ALTERNATE: lower, flatter near-graze angle along the cut edge, the
    #     lid set aside so the bare die/interposer face is the subject.
    "2": (
        "Photo-realistic editorial macro photograph, a very close macro shot "
        "on a 100mm macro lens at f/3.5 on a full-frame camera, camera "
        "dropped almost to bench level and looking in almost edge-on down "
        "the length of a matte dark charcoal inspection bench under a "
        "single clinical task light, the composition running diagonally "
        "with the subject slightly left of centre and the background falling "
        "away to the right. The subject is the bare silicon side of a large "
        "multi-die AI accelerator package, an engineering sample lying face "
        "up on the bench with its plain unmarked metal lid set down flat "
        "beside it a short distance away: a broad rectangular greenish-grey "
        "carrier substrate patterned with extremely fine copper routing "
        "traces that sweep in dense parallel curves and bundles between the "
        "die sites, and set into that carrier, four separate rectangular "
        "silicon dies with plain mirror-polished tops and clean etched "
        "edges, each die reflecting the task light as a flat dark mirror "
        "with a faint iridescent blue-violet cast drifting across one of "
        "them. The fine copper and the tiny gold bond wires looping to the "
        "carrier lands are rendered as real metal seen under a raking light, "
        "physically present and slightly imperfect, absolutely not a "
        "circuit-board graphic. The nearest long cut edge of the substrate "
        "runs across the lower foreground in very sharp focus, and along it "
        "runs one dense staggered row of hundreds of microscopic solder "
        "bumps, each catching a small hard specular glint, the row receding "
        "away from the camera and blurring into a soft metallic band. From "
        "the upper right, angling steeply down into frame, a slender "
        "brushed-steel probe or microlens barrel with a tiny dark optic at "
        "its tip points in toward the nearest die, crisp at the tip and "
        "running out of frame on the shaft, the rest of the instrument never "
        "visible. Cool focused task light rakes hard across the bench from "
        "the upper left at a low grazing angle, carving the die edges and "
        "the solder-bump row in fine specular relief and pushing the far "
        "side of the package into rich clean shadow, with one softly "
        "defocused highlight blooming off the distant bench behind. "
        "Extremely shallow depth of field, creamy smooth bokeh, the near "
        "edge and the lens tip the only fully resolved elements. Faint "
        "dust-free still lab atmosphere, no haze, no smoke. The frame reads "
        "as a real engineer's macro look at real hardware — the silicon "
        "itself, lying open on the bench. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — NOISE-SUPPRESSED VARIANT of 1 (2026-09-22): the OCR smoke test on
    #     attempts 1 and 2 returned 13 and 29 low-confidence micro-fragments
    #     against a 0-6 baseline on accepted heroes. The cause is texture, not
    #     real lettering: hair-thin copper routing traces, die seams and
    #     brushed-metal sparkle all render as glyph-like micro-squiggles that
    #     tesseract reads as characters. Attempt 3 keeps the framing that
    #     worked and removes that failure mode at the source: a smooth satin
    #     lid instead of brushed metal, plain tile-like dies with clean
    #     straight seams instead of dense routing, and an explicit ban on
    #     letter-like micro-marks anywhere in the texture.
    "3": (
        "Photo-realistic editorial macro photograph, an extreme close-up shot "
        "on a 100mm macro lens at f/4 on a full-frame camera, camera set low "
        "and angled down at roughly thirty-five degrees across a smooth matte "
        "dark grey laboratory inspection bench with a fine even surface and "
        "no strong texture, no visible grain pattern and no speckling. The "
        "single subject filling the sharp centre of the frame is a large "
        "rectangular multi-die AI accelerator chip package about the size of "
        "a matchbox, an engineering sample with its protective lid still on, "
        "resting squarely on the bench with nothing under it and nothing "
        "around it. The package is a flat squared slab with a smooth satin-"
        "finish dark metal lid that is completely plain and unmarked, its "
        "surface clean and even with no brushed striations, no scratches, no "
        "engraving and no printing of any kind, its beveled edges catching a "
        "thin cold highlight. Beneath the lid a dark neutral grey laminate "
        "carrier substrate is visible along the cut edges, and on the lower-"
        "left edge the multi-die construction is exposed in sharp focus: "
        "three or four plain rectangular silicon dies of slightly different "
        "sizes set down flat into the larger carrier, their matte grey "
        "surfaces perfectly smooth and blank, separated only by simple clean "
        "straight seams, with no fine line-work of any kind between or across "
        "them — no dense routing traces, no hair-thin scribble, no fine "
        "interconnect pattern, no microscopic squiggle, no glyph-like detail, "
        "no character-like or letter-like micro-marks anywhere on the "
        "substrate or the dies, just plain smooth silicon tiles with straight "
        "edges. Along the nearest cut edge of the package runs a single row "
        "of tiny solder bumps, each one a smooth bright mercury-like "
        "micro-sphere smaller than a grain of salt, arrayed in a plain "
        "regular evenly spaced line, the near end of that row falling softly "
        "out of focus as it recedes along the edge. From the upper right "
        "corner of the frame, entering steeply at a sharp angle, comes a "
        "slender smooth steel inspection microlens barrel with a tiny dark "
        "glass objective at its tip, hovering just above and slightly to the "
        "right of the package, tilted down toward the exposed die seams — the "
        "probe head and the tip of the lens barrel are the closest objects to "
        "the camera on that side and stay crisp, while the shaft runs out of "
        "the frame entirely and the rest of the instrument is never shown; "
        "the barrel is plain polished metal with no engraved scale, no ring "
        "markings and no printed detail. Cool focused task lighting rakes low "
        "across the bench from the upper left, clinical and controlled, "
        "grazing the lid so that its smooth satin sheen rolls gently across "
        "the surface, defining the straight edge of the package and letting "
        "the far right of the bench fall into deep clean darkness. Shallow "
        "depth of field with creamy smooth bokeh behind the package: only the "
        "near cut edge, the row of solder bumps and the lens tip are truly "
        "sharp, the die seams stay almost sharp, the lid softens toward its "
        "far corner, and the bench dissolves into an even untextured dark "
        "falloff with one or two small, entirely defocused bright specular "
        "points where lab light catches something far away. Faint dust-free "
        "still lab atmosphere, no smoke, no haze, no motion, no speckle, no "
        "noise pattern that could be mistaken for writing. The frame reads as "
        "the hardware at the centre of the story — real silicon, real metal, "
        "a real instrument over it, the physical fact of a chip. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 4 — BEST-OF-BOTH (2026-09-22): attempt 1 had genuine macro detail (centre
    #     edge-energy 41.3) but 13 OCR noise fragments; attempt 3 was OCR-clean
    #     but mushy (centre edge-energy 9.6) — it bought the clean read by going
    #     soft, which fails the macro brief. Attempt 4 keeps attempt 1's sharp
    #     in-focus subject and its structural detail (die tiles, clean seams,
    #     the solder-bump row, the probe barrel, the package edges) while
    #     banning the specific glyph factories: hair-thin copper routing,
    #     brushed-metal striations, handling fingerprints and speckle.
    "4": (
        "Photo-realistic editorial macro photograph, an extreme close-up shot "
        "on a 100mm macro lens at f/4 on a full-frame camera, camera set low "
        "and angled down at roughly thirty-five degrees across a smooth matte "
        "dark grey laboratory inspection bench, its surface even and plain "
        "with no speckle and no fine grain pattern of its own. The single "
        "subject, filling the centre of the frame and held in sharp macro "
        "focus, is a large rectangular multi-die AI accelerator chip package "
        "about the size of a matchbox, an engineering sample with its "
        "protective lid still on, resting squarely on the bench with nothing "
        "under it and nothing around it. The package is a flat squared slab "
        "with a smooth satin-finish dark metal lid, completely plain and "
        "unmarked, clean and even with no brushed striations, no scratches, "
        "no fingerprint smudges, no engraving and no printing; a thin cold "
        "highlight runs along its beveled near edge, and the package's four "
        "straight edges and squared corners are crisp and geometrically "
        "clean. Beneath the lid, along the lower-left cut edge of the "
        "package in sharp focus, the multi-die construction is exposed: three "
        "or four plain rectangular silicon dies of slightly different sizes "
        "set down flat and flush into a larger dark grey carrier substrate, "
        "their matte grey tops smooth and completely blank, separated by "
        "simple clean straight seams, the copper lands around them rendered "
        "as broad plain smooth shapes rather than hair-thin line-work — there "
        "is no dense maze of microscopic routing, no fine scribble of traces, "
        "no squiggle, no glyph-like or character-like micro-mark, no "
        "letterform anywhere in the texture, just plain smooth silicon tiles "
        "with straight edges meeting at clean angles. Along the nearest cut "
        "edge of the package runs one row of tiny solder bumps, each a smooth "
        "bright mercury-like micro-sphere smaller than a grain of salt, "
        "arrayed in a plain, evenly spaced, perfectly regular line, the row "
        "receding along the edge and the far end falling softly out of focus. "
        "From the upper right corner of the frame, entering steeply at a "
        "sharp angle, comes a slender smooth polished-steel inspection "
        "microlens barrel with a tiny dark glass objective at its tip, "
        "hovering just above and slightly right of the package and tilted "
        "down toward the exposed die seams; the tip and the front of the "
        "barrel are the nearest sharp objects on that side, while the shaft "
        "runs cleanly out of the frame so the rest of the instrument is never "
        "shown, and the barrel carries no engraved scale, no ring markings, "
        "no knurling and no printed detail. Cool focused task lighting rakes "
        "low across the bench from the upper left, controlled and clinical, "
        "modelled softly enough to avoid harsh sparkle and glitter, grazing "
        "the package to define the straight edge of the lid and the tops of "
        "the die tiles, while the far right of the bench falls away into deep "
        "clean darkness. Shallow depth of field, creamy smooth bokeh: the "
        "near cut edge, the die seams and the solder-bump row are tack sharp, "
        "the lens tip sharp, the far side of the lid softening, and the bench "
        "dissolving into an even untextured dark falloff with one or two "
        "small, fully defocused specular points where lab light catches "
        "something distant. Faint dust-free still lab atmosphere, no smoke, "
        "no haze, no motion, no speckle, no glitter, no micro-noise pattern. "
        "The frame reads as the hardware at the centre of the story — real "
        "silicon, real metal, a real instrument over it, the physical fact of "
        "a chip. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 5 — SHARP + PLAIN (2026-09-22): attempt 4 kept the detail (centre energy
    #     comparable to attempt 1) but still pulled 10 OCR micro-fragments.
    #     Attempt 3 proved a plain-texture read can be OCR-clean but went soft.
    #     Attempt 5 asks for both at once: an unmistakably tack-sharp, high
    #     micro-contrast macro subject built ONLY from large simple shapes
    #     (squared package, flat lid, plain die tiles, one regular bump row,
    #     the smooth barrel) with every fine-texture source named and removed.
    "5": (
        "Photo-realistic editorial macro photograph, a tack-sharp extreme "
        "close-up shot on a 100mm macro lens at f/5.6 on a full-frame camera, "
        "camera set low and angled down at roughly thirty-five degrees across "
        "a plain smooth matte dark grey laboratory inspection bench that has "
        "an even, featureless surface with no speckle and no grain of its "
        "own. The centre of the frame is filled by a single large rectangular "
        "multi-die AI accelerator chip package, roughly matchbox sized, an "
        "engineering sample with its lid on, resting flat and square on the "
        "bench with nothing under it and nothing around it. Held in crisp, "
        "high micro-contrast macro focus, the package is a flat squared slab: "
        "a smooth satin dark metal lid that is perfectly plain and unmarked "
        "with no brushed striations, no scratching, no smudges and no "
        "printing, its surfaces flat and its four straight edges and square "
        "corners geometrically exact, with a thin cold specular highlight "
        "running along the bevel of its near edge. Along the lower-left cut "
        "edge of the package, shown at a steep angle and sharply resolved, "
        "the multi-die construction is exposed: three or four plain "
        "rectangular silicon dies of slightly different sizes sitting flat "
        "and flush in a larger dark grey carrier, their matte tops smooth and "
        "blank, divided by a few simple straight seams, the copper around "
        "them drawn as broad plain smooth areas rather than any fine "
        "line-work. There is no maze of fine traces, no hair-thin scribble, "
        "no squiggle, no glyph-like or character-like micro-mark, no "
        "letterform hidden in the texture — only big, simple, clean-edged "
        "shapes. Along the nearest cut edge of the package sits one row of "
        "tiny solder bumps: smooth bright mercury-like micro-spheres, smaller "
        "than a grain of salt, in a perfectly regular evenly spaced line, "
        "each catching a small hard clean specular glint, the row receding "
        "along the edge with its far end softening out of focus. From the "
        "upper right of the frame, angling steeply down, a slender smooth "
        "polished-steel inspection microlens barrel enters with a tiny dark "
        "glass objective at its tip, hovering just above and to the right of "
        "the package, aimed down at the exposed die seams; the tip and the "
        "front of the barrel are among the sharpest things in the picture "
        "while the shaft runs out of frame, and the barrel carries no "
        "engraved scale, no ring markings, no knurling, no printed detail. "
        "Cool focused task lighting rakes low across the bench from the upper "
        "left, controlled and clinical but softly modelled, so there is no "
        "harsh glitter or sparkle anywhere: it defines the straight edge of "
        "the lid, the corners of the die tiles and the crests of the bump "
        "row, and lets the far right of the bench fall into deep clean "
        "darkness. Shallow depth of field with creamy smooth bokeh: the die "
        "seams, the near cut edge and the solder-bump row tack sharp, the "
        "lens tip sharp, the far side of the lid and the distant bench "
        "melting into an even untextured dark falloff with one or two fully "
        "defocused specular points. Faint dust-free still lab atmosphere, no "
        "smoke, no haze, no motion, no speckle, no glitter, no micro-noise "
        "pattern that could be mistaken for writing. The frame reads as the "
        "hardware at the centre of the story — real silicon, real metal, a "
        "real instrument over it, the physical fact of a chip. "
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
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def ocr_text_check(path):
    """Run tesseract OCR as a text-artifact smoke test. Returns list of words."""
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping text check")
        return []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11"],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping text check")
            return []
        txt_path = base + ".txt"
        if not os.path.exists(txt_path):
            return []
        with open(txt_path, errors="ignore") as f:
            raw = f.read()
    words = []
    for line in raw.splitlines():
        clean = "".join(ch for ch in line if ch.isalnum())
        if len(clean) >= 3:
            words.append(line.strip())
    return words


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
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )
    # OCR text-artifact smoke test on the published file
    words = ocr_text_check(OUTPUT)
    if not words:
        print("OCR TEXT CHECK: clean — no readable text detected")
    else:
        print(f"OCR TEXT CHECK: WARNING {len(words)} candidate token(s): {words[:12]}")


if __name__ == "__main__":
    main()
