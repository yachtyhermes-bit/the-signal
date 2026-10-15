#!/usr/bin/env python3
"""Generate hero for dell-memory-cost-pass-through-2026 (fal flux/schnell).

Subject: Dell Technologies (NYSE: DELL) — AI server and PC manufacturing, and the
DRAM/NAND memory-cost squeeze. Component prices are rising on AI demand and Dell
is passing higher memory costs into server selling prices, so revenue climbs
partly because each machine costs more.

Scene chosen (must be visually DISTINCT from recent heroes and NOT a data-center
hallway / server aisle / rack room / cable runs through a building): a
PHOTO-REALISTIC editorial stock photograph of a COMPUTER AND SERVER FACTORY
ASSEMBLY FLOOR — an open rack-scale server chassis in the sharp foreground with
rows of DRAM memory modules seated in their slots, a tray of identical bare
memory sticks beside it, a green circuit board, an assembly jig or conveyor
surface, industrial factory lighting, shallow depth of field.

Rules:
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/CGI/HUD.
- TEXT-FREE: no writing, letters, numbers, logos, brand names, watermarks.
- No people, no faces, no hands anywhere in the frame.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-dell-memory-cost-pass-through-hero-20261015.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "dell-memory-cost-pass-through-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The scene is completely free of any writing: no text, no letters, no "
    "numbers, no words, no signage, no signs, no placards, no labels, no "
    "stickers, no barcodes, no QR codes, no part numbers, no serial numbers, no "
    "printed markings, no stencilled characters, no silkscreen text, no screen "
    "text, no instrument displays showing writing, no brand names, no "
    "manufacturer names, no logos, no watermark, no captions, no legible "
    "writing of any kind anywhere in the image. All equipment surfaces, test "
    "board silkscreen, connector bodies, oscilloscope and instrument panels are "
    "plain and unmarked. No people, no faces, no person in the scene, no hands "
    "in the frame, no arms. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no data-center hallway, no server aisle, no "
    "server racks, no cable runs through a building."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph of a computer and server "
        "factory assembly floor. In the sharp foreground, an open rack-scale "
        "server chassis sits on a matte steel assembly jig, its green printed-"
        "circuit motherboard exposed and filled with two long rows of identical "
        "DRAM memory modules seated upright and evenly spaced in their latching "
        "slots, the bare green cards and their gold edge contacts catching the "
        "light. Immediately beside the chassis, a shallow grey plastic tray "
        "holds a neat ranked row of identical loose memory sticks, unseated and "
        "waiting, their flat green surfaces and gold fingers clearly readable. "
        "Farther back along the assembly line, conveyor rails and the blurred "
        "silhouettes of more server chassis and component feed bins recede into "
        "smooth creamy bokeh. Industrial overhead factory lighting with cool "
        "white panels and a faint warm practical glow in the far background. "
        "Extremely shallow depth of field: the nearest DIMMs, the tray and the "
        "chassis edge are tack sharp while the assembly line behind melts away. "
        "Shot on a 90mm lens at f/2.8, real optical blur, honest industrial "
        "material textures of aluminium, fibreglass and solder, subtle sensor "
        "noise and fine film grain, no glossy CGI sheen, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "A real documentary photograph taken on a fast lens inside a high-volume "
        "electronics manufacturing plant, not a render and not computer "
        "generated. The frame looks along a server assembly bench: a wide open "
        "rack-mount server chassis dominates the sharp foreground, its lid "
        "removed, revealing a green motherboard densely populated with banks of "
        "unterseated DRAM memory modules standing upright in their slots and "
        "fine copper traces running away beneath them. To the left on the same "
        "bench rests a ribbed plastic tote of identical bare memory sticks laid "
        "in tidy parallel rows, their green circuit cards, gold contact edges "
        "and small black chips plainly visible. The bench itself is scuffed "
        "brushed steel on a rolling metal jig, with hex standoffs, a coil of "
        "flat ribbon cable and a small bin of screws nearby. Behind, completely "
        "out of focus, the long perspective of the factory floor shows the "
        "vague shapes of more assembly stations, overhead truss lighting and "
        "conveyor line hardware dissolved into soft bokeh. Cool white industrial "
        "overhead light with a warm sodium practical far in the background, "
        "honest natural shadows and believable reflections on the metal. Very "
        "shallow depth of field focused on the DIMM rows and the tray of loose "
        "memory sticks, everything behind blurred. Real optical blur, subtle "
        "lens vignette, believable sensor noise in the shadows, honest "
        "imperfect realism of a working factory, no perfect symmetry, no "
        "airbrushed surfaces, no plastic render look, no digital illustration, "
        "photorealistic, high detail, professional editorial stock photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "A real photograph shot with a fast prime lens on a factory assembly "
        "floor, the work of a professional industrial photographer, not a 3D "
        "visualisation and not an AI render. Tight three-quarter angle on an "
        "open rack-scale server chassis resting on a grey conveyor surface: the "
        "sheet-metal frame, the lift handles and the exposed green motherboard "
        "are rendered razor sharp, and seated in the board are long neat rows of "
        "vertical DRAM module sticks, their flat matte circuit cards and gold "
        "edge fingers picked out by pale light. Beside the chassis, a shallow "
        "moulded parts tray holds a batch of loose identical memory modules laid "
        "side by side, and the sloping edge of an aluminium assembly jig enters "
        "the frame at the lower right. Faint dust, tiny solder specks and small "
        "machining marks on the metal give the scene honest working wear. Behind, "
        "blurred into heavy bokeh, the factory hall recedes with the dark "
        "silhouettes of more chassis, tooling and overhead gantry lighting, "
        "their outlines softened and indistinct. Cool neutral industrial "
        "illumination with a soft warm practical in the far background, a "
        "low-key but honest look. Extremely shallow depth of field, sharp only "
        "on the DIMM rows, the tray and the near bench edge. Real lens bokeh, "
        "faint dust motes in the air, natural grain and sensor noise, slightly "
        "uneven real white balance, subtle vignette, no glowing lines, no neon, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A genuine photograph shot on a fast lens by a professional industrial "
        "photographer on the assembly floor of a server and PC manufacturing "
        "plant, not a render, not a 3D visualisation, not computer generated. "
        "Extreme close three-quarter view of an open server chassis in the sharp "
        "lower foreground: the bare green motherboard is fully exposed, and "
        "spaced evenly along its two long memory channels stand rows of "
        "identical DRAM modules seated in their retention slots, the matte "
        "fibreglass card edges, the small black memory chips and the gold-plated "
        "contact fingers rendered razor sharp with real specular highlights "
        "sliding along them. Just behind and beside the board, a low grey tray "
        "of identical bare memory sticks lies in a tidy row, unseated, showing "
        "their identical green carriers and gold edges at an angle. The whole "
        "assembly rests on a scuffed steel conveyor surface with a bolted "
        "aluminium jig rail and a flat ribbon cable looping past at the frame "
        "edge. Deep in the background and heavily out of focus, the dark "
        "unlit silhouettes of further server chassis and tooling on the "
        "production line dissolve into smooth creamy bokeh. Soft cool daylight "
        "from high industrial windows on the left with a gentle warm practical "
        "bounce, honest natural shadows, low-key but clean. Extremely shallow "
        "depth of field, sharp only on the memory modules and the near tray. "
        "Real optical blur, faint dust motes in the air, natural sensor noise "
        "and fine film grain, slightly imperfect real-world exposure and white "
        "balance, subtle vignette, tactile realistic material textures of "
        "aluminium, fibreglass and solder, no plastic CGI sheen, no glossy "
        "render look, no airbrushed surfaces, no perfect symmetry, no digital "
        "illustration, no AI-generated look, no neon, no glowing lines, no "
        "geometric patterns, no HUD graphics, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
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
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
