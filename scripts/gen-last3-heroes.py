#!/usr/bin/env python3
"""Generate hero images for the 3 latest readthesignal.net articles using FAL flux/schnell.

Articles (2026-08-07):
  zs-cloud-native-zero-trust-moat-2026      (Zscaler — cloud Zero Trust, 160+ DCs, 750B tx/day)
  panw-ai-security-supercycle-2026          (Palo Alto Networks — AI security supercycle, NGS ARR)
  intc-historic-q2-2026-earnings-turnaround-2026  (Intel — best quarter in 15 years, 18A ramp)
"""

import os
import sys
import requests

W, H = 1200, 675
BASE = "/home/chino/thesignal"

ARTICLES = [
    {
        "slug": "zs-cloud-native-zero-trust-moat-2026",
        "prompt": (
            "Professional stock photograph of a massive global cloud security network visualized as a glowing "
            "fabric of interconnected data centers spanning the globe. A central luminous proxy exchange node "
            "surrounded by a halo of blue light, with countless fiber-optic data streams flowing between server "
            "racks. Rows of modern data center server cabinets with blue LED status lights in the foreground, "
            "soft depth of field. A translucent shield-like digital firewall surface hovering over the network "
            "grid. Dark navy atmosphere with electric cyan and blue accent lighting. Photo-realistic, cinematic "
            "grading, professional industrial photography, 8K resolution. No text overlays, no logos, no "
            "branding, no watermarks. Conveys a cloud-native zero trust security fabric at planetary scale."
        ),
    },
    {
        "slug": "panw-ai-security-supercycle-2026",
        "prompt": (
            "Professional stock photograph of a futuristic security operations command center facing a massive "
            "wall of glowing displays showing an AI-driven network defense grid. In the center, a large "
            "holographic artificial intelligence core — a luminous neural network sphere of interconnected "
            "nodes — radiating red and amber energy, symbolizing an AI security platform. Dark modern SOC "
            "environment with black and crimson accents, analysts silhouetted at consoles, screens casting "
            "electric red-blue light. Dramatic atmospheric haze, cinematic lighting, shallow depth of field. "
            "Photo-realistic, 8K resolution, professional cinematic grading. No text overlays, no logos, no "
            "readable screens, no branding. Conveys an AI security supercycle — machine-speed defense at scale."
        ),
    },
    {
        "slug": "intc-historic-q2-2026-earnings-turnaround-2026",
        "prompt": (
            "Professional stock photograph inside a state-of-the-art semiconductor fabrication cleanroom at "
            "golden hour. A close-up of a circular silicon wafer glinting under cool blue light in the "
            "foreground, held by a robotic arm, with rows of advanced lithography machines receding into a "
            "warm amber-lit distance. Technicians in white cleanroom suits monitoring glowing equipment. "
            "Polished reflective floors, dramatic mixed blue-amber lighting, cinematic atmosphere suggesting "
            "momentum and resurgence. Photo-realistic, shallow depth of field, professional industrial "
            "photography, 8K resolution. No text overlays, no logos, no branding. Subtle Intel-blue corporate "
            "tones. Conveys a historic manufacturing turnaround at full industrial scale."
        ),
    },
]

R2_BUCKET = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev"


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("FAL_KEY")


def main():
    import fal_client

    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    os.environ["FAL_KEY"] = key

    for art in ARTICLES:
        slug = art["slug"]
        print(f"\n{'='*70}\nGenerating hero for {slug}...")
        print(f"Prompt: {art['prompt'][:110]}...")

        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": art["prompt"],
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
            print(f"ERROR: no image URL in result for {slug}: {list(result.keys())}")
            sys.exit(1)

        print(f"Image URL: {image_url[:90]}...")
        r = requests.get(image_url, timeout=120)
        r.raise_for_status()
        img_data = r.content

        from PIL import Image
        outputs = [
            f"{BASE}/public/img/articles/{slug}.jpg",
            f"{BASE}/_backup_dist/img/articles/{slug}.jpg",
        ]
        for output_path in outputs:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(img_data)
            img = Image.open(output_path)
            if img.size != (W, H):
                img = img.resize((W, H), Image.LANCZOS)
                img.save(output_path, "JPEG", quality=92, optimize=True)
            size = os.path.getsize(output_path)
            print(f"✅ Saved {output_path} ({size/1024:.0f} KB, {img.size})")

        print(f"Uploading {slug} to R2...")
        rc = os.system(f"cd {BASE} && python3 scripts/r2_upload.py hero {slug}")
        if rc != 0:
            print(f"❌ R2 upload failed for {slug} (exit {rc})")
            sys.exit(1)

        r2_url = f"{R2_BUCKET}/img/articles/{slug}.jpg"
        try:
            resp = requests.get(r2_url, headers={"User-Agent": "Mozilla/5.0 Chrome/125", "Range": "bytes=0-1023"}, timeout=30)
            print(f"✅ R2 verify: HTTP {resp.status_code} — {r2_url}")
        except Exception as e:
            print(f"⚠️  R2 verify error: {e}")

    print("\n✅ All 3 hero images generated, saved, and uploaded!")


if __name__ == "__main__":
    main()
