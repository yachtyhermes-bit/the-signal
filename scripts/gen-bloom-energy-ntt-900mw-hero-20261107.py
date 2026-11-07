#!/usr/bin/env python3
"""Generate hero for bloom-energy-ntt-900mw-international-order-2026 (fal flux/schnell).

Subject: Bloom Energy solid-oxide fuel cell "Energy Server" cabinets — shipping-
container-scale units that make electricity on-site from natural gas. Bloom just
signed 900 MW with NTT Global Data Centers.

Scene (per brief): a large array of matte-grey industrial solid-oxide fuel cell
cabinets installed outdoors on a concrete pad beside a modern data center
building, with visible gas piping and electrical conduit, golden hour. Industrial
power-plant photography, NOT a data-center hallway / server aisle / server room.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-bloom-energy-ntt-900mw-hero-20261107.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "bloom-energy-ntt-900mw-international-order-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080
R2_URL = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/{SLUG}.jpg"

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no decals, no adhesive tags, no barcodes, no QR codes, no part "
    "numbers, no printed markings, no engraved nameplates, no riveted metal "
    "tags, no stencilled characters, no screen text, no instrument displays, no "
    "brand names, no manufacturer names, no company names, no logos, no "
    "watermark, no captions, no legible writing of any kind anywhere in the "
    "image. Every cabinet face, door, panel and pipe is plain, unmarked and "
    "uniform in colour, with no plates, stickers or labels attached. "
    "No people, no faces, no hands, no figures. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no overlay graphics, no abstract "
    "digital patterns. This is not a data-center hallway, not a server aisle, "
    "not a server room interior, not a corridor, not a tunnel of cabinets receding "
    "to a vanishing point: the camera is outdoors in open air."
)

STYLE = (
    "Realistic photo, shot on 35mm, shallow depth of field, professional "
    "lighting, natural daylight, photorealistic, very high detail, honest "
    "industrial textures, subtle film grain and real sensor noise, slightly "
    "imperfect framing and exposure, uneven weathering, no CGI sheen, no "
    "perfect symmetry, no spotless surfaces, 16:9 landscape composition. "
)

PROMPTS = {
    "1": (
        "Professional stock photograph of a large array of matte-grey industrial "
        "solid-oxide fuel cell cabinets installed outdoors on a concrete pad "
        "beside a modern data center building. Three long orderly rows of tall "
        "rectangular matte-grey steel fuel-cell cabinets, each about the size of "
        "a shipping container and plain and unmarked, stand bolted to a poured "
        "concrete pad in clean perspective, receding toward the right of the "
        "frame. Bright stainless gas piping runs along the top of the rows with "
        "insulated elbows and manual valves, and galvanised electrical conduit "
        "and cable tray run in neat parallel lines at ground level between the "
        "cabinets. Behind and to the left, the pale grey precast-concrete and "
        "glass wall of a large modern data center building rises out of frame, "
        "plain and windowless at ground level. Low golden-hour sunlight rakes "
        "across the cabinet faces from the left, long soft shadows on the "
        "concrete, warm light on the steel while the shadowed sides stay cool "
        "grey. Slightly low camera angle at eye level with the cabinets, "
        "looking down the row. " + STYLE + NO_TEXT
    ),
    "2": (
        "Professional stock photograph of an outdoor field of matte-grey "
        "solid-oxide fuel cell power modules on a concrete equipment pad at "
        "golden hour, photographed from a three-quarter oblique angle so the "
        "cabinets sit as staggered blocks across the frame rather than in a "
        "central corridor. In the right foreground, one container-scale "
        "matte-grey painted steel fuel cell cabinet stands plain and unmarked, "
        "its bolted panel seams, louvred vents, hinges and weathered lower edge "
        "sharp and detailed, a few faint water stains and scuffs on the paint. "
        "Behind it, two further rows of identical grey cabinets stand offset at "
        "different angles, some sides catching warm low sun, others in cool "
        "shadow, receding into soft focus. Above them a galvanised steel pipe "
        "rack carries stainless gas lines with flanged joints and plain "
        "handwheel valves, and black electrical conduit runs down the rear of "
        "the nearest cabinet into a sealed enclosure at its base. Behind "
        "everything, the long blank service wall of a modern data center "
        "building — grey ribbed metal cladding, a couple of plain louvred "
        "exhaust vents, no windows and no doors at ground level — fills the "
        "upper left background and runs out of frame. Cracked, patched concrete "
        "with expansion joints, a little windblown grit, dry weeds at the pad "
        "edge. Late golden-hour sun rakes in from the lower left, long soft "
        "shadows, warm haze in the air. " + STYLE + NO_TEXT
    ),
    "3": (
        "Professional stock photograph of an outdoor industrial fuel cell "
        "generating yard beside a hyperscale data center at golden hour, taken "
        "from a slightly raised corner viewpoint looking diagonally across the "
        "installation. A large array of matte-grey container-scale solid-oxide "
        "fuel cell cabinets fills the frame in four parallel banks laid on a "
        "swept concrete pad, the rows angled across the picture rather than "
        "running straight away from the camera, so the assembly reads as a wide "
        "staggered field of grey boxes. Overhead, galvanised steel pipe racks "
        "with stainless gas lines and clusters of handwheel valves run between "
        "the banks, and shallow concrete cable trenches with steel covers and "
        "black conduit run along the pad. The long blank flank of a modern data "
        "center building closes the composition on the right — grey ribbed metal "
        "cladding, a flat roofline, a few plain louvred vents, windowless at "
        "ground level — with a second lower building block and a substation "
        "transformer behind it. A chain-link fence and a strip of dry gravel and "
        "weeds edge the near foreground. Warm low golden sunlight from the left "
        "lights the cabinet tops and pipework, long soft shadows stretch across "
        "the concrete between the banks, and the sky is clean pale blue fading "
        "to warm haze at the horizon. " + STYLE + NO_TEXT
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT} (hard cap: 1-3)")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    quality = 92
    img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and quality > 60:
        quality -= 4
        img.save(OUTPUT, "JPEG", quality=quality, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}  q={quality}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")

    if os.environ.get("R2", "1") == "1":
        print("\nUploading to R2 via r2_upload.py...")
        rc = os.system(f"cd /home/chino/thesignal && /home/chino/video-venv/bin/python3 scripts/r2_upload.py hero {SLUG}")
        if rc != 0:
            print(f"R2 upload FAILED (exit {rc})")
        else:
            try:
                resp = requests.head(R2_URL, timeout=30)
                print(f"R2 verify HTTP {resp.status_code}: {R2_URL}")
            except Exception as e:
                print(f"R2 verify error: {e}")
    with open("/home/chino/thesignal/.last_hero_prompt.txt", "w") as f:
        f.write(f"SLUG={SLUG}\nATTEMPT={ATTEMPT}\n\n{prompt}\n")


if __name__ == "__main__":
    main()
