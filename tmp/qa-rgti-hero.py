#!/usr/bin/env python3
"""Ad-hoc vision QA for a hero image via OpenRouter gemini-2.5-flash."""
import base64
import json
import os
import sys

import requests

IMG = sys.argv[1] if len(sys.argv) > 1 else (
    "/home/chino/thesignal/public/img/articles/"
    "rgti-quantum-shakeout-government-backstop-2026.jpg"
)

key = os.environ.get("OPENROUTER_API_KEY")
if not key:
    for p in ("/home/chino/.hermes/.env", "/home/chino/thesignal/.dev.vars"):
        if os.path.exists(p):
            for line in open(p):
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                    break
        if key:
            break

if not key:
    print("ERROR: no OPENROUTER_API_KEY")
    sys.exit(1)

b64 = base64.b64encode(open(IMG, "rb").read()).decode()

Q = """You are a photo editor for a financial news site. Answer concisely:
1) Does this look like a REAL photograph (DSLR) or CGI/render/digital art?
2) What is the main subject? Is it a quantum computing dilution refrigerator (gold chandelier cryostat with stacked gold circular plates and dense silver coax cables)? Or a quantum processor chip? Or something else? A server room / data center aisle is BAD.
3) Is there ANY visible text, lettering, logo, watermark, signage or garbled characters anywhere? Say where.
4) Any obviously broken anatomy, malformed objects, or nonsense hardware?
5) Is it roughly 16:9 landscape with a clean composition suitable as a hero image?
6) Verdict: SHIP or REDO, one line why."""

payload = {
    "model": "google/gemini-2.5-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": Q},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
            ],
        }
    ],
}

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
print("HTTP", r.status_code)
try:
    print(r.json()["choices"][0]["message"]["content"])
except Exception:
    print(r.text[:1200])
