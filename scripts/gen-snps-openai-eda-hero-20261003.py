#!/usr/bin/env python3
"""Hero for: Synopsys (SNPS) — EDA chip-design software, the OpenAI
'GPT-Synopsys' partnership and the 2026-09-30 Investor Day growth-reset story.
Slug: snps-openai-eda-growth-reset-2026

The FAL flux/schnell generator is LOCKED on this box ("User is locked. Reason:
TOP_UP." — re-verified 2026-10-03 with a single POST to https://fal.run/fal-ai/flux/schnell,
HTTP 403). So this hero is a real, freely licensed photograph of the CHIP DESIGN /
VERIFICATION layer Synopsys' EDA tools exist to serve.

Scene: fine metallic probe needles making contact with a strip of silicon dies on a
bench — a semiconductor probe / verification macro. Reads as chip-DESIGN verification
engineering, NOT a data-centre, NOT a fab/cleanroom, NOT a finance story, NOT a
wafer-in-hand glamour shot.

Deliberately DISTINCT from recent heroes:
 - MRVL, Oct 2 : optical-fibre communications testbed
 - ON,   Oct 2 : power IGBT module with the cover off
 - SNPS, Sep 22: design engineer at a monitor showing a chip floorplan (NOT reused)
Not a monitor-with-floorplan, not a server aisle / GPU rack / cable run, not abstract
or neon / synthwave, not a 3D render, not a chart.

Source : Wikimedia Commons, "Positioning test probes on to a microchip.jpg"
         by Iuri Kothe (Flickr: iurikothe), CC BY 2.0
         https://commons.wikimedia.org/wiki/File:Positioning_test_probes_on_to_a_microchip.jpg
         Original Flickr credit: "chip 02" by Iuri Kothe, Rafael Soares & Pablo Vogel.
         Verified photo-real, and verified free of any legible text / brand / watermark
         by adversarial vision inspection of the actual pixels.
Credit : the CC BY 2.0 attribution lives in the article JSON image.caption.
Process: center-crop to 16:9 -> 1920x1080 LANCZOS -> JPEG q88 optimize -> public/ +
         _backup_dist/ -> R2.

Re-run AFTER FAL is topped up to replace it with a generated hero (then update caption).
"""
import os
import shutil
import subprocess
import sys

import requests
from PIL import Image

SLUG = 'snps-openai-eda-growth-reset-2026'
SRC = ('https://upload.wikimedia.org/wikipedia/commons/4/4b/'
       'Positioning_test_probes_on_to_a_microchip.jpg')
ROOT = '/home/chino/thesignal'
UA = {'User-Agent': 'TheSignal/1.0 (editorial; editorial@readthesignal.net)'}
RAW = '/tmp/snps_openai_eda_hero_src.jpg'
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
    print('wrote', bak, os.path.getsize(bak), 'bytes')
    out = subprocess.run([PY, os.path.join(ROOT, 'scripts/r2_upload.py'), 'hero', SLUG],
                         capture_output=True, text=True)
    print(out.stdout, out.stderr)
    sys.exit(out.returncode)


if __name__ == '__main__':
    main()
