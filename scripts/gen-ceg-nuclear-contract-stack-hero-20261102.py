#!/usr/bin/env python3
"""Hero for ceg-nuclear-contract-stack-2026 (fal flux/schnell).

Subject: Constellation Energy (CEG) — largest US nuclear fleet operator,
signing long-term power purchase agreements with AI hyperscalers.

Scene: a large nuclear generating station at dusk — two concrete cooling
towers venting soft white steam, high-voltage transmission lines and steel
lattice pylons heading off toward the horizon, warm amber sunset light on the
towers, deep blue sky with thin clouds, chain-link security fence in the near
foreground. Editorial/documentary realism, 35mm, shallow DOF.

NO text, no logos, no signage, no people, no data-center interior, no neon,
no digital art, no CGI look, no glowing lines.

HARD CAP: 3 fal flux/schnell generations (ATTEMPT 1-3). Never a 4th.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-ceg-nuclear-contract-stack-hero-20261102.py
"""
import os
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ceg-nuclear-contract-stack-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/%s.jpg" % SLUG
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/%s.jpg" % SLUG
W, H = 1536, 864
MAX_BYTES = 400_000

NO_TEXT = (
    "Absolutely no text anywhere in the image: no words, no letters, no "
    "numerals, no signage, no warning placards, no labels, no billboards, no "
    "brand names, no logos, no corporate marks, no watermarks, no captions, "
    "no signatures, no legible writing of any kind on any surface. "
    "No people and no human figures anywhere in the frame. Not an "
    "illustration, not digital art, not a 3D render, not CGI, not matte "
    "painting, no neon, no synthwave, no glowing lines, no light trails, no "
    "geometric patterns, no abstract shapes, no data visualization, no HUD "
    "overlays, no split screen, no collage. Not a data center, not a server "
    "room, not a server aisle, not server racks. Strictly photo-realistic "
    "editorial stock photography with true-to-life materials, real lens "
    "optics, natural film grain and honest atmospheric haze."
)

