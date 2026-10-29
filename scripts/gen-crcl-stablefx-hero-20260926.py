#!/usr/bin/env python3
"""Generate hero for crcl-stablefx-onchain-settlement-rails-2026 (fal flux/schnell).

Subject: Circle Internet Group (CRCL) put a 24/7 stablecoin foreign-exchange
settlement engine live on its Arc blockchain. The article is about stablecoins
becoming payment / settlement infrastructure for businesses — card settlement,
FX settlement, money moving around the clock instead of through overnight
banking rails.

Frame chosen: SCENE (a) THE RETAIL CHECKOUT — a close-up of a customer tapping a
contactless bank card on a modern plain payment terminal at a shop counter.
This is human, warm, instantly legible, and visually distinct from the data
centre / server hallway heroes used on other articles.

Deliberately NOT (banned): no data centre, no server room, no server aisle, no
server racks, no glowing cables, no neon / synthwave colour, no abstract digital
art, no geometric patterns, no glowing wireframe lines, no holograms, no robots,
no long data-centre hallway of any kind. No readable text anywhere.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. Prior attempts on other
  heroes read as CGI renders, so the prompt leans hard on documentary cues:
  available window light, sensor noise, wear, clutter, imperfect handheld
  framing, shallow depth of field.
- TEXT-FREE is the hard one here: cards, terminals, screens and shop signage
  all invite lettering, numbers and logos, so every display is explicitly
  blank and every surface explicitly unmarked.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-crcl-stablefx-hero-20260926.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "crcl-stablefx-onchain-settlement-rails-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no price "
    "figures, no currency symbols, no dollar signs, no euro signs, no "
    "pound signs, no percent signs, no ticker symbols, no stock tickers, "
    "no stencilled codes, no serial numbers, no account numbers, no card "
    "numbers, no expiry dates, no embossed digits on the card, no printed "
    "name on the card, no bank name on the card, no network mark on the "
    "card, no chip artwork, no receipt text, no printed receipts at all, "
    "no signage, no shop signs, no shelf labels, no price tags, no "
    "placards, no posters, no hanging signs, no menu boards, no branding "
    "anywhere, no brand names, no manufacturer names, no company names, "
    "no corporate logos, no trademarks, no watermarks, no signatures, no "
    "barcodes, no QR codes, no data-matrix codes, no loyalty cards with "
    "writing, no graffiti, no handwriting, no documents, no clipboards "
    "with writing, no brochures, no newspapers, no magazines, no labels, "
    "no tags, no stickers, no decals on any surface, no legible writing of "
    "any kind anywhere in the image. Every card, terminal, keypad, "
    "receipt roll, screen, monitor, tablet, display and machine readout is "
    "entirely blank, dark or softly out of focus with no readable content "
    "at all — the payment terminal's little display is dark and shows "
    "nothing, its keypad carries only plain unmarked key caps with no "
    "characters on them, and the card in the hand is plain matte plastic "
    "with no markings of any kind. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no video-game still, no concept art, "
    "no matte painting, no neon, no synthwave colour, no glowing lines, no "
    "light trails, no lens-flare trails, no abstract geometric art, no "
    "floating holographic elements, no augmented-reality graphics, no "
    "wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no screens full of data, no data centre, no server "
    "room, no server racks, no server aisles, no cable runs, no GPU racks, "
    "no racks of any kind."
)

COMMON = (
    "This is unposed documentary reportage caught in a single unrehearsed "
    "moment, not a staged commercial product shot and not a hero render: "
    "the subject sits off-centre, the framing is loose and a little "
    "careless, and foreground clutter cuts into the bottom of the frame. "
    "Warm late-afternoon window light rakes in from the left of the camera, "
    "soft and directional, catching the top edges of the hardware and "
    "falling into genuinely deep shadows; ambient bounce from a neighbouring "
    "white surface fills the shadow side just a little. Honest available-light "
    "exposure, not a lit studio set. Shallow depth of field from a wide "
    "aperture on a full-frame camera, real optical lens blur and creamy "
    "natural bokeh behind the subject, unobtrusive grain visible in the "
    "smooth mid-tones, faint chromatic fringing on high-contrast edges, a "
    "subtle lens vignette, slight sensor softness in the shadows, dust "
    "motes in the air catching the light, scuffed worn surfaces with real "
    "fingerprints, smears, scratches and grime on every object, asymmetric "
    "unidealised composition, no plastic CGI sheen, no glossy render, no "
    "perfect symmetry, no immaculate showroom cleanliness, no retouched "
    "hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial stock "
    "photography for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — close-up of a customer tapping a contactless bank card on a modern
    #     payment terminal on a shop counter.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 50mm lens at "
        "f/2.0 on a full-frame camera at close range, of a customer paying "
        "at a shop counter by tapping a plain contactless bank card on a "
        "small modern payment terminal. The terminal is tack sharp in the "
        "centre-right of frame and sits slightly off-centre, tilted a few "
        "degrees: a compact matte black and light grey card reader on a low "
        "angled stand, its rounded body plainly unmarked, a small dark "
        "rectangular display screen that is completely blank and off, a "
        "row of plain blank key caps with no characters on them, and the "
        "reader's flat contactless sensing face angled up toward the top "
        "left of the frame. A bare hand comes in from the left of frame, "
        "sharply in focus at the fingertips, holding a plain unbranded "
        "matte plastic card — cool grey-blue card stock with a bare metal "
        "chip only, absolutely no bank name, no network mark, no embossed "
        "digits, no printed characters of any kind — hovering a couple of "
        "centimetres above the sensing face in the act of tapping, the "
        "fingers relaxed and natural with a clean short fingernail and "
        "honest skin texture showing fine lines and pores. The terminal "
        "body is real-world worn: dust and a faint smudge across the "
        "screen bezel, a scuffed corner, a hairline scratch on the palm "
        "rest, a thin cable running off the bottom edge of the frame out "
        "of focus. On the counter around it, softly out of focus in the "
        "near foreground and cropped by the bottom of the frame, sit the "
        "clutter of a working till point: a loose coil of receipt paper "
        "with nothing printed on it, a small stack of plain blank cards "
        "with no writing, a paper cup lid, a couple of coins, and the edge "
        "of a wooden counter worn pale along its lip. Behind and to the "
        "right, rendered in soft creamy bokeh, a shop interior recedes: "
        "out-of-focus shelves of plain boxes, a hanging pendant lamp "
        "blooming gently, a blurred figure of a shop assistant in a plain "
        "dark apron turned away from camera, and a tall window pouring "
        "warm late-afternoon light across the scene. No readable text "
        "anywhere in the shop, no signs, no labels, no price tags. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — tighter macro-adjacent version of the tap, terminal dominant.
    "2": (
        "Photo-realistic editorial stock photograph, shot on an 85mm lens "
        "wide open at f/1.8 on a full-frame camera from just above counter "
        "height, of the moment a customer taps a plain bank card against a "
        "compact modern payment terminal at a retail till. The terminal "
        "fills the lower right two-thirds of the frame, angled three-quarter "
        "toward camera and tack sharp: a small matte dark grey rectangular "
        "card reader with a soft matte finish, absolutely unmarked, with a "
        "tiny completely blank unlit display and a set of plain blank "
        "rounded key caps carrying no characters at all, mounted on a low "
        "black stand and connected by a thin cable that runs out of the "
        "bottom edge of the frame. Above it in the top left of the frame, "
        "crisp at the fingertips and softly blurred toward the wrist, a "
        "bare hand holds a plain unbranded matte white plastic card by its "
        "edge, hovering a centimetre from the reader's sensing face, "
        "mid-tap: the card carries only a bare metal chip with no bank "
        "name, no logo, no network symbol and no embossed or printed "
        "digits whatsoever, and the hand shows natural skin texture, fine "
        "creases and a clean short nail. The counter beneath is a worn "
        "wood-grain surface with real grain, a few faint scratches, a "
        "dusting of crumbs and a smear of spilled liquid catching the "
        "light, and in the soft foreground bottom left, out of focus, a "
        "folded plain till receipt with nothing printed on it, a small "
        "green potted plant, and the blurred base of a glass display. "
        "Behind everything a bright shop interior dissolves into creamy "
        "bokeh: plain out-of-focus shelving, a warm pendant light, and the "
        "soft silhouette of a customer further away with their back turned, "
        "unidentifiable and out of focus. Warm directional late-afternoon "
        "light comes in from the left, the highlights catching the leading "
        "edge of the card and the top rim of the reader, the shadows "
        "falling genuinely deep. No readable text anywhere, no signage, "
        "no labels, no numbers, no logos. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider: customer at the counter tapping, assistant in soft focus
    #     behind, whole scene.
    "3": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera in warm late-afternoon window light "
        "inside a small modern shop, of a customer paying by tapping a "
        "plain contactless bank card on a payment terminal on the counter, "
        "seen in three-quarter view from slightly behind and to the side of "
        "the customer. The customer is a person in a plain unmarked pale "
        "shirt, seen from the side and rear so the face is only partly "
        "visible and unidentifiable, left arm extended to the counter in "
        "the sharp middle of frame, hand holding a plain unbranded matte "
        "grey card with only a bare metal chip and no bank name, no logo "
        "and no printed characters, the card just touching the top face of "
        "a small matte black unmarked card reader standing on a low angled "
        "stand on the wooden counter. The reader has a completely blank "
        "unlit display and plain blank key caps with no characters on "
        "them, its body scuffed and lightly dusty, a thin cable trailing "
        "off. On the counter around the terminal, softly out of focus, lie "
        "the ordinary clutter of a till point: a loose curl of blank "
        "receipt paper, a couple of coins, a plain paper bag with no "
        "printing on it, a pen, and a small plain card-holder. Across the "
        "counter on the right of frame, soft and out of focus, a shop "
        "assistant in a plain dark apron stands facing the customer, "
        "partly turned away, their dark hair catching the window light, "
        "their face angled away and unidentifiable, no badge, no name tag "
        "and no logo on the apron. Behind them the shop recedes into "
        "warm creamy bokeh: plain undetailed shelves, a few out-of-focus "
        "boxes with no writing on them, and a tall window on the left "
        "pouring soft directional daylight across the counter with dust "
        "motes floating in the beam. Everything is calm, ordinary and "
        "workmanlike. No readable text anywhere in the scene, no signage, "
        "no labels, no price tags, no numbers, no logos. "
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
