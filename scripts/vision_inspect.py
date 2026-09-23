#!/usr/bin/env python3
"""Ad-hoc vision inspection of a generated hero image using the Gemini API key
found at /home/chino/video_output/.gemini_key.

Reports: (a) any legible text/lettering, (b) whether the composition is a
photo-realistic press photograph of the intended subject, (c) whether it drifts
into any banned composition (server room / data-center aisle / substation).

Usage: python3 vision_inspect.py <image.jpg>
"""
import base64
import json
import sys

import requests

KEY_PATH = "/home/chino/video_output/.gemini_key"
MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]

PROMPT = """You are an image-quality inspector for a photo-realistic news site.
Look at this image and answer in EXACTLY this format, nothing else:

TEXT: <YES or NO> — <either the exact text you can read, or "no legible text">
TYPE: <"photo" if it looks like a real camera photograph, or "render/illustration/CGI">
SUBJECT: <one sentence describing what the picture actually shows>
SERVER_ROOM: <YES or NO> — is this a server room, server aisle, data-center hallway, GPU rack or cable-run interior?
LOGO: <YES or NO> — any brand logo, company name, trademark or watermark visible?
REALISM: <one sentence on whether it reads as an authentic editorial press photograph>"""


def load_key():
    with open(KEY_PATH) as f:
        return f.read().strip()


def inspect(path):
    key = load_key()
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 800,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    last = None
    for model in MODELS:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent"
        )
        r = requests.post(
            url, headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            data=json.dumps(payload), timeout=120,
        )
        if r.status_code == 200:
            j = r.json()
            try:
                return model, j["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception as e:  # noqa: BLE001
                return model, f"PARSE ERROR {e}: {json.dumps(j)[:300]}"
        last = f"{model} -> HTTP {r.status_code}: {r.text[:200]}"
        print(f"  [warn] {last}")
    return None, last


if __name__ == "__main__":
    model, out = inspect(sys.argv[1])
    print(f"MODEL={model}")
    print(out)
