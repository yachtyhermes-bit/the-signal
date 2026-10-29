#!/usr/bin/env python3
"""Vision inspection of the generated hero: describe it, hunt for text/people/render tells."""
import base64
import json
import os
import sys

import requests

IMG = sys.argv[1] if len(sys.argv) > 1 else "/home/chino/thesignal/public/img/articles/etf-review-shld-2026-09-30.jpg"

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    print("ERROR: no OPENROUTER_API_KEY")
    sys.exit(1)

b64 = base64.b64encode(open(IMG, "rb").read()).decode()

PROMPT = """You are a strict image QA inspector for a financial news site. Look at this hero image very carefully and answer these questions honestly and literally, based ONLY on what is actually visible:

1) SCENE: Describe exactly what objects are visible, their materials and colours, the surface they sit on, the lighting direction and quality, and the camera angle/distance. One paragraph, plain factual description. Do not guess at anything not visible.
2) PEOPLE: Is there any person, face, hand, arm, finger, or any body part, anywhere in frame including the edges? Answer YES or NO and say where.
3) TEXT: Is there any text, letter, word, number, digit, percentage, currency symbol, ticker, logo, brand name, watermark, barcode, label, tag, ruler graduation/measurement mark, or any letter-like or typography-like marking ANYWHERE (readable or garbled)? Answer YES or NO. If YES, quote exactly what you can read.
4) PRINT/PATTERN: Do any cloth or paper surfaces show printed, woven-in, or letter-like patterns/marks? YES or NO.
5) MILITARY: Any insignia, weapons, ammunition, flags, camouflage, uniforms, drones, vehicles, or military hardware? YES or NO (say what if yes).
6) RENDER TELLS: Does it look like a real photograph (natural noise, honest exposure, real lens blur) or like a CGI/3D render / glossy digital illustration / AI art with plastic sheen? Answer PHOTOGRAPH-LIKE or RENDER-LIKE and say why.
7) OBJECT INVENTORY: List every distinct object in the frame as a numbered list.

Format your reply with the numbered headings 1-7 and nothing else."""

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://readthesignal.net",
        "X-Title": "The Signal Hero QA",
    },
    json={
        "model": "google/gemini-2.5-flash",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
                ],
            }
        ],
        "max_tokens": 1400,
    },
    timeout=180,
)
d = r.json()
if "error" in d:
    print("ERROR:", json.dumps(d["error"])[:500])
    sys.exit(1)
print(d["choices"][0]["message"]["content"])
