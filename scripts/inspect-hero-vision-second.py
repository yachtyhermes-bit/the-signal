#!/usr/bin/env python3
"""Second-opinion QA + quadrant OCR prep for the chosen hero."""
import base64
import json
import os
import subprocess
import sys

import requests
from PIL import Image

IMG = "/home/chino/thesignal/public/img/articles/etf-review-shld-2026-09-30.jpg"
im = Image.open(IMG)
print("PIL:", im.size, im.mode, os.path.getsize(IMG), "bytes")

# quadrant crops -> OCR each (catches small text OCR misses at full size)
w, h = im.size
boxes = {
    "TL": (0, 0, w // 2, h // 2),
    "TR": (w // 2, 0, w, h // 2),
    "BL": (0, h // 2, w // 2, h),
    "BR": (w // 2, h // 2, w, h),
}
for name, box in boxes.items():
    p = f"/tmp/q_{name}.png"
    im.crop(box).resize((w, h), Image.LANCZOS).save(p)
    for psm in ("6", "11"):
        out = subprocess.run(
            ["tesseract", p, "-", "--psm", psm], capture_output=True, text=True
        ).stdout.strip()
        print(f"OCR {name} psm{psm}: {'<<EMPTY>>' if not out else repr(out[:200])}")

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
assert key, "no OPENROUTER_API_KEY"

b64 = base64.b64encode(open(IMG, "rb").read()).decode()
ASK = (
    "Answer each with the short format given. Be literal; do not invent.\n"
    "A) List every object you can see and its colour/material: ...\n"
    "B) Any human being or body part anywhere (face, hand, arm, finger, "
    "edge of a hand)? YES/NO plus location: ...\n"
    "C) Any text, letters, numbers, digits, tick marks, graduations, logos, "
    "brand marks, labels, tags, barcodes or letter-like marks ANYWHERE, "
    "readable or garbled? YES/NO; if YES quote it exactly: ...\n"
    "D) Any printed/woven pattern or letter-like marks on cloth or paper? "
    "YES/NO: ...\n"
    "E) Any military insignia, weapon, ammunition, flag, camouflage, "
    "uniform, drone or military vehicle? YES/NO: ...\n"
    "F) Real photograph or CGI/3D render/AI digital art? one of "
    "PHOTOGRAPH / RENDER, with one sentence why: ...\n"
    "G) Camera angle (top-down overhead / eye-level side view / low angle): ...\n"
)

for model in ("openai/gpt-4o-mini", "anthropic/claude-3.5-haiku"):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://readthesignal.net",
            "X-Title": "The Signal Hero QA",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ASK},
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64," + b64},
                        },
                    ],
                }
            ],
            "max_tokens": 800,
        },
        timeout=180,
    )
    d = r.json()
    print(f"\n===== {model} =====")
    if "error" in d:
        print("ERROR:", json.dumps(d["error"])[:300])
    else:
        print(d["choices"][0]["message"]["content"])
