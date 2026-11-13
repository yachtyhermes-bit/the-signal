#!/usr/bin/env python3
"""Deterministic post-fix for the MOD (Modine/Samsung) cartoon hero — no new generation.

The 3-generation cap was spent. Best of the three takes (correct staging: a chiller
inspected by a bespectacled buyer with a clipboard, a worker in coveralls, a clean
"MOD" sign, single-panel ink-and-watercolour) carried one defect: a bold cursive
artist handle "@Makyoline" (~156x26 px, 1750 ink pixels) in the bottom-right
corner, painted over the pale top edge of the orange floor wash.

The other two takes read "$" and "Readinq Facccestion" on the sign, so they lose.

Fill strategy — variants tried on this frame, kept for the record:
  * fixed-threshold mask -> pale halo (lum 205-235) survived and, once mirrored,
                            left ghost letters "AM" in the wash
  * box / row median     -> cream pulled into wash (grey blotch) or wash smeared
                            over paper (straight edge)
  * Jacobi diffusion     -> rectangular light patch
This file: ADAPTIVE per-row threshold (90th percentile minus a margin) so the
whole halo goes, a wide dilation so the mask edge sits on clean pixels, a hard
composite (no partial-alpha blending, which is what made the ghosts), and a
reflection clone so hue and brush texture come from the artwork itself.

Usage: python3 scripts/retouch-mod-samsung-cartoon-hero.py <in.jpg> <out.jpg>
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC, DST = sys.argv[1], sys.argv[2]
W, H = 1536, 864
MAX_BYTES = 400_000

BOX = (1166, 790, 1474, 864)          # handle box, from a 3x zoom of the corner


def glyph_mask(arr, box, margin=12, grow=9):
    """Mask ink in box using a per-row adaptive threshold (paper-relative)."""
    x0, y0, x1, y1 = box
    lum = arr[y0:y1, x0:x1].max(axis=2)
    thr = np.percentile(lum, 90, axis=1, keepdims=True) - margin
    m = (lum < thr).astype(np.uint8) * 255
    img = Image.fromarray(m)
    img = img.filter(ImageFilter.MaxFilter(2 * grow + 1))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    return (np.array(img, np.float32) / 255.0 > 0.5).astype(np.float32)


def nearest_clean(covered, iters=80):
    h, w = covered.shape
    rr, cc = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    sr, sc = rr.copy(), cc.copy()
    known = ~covered
    for _ in range(iters):
        if known.all():
            break
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            kn = np.roll(known, (dr, dc), (0, 1))
            sr_s = np.roll(sr, (dr, dc), (0, 1))
            sc_s = np.roll(sc, (dr, dc), (0, 1))
            take = (~known) & kn
            if take.any():
                sr[take] = sr_s[take]
                sc[take] = sc_s[take]
                known[take] = True
    return sr, sc


def reflect_clone(a, orig, box, mask):
    """Copy pigment mirrored across the nearest clean pixel; never copy ink."""
    x0, y0, x1, y1 = box
    covered = mask > 0.5
    if not covered.any():
        return
    sr, sc = nearest_clean(covered)
    h, w = covered.shape
    rr, cc = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    src = orig[y0:y1, x0:x1]
    pr = np.clip(2 * sr - rr, 0, h - 1)
    pc = np.clip(2 * sc - cc, 0, w - 1)
    fill = src[pr, pc]
    bad = (fill.max(axis=2) < 205) | covered[pr, pc]
    if bad.any():
        fill[bad] = src[sr[bad], sc[bad]]
        still = fill.max(axis=2) < 205
        if still.any():
            fill[still] = np.median(src[~covered], axis=0)
    # hard composite: partial alpha here blends the pale halo back in as ghosts
    a[y0:y1, x0:x1] = np.where(covered[:, :, None], fill, a[y0:y1, x0:x1])


im = Image.open(SRC).convert("RGB")
if im.size != (W, H):
    im = im.resize((W, H), Image.LANCZOS)
a = np.array(im).astype(np.float32)
orig = a.copy()

union = np.zeros((BOX[3] - BOX[1], BOX[2] - BOX[0]), np.float32)
for i, margin in enumerate((12, 9, 6), 1):
    lum = a[BOX[1]:BOX[3], BOX[0]:BOX[2]].max(axis=2)
    before = int((lum < 205).sum())
    m = glyph_mask(a, BOX, margin=margin)
    union = np.maximum(union, m)
    reflect_clone(a, orig, BOX, m)
    lum = a[BOX[1]:BOX[3], BOX[0]:BOX[2]].max(axis=2)
    print("pass %d margin=%d ink_before=%d ink_left=%d min_lum=%d"
          % (i, margin, before, int((lum < 205).sum()), int(lum.min())))
    if before == 0 and (lum < 205).sum() == 0:
        break

print("mask coverage %.1f%% of box" % (100.0 * (union > 0.5).mean()))

out = Image.fromarray(np.uint8(np.clip(a, 0, 255)))
for q in (92, 90, 88, 86, 84, 82, 80):
    out.save(DST, "JPEG", quality=q, optimize=True, progressive=True)
    n = os.path.getsize(DST)
    if n <= MAX_BYTES:
        print("saved q=%d bytes=%d -> %s" % (q, n, DST))
        break

lum = np.array(out).astype(np.float32)[BOX[1]:BOX[3], BOX[0]:BOX[2]].max(axis=2)
print("residual ink px<205: %d (min_lum=%d)" % (int((lum < 205).sum()), int(lum.min())))
print("dims %dx%d" % out.size)
