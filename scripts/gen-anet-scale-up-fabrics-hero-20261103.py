#!/usr/bin/env python3
"""Hero for anet-ethernet-scale-up-fabrics-2026 (fal flux/schnell).

Subject: Arista Networks — high-speed Ethernet switches plus the EOS network
operating system that link AI accelerator clusters; Ethernet moving into the
scale-up network inside an AI rack.

Scene: a networking lab / optics bench, NOT a data centre. Tight
photo-realistic close-up of a network engineer's hands seating a pluggable
optical transceiver (QSFP/OSFP module) into a high-density Ethernet switch
port. Real metal, real moulded plastic, visible port cages, shallow depth of
field, cool neutral working light, soft out-of-focus instrument shapes behind.

Deliberately NOT a data-centre hallway / server aisle / rack row (banned
site-wide), NOT a server room, NOT neon / synthwave / glowing lines, NOT
digital art, NOT 3D render or CGI, NOT abstract, NOT geometric pattern.

Rules:
- PHOTO-REALISTIC editorial photograph only.
- TEXT-FREE: no letters / numbers / labels / logos / port numbers / silkscreen
  markings / screens / signage anywhere.
- Generate 1536x864, save <=400KB, mirror EXACT SAME BYTES to _backup_dist.

HARD CAP: 3 fal flux/schnell generations (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-anet-scale-up-fabrics-hero-20261103.py
"""
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "anet-ethernet-scale-up-fabrics-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "The image is completely free of lettering of any kind: no text, no "
    "words, no letters, no numbers, no signage, no wall signs, no warning "
    "placards, no equipment nameplates, no asset tags, no barcode stickers, "
    "no labels on any machine, no printed paper, no clipboards, no monitor "
    "screens, no digital readouts, no control panels with characters, no "
    "user interface, no dashboards. The switch faceplate is completely "
    "blank: absolutely no silkscreen printing, no port numbering, no "
    "channel identifiers, no engraved part codes, no moulded-in text on "
    "the plastic housings, no text on the transceiver module and no text on "
    "its pull tab. No brand names, no company names, no corporate logos, no "
    "trademarks, no watermarks, no signatures. Not an illustration, not "
    "digital art, not a 3D render, not CGI, not a matte painting, no neon, "
    "no synthwave, no glowing light trails, no geometric pattern overlay, "
    "no abstract shapes, no data visualisation graphics, no HUD overlay, no "
    "hologram, no circuit-board graphic. Not a data center, not a server "
    "room, not a server aisle, not rows of server racks, not a corridor of "
    "any kind, not a rack elevation, not an equipment showroom."
)

PHOTO_TAIL = (
    " Strictly photo-realistic editorial stock photography: real lens "
    "optics with honest optical blur, true-to-life materials, natural "
    "sensor noise, very fine film grain, subtle vignette, restrained "
    "true-to-life colour, no HDR, no plastic CGI sheen, no glossy render, "
    "no perfect symmetry. Horizontal 16:9 landscape composition, "
    "professional lighting, very high detail, tack-sharp focus on the "
    "hands and the transceiver."
)

