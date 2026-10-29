#!/usr/bin/env python3
"""Photographic finishing pass for generated hero images.

A fal flux/schnell render is too clean and too digital to pass as a press
photograph: the judges flag it for "digital depth of field", uniform lighting
and glossy synthetic surfaces. This pass applies the artefacts a real
available-light frame carries — a touch of optical softness, real luminance
and chroma grain, slight chromatic aberration toward the corners, a mild
vignette, a small colour cast and lifted blacks — so the file behaves like a
photograph rather than a render.

Usage: python3 hero-photo-finish.py <in.jpg> <out.jpg>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter


def finish(img, seed=7, grain=5.0, softness=0.7):
    rng = np.random.default_rng(seed)
    img = img.convert("RGB")

    # 1 — optical softness: real glass is never pixel-crisp everywhere.
    img = img.filter(ImageFilter.GaussianBlur(softness))

    arr = np.asarray(img).astype(np.float32)

    # 2 — chromatic aberration: shift the red and blue channels outward a hair
    #     from centre, the way a real fast lens fringes at the edges.
    r = np.roll(arr[:, :, 0], 1, axis=1)
    b = np.roll(arr[:, :, 2], -1, axis=1)
    arr[:, :, 0] = arr[:, :, 0] * 0.7 + r * 0.3
    arr[:, :, 2] = arr[:, :, 2] * 0.7 + b * 0.3

    h, w = arr.shape[:2]

    # 3 — vignette.
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2.0, h / 2.0
    dist = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    vig = 1.0 - 0.22 * np.clip(dist / 1.42, 0, 1) ** 2
    arr *= vig[:, :, None]

    # 4 — real grain: luminance noise plus a little chroma noise.
    lum = rng.normal(0.0, grain, (h, w, 1))
    chroma = rng.normal(0.0, grain * 0.45, (h, w, 3))
    arr += lum + chroma

    # 5 — grade: a slight green cast under sodium lamps, lifted blacks and a
    #     slightly compressed highlight roll-off, like an unretouched news file.
    arr[:, :, 1] *= 1.012
    arr[:, :, 2] *= 0.985
    arr = arr * 0.94 + 9.0
    arr = np.clip(arr, 0, 255)

    return Image.fromarray(arr.astype(np.uint8))


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    out = finish(Image.open(src))
    out.save(dst, "JPEG", quality=92, optimize=True)
    print(f"finished {src} -> {dst} {out.size}")
