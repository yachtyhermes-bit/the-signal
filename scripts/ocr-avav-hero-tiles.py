#!/usr/bin/env python3
"""OCR sweep over tiles of the hero image at 2x upscale, to catch small text."""
import subprocess
import sys
from PIL import Image

src = sys.argv[1]
im = Image.open(src)
w, h = im.size
tiles = {
    "tl": (0, 0, w // 2, h // 2),
    "tr": (w // 2, 0, w, h // 2),
    "bl": (0, h // 2, w // 2, h),
    "br": (w // 2, h // 2, w, h),
    "center": (w // 4, h // 4, 3 * w // 4, 3 * h // 4),
}
for name, box in tiles.items():
    t = im.crop(box).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2), Image.LANCZOS)
    p = f"/tmp/ocr_{name}.png"
    t.convert("L").save(p)
    out = subprocess.run(
        ["tesseract", p, "stdout", "--psm", "11"], capture_output=True, text=True
    ).stdout
    words = [ln.strip() for ln in out.splitlines() if len(ln.strip()) >= 3]
    print(f"{name}: {words if words else 'no text'}")
