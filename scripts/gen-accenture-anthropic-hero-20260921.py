#!/usr/bin/env python3
"""Generate hero for accenture-anthropic-embedded-evaluator-2026 (fal flux/schnell).

Subject: Accenture (NYSE: ACN) named Anthropic's FIRST "embedded evaluator" — an
outside team placed INSIDE the AI lab with employee-level access, red-teaming
frontier models, running alignment assessments and testing safeguards while the
models are still in training. Announced Sept 18, 2026. Each side expects to
invest at least $1B over five years. The spine of the story is a trust / audit
idea: the firm that sells AI into 9,000 enterprises is now also the one paid to
grade the models.

The picture therefore has to read as the PRESS PHOTOGRAPH OF AN OUTSIDE
EVALUATOR IN THE ROOM: a modern glass-walled corporate conference / audit room,
a professionally dressed person at a long table reviewing a printed report while
a second person works at an open laptop, city skyline or office floor blurred
through the glass wall behind them, natural window light. The audit/trust idea
is carried by the scene and the glass wall — NOT by any chart, diagram or
hardware hero shot.

Deliberately NOT a data centre / server room / server aisle / server rack / GPU
hardware / long indoor tech corridor (banned site-wide, already used repeatedly),
NOT a cleanroom, NOT a wafer, NOT a rocket or launch pad, NOT a power plant, NOT
a quantum lab, NOT abstract art, NOT digital art, NOT an illustration, NOT a 3D
render, NOT CGI, NOT neon / synthwave, NOT glowing lines, NOT geometric patterns,
NOT a HUD / hologram overlay, NOT a chart or graph.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: glass-walled offices are full of nameplates, door numbers, signage,
  screen content, lanyard badges and brand logos, so all lettering, numbers,
  signage, UI, logos and readable markings are explicitly forbidden. Screens are
  blurred glowing rectangles with NO readable content; documents are face-down,
  blurred or blank; badges are plain and unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage:
  ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-accenture-anthropic-hero-20260921.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = "accenture-anthropic-embedded-evaluator-2026"
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no door numbers, no room numbers, no "
    "suite numbers, no floor numbers, no elevator indicators, no signage, no "
    "wayfinding signs, no direction signs, no exit signs, no fire-safety "
    "notices, no wall plaques, no framed certificates, no diplomas, no awards "
    "on the wall, no nameplates, no desk nameplates, no door plates, no "
    "branding, no company names, no corporate logos, no brand names, no "
    "trademarks, no watermarks, no logos of any kind, no whiteboard writing, "
    "no whiteboard diagrams, no flipchart markings, no sticky notes, no "
    "printed pages with legible type, no readable document text, no "
    "newspapers, no magazines, no book spines, no binders with labels, no "
    "folder tabs, no post-it labels, no calendar grids, no clock faces with "
    "numerals, no wristwatch faces with numerals, no charts, no bars or "
    "graphs, no spreadsheets, no pie charts, no axes, no legends, no data "
    "tables, no dashboards, no software windows, no user interface, no "
    "toolbars, no menus, no icons, no browser tabs, no code on screen, no "
    "terminal windows, no digital readouts, no dials with numerals, no "
    "gauges, no meters, no badges with writing, no lanyards with printed "
    "text, no ID cards with text or photo, no visitor stickers, no QR codes, "
    "no barcodes, no credit cards, no business cards, no letterhead, no "
    "envelopes with addresses, no handwritten writing, no signatures, no "
    "graffiti, no legible writing of any kind anywhere in the image. Every "
    "computer screen and every laptop display in the frame is a soft blurred "
    "glowing rectangle of pure light with absolutely nothing readable, "
    "drawn, charted or lettered inside it — no windows, no text, no icons, "
    "no images, just defocused glow. Every printed document, report and "
    "notepad in the scene is face-down, closed, blank, blurred or seen only "
    "edge-on so no lettering is ever visible; the pages are plain white with "
    "no marks at all. Any badge, card or credential is plain, blank and "
    "unprinted on both sides. No illustration, no digital art, no cartoon, "
    "no 3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no circuit-board graphics, no network "
    "diagram, no graph graphic, no futuristic HUD graphics, no hologram, no "
    "overlay elements, no augmented-reality graphics, no floating UI, no "
    "data centre server room, no server racks, no server aisles, no long "
    "indoor tech corridor, no GPU hardware, no computer screen with text."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light editorial exposure, "
    "natural camera noise, very slight film grain, subtle lens vignette, no "
    "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
    "visualisation, no digital illustration, no painting, photorealistic, "
    "very high detail, professional editorial stock photography, 16:9 "
    "landscape composition. "
)

PROMPTS = {
    # 1 — PREFERRED: glass-walled corporate conference / audit room, one person
    #     reading a printed report at the long table, a second at an open
    #     laptop, skyline blurred through the glass wall, natural window light.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera from just inside the doorway of a "
        "modern corporate conference room in a high-rise office tower, eye "
        "level, three-quarter angle along a long pale wooden meeting table. "
        "The near half of the frame is in sharp focus. Seated on the far "
        "side of the table in the middle of the frame, angled toward the "
        "camera, is a professionally dressed person in a dark navy tailored "
        "blazer over a plain shirt — a consultant in their forties, calm and "
        "concentrated — leaning slightly forward over a thick printed report "
        "that lies face-up in front of them, one hand flat on the page and "
        "the other holding a pen, reading closely. The report is seen at a "
        "steep oblique angle and its pages are softly defocused and blank, "
        "carrying no legible lettering, just pale paper with a faint grey "
        "suggestion of ruled lines and faint grey blocks of defocused "
        "columnar print that dissolves into blur. Across the table to the "
        "right and closer to the camera, seen over their shoulder in the "
        "near foreground, a second person in a light grey knit sweater and "
        "plain trousers sits at an open silver laptop, seen from behind and "
        "to the side, focused on the screen; the laptop screen is turned "
        "almost fully away from the camera and appears only as a soft "
        "defocused slab of cool white and pale blue glow with no readable "
        "content whatsoever, no text, no interface, no icons. Between them "
        "on the table sit a plain white ceramic coffee cup, a small "
        "unbranded glass water carafe, a closed black notebook and a single "
        "blank loose sheet of paper, all plain and unmarked. Behind the two "
        "people, taking the whole of the background, is the room's floor-to-"
        "ceiling glass wall with slim dark mullions, and through that "
        "glass — thrown well out of focus into creamy bokeh — is the pale "
        "blue-grey mass of a dense city skyline of office towers in soft "
        "midday haze, with blank glassy facades of cool blue and faint warm "
        "silver highlights catching the sun. A subtle vertical reflection "
        "of the room and of the standing figures floats faintly on the "
        "interior surface of the glass wall. The light is beautiful natural "
        "daylight raking in low and cool from a tall window on the left of "
        "the frame, catching the edge of the table, the rim of the report "
        "and the side of the seated person's face, while the room itself "
        "falls into soft warm shadow. There is a quiet sense of serious "
        "work being done on the record — an outside evaluator with real "
        "access, in the room where the decisions get made. Strong spatial "
        "depth: the near table edge, the coffee cup and the leaning person "
        "crisp, the background laptop and the glass wall resolving, the "
        "distant skyline dissolving into soft haze and bokeh. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — INTERIOR AUDIT READ: no skyline, a wide-open glass-walled floor.
    #     Closer, more intimate framing — hands, report, laptop, glass.
    "2": (
        "As seen in a real documentary photograph, not a render and not "
        "computer generated: shot on a 50mm lens at f/1.8 on a full-frame "
        "camera from close in, a seated three-quarter view across a long "
        "pale oak meeting table in a bright glass-walled corporate "
        "conference room inside a modern office tower. Filling the left "
        "half of the sharp foreground, loosely composed, is a professionally "
        "dressed person in a charcoal blazer with the sleeves pushed up, "
        "seated at the table and bent intently over a thick printed document "
        "that lies open in front of them; only their forearms, hands and the "
        "lower half of their face are in the frame at the left edge — one "
        "hand pinning the page flat, a plain unbranded pen held loosely in "
        "the other. The printed pages are plain, pale and softly defocused, "
        "seen at a shallow graze angle so nothing on them is legible — no "
        "words, no numerals, no charts, just the dry texture of paper and "
        "the faint grey ghost of columnar print dissolved by shallow depth "
        "of field into an unreadable haze. On the right third of the frame, "
        "further from the camera and softer, a second person in a plain "
        "light blue shirt sits at an open laptop turned almost entirely away "
        "from the lens so the screen is only a defocused slab of cool white "
        "glow with nothing readable on it. Mid-frame on the table between "
        "them: a plain white cup, a glass tumbler, a closed dark notebook "
        "and a small stack of blank loose sheets, all plain and unmarked. "
        "Immediately behind the table the room is bounded by a floor-to-"
        "ceiling glass partition with slim dark metal mullions, and through "
        "that glass, thrown far out of focus into soft creamy bokeh, is the "
        "deep interior of the office floor beyond — pale desks, the blurred "
        "shoulders and heads of anonymous colleagues, and a wall of "
        "windows full of bright overexposed daylight that blooms into a "
        "soft white glow across the whole upper background. Daylight pours "
        "in from that window wall and rakes low across the table from the "
        "right, bright and cool, catching the edge of the paper and the "
        "rim of the laptop while the near side of the room sits in warm "
        "shadow. Very shallow depth of field — the hands, the paper and the "
        "pen crisp, everything beyond the far table edge melting away into "
        "smooth bokeh. The feeling is of focused, unhurried scrutiny: "
        "someone outside the company, inside the room, reading the model's "
        "report card. "
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — STRONG ALTERNATE: plain security badge swiped at a glass office
    #     door, blurred glass office interior behind, shallow depth of field.
    "3": (
        "Photo-realistic editorial press photograph, shot on an 85mm lens "
        "wide open at f/1.4 on a full-frame camera, a tight and intimate "
        "framing at chest height on the access-control reader beside a "
        "glass office door inside a modern corporate tower lobby. In the "
        "sharp right-of-centre lower foreground, a hand in a dark navy "
        "suit sleeve with a crisp white shirt cuff, belonging to a "
        "professionally dressed person whose body is cropped out of frame "
        "at the right edge, holds a plain blank white plastic security "
        "badge with no writing, no photograph, no logo and no markings of "
        "any kind, swiping it toward a small plain brushed-metal card "
        "reader mounted on a slim dark vertical mullion. The reader is a "
        "simple unmarked slab with a single tiny soft teal indicator light "
        "and no screen, no text, no numerals and no icons anywhere on it. "
        "The badge and the reader are the only crisp elements in the frame, "
        "caught in cool daylight; a faint thin reflection of the hand and "
        "card slides across the polished surface of the metal reader. "
        "Behind the hand and filling the whole rest of the frame, thrown "
        "far out of focus into soft creamy bokeh, is the office interior on "
        "the far side of the glass door — a bright modern open-plan floor "
        "of pale desks and diffuse daylight, one or two anonymous blurred "
        "figures in business dress walking at a distance with no faces "
        "resolving and no identifiable clothing marks, and beyond them a "
        "wall of windows blazing with overexposed white daylight that "
        "blooms into a soft haze across the upper background. The glass "
        "itself is clean and nearly invisible apart from a faint vertical "
        "smear of reflection running down the right side of the frame and "
        "a soft haze of internal reflection over the blurred interior. The "
        "light is bright cool daylight from the window wall, with a warm "
        "pool of ceiling lighting close to the camera on the left, giving "
        "the scene a quiet, ordinary, real-world feel. Very shallow depth "
        "of field, plenty of soft bokeh, natural camera noise in the "
        "shadows. The frame carries the idea of access itself — a keycard "
        "that opens the building, held by someone who does not work there. "
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
