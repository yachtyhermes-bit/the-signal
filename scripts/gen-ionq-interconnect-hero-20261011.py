#!/usr/bin/env python3
"""Generate hero for ionq-quantum-interconnect-defense-2026 (fal flux/schnell).

Subject: IonQ's quantum interconnect milestone — photonic entanglement between a
trapped-ion qubit and a diamond silicon-vacancy (SiV) quantum memory — and its
DARPA Stage C validation.

Chosen visual: a REAL photonic / quantum-optics laboratory bench, shot as
documentary editorial photography — a precision optical table with rows of small
black-anodised mounts, silver mirrors, lenses and fiber-collimation assemblies in
a purposeful optical path, a thin free-space laser beam crossing the frame, a
fiber patch cable curving into a metal ferrule, and in the sharp focal plane a
small mounted diamond photonic chip / tiny die clamped in a machined brass or
copper holder with a single fiber coupling into its edge. In the soft background,
a stainless vacuum chamber with a round viewport and a faint internal glow.

Deliberately DISTINCT from recent Signal heroes that must not repeat:
  (1) TSMC record revenue        — fab / silicon.
  (2) GlobalFoundries packaging  — chip packaging.
  (3) Rocket Lab Neutron         — rocket on launch pad.
  (4) Powell Industries          — electrical switchgear.
  (5) Cloudflare birthday week   — edge networking / ethernet rack fabric.
  (6) Applied Optoelectronics    — optical transceiver module.
  (7) data-center server aisle   — server racks / aisle.
  (8) semiconductor cleanroom    — fab cleanroom.
  (9) nuclear plant.
 (10) plain office.
 (11) D-Wave / QBTS              — CRYOSTAT dilution-refrigerator chandelier
                                   (must NOT repeat).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon, synthwave,
  CGI, 3D render, cartoon, glowing lines, light trails, HUD, holograms, particles.
- Optical-table / free-space optics scene — NOT a cryostat chandelier, NOT a
  data-center hallway / server aisle / server racks / cleanroom.
- TEXT-FREE / no legible text: no words, letters, numbers, logos, brand names,
  labels, screen readouts, gibberish lettering. Any instrument panel reads as soft
  indistinct shapes only, at an oblique angle.
- FACES NOT identifiable (from behind / side / out of focus / at distance).
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \\
    scripts/gen-ionq-interconnect-hero-20261011.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ionq-quantum-interconnect-defense-2026")
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
    "futuristic HUD graphics, no augmented-reality overlays, no floating particles. Not a cryostat, "
    "no dilution refrigerator, no chandelier of stacked gold plates, no gold-plated cryogenic "
    "hardware, no cryogenic wiring loom. Not a data center, no server room, no server aisle, no "
    "server racks, no data-center hallway, no racks of network gear, no cable-run macro, no "
    "cleanroom, no bunny suits, no abstract cyberspace."
)

PROMPTS = {
    # Scene A — optical table with diamond photonic chip in the sharp focal plane (50mm f/2).
    "1": (
        "A real documentary editorial photograph, shot on a full-frame DSLR with a 50mm lens wide "
        "open at f/2, available light, no flash, not a render and not CGI: a precision photonics "
        "and quantum-optics laboratory bench. Across the frame stretches a thick matte-black "
        "optical table drilled with dense rows of mounting holes, and onto it are bolted a "
        "purposeful optical path of small black-anodised kinematic mounts, silver first-surface "
        "mirrors, cylindrical lens barrels and fibre-collimation assemblies held at precise "
        "angles. A thin, subtle free-space laser beam, a faint realistic glint rather than a glow, "
        "crosses the frame low and level. A slim optical fibre patch cable with yellow or orange "
        "buffer curves gently out of focus and terminates in a polished metal ferrule fitting. In "
        "the sharp focal plane, at center-left, a tiny mounted diamond photonic chip — a "
        "thumbnail-sized transparent die the size of a grain of rice — is clamped in a machined "
        "brass and copper holder, with a single optical fibre coupling into its polished edge, the "
        "metal bearing fine tool marks and honest wear. The mounts and table are used and dusty, "
        "with faint fingerprints, not pristine. Lighting is real and directional: warm practical "
        "bench lamps cast a soft amber pool, while a cool blue-white spill rakes in from one side, "
        "sculpting the silver mirrors with realistic specular highlights and soft shadows. Behind, "
        "the lab dissolves into creamy bokeh: the curved flank of a brushed stainless vacuum "
        "chamber with a round glass viewport holding a faint warm internal glow, and indistinct "
        "blurred instruments, nothing identifiable and nothing legible. Very shallow depth of "
        "field, buttery real optical lens blur, natural camera sensor noise, very slight film "
        "grain, subtle vignette, dust, honest worn metal, no plastic CGI sheen, no glossy render, "
        "no perfect symmetry, photorealistic, extremely high detail, authentic editorial stock "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # Scene B — 100mm macro of the fiber-coupled diamond chip in its copper holder.
    "2": (
        "A real macro photograph, shot on a 100mm macro lens at f/2.8, extremely shallow depth of "
        "field, available light, not a render and not CGI: an extreme close-up of a diamond "
        "photonic chip mounted on an optical bench. In the sharp centre a minuscule transparent "
        "square diamond die, barely larger than a sesame seed, sits clamped inside a machined brass "
        "and copper holder with tiny torx or hex screws; the die has crisp polished facets and "
        "faint internal structure, and a single hair-thin optical fibre with a metal ferrule "
        "couples straight into its polished edge, the fibre buffer curving softly out of focus. "
        "Around the holder, in the soft blur of the optical table, stand out-of-focus rows of "
        "small black-anodised mounts and a silver mirror edge catching a stray highlight. A thin "
        "faint free-space laser beam, a subtle realistic glint not a neon glow, skims across the "
        "mid-ground. The metal is used, brushed and slightly tarnished with honest dust and tiny "
        "scratches, not a flawless render. Lighting is soft and directional from above, raking "
        "across the metal and glass to reveal real texture, with a cool blue-white tint from one "
        "side and a warm amber practical glow from the other; behind everything melts into deep "
        "creamy dark bokeh with a barely visible round vacuum-chamber viewport and no identifiable "
        "detail. Real optical lens blur, natural sensor noise, very slight film grain, subtle "
        "vignette, no plastic CGI sheen, no glowing lines, no neon, no perfect symmetry. "
        "Photorealistic, extremely high detail, professional scientific editorial stock "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # Scene C — wider environmental view of the optical table and vacuum chamber.
    "3": (
        "A photojournalistic wide environmental photograph, shot on a 35mm lens at f/2.5 on a "
        "full-frame camera in an available-light photonics laboratory, unretouched, not a render "
        "and not CGI: the interior of a real quantum-optics lab. A large black perforated optical "
        "table fills the mid-ground, crowded with black-anodised kinematic mounts, silver mirrors, "
        "lens tubes and fibre-collimation assemblies arranged in an ordered free-space beam path; a "
        "single thin laser beam, faint and realistic, threads low across the table. A yellow-buffered "
        "fibre patch cable loops loosely across the bench, and near the centre a small diamond "
        "photonic die clamped in a machined copper holder has one hair-thin fibre collimated into "
        "its edge, though at this distance it reads as a small precise detail rather than a macro. "
        "In the soft background, out of focus, stands a brushed stainless vacuum chamber with a "
        "round glass viewport and a faint warm internal glow, alongside blurred matte instruments "
        "and a dim painted lab wall; deeper in the room a lone technician in a plain shirt is seen "
        "only from behind and at distance, unidentifiable and out of focus. The room is real and "
        "lived-in: scuffed floor, coiled cables, dust, an angled gauge panel showing only soft "
        "indistinct forms and no legible content. Cool ambient ceiling light is mixed with a warm "
        "practical bench lamp that rakes across the metal. Natural sensor noise, very slight film "
        "grain, subtle vignette, honest imperfect composition, no neon, no glowing lines, no "
        "perfect symmetry, no CGI look. Photorealistic, extremely high detail, authentic editorial "
        "stock photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # Scene D — three-quarter hero of the optical path with the chamber behind (50mm f/2).
    "4": (
        "A real documentary editorial press photograph, shot on a 50mm lens at f/2 on a full-frame "
        "camera, available light, not a render and not CGI: a photonics laboratory optical bench. "
        "A dense, purposeful optical path marches diagonally across the frame — small matte-black "
        "anodised mounts each holding a silver mirror, a lens barrel or a fibre-collimation "
        "assembly, arranged in a deliberate free-space beam line — while a slim fibre patch cable "
        "curves in from the right into a polished metal ferrule. In the sharp foreground plane a "
        "tiny diamond photonic chip is clamped in a machined brass and copper holder with a single "
        "optical fibre bonded into its edge, the metal showing honest machining and wear. A thin, "
        "subtle free-space laser beam, a faint realistic glint rather than a neon glow, crosses "
        "the scene. Behind and out of focus rises the round flank of a brushed stainless vacuum "
        "chamber with a glass viewport harbouring a faint warm internal glow, together with "
        "indistinct blurred lab equipment and a soft dark wall. Lighting is real and mixed: warm "
        "amber practical lamps against a cool blue-white spill, casting genuine specular highlights "
        "and soft shadows on the silver optics, dust suspended in the air. Very shallow depth of "
        "field, real optical lens blur, natural camera sensor noise, very slight film grain, subtle "
        "vignette, honest worn metal, no perfect symmetry, no plastic CGI sheen, no glowing lines, "
        "no neon. Photorealistic, extremely high detail, authentic editorial stock photography, "
        "16:9 landscape composition. " + NO_TEXT
    ),
    # Scene E — over-the-bench working view, fibre ferrule and chip, chamber bokeh.
    "5": (
        "A real documentary editorial photograph, shot on an 85mm lens at f/2 on a full-frame "
        "camera, available light, not a render and not CGI: a low view across a quantum-optics "
        "optical table seen almost at bench height. Rows of small black-anodised mounts with silver "
        "mirrors, lens tubes and fibre launchers recede into soft focus, forming an ordered "
        "free-space beam path; a single thin laser beam, faint and realistic, runs across the "
        "mid-ground at just above table height. In the sharp focal plane the eye lands on a tiny "
        "diamond photonic die clamped in a small machined copper and brass holder with a hair-thin "
        "optical fibre collimated into its edge, the fibre buffer curving away into blur, and the "
        "metal honest and slightly dusty. Beside it, a metal ferrule on a yellow-buffered patch "
        "cable catches a highlight. The background is a quiet soft bokeh of a brushed stainless "
        "vacuum chamber with a round viewport and a faint internal glow, a dim wall and indistinct "
        "scientific instruments, nothing identifiable and nothing legible. Lighting is real and "
        "mixed: a warm amber practical lamp pools on the bench while a cool blue-white spill rakes "
        "from the left, sculpting the silver surfaces with realistic highlights and soft shadows; "
        "dust hangs in the air. Very shallow depth of field, real optical lens blur, natural camera "
        "sensor noise, very slight film grain, subtle vignette, honest imperfect composition, no "
        "neon, no glowing lines, no perfect symmetry, no CGI look. Photorealistic, extremely high "
        "detail, authentic editorial stock photography, 16:9 landscape composition. " + NO_TEXT
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