PROMPTS = {
    # 1 — PRIMARY: hands seating a QSFP module into a switch port cage.
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 100mm macro lens at f/4 on a matte grey "
        "workbench in a networking test laboratory. A tight close-up, "
        "looking slightly down and across the front panel of a single "
        "high-density Ethernet switch chassis that occupies the left two "
        "thirds of the frame as a slab of dark anodised brushed aluminium "
        "with a row of rectangular port cages cut into its face. Both hands "
        "of a network engineer enter from the right edge of the frame, "
        "bare-skinned, short clean nails, fine hairs and knuckle creases "
        "catching the light, a plain black antistatic wrist strap looped "
        "loosely around the nearer wrist. The fingers of the right hand "
        "pinch the sides of a small pluggable optical transceiver module — "
        "a stubby rectangular cartridge about the size of a large eraser, "
        "its body a mix of die-cast silver-grey metal shell and matte "
        "black moulded plastic with a slim wire pull bail folded flat "
        "against its side — and are sliding it squarely into one of the "
        "port cages, the module already halfway home, its leading edge "
        "swallowed by the metal cage so only the rear third and the "
        "fingers remain outside. The left hand rests flat against the "
        "chassis edge, steadying it, thumb braced on the lip of the "
        "faceplate. The port cages are precisely cut rectangular tunnels "
        "in the aluminium, their thin stamped metal lips and internal "
        "spring fingers faintly visible, each neighbouring cage empty and "
        "dark inside with a shallow shadow in its throat; a fine seam runs "
        "along the panel and small torx screw heads sit flush at intervals. "
        "Cool neutral working light comes from a soft source high on the "
        "left, laying a clean silver sheen along the brushed aluminium, a "
        "crisp specular highlight on the module's metal shell, and a "
        "gentle falloff into shadow under the hands. Behind and above, "
        "thrown well out of focus into smooth planes of cool grey, stand "
        "the rounded matte housings of optical test instruments and a "
        "coiled grey measurement lead, reduced to soft unreadable shapes. "
        "Photographic, shallow depth of field: the fingertips, the "
        "transceiver shell and the near port cage tack sharp, everything "
        "behind dissolving into creamy bokeh." + PHOTO_TAIL
        + NO_TEXT
    ),
    # 2 — TIGHTER / FRONTAL: single hand, module mid-insertion, only a few
    #     cages in frame. Hardened after attempt 1 came back with printed
    #     port numbers on the faceplate and a rack-density read.
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 90mm macro lens at f/3.5 on an optics "
        "bench in a network hardware lab. An extremely tight macro view "
        "raking along the front edge of a single high-speed Ethernet switch "
        "standing on the bench, close enough that only FOUR rectangular "
        "port cages are inside the frame, the nearest one large in the "
        "lower left and the others marching away toward the upper right, "
        "each further cage smaller and softer until the last is a soft grey "
        "smudge. The faceplate between and around the cages is a plain dark "
        "graphite metal plate, finely bead-blasted rather than polished, "
        "and it is completely bare: no printed markings of any kind sit "
        "anywhere on it, just clean unbroken metal from edge to edge, with "
        "a single fine machined seam and one small flush screw head. The "
        "cage openings are square-shouldered cuts with razor-thin bright "
        "edges where light catches the stamped lip, and inside the nearest "
        "cage a thin metal retention spring and a row of gold contact "
        "fingers gleam in the shadow of the throat. One hand dominates the "
        "right of the frame — a man's hand, mid-thirties, skin warm and "
        "lightly lined, tendons and knuckle ridges reading clearly under "
        "the light — thumb and forefinger gripping a small pluggable "
        "optical transceiver by its ribbed plastic side cheeks and pushing "
        "it into the open cage, the module aligned dead square, three "
        "quarters inserted, the gold edge connector just disappearing into "
        "the slot. The module itself is a compact rectangular block: "
        "die-cast metal top shell with a faint tooled texture, matte black "
        "end cap, a small folded wire pull tab lying against its flank, a "
        "plain blank metal face with no sticker, no printed legend and no "
        "barcode anywhere on it. No other cable is plugged into the switch "
        "and no cable coils through the frame. Cool neutral overhead "
        "working light, slightly raking from the upper left, gives the "
        "metal a matter-of-fact industrial sheen and throws a soft short "
        "shadow from the hand across the panel; a cold pale reflection of "
        "an instrument housing slides across the top shell. Far behind, out "
        "of focus into smooth cool grey and faint white shapes, sit the "
        "corner of a bench power supply and the grey housing of an optical "
        "test set. Photographic, very shallow depth of field, real optical "
        "blur, the fingertips, the module's near corner and the bright cage "
        "lip in sharp focus." + PHOTO_TAIL
        + NO_TEXT
    ),
    # 3 — FALLBACK (sanctioned alternative): no hands. Macro of a bundle of
    #     yellow and aqua fibre patch cords fanning out of switch ports.
    #     Hardened after attempts 1-2 both came back with printed digits on
    #     the faceplate: the switch panel here is deliberately bare and is
    #     cropped off the top-left corner, the cords are the subject.
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on "
        "a full-frame camera with a 100mm macro lens at f/3.2 on a matte "
        "grey workbench in a networking laboratory. A tight macro still "
        "life of fibre-optic patch cords leaving a high-density Ethernet "
        "switch: in the extreme upper left corner of the frame, cropped by "
        "the edge so only a blank slab of it shows, a dark graphite metal "
        "faceplate runs off the picture with a few small rectangular port "
        "openings cut into it, its exposed surface bare unmarked metal "
        "with nothing printed, stamped or stencilled anywhere on it. From "
        "those ports a bundle of thin two-millimetre fibre-optic patch "
        "cords fans out toward the viewer and down to the right, the cords "
        "spreading apart and bowing in loose natural curves as they leave "
        "the panel and pass out of the bottom and right edges of the "
        "frame. Most of the cords are a saturated safety yellow, four or "
        "five of them a clear translucent aqua-teal, a couple pale grey; "
        "each one is a soft-touch jacketed cable about as thick as a "
        "pencil lead, its surface slightly matte with a faint bloom of "
        "dust and a long soft specular line of light running along its "
        "top, the aqua cords glowing faintly from within where the light "
        "passes through the translucent jacket. Near the panel each cord "
        "terminates in a small moulded plastic connector body with a slim "
        "latch and a short rubber strain-relief boot, seated squarely in "
        "its port, the connector shells a mix of black plastic and faintly "
        "translucent blue-grey, the boots wrinkled where they grip the "
        "cable, every connector body plain and blank with no sticker, no "
        "printed legend, no colour code tag, no barcode. The nearest "
        "connectors are large in frame and razor sharp, showing moulding "
        "seams, a little grit in the crevices and the slight sheen of "
        "handled plastic; further along the bundle the cords soften into "
        "blur and finally merge into a smooth out-of-focus mass of warm "
        "yellow and cool teal at the lower right. Cool neutral working "
        "light from high on the left, soft and even, a faint cool fill from "
        "the right, no coloured gels, no coloured lighting. Behind and "
        "above, thrown far out of focus into smooth planes of cool grey, "
        "the rounded matte housing of an optical test instrument sits as an "
        "unreadable shape. Photographic, very shallow depth of field, "
        "honest optical blur, natural grain, dust on the cable jackets, "
        "the nearest connector bodies and the first few centimetres of "
        "jacket in critical focus." + PHOTO_TAIL
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
