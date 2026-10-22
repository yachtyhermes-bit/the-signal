#!/usr/bin/env python3
"""Vision QA for vertiv-ai-factory-power-slide-2026 hero."""
import base64
import json

import requests

IMG = "/home/chino/thesignal/public/img/articles/vertiv-ai-factory-power-slide-2026.jpg"

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
assert key, "no OPENROUTER_API_KEY"

b64 = base64.b64encode(open(IMG, "rb").read()).decode()
ASK = (
    "Look at this image carefully and answer literally. Do not invent.\n"
    "A) What is the scene? Name every major object and colour: ...\n"
    "B) Is this INSIDE an industrial chiller plant / mechanical plant room "
    "with large chillers, insulated coolant piping, pumps and valves? "
    "YES/NO, with evidence: ...\n"
    "C) Is it a data-center hallway, server aisle, or rack row? YES/NO: ...\n"
    "D) Is there a human being, and is a person visible doing industrial work "
    "(PPE, hard hat, valve/handwheel)? YES/NO + describe: ...\n"
    "E) Any readable text, letters, numbers, logos, labels or signage anywhere? "
    "YES/NO; quote exactly if yes: ...\n"
    "F) Real photograph or CGI/3D render/AI digital art? one of PHOTOGRAPH / "
    "RENDER, with one sentence why: ...\n"
    "G) Any neon, glowing lines, geometric patterns, hud overlays? YES/NO: ...\n"
    "H) Does it look like professional stock photography suitable as a "
    "finance-news article hero image? YES/NO + why: ...\n"
)

for model in ("google/gemini-4-argon", "mistralai/mistral-large-4-0"):
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
            "max_tokens": 900,
        },
        timeout=180,
    )
    d = r.json()
    print(f"\n===== {model} =====")
    if "error" in d:
        print("ERROR:", json.dumps(d["error"])[:300])
    else:
        print(d["choices"][0]["message"]["content"])
