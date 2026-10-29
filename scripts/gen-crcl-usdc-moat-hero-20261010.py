#!/usr/bin/env python3
"""Hero regen for crcl-usdc-moat-consortium-trust-charter-2026 via fal flux/schnell.

Subject: Circle (CRCL) / USDC — the moat question is the stablecoin FLOAT (interest
on reserves) and a distribution revolt. Prior hero = neoclassical bank facade in a
financial district. It FAILED QC: a blue streetlamp banner rendered as AI letter-soup
("Tlh& CUAL") and carved facade text was garbled.

Fix: keep the institutional-finance concept but remove every signage-prone surface.
Frame on monumental architecture only — columns, stone, bronze — with no banners,
placards, signs, awnings, addresses or carved words anywhere.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-crcl-usdc-moat-hero-20261010.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "crcl-usdc-moat-consortium-trust-charter-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTDIR = "/home/chino/thesignal/public/img/articles"
OUTPUT = f"{OUTDIR}/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no letters, "
    "no words, no numbers, no numerals, no digits, no engraved inscriptions, "
    "no carved inscriptions or names on stonework, no chiselled lettering on "
    "any pediment, frieze, architrave or lintel, no cornerstone plaques, no "
    "bronze nameplates, no memorial plaques, no building addresses, no street "
    "numbers, no street name plates, no hanging banners, no fabric banners, no "
    "flag banners, no lamppost banners, no pennants, no flags, no pennant "
    "string, no awnings with writing, no signs, no signage, no shopfront signs, "
    "no directional signage, no traffic signs, no road markings with symbols, "
    "no painted letters on the road, no posters, no hoardings, no billboards, "
    "no advertising panels, no window decals, no signage of any kind, no "
    "branding, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no emblems with lettering, no monograms, no trademarks, "
    "no watermarks, no signatures, no graffiti, no handwriting, no printed "
    "documents, no newspapers, no magazines, no brochures, no clipboards, no "
    "barcodes, no QR codes, no labels, no tags, no stickers, no decals, no "
    "legible writing of any kind anywhere in the image. Every possible "
    "text-bearing surface — banners, flags, signs, plaques, stone friezes, "
    "window glass, doors and lintels — is entirely plain, blank or unmarked, "
    "with absolutely no readable content at all. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no video-game still, no concept "
    "art, no matte painting, no neon, no synthwave colour, no glowing lines, no "
    "light trails, no abstract geometric art, no floating holographic elements, "
    "no augmented-reality graphics, no wireframe, no charts, no graphs, no "
    "dashboards, no data visualisation, no data centre, no server room, no "
    "server racks, no cryptocurrency imagery, no coin graphics, no bitcoin, no "
    "digital-currency symbols."
)

COMMON = (
    "This is unposed documentary reportage caught in a single unrehearsed "
    "moment, not a staged commercial architectural shoot and not a hero render: "
    "the subject sits off-centre, the framing is loose and a little careless, "
    "and foreground elements cut into the bottom of the frame. Warm "
    "late-afternoon sunlight rakes in from the left of the camera, soft and "
    "directional, catching the top edges of the stone and metalwork and falling "
    "into genuinely deep shadows; ambient bounce from a neighbouring pale "
    "surface fills the shadow side just a little. Honest available-light "
    "exposure, not a lit studio set. Shallow depth of field from a wide "
    "aperture on a full-frame camera, real optical lens blur and creamy natural "
    "bokeh behind the subject, unobtrusive grain visible in the smooth "
    "mid-tones, faint chromatic fringing on high-contrast edges, a subtle lens "
    "vignette, slight sensor softness in the shadows, dust motes in the air "
    "catching the light, weathered and lightly stained real stone with genuine "
    "patina, asymmetric unidealised composition, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no immaculate showroom cleanliness, no "
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic, "
    "photorealistic, very high detail, professional editorial stock photography "
    "for a business newspaper, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — close, low-angle on monumental fluted stone columns of an old bank
    #     building; no facade signage in frame at all.
    "1": (
        "Photo-realistic editorial stock photograph, shot on a 35mm lens at "
        "f/2.8 on a full-frame camera from a low three-quarter angle, of the "
        "monumental fluted stone columns and deep entrance recess of a century-"
        "old neoclassical bank building on a downtown financial street. Three "
        "enormous warm limestone columns rise out of the top of the frame, "
        "tack sharp, their fluting and weathered capitals filling the right "
        "two-thirds of the image; between and behind them the entrance recess "
        "falls into deep shadow, its smooth polished stone entirely plain with "
        "no carving, no lettering and no plaque anywhere. The columns stand on "
        "a broad worn granite step with a scuff-marked foot-polished threshold. "
        "A single anonymous pedestrian in a plain dark coat crosses the lower "
        "left of frame in soft motion blur, out of focus, face turned away and "
        "unidentifiable. Far down the street on the left, dissolved into creamy "
        "bokeh, the faces of newer glass towers rise into a pale hazy sky. Warm "
        "late-afternoon sun rakes across the stone from the left, catching the "
        "leading edges of the flutes and the swelling of the capitals, shadows "
        "falling genuinely deep and cool. Fine dust hangs in the light. No "
        "readable text anywhere in the scene — no banners, no signs, no "
        "plaques, no carving, no lettering on the stone. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — interior of an empty classical banking hall: marble columns and brass
    #     teller grilles, no signage anywhere.
    "2": (
        "Photo-realistic editorial stock photograph, shot on a 24mm lens at "
        "f/2.8 on a full-frame camera inside an empty grand classical banking "
        "hall, of tall polished marble columns marching down the left side of "
        "frame beneath a coffered ceiling, with a long row of ornate brass "
        "teller grilles receding down the right into creamy bokeh. A single "
        "long shaft of warm late-afternoon light falls through a high clerestory "
        "window across the polished stone floor, catching floating dust motes. "
        "The hall is completely deserted and the surfaces are entirely plain: "
        "the marble walls, counters and grilles carry no carved names, no "
        "plaque, no inscription and no signage of any kind, and the floor is "
        "bare polished stone with no markings. Worn brass, faint scuffs and real "
        "patina on the metalwork, deep falloff into shadow between the columns, "
        "warm directional light from the left. No readable text anywhere — no "
        "signs, no plaques, no teller notices, no carved lettering, no banners, "
        "no currency symbols, no coin imagery. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — tight abstract-ish detail: weathered stone column base and gilt-bronze
    #     door hardware, no signage in frame at all.
    "3": (
        "Photo-realistic editorial stock photograph, shot on an 85mm lens wide "
        "open at f/1.8 on a full-frame camera at close range, of the weathered "
        "carved stone base of a monumental fluted column leading the eye toward "
        "the polished dark timber and gilt-bronze hardware of a heavy old bank "
        "door at the right edge of frame. The stone base is tack sharp — real "
        "limestone with chips, stains, hairline cracks and a century of patina — "
        "and the door stands partly open on a plain unmarked dark panel with a "
        "large brass pull handle and an escutcheon, entirely free of any plate, "
        "name or lettering. Beyond the gap a warm interior glow spills out onto "
        "the scuffed polished step. Warm directional late light rakes from the "
        "left across the stone, deep cool shadows to the right, dust in the "
        "beam. No readable text anywhere in the scene: no plaques, no nameplates, "
        "no signs, no lettering, no numbers, no emblems with lettering. "
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


def generate(prompt, out_path, seed=None):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if seed is not None:
        args["seed"] = seed
    print("Generating image with fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    image_url = None
    if result.get("images"):
        image_url = result["images"][0]["url"]
    elif result.get("image"):
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: no image url: {result}")
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
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


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
        print(f"Re-saved higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
