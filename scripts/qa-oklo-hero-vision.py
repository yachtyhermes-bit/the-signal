#!/usr/bin/env python3
"""Combined hero QA via fal any-llm/vision: text, people, photorealism, traps, framing.

Usage: python3 scripts/qa-oklo-hero-vision.py <image.jpg> [...]
"""
import base64
import os
import sys

Q = (
    "You are a strict QA inspector for a financial news site hero image.\n"
    "Answer in EXACTLY five lines, no preamble:\n"
    "TEXT: YES or NO, then list every legible or garbled letter, word, number, digit, tick "
    "mark, logo, brand name or watermark anywhere in the frame (say NONE if none).\n"
    "PEOPLE: YES or NO, then list any person, face, hand, finger, arm or body part visible "
    "in the frame (say NONE if none).\n"
    "PHOTOREAL: YES or NO - does this look like a genuine photograph taken with a real "
    "camera (as opposed to an illustration, 3D render, digital art or AI art look)?\n"
    "TRAPS: list any of these present, else NONE - data-centre or server-room or aisle "
    "scene, neon, glowing lines, geometric patterns, abstract art, cartoon or illustration, "
    "watermark, text.\n"
    "SCENE: one precise sentence describing every object in the scene and the framing."
)


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def main():
    import fal_client
    load_fal_key()
    for img in sys.argv[1:]:
        with open(img, "rb") as f:
            url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        out = fal_client.subscribe(
            "fal-ai/any-llm/vision",
            arguments={"prompt": Q, "image_url": url, "model": "google/gemini-flash-1.5"},
        )
        print(f"=== {img} ===")
        print(str(out.get("output", out)).strip())
        print()


if __name__ == "__main__":
    main()
