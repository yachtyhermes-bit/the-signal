#!/usr/bin/env python3
"""Generate hero images for the 5 most recent articles using FAL flux/schnell."""
import os, sys, requests
from PIL import Image

ARTICLES = [
    {
        "slug": "orcl-ai-infrastructure-backlog-2026",
        "prompt": (
            "Professional stock photograph of Oracle corporate headquarters. "
            "Modern glass office buildings with the red ORACLE logo on the exterior. "
            "Clean, corporate, professional photography. "
            "Photo-realistic, shallow depth of field, professional lighting. "
            "No AI art, no neon, no abstract. "
            "No model numbers, no serial numbers, no text labels, no markings — only the company logo. "
            "Clear blue sky, manicured landscaping, sharp focus, high detail."
        ),
    },
    {
        "slug": "aapl-ai-china-rally-2026",
        "prompt": (
            "Professional stock photograph of Apple Park, the Apple headquarters in Cupertino. "
            "The iconic circular glass building with the Apple logo. "
            "Clean, corporate, professional photography. "
            "Photo-realistic, shallow depth of field, professional lighting. "
            "No AI art, no neon, no abstract. "
            "No model numbers, no serial numbers, no text labels, no markings — only the company logo. "
            "Clear blue sky, manicured landscaping, sharp focus, high detail."
        ),
    },
    {
        "slug": "smci-ai-server-comeback-2026",
        "prompt": (
            "Professional photograph of AI server racks in a modern data center. "
            "Rows of high-performance computing servers with liquid cooling pipes. "
            "Clean, corporate, professional photography style. "
            "Photo-realistic, shallow depth of field, professional lighting. "
            "No AI art, no neon, no abstract. "
            "No model numbers, no serial numbers, no text labels, no markings. "
            "Blue LED lights, sharp focus, high detail."
        ),
    },
    {
        "slug": "sofi-everything-app-bank-charter-2026",
        "prompt": (
            "Professional photograph of the SoFi Stadium or SoFi office exterior. "
            "Modern fintech company headquarters. "
            "Clean, corporate, professional photography. "
            "Photo-realistic, shallow depth of field, professional lighting. "
            "No AI art, no neon, no abstract. "
            "No model numbers, no serial numbers, no text labels, no markings — only the company logo if visible. "
            "Clear blue sky, sharp focus, high detail."
        ),
    },
    {
        "slug": "rddt-ai-data-licensing-moat-2026",
        "prompt": (
            "Professional stock photograph of the Reddit headquarters building exterior in "
            "San Francisco. The Reddit logo visible on the building sign or entrance. Modern "
            "tech office architecture with glass facade, clear blue sky, professional "
            "real-estate photography style. Shallow depth of field, professional lighting, "
            "photorealistic, 8K resolution, sharp focus, high detail."
        ),
    },
]

W, H = 1200, 675
OUTDIR = "/home/chino/thesignal/public/img/articles"

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    import fal_client

    for art in ARTICLES:
        slug = art["slug"]
        prompt = art["prompt"]
        output_path = os.path.join(OUTDIR, f"{slug}.jpg")

        print(f"\n{'='*60}")
        print(f"Generating image for: {slug}")
        print(f"{'='*60}")

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
            print(f"ERROR: Could not find image URL for {slug}")
            print(f"Result: {result}")
            continue

        print(f"Downloading from: {image_url}")
        r = requests.get(image_url, timeout=120)
        r.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(r.content)

        img = Image.open(output_path)
        print(f"Saved: {output_path}")
        print(f"  Size: {os.path.getsize(output_path)} bytes")
        print(f"  Dimensions: {img.size}")

        if img.size != (W, H):
            print(f"  Resizing to ({W}, {H})...")
            img = img.resize((W, H), Image.LANCZOS)
            img.save(output_path, "JPEG", quality=92, optimize=True)

        if os.path.getsize(output_path) < 10240:
            img.save(output_path, "JPEG", quality=98, optimize=True)

        print(f"  Final size: {os.path.getsize(output_path)} bytes")
        print(f"  Done!")

    print(f"\n{'='*60}")
    print(f"All 5 images generated successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
