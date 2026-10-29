#!/usr/bin/env python3
"""Custom vision QA for the HII shipyard hero: confirms shipyard/submarine
scene, no text, no data-center drift. Usage: qa-hii-hero.py <image.jpg>"""
import base64
import os
import sys

IMG = sys.argv[1]

Q = (
    "You are a strict photo editor for a financial news site. Look at this image and answer in "
    "EXACTLY four lines, no preamble:\n"
    "SCENE: one precise sentence listing what is physically in the frame and the dominant materials.\n"
    "SHIPYARD: YES or NO -- is this unmistakably a shipyard / shipbuilding hall with a large steel "
    "ship or submarine hull section under construction, gantry cranes and workers in hard hats? "
    "Then say what specifically makes it readable as that.\n"
    "TEXT: YES or NO, then list every legible OR garbled letter, word, number, digit, logo, brand, "
    "sign or watermark anywhere (say NONE if none).\n"
    "DRIFT: YES or NO -- does it look like a data center, server room, rack aisle, office, or "
    "abstract/digital/neon/CGI art instead of a real photograph? Then rate photo-realism 1-10.\n"
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
    print(str(out.get("output", out)).strip())


if __name__ == "__main__":
    main()
