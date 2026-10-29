#!/usr/bin/env python3
"""Generate hero for tsla-optimus-humanoid-mass-production-2026 (fal flux/schnell).

Subject: Tesla (TSLA) — the Optimus humanoid robot heading toward mass
production. Physical AI: the robot as the next product of Tesla's neural-net +
inference-silicon stack. Sector: MEGA-CAP / ROBOTICS MANUFACTURING.

The picture is therefore a HUMANOID ROBOT ON AN AUTOMOTIVE ASSEMBLY LINE /
ROBOT PRODUCTION FLOOR — a blank metal-and-matte-panel humanoid, no branding,
being built or worked on at a line station, with car bodies or metal pressings
softly out of focus behind.

Scene set for the three attempts (all inside these bounds):
  1 — the humanoid robot standing/partially assembled at a line station, a
      technician's gloved hands on its forearm guiding a connection.
  2 — a wide factory floor: the humanoid beside workers at a station, car
      bodies on the line out of focus behind.
  3 — a tight close crop of the robot's hand/forearm on a workbench with a
      gloved hand.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack /
cable-run / long-hallway composition (banned and overused on this site), NOT
abstract art, NOT digital art / 3D render / CGI, NOT neon / synthwave, NOT
glowing lines, NOT geometric patterns, NOT a lit screen or display in frame,
NOT any brand mark on the robot (nothing resembling Tesla or any real marque).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: factory floors are covered in signage, bin labels, part numbers,
  safety placards and line-andon boards, so all lettering, numbers, serial
  numbers, part numbers, logos, brand names, signage, badges, printed
  documents, charts and readouts are explicitly forbidden. Any monitor, screen,
  andon board, HMI panel or instrument display in frame is switched off, angled
  away, or so far out of focus it reads as a flat dark rectangle.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-tsla-optimus-hero-20260923.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "tsla-optimus-humanoid-mass-production-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_DISPLAYS = (
    " Critically, there is not one single lit or active display anywhere in "
    "this photograph: no glowing screens, no monitor content, no andon board, "
    "no production-count board, no glowing red or green digital numbers, no "
    "seven-segment numerals, no LED digits, no backlit LCD, no HMI touch "
    "panel, no lit instrument window, no lit panel meter, no glowing indicator "
    "lamp, no illuminated button, no status light, no blinking LEDs, no lit "
    "power switch, no stack-light showing a colour, no readout of any kind "
    "glowing in the scene. Every panel, cabinet, machine housing and control "
    "box in the frame has a plain flat unlit blank face: continuous smooth "
    "unmarked metal or matte plastic, with no window, no screen, no glass, no "
    "display, no digits, no dial face and no lit element anywhere on it. "
    "Anything that could be mistaken for a screen is dark, dead and switched "
    "off, reading only as a flat unlit rectangle of dark material. The only "
    "light in the image comes from the hall's own overhead lamps and the high "
    "windows, never from a screen or an indicator. "
)

NO_TEXT = (
    "This is not a digital illustration and not a 3D render: it is an "
    "ordinary available-light documentary photograph made with a real camera "
    "in a working vehicle factory, with the imperfect framing, uneven "
    "exposure, slight dust, faint smudges, scuffs and small asymmetries of a "
    "real photo. The entire scene is completely free of any lettering: no "
    "text, no letters, no words, no numbers, no serial numbers, no part "
    "numbers, no model numbers, no engraved or stamped markings on the metal, "
    "no machine markings, no labels, no sticker labels, no bin labels, no "
    "nameplates, no manufacturer names, no company names, no brand names, no "
    "corporate logos, no trademarks, no name badges, no lanyards, no hi-vis "
    "vest lettering, no hard-hat lettering, no signage of any kind anywhere "
    "in the picture — no wall signs, no safety signs, no warning signs, no "
    "placards, no notices, no banners, no stencilled numbers or codes on the "
    "machines, the racks, the totes or the concrete, no coloured safety "
    "signage or pictograms, no floor "
    "markings, no painted floor stripes with words, "
    "no banners, no production boards, no charts, no graphs, no dashboards, "
    "no monitor content, no control-panel content, no barcodes, no QR codes, "
    "no handwriting, no watermarks, and absolutely no automaker logo or "
    "marque anywhere in the image. Every display, monitor, screen, andon "
    "board, HMI panel or instrument face in the frame is switched off, angled "
    "away, or so far out of focus that it shows only a soft flat wash of dark "
    "colour with absolutely nothing readable or drawn on it, like an "
    "out-of-focus colour field photograph. The robot's own body panels are "
    "plain smooth matte metal and dark composite with no printing, no "
    "engraving, no badge and no wordmark on them; its head is a plain "
    "unmarked smooth visor. No illustration, no digital art, no cartoon, no "
    "3D render, no CGI, no video-game asset, no concept art, no neon, no "
    "glowing lines, no light trails, no synthwave, no geometric patterns, no "
    "circuit-board graphics, no wireframe, no glowing sensor, no lit eyes, no "
    "hologram, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no floating UI, no data center, no server "
    "room, no server racks, no server aisles, no GPU racks, no rack aisle, no "
    "long hallway of cabinets, no cable-run perspective down an aisle, no "
    "server lights, no blinking network switch LEDs, no computer screen with "
    "text."
)

# Applied to every prompt. flux/schnell has no negative prompt, so the anti-CGI
# and anti-showroom pressure has to live in the positive text.
NO_CGI = (
    " This is a candid, unretouched documentary frame grabbed in the middle of "
    "a working shift, not a product shot, not a beauty portrait, not a "
    "showroom display and not a hero pose. The plant is an old working "
    "industrial hall that has been in service for decades: the concrete is "
    "dull, stained and cracked, the steel fixtures are oxidized and chipped, "
    "there are grease smears, dust films, worn paint, cable ties, tape and "
    "honest clutter in the frame, and the machine and robot surfaces are worn, "
    "dull and a little grimy from use rather than pristine, polished or "
    "freshly unboxed. The workers' overalls are creased and grubby. The "
    "lighting is mundane and mixed, flat in places and blown out or muddy in "
    "others, auto-white-balance colour, the way a real press photo in a "
    "factory actually looks, never cinematic, never a dramatic grade, never a "
    "clean studio setup. Composition is slightly off-centre and slightly "
    "tilted, framed a touch too loose, as if taken quickly on the move by a "
    "staff photographer who was not allowed to stop the line. Absolutely no "
    "smooth plastic sheen, no airbrushed perfection, no clean bevels, no "
    "reflections of unseen studio lights, no floating elements, no "
    "impossible geometry, no sharp-edged sci-fi armour plating, no matte "
    "black glossy finish, no concept-art silhouette — ordinary industrial "
    "hardware photographed by an ordinary camera in ordinary daylight. "
)

PROMPTS = {
    # 1 — backlit silhouette of the humanoid at its line station, low-key hall.
    "1": (
        "A real available-light photograph taken against the light inside a "
        "vehicle assembly plant, shot hand-held on a full-frame body with a "
        "35mm lens at f/2.8, ISO 3200, exposure set for the bright lamps so "
        "the whole hall goes dark and the machines in front of it are almost "
        "silhouettes, colour muddy and slightly green, framed loose and "
        "slightly off-level with the horizon tilted, and a fine haze of "
        "industrial dust in the air catching the light so the far end of the "
        "hall is a milky flare-washed grey. Standing in the middle distance "
        "in the centre-left of the frame, facing away from the camera at a "
        "line station, is a large humanoid robot of human height and "
        "proportions, the only thing in the picture you look at: because the "
        "bright lamps are behind it and the camera is exposed for them, it "
        "reads almost as a dark shape, but its outline is completely legible "
        "— two heavy legs braced apart on the concrete, a boxy torso, two "
        "thick articulated arms hanging, a wide shoulder yoke and a plain "
        "blank rounded head block with no face and nothing lit on it. The "
        "rim of light along its shoulder, forearm and thigh shows dull, "
        "handled, dusty metal that is scuffed and unfinished rather than "
        "polished: the cover plate is missing from one shin so the bare "
        "aluminium tube leg and the machined steel actuator show against the "
        "light, its chest cover hangs open on a hinge with the bare frame "
        "and a loose bundle of plain black cable held with tie-wraps "
        "showing, and a strip of plain unmarked masking tape and cream foam "
        "shipping padding are still stuck around one wrist. No badge, no "
        "wordmark, no logo, no painted trim, no glowing eyes, nothing lit "
        "anywhere on it. Around it the line is ordinary and messy: a bare "
        "unpainted car body shell on the conveyor throwing the same dark "
        "profile, steel racking stacked with stamped pressings, stacked grey "
        "totes, a coil of air hose, loose washers and dropped bolts on the "
        "stained cracked concrete with worn-away old paint stripes, hanging "
        "cable festoon runs and, high overhead, the dusty steel roof trusses "
        "carrying rows of ordinary industrial lamps. Two workers in creased "
        "grubby dark grey overalls pass in the near foreground on the left, "
        "cropped at the chest and thigh, closer to the camera than the "
        "robot, backs to the lens, unaware of the camera and rendered as "
        "deep shadow. The light is flat, dull and mixed, uneven and muddy "
        "rather than cinematic, no dramatic grade, no rim light, no studio "
        "setup, heavy shadow across the whole frame, slight highlight bloom "
        "and veiling glare around the lamps. Real photographic grain and "
        "visible high-ISO noise in the dark areas, subtle lens vignette, "
        "mild chromatic aberration on the high-contrast edges, slightly "
        "dirty sensor speckle, "
        + NO_CGI
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 2 — candid with motion blur, taken while walking past the line station.
    "2": (
        "A real candid photograph taken while walking past, hand-held on a "
        "full-frame body with a 35mm lens at f/4, ISO 4000, shutter speed "
        "too slow for the movement, so the whole picture carries a soft "
        "directional smear from the photographer moving and a trace of "
        "camera shake, and nothing in the frame is pin-sharp: exposure set "
        "for the pale car bodies so the hall falls flat and a little dark, "
        "colour cool and slightly green under the sodium and mercury lamps, "
        "framed carelessly and off-level with too much floor in the bottom "
        "of the picture, a fine haze of industrial dust in the air making "
        "the far end of the hall milky and low in contrast. In the centre "
        "right of the frame, a few metres away and smeared by the movement "
        "but still perfectly readable, stands a large humanoid robot of "
        "human height and proportions at a line station: a heavy machine "
        "with two heavy legs on the concrete, a boxy worn torso, two thick "
        "articulated arms hanging at its sides, a wide shoulder yoke and a "
        "plain blank matte grey head block with no face and nothing lit on "
        "it. It is caught mid-production and unfinished in the way real "
        "product on a line is: the cover plate is missing from one shin with "
        "the bare aluminium tube leg and machined steel actuator showing, "
        "its chest cover hangs open on a hinge showing bare frame tube and a "
        "loose bundle of plain black cable held with tie-wraps, strips of "
        "plain unmarked masking tape and cream foam shipping padding are "
        "still stuck around one wrist, and its scuffed dark grey composite "
        "panels and dull oxidised aluminium are coated in the same fine grey "
        "shop dust as the floor and the bench. No badge, no wordmark, no "
        "logo, no painted trim, no glowing eyes, nothing lit anywhere on "
        "it. In the near foreground, closer to the camera than the robot and "
        "sharper than everything else only in a relative sense, two workers "
        "in creased grubby dark grey overalls walk past with their backs to "
        "the lens, one carrying a plain grey parts tote, unaware of the "
        "camera. Around and behind them the hall is messy and ordinary: a "
        "conveyor of bare unpainted car body shells and stamped pressings, "
        "steel racking, stacked grey totes, hanging cable festoon runs, an "
        "idle spot welding robot folded at rest, a coiled air hose on the "
        "stained cracked concrete with worn-away old paint stripes and "
        "grit, and high overhead the dusty steel trusses with rows of "
        "ordinary industrial lamps. The light is flat, dull and mixed, "
        "uneven and muddy rather than cinematic, no dramatic grade, no rim "
        "light, no studio setup, deep shadow pooling under the line and the "
        "benches. Real photographic grain and heavy visible high-ISO noise, "
        "subtle lens vignette, mild chromatic aberration on the high-"
        "contrast edges, slightly dirty sensor speckle, "
        + NO_CGI
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 3 — the humanoid at the line with a real lens flare cutting the frame.
    "3": (
        "A real photograph taken into a bright overhead lamp on the shop "
        "floor of a vehicle assembly plant, shot hand-held on a full-frame "
        "body with a 35mm lens at f/4, ISO 2000, and because the camera is "
        "pointed almost at the lamp the frame is crossed by a long soft "
        "veiling flare and a chain of pale ghost reflections running from "
        "the upper right corner down across the middle of the picture, "
        "washing out contrast over part of the scene, with a haze of "
        "industrial dust in the air catching the light so the far end of the "
        "hall is milky and low-contrast. Framed loose and slightly "
        "off-level, exposure set for the bright metal so the rest of the "
        "hall sits a little dark and muddy, colour cool and slightly green "
        "under the sodium and mercury lamps. Standing at a line station in "
        "the centre left of the frame, a few metres away and fully "
        "readable despite the flare, is a large humanoid robot of human "
        "height and proportions: a heavy machine with two heavy legs on the "
        "concrete, a boxy worn torso, two thick articulated arms hanging at "
        "its sides, a wide shoulder yoke and a plain blank matte grey head "
        "block with no face and nothing lit on it. It is caught "
        "mid-production and clearly unfinished: the cover plate is missing "
        "from one shin with the bare aluminium tube leg and machined steel "
        "actuator showing, its chest cover hangs open on a hinge showing "
        "bare frame tube and a loose bundle of plain black cable held with "
        "tie-wraps, strips of plain unmarked masking tape and cream foam "
        "shipping padding are still stuck around one wrist, and its scuffed "
        "dark grey composite panels and dull oxidised aluminium are coated "
        "in the same fine grey shop dust as everything around it. No badge, "
        "no wordmark, no logo, no painted trim, no glowing eyes, nothing lit "
        "anywhere on it. Two workers in creased grubby dark grey overalls "
        "stand nearer the camera on the right, backs to the lens, one bent "
        "over a plain steel tray on a low bench, unaware of the camera. "
        "Around them the hall is ordinary and messy: a conveyor of bare "
        "unpainted car body shells and stamped pressings, steel racking, "
        "stacked grey totes, a coiled air hose on the stained cracked "
        "concrete with worn-away old paint stripes and grit, hanging cable "
        "festoon runs, and high overhead the dusty steel trusses carrying "
        "the rows of industrial lamps that are causing the flare. The light "
        "is flat, dull and mixed, uneven and muddy rather than cinematic, no "
        "dramatic grade, no rim light, no studio setup, deep shadow pooling "
        "under the line. Real photographic grain and visible high-ISO noise "
        "in the flat grey areas, subtle lens vignette, mild chromatic "
        "aberration on the high-contrast edges, slightly dirty sensor "
        "speckle, "
        + NO_CGI
        + NO_TEXT
        + NO_DISPLAYS
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
    img = img.convert("RGB")
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
