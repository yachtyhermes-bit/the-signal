#!/usr/bin/env python3
"""Quick vision QA for a hero image (fal any-llm/vision, gemini-flash)."""
import base64, os, sys
import fal_client

IMG = sys.argv[1]
for line in open("/home/chino/hermes-workspace/studio-api/.env"):
    if line.startswith("FAL_KEY="):
        os.environ["FAL_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")

url = "data:image/jpeg;base64," + base64.b64encode(open(IMG, "rb").read()).decode()
Q = (
    "Grade this news-site hero image strictly, 5 short labelled lines:\n"
    "1 REALISM: real DSLR editorial photograph, or CGI/3D render/digital art? Say which and why.\n"
    "2 SCENE: what objects and materials are in frame.\n"
    "3 WAFER: is a silicon wafer clearly visible? are individual rectangular dies and the circuit grid sharp? is iridescent thin-film colour present?\n"
    "4 LIGHT: dominant colour cast, and is there warm amber rim light alongside cool white?\n"
    "5 PROBLEMS: check specifically for (a) any letter/digit/word/logo/emblem/watermark anywhere, (b) data-center or server-rack look, (c) neon/glow/light-trails/geometric-pattern art, (d) hand/finger anatomy errors, (e) overall verdict PASS or FAIL for a photo-realistic editorial hero."
)
out = fal_client.subscribe(
    "fal-ai/any-llm/vision",
    arguments={"prompt": Q, "image_url": url, "model": "google/gemini-flash-1.5"},
)
print(str(out.get("output", out)).strip())
