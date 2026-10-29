#!/usr/bin/env python3
"""Second-opinion vision inspection for the TSLA Optimus hero.

Asks specifically whether the frame reads as a HUMANOID ROBOT on a factory /
assembly floor (vs. a prosthetic limb, a medical device, a product shot), and
whether it is a real photograph.

Usage: python3 inspect-optimus-hero.py <image.jpg>
"""
import base64
import json
import sys

import requests

KEY_PATH = "/home/chino/video_output/.gemini_key"
MODELS = ["gemini-2.5-pro", "gemini-2.5-flash"]

PROMPT = """You are an image-quality inspector for a photo-realistic financial
news site. A hero image must clearly read to a casual viewer as A HUMANOID
ROBOT ON A FACTORY / ASSEMBLY FLOOR (robotics manufacturing). Answer in EXACTLY
this format, nothing else:

TEXT: <YES or NO> — <the exact text you can read, or "no legible text">
TYPE: <"photo" or "render/illustration/CGI">
SUBJECT: <one sentence: what the picture actually shows>
HUMANOID_ROBOT: <YES or NO> — does it clearly read as a humanoid robot, and not
  as a prosthetic limb, medical device, mannequin, toy or generic product shot?>
FACTORY_FLOOR: <YES or NO> — is there any clear factory / assembly-line context
  (industrial hall, car bodies, pressings, workers, line equipment)?>
FIRST_READ: <the single most likely interpretation of the image by a viewer who
  sees it for one second, in five words or fewer>
LOGO: <YES or NO> — any brand logo, company name, trademark or watermark?>
REALISM: <one sentence on whether it reads as an authentic editorial press
  photograph rather than a CGI render or digital illustration>
CGI_CLUES: <list the specific visual details that make it look computer
  generated, or "none">"""


def load_key():
    with open(KEY_PATH) as f:
        return f.read().strip()


def inspect(path):
    key = load_key()
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    out = []
    for model in MODELS:
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
                "maxOutputTokens": 3000,
            },
        }
        if "flash" in model:
            payload["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent"
        )
        r = requests.post(
            url,
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=180,
        )
        if r.status_code == 200:
            j = r.json()
            try:
                txt = j["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception:  # noqa: BLE001
                txt = "PARSE ERROR " + json.dumps(j)[:300]
        else:
            txt = f"HTTP {r.status_code}: {r.text[:200]}"
        out.append(f"----- {model} -----\n{txt}")
    return "\n".join(out)


if __name__ == "__main__":
    print(inspect(sys.argv[1]))
