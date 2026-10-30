#!/usr/bin/env python3
"""Tailored vision QA for a trading-desk hero: checks text, faces, banned tropes.

Usage: python3 qa-coin-binance-hero-vision.py <image.jpg>
"""
import base64
import os
import sys

IMG = sys.argv[1]

Q = (
    "You are a strict photo editor inspecting a news-site hero image. Answer in "
    "EXACTLY these lines, no preamble:\n"
    "TEXT: YES or NO, then list every legible OR garbled letter, word, number, "
    "digit, ticker, price, axis label, logo, brand mark or watermark anywhere in frame (NONE if none).\n"
    "FACES: YES or NO, then say whether any person's full face is identifiable (NONE if no face).\n"
    "BANNED: YES or NO, then list any of these present: server racks / data-center aisle, neon or "
    "synthwave colours, glowing geometric lines, abstract digital art, 3D-render/CGI look, bitcoin logo, "
    "crypto coin icons.\n"
    "PHOTO: YES or NO, then say whether it reads as a real photograph (lens blur, grain, real light) "
    "rather than an illustration or render.\n"
    "SCENE: two sentences describing exactly what is in the frame, the light, and the mood."
)


def load_fal_key():
    for env_path in ("/home/chino/hermes-workspace/studio-api/.env",):
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("FAL_KEY="):
                        os.environ["FAL_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
                        return os.environ["FAL_KEY"]
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
    print(str(out.get("output", out)).strip())


if __name__ == "__main__":
    main()
