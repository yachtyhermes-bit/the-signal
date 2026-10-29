#!/usr/bin/env python3
"""Cross-model QC on hero candidates via fal any-llm/vision."""
import base64
import json
import sys

import fal_client

sys.path.insert(0, "/home/chino/thesignal/scripts")
from gen_avav_key import load_key  # noqa: E402

load_key()

model = sys.argv[1]
img_path = sys.argv[2]
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

question = (
    "You are a photo editor judging this image as a news-article hero banner. "
    "Be precise and literal. Answer each line briefly:\n"
    "1. PHOTO or RENDER? (would a picture editor believe this was shot on a "
    "real camera?)\n"
    "2. TEXT: list every piece of visible lettering, numeral, logo, brand name "
    "or watermark you can actually read or half-read. Write 'none' if truly none.\n"
    "3. Is any part of the image a data center, server room, server rack or "
    "cable aisle? yes/no\n"
    "4. Foreground subject, background, and is the frame full of subject?\n"
    "5. Human figures present? Are faces hidden or out of focus?\n"
    "6. Rendering defects? (melted or impossible machinery, extra limbs, "
    "duplicated objects, nonsense shapes, fake text-like squiggles)\n"
    "7. Would this work as a hero image for an article about laser weapons and "
    "counter-drone air defence? USABLE or REJECT + one sentence."
)

try:
    result = fal_client.subscribe(
        "fal-ai/any-llm/vision",
        arguments={
            "model": model,
            "prompt": question,
            "image_url": "data:image/jpeg;base64," + b64,
        },
    )
    print(f"--- {model} :: {img_path}")
    print(result.get("output", json.dumps(result)))
except Exception as e:
    print(f"--- {model} :: {img_path}")
    print("ERR:", type(e).__name__, str(e)[:400])
