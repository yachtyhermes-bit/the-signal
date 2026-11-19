#!/usr/bin/env python3
"""Hero for panw-applied-compute-security-platform-2026 (fal flux/schnell).

Subject: Palo Alto Networks beats earnings and buys the AI startup Applied
Compute for $4.5B in stock — a security platform absorbing AI capability.
Sector = cyber / enterprise software, so the scene is PEOPLE AT WORK in a
bright modern security operations room: two analysts reviewing code and
access logs on large monitors. Expressly NOT a data center, NOT a server
room, NOT a server aisle, NOT glowing lines / abstract digital art.

Rules:
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon,
  render, illustration, synthwave, HUD, matrix rain, glowing lines.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks,
  no legible content on any monitor.
- Faces not prominent: analysts seen from behind / three-quarter / side.
- Generate 1536x864, cap <=400KB, mirror EXACT SAME BYTES to _backup_dist.

HARD CAP: 3 fal flux/schnell generations (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-panw-applied-compute-security-platform-2026-hero.py
"""
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "panw-applied-compute-security-platform-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    " The image is completely free of lettering of any kind: no text, no "
    "words, no letters, no numbers, no code rendered as characters, no "
    "logging output, no console windows, no signage, no wall signs, no "
    "whiteboards with writing, no sticky notes with writing, no printed "
    "paper with legible print, no badges with names, no lanyards with "
    "text, no posters, no brand names, no company names, no corporate "
    "logos, no emblems, no trademarks, no watermarks, no signatures. Every "
    "monitor shows only soft indistinct bluish-grey luminance, out of "
    "focus, with no readable lines of text, no tables of numbers, no "
    "dashboards with labels, no charts with axes, no terminal prompts. The "
    "notebooks on the desks are closed or blank. Keyboard keys are plain and "
    "unmarked, blurred to smooth grey rectangles with no legends, and no "
    "keycap has any visible character. Every monitor, laptop, tablet and "
    "phone is an entirely plain unbranded device: no manufacturer wordmark "
    "on any bezel, no logo badge at the bottom centre or bottom right of any "
    "screen frame, no emblem or printed mark on any laptop lid, no embossed "
    "or etched brand name on any device, no sticker on any chassis. Not an "
    "illustration, not "
    "digital art, not a 3D render, not CGI, not a matte painting, no neon, "
    "no synthwave, no glowing light trails, no holograms, no HUD overlay, "
    "no geometric pattern overlay, no abstract shapes, no data "
    "visualisation graphics, no padlock icons, no shields, no circuit-board "
    "graphics, no binary rain. Not a data center, not a server room, not a "
    "server aisle, not rows of server racks, not a cold corridor of any "
    "kind, not a dark blue-lit cyber cave."
)

PHOTO_TAIL = (
    " Strictly photo-realistic editorial stock photography shot on a "
    "full-frame camera, real lens optics with honest optical blur, "
    "true-to-life skin and fabric texture, natural sensor noise, very fine "
    "film grain, subtle vignette, restrained true-to-life colour, no HDR, "
    "no plastic CGI sheen, no glossy render, no perfect symmetry. "
    "Horizontal 16:9 landscape composition, bright airy interior, very high "
    "detail."
)