PROMPTS = {
    # 1: the brief, wide — two towers, pylons, fence, sunset
    "1": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "full-frame camera with a 35mm lens at f/4, from a low rise of rough "
        "grass beside a large nuclear generating station at dusk. Two vast "
        "hyperboloid concrete cooling towers dominate the middle distance, "
        "their weathered grey concrete streaked with rain stains and faded "
        "mineral bloom, both venting thick soft white plumes of steam that "
        "drift and flatten toward the right under a light breeze. The last of "
        "the sunset catches the towers warm amber and rose on their left "
        "flanks while their shadowed sides fall into cool grey-blue. Behind "
        "them, low and partly hidden, the pale boxy turbine hall and a slim "
        "vent stack with a faint wisp from its top. To the right, a line of "
        "tall steel lattice transmission pylons marches away toward the "
        "horizon, carrying heavy conductors and a catenary of high-voltage "
        "lines that step down in perspective and disappear into the haze. "
        "In the near foreground, slightly out of focus, a galvanised "
        "chain-link security fence runs diagonally across the bottom of the "
        "frame with its plain steel posts, tension wire and a coiled razor "
        "coil along the top; beyond it a strip of mown grass and a gravel "
        "service track. Deep blue evening sky above, layered with thin "
        "streaked cirrus lit pink and apricot near the horizon on the left, "
        "already going indigo overhead. A single distant sodium work light "
        "glows warm at the base of a tower. Wide horizontal framing, the "
        "towers placed left of centre with open sky to the right, the fence "
        "anchoring the lower third. Real atmospheric perspective, distance "
        "haze softening the far pylons, natural sensor noise, fine film "
        "grain, subtle vignette, no HDR, no clarity boost, no digital "
        "polish, believable mundane industrial landscape. Photorealistic, "
        "extremely high detail, authentic editorial photography. " + NO_TEXT
    ),
    # 2: closer — tower base and switchyard, fence sharp in foreground
    "2": (
        "Professional editorial stock photograph, horizontal 16:9, full-frame "
        "camera, 35mm lens at f/2.8, eye level just outside the perimeter of "
        "a nuclear power station at last light. In the sharp near foreground "
        "a galvanised chain-link fence fills the bottom left of the frame, "
        "its diamond mesh and plain steel top rail rim-lit warm, a few dry "
        "weeds and grass stalks caught in the mesh; focus lands on the fence "
        "wire, the world beyond falling gently out of focus. Beyond it, at "
        "medium distance, one enormous concrete cooling tower rises out of "
        "frame at the top, its curved base and buttressed legs dark against "
        "the sky, a broad soft white steam plume pouring from its mouth and "
        "catching the dying amber sun so its upper edge glows peach and "
        "gold. Between the fence and the tower lies an electrical switchyard: "
        "grey steel gantries, ribbed porcelain insulators, busbars, a bank of "
        "transformer tanks with cooling fins, and a run of heavy cables "
        "sagging between frames, all of it unlit and matter-of-fact. To the "
        "right two lattice pylons stand against the sky with their conductor "
        "bundles sweeping out of frame. Sky is deep blue overhead shading to "
        "burnt orange near the horizon behind the tower, with thin ragged "
        "cloud catching the last light, and one faint early star. Warm "
        "low-angle rim light on metal and concrete, cool blue shadow in the "
        "foreground, real contrast between the two. Shallow depth of field, "
        "authentic lens blur, natural grain, faint chromatic aberration at "
        "the edges, slight vignette, scuffed and weathered surfaces, no "
        "glossy CGI sheen. Photorealistic, extremely high detail, "
        "documentary editorial photography. " + NO_TEXT
    ),
    # 3: wide horizon, long line of pylons receding, both towers right
    "3": (
        "Professional editorial stock photograph, horizontal 16:9, shot on a "
        "full-frame camera with a 35mm lens at f/5.6 from an open field "
        "half a kilometre from a nuclear generating station, looking across "
        "flat farmland at sunset. A long line of steel lattice transmission "
        "pylons runs from the right foreground straight back to the plant, "
        "the nearest pylon cropping the top right corner with its insulators "
        "and bundled conductors clearly rendered, the rest stepping down in "
        "perfect perspective toward the horizon where they meet the "
        "switchyard. At the end of that line, two concrete cooling towers "
        "stand side by side on the right third of the frame, small in scale "
        "against the sky but unmistakable, both emitting broad soft white "
        "steam plumes that lean left and dissolve into the evening air; the "
        "low sun behind them rims their left edges in amber and turns the "
        "steam a warm cream. Between the pylons and the towers, a hazy band "
        "of bare winter trees, a distant farm shed with a dark roof, and "
        "faint grey outbuildings. The foreground is ordinary rough pasture: "
        "tussocked grass, a fence line of leaning wooden posts and three "
        "strands of wire running out of frame at the bottom edge, a puddle "
        "holding the orange sky. Big open sky occupying the upper two thirds, "
        "graded from deep indigo at the top through slate blue to a wide "
        "band of amber, apricot and dusty rose at the horizon, with long thin "
        "streaks of high cloud. Distance haze greys out the far pylons and "
        "the plant; real atmospheric layering, natural sensor noise, fine "
        "film grain, gentle vignette, no HDR, no saturation push, quiet and "
        "believable. Photorealistic, extremely high detail, authentic "
        "editorial landscape photography. " + NO_TEXT
    ),
}


def load_fal_key():
    for path in ("/home/chino/hermes-workspace/studio-api/.env",
                 "/home/chino/video_output/.fal_real"):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
                if path.endswith(".fal_real") and line.strip():
                    raw = line.strip()
                    key = raw.split("|", 1)[1] if "|" in raw else raw
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def generate(prompt, out_path, seed=None):
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if seed is not None:
        args["seed"] = int(seed)
    print("Generating with fal flux/schnell ...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    url = (result.get("images") or [{}])[0].get("url") or result.get("image")
    if not url:
        print("ERROR: no image url: %s" % result)
        sys.exit(1)
    print("Image URL: %s" % url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded %s size=%s bytes=%d" % (out_path, img.size, len(r.content)))
    return img


def save_capped(img, path):
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def main():
    if ATTEMPT not in PROMPTS:
        print("ERROR: no prompt for ATTEMPT=%s (hard cap 1-3)" % ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=%s ATTEMPT=%s" % (SLUG, ATTEMPT))
    img = generate(prompt, OUTPUT, os.environ.get("SEED") or None)
    if img.size != (W, H):
        resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
        img = img.resize((W, H), resample)
    img = img.convert("RGB")
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    save_capped(img, BACKUP)
    print("VERIFY %s dims=%s bytes=%d" % (OUTPUT, img.size, os.path.getsize(OUTPUT)))


if __name__ == "__main__":
    main()
