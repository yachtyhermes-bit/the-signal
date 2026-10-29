#!/usr/bin/env python3
"""Neutral second-opinion QA from a different model family (independent of the
gemini read used earlier, which is inconsistent pass-to-pass)."""
import base64
import sys

import requests

IMG = sys.argv[1]
MODEL = sys.argv[2] if len(sys.argv) > 2 else "openai/gpt-4o-mini"

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")

b64 = base64.b64encode(open(IMG, "rb").read()).decode()

P = """Describe this image factually, then answer. Be literal; do not invent.
1) VISIBLE: one paragraph on exactly what is in the frame (objects, materials, surface, light, angle).
2) PEOPLE: any person, hand, arm, finger, or body part anywhere, including edges? YES/NO.
3) TEXT: any letter, word, number, digit, logo, sign, label, plate, or marking that reads as writing (even garbled)? YES/NO + where.
4) GLITCH: any impossible geometry, floating object, duplicated fragment, or obvious AI artefact? YES/NO + where.
5) READ: does it read as US physical infrastructure / heavy engineering? YES/NO + why.
6) QUALITY: 1-10 for editorial magazine use, one line why."""

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://readthesignal.net",
        "X-Title": "PAVE second-opinion QA",
    },
    json={
        "model": MODEL,
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
        "max_tokens": 800,
    },
    timeout=180,
).json()
print(r.get("error") or r["choices"][0]["message"]["content"])
