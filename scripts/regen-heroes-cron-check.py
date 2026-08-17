#!/usr/bin/env python3
"""Regenerate failing hero images (keys, riot): text-free photo-realistic prompts, 16:9 1920x1080."""
import os
import sys
import io
import requests
from PIL import Image

# slug -> list of prompts (attempt 1, attempt 2 adjusted)
TARGETS = {
    "keys-ai-data-center-test-moat-2026": [
        # Attempt 1: test lab, blank unlit panels, no screens
        (
            "Professional stock photograph of a high-tech electronics testing laboratory for high-speed "
            "networking equipment. A clean white workbench with precision test instruments in matte "
            "brushed-metal enclosures with completely blank unlit front panels, neat bundles of grey and "
            "blue coaxial test cables routed to a bare green circuit board under test, a black rubber "
            "anti-static mat, bright even overhead lab lighting, shallow depth of field, realistic "
            "industrial photography, sharp focus on the instruments and cables, 4K, shot on a full-frame "
            "DSLR. "
            "No screens, no monitors, no displays, no computer UI, no text, no letters, no numbers, no "
            "signage, no labels, no logos, no brand markings, no people, no illustration, no digital art, "
            "no neon, no abstract shapes."
        ),
        # Attempt 2 (adjusted): focus on cable/rack hardware, further from any UI
        (
            "Professional stock photograph of a modern AI data center network row, tall matte-black server "
            "racks packed with dense network switch hardware, thick bundles of blue and purple high-speed "
            "copper and fiber cables neatly routed through cable trays overhead, subtle green and blue LED "
            "status lights on blank switch faceplates, cool ambient lighting, clean industrial environment, "
            "shallow depth of field, realistic photography, 4K, shot on a full-frame DSLR. "
            "No screens, no monitors, no displays, no computer UI, no text, no letters, no numbers, no "
            "signage, no labels, no logos, no brand markings, no people, no illustration, no digital art, "
            "no neon, no abstract shapes."
        ),
    ],
    "riot-anthropic-ai-data-center-lease-2026": [
        # Attempt 1: exterior aerial, inherently text-free
        (
            "Professional aerial photograph of a vast industrial data center campus at dusk on the flat "
            "Texas plains. Dozens of long low metal warehouse buildings with rows of massive cooling towers "
            "and chiller units, warm golden light glowing softly from louvered wall vents, a few utility "
            "vehicles parked in a lot, distant transmission towers and power lines, dramatic orange and "
            "purple sunset sky, realistic landscape photography, high dynamic range, 4K, shot on a "
            "full-frame DSLR from a helicopter. "
            "No screens, no monitors, no displays, no computer UI, no text, no letters, no numbers, no "
            "signage, no labels, no logos, no brand markings, no people, no illustration, no digital art, "
            "no neon, no abstract shapes."
        ),
        # Attempt 2 (adjusted): interior but only blank hardware, no overhead light fixtures with patterns
        (
            "Professional stock photograph of the interior of a large converted industrial data center "
            "hall. Rows of tall matte-black server racks with smooth completely blank front doors, soft "
            "diffused cool blue-white ambient lighting from hidden sources, dark polished concrete floor "
            "with subtle reflections, heavy-duty grey power distribution units with blank panels, clean "
            "minimal industrial aesthetic, shallow depth of field, realistic photography, 4K, shot on a "
            "full-frame DSLR. "
            "No screens, no monitors, no displays, no computer UI, no text, no letters, no numbers, no "
            "signage, no labels, no logos, no brand markings, no people, no illustration, no digital art, "
            "no neon, no abstract shapes."
        ),
    ],
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


def generate(slug, prompt, attempt):
    import fal_client
    print(f"\n=== [{slug}] attempt {attempt} ===")
    print(f"Prompt: {prompt[:160]}...")
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
        raise RuntimeError(f"Could not find image URL in result: {list(result.keys())}")
    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    return r.content


def process_and_save(slug, data):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print(f"Raw dimensions: {w}x{h}")
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
    out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Saved {out_path} ({img.size[0]}x{img.size[1]}, {os.path.getsize(out_path)} bytes)")
    bak = os.path.join(BACKUP_DIR, f"{slug}.jpg")
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    img.save(bak, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {bak}")
    return out_path


def main():
    load_fal_key()
    slugs = sys.argv[1:] if len(sys.argv) > 1 else list(TARGETS.keys())
    for slug in slugs:
        prompts = TARGETS[slug]
        for attempt, prompt in enumerate(prompts, start=1):
            try:
                data = generate(slug, prompt, attempt)
                process_and_save(slug, data)
                break
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt == len(prompts):
                    print(f"ERROR: all generation attempts failed for {slug}")
                    sys.exit(1)
    print("\nAll regenerations complete.")


if __name__ == "__main__":
    main()
