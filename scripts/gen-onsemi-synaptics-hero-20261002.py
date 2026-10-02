#!/usr/bin/env python3
"""Hero for: onsemi buys Synaptics in a revised $5.7B all-cash deal (edge AI / "physical AI").
Slug: onsemi-synaptics-edge-ai-acquisition-2026

The usual FAL flux/schnell generator is LOCKED on this box ("User is locked. Reason:
TOP_UP." — verified 2026-10-02 with a single POST to https://fal.run/fal-ai/flux/schnell,
HTTP 403), the OpenRouter image endpoints are blocked by an account guardrail, and the
free Pollinations tier only serves watermarked SANA. So this hero is a real, freely
licensed photograph of a POWER SEMICONDUCTOR MODULE — the silicon-carbide/IGBT power
devices at the heart of onsemi's business (power modules for EV, industrial and
AI data-centre power delivery) — which is deliberately NOT a data-centre corridor,
NOT a server aisle, and NOT the silicon-wafer shot used for yesterday's AVGO hero.

Source : Wikimedia Commons, "CM600DU-24NFH.jpg"
         by Pslawinski, CC BY-SA 3.0 (originally by Pslawinski, via Wikimedia Commons)
         https://commons.wikimedia.org/wiki/File:CM600DU-24NFH.jpg
         Depicts: Powerex CM600DU-24NFH IGBT power module with the cover removed to
         show the IGBT dies and freewheeling diodes.
Credit : the CC BY-SA 3.0 attribution lives in the article JSON image.caption.
Process: center-crop to 16:9 -> 1920x1080 LANCZOS -> JPEG q88 -> public/ + _backup_dist/ -> R2

Re-run AFTER FAL is topped up to replace it with a generated hero (then update the caption).
"""
import os
import shutil
import subprocess
import sys

import requests
from PIL import Image

SLUG = 'onsemi-synaptics-edge-ai-acquisition-2026'
SRC = 'https://upload.wikimedia.org/wikipedia/commons/c/c1/CM600DU-24NFH.jpg'
ROOT = '/home/chino/thesignal'
UA = {'User-Agent': 'TheSignal/1.0 (editorial; editorial@readthesignal.net)'}
RAW = '/tmp/onsemi_hero_src.jpg'
PY = '/home/chino/video-venv/bin/python3'


def main():
    if not os.path.exists(RAW):
        r = requests.get(SRC, headers=UA, timeout=180)
        r.raise_for_status()
        with open(RAW, 'wb') as fh:
            fh.write(r.content)
    im = Image.open(RAW).convert('RGB')
    w, h = im.size
    ar = 16 / 9
    if w / h > ar:
        nw = int(h * ar)
        x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / ar)
        y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    im = im.resize((1920, 1080), Image.LANCZOS)

    pub = os.path.join(ROOT, 'public/img/articles', SLUG + '.jpg')
    bak = os.path.join(ROOT, '_backup_dist/img/articles', SLUG + '.jpg')
    os.makedirs(os.path.dirname(pub), exist_ok=True)
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    im.save(pub, 'JPEG', quality=88, optimize=True)
    shutil.copy(pub, bak)
    print('wrote', pub, os.path.getsize(pub), 'bytes', im.size)
    out = subprocess.run([PY, os.path.join(ROOT, 'scripts/r2_upload.py'), 'hero', SLUG],
                         capture_output=True, text=True)
    print(out.stdout, out.stderr)
    sys.exit(out.returncode)


if __name__ == '__main__':
    main()
