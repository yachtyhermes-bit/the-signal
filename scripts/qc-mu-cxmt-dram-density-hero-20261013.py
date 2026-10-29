#!/usr/bin/env python3
"""One-off targeted QA: orientation of the technician + wafer sheen."""
import base64
import json
import sys

import requests

IMG = sys.argv[1]
key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")

b64 = base64.b64encode(open(IMG, "rb").read()).decode()
PROMPT = """Strict literal QA on this hero photo. Answer only what is visible:
A) ORIENTATION: Is the person shown FROM BEHIND / three-quarter back (back of hood and suit toward camera, no face or face-shield visible), or are we seeing their FRONT (face, eyes, mask front, or front of hood toward camera)? One or two sentences.
B) WAFER: Describe the round object they hold - is it a polished mirror-like silicon disc/wafer? Does it show a rainbow / prismatic diffraction sheen or iridescent colour band anywhere on its surface? YES/NO + brief.
C) Hands: is it held with BOTH gloved hands? YES/NO.
D) Any signage, screen, monitor, printed label, letter, number, logo or watermark anywhere? YES/NO (quote if yes).
E) Does the background read as a wafer-fab cleanroom interior with equipment/piping, or as a data-center server aisle/racks? Which?
F) Overall: does this look like a real editorial stock photograph, or a CGI/render/digital art? Why in one sentence.
"""
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
        "max_tokens": 900,
    },
    timeout=180,
)
d = r.json()
if "error" in d:
    print("ERROR:", json.dumps(d["error"])[:500])
    sys.exit(1)
print(d["choices"][0]["message"]["content"])
