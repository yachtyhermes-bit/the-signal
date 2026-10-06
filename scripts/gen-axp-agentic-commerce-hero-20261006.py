#!/usr/bin/env python3
"""Generate hero for axp-agentic-commerce-playbook-2026 (fal flux/schnell).

Subject: American Express releases a merchant playbook and advisory council for
agentic commerce — autonomous AI shopping agents transacting over a closed-loop
card network. Theme: high-end retail point of sale, premium payments, trust.

Frames chosen (photo-realistic editorial stock only):
  1 — sleek contactless payment terminal on a dark polished marble boutique
      counter, upscale leather wallet beside it, luxury retail goods in soft
      focus behind, warm ambient lighting.
  2 — tighter three-quarter close-up of a contactless card being tapped on a
      terminal at a boutique counter, shallow depth of field.
  3 — wide boutique interior shot past a marble counter with the terminal
      foregrounded and elegant shelves softly out of focus.

Deliberately NOT (banned): no data centre, no server room, no server racks, no
glowing cable runs, no neon / synthwave colour, no abstract digital art, no
geometric patterns, no glowing lines, no holograms, no robots, no charts /
graphs / dashboards / floating UI, no 3D render / CGI / video-game look, no
readable text of any kind, no logos, no letters, no words, no brand marks.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock ONLY: available warm light, real sensor noise,
  shallow depth of field, genuine material textures. No CGI sheen.
- TEXT-FREE: terminals, cards, screens, signage and packaging all invite
  lettering, so every surface is explicitly unmarked and every screen blank.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-axp-agentic-commerce-hero-20261006.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "axp-agentic-commerce-playbook-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no ticker "
    "symbols, no price tags with numbers, no printed prices, no signage "
    "with words, no shop signage, no window decals with writing, no "
    "branding anywhere, no brand names, no manufacturer names, no retailer "
    "names, no corporate logos, no trademarks, no watermarks, no "
    "signatures, no graffiti, no handwriting, no documents, no receipts "
    "with writing, no paperwork, no newspapers, no magazines, no labels, "
    "no tags, no stickers, no decals, no embossed lettering, no engraved "
    "lettering, no monograms, no bank names, no card network logos, no "
    "card numbers, no cardholder names, no expiry dates, no security codes, "
    "no screen text of any kind, no digital display readouts, no legible "
    "writing of any kind anywhere in the image. Every screen and display "
    "in the scene is completely dark or showing only an abstract soft "
    "glow with no characters, and every card, wallet, box and package is "
    "completely plain and unlettered. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game still, no concept art, "
    "no matte painting, no neon, no synthwave colour, no glowing lines, "
    "no light trails, no abstract geometric art, no floating holographic "
    "elements, no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no user interface overlays, no data centre, no server "
    "room, no server racks, no server aisles, no cable runs, no GPU racks, "
    "no racks of any kind, no robots, no drones, no lasers, no holograms."
)

COMMON = (
    "This is upscale editorial lifestyle stock photography for a business "
    "newspaper, a real photograph and not a render: available warm ambient "
    "light, honest exposure, not a harshly lit studio set and not an HDR "
    "composite. Shallow depth of field from a wide aperture on a 35mm lens "
    "on a full-frame camera, real optical lens blur and creamy natural "
    "bokeh, unobtrusive film-like grain visible in the smooth mid-tones, "
    "a subtle lens vignette, slight sensor softness in the shadows, "
    "asymmetric unidealised composition, a slight hand-held tilt, "
    "photorealistic, very high detail, natural colour, no plastic CGI "
    "sheen, no glossy render, no perfect symmetry, no immaculate over-"
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "professional editorial magazine quality, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — sleek contactless payment terminal on a dark polished marble
    #     boutique counter, upscale leather wallet beside it, luxury retail
    #     goods softly out of focus in the background, warm ambient light.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera from a slightly low counter-level "
        "angle, of a sleek modern contactless card payment terminal resting "
        "on a dark polished marble boutique counter. The terminal is the "
        "sharp, centred hero of the frame: a minimalist matte-black and "
        "brushed-metal reader with a gently angled face, a smooth blank "
        "display gently catching a soft warm reflection, and a slender "
        "sensor strip along its edge, entirely unbranded and plain with no "
        "lettering, no logos and a completely dark unlit screen. Immediately "
        "beside the terminal on the right, tack sharp and partly cropped by "
        "the frame edge, rests an upscale tan leather wallet, softly worn "
        "with visible stitching and natural grain, lying closed and plain "
        "with no embossing or lettering. The counter beneath is dark "
        "polished marble with warm veining, its surface catching long soft "
        "highlights and reflecting the terminal faintly. In the background, "
        "thrown well out of focus into soft creamy bokeh, the interior of "
        "an elegant luxury retail boutique: warm timber shelving with "
        "abstract unlabelled objects at rest, a soft folded cashmere scarf "
        "in muted cream, a slim glass vase, all reduced to gentle shapes "
        "and warm highlights with no readable detail. The lighting is warm, "
        "natural and ambient, like late-afternoon light through a shop "
        "window, falling softly from the upper left and gently wrapping the "
        "metal edge of the terminal. The mood is quiet, refined and "
        "expensive. No people are visible. Nothing in the scene carries any "
        "writing of any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — tighter three-quarter close-up of a contactless card being tapped
    #     on the terminal at a boutique counter, shallow depth of field.
    "2": (
        "Photo-realistic editorial stock photograph, shot on a 50mm lens at "
        "f/2.2 on a full-frame camera from a close three-quarter angle a "
        "little above counter height, of the moment a plain unbranded "
        "contactless bank card is held a few centimetres above a sleek "
        "modern payment terminal on a dark polished marble boutique "
        "counter. The terminal is tack sharp and off-centre to the left: a "
        "minimalist matte-black and brushed-metal reader with a gently "
        "angled face and a smooth blank display glowing only a faint soft "
        "wash of light with no characters, entirely unbranded with no "
        "lettering or logos. Hovering above its sensor area, a slim "
        "matte-finish metallic card, entirely plain on its visible face "
        "with no card numbers, no bank name, no network logo and no "
        "lettering of any kind, held by a hand that enters the frame from "
        "the upper right, softly out of focus. The dark polished marble "
        "surface below catches a crisp reflected highlight and a faint "
        "mirror image of the terminal and card. In the warmly blurred "
        "background, the boutique interior dissolves into soft shapes: "
        "dark timber shelving, a folded textile in muted cream, warm "
        "reflections off polished surfaces, all far out of focus and "
        "unreadable. The light is warm and ambient, raking gently from the "
        "left and glinting along the brushed-metal edge of the terminal and "
        "the flat face of the card. Rich contrast, warm tones, an air of "
        "quiet premium retail. No readable text anywhere in the scene. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wide boutique interior shot past the marble counter with the
    #     terminal foregrounded and elegant shelves softly out of focus.
    "3": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.5 on a full-frame camera from a standing eye-level position at "
        "the edge of a boutique sales counter, looking across the counter "
        "into the shop. In the near foreground, tack sharp and resting on a "
        "dark polished marble counter that runs across the lower third of "
        "the frame, sits a sleek modern contactless payment terminal: a "
        "minimalist matte-black and brushed-metal reader with a gently "
        "angled face and a smooth blank display glowing a faint soft wash "
        "with no characters, completely unbranded with no lettering or "
        "logos. Beside it, softly catching the light and partly cropped by "
        "the right edge, lies an upscale tan leather wallet, closed and "
        "plain with visible stitching and natural grain but no embossing "
        "or lettering. The dark marble counter shows warm veining, long "
        "soft highlights and faint reflections of the terminal and wallet. "
        "Beyond the counter the elegant boutique interior falls gradually "
        "out of focus: warm timber shelving along the walls holding "
        "abstract unlabelled objects and folded textiles in muted cream, "
        "dusty rose and soft green, a slim glass vase, a low display table "
        "with an object under a soft cloth, all dissolving into creamy "
        "bokeh with no readable detail. The lighting is warm, natural and "
        "ambient, like afternoon window light drifting through the shop, "
        "gently modelling the metallic face of the terminal and glowing on "
        "the marble. The atmosphere is quiet, refined, expensive and "
        "unhurried. No people are visible. Nothing in the scene carries any "
        "writing of any kind. No readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — even tighter macro-feel shot on the terminal's contactless zone
    #     with a luxury shopping bag soft in the background.
    "4": (
        "Photo-realistic editorial stock photograph, shot on a 85mm lens at "
        "f/1.8 on a full-frame camera from a close counter-level angle, of a "
        "sleek modern contactless payment terminal on a dark polished "
        "marble boutique counter, framed tightly so the device fills much "
        "of the lower frame. The terminal is razor sharp: a minimalist "
        "matte-black and brushed-metal reader with a gently angled face, a "
        "smooth blank display glowing only a faint warm wash with no "
        "characters, and a subtly defined contactless sensor area, "
        "completely unbranded with no lettering of any kind. A plain "
        "unbranded matte card rests flat on the marble just in front of it, "
        "its visible face entirely blank with no numbers, no bank name and "
        "no network logo. The dark polished marble catches crisp reflected "
        "highlights and a faint mirror image of the terminal. Behind it, "
        "thrown far out of focus into creamy bokeh, the corner of a "
        "premium paper shopping bag in warm muted tone and the edge of a "
        "soft folded textile, both plain and unlettered, dissolving into "
        "gentle abstract shapes. The lighting is warm and ambient, raking "
        "softly from the upper right, glinting on the brushed metal and "
        "gently glowing on the marble. Shallow focus isolates the terminal; "
        "rich warm tones, an air of understated luxury. No people are "
        "visible. Nothing in the scene carries any writing of any kind. No "
        "readable text anywhere. "
        + COMMON
        + NO_TEXT
    ),
    # 5 — wider refined boutique counter still life: terminal, wallet and a
    #     luxury watch/cufflink tray, warm architectural background.
    "5": (
        "Photo-realistic editorial stock photograph, shot on a 40mm lens at "
        "f/2.2 on a full-frame camera from a gentle three-quarter angle at "
        "counter height, of a refined still life arranged on a dark "
        "polished marble boutique counter. Towards the centre-right, tack "
        "sharp, sits a sleek modern contactless payment terminal: a "
        "minimalist matte-black and brushed-metal reader with a gently "
        "angled face and a smooth blank display glowing a faint soft wash "
        "with no characters, completely unbranded with no lettering or "
        "logos. To its left lies an upscale tan leather wallet, closed and "
        "plain with fine visible stitching and natural grain but no "
        "embossing or lettering, and beyond it a shallow open tray of "
        "unbranded luxury small objects rendered as soft warm metallic "
        "shapes. The dark polished marble counter shows rich veining, long "
        "soft highlights and faint reflections of everything upon it, and "
        "its front edge is cropped by the bottom of the frame. Behind the "
        "counter the boutique dissolves into warm out-of-focus bokeh: dark "
        "timber panelling, a sliver of a soft-lit display case, a folded "
        "textile in muted cream, all unreadable and abstract. The lighting "
        "is warm and ambient, drifting in from the upper left like late-"
        "afternoon shop light, glinting along the brushed-metal edges and "
        "softly glowing on the marble. Quiet, refined, premium and "
        "unhurried. No people are visible. Nothing in the scene carries any "
        "writing of any kind. No readable text anywhere. "
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
