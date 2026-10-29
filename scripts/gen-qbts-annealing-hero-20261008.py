#!/usr/bin/env python3
"""Generate hero for qbts-annealing-quantum-moat-2026 (fal flux/schnell).

Subject: D-Wave Quantum (NYSE/TSX: QBTS) — the company that builds quantum
ANNEALING computers, the physically different cousin of the gate-model machines
IonQ and Rigetti build. The article is a deep dive on D-Wave's moat.

Chosen visual: the iconic, unmistakable quantum-hardware image — the cryogenic
dilution refrigerator, the tall gold-and-copper "chandelier" of stacked circular
plates and coiled wiring suspended in a frame, photographed as real documentary
editorial photography.

Deliberately DISTINCT from recent Signal heroes that must not repeat:
  (1) TSMC record revenue       — fab / silicon.
  (2) GlobalFoundries packaging — chip packaging.
  (3) Rocket Lab Neutron        — rocket.
  (4) Powell Industries         — electrical switchgear.
  (5) Cloudflare birthday week  — edge networking.
  (6) Applied Optoelectronics   — optical transceivers.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon, synthwave,
  CGI, 3D render, cartoon, glowing lines, light trails, HUD, holograms, particles.
- NO data-center hallway / server aisle / server racks / cable-run macro.
- TEXT-FREE / no legible text: no words, letters, numbers, logos, brand names,
  labels, screen readouts, gibberish lettering. Any instrument panel reads as soft
  indistinct shapes only, at an oblique angle.
- FACES NOT identifiable (from behind / side / out of focus / at distance).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \\
    scripts/gen-qbts-annealing-hero-20261008.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "qbts-annealing-quantum-moat-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "There is absolutely no legible text anywhere in the frame: no readable words, no letters, no "
    "numbers, no digits, no characters, no glyphs, no labels, no stickers, no nameplates, no "
    "branding, no logos, no brand names, no company marks, no serial plates, no signage, no screen "
    "readouts, no gauge text, no dial faces with numbers, no keyboard lettering, no cable tags, no "
    "gibberish or pseudo-lettering of any kind. Any instrument panel, monitor or gauge in the "
    "background is turned at an oblique angle and reads only as a soft indistinct glowing or matte "
    "rectangle with no content. No illustration, no digital art, no cartoon, no 3D render, no CGI, "
    "no video-game look, no neon, no synthwave, no glowing holographic lines, no light trails, no "
    "futuristic HUD graphics, no augmented-reality overlays, no floating particles. Not a data "
    "center, no server room, no server aisle, no server racks, no data-center hallway, no racks of "
    "network gear, no cable-run macro, no cleanroom, no abstract cyberspace."
)

PROMPTS = {
    # Scene B — tight three-quarter detail of the chandelier (50mm f/2).
    "1": (
        "A real documentary editorial photograph, shot on a full-frame DSLR with a 50mm lens wide "
        "open at f/2, available light, no flash, not a render and not CGI: a tight three-quarter "
        "detail of the lower stages of a cryogenic dilution refrigerator inside a real quantum "
        "computing laboratory. The subject fills the frame: the iconic chandelier of stacked, "
        "polished gold-plated copper circular plates of decreasing diameter, separated by thin "
        "stainless-steel rods, with a dense, delicate harness of fine silver and copper wiring "
        "sweeping in graceful curves between the plates and down to the lowest mixing-chamber "
        "stage. Micro coaxial cables, tiny brass SMA connectors and laced wiring bundles are "
        "visible in crisp detail at the sharp focal plane, while the upper plates and the plate "
        "edges beyond fall softly out of focus. The metal is warm and used, with faint tool marks, "
        "fingerprints, machining swirls and honest dust, not mirror-perfect. Lighting is real and "
        "directional: a cool blue-white lab light spills from one side, a warm amber practical "
        "lamp glows from the other, both sculpting the gold surfaces with soft realistic shadows "
        "and specular highlights. Behind, a dark laboratory dissolves into creamy bokeh — a blurry "
        "rack of test equipment and a table edge, nothing identifiable and nothing legible. Very "
        "shallow depth of field, buttery real optical lens blur, natural camera sensor noise, very "
        "slight film grain, subtle vignette, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, photorealistic, extremely high detail, authentic editorial stock photography, "
        "16:9 landscape composition. " + NO_TEXT
    ),
    # Scene A — wide dim cryogenics lab with anonymous engineer.
    "2": (
        "A real documentary editorial press photograph, shot on a 24mm lens at f/2.8 on a "
        "full-frame camera, available light, not a render and not CGI: a wide, dimly lit cryogenics "
        "laboratory at a quantum computing company. In the centre of the frame the gold-plated "
        "dilution refrigerator dominates — a tall chandelier of stacked circular copper plates and "
        "radiating silver wiring hanging inside a simple dark support gantry, rising from its "
        "cylindrical vacuum can toward the ceiling. Its warm gold and copper surfaces catch a "
        "low-key warm key light that rakes across the metal, while the room falls away into deep "
        "shadow. At the base of the fridge an anonymous engineer in a plain untucked shirt is seen "
        "from behind and to the side — only their back, shoulders and one arm are visible, the face "
        "turned entirely away and unidentifiable — one hand carefully adjusting a cable near the "
        "base of the machine. The composition is honest and imperfect, with a workbench, a coiled "
        "cable and a piece of dark test equipment blurred in the near foreground so they read only "
        "as soft shapes. A gauge panel at the left edge, angled away, shows nothing but indistinct "
        "soft forms. The atmosphere is quiet, real and industrial-scientific: concrete floor, "
        "painted steel, matte black cable sheathing, warm practical light mixed with a cool ambient "
        "spill, dust in the air, all unretouched. Shallow depth of field with the fridge sharp and "
        "the foreground and background soft; natural sensor noise, very slight film grain, subtle "
        "vignette, no neon, no glowing lines, no perfect symmetry, no CGI look. Photorealistic, "
        "extremely high detail, authentic editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # Scene C — macro of superconducting quantum processor chip in gold sample holder.
    "3": (
        "A real macro photograph, shot on a 100mm macro lens at f/2.8, extremely shallow depth of "
        "field, available light, not a render and not CGI: an extreme close-up of a superconducting "
        "quantum processor chip mounted inside its gold-plated sample holder, the kind used in a "
        "dilution refrigerator. In the sharp centre a small square silicon die sits recessed in a "
        "machined, gold-plated copper block; the die is etched with a fine grid of tiny radiating "
        "traces and metallic features, bordered by rows of minute wire bonds — whisper-thin gold "
        "wires connecting the chip to its surrounding carrier — and by delicate machined channels "
        "and gold-plated screw holes around the holder. The gold plating has a real brushed, used "
        "sheen with tiny scratches and honest dust, not a flawless render. Lighting is soft and "
        "directional from above, raking across the metal to reveal its texture, with a cool "
        "blue-white tint from one side and a faint warm amber glow from the other; behind, the "
        "inside of the fridge melts into pure dark creamy bokeh with nothing identifiable. Real "
        "optical lens blur, natural sensor noise, very slight film grain, subtle vignette, no "
        "plastic CGI sheen, no glowing lines, no neon, no perfect symmetry. Photorealistic, "
        "extremely high detail, professional scientific editorial stock photography, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    # Scene B variant — three-quarter hero of the full chandelier body.
    "4": (
        "A real photographic portrait of a machine, shot on a 35mm lens at f/2.5 on a full-frame "
        "camera in an available-light laboratory, not a render and not CGI: a three-quarter view of "
        "a complete dilution refrigerator chandelier, the tall stack of gold-plated copper circular "
        "plates getting smaller toward the bottom, laced with countless fine silver and copper "
        "wires, coax cables and small connectors, hanging from the base of its vacuum can. The "
        "plates gleam a warm brushed gold; the wiring is a dense, delicate lace of silver, copper "
        "and pale insulation. The metal shows honest wear — faint oxidation, tiny scratches, dust — "
        "not a pristine glossy render. Warm low-key light rakes the stack from the upper left while "
        "a cool shadowed background of a dim lab wall and a blurred bench with indistinct equipment "
        "falls off into deep shadow on the right. Slight perspective from just above the base, the "
        "lowest plate and its wiring harness the sharpest, everything else gently out of focus. "
        "Natural camera sensor noise, very slight film grain, subtle vignette, realistic materials, "
        "no CGI sheen, no perfect symmetry, no neon, no glowing lines. Photorealistic, extremely "
        "high detail, authentic editorial stock photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # Scene A variant — wider environmental lab portrait.
    "5": (
        "A photojournalistic wide environmental photograph, shot on a 28mm lens at f/2.8, available "
        "light, unretouched, not a render and not CGI: the interior of a dim quantum computing "
        "laboratory. A tall gold-and-copper dilution refrigerator chandelier of stacked circular "
        "plates and fine coiled wiring stands prominently in the mid-ground, suspended in its "
        "support frame, its warm gleaming surfaces the brightest thing in the room. In the soft "
        "foreground, out of focus at the edge of frame, a dark workbench holds a coil of cable and "
        "a matte instrument, reading only as soft dark shapes; a large angled piece of test gear on "
        "the right shows only indistinct soft forms and no legible content. Deeper in the room, "
        "blurred and unidentifiable, a lone person in a plain shirt stands with their back to the "
        "camera working at a bench. The room is real and industrial-scientific: concrete floor, "
        "painted walls, plain steel framing, quiet shadows, a cool ambient ceiling light mixed with "
        "a warm practical light that rakes across the gold plates, dust in the air. Natural sensor "
        "noise, very slight film grain, subtle vignette, honest imperfect composition, no neon, no "
        "glowing lines, no perfect symmetry, no CGI look. Photorealistic, extremely high detail, "
        "authentic editorial stock photography, 16:9 landscape composition. " + NO_TEXT
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
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
