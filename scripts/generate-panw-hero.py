#!/usr/bin/env python3
"""Generate a Palo Alto Networks (PANW) hero image using FAL flux/schnell."""
import os
import sys
import requests

OUTPUT = "/home/chino/thesignal/public/img/articles/panw-ai-security-supercycle-2026.jpg"
SLUG = "panw-ai-security-supercycle-2026"
W, H = 1200, 675

PROMPT = (
    "Professional stock photograph of a modern cybersecurity operations center "
    "(SOC) during a busy workday. In the foreground, security analysts sit at "
    "rows of desks with large multi-monitor setups showing network security "
    "dashboards and world map threat displays, one analyst pointing at a screen. "
    "In the softly blurred background, tall rows of server racks with small "
    "blinking status lights and neatly organized cables. Clean office lighting, "
    "natural realistic colors, shallow depth of field focused on the analysts, "
    "professional corporate photography, sharp focus, high detail. "
    "Ultra-realistic photo, no abstract art, no digital art, no neon/synthwave, "
    "no glowing lines, no geometric patterns, no text, no logos, no watermark."
)

def main():
    import fal_client

    # Set FAL_KEY from the studio-api env file
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    break

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    print(f"Generating image with FAL flux/schnell...")
    print(f"Prompt: {PROMPT[:80]}...")

    # Use the subscribe method which blocks until complete
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": PROMPT,
            "image_size": {
                "width": W,
                "height": H
            },
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )

    print(f"Result keys: {list(result.keys())}")

    # Extract the image URL
    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]

    if not image_url:
        print(f"ERROR: Could not find image URL in result")
        print(f"Full result: {result}")
        sys.exit(1)

    print(f"Image URL: {image_url}")

    # Download the image
    print(f"Downloading image...")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()

    # Save to output path
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(r.content)

    file_size = os.path.getsize(OUTPUT)
    print(f"Saved to {OUTPUT}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")

    # Verify dimensions
    from PIL import Image
    img = Image.open(OUTPUT)
    print(f"   Dimensions: {img.size}")

    if img.size != (W, H):
        print(f"Resizing from {img.size} to ({W}, {H})...")
        img = img.resize((W, H), Image.LANCZOS)
        img.save(OUTPUT, "JPEG", quality=92, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")
        print(f"   New dimensions: {img.size}")

    if file_size < 10240:
        print(f"File too small ({file_size} bytes), re-saving with higher quality...")
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        file_size = os.path.getsize(OUTPUT)
        print(f"   New size: {file_size} bytes ({file_size/1024:.1f} KB)")

    print(f"All checks passed!")


if __name__ == "__main__":
    main()
