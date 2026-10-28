#!/usr/bin/env python3
import base64, json, os, sys, urllib.request

IMG = sys.argv[1]
QUESTION = sys.argv[2]

key = None
for p in ["/home/chino/.hermes/profiles/yachty/.env", "/home/chino/thesignal/.env"]:
    if os.path.exists(p):
        for line in open(p):
            if line.strip().startswith("OPENROUTER_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    break
    if key:
        break
if not key:
    print("NO_KEY")
    sys.exit(1)

b64 = base64.b64encode(open(IMG, "rb").read()).decode()
payload = {
    "model": "google/gemini-2.5-flash",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": QUESTION},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
        ],
    }],
    "max_tokens": 400,
}
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
        "HTTP-Referer": "https://readthesignal.net",
        "X-Title": "The Signal Hero QA",
    },
)
try:
    r = urllib.request.urlopen(req, timeout=180)
    j = json.load(r)
    print(j["choices"][0]["message"]["content"].strip())
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("ERR", e, body[:400].decode(errors="replace"))
