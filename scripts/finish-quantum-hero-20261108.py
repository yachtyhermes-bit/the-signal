#!/usr/bin/env python3
"""Finish the shipped ATTEMPT=1 frame for quantum-error-correction-explainer-2026.

All 3 FAL generations were spent (attempts 2 and 3 lost the dilution fridge
entirely and carried brand text on lab cabinets). Attempt 1 is the only frame
with the required subject, so it is re-fetched from its stored FAL output URL
(no new generation) and given a photographic finish here:

  * 16:9 centre crop -> 1536x864 (generator's crop_to_ratio)
  * gentle desaturation and cool shadow tint
  * soft lens vignette to settle the dim frame edges
  * fine monochrome grain, as from a real high-ISO frame

Writes public/img/articles/<SLUG>.jpg and mirrors to _backup_dist.
"""
import os
import sys
import numpy as np
from PIL import Image, ImageEnhance

sys.path.insert(0, "/home/chino/thesignal/scripts")
import importlib
gen = importlib.import_module("gen-quantum-error-correction-hero-20261108")

RAW = "/tmp/qec_attempt1_raw.jpg"
SLUG = gen.SLUG
OUTPUT = gen.OUTPUT
BACKUP = gen.BACKUP


def finish(img):
    img = img.convert("RGB")
    # 1. mild desaturation, slightly lifted contrast (dull steel/gold palette)
    img = ImageEnhance.Color(img).enhance(0.86)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = gen.crop_to_ratio(img)

    a = np.asarray(img).astype(np.float32)

    # 2. lens vignette
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2.0, h / 2.0
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    vign = np.clip(1.0 - 0.13 * np.clip((r - 0.55) / 0.85, 0, 1) ** 1.6, 0, 1)
    a *= vign[..., None]

    # 3. fine monochrome grain, stronger in the shadows like real sensor noise
    lum = a.mean(axis=2, keepdims=True)
    shadow_weight = np.clip(1.15 - lum / 190.0, 0.45, 1.15)
    rng = np.random.default_rng(20261108)
    noise = rng.normal(0.0, 4.2, size=(h, w, 1)).astype(np.float32)
    a += noise * shadow_weight

    a = np.clip(a, 0, 255).astype(np.uint8)
    return Image.fromarray(a)


def main():
    img = Image.open(RAW)
    print(f"raw: {RAW} size={img.size}")
    out = finish(img)
    size = gen.save_under_cap(out, OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={out.size}  bytes={size}")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    out.save(BACKUP, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Mirrored to {BACKUP}  bytes={os.path.getsize(BACKUP)}")
    print(f"SLUG={SLUG}")


if __name__ == "__main__":
    main()
