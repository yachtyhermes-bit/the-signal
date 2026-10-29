#!/usr/bin/env python3
"""Generate hero for avav-directed-energy-production-economics-2026 (fal flux/schnell).

Subject: AeroVironment (AVAV) — directed-energy weapons. High-energy LASER
weapon systems (the LOCUST X3, 30 kilowatt class) crossing from prototype into
mass production, and the economics of counter-drone air defence: a laser shot
costing under $10 versus expensive interceptor missiles. Related kit: drones,
loitering munitions, RF jamming, mobile air-defence vehicles, test ranges.

Frame: THE COUNTER-DRONE TEST RANGE — a ground-based laser weapon system and a
tripod-mounted optical tracker on a mobile air-defence position at an
instrumented desert range at dawn. NOT a data center, NOT a server room, NOT a
cleanroom, NOT a factory line, NOT a lab.

Scene 1 (ATTEMPT=1): operators at a mobile counter-drone air-defence station —
a big tripod-mounted optical tracker in the sharp foreground, dusty ground,
cabling and an open case, desert test range and mountains behind, one operator
turning away from camera.

Scene 2 (ATTEMPT=2): a ground-based high-energy laser weapon turret / beam
director mounted on the flatbed of a mobile air-defence vehicle, big plain
optics aperture facing camera-left over a desert test range at dawn, mountains
behind, dust haze, an operator working at the rear of the vehicle.

Scene 3 (ATTEMPT=3): a rugged small fixed-wing reconnaissance drone on a
catapult / launch rail on a dry test range at dawn, hand-launched airframe,
transit case and ground equipment around it, figures walking away, mountains
behind.

Deliberately NOT (banned): no data-center long hallway, no server aisle, no
server racks, no cable runs, no GPU rack, no fibre patch panel, no satellite
bus, no cleanroom, no semiconductor packaging line, no bare chip macro, no
humanoid robot, no gas power station, no dilution refrigerator, no steam
turbine, no boardroom, no security ops desk, no desert transmission towers.
NOT neon / synthwave, NOT glowing light trails or a visible laser beam, NOT
abstract geometric digital art, NOT a chart / graph / dashboard / screen full
of data, NOT a 3D render or CGI look.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY. Prior attempts read as CGI
  renders, so the prompt leans hard on documentary reportage cues: available
  light, sensor noise, dust, wear, clutter, imperfect handheld framing.
- Keep it non-graphic: hardware and operators only, no combat, no
  explosions, no fire, no injured people, no violence.
- TEXT-FREE: military hardware invites stencils, unit patches, tail numbers,
  HUD reticles and maker's brand names on tripod heads and camera bodies, so
  all lettering and numerals are explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-avav-directed-energy-hero-20260925.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "avav-directed-energy-production-economics-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no stencilled "
    "codes, no serial numbers, no unit patches, no name tapes, no rank "
    "insignia, no national flags, no tail numbers, no vehicle markings, no "
    "stencilled letters or numerals on the airframe or launcher or optics "
    "mount, no signage, no placards, no warning labels, no safety posters, "
    "no labels, no tags, no stickers, no decals, no painted markings on "
    "machinery or vehicles, no words on push buttons or switches, no START "
    "or STOP legends, no button lettering, no control-panel instructions, "
    "no machine nameplates, no data plates, no asset tags, no inventory "
    "stickers, no equipment identification plates, no illuminated indicator "
    "words, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no trademarks, no watermarks, no signatures, no "
    "barcodes, no QR codes, no data-matrix codes, no hatching IDs, no "
    "graffiti, no handwriting, no documents, no clipboards with writing, no "
    "map cards or laminated cards with writing, no legible writing of any "
    "kind anywhere in the image. No brand name or maker's mark printed or "
    "embossed on any piece of equipment: no name stamped, engraved, moulded "
    "or cast into a tripod head, ball head, quick-release plate, clamp, "
    "camera body, lens barrel, filter ring, equipment case, latch, buckle, "
    "helmet, radio, antenna, mast, jack or bicycle-style frame tube, no "
    "embossed logo or wordmark on any metal, rubber or plastic hardware "
    "anywhere. No HUD or targeting-reticle lettering, no range figures, no "
    "crosshair annotation text, no printed markings on the optics, no "
    "lettering on the tiny components, no control panel, no keypad and no "
    "buttons are visible in frame at all. Any display, monitor, sight, "
    "scope, eyepiece, tablet or machine readout is entirely blank, dark or "
    "softly out of focus with no readable content at all. Every surface, "
    "hull panel, camera body, rail, tripod, case, clothing and vehicle is "
    "plain and unmarked, carrying no lettering, no numerals and no logos at "
    "all. No illustration, no digital art, no cartoon, no 3D render, no "
    "CGI, no video-game still, no concept art, no matte painting, no neon, "
    "no glowing lines, no light trails, no visible laser beam, no glowing "
    "energy beam, no lens flare trails, no synthwave, no abstract geometric "
    "art, no floating holographic elements, no augmented-reality graphics, "
    "no wireframe, no charts, no graphs, no dashboards, no data "
    "visualisation, no screens full of data, no data center, no server "
    "room, no server racks, no server aisles, no cable runs, no GPU racks."
)

COMMON = (
    "This is unposed documentary photojournalism caught in a single "
    "unrehearsed moment, not a staged product shot and not a hero render: "
    "the subject sits off-centre, the horizon is very slightly tilted, the "
    "framing is loose and a little careless, and foreground clutter cuts "
    "into the bottom of the frame. Low raking first light of dawn coming in "
    "from behind and to the left of the camera, long soft shadows, cool "
    "blue-grey mountain haze deepening with distance and a pale washed dusty "
    "sky, honest available-light exposure with the shadows genuinely falling "
    "off to near black. Shallow depth of field from a wide aperture, real "
    "optical lens blur and creamy natural bokeh, unobtrusive grain visible "
    "in the smooth mid-tones, faint chromatic fringing on high-contrast "
    "edges, subtle lens vignette, slight sensor softness in the shadows, "
    "dust and grit in the air catching the backlight, scuffed worn surfaces "
    "with real fingerprints, smears, chips and grime on every object, "
    "asymmetric unidealised composition, no plastic CGI sheen, no glossy "
    "render, no perfect symmetry, no immaculate showroom cleanliness, no "
    "retouched hyper-clean digital look, no 3D visualisation, no digital "
    "illustration, no concept-art lighting, no video-game aesthetic,"
    "photorealistic, very high detail, professional editorial reportage "
    "photography for a newspaper, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — operators at a mobile counter-drone air-defence station with a
    #     tripod-mounted optical tracker on a desert test range at dawn.
    "1": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at "
        "f/2.0 on a full-frame camera in dusty dawn light, at a mobile "
        "counter-drone air-defence observation position on a rocky desert "
        "test range. In the sharp near foreground, filling the left two "
        "thirds of the frame and sitting slightly off-centre, a heavy "
        "tripod-mounted optical tracker stands on scarred spread aluminium "
        "legs on loose grey rock and dry cracked earth: a big dark grey "
        "cast-metal pan-and-tilt head carrying a long cylindrical lens "
        "barrel roughly half a metre long with a matte black sunshade hood "
        "screwed onto its front, a smaller parallel sighting tube clamped "
        "alongside it, and a counterweight arm reaching out behind over the "
        "legs, every surface brushed aluminium or dull matte black, "
        "unlabelled and unmarked, dust worked into the knurling of the "
        "locking knobs, anodising scratched and rubbed pale along the "
        "edges, a cold thin specular highlight running the length of the "
        "barrel from the low sun, the whole assembly rock steady and real. "
        "Under and around the tripod the ground is littered with the "
        "untidiness of a working position: a sandbag hooked over the centre "
        "column, a coiled black cable snaking away across the gravel, a "
        "flattened rectangle of dark groundsheet, half a dozen bootprints "
        "in the dust, a discarded flannel rag, an empty metal mug and a "
        "small folded camp stool lying on its side, and in the lower right "
        "corner, partly cropped by the edge of frame and falling out of "
        "focus, a battered open hard-shell equipment case with plain dark "
        "foam interior and a spare lens canister resting beside it. Two "
        "operators are at work in the mid-ground just behind and right of "
        "the tripod, seen from behind and in three-quarter rear view, "
        "softly out of focus: one crouched low and folded over to the "
        "eyepiece with his shoulders turned entirely away from the camera, "
        "the other standing close at his shoulder with one hand shading his "
        "goggles and the other resting on a plain unmarked black radio on "
        "his chest harness, both in plain drab dusty field clothing with "
        "helmet and dark goggles, faces completely hidden and "
        "unidentifiable, no name tape, no patch and no badge anywhere on "
        "their clothing or kit. Behind them the range falls away into warm "
        "haze: a shallow dry valley of pale gravel and thorn scrub, faint "
        "vehicle tracks curving away, a canvas-topped utility trailer and a "
        "slender antenna mast far off as soft blurred shapes without any "
        "legible marking, then a long receding ridge of rugged grey-brown "
        "mountains strung right across the horizon under a pale blue-gold "
        "morning sky with a few thin high clouds. Nothing is firing, "
        "nothing is flying, the scene is calm, quiet and methodical. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — ground-based laser weapon turret / beam director on an air-defence
    #     vehicle at a desert test range at dawn.
    "2": (
        "Photo-realistic editorial press photograph, shot on a 70-200mm "
        "lens at f/2.8 set to about 110mm on a full-frame camera, of a "
        "ground-based high-energy laser weapon system parked on an "
        "instrumented desert test range at first light, caught between "
        "tests with everything at rest. At the centre of frame, crisp and "
        "tack sharp, the weapon's beam-director turret sits on a low "
        "rotating pedestal bolted to the flatbed of an unmarked matte "
        "olive-drab air-defence vehicle: a heavy weathered housing with a "
        "large plain circular optics aperture at its front, roughly thirty "
        "centimetres across, dark, uncapped and unlit, its coated glass "
        "catching only a dull grey-green reflection of the morning sky, "
        "flanked by a gimballed secondary tracking sensor housing and a "
        "pair of smaller square apertures, everything plain, matte and "
        "unlabelled, no lettering and no markings anywhere on the metal, "
        "fine pale desert dust settled along the panel seams and in every "
        "recess, sun-bleached paint scuffed and chipped back to bare metal "
        "on the corners, faint warm rim light along the top of the aperture "
        "ring. The pedestal, elevation yoke, coiled cable wrap and sealed "
        "connector boxes below it are sharp industrial hardware with "
        "visible bolt heads, dull hydraulic fittings, dark grease at the "
        "pivot and a stabilising jack leg splayed onto a timber sole board "
        "beside the rear wheel, the flatbed underframe of the vehicle "
        "partly cropped by the bottom of the frame, a heavy canvas bag and "
        "a coiled tow strop dumped on the deck beside it. On the right of "
        "frame, mid-ground and softly out of focus, one operator in plain "
        "dusty fatigues and a plain helmet with a dark visor stands on the "
        "ground beside the vehicle, seen from behind and in three-quarter "
        "view, bending slightly toward an open unmarked equipment case and "
        "a small tripod, face hidden, unidentifiable, no patch, tape or "
        "badge on his clothing. Beyond him the desert test range recedes "
        "into warm haze: dry gravel and low scrub in the mid-ground with "
        "faint tyre tracks and a scattering of plain marker stakes, and a "
        "low line of rugged grey-brown mountains across the whole horizon "
        "under a pale washed dawn sky with thin high cloud. Nothing is "
        "firing; the weapon is at rest, hatches closed, the scene calm, "
        "clinical and industrial rather than dramatic. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — rugged small fixed-wing reconnaissance drone on a launcher rail on a
    #     dry test range at dawn.
    "3": (
        "Photo-realistic editorial press photograph, shot on a 50mm lens at "
        "f/2.2 on a full-frame camera, of a small rugged fixed-wing "
        "reconnaissance drone sitting on its launch rail on a dry desert "
        "test range at dawn, seen close from a low three-quarter front "
        "angle with the camera slightly tilted. The drone is tack sharp in "
        "the centre of frame but not clean, and shows real field wear: a "
        "short straight wing of tough matte khaki composite with a faint "
        "weave visible under the paint and patches of rubbed-off finish "
        "along the leading edge, a blunt cylindrical fuselage with a "
        "compact sensor turret tucked under the nose, its dark glass ball "
        "unlit and blank, a slim pusher propeller at the tail with a "
        "chipped tip, thin stiff antennae and a couple of plain pitot tubes "
        "protruding forward, dust bloomed into the panel seams, sun-faded "
        "tape over one inspection hatch, oil smeared around the propeller "
        "hub, the whole airframe plain, scuffed and unmarked with no "
        "lettering, no numerals, no tail number and no insignia anywhere. "
        "It rests on a simple angled extruded-aluminium launch rail fixed "
        "to a ground frame, supported by two scarred uprights and a spread "
        "base on bare gravel, with loose wire, a coil of shock cord, a "
        "welding glove and a scuffed jerry can lying about the foot of the "
        "rail. A battered hard-shell transit case lies open on the ground "
        "in the sharp right foreground, partly cropped by the frame and "
        "falling out of focus at the edge, containing dark foam cutouts and "
        "a spare wing panel; a folded ground-control tripod and a coiled "
        "cable sit beside it, all plainly unlabelled and unmarked. In the "
        "mid-ground, softly out of focus, two figures in plain drab field "
        "clothing walk away from the camera toward a canvas-topped utility "
        "trailer, seen only from behind as blurred silhouettes in the haze, "
        "faces not visible, unidentifiable, no patch or badge on their "
        "clothing. Beyond them the test range opens out into warm haze — "
        "dry gravel plain, low scrub, a faint track and a few plain marker "
        "posts without any legible marking — and a long line of rugged "
        "grey-brown mountains across the horizon under a pale washed gold "
        "dawn sky. Nothing is flying, nothing is firing, the scene is calm "
        "and workmanlike. "
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
