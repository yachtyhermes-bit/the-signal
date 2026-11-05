#!/usr/bin/env python3
"""Post-process the shipped AMAT hero: colour grade + wafer-surface retouch.

The 2026-11-05 hero for amat-memory-capex-test-2026 was generated with
gen-amat-memory-capex-hero-20261105.py ATTEMPT=2 (robot transfer arm, 300mm
wafer, technician behind glass).  flux/schnell rendered the wafer with a
concentric spun-metal texture, so this script (a) grades the frame to kill the
cyan cast, and (b) suppresses only the fine groove detail inside the disc so it
reads as a mirror-polished wafer, leaving reflections and geometry intact.

Usage:
  /home/chino/video-venv/bin/python3 scripts/grade_amat_hero.py <raw-attempt.jpg>

Writes public/img/articles/<slug>.jpg, img/articles/<slug>.jpg and
_backup_dist/img/articles/<slug>.jpg.
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

SLUG = "amat-memory-capex-test-2026"
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
REPO_COPY = f"/home/chino/thesignal/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"

# disc geometry in the 1920x1080 attempt-2 frame
CX, CY, R = 1162, 540, 315


def grade(img):
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * 1.045 + 2)))
    g = g.point(lambda v: min(255, int(v * 1.008)))
    b = b.point(lambda v: int(v * 0.955))
    img = Image.merge("RGB", (r, g, b))
    img = ImageEnhance.Contrast(img).enhance(1.07)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=3))

    arr = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(7)
    grain = rng.normal(0.0, 2.6, arr.shape[:2])[..., None]
    arr = np.clip(arr + grain, 0, 255)

    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vign = np.clip(1.0 - 0.16 * np.clip((dist - 0.55) / 0.75, 0, 1) ** 1.6, 0.80, 1.0)[..., None]
    return Image.fromarray(np.clip(arr * vign, 0, 255).astype(np.uint8))


def retouch_wafer(img):
    w, h = img.size
    a = np.asarray(img).astype(np.float32)
    low = np.asarray(img.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    reduced = np.clip(low + (a - low) * 0.25, 0, 255)

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
    m = np.clip(((R - 10) - dist) / 8.0, 0, 1)
    m = (m * m * (3 - 2 * m))[..., None]

    out = np.clip(a * (1 - m) + reduced * m, 0, 255)
    lum = out.mean(axis=2, keepdims=True)
    out = np.clip(out + (lum - 128) * 0.05 * m, 0, 255)
    return Image.fromarray(out.astype(np.uint8))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    img = Image.open(src).convert("RGB")
    if img.size != (1920, 1080):
        img = img.resize((1920, 1080), Image.LANCZOS)
    img = retouch_wafer(grade(img))

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    q = 93
    img.save(OUTPUT, "JPEG", quality=q, optimize=True)
    size = os.path.getsize(OUTPUT)
    while size > 390000 and q > 60:
        q -= 3
        img.save(OUTPUT, "JPEG", quality=q, optimize=True)
        size = os.path.getsize(OUTPUT)
    print(f"saved {OUTPUT} {img.size} {size} bytes q={q}")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    os.makedirs(os.path.dirname(REPO_COPY), exist_ok=True)
    shutil.copy(OUTPUT, REPO_COPY)
    print(f"mirrored to {BACKUP} and {REPO_COPY}")


if __name__ == "__main__":
    main()
