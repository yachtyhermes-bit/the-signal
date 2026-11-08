#!/usr/bin/env python3
"""Deterministic post-fix for the CLPS cartoon hero (no image generation).

The fal flux/schnell pass produced the right staging but (a) put a garbled
speech-bubble placard in the sky, (b) put a scribbled "signature" in the
bottom-right corner, and (c) never lettered the sign CLPS. The 3-generation
cap was already spent, so this script repairs the chosen frame by hand:

  1. repaint the sky where the garbled bubble + tail sat
  2. median-filter away the corner signature
  3. draw a painted plank sign over the desk lettered CLPS

Usage: python3 scripts/patch-cartoon-label.py <in.jpg> <out.jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

SRC, DST = sys.argv[1], sys.argv[2]
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.array(im).astype(np.float32)

# ---- 1. sky repaint over the garbled bubble + its tail -------------------
def patch(rect, src_xy, feather=7):
    """Copy a clean block to rect with a feathered edge."""
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    sx, sy = src_xy
    block = a[sy:sy + h, sx:sx + w]
    m = np.zeros((H, W), np.float32)
    m[y0:y1, x0:x1] = 1.0
    m = np.array(Image.fromarray((m * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(feather)), np.float32) / 255.0
    m = m[:, :, None]
    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - m[y0:y1, x0:x1]) + block * m[y0:y1, x0:x1]

patch((1170, 78, 1434, 214), (452, 70))      # placard body  <- clean sky
patch((1246, 206, 1324, 342), (786, 204))    # bubble tail   <- clean sky

# ---- 2. median away the corner signature --------------------------------
def deink(rect, size=15, feather=6):
    x0, y0, x1, y1 = rect
    region = Image.fromarray(np.uint8(a[y0:y1, x0:x1]))
    clean = np.array(region.filter(ImageFilter.MedianFilter(size))).astype(np.float32)
    m = np.zeros((y1 - y0, x1 - x0), np.float32)
    m[:] = 1.0
    m = np.array(Image.fromarray((m * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(feather)), np.float32)[:, :, None] / 255.0
    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - m) + clean * m

deink((1200, 758, 1425, 856))
deink((1398, 770, 1516, 834), size=17)

base = Image.fromarray(np.uint8(np.clip(a, 0, 255))).convert("RGB")

# ---- 3. painted plank sign over the desk, lettered CLPS ------------------
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
WORD = "CLPS"
BOARD_W, BOARD_H = 206, 94
CANVAS = 300, 200
cx, cy = 218, 272          # board centre in the frame
TILT = -2.6

board = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
d = ImageDraw.Draw(board)
ox, oy = (CANVAS[0] - BOARD_W) // 2, (CANVAS[1] - BOARD_H) // 2
bx0, by0, bx1, by1 = ox, oy, ox + BOARD_W, oy + BOARD_H

# plank face with a little paper/wood grain
d.rectangle([bx0, by0, bx1, by1], fill=(233, 224, 199, 255))
rng = np.random.default_rng(7)
grain = np.array(board)
for gy in range(by0 + 6, by1 - 4, 9):
    pts = [(bx0 + 4 + i * 12, gy + int(rng.integers(-2, 3))) for i in range(BOARD_W // 12)]
    d.line(pts, fill=(206, 195, 168, 130), width=1, joint="curve")

# ink border, drawn twice for a slightly uneven hand-inked weight
d.rectangle([bx0, by0, bx1, by1], outline=(54, 45, 38, 255), width=5)
d.rectangle([bx0 + 4, by0 + 4, bx1 - 4, by1 - 4], outline=(88, 76, 62, 90), width=1)
# nail heads
d.ellipse([bx0 + 9, by0 + 9, bx0 + 17, by0 + 17], fill=(70, 60, 50, 255))
d.ellipse([bx1 - 17, by0 + 9, bx1 - 9, by0 + 17], fill=(70, 60, 50, 255))

# letters: one at a time, jittered, so it reads hand-painted not typeset
size = 62
font = ImageFont.truetype(FONT, size)
track = 6
widths = [d.textbbox((0, 0), c, font=font)[2] - d.textbbox((0, 0), c, font=font)[0] for c in WORD]
total = sum(widths) + track * (len(WORD) - 1)
x = bx0 + (BOARD_W - total) / 2
for i, c in enumerate(WORD):
    lw = widths[i]
    lh = 74
    gl = Image.new("RGBA", (int(lw) + 24, int(lh) + 24), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.text((12, 6), c, font=font, fill=(45, 38, 32, 255))
    gl = gl.rotate(float(np.random.default_rng(100 + i).uniform(-4.5, 4.5)),
                   resample=Image.Resampling.BICUBIC, expand=False)
    board.alpha_composite(gl, (int(x) - 12, by0 + (BOARD_H - lh) // 2 - 12 + int(rng.integers(-2, 3))))
    x += lw + track

# support rods down into the canopy frame
rod = ImageDraw.Draw(board)
rod.line([(bx0 + 26, by1), (bx0 + 30, by1 + 34)], fill=(48, 40, 34, 255), width=4)
rod.line([(bx1 - 26, by1), (bx1 - 30, by1 + 34)], fill=(48, 40, 34, 255), width=4)

board = board.rotate(TILT, resample=Image.Resampling.BICUBIC, expand=False)
shadow = board.split()[3].filter(ImageFilter.GaussianBlur(9))
sh = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
sh.paste((20, 18, 16, 90), (0, 0), shadow)

base = base.convert("RGBA")
base.alpha_composite(sh, (cx - CANVAS[0] // 2 + 6, cy - CANVAS[1] // 2 + 8))
base.alpha_composite(board, (cx - CANVAS[0] // 2, cy - CANVAS[1] // 2))

out = base.convert("RGB")
for q in (94, 92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
    out.save(DST, "JPEG", quality=q, optimize=True, progressive=True)
    if len(open(DST, "rb").read()) <= 400_000:
        print("saved q=%d bytes=%d -> %s" % (q, len(open(DST, "rb").read()), DST))
        break
print("dims", out.size)
