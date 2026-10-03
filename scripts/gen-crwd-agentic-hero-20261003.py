#!/usr/bin/env python3
"""Hero for: CrowdStrike (CRWD) -- AI agents as the next enterprise security perimeter
(Agentic Identity Provider / Falcon Guardian / OpenAI Marketplace).
Slug: crwd-agentic-security-perimeter-ai-budget-2026

The usual FAL flux/schnell generator is LOCKED on this box ("User is locked. Reason:
TOP_UP." -- re-verified 2026-10-03 with a single POST to https://fal.run/fal-ai/flux/schnell,
HTTP 403). So, per house convention, this hero is a real, freely-licensed photograph of a
BIOMETRIC FINGERPRINT IDENTITY SCANNER -- the "something that verifies who you are before it
lets you in" object at the heart of the article's thesis (AI agents now getting their own
verifiable, short-lived identities for enterprise access). Deliberately NOT a data-centre
corridor / server aisle, NOT abstract digital art, NOT a monitor wall.

Source : Wikimedia Commons, "Biometric Fingerprint Scanner.jpg"
         by Sanskritibharti1398, CC BY-SA 4.0
         https://commons.wikimedia.org/wiki/File:Biometric_Fingerprint_Scanner.jpg
         Depicts: a biometric fingerprint identity scanner of the kind used for verifiable
         access/attendance in institutions.
Credit : the CC BY-SA 4.0 attribution lives in the article JSON image.caption.
Process: center-crop to 16:9 -> 1920x1080 LANCZOS -> JPEG q88 -> public/ + _backup_dist/ -> R2

Re-run AFTER FAL is topped up to replace it with a generated hero (then update the caption).
"""
import os
import shutil
import subprocess
import sys

import requests
from PIL import Image

SLUG = 'crwd-agentic-security-perimeter-ai-budget-2026'
SRC = 'https://upload.wikimedia.org/wikipedia/commons/8/82/Biometric_Fingerprint_Scanner.jpg'
ROOT = '/home/chino/thesignal'
UA = {'User-Agent': 'TheSignal/1.0 (editorial; editorial@readthesignal.net)'}
RAW = '/tmp/crwd_hero_src.jpg'
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
