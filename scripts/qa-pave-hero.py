#!/usr/bin/env python3
"""Hostile-editor QA for hero candidates (single OpenRouter vision call)."""
import base64
import sys

import requests

IMG = sys.argv[1]

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")

b64 = base64.b64encode(open(IMG, "rb").read()).decode()

P = """You are a hostile photo editor at a financial news site. Inspect this image and answer ONLY with short lines:
A) What exactly is in frame? One factual paragraph, objects + materials + surface + light direction + camera angle. No guessing.
B) Is this readable as a physical-infrastructure / engineering still life (bridge, concrete, steel, surveying)? YES/NO + one line why.
C) Any letters, words, numerals, stamps, embossing, moulded marks, tick marks or faint engraving on ANY surface? YES/NO + where exactly.
D) Any person, hand, arm, finger or partial body part at any edge? YES/NO.
E) Any object that looks like a tool, pen, pencil, cup, plant, or random clutter? YES/NO + what.
F) Composition problems a picture editor would reject (dead space, cropped sliver at edge, blown highlights, awkward crop, tilt)? One line.
G) Editorial magazine quality score 1-10 + one-line justification.
H) One-sentence factual caption, then one-sentence alt text listing EXACTLY what is visible."""

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://readthesignal.net",
        "X-Title": "PAVE hero QA",
    },
    json={
        "model": "google/gemini-2.5-flash",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": P},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64," + b64},
                    },
                ],
            }
        ],
        "max_tokens": 900,
    },
    timeout=180,
).json()
print(r.get("error") or r["choices"][0]["message"]["content"])
