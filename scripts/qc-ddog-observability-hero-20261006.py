#!/usr/bin/env python3
"""QC a hero image via fal any-llm/vision (gemini). Usage: python3 qc-ddog-hero.py <img>"""
import base64
import json
import os
import sys

import fal_client


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith("FAL_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                os.environ["FAL_KEY"] = key
                return key
    return os.environ.get("FAL_KEY")


load_fal_key()
img_path = sys.argv[1]
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

question = (
    "You are a photo editor judging this image as a news-article hero banner. "
    "Answer each line briefly:\n"
    "1. Does this look like a real photograph taken on a camera, or a computer "
    "render/illustration/CGI?\n"
    "2. List every piece of visible text, lettering, numeral, logo or watermark. "
    "Say 'none' if there is truly none.\n"
    "3. Is any part of the image a data center, server room, server rack, or cable "
    "aisle? (yes/no)\n"
    "4. Describe the setting and composition: what is sharp in the foreground, what "
    "is in the background?\n"
    "5. Are human figures present, and are their faces hidden or out of focus?\n"
    "6. Are there obvious rendering defects (melted/impossible objects, extra limbs, "
    "duplicated items, nonsense shapes)?\n"
    "7. Is the lighting natural and plausible?\n"
    "8. FINAL: USABLE or REJECT, and one sentence why."
)

result = fal_client.subscribe(
    "fal-ai/any-llm/vision",
    arguments={
        "model": "google/gemini-flash-1.5",
        "prompt": question,
        "image_url": "data:image/jpeg;base64," + b64,
    },
)
print(result.get("output", json.dumps(result))[:4000])
