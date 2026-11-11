#!/usr/bin/env python3
"""Deterministic post-fix for the CRWV cartoon hero (no image generation).

The 3-generation cap was spent on this frame. The chosen take (best of three:
correct staging, ink+watercolour, no signature/watermark) still had two defects:

  1. garbled small print on the oversized invoice ("INW IDT")
  2. a bare "4" plate on the chain-link fence where the RENT label belongs

Fixes, in the same spirit as patch-cartoon-label.py:
  1. mask-fill only the dark glyph pixels of the invoice print (paper stays blank)
  2. mask-fill the plate interior and hand-letter RENT with per-character jitter

Usage: python3 scripts/retouch-crwv-cartoon-hero.py <in.jpg> <out.jpg>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, DST = sys.argv[1], sys.argv[2]
W, H = 1536, 864
MAX_BYTES = 400_000

im = Image.open(SRC).convert("RGB")
im = im.resize((W, H), Image.LANCZOS) if im.size != (W, H) else im
a = np.array(im).astype(np.float32)


def flat_fill(rect, keep_bright, feather=3, noise=2.5, med=9):
    """Fill rect with the median colour of its clean (non-ink) pixels + grain."""
    x0, y0, x1, y1 = rect
    region = a[y0:y1, x0:x1]
    lum = region.max(axis=2)
    clean = region[lum >= keep_bright]
    if clean.size == 0:
        return
    col = np.median(clean, axis=0)
    h, w = region.shape[:2]
    rng = np.random.default_rng(991)
    fill = np.ones((h, w, 3), np.float32) * col[None, None, :]
    fill += rng.normal(0, noise, (h, w, 3)).astype(np.float32)
    m = np.ones((h, w), np.float32)
    m = np.array(Image.fromarray((m * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(feather)), np.float32) / 255.0
    m = m[:, :, None]
    a[y0:y1, x0:x1] = region * (1 - m) + fill * m


# ---- 1. invoice small print -> blank paper ------------------------------
flat_fill((632, 72, 692, 102), keep_bright=200, feather=4, noise=2.0)

# ---- 2. fence plate: clear the "4" and letter RENT ----------------------
PLATE = (125, 519, 208, 608)          # outer edge of the orange plate
x0, y0, x1, y1 = PLATE
inner = (x0 + 7, y0 + 7, x1 - 7, y1 - 7)
flat_fill(inner, keep_bright=170, feather=3, noise=3.0)

base = Image.fromarray(np.uint8(np.clip(a, 0, 255))).convert("RGB")

WORD = "RENT"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
iw, ih = inner[2] - inner[0], inner[3] - inner[1]

size = 26
font = ImageFont.truetype(FONT, size)
widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in WORD]
track = 1
total = sum(widths) + track * (len(WORD) - 1)

layer = Image.new("RGBA", (int(total) + 40, int(size * 2) + 30), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
rng = np.random.default_rng(1207)
px = 20
for i, c in enumerate(WORD):
    lw = widths[i]
    gh = int(size * 1.9)
    gl = Image.new("RGBA", (lw + 24, gh + 24), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    bb = font.getbbox(c)
    # doubled pass = slightly uneven ink weight, like a loaded brush
    gd.text((12 - bb[0], 10 - bb[1]), c, font=font, fill=(40, 33, 28, 255))
    gd.text((12 - bb[0] + 1, 10 - bb[1]), c, font=font, fill=(40, 33, 28, 150))
    gl = gl.rotate(float(rng.uniform(-7.0, 7.0)),
                   resample=Image.Resampling.BICUBIC, expand=False)
    layer.alpha_composite(gl, (int(px) - 12,
                               int((layer.height - gh) / 2) + int(rng.integers(-3, 4))))
    px += lw + track

# condense to the plate and soak the fresh ink into the paper a touch
fit = (iw - 8) / (layer.width - 40)
layer = layer.resize((max(1, int(layer.width * min(1.0, fit))), layer.height),
                     Image.LANCZOS)
layer = layer.filter(ImageFilter.GaussianBlur(0.5))

out = base.convert("RGBA")
out.alpha_composite(layer, (inner[0] + (iw - layer.width) // 2,
                            inner[1] + (ih - layer.height) // 2))
out = out.convert("RGB")

for q in (92, 90, 88, 86, 84, 82, 80, 78):
    out.save(DST, "JPEG", quality=q, optimize=True, progressive=True)
    n = len(open(DST, "rb").read())
    if n <= MAX_BYTES:
        print("saved q=%d bytes=%d -> %s" % (q, n, DST))
        break
print("dims %dx%d font=%d ink_x=%d-%d" % (out.size[1], out.size[0], size,
                                          inner[0], inner[2]))
