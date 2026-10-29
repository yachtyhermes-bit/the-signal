#!/usr/bin/env python3
"""Side-by-side judge: pick the better hero for mu-cxmt-dram-density-race-2026."""
import base64
import json
import sys

import requests

key = None
for line in open("/home/chino/.hermes/.env"):
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"').strip("'")

imgs = sys.argv[1:]
content = [
    {
        "type": "text",
        "text": (
            "These are two candidate hero photos for a financial news article about "
            "Micron Technology and DRAM memory-chip density. The brief REQUIRED: "
            "(1) a photo-realistic editorial stock PHOTOGRAPH (not CGI/render) inside a "
            "semiconductor wafer-fab CLEANROOM; (2) a technician in a white bunny suit, hood "
            "and mask, FACE NOT IDENTIFIABLE, seen FROM BEHIND or three-quarter back, holding "
            "up a large polished 300mm silicon wafer with BOTH gloved hands; (3) the wafer's "
            "mirror surface reflecting pale cleanroom light with a faint diffraction rainbow "
            "sheen; (4) cool white/blue lighting, a hint of amber in the far background, "
            "rows of process equipment/piping softly out of focus; (5) shallow depth of field "
            "on the wafer and gloves; (6) absolutely TEXT-FREE; (7) must NOT look like a "
            "data-center server aisle, must NOT be abstract/digital art/neon/CGI.\n\n"
            "Image A is the first attachment, Image B is the second. For EACH of the 7 "
            "requirements give a 0/1 verdict for A and for B, then give a TOTAL score out of 7 "
            "for each and name the WINNER plus one line of reasoning. Be strict and literal."
        ),
    }
]
for p in imgs:
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}})

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
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1200,
    },
    timeout=180,
)
d = r.json()
if "error" in d:
    print("ERROR:", json.dumps(d["error"])[:500])
    sys.exit(1)
print(d["choices"][0]["message"]["content"])
