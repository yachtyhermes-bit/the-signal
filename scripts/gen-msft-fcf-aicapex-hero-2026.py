#!/usr/bin/env python3
"""Generate hero for msft-free-cash-flow-ai-capex-payback-2026 (fal flux/schnell).

Subject: Microsoft's AI capital-spending squeeze, seen from the finance side —
a corporate finance team in a glass-walled boardroom reviewing printed
financial statements and a laptop, late-afternoon / dusk light, city skyline
behind the glass.

  ATTEMPT 1 — three finance people around a boardroom table, printed statement
  pages spread out, laptop open, skyline behind glass, dusk backlight.
  ATTEMPT 2 — two people, one standing at the glass looking at the skyline,
  one seated over the spreadsheets; unbranded laptop lid, film look.
  ATTEMPT 3 — closer over-the-shoulder on hands and papers, one face out of
  focus, skyline bokeh, unbranded equipment.

Deliberately NOT a data center / server room / server aisle / rack corridor.
No digital art, neon, synthwave, glowing lines, geometric abstraction,
charts, text, logos.

HARD CAP: 3 fal flux/schnell generations total (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-msft-fcf-aicapex-hero-2026.py
"""
import os
import shutil
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "msft-free-cash-flow-ai-capex-payback-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
REPO_COPY = f"/home/chino/thesignal/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The image contains absolutely no readable writing: no text, no letters, "
    "no numbers, no words, no handwriting, no printed paragraphs, no column "
    "headings, no signage, no labels, no stickers, no whiteboard content, no "
    "brand names, no corporate logos, no manufacturer emblems, no watermark, "
    "no captions, no on-screen interface text. Every laptop and phone is a "
    "plain unbranded matte shell with a completely blank outer lid, with no "
    "logo, no apple-shaped or bitten-fruit emblem, no badge and no insignia of "
    "any kind. All documents are seen from a distance or at an angle at which "
    "the ruling lines and tables read only as faint grey horizontal bands and "
    "blurs of ink, never as legible characters; the laptop screen is turned "
    "away from camera and its contents are never visible. No illustration, no "
    "digital art, no cartoon, no 3D render, no CGI, no neon, no synthwave, no "
    "glowing lines, no light trails, no futuristic HUD graphics, no "
    "augmented-reality overlays, no abstract digital patterns, no charts, no "
    "graphs, no data visualization, no infographic shapes. This is a "
    "corporate boardroom, not a data center: no server room, no server aisle, "
    "no server racks, no rack of blinking lights, no computer room, no "
    "corridor of cabinets, no cabling, no network hardware."
)

STYLE = (
    "Photo-realistic editorial photograph, shot on a full-frame camera with a "
    "35mm lens at f/2.8, natural available light only, not a render and not "
    "CGI, looks like a real photograph taken by a human on assignment: "
)

TAIL = (
    " Late afternoon into early dusk: low warm sun rakes in from behind the "
    "skyline, mixing with cool dim interior fill, soft and diffuse, no glare, "
    "no light bloom, nothing emitting its own light, no LED strips, no neon "
    "signs. Real optical lens blur, shallow but honest depth of field, "
    "natural sensor noise, fine film grain, subtle vignette, believable skin "
    "texture with pores and small imperfections, believable fabric weave, "
    "believable paper and glass, slightly off-centre casual framing, slight "
    "handheld tilt, no CGI sheen, no plastic skin, no perfect symmetry, "
    "authentic editorial reportage. Photorealistic, extremely high detail, "
    "16:9 landscape composition, wide horizontal framing. "
)

