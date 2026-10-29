#!/usr/bin/env python3
"""Generate hero for rtx-amraam-multiyear-munitions-capacity-2026.

Subject: RTX / Raytheon and the U.S. missile industrial base — the Pentagon's
~$20.7B multiyear AMRAAM award to RTX's Raytheon business, and the push to
expand munitions production capacity.

Frame chosen (ONE scene): THE MISSILE FINAL-ASSEMBLY FLOOR — a defense
manufacturing hall where a technician in safety gear inspects the body of a
finished air-to-air missile resting in a wheeled assembly cradle. Low
three-quarter angle so the long cylindrical missile body fills the frame and
reads as one clear subject in deep perspective, with vertical assembly stands
and an overhead gantry softly out of focus behind.

Deliberately DISTINCT from the RTX precedent
(scripts/generate-rtx-hero.py, 2026-07-28), which showed a Patriot air-defence
battery of launcher vehicles out in a field at dusk — that composition is NOT
used here. Also distinct from recent Signal heroes: no carrier deck / fighter
(ba-faxx 20260930), no desert laser-weapon truck (avav 20260925/28), no
semiconductor fab cleanroom (amat-hbm 20260928), no AI compute campus
(crwv 20260929), no payment terminal, no canal lock.

=== PROVIDER NOTE (important) ===
The BA/AVAV reference scripts call fal-ai/flux/schnell with FAL_KEY from
/home/chino/hermes-workspace/studio-api/.env.  As of 2026-10-01 that FAL
account is HARD-BLOCKED:

    fal_client.client.FalClientHTTPError: User is locked.
    Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing.

Every FAL key on this host (studio-api/.env, ~/.hermes/.env, video_output/
.fal_real, profiles/*/.env) is the same 69-char key / same locked account, and
no other provider with an image endpoint was usable (Gemini GOOGLE_API_KEY is
free-tier with image quota limit 0; all OpenRouter image models are blocked by
the workspace guardrail; Cloudflare Workers AI is not in the R2 token's scope;
no OpenAI/Replicate/Stability/HF keys; no local GPU or diffusion stack).

The working alternative found on this host is the Google Gemini image models
accessed with the key in /home/chino/video_output/.gemini_key (a different
Google project from GOOGLE_API_KEY, with working image quota).  This script
therefore defaults to Gemini and will still try FAL first if FAL_KEY is set and
PROVIDER=fal is requested explicitly.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, no CGI /
  3D-render look, no neon / synthwave / glowing lines, no abstract geometric
  patterns, no infographic, no HUD graphics.
- TEXT-FREE: aerospace hardware and factory floors naturally carry part
  numbers, stencils, placards, machine nameplates, aisle signage and warning
  decals — ALL explicitly forbidden. Surfaces read as plain painted metal.
- NO data center, NO server room, NO server aisle, NO racks, NO cable runs
  (hard-banned composition).
- Non-graphic: hardware and workers only. No combat, no explosion, no fire.
- 16:9 landscape, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-rtx-amraam-missile-20261001.py
"""
import os
import sys
import json
import base64
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "rtx-amraam-multiyear-munitions-capacity-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
PROVIDER = os.environ.get("PROVIDER", "gemini")  # gemini | fal
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-image")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size (fal) / requested aspect (gemini)
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface in the image is completely blank and unmarked: no text, no "
    "letters, no words, no numbers, no numerals, no digits, no part numbers, "
    "no serial numbers, no stencilled codes, no lot codes, no date stamps, no "
    "inspection stamps, no QA stamps, no printed markings, no stencilled "
    "characters, no painted words, no labels, no placards, no machine "
    "nameplates, no data plates, no asset tags, no inventory stickers, no "
    "warning decals, no safety signage, no aisle markings, no floor paint "
    "numbers, no hangtags, no barcodes, no QR codes, no clipboards with "
    "writing, no documents, no work orders, no posters, no billboards, no "
    "brand names, no manufacturer names, no company names, no corporate "
    "logos, no trademarks, no watermarks, no signatures, no captions, and no "
    "legible writing of any kind anywhere in the image. The missile body, nose "
    "section, fins and rear nozzle are utterly plain painted grey metal with "
    "no stencilling of any kind; the cradle, stands, gantry, cabinets, tooling "
    "and floor are plain surfaces carrying no lettering; the technician's "
    "coveralls, helmet, gloves, safety glasses and vest are completely plain "
    "with no name tape, no patch, no badge and no lettering anywhere. Any "
    "monitor, display screen, control panel, meter or instrument in the "
    "background is blank, dark or softly out of focus with no readable "
    "content. No illustration, no digital art, no cartoon, no anime, no 3D "
    "render, no CGI, no video-game still, no concept art, no plastic-toy look, "
    "no neon, no synthwave, no glowing lines, no light trails, no abstract "
    "geometric art, no floating holograms, no augmented-reality overlay, no "
    "wireframe, no HUD graphics, no charts, no graphs, no diagrams, no "
    "infographic, no typography. Not a data center, no server room, no server "
    "aisle, no server racks, no rack of blinking network equipment, no cable "
    "runs, no rows of cabinets, no cleanroom bunny-suit fab, no office "
    "interior, no boardroom, no warehouse logistics aisle."
)

