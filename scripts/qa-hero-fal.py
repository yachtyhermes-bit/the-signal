#!/usr/bin/env python3
"""Strict vision QA for a hero image via fal any-llm/vision (no OpenRouter key needed).

Usage: python3 qa-hero-fal.py <image.jpg>
Prints TEXT / PEOPLE / SCENE verdict lines and exits 1 if TEXT or PEOPLE is YES.
"""
import base64
import os
import sys

IMG = sys.argv[1]

Q = (
    "You are a strict QA inspector for a financial news site hero image.\n"
    "Answer in EXACTLY three lines, no preamble:\n"
    "TEXT: YES or NO, then list every legible OR garbled letter, word, number, digit, tick mark, "
    "graduation, logo, brand name or watermark you can see anywhere in the frame (say NONE if none).\n"
    "PEOPLE: YES or NO, then list any person, face, hand, finger, arm, silhouette, statue of a human "
    "or body part visible in the frame (say NONE if none).\n"
    "SCENE: one precise sentence describing every object in the scene and the dominant materials."
)


def load_fal_key():
    for env_path in ("/home/chino/hermes-workspace/studio-api/.env",):
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
    with open(IMG, "rb") as f:
        url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    out = fal_client.subscribe(
        "fal-ai/any-llm/vision",
        arguments={"prompt": Q, "image_url": url, "model": "google/gemini-flash-1.5"},
    )
    text = str(out.get("output", out)).strip()
    print(text)

    up = text.upper()
    text_line = up.split("PEOPLE:")[0]
    people_line = up.split("PEOPLE:")[1].split("SCENE:")[0] if "PEOPLE:" in up else ""
    bad = text_line.startswith("TEXT: YES") or people_line.strip().startswith("YES")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
