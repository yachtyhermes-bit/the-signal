#!/usr/bin/env python3
"""Hero for: Marvell Technology (MRVL) — custom AI silicon + electro-optics ahead of
the 2026-10-06 Investor Day.
Slug: mrvl-custom-silicon-investor-day-2026

The FAL flux/schnell generator is LOCKED on this box ("User is locked. Reason: TOP_UP."
— re-verified 2026-10-02 with a single POST to https://fal.run/fal-ai/flux/schnell,
HTTP 403). So this hero is a real, freely licensed photograph of the OPTICAL INTERCONNECT
layer Marvell sells into — a working optical communications system testbed (optical fibre,
lab bench, instrumented optics) — i.e. the "nervous system" of the AI data centre
(1.6T optical modules / PAM4 DSP / silicon photonics), NOT a data-centre hallway, NOT a
server aisle, NOT a plain silicon wafer, and NOT the IGBT module / rooftop cooling plant /
aircraft-factory shots used on recent heroes.

Source : Wikimedia Commons, "Working at an optical communications system testbed.jpg"
         by NiamhTalking90, CC BY-SA 4.0
         https://commons.wikimedia.org/wiki/File:Working_at_an_optical_communications_system_testbed.jpg
         Depicts: an engineer adjusting an instrumented optical-fibre testbed (hollow-core /
         optical communications rig) — verified photo, no legible text, no logo, no watermark.
Credit : the CC BY-SA 4.0 attribution lives in the article JSON image.caption.
Process: center-crop to 16:9 -> 1920x1080 LANCZOS -> JPEG q88 optimize -> public/ + _backup_dist/ -> R2

Re-run AFTER FAL is topped up to replace it with a generated hero (then update the caption).
"""
import os
import shutil
import subprocess
import sys

import requests
from PIL import Image

SLUG = 'mrvl-custom-silicon-investor-day-2026'
SRC = ('https://upload.wikimedia.org/wikipedia/commons/8/82/'
       'Working_at_an_optical_communications_system_testbed.jpg')
ROOT = '/home/chino/thesignal'
UA = {'User-Agent': 'TheSignal/1.0 (editorial; editorial@readthesignal.net)'}
RAW = '/tmp/mrvl_hero_src.jpg'
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
