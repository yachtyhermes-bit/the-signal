#!/usr/bin/env python3
"""Hero for amd-helios-rack-margin-test-2026 (fal flux/schnell).

Subject: AMD shifting from selling AI accelerator chips to selling whole
rack-scale AI systems ("Helios" cabinets), heading into the Q3 2026 print.

Scene: a semiconductor CLEANROOM — one engineer in a white bunny suit and
hood holds a reflective silicon wafer up toward the light with gloved hands,
seen from the side; fab equipment and a second engineer softly out of focus
behind. Cool white/blue cleanroom light, real photographic depth of field.

Deliberately NOT a data-centre hallway / server aisle / rack row (banned
site-wide), NOT a server room, NOT neon / synthwave / glowing lines, NOT
digital art, NOT 3D render or CGI, NOT abstract.

Rules:
- PHOTO-REALISTIC editorial photograph only.
- TEXT-FREE: no letters / numbers / labels / logos / wafer lot codes / die
  markings / signage / screens anywhere.
- Generate 1536x864, save <=400KB, mirror EXACT SAME BYTES to _backup_dist.

HARD CAP: 3 fal flux/schnell generations (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-amd-helios-rack-margin-test-hero-20261103.py
"""
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "amd-helios-rack-margin-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "The image is completely free of lettering of any kind: no text, no "
    "words, no letters, no numbers, no signage, no wall signs, no warning "
    "placards, no equipment nameplates, no asset tags, no labels on any "
    "machine, no printed paper, no clipboards, no monitor screens, no "
    "digital readouts, no control panels with characters, no user "
    "interface, no dashboards. The silicon wafer is a plain polished "
    "mirror disc with absolutely no laser-scribed lot codes, no wafer "
    "identification text, no die markings, no etched characters, no "
    "flat-edge notch lettering, no printed or engraved marks of any kind "
    "on its surface or on its edge. The bunny suit is plain unmarked white "
    "fabric with no embroidered name, no printed patch, no wordmark, no "
    "badge with writing. The gloves are plain with no printed legend. No "
    "brand names, no company names, no corporate logos, no trademarks, no "
    "watermarks, no signatures. Not an illustration, not digital art, not "
    "a 3D render, not CGI, not a matte painting, no neon, no synthwave, no "
    "glowing light trails, no geometric pattern overlay, no abstract "
    "shapes, no data visualisation graphics, no HUD overlay, no hologram, "
    "no circuit-board graphic. Not a data center, not a server room, not a "
    "server aisle, not rows of server racks, not a corridor of any kind."
)

PHOTO_TAIL = (
    " Strictly photo-realistic editorial stock photography: real lens "
    "optics with honest optical blur, true-to-life materials, natural "
    "sensor noise, very fine film grain, subtle vignette, restrained "
    "true-to-life colour, no HDR, no plastic CGI sheen, no glossy render, "
    "no perfect symmetry. Horizontal 16:9 landscape composition, "
    "professional lighting, very high detail, tack-sharp focus on the "
    "hands and the wafer."
)

