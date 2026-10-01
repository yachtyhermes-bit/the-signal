#!/usr/bin/env python3
"""
Hero for: Broadcom Will Lend Anthropic Up to $42 Billion for Chip Leases
(articles/posts/avgo-anthropic-42b-chip-lease-financing-2026.json)

The usual FAL flux/schnell generator was unavailable for this article — every FAL key on the
box returned 403 "User is locked. Reason: TOP_UP.", the Google image models returned 429
(quota), the OpenRouter image endpoints are blocked by the account guardrail, and the free
Pollinations tier only serves SANA (watermarked). So this hero is a real, freely licensed
photograph of a processed silicon wafer — the disc every custom AI accelerator is cut from.

Source : Wikimedia Commons, "5C2A5953R - 49913961083 – Silicon Wafer 20200519.jpg"
         by Rob Bulmahn, CC BY 2.0 (via https://www.flickr.com/photos/rbulmahn/49913961083/)
Credit : the attribution lives in the article JSON image.caption (CC BY 2.0 requires it)
Process: center-crop to 16:9 -> 1920x1080 LANCZOS -> JPEG q88 -> public/ + _backup_dist/ -> R2

Re-run AFTER FAL is topped up to replace it with a generated hero (then update the caption).
"""
import os
import shutil
import subprocess
import sys

import requests
from PIL import Image

SLUG = 'avgo-anthropic-42b-chip-lease-financing-2026'
SRC = ('https://upload.wikimedia.org/wikipedia/commons/c/c0/'
       '5C2A5953R_-_49913961083_%E2%80%93_Silicon_Wafer_20200519.jpg')
ROOT = '/home/chino/thesignal'
UA = {'User-Agent': 'TheSignal/1.0 (editorial; editorial@readthesignal.net)'}
RAW = '/tmp/avgo_hero_src.jpg'


def main():
    if not os.path.exists(RAW):
        r = requests.get(SRC, headers=UA, timeout=180)
        r.raise_for_status()
        open(RAW, 'wb').write(r.content)
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
    im.save(pub, 'JPEG', quality=88, optimize=True)
    shutil.copy(pub, bak)
    print('wrote', pub, os.path.getsize(pub), 'bytes')
    print(subprocess.run([sys.executable, os.path.join(ROOT, 'scripts/r2_upload.py'), 'hero', SLUG],
                         capture_output=True, text=True).stdout)


if __name__ == '__main__':
    main()
