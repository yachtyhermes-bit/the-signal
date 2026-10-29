#!/usr/bin/env python3
"""Composition QC for a generated hero — does it read editorially, any tells?"""
import base64
import json
import os
import sys

import requests

IMG = sys.argv[1]
key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    print("ERROR: no OPENROUTER_API_KEY")
    sys.exit(1)

b64 = base64.b64encode(open(IMG, "rb").read()).decode()

PROMPT = """You are a photo editor at a financial news site reviewing a hero image for an article about an enterprise software company whose earnings beat guidance but whose stock crashed 26% in one day. The intended mood: a company whose quarter went sideways — quiet, deflated, human, documentary.

Answer literally and honestly, numbered:

1) FIRST IMPRESSION: What does this image communicate to a reader at a glance? Does it read as a real editorial photograph of a modern software company having a bad moment, or as generic corporate stock? Be blunt.

2) COMPOSITION: Is the framing clean or cluttered? Is there a clear focal point? Name anything that looks accidental, floating, duplicated, or like a compositing error (objects on tables, limbs, furniture).

3) ANATOMY: Any malformed hands, fingers, faces, ears, necks, or body proportions? Any duplicated or merged limbs? YES/NO + where.

4) TEXT: Any letters, numerals, logos, screen content, book/graphic printing, signage, or letter-like marks anywhere — including small, blurred or garbled? YES/NO + where and what.

5) RENDER TELLS: Any plastic sheen, over-smooth skin, impossible lighting, hyper-saturated colour, glowing edges, or CGI feel? PHOTOGRAPH-LIKE or RENDER-LIKE + why.

6) NEGATIVES PRESENT: data center / server racks / neon / glowing lines / geometric patterns / abstract art? YES/NO + what.

7) VERDICT: SHIP or REJECT, and if REJECT, the single biggest reason."""

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://readthesignal.net",
        "X-Title": "The Signal Hero QC",
    },
    json={
        "model": "google/gemini-2.5-flash",
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
        ]}],
        "max_tokens": 1200,
    },
    timeout=180,
)
d = r.json()
if "error" in d:
    print("ERROR:", json.dumps(d["error"])[:500])
    sys.exit(1)
print(d["choices"][0]["message"]["content"])
