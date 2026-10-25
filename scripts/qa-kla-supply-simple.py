#!/usr/bin/env python3
"""Simple, robust two-question vision check (no rigid format).

Usage: python3 qa-kla-supply-simple.py <image.jpg>
"""
import base64
import os
import sys

IMG = sys.argv[1]

PROMPTS = [
    "Describe this photograph in 4 sentences. Say what room it is, what the "
    "large machines are, what the person is doing, and what colour the "
    "lighting is.",
    "Look very carefully at every surface in this image. Is there any text, "
    "letter, number, logo, brand name, sign, label, or readable screen "
    "content anywhere, even small or blurry? Answer with one of: "
    "'NO TEXT ANYWHERE' or 'TEXT FOUND: <quote it and say where>'. Then, on "
    "a new line, answer 'DATA CENTER: YES' or 'DATA CENTER: NO' depending on "
    "whether this shows a server room or rack aisle.",
]


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
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(2)
    with open(IMG, "rb") as f:
        url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    for i, p in enumerate(PROMPTS, 1):
        out = fal_client.subscribe(
            "fal-ai/any-llm/vision",
            arguments={"prompt": p, "image_url": url, "model": "google/gemini-flash-1.5"},
        )
        print(f"--- Q{i} ---")
        print(str(out.get("output", out)).strip())


if __name__ == "__main__":
    main()