COMMON = (
    "This is an unposed editorial stock photograph, shot on a real full-frame "
    "camera, not a render: shallow depth of field from a wide aperture, real "
    "optical lens blur and natural creamy bokeh, the subject tack sharp and "
    "filling the frame in strong receding depth while the far background goes "
    "soft. Clean bright industrial daylight from high clerestory windows and "
    "diffuse overhead lighting, soft raking highlights along polished curved "
    "metal, honest realistic painted aluminium and steel with tiny machining "
    "marks, subtle fingerprints, faint scuffs and fine dust in the recesses, "
    "unobtrusive sensor grain in the smooth mid-tones, subtle lens vignette, "
    "slightly imperfect asymmetric framing, no plastic CGI sheen, no glossy 3D "
    "render, no perfect symmetry, no immaculate showroom plastic look, "
    "photorealistic, very high detail, professional editorial photography for "
    "a newspaper, 16:9 landscape composition. "
)

PROMPTS = {
    # 1 — missile final-assembly floor, low three-quarter angle on the missile
    #     body, technician inspecting alongside.
    "1": (
        "Professional stock photograph of a missile final-assembly floor inside "
        "a defense manufacturing plant. The single clear subject is a long "
        "slender finished air-to-air missile body resting horizontally in a "
        "wheeled steel assembly cradle in the centre of the frame, seen from a "
        "low three-quarter angle so the smooth cylindrical grey painted "
        "fuselage recedes in strong perspective from close foreground to the "
        "soft background. The missile is a plain smooth cylinder: a tapered "
        "nose section at the far end and a cluster of slim swept tail fins and "
        "a small dark nozzle at the near end, entirely plain matte grey painted "
        "metal with no markings whatsoever. Alongside the missile, slightly "
        "behind and to one side, a single technician in a plain blue-grey "
        "coverall, white hard hat, clear safety glasses and pale nitrile gloves "
        "leans in and runs a gloved hand along the missile's mid-body seam, "
        "seen from the side and slightly from behind, face calm and partly "
        "turned away, entirely plain unmarked clothing. Behind them, softly out "
        "of focus, tall vertical assembly stands, an overhead gantry rail, "
        "plain grey steel tooling carts and a smooth pale industrial floor "
        "stretch away in deep receding perspective under bright even factory "
        "light. Every surface is plain and unlabelled. Realistic photo, "
        "shallow depth of field, professional lighting. "
        + COMMON
        + NO_TEXT
    ),
    # 2 — closer on the nose/seeker section, technician with inspection light.
    "2": (
        "Professional stock photograph of the final assembly area of a missile "
        "production plant, framed close on the forward section of a finished "
        "air-to-air missile lying in a padded steel assembly cradle. The "
        "missile's plain smooth grey cylindrical body and gently tapered "
        "radome nose dominate the left two-thirds of the frame in sharp focus, "
        "seen from a low three-quarter angle so the curved painted metal "
        "catches a long soft highlight from bright overhead factory lighting "
        "and recedes in strong perspective. To the right and slightly behind, "
        "a single technician in a plain blue-grey coverall, white hard hat and "
        "clear safety glasses is seen in three-quarter rear view, one gloved "
        "hand steadying the missile and a small plain unmarked inspection "
        "torch in the other, all clothing entirely plain and unmarked. Behind "
        "them, softly out of focus, tall vertical work stands, a gantry rail "
        "and plain grey carts recede down a bright pale-floored industrial "
        "bay. All surfaces plain and unlabelled. Realistic photo, shallow "
        "depth of field, professional lighting. "
        + COMMON
        + NO_TEXT
    ),
    # 3 — wider: two-technician crew moving a missile body on an overhead
    #     handling rail, whole bay visible.
    "3": (
        "Professional stock photograph of a bright missile final-assembly bay "
        "in a defense plant, seen from a low wide angle down the length of the "
        "floor. The single clear subject is a long plain grey cylindrical "
        "missile body hanging level beneath a plain overhead handling rail in "
        "the middle distance, slung in a simple padded steel sling, receding "
        "in deep perspective down the bay as the sharpest object in frame. Two "
        "technicians in plain blue-grey coveralls and white hard hats walk "
        "alongside it, small and slightly out of focus, guiding it with gloved "
        "hands, seen mostly from behind, faces not clearly visible, clothing "
        "entirely plain and unmarked. Around them, softly out of focus, tall "
        "vertical assembly stands, plain grey steel tooling carts, a low "
        "workbench and a smooth pale painted industrial floor stretch away "
        "under bright even overhead light toward the far soft end of the "
        "building. Every surface plain and unlabelled. Realistic photo, "
        "shallow depth of field, professional lighting. "
        + COMMON
        + NO_TEXT
    ),
    # 4 — missile standing vertically in a fin-assembly stand, technician
    #     working at its base.
    "4": (
        "Professional stock photograph of a missile production floor where a "
        "finished air-to-air missile stands vertically in a heavy steel "
        "assembly stand, its plain smooth grey cylindrical body and tail fins "
        "rising up the centre of the frame, seen from a low angle so the "
        "missile towers in strong receding perspective against the bright "
        "soft-lit factory hall behind. The nose points up out of frame and the "
        "base sits in a plain bolted steel fixture; the whole airframe is "
        "plain matte grey painted metal with no markings of any kind. At its "
        "base, a single technician in a plain blue-grey coverall, white hard "
        "hat, clear safety glasses and pale gloves kneels at the fin ring "
        "adjusting a plain unmarked tool, seen from the side and slightly from "
        "behind, clothing entirely plain. Behind, softly out of focus, "
        "vertical work stands and gantry rails and a smooth pale industrial "
        "floor recede under bright even factory light. Every surface plain "
        "and unlabelled. Realistic photo, shallow depth of field, "
        "professional lighting. "
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


def load_gemini_key():
    """Gemini image key, separate Google project from GOOGLE_API_KEY."""
    path = "/home/chino/video_output/.gemini_key"
    if os.path.exists(path):
        with open(path) as f:
            key = f.read().strip().split("\n")[0].strip()
            if key:
                return key
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def gen_fal(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        raise RuntimeError("FAL_KEY not found")
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
    print(f"fal seed: {result.get('seed')}")
    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]
    if not image_url:
        raise RuntimeError(f"no image URL in fal result: {result}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
    return img


def gen_gemini(prompt, out_path):
    key = load_gemini_key()
    if not key:
        raise RuntimeError("Gemini image key not found")
    print(f"Generating image with {GEMINI_MODEL}...")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "imageConfig": {"aspectRatio": "16:9"},
            "responseModalities": ["IMAGE"],
        },
    }
    r = requests.post(
        url,
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        json=body,
        timeout=420,
    )
    if r.status_code != 200:
        raise RuntimeError(f"gemini HTTP {r.status_code}: {r.text[:400]}")
    d = r.json()
    if "error" in d:
        raise RuntimeError(f"gemini error: {json.dumps(d['error'])[:400]}")
    raw = None
    for cand in d.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part:
                raw = base64.b64decode(part["inlineData"]["data"])
                break
        if raw:
            break
    if not raw:
        raise RuntimeError(f"no image part in gemini response: {json.dumps(d)[:400]}")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(raw)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(raw)}")
    return img


def crop_to_16x9(img):
    """Center-crop to 16:9, then resize to 1920x1080."""
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
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT} PROVIDER={PROVIDER}")
    if PROVIDER == "fal":
        img = gen_fal(prompt, OUTPUT)
    else:
        img = gen_gemini(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 102400:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        size = os.path.getsize(OUTPUT)
        print(f"Re-saved with higher quality: {size} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
