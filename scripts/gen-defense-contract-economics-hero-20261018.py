#!/usr/bin/env python3
"""Hero for defense-contracts-cost-plus-vs-fixed-price-explainer-2026 (fal flux/schnell).

Subject: an evergreen explainer on US DEFENSE CONTRACT ECONOMICS — how cost-plus
versus fixed-price contract structures decide a defense supplier's margin before a
single part is machined. Sector: DEFENSE / AEROSPACE MANUFACTURING.

The story is about where the money is decided: not in the sky, not on a trading
floor, but on the shop floor where the part is cut and the cost is locked in. So
the picture is a precision aerospace machine shop: a large bare machined aluminium
aerostructure rib clamped in a steel work-holding fixture on a CNC machining bed.

Deliberately DISTINCT from recent heroes on this site:
- NOT a data-centre / server-room / server-aisle / GPU-rack / cable-run shot (banned).
- NOT rockets, launch pads, fighter jets in the sky, flying drones, radar dishes.
- NOT a trading floor, NOT neon / synthwave / glow / HUD / geometric / digital art.
- NOT the semiconductor cleanroom / wafer heroes (AVGO, TSM, MU).
- NOT a ship canal lock (moat hero).

Rules: photo-realistic industrial documentary photography ONLY. Every surface is
plain and unmarked — machine shops are full of part numbers, traveller tags, gauge
faces, control screens and safety placards, so all lettering, numerals, dial
graduations, screens, logos and signage are explicitly forbidden.

Generate 1440x810, finalize 1600x900 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-defense-contract-economics-hero-20261018.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get(
    "SLUG", "defense-contracts-cost-plus-vs-fixed-price-explainer-2026"
)
ATTEMPT = os.environ.get("ATTEMPT", "3")
SEED = os.environ.get("SEED", "2026101803")  # optional fixed seed for reproducible re-rolls
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
# optional candidate override — writes to a scratch path instead of the real target
CAND = os.environ.get("CAND")
if CAND:
    OUTPUT = CAND
    BACKUP = CAND
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1600, 900

NO_TEXT = (
    "The entire scene contains no legible lettering of any kind: no text, no "
    "letters, no words, no numbers, no digits, no numerals, no part numbers, no "
    "serial numbers, no drawing numbers, no revision codes, no lot codes, no job "
    "traveller cards, no paper tags, no tie-on labels, no stickers, no decals, no "
    "stencilled marks, no ink stamps, no vibro-etch or laser-etched characters, no "
    "engraved characters, no machine-tool maker's plate, no nameplate, no asset "
    "tag, no barcodes, no QR codes, no datamatrix codes, no colour-coded tooling "
    "bands with printing, no signage, no safety placards, no warning labels, no "
    "posters, no whiteboards, no clipboards, no paper, no documents, no drawings, "
    "no charts, no screens, no monitors, no displays, no control panels, no CNC "
    "control pendant, no user interface, no UI, no software windows, no icons, no "
    "dashboard, no readouts, no digital counter, no LED numerals, no dial "
    "graduations, no gauge faces with markings, no ruler graduations, no scale "
    "ticks, no engraved measurement lines, no depth markings, no logos, no brand "
    "names, no trademarks, no watermarks, no captions, no signatures, no "
    "graffiti, no stencilling. The aluminium part is bright bare machined metal "
    "with nothing written anywhere on it; the steel fixture, clamps and machine "
    "bed are plain worn metal with no plates or markings; the round face of the "
    "dial indicator is turned away from the camera so it reads only as a plain "
    "pale disc with no graduations visible. No people, no hands, no faces, no "
    "human figures, no silhouettes, no body parts. No illustration, no digital "
    "art, no cartoon, no 3D render, no CGI, no CGI sheen, no neon, no glowing "
    "lines, no light trails, no synthwave, no geometric patterns, no circuit "
    "graphics, no network diagram, no word clouds, no futuristic HUD, no "
    "hologram, no augmented-reality overlay, no data visualization, no data "
    "center, no server room, no server racks, no server aisles, no cable-run "
    "composition, no GPU hardware, no trading floor, no office, no desk, no "
    "rocket, no launch pad, no spacecraft, no fighter jet, no aircraft in the "
    "sky, no drone, no radar dish, no antenna array, no satellite."
)

REALISM = (
    "This is a real industrial documentary photograph taken on the shop floor by "
    "an editorial photographer with available light, not a studio setup and not a "
    "rendering: honest uneven exposure with slightly blown highlights on the bare "
    "aluminium, real high-ISO sensor noise and fine film grain, faint chromatic "
    "aberration on the sharp metal edges, subtle vignetting in the corners, "
    "machining marks and tool swirls and a few fine chips of swarf on the metal, "
    "a faint smear of cutting fluid, and a softly imperfect out-of-focus "
    "background with real workshop clutter. Muted natural colour warmed by amber "
    "work lighting, documentary reportage feel, 16:9 landscape composition."
)

PROMPTS = {
    # 1 — three-quarter close shot along the CNC bed, rib clamped in its fixture.
    "1": (
        "Photo-realistic editorial press photograph, a genuine industrial documentary "
        "news picture shot on a 50mm lens at f/2.2 on a full-frame camera inside a "
        "precision aerospace machine shop, close in at the machining bed of a large "
        "CNC vertical mill. Lying flat on the grey cast-iron machine table, filling "
        "the centre of the frame and running diagonally from the lower left toward "
        "the upper right, is a single large bare aluminium aerostructure rib: a long "
        "curved machined component with a thick spar web and a row of raised stiffening "
        "flanges and lightening pockets milled into it, its freshly cut surface bright "
        "silvery aluminium covered in the fine concentric tool-path swirls of a face "
        "mill, with soft rounded edges and machined radii, and completely plain and "
        "unmarked with nothing written on it anywhere. The rib is gripped across its "
        "middle by a heavy steel work-holding fixture: dark oil-stained steel jaw "
        "blocks and a thick bolted strap clamp pressing down on the part, held by big "
        "hex bolts and T-nuts in the table's slots. Fine curled aluminium chips and "
        "bright metal shavings are scattered on the table around the fixture and "
        "caught in the slots, and a thin film of pale green-grey cutting fluid pools "
        "and streaks across the machined surface, catching the overhead light in wet "
        "slippery highlights along the ribs and in the milled pockets. In the near "
        "foreground at the bottom right of the frame, slightly out of focus, stands a "
        "dial indicator on a heavy magnetic base with its articulated steel arm, its "
        "round face angled away from the lens so it reads only as a plain pale disc, "
        "the base's worn cast metal and knurled adjustment knob sharp against the "
        "blurred bed. Above and behind, warm amber work lighting from high overhead "
        "rakes down across the part, warm pools of light and soft shadow in the "
        "pockets and under the clamps; the far background is a softly out-of-focus "
        "wall of the machine enclosure and blurred shop clutter in cool shadow. "
        "Shallow depth of field — the near clamp, the rib's machined face and the "
        "shavings crisp, the far end of the rib and the machine softening into creamy "
        "haze. Real optical lens blur, natural camera noise, clearly visible fine film "
        "grain, subtle optical vignette, slightly off-level hand-held framing with "
        "the part placed just off centre, no perfect symmetry, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 landscape "
        "composition. " + REALISM + " " + NO_TEXT
    ),
    # 2 — higher, wider angle across the bed showing fixture + coolant + swarf.
    "2": (
        "A real photograph taken on location inside a working aerospace machine shop, "
        "not a render and not computer generated: a wide three-quarter shot on a 35mm "
        "lens at f/2.8 from just above working height, looking down across the bed of "
        "a large CNC machining centre at a bare aluminium aerostructure bulkhead. The "
        "bulkhead is a big machined frame-like component, an arc of bright silvery "
        "aluminium with a broad flange, a machined pocket grid and a curved outer "
        "contour, sitting clamped flat on the grey cast-iron table and filling the "
        "lower two-thirds of the frame from the near edge toward the middle distance. "
        "Its surface is fresh from the cutter, covered in fine parallel tool-path "
        "swirls and tiny burrs, wet with a thin sheen of pale green-grey coolant that "
        "has run down the flanges and gathered in the pockets, reflecting the warm "
        "overhead lamps in long soft wet streaks. In the mid-ground a massive steel "
        "fixture tower and two heavy swing clamps bear down on the part, dark steel "
        "with oil-stained shoulders, thick bolts and worn knurled nuts, and a heavy "
        "steel angle plate sits bolted at the far edge of the table. Bright curled "
        "aluminium swarf is heaped and scattered across the table slots and the floor "
        "of the machine, some of it catching the light as thin bright spirals. In the "
        "near foreground at the lower left edge a heavy cast-iron clamp body and a "
        "dial indicator on a magnetic base sit slightly out of focus, its round face "
        "turned away so no graduations show. Warm amber work lighting from high above "
        "the machine floods down in soft pools, with deep shadow under the fixture "
        "tower and along the far edge of the bed; the workshops beyond are a blurred "
        "expanse of grey machines and cluttered benches in dim cool shadow. Very "
        "shallow depth of field — the machined flange and the near clamp sharp, the "
        "far end of the part and the shop already reduced to soft blur. Real optical "
        "blur, natural camera noise, visible fine film grain, subtle lens vignette, "
        "slightly off-centre hand-held framing, no CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + REALISM + " " + NO_TEXT
    ),
    # 3 — low raking angle down the bed, amber work light dominating, swarf in the
    # sharp foreground plane so the machining is unmistakable.
    "3": (
        "Photo-realistic editorial press photograph, a real documentary picture shot "
        "on an 85mm lens at f/2 from a low raking angle close to the machine table, "
        "looking along the surface of the work at eye level with the bed. The whole "
        "scene is lit only by warm amber sodium-toned work lamps high above the "
        "machine, so the entire frame is bathed in a deep golden orange glow with the "
        "metal reading warm bronze-gold rather than cold silver, and the shadows are "
        "dense and brown. Dominating the centre and right of the frame, a large bare "
        "machined aluminium aerostructure rib lies clamped flat and curves gently away "
        "from the lens: a heavy machined component with a curved vertical web, a row "
        "of raised stiffening ribs and deep milled lightening pockets between them, its "
        "surface covered in the fine parallel tool-path swirls of a face mill and "
        "bright bare metal with no marking of any kind on it. Its pockets hold small "
        "pools of pale cutting fluid that reflect the amber lamps in tiny soft bright "
        "spots, and rivulets of coolant have run down the ribs and left wet dark "
        "streaks on the bright metal. In the sharp nearest foreground, right at the "
        "bottom edge of the frame and only just in focus, a scatter of fine curled "
        "aluminium chips and bright spiral shavings lies heaped on the oiled grey "
        "cast-iron table, some caught against the base of a heavy steel clamp, each "
        "curl glinting warm amber along its bright cut edge, with a shallow film of "
        "cutting fluid pooling and reflecting around them. Just beyond the shavings a "
        "massive dark steel work-holding fixture with a thick bolted strap and two "
        "heavy hex bolts presses down on the rib's web. To the left of the part, out "
        "of focus in the middle distance, a dial indicator stands on its magnetic base "
        "with the round face turned away from the lens. The background dissolves into "
        "warm brown darkness with the faint blurred shapes of the machine column and "
        "the shop beyond, lit by a distant amber lamp. Very shallow depth of field — "
        "the near shavings, fluid and clamp crisp, the part's near edge sharp, and "
        "everything past the middle of the rib falling into soft creamy blur. Real "
        "optical lens blur, natural camera noise, clearly visible fine film grain, "
        "subtle optical vignette, slightly off-level hand-held framing with the part "
        "placed off centre, no perfect symmetry, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + REALISM + " " + NO_TEXT
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
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    hermes_env = "/home/chino/.hermes/profiles/yachty/.env"
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if line.strip().startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    return None


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
    if SEED:
        args["seed"] = int(SEED)
        print(f"  SEED={SEED}")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments=args,
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
    """Center-crop to 16:9, then resize to 1600x900."""
    img = img.convert("RGB")
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
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )


if __name__ == "__main__":
    main()
