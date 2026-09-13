#!/usr/bin/env python3
"""Generate hero image for googl-finland-nuclear-ai-power-2026.

Story: Alphabet/Google is investing EUR 13bn+ in AI infrastructure in Finland
across 2027-2028, bundled with a 22-year PPA for up to 50% of Fortum's Loviisa
nuclear plant output, plus onshore wind PPAs, a 94 MW grid-connected battery
near Kajaani and grid improvements. Theme = POWER + GEOGRAPHY, Nordic coast.

Distinctive point: Nordic coastal nuclear power station / frozen Baltic
shoreline with wind turbines and transmission pylons — NOT a modular
data-center construction site, NOT a server aisle, NOT abstractions.

Text-free photo-realistic stock photography, 16:9 1920x1080 center-crop.

Usage: python3 gen-googl-finland-hero-20260913.py [1|2|3]
"""
import os
import sys
import io
import requests
from PIL import Image

SLUG = "googl-finland-nuclear-ai-power-2026"

# Shared negative-style guard tail required on every prompt.
GUARD = (
    "No text, no letters, no numbers, no signage, no warning signs, no labels, no logos, "
    "no brand marks, no screens, no monitors, no displays, no UI, no people, no illustration, "
    "no digital art, no neon, no glowing lines, no holograms, no abstract shapes, "
    "no geometric patterns, no server room, no data center hallway, no server racks indoors."
)

PROMPTS = {
    # Variant 1 — Nordic coastal nuclear station, low raking dawn light, ice at the shore
    1: (
        "Professional stock photograph of a Nordic coastal nuclear power station on the Baltic "
        "coast of Finland at sunrise: massive pale gray concrete reactor buildings with a single "
        "smooth containment dome and heavy flat-roofed turbine halls, two tall white plumes of "
        "condensation steam rising straight up into a pale cold blue northern sky and drifting "
        "slightly sideways, the plant sitting on a low rocky granite headland beside dark slate-"
        "blue sea water with thin broken sheets of ice and slush along the shoreline, snow-dusted "
        "spruce and pine forest framing the left and right edges of the frame, low raking golden "
        "Nordic winter light grazing across the concrete facades and casting long cold shadows, "
        "a steel lattice transmission gantry and a few high-voltage pylons carrying lines away "
        "inland in the middle distance, gravel access road and a plain chain-link fence with no "
        "markings in the foreground, crisp clean air, cinematic wide landscape photography, "
        "natural realistic lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        + GUARD
    ),
    # Variant 2 — frozen Arctic coastline: wind turbines + transmission pylons to a data-center campus
    2: (
        "Professional stock photograph of a frozen Arctic coastline in northern Finland at twilight: "
        "a row of very tall white three-bladed onshore wind turbines standing on a low snow-"
        "covered granite shore, dark icy water of the Gulf of Bothnia with shattered pack ice and "
        "snow drifts on the rocks in the foreground, a long line of tall steel lattice high-voltage "
        "transmission pylons marching from the turbines across the snowy coastal plain toward a "
        "compact industrial campus in the middle distance made of low flat-roofed pale concrete "
        "buildings with a few cooling units and no markings whatsoever, transformer yard and "
        "switchgear beside the pylons, deep blue and faint violet twilight sky with a low band of "
        "dull orange light along the horizon, overhead power lines strung between the pylons, "
        "crisp cold winter atmosphere, wide cinematic industrial landscape photography, natural "
        "realistic lighting, sharp detail, 4K, shot on a full-frame DSLR, photo-realistic. "
        + GUARD
    ),
    # Variant 3 — the two-reactor plant seen across calm icy water, cold gray daylight
    3: (
        "Professional stock photograph of two large pressurised-water nuclear reactor units on a "
        "Finnish Baltic island seen from across a wide stretch of calm cold sea water: two pale "
        "gray concrete reactor buildings with gently domed containment roofs standing side by side "
        "beside long low turbine halls and auxiliary blocks, thin white trails of steam drifting "
        "from the roof vents into an overcast pale gray winter sky, the island shore lined with "
        "granite outcrops dusted with snow and a fringe of broken ice floating on the near-black "
        "water, dark snow-dusted spruce forest behind the plant buildings, a lattice high-voltage "
        "transmission tower on the far right carrying lines toward the mainland, muted blue-gray "
        "and white winter palette, soft diffused overcast light with no harsh shadows, distant "
        "documentary industrial landscape photography, sharp detail, 4K, shot on a full-frame "
        "DSLR, photo-realistic. "
        + GUARD
    ),
}

TARGET_W, TARGET_H = 1920, 1080
OUT_DIR = "/home/chino/thesignal/public/img/articles"
BACKUP_DIR = "/home/chino/thesignal/_backup_dist/img/articles"


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)


def generate(prompt):
    import fal_client
    print("Prompt: " + prompt[:200] + "...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": 1440, "height": 810},
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
        raise RuntimeError("Could not find image URL in result: " + str(list(result.keys())))
    print("Image URL: " + str(image_url))
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    return r.content


def process_and_save(data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print("Raw dimensions: " + str(w) + "x" + str(h))
    target_ratio = TARGET_W / TARGET_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    if img.size != (TARGET_W, TARGET_H):
        img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, SLUG + ".jpg")
    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print("Saved " + out_path + " (" + str(img.size[0]) + "x" + str(img.size[1]) + ", " + str(os.path.getsize(out_path)) + " bytes)")
    bak = os.path.join(BACKUP_DIR, SLUG + ".jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=92, optimize=True)
    print("Mirrored to " + bak)
    return out_path


def main():
    attempt = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    load_fal_key()
    print("=== [" + SLUG + "] attempt " + str(attempt) + " ===")
    data = generate(PROMPTS[attempt])
    process_and_save(data)
    print("DONE")


if __name__ == "__main__":
    main()