PROMPTS = {
    # 1 — PRIMARY: two analysts side by side at a shared desk, seen from
    #     behind/three-quarter, large monitors angled away, window light.
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 35mm lens at f/2 in a bright modern "
        "security operations room inside a corporate office. Two analysts "
        "sit side by side at a long pale oak desk, both viewed from behind "
        "and slightly to the left at a three-quarter angle so their faces "
        "are turned away from the camera: the nearer one is a woman in a "
        "soft grey knit sweater with her hair loosely tied back, leaning "
        "forward with her right hand on a mouse and her left forearm "
        "resting on the desk; the second is a man in a light blue button-up "
        "shirt with the sleeves rolled, sitting a little further along the "
        "desk, turned toward her as if they are discussing something on "
        "screen. In front of them, three large thin-bezel monitors stand on "
        "plain arms, tilted slightly away from the lens so the viewer sees "
        "only the backs and edges of the screens and a faint wash of pale "
        "blue-white light spilling onto the desk surface; the screens carry "
        "no readable content, just soft diffuse glow. On the desk: a "
        "keyboard, a mouse, a closed notebook, a ceramic mug, a pair of "
        "reading glasses, a pen, and a small trailing plant. The room is "
        "airy and light: pale grey walls, light wood, a fabric acoustic "
        "panel, a couple of green plants, and a second pair of desks "
        "further back where two distant colleagues are reduced to soft "
        "shapes. Tall windows on the right side of the frame flood the "
        "scene with bright, soft morning daylight, rim-lighting the "
        "analysts' shoulders and hair, with gentle shadow falloff across "
        "the desk and a warm highlight on the oak. Photographic shallow "
        "depth of field: the near analyst's shoulder, hair, hand and the "
        "mug tack sharp, the second analyst and the monitor arms softening, "
        "and the far desks dissolving into creamy bokeh. Unposed, candid, "
        "believable working posture, natural imperfect framing."
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — WIDER: open-plan floor, pair at a monitor bank in mid-ground,
    #     foreground desk edge blurred. More room, more light.
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 50mm lens at f/2.2 in a bright "
        "open-plan office of a cybersecurity company. The camera stands at "
        "desk height a few metres back, the near edge of an empty desk "
        "blurred in the bottom left foreground with a coffee cup and a "
        "closed laptop on it. In the middle distance, two colleagues work "
        "together at a bank of four large monitors mounted on a shared "
        "stand: a man in a charcoal quarter-zip sweater sits at the "
        "keyboard, seen from behind at a slight angle so only the back of "
        "his head and his shoulders are visible, and a woman in a cream "
        "blouse stands beside his chair leaning one hand on the desk, "
        "turned toward the screens in profile with her face soft and partly "
        "occluded by her hair. The monitors are angled away from the camera "
        "so their faces are lit only by a cool pale-blue glow while the "
        "screen surfaces themselves are out of focus and show nothing but "
        "diffuse luminous grey-blue, no readable lines. The monitors are "
        "clearly switched on and working: they glow and cast visible light "
        "across the desk, the keyboard and the analysts' forearms, but the "
        "glow is a featureless pale haze with no distinct glyphs, no lines "
        "of code, no rows of characters, no window borders. Around them the "
        "floor is calm and generously spaced: pale wood desks in loose "
        "rows, light grey carpet, white columns, tall windows along the "
        "left wall letting in broad soft daylight with faint green tree "
        "shapes beyond the glass, two potted plants, an acoustic fabric "
        "divider. Bright natural daylight dominates, mixing with the cool "
        "monitor glow; honest white balance, gentle contrast, no coloured "
        "gels. Photographic shallow depth of field with real optical bokeh: "
        "the two analysts crisp enough to read posture and clothing "
        "texture, the foreground desk and the far offices falling away into "
        "smooth blur. Documentary realism, slightly off-centre "
        "composition, unposed."
        + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — FALLBACK: closer two-shot over the shoulder of one analyst, second
    #     analyst leaning in, monitor light on faces. Highest-emotion frame.
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with an 85mm lens at f/2 in a modern corporate "
        "security operations room. An over-the-shoulder two-shot: in the "
        "near foreground, cropped at the shoulder and the side of the head "
        "on the left edge of the frame, an analyst in a dark navy shirt is "
        "seen from behind, one hand raised to point at the middle of a "
        "large monitor that fills the centre-right of the frame. The "
        "monitor is turned away at a steep angle so the viewer sees mostly "
        "its dark matte back and the thin silver arm that holds it, with "
        "only a sliver of pale blue glow escaping around the edge and "
        "washing across the analyst's forearm and cheekbone. Beyond the "
        "monitor, a second analyst in a light grey sweater stands leaning "
        "in from the right, seen in three-quarter profile with the face "
        "softly out of focus and partly turned away, holding a printed "
        "sheet face-down in one hand and a pen in the other, listening. A "
        "keyboard, a trackpad and a glass of water sit on the desk in the "
        "sharpest plane of focus. Warm daylight from a tall window behind "
        "them on the right creates a soft rim along the standing analyst's "
        "shoulder and the edge of the monitor, while the front of the scene "
        "sits in gentle cool shadow lit only by the screen spill. Pale "
        "wood, muted grey walls, a blurred plant in the background. "
        "Photographic shallow depth of field, very shallow, real optical "
        "blur and creamy bokeh, sharp only on the keyboard and the near "
        "hand, everything else falling softly away. Candid, quiet, "
        "concentrated atmosphere, believable office realism."
        + PHOTO_TAIL
        + NO_TEXT
    ),
}


def load_fal_key():
    candidates = (
        "/home/chino/.hermes/profiles/yachty/.env",
        "/home/chino/hermes-workspace/studio-api/.env",
        "/home/chino/video_output/.fal_real",
    )
    for path in candidates:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
                if path.endswith(".fal_real") and line:
                    key = line.split("|", 1)[1] if "|" in line else line
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating with fal flux/schnell ...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )
    url = (result.get("images") or [{}])[0].get("url") or result.get("image")
    if not url:
        print("ERROR: no image url: %s" % result)
        sys.exit(1)
    print("Image URL: %s" % url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded %s size=%s bytes=%d" % (out_path, img.size, len(r.content)))
    return img


def save_capped(img, path):
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=%s (hard cap 1-3)" % ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT)
    if img.size != (W, H):
        resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
        img = img.resize((W, H), resample)
    img = img.convert("RGB")
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy2(OUTPUT, BACKUP)  # exact same bytes
    print("Mirrored (byte-identical) to %s" % BACKUP)
    print("VERIFY %s dims=%s bytes=%d" % (OUTPUT, img.size, os.path.getsize(OUTPUT)))
    with open("/tmp/panw-prompt-%s.txt" % ATTEMPT, "w") as f:
        f.write(prompt)


if __name__ == "__main__":
    main()
