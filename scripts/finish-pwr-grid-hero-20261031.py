#!/usr/bin/env python3
"""Photographic finishing pass for the pwr-grid-backlog hero.

Flux/schnell output reads slightly airbrushed at web size: smooth midtones,
no grain, flat micro-contrast. This applies a mild camera-negative treatment
(tiny S-curve, unsharp mask, fine luminance grain) so it reads as a press
photograph rather than a render. No content is added or removed, no text is
introduced. Output stays under the 400KB cap at 1536x864.

Usage: finish-pwr-grid-hero-20261031.py <in.jpg> <out.jpg>
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC = sys.argv[1]
DST = sys.argv[2]
MAX_BYTES = 400 * 1024


def srgb_to_linear(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(a):
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.clip(a, 0, None), 1 / 2.4) - 0.055)


img = Image.open(SRC).convert("RGB")

# 1. gentle contrast + saturation
img = ImageEnhance.Contrast(img).enhance(1.06)
img = ImageEnhance.Color(img).enhance(1.03)

# 2. unsharp mask: gentle radius to avoid edge halos
img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=4))
img = img.filter(ImageFilter.UnsharpMask(radius=4.0, percent=14, threshold=0))

# 3. fine luminance grain, applied in linear-ish midtones
arr = np.asarray(img, dtype=np.float32) / 255.0
lin = srgb_to_linear(arr)
rng = np.random.default_rng(20261031)
grain = rng.normal(0.0, 0.0028, size=arr.shape[:2]).astype(np.float32)
roll = rng.integers(0, 3)
grain = np.roll(grain, roll, axis=1)
# grain strongest in midtones, minimal in deep shadow/highlight
lum = arr.mean(axis=2)
weight = (0.35 + 0.9 * lum * (1.0 - lum) * 2.0)[..., None]
lin = lin + grain[..., None] * weight
arr = np.clip(linear_to_srgb(np.clip(lin, 0, 1)), 0, 1)
img = Image.fromarray((arr * 255.0 + 0.5).astype(np.uint8), "RGB")

# 4. save under cap (target well under 400KB even counting KB as 400,000 bytes)
TARGET = 340 * 1024
for q in (95, 94, 93, 92, 91, 90, 88, 86, 84, 82):
    img.save(DST, "JPEG", quality=q, optimize=True, progressive=True, subsampling=2)
    size = __import__("os").path.getsize(DST)
    print(f"q={q} 4:2:0 -> {size} bytes")
    if size < TARGET:
        break

print(f"WROTE {DST} dims={img.size} bytes={size}")
