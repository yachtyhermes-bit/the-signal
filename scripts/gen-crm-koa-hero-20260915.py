#!/usr/bin/env python3
"""Generate hero for salesforce-koa-reasoning-model-agentforce-2026 (fal flux/schnell).

Subject: Salesforce + NVIDIA 'Koa' — Salesforce's first CRM reasoning model,
built for Agentforce (enterprise sales / service / marketing agents).

Scene chosen: enterprise software at work AMONG PEOPLE — a close, human moment
of a service/sales professional at their desk mid-conversation on a headset,
with a softly blurred bright open-plan office behind them. Real people doing
real work, the software implied rather than shown.

Deliberately NOT a data-center / server-rack / cable-run / silicon-die / GPU /
rocket composition. No neon, no glowing lines, no HUD overlays, no 3D-render
look, no geometric patterns, no digital art.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial business-press stock photograph ONLY.
- TEXT-FREE: desks naturally carry screens, keyboards, badges and signage, so
  all lettering, UI, logos and brand names are explicitly forbidden.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-crm-koa-hero-20260915.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "salesforce-koa-reasoning-model-agentforce-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no user interface, no software windows, "
    "no dashboards, no chat windows, no toolbars, no menus, no icons, no "
    "filename labels, no captions, no subtitles, no keyboard lettering, no "
    "name badges, no lanyards, no printed signage, no whiteboard writing, no "
    "post-it note writing, no brand names, no manufacturer names, no company "
    "names, no logos, no trademarks, no watermarks, no stickers, no barcodes, "
    "no QR codes, no legible writing of any kind anywhere in the image. Every "
    "computer monitor in the frame is angled away, turned off, or so far out "
    "of focus that it shows only a soft flat wash of colour with absolutely "
    "nothing readable or drawn on it, like an out-of-focus colour field "
    "photograph, not a computer screen with content. The keyboards are plain "
    "and blank, the headsets are plain and unmarked, all clothing is plain and "
    "unbranded, the walls carry only plain paint, and any notepads or papers "
    "are blank with no writing on them. No illustration, no digital art, no "
    "cartoon, no 3D render, no CGI, no neon, no glowing lines, no light "
    "trails, no synthwave, no geometric patterns, no network diagram, no graph "
    "graphic, no futuristic HUD graphics, no overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no cable runs, no server lights, no GPU hardware, no computer "
    "screen with text."
)

PROMPTS = {
    "1": (
        "Photo-realistic editorial business-press stock photograph of a "
        "customer-service professional mid-conversation at their desk in a "
        "bright modern office, shot from behind and slightly to the side over "
        "their shoulder at eye height. In the near foreground and tack sharp, "
        "the back of a person's head and shoulders — natural dark hair tied "
        "back, a plain unbranded light blue shirt, one hand raised loosely "
        "near their cheek mid-sentence and the other resting near a plain "
        "blank keyboard — with a slim unmarked matte black headset boom "
        "curving past their jaw, the microphone tip small and unlabelled. "
        "Their posture is relaxed and attentive, the shoulders slightly "
        "turned, clearly listening and talking, not posing. On the desk in "
        "front of them sit a plain white ceramic mug, a loose blank notepad "
        "with nothing written on it, and a couple of plain pens. Behind them, "
        "falling away into beautiful smooth bokeh, the bright open-plan "
        "office stretches out: a long row of colleagues at similar desks "
        "seen from behind, several wearing plain headsets, softly out of "
        "focus and clearly at work. None of the monitors in the frame are "
        "legible — they are angled away or blurred to soft flat washes of "
        "pale colour. Daylight floods in from tall windows along the left, "
        "backlighting faint highlights in the hair and shoulders of the near "
        "subject and filling the room with clean warm-white light. Very "
        "shallow depth of field: the near headset boom, ear and shoulder are "
        "crisp while the office behind melts into creamy bokeh. Real optical "
        "blur, honest natural lighting with gentle quiet contrast, subtle "
        "lens vignette, natural camera noise and very slight film grain, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "2": (
        "A real photograph taken on an 85mm lens at f/1.4, not a render and "
        "not computer generated: a warm, human moment in a bright modern "
        "office, styled as an authentic business-press stock photo. A "
        "service professional sits at their desk turned three-quarters away "
        "from camera, caught mid-conversation — mouth slightly open, "
        "listening intently, wearing a plain unmarked over-ear headset with a "
        "thin boom microphone, dressed in a simple plain grey knit sweater "
        "with no branding anywhere. Their hand holds a plain pen above a "
        "blank open notebook. The near side of their face, cheek, ear and the "
        "curve of the headset are tack sharp, the rest of the frame falling "
        "gently out of focus. Beyond them, softened into creamy blur, is a "
        "light-filled open-plan floor: two or three colleagues in plain "
        "clothing talking near a glass-walled meeting room whose glass "
        "carries no writing or frosting graphics, a few desks with plain "
        "monitors angled away from camera and glowing only as soft pale "
        "colour, a tall potted plant, and daylight pouring through floor-to-"
        "ceiling windows on the right. Warm neutral palette of soft greys, "
        "pale oak desk surfaces and clean daylight white. Extremely shallow "
        "depth of field with smooth heavy bokeh behind the subject, honest "
        "available-light editorial exposure, natural camera noise and very "
        "slight film grain, faint dust in the light, subtle lens vignette, "
        "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    "3": (
        "A genuine documentary-style photograph, not a render and not "
        "computer generated, of a sales and support team at work in a bright "
        "contemporary office, composed in a wide editorial frame. In the "
        "sharp near foreground on the left, seen from behind and to the "
        "side, a woman in a plain white blouse and plain dark blazer sits at "
        "a pale oak desk wearing a slim unmarked headset, phone conversation "
        "implied by her turned head and gesturing free hand, a plain blank "
        "notepad and an unbranded pen under her forearm, a plain white mug "
        "beside them. To her right, further back and softening into blur, "
        "two colleagues stand together in the aisle in mid-discussion, both "
        "in plain unbranded business-casual clothing, one holding a plain "
        "unmarked folder, in front of a glass-walled meeting room whose walls "
        "are clear and carry absolutely no writing, no graphics and no "
        "frosted lettering. Behind them the open-plan floor recedes into "
        "smooth bokeh: softly blurred desks, plain monitors turned away from "
        "camera or switched off to dark blank glass, a tall plant, acoustic "
        "pendant lights hanging overhead. Bright clean daylight streams in "
        "through large windows on the left, giving soft directional light "
        "across the desks with gentle shadow falloff and warm bounce off the "
        "pale floor. Shallow depth of field holding the near woman crisp "
        "while everything past her shoulder melts into creamy bokeh, real "
        "optical blur, honest editorial exposure, natural camera noise and "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, "
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
