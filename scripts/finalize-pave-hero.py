#!/usr/bin/env python3
"""Finalize the PAVE hero: N2 candidate -> 1920x1080 JPEG (q92) into both
public/img/articles and _backup_dist/img/articles, then report specs.

Source /tmp/pave_cand/N2.jpg is 1440x800 (16:8.89). We trim 8% off the top to
tighten the composition (the QA flagged dead sky above the bridge), crop to
exact 16:9 and upscale with LANCZOS.
"""
import hashlib
import os
import shutil

from PIL import Image

SRC = "/tmp/pave_cand/N2.jpg"
SLUG = "etf-review-pave-2026-10-21"
PUB = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BAK = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
FINAL = (1920, 1080)

im = Image.open(SRC).convert("RGB")
w, h = im.size

top_trim = int(h * 0.08)
ch = h - top_trim
cw = int(ch * 16 / 9)
left = (w - cw) // 2
im = im.crop((left, top_trim, left + cw, top_trim + ch))
im = im.resize(FINAL, Image.LANCZOS)

for p in (PUB, BAK):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im.save(p, "JPEG", quality=92, optimize=True, progressive=True)

for p in (PUB, BAK):
    im2 = Image.open(p)
    b = os.path.getsize(p)
    md5 = hashlib.md5(open(p, "rb").read()).hexdigest()
    print(p)
    print("  dims=" + str(im2.size) + " format=" + im2.format
          + " ratio=" + str(round(im2.size[0] / im2.size[1], 4)))
    print("  bytes=" + str(b) + "  md5=" + md5)
