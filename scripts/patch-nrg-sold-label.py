#!/usr/bin/env python3
"""Deterministic post-fix for the NRG/LS Power cartoon hero (no image generation).

The flux/schnell pass staged the scene correctly (plant roped to the flatbed,
buyer driving, seller handing over the deed) but never lettered the SOLD sign,
and the 3-generation cap was already spent. Same repair the CLPS hero needed:
paint a plank sign flat against the big cooling tower and letter it S O L D.

Usage: python3 scripts/patch-nrg-sold-label.py <in.jpg> <out.jpg>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, DST = sys.argv[1], sys.argv[2]
im = Image.open(SRC).convert("RGBA")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
WORD = "SOLD"
BOARD_W, BOARD_H = 180, 86
CANVAS = 260, 180
cx, cy = 355, 400          # board centre: blank face of the main cooling tower
TILT = -2.2

board = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
d = ImageDraw.Draw(board)
ox, oy = (CANVAS[0] - BOARD_W) // 2, (CANVAS[1] - BOARD_H) // 2
bx0, by0, bx1, by1 = ox, oy, ox + BOARD_W, oy + BOARD_H

d.rectangle([bx0, by0, bx1, by1], fill=(236, 227, 203, 255))
rng = np.random.default_rng(11)
for gy in range(by0 + 6, by1 - 4, 9):
    pts = [(bx0 + 4 + i * 12, gy + int(rng.integers(-2, 3))) for i in range(BOARD_W // 12)]
    d.line(pts, fill=(208, 197, 170, 130), width=1, joint="curve")

d.rectangle([bx0, by0, bx1, by1], outline=(54, 45, 38, 255), width=4)
d.rectangle([bx0 + 4, by0 + 4, bx1 - 4, by1 - 4], outline=(88, 76, 62, 90), width=1)
d.ellipse([bx0 + 8, by0 + 8, bx0 + 15, by0 + 15], fill=(70, 60, 50, 255))
d.ellipse([bx1 - 15, by0 + 8, bx1 - 8, by0 + 15], fill=(70, 60, 50, 255))

font = ImageFont.truetype(FONT, 56)
track = 5
widths = [d.textbbox((0, 0), c, font=font)[2] - d.textbbox((0, 0), c, font=font)[0] for c in WORD]
total = sum(widths) + track * (len(WORD) - 1)
x = bx0 + (BOARD_W - total) / 2
for i, c in enumerate(WORD):
    lw = widths[i]
    lh = 66
    gl = Image.new("RGBA", (int(lw) + 24, int(lh) + 24), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.text((12, 4), c, font=font, fill=(43, 36, 30, 255))
    gl = gl.rotate(float(np.random.default_rng(200 + i).uniform(-3.5, 3.5)),
                   resample=Image.Resampling.BICUBIC, expand=False)
    board.alpha_composite(gl, (int(x) - 12, by0 + (BOARD_H - lh) // 2 - 12 + int(rng.integers(-2, 3))))
    x += lw + track

# two nails/supports up into the tower face
rod = ImageDraw.Draw(board)
rod.line([(bx0 + 24, by0), (bx0 + 28, by0 - 26)], fill=(48, 40, 34, 255), width=3)
rod.line([(bx1 - 24, by0), (bx1 - 28, by0 - 26)], fill=(48, 40, 34, 255), width=3)

board = board.rotate(TILT, resample=Image.Resampling.BICUBIC, expand=False)
shadow = board.split()[3].filter(ImageFilter.GaussianBlur(8))
sh = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
sh.paste((20, 18, 16, 95), (0, 0), shadow)

im.alpha_composite(sh, (cx - CANVAS[0] // 2 + 5, cy - CANVAS[1] // 2 + 7))

# ghost the underlying ink/paper through the plank face so it reads drawn-on
# rather than collaged: multiply-blend a soft copy of the base under the board
px, py = cx - CANVAS[0] // 2, cy - CANVAS[1] // 2
under = im.crop((px, py, px + CANVAS[0], py + CANVAS[1])).convert("RGB")
under = under.filter(ImageFilter.GaussianBlur(3))

_stage = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
_stage.alpha_composite(board)
_sa = np.array(_stage).astype(np.float32)
_ua = np.array(under).astype(np.float32)
_mask = (_sa[:, :, 3:4] / 255.0) * 0.22
_rgb = _sa[:, :, :3] * (_ua / 255.0)
_ink = _sa[:, :, :3] * (1 - _mask) + _rgb * _mask
# soften + grain so the plank reads as painted on paper, not a vector overlay
_rng = np.random.default_rng(5)
_ink = np.clip(_ink + _rng.normal(0, 4.2, _ink.shape), 0, 255)
_stage = Image.fromarray(np.uint8(np.clip(np.dstack([_ink, _sa[:, :, 3]]), 0, 255)), "RGBA")
_stage = _stage.filter(ImageFilter.GaussianBlur(0.7))
im.alpha_composite(_stage, (px, py))

out = im.convert("RGB")
for q in (94, 92, 90, 88, 86, 84, 82, 80, 78, 76, 74):
    out.save(DST, "JPEG", quality=q, optimize=True, progressive=True)
    n = len(open(DST, "rb").read())
    if n <= 400_000:
        print("saved q=%d bytes=%d -> %s" % (q, n, DST))
        break
print("dims", out.size)
