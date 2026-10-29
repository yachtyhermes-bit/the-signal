#!/usr/bin/env bash
# Helper: run tesseract + OpenRouter vision text/scene check on a hero image.
# Usage: scripts/vcheck-hero.sh <image-path>
set -euo pipefail
IMG="${1:?usage: vcheck-hero.sh <image-path>}"
echo "=== tesseract OCR (stdout) ==="
tesseract "$IMG" stdout 2>/dev/null | tr -s '\n' | tr -d '\n' ; echo ""
echo "=== OpenRouter vision ==="
KEY=$(grep -E "^OPENROUTER_API_KEY=sk-or" /home/chino/.hermes/.env | head -1 | cut -d= -f2- | tr -d '"'"'"' ')
KEY="$KEY" IMG="$IMG" /home/chino/video-venv/bin/python3 - <<'PY'
import os, json, base64, urllib.request
key = os.environ["KEY"]; img = os.environ["IMG"]
b64 = base64.b64encode(open(img,"rb").read()).decode()
payload = json.dumps({
  "model": "google/gemini-2.5-flash",
  "messages": [{"role":"user","content":[
    {"type":"text","text":"Inspect this image and answer in 4 short labeled lines only. TEXT: is there ANY legible text, letter, number or logo anywhere? answer none or describe it. SCENE: in one sentence, what does the photo actually show (outdoor or indoor, what objects)? SERVERS: does it look like an indoor data-center hallway / server-aisle room? answer yes or no. QUALITY: photorealistic or digital art/render? answer photo or render."},
    {"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+b64}}
  ]}],
  "max_tokens": 250
}).encode()
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=payload,
    headers={"Content-Type":"application/json","Authorization":"Bearer "+key,"HTTP-Referer":"https://readthesignal.net","X-Title":"The Signal Image Check"})
try:
    d = json.load(urllib.request.urlopen(req, timeout=90))
    print(d["choices"][0]["message"]["content"])
except Exception as e:
    print("ERR", e)
PY