PROMPTS = {
    "1": STYLE + (
        "inside a modern corporate boardroom on a high floor of a city office "
        "tower, seen from one end of a long dark wood conference table. Three "
        "finance professionals in business attire — a woman in her forties in "
        "a navy blazer seated at the near end, turned three-quarters toward "
        "the camera leaning over an open laptop, and two colleagues further "
        "down the table, one standing with sleeves rolled up and one seated, "
        "both absorbed in the documents in front of them, faces in soft focus "
        "and not identifiable. The table is strewn with stacks of printed "
        "financial statements and printed spreadsheets, loose pages, a few "
        "paper-clipped printouts, a couple of ballpoint pens, a black coffee "
        "cup, a smartphone lying face down, and a slim open laptop whose "
        "blank unbranded lid faces the camera. The printed pages show only "
        "soft grey bands of tabular ruling and blurred columns of ink at this "
        "viewing distance. Behind them the entire far wall "
        "is floor-to-ceiling glass, and beyond it a dense downtown skyline of "
        "glass and concrete towers in hazy blue-grey layers under a warm "
        "orange and pale rose dusk sky, with a few windows faintly reflecting "
        "the setting sun. Thin dark mullions divide the glass. Interior walls "
        "are warm grey acoustic panel, a single large abstract canvas hangs "
        "unlabelled and blank-toned on the left wall, a long linear pendant "
        "light fixture hangs unlit above the table. The near end of the table "
        "and the woman's hands and laptop keyboard are razor sharp; the "
        "paperwork, the colleagues and the skyline fall into gentle bokeh."
    ) + TAIL + NO_TEXT,
    "2": STYLE + (
        "candid documentary photograph taken with a 35mm film camera on Kodak "
        "Portra 400, available window light, visible fine film grain and "
        "slight natural overexposure in the highlights, an ordinary un-posed "
        "moment inside a glass-walled executive meeting room at dusk, camera "
        "at standing eye level a few metres back. Two people: a man in his "
        "fifties in a dark suit, seen from behind and slightly to the side as "
        "a soft silhouette, stands close to the floor-to-ceiling window with "
        "one hand in his pocket looking out at the city; a woman in a light "
        "grey blouse sits at the near corner of the conference table with her "
        "back half to camera, elbows on the table, reading a thick stack of "
        "printed financial statements. On the table between them: several "
        "stapled printouts and loose spreadsheet pages fanned out, a plain "
        "leather folio, reading glasses folded on top of a document, a glass "
        "of water, and a closed laptop with a completely blank plain matte "
        "grey lid carrying no markings and no emblem. The printed pages read "
        "only as pale rectangles with faint grey horizontal ruling, never "
        "legible. Outside the glass, a downtown skyline of generic office "
        "towers recedes in hazy blue layers under a low warm sunset glow near "
        "the horizon; a few lit windows are the only bright points, and no "
        "building carries any signage or lettering. Reflections of the room "
        "float faintly on the inner surface of the glass. Pale oak floor, "
        "matte white ceiling with recessed downlights switched off, one bare "
        "dark wood credenza along the right wall with nothing on it. The "
        "woman's hands and the nearest papers are sharp; the standing man and "
        "the skyline are soft. Ordinary corporate furniture with honest wear, "
        "natural colour falloff from warm daylight into cool dusk."
    ) + TAIL + NO_TEXT,
    "3": STYLE + (
        "candid documentary photograph made on 35mm colour negative film, "
        "scanned, with visible fine grain, slightly uneven natural white "
        "balance, gentle motion blur on the moving hand, imperfect focus and "
        "soft corners, an ordinary un-posed moment in a corporate finance "
        "office at dusk. Over-the-shoulder view: camera just behind and above "
        "the shoulder of a person in a white shirt with sleeves rolled to the "
        "forearm, whose out-of-focus shoulder and back of the head occupy the "
        "left edge of the frame, face turned away and not visible. In the "
        "sharp focal plane, their hand rests on a thick printed financial "
        "statement lying open on the table, forefinger tracing down the page; "
        "a second stack of printouts sits squared up beside it with a paper "
        "clip and a plain mechanical pencil on top. The page is seen at a low "
        "oblique angle so rows of figures compress into fine grey tonal bands "
        "and blurred ink marks, not readable characters. Just beyond the "
        "papers, an open laptop is angled away from the camera so only its "
        "blank plain matte back is visible, unmarked, no emblem. Across the "
        "table, softly out of focus, a second colleague in a dark blazer sits "
        "with their back three-quarters to camera, head turned down toward "
        "their own papers, face not visible. Behind them, floor-to-ceiling "
        "glass shows a downtown skyline in dusk haze, towers stacked in muted "
        "blue-grey with a warm apricot band of sky low down, a few "
        "aircraft-warning lights just beginning to glow. Warm low sunlight "
        "grazes the tabletop and the edge of the paper, everything else in "
        "cool soft shadow. Hands with visible knuckles, veins and short "
        "fingernails, honest skin texture, one fingernail slightly uneven."
    ) + TAIL + NO_TEXT,
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
    os.makedirs(os.path.dirname(REPO_COPY), exist_ok=True)
    shutil.copy(OUTPUT, REPO_COPY)
    print(f"Mirrored to {REPO_COPY}")


if __name__ == "__main__":
    main()
