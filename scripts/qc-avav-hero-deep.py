#!/usr/bin/env python3
"""Deeper QC on a hero candidate via fal any-llm/vision."""
import base64
import json
import sys

import fal_client

sys.path.insert(0, "/home/chino/thesignal/scripts")
from gen_avav_key import load_key  # noqa: E402

load_key()

img_path = sys.argv[1]
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

question = (
    "You are a photo editor judging this image as a news-article hero banner. "
    "Answer each line briefly:\n"
    "1. Does this look like a real photograph taken on a camera, or a computer render?\n"
    "2. List every piece of visible text, lettering, numeral, logo or watermark. Say "
    "'none' if there is truly none.\n"
    "3. Is any part of the image a data center, server room, server rack, or cable aisle?\n"
    "4. Describe the composition: what is sharp in the foreground, what is in the "
    "background, and is the frame roughly full of subject rather than empty sky?\n"
    "5. Are human figures present, and are their faces hidden or out of focus?\n"
    "6. Are there obvious rendering defects (melted or impossible machinery, extra "
    "limbs, duplicated objects, nonsense shapes)?\n"
    "7. Is the lighting natural and the colours plausible for the time of day?\n"
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
