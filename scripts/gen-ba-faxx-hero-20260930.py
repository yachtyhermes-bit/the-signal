#!/usr/bin/env python3
"""Generate hero for ba-faxx-sixth-gen-fighter-defense-margin-2026 (fal flux/schnell).

Subject: Boeing wins the U.S. Navy's F/A-XX sixth-generation fighter contract
(~$20B full-scale development award, announced 29 Sep 2026). No public photos of
the F/A-XX exist, so the hero depicts the aircraft it replaces: a U.S. Navy
F/A-18E Super Hornet strike fighter on a carrier flight deck at dawn.

Scene chosen: a Super Hornet on the catapult of an aircraft carrier at sea in
the first light of dawn — three-quarter view, nose gear in the shuttle, steam
drifting across a wet non-skid deck, a few small distant deck crew in coloured
jerseys and float coats far behind, deep blue-grey ocean and a low horizon,
warm early sun raking the canopy and spine. One clear subject, deep
perspective, documentary naval photography.

Deliberately DISTINCT from the recent Signal heroes that must not repeat:
  (1) avav-moat (20260928): a desert laser-weapon truck on a test range.
  (2) amat-hbm-packaging (20260928): a semiconductor fab CLEANROOM interior.
  (3) crwv-ai-compute-credit-residual-value-2026 (20260929): a vast AI compute
      campus under construction at dusk (exterior, building scale).
  (4) v (20260929): a retail payment terminal close-up.
  (5) moat-test (20260927): a ship canal lock at golden hour.

Rules (per repo regen lessons):
- PHOTO-REALISTIC stock photograph style ONLY. No digital art/neon/render/
  geometric patterns/illustration/cartoon/synthwave/glowing lines/HUD.
- TEXT-FREE: naval aircraft and carrier decks naturally carry modex numbers,
  squadron markings, tail codes, stencilled maintenance data and warning
  decals — ALL explicitly forbidden. Surfaces must read as plain painted
  metal with no lettering of any kind.
- NO data-center long hallway / server aisle / rack interior composition
  (banned). NO infographic look; the image must contain no words at all.
- Generate 1440x810, finalize 1920x1080 center-crop.

Shipped artifact: ATTEMPT=4 (this prompt), fal seed 915962305, md5
ba6d556a684236ed772d1e890bcd78fd. Note: fal did NOT reproduce this frame
bit-for-bit when re-run with SEED pinned, so treat SEED as best-effort only.
Chosen after vision QC of rolls of ATTEMPT 1-8 (1,2,3 rejected: CGI look /
markings "CEPC", "707"+insignia+"GO", "11"+nose insignia respectively;
4 and 7 scored 9/10 "real photograph, no text, no defects").

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-ba-faxx-hero-20260930.py
Optional: SEED=915962305 ATTEMPT=4 ... (best-effort reproducibility)
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ba-faxx-sixth-gen-fighter-defense-margin-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
SEED = os.environ.get("SEED", "").strip()  # optional: pin the fal seed
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is completely blank and unmarked: no text, no letters, no "
    "numbers, no digits, no codes, no serial numbers, no part numbers, no "
    "modex numbers, no nose numbers, no tail codes, no squadron markings, no "
    "unit insignia, no roundels, no stars, no flags, no printed markings, no "
    "stencilled characters, no warning decals, no maintenance stencils, no "
    "painted words, no labels, no stickers, no barcodes, no QR codes, no "
    "safety signage, no billboards, no brand names, no manufacturer names, no "
    "company logos, no aircraft type lettering, no helmet markings, no jersey "
    "writing, no deck markings, no runway numbers, no painted letters, no "
    "screen, no display panel, no digital readout, no instrument text, no "
    "signage of any kind anywhere in the image, no watermark, no signature, "
    "no captions, no legible writing anywhere. The aircraft, vehicles, deck "
    "and crew are entirely plain and unbranded: plain unmarked low-visibility "
    "grey painted metal, blank flat grey fuselage sides, blank wings, blank "
    "tail fins, blank canopy rails, plain coloured crew jerseys with no "
    "lettering, plain unmarked deck surfaces. No illustration, no digital "
    "art, no cartoon, no anime, no 3D render, no CGI, no video-game look, no "
    "plastic toy look, no neon, no synthwave, no glowing lines, no light "
    "trails, no geometric patterns, no futuristic HUD graphics, no holograms, "
    "no overlay elements, no augmented-reality graphics, no charts, no "
    "graphs, no diagrams, no infographic, no title text, no typography. Not a "
    "data-center hallway, no server aisle, no server racks, no rack of "
    "blinking network equipment, no cable runs, no rows of cabinets, no "
    "cleanroom, no office interior, no rocket launch pad, no wind turbines, "
    "no hangar interior, no museum display, no airshow crowd."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: a U.S. Navy F/A-18E Super Hornet strike fighter sitting on "
        "the catapult of an aircraft carrier at sea in the first light of "
        "dawn. The jet is seen in three-quarter front view, a single clear "
        "subject filling the centre of the frame, its nose gear hooked into "
        "the catapult shuttle, wings folded slightly back, canopy closed. "
        "Steam drifts low across the wet dark non-skid deck around the "
        "aircraft's undercarriage and the shuttle track, catching the light "
        "in soft wisps. Far behind the jet, tiny and out of focus, two or "
        "three deck crew in coloured jerseys and float coats stand small in "
        "the distance near the deck edge, deliberately secondary in the "
        "frame. Behind the ship, a deep blue-grey ocean meets a low, flat, "
        "hazy horizon; the carrier's plain superstructure is a soft dark "
        "mass at the far left edge. Warm early sun rakes along the "
        "aircraft's canopy and spine from the right, modelling the curved "
        "grey paint in long soft highlights while the deck stays in cool "
        "blue shadow; the aircraft itself is entirely plain low-visibility "
        "grey with no markings or lettering of any kind. Shot on a 50mm lens "
        "at f/5.6 from a low, stable, deck-level perspective: the aircraft's "
        "nose and undercarriage tack sharp, the deck and drifting steam "
        "carrying depth to the blurred crew and horizon. Natural camera "
        "noise and very slight film grain, subtle lens vignette, honest "
        "realistic painted metal, wet non-skid and steam texture, "
        "professional documentary naval photography, extremely detailed, "
        "photorealistic, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph, shot on a real camera, not computer generated: "
        "an authentic U.S. Navy documentary photo of an F/A-18E Super Hornet "
        "on the flight deck of an aircraft carrier at first light. The "
        "fighter sits on the catapult in three-quarter view from the front "
        "left, nose gear locked in the shuttle, its single dark canopy "
        "facing the camera, wings spread and slightly drooped, filling the "
        "left two-thirds of the frame with strong depth. Wisps of white "
        "steam curl across the wet deck beneath and behind the jet, and the "
        "damp non-skid surface holds a long pale reflection of the dawn "
        "sky. In the far distance behind the aircraft, three tiny "
        "silhouetted deck crew in coloured jerseys and float coats walk "
        "along the deck edge, small and entirely secondary. Beyond the ship "
        "the sea is deep blue-grey and calm, meeting a low hazy horizon; a "
        "plain dark carrier structure rises softly at the far right edge. "
        "Warm low sun from the side rakes the canopy and the long spine of "
        "the fuselage with soft golden light, leaving the deck in cool "
        "shadow, warm-and-cool contrast only. The aircraft is plain "
        "low-visibility grey with utterly blank, unmarked surfaces. Shot on "
        "a 50mm lens at f/5.6, low stable deck-level viewpoint, crisp nose "
        "gear and sharp canopy, clean receding depth. Natural camera noise, "
        "very slight film grain, subtle vignette, realistic painted metal, "
        "wet non-skid and steam texture, no CGI sheen, no glossy render, no "
        "perfect symmetry, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera: a U.S. Navy F/A-18E Super Hornet strike fighter held on the "
        "catapult of a carrier flight deck at dawn, seen in three-quarter "
        "view from just off the port bow so the aircraft reads as one clear "
        "subject in deep perspective. The wet dark non-skid deck stretches "
        "away in strong recession behind the jet toward a small group of "
        "distant deck crew in coloured jerseys and float coats, tiny in the "
        "frame. Low ground steam from the catapult drifts across the deck "
        "surface in thin torn layers around the aircraft's wheels and the "
        "shuttle, glowing faintly in the warm light. Behind the flight deck "
        "the carrier's plain grey structure is a soft unlit mass at the left "
        "edge, and beyond it the open sea is deep blue-grey under a low "
        "hazy horizon with the first warm band of sunrise. Early sun rakes "
        "the fighter's closed canopy and long spine from the upper right, "
        "warm highlights running along the curved grey fuselage while the "
        "deck stays cool blue. The jet is entirely plain low-visibility grey "
        "paint, blank and unmarked, no lettering anywhere. Shot on a 50mm "
        "lens at f/5.6 from a low deck-level stance: sharp undercarriage and "
        "nose, deep clean recession to the crew and horizon. Natural sensor "
        "noise, very slight film grain, subtle lens vignette, honest "
        "realistic metal, non-skid and steam texture, no plastic render "
        "look, no perfect symmetry, no digital illustration, photorealistic, "
        "extremely high detail, professional documentary naval photography, "
        "16:9 landscape composition. "
        + NO_TEXT
    ),
    "4": (
        "A genuine photograph, not a render and not computer generated: an "
        "F/A-18E Super Hornet fighter on an aircraft carrier's flight deck at "
        "dawn, framed wide and low from deck level. The jet occupies the "
        "right side of the frame in three-quarter view, nose toward the "
        "left, sitting on the catapult with its nose gear in the shuttle and "
        "its wings spread; it is one clear subject seen against the opening "
        "sky. Steam hangs and drifts in soft ragged sheets across the wet "
        "deck behind the aircraft, and thin mist clings to the non-skid "
        "surface, which mirrors the sky in long dull streaks. Small and far "
        "away behind the jet, three deck crew in coloured jerseys and float "
        "coats stand conversing near the deck edge, entirely secondary in "
        "the composition. Beyond the deck lies a deep blue-grey ocean and a "
        "low, flat, hazy horizon; the carrier's dark plain structure fills "
        "the far left edge in silhouette. Warm rising sun from the lower "
        "right rakes the canopy and the aircraft's spine with golden light, "
        "leaving the wet deck in cool blue shadow, gentle warm-and-cool "
        "contrast only. The aircraft is plain low-visibility grey, blank and "
        "unmarked, no numbers, no lettering. Shot on a 50mm lens at f/5.6, "
        "low stable perspective: tack-sharp nose and wheels, deep clean "
        "depth into the deck haze. Natural camera noise, very slight film "
        "grain, subtle vignette, realistic painted metal, wet non-skid and "
        "steam texture, no CGI look, no glossy render, no perfect symmetry, "
        "no digital illustration, photorealistic, high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: the first light of dawn over an aircraft carrier's flight "
        "deck, with a U.S. Navy F/A-18E Super Hornet strike fighter alone on "
        "the catapult as the single dominant subject. Shot in three-quarter "
        "view from the front, the jet is compact and purposeful, nose gear "
        "down in the shuttle, canopy closed, wings spread, its plain grey "
        "low-visibility paint catching warm light along the canopy and the "
        "long spine while the shadowed underside stays cool. Wet non-skid "
        "deck in the foreground, dark and sheened, carries a soft "
        "reflection of the dawn; low steam from the catapult stretches and "
        "thins across the deck in ragged horizontal layers. Far behind the "
        "jet, tiny and shallow in focus, a few deck crew in coloured jerseys "
        "and float coats move along the deck edge, deliberately small and "
        "secondary. The sea beyond is deep blue-grey under a low hazy "
        "horizon with a warm compressed sunrise band; the carrier's plain "
        "grey superstructure sits as a soft dark shape at the right edge. "
        "Every surface is blank and unmarked, the aircraft entirely without "
        "markings or lettering. Shot on a 50mm lens at f/5.6, low stable "
        "deck-level viewpoint: sharp nose, canopy and landing gear, deep "
        "receding perspective to the crew and the horizon. Natural camera "
        "noise, very slight film grain, subtle lens vignette, honest "
        "realistic painted aluminium, wet non-skid and drifting steam "
        "texture, no plastic CGI sheen, no glossy render, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "documentary naval photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "A real photograph, not a render: a U.S. Navy Super Hornet strike "
        "fighter on a carrier flight deck at sunrise, photographed from a "
        "low position alongside the jet looking forward down the deck. The "
        "aircraft is seen in three-quarter rear-to-side view, its folded "
        "outer wing panels and two angled tail fins reading strongly against "
        "the brightening sky, its nose gear planted in the catapult track "
        "ahead. The wet non-skid deck recedes past it to a small, distant "
        "group of deck crew in coloured jerseys and float coats, tiny in "
        "the frame and badly secondary to the aircraft. Thin steam drifts "
        "low over the deck and around the wheels in slow straggling veils "
        "that catch the warm light. Beyond the deck edge the ocean is deep "
        "blue-grey and still, cut by a low flat horizon; no land, no other "
        "ships. Early warm sun from the far right rakes the aircraft's spine "
        "and the tops of the fins with golden light, leaving the deck in "
        "cool blue shadow, warm-and-cool contrast only. The jet is plain "
        "low-visibility grey and completely unmarked, no codes, no "
        "lettering, no insignia. Shot on a 50mm lens at f/5.6, low stable "
        "perspective: sharp tail fins and undercarriage, deep clean "
        "recession down the deck. Natural camera noise, very slight film "
        "grain, subtle lens vignette, realistic painted metal, wet non-skid "
        "and steam texture, no CGI sheen, no glossy render, no perfect "
        "symmetry, no digital illustration, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "7": (
        "Photo-realistic documentary stock photograph taken with a real "
        "camera at dawn: an F/A-18E Super Hornet strike fighter on the "
        "catapult of an aircraft carrier's flight deck, seen in "
        "three-quarter view from slightly above deck level so the whole "
        "aircraft and a broad strip of wet non-skid deck are visible at "
        "once. The jet is the one clear subject: plain grey low-visibility "
        "paint, canopy shut, nose gear hooked in the shuttle, wings spread, "
        "its long shadow thrown across the wet deck toward the camera. "
        "Steam from the catapult blurs and floats in soft horizontal bands "
        "across the deck behind the aircraft, thinning as it drifts toward "
        "the deck edge. Far behind, small and softly out of focus, a few "
        "deck crew in coloured jerseys and float coats move along the deck, "
        "entirely secondary. Past the deck edge, deep blue-grey ocean meets "
        "a low flat hazy horizon with a warm band of sunrise; the carrier's "
        "plain structure is a soft dark mass at the left of frame. Warm "
        "early sun rakes the canopy and spine with golden light while the "
        "deck lies in cool shadow, gentle warm-and-cool contrast only. No "
        "markings, no lettering, no numbers anywhere on the aircraft or "
        "deck. Shot on a 50mm lens at f/5.6, low stable perspective: sharp "
        "canopy, nose and gear, deep clean recession into the deck haze. "
        "Natural sensor noise, very slight film grain, subtle vignette, "
        "honest realistic metal, wet non-skid and steam texture, no CGI "
        "look, no glossy render, no perfect symmetry, no digital "
        "illustration, photorealistic, extremely high detail, professional "
        "documentary naval photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "8": (
        "Photo-realistic editorial stock photograph, real camera, not a "
        "render: dawn over a U.S. aircraft carrier, with a Super Hornet "
        "strike fighter staged on the catapult as the single subject of the "
        "frame. Seen in three-quarter view from the front right, the jet is "
        "plain low-visibility grey, utterly unmarked, canopy closed, nose "
        "gear down in the shuttle, wings spread, standing on wet dark "
        "non-skid deck that stretches away in deep perspective. Thin steam "
        "smears across the deck in slow ragged sheets around the aircraft "
        "and the catapult track, faintly luminous in the warm light. Far "
        "behind the jet and small in the frame, a handful of deck crew in "
        "coloured jerseys and float coats walk the deck near the edge, "
        "sharp enough to read as people but entirely secondary. Beyond the "
        "deck, the sea is deep blue-grey with a low hazy horizon and a "
        "compressed band of warm sunrise; the carrier's plain grey "
        "structure sits softly out of focus at the far right edge. Low warm "
        "sun rakes the canopy and the long spine of the fuselage with "
        "golden light, while the wet deck and the far side of the aircraft "
        "remain cool blue. Shot on a 50mm lens at f/5.6 from a low, stable, "
        "deck-level stance: tack-sharp nose, canopy and undercarriage, "
        "smooth deep recession to the crew and horizon. Natural camera "
        "noise, very slight film grain, subtle lens vignette, honest "
        "realistic painted metal, wet non-skid and drifting steam texture, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no "
        "digital illustration, no infographic, photorealistic, high detail, "
        "professional editorial stock photography, 16:9 landscape "
        "composition. "
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
    arguments = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if SEED:
        arguments["seed"] = int(SEED)
        print(f"Using pinned SEED={SEED}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=arguments)
    print(f"fal seed: {result.get('seed')}")
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
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