PROMPTS = {
    # 1 — PRIMARY: side-on profile, engineer in white bunny suit holding a
    #     mirror wafer up to the cleanroom light. Wafer + gloved hands are
    #     the subject; hood and fab equipment fall out of focus.
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with an 85mm lens at f/2 on a semiconductor "
        "fab cleanroom floor. Seen in clean side profile from about waist "
        "height, a single engineer stands in the centre-right of the frame "
        "wearing a plain white full-body bunny suit with the hood up and a "
        "white face mask, only a narrow strip of skin and one eye visible "
        "at the hood opening, the fabric softly creased and faintly "
        "translucent at the shoulders. Both arms are raised in front of "
        "the chest: two hands in thin white nitrile cleanroom gloves hold a "
        "single large circular silicon wafer up toward the ceiling light, "
        "gripping it delicately by opposite edges between thumb and "
        "fingertips so the full disc faces the lens at a slight angle. The "
        "wafer is a flawless mirror-polished disc about 300 millimetres "
        "across, its surface catching the overhead light as a broad soft "
        "silvery sheen with a faint rainbow diffraction bloom sliding "
        "across the upper left quadrant and a deep charcoal reflection of "
        "the room in the lower right; beneath the glare the faint "
        "rectilinear grid of unprinted die sites is just perceptible as a "
        "ghost pattern in the mirror surface, and the polished chamfered "
        "edge glints as a thin bright rim. The engineer's head is tilted "
        "slightly back and toward the wafer, intent on inspecting it. Cool "
        "white and pale blue cleanroom light falls from flat luminous "
        "ceiling panels and from a soft source behind, rim-lighting the "
        "edge of the hood and the shoulder of the suit; the light on the "
        "wafer is a clean even silver with one soft specular streak. "
        "Behind and to the left, thrown well out of focus into smooth "
        "pale grey-blue planes, stand the matte white and stainless steel "
        "housings of fab process equipment with rounded corners and plain "
        "dark viewports, and beyond them a second engineer in an identical "
        "white bunny suit walks away at an angle, reduced to a soft pale "
        "silhouette. Photographic, shallow depth of field: the wafer, the "
        "gloved fingertips and the creases of the suit sleeve tack sharp, "
        "the background dissolving into creamy cool bokeh." + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — TIGHTER: closer on hands + wafer, engineer's hooded head cropped
    #     at frame edge, wafer dominant and larger.
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 100mm lens at f/2.2 in a semiconductor "
        "cleanroom. A tight medium close-up from the side: a technician in "
        "a plain white cleanroom bunny suit and hood, cropped at the "
        "shoulder on the left edge of the frame, seen in profile, holds a "
        "large mirror-polished silicon wafer up at chest height toward the "
        "light with both hands in thin white nitrile gloves. The wafer "
        "fills the centre of the frame, tilted toward camera at a shallow "
        "angle so it reads as a wide ellipse of silver: its polished face "
        "is a soft mirror carrying a blurred cool reflection of the "
        "ceiling panels, a faint iridescent rainbow band of diffraction "
        "curling along one edge, a handful of minute dust specks catching "
        "pinpoints of light, and the ghost of an unprinted rectilinear die "
        "grid barely visible under the sheen. The gloved fingers grip the "
        "rim at two opposite points, fingertips pressing flat, the thin "
        "nitrile stretched and creased at the knuckles, the wrist of the "
        "suit gathered in soft folds where the glove meets the sleeve. "
        "Cool blue-white light from overhead and from the left makes the "
        "wafer glow and leaves the underside of the hands in gentle "
        "shadow; the engineer's masked face is turned down toward the disc "
        "and softly out of focus at the frame edge. All around, the fab "
        "floor falls away into pale grey and cool white bokeh: the blurred "
        "vertical mass of a process tool, a stainless rail, a faint pale "
        "shape of another worker in white. Photographic, very shallow "
        "depth of field, real optical blur, sharp on the wafer surface, "
        "the gloved fingertips and the near sleeve seam." + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — FALLBACK (sanctioned alternative): no people. Macro of a mirror
    #     wafer resting on a matte surface. Prompt hardened against the
    #     "brushed metal plate" failure mode seen in attempts 1-2:
    #     the wafer must read as glassy, specular, near-black mirror with a
    #     faint die grid and diffraction, never a concentric-brushed disc.
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a 100mm macro lens at f/3.2 from a low three-quarter angle in a "
        "semiconductor cleanroom. The frame is dominated by ONE large "
        "circular silicon wafer, 300 millimetres across, lying flat on a "
        "smooth matte pale grey anodised surface that fills the lower "
        "third of the frame, the disc tilted toward the lens so it reads "
        "as a wide oval filling most of the picture. This is a "
        "semiconductor wafer, not a metal plate: its face is a glassy, "
        "almost black mirror, so smooth and specular that it behaves like "
        "a dark reflecting pool, showing a soft dark reflection of the "
        "room and a cluster of pale blurred ceiling light panels floating "
        "in its surface, with a narrow band of iridescent rainbow "
        "diffraction — magenta, green, gold — smeared along one curved "
        "edge where the light grazes it, and a faint even rectilinear "
        "grid of identical rectangular die sites visible as a ghost "
        "lattice across the whole face, thousands of tiny repeated "
        "squares in neat rows and columns. The surface is absolutely not "
        "brushed metal: no concentric rings, no radial scratch pattern, "
        "no spun-aluminium swirl, no drum skin, no polished steel "
        "sheen. Only a scatter of minute dust specks catches single "
        "points of light across the dark mirror, and the wafer's polished "
        "chamfered rim catches a thin hard highlight where it meets the "
        "matte surface, with a soft cool shadow pooling under the near "
        "edge. Behind and above, thrown far out of focus into smooth "
        "planes of pale grey-white and cool blue, the plain matte "
        "housings of fab process equipment stand as soft vertical masses "
        "without detail. Cool white cleanroom light from overhead, soft "
        "and even, one gentle specular streak across the disc. "
        "Photographic, very shallow depth of field with the near rim, the "
        "dust specks and one patch of the die lattice tack sharp, the far "
        "edge of the disc already softening into creamy bokeh." + PHOTO_TAIL
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


if __name__ == "__main__":
    main()
