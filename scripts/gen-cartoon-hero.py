#!/usr/bin/env python3
"""Generate an editorial-cartoon hero for The Signal (fal flux/schnell).

Why: the photo heroes are wire-service realism. Some stories land harder as a
single-panel newspaper cartoon (ink + watercolour caricature). This script is
the cartoon lane, kept separate from gen-*-hero.py so the default stays
photo-real.

Usage:
  SLUG=cartoon-test \
  SUBJECT="a grinning founder in a hard hat sprinting toward a half-built building" \
  LABEL="xAI" \
  /home/chino/video-venv/bin/python3 scripts/gen-cartoon-hero.py

Env:
  SLUG      required, output file name (public/img/articles/<slug>.jpg)
  SUBJECT   required, one or two sentences describing the scene
  LABEL     optional, ONE short word painted on a sign (xAI, OpenAI, Nvidia).
            Anything longer garbles. Omit for a sign-free scene.
  DETAILS   optional, background/foreground extras
  SEED      optional int for a different take on the same idea
  UPLOAD_R2 set to 1 to mirror to R2 as the live hero
  DRY_RUN   set to 1 to print the prompt and exit

Rules baked in: no real names (models refuse public figures, and "billionaire
founder with swept-back hair" reads the same), one sign only, 16:9, JPEG under
400KB, mirror to _backup_dist.
"""
import os
import subprocess
import sys

import requests
from PIL import Image

W, H = 1536, 864
MAX_BYTES = 400_000
OUT_DIR = "/home/chino/thesignal/public/img/articles"
BACKUP_DIR = "/home/chino/thesignal/_backup_dist/img/articles"

STYLE = (
    "Single-panel satirical editorial newspaper cartoon, hand-drawn ink "
    "linework with loose watercolour wash, muted palette of concrete grey, "
    "rust orange, dusty blue and cream paper. Exaggerated caricature "
    "proportions, big heads, expressive hands, sketchy cross-hatching for "
    "shadow, slight paper texture. No photorealism, no 3D render, no neon, "
    "no glowing lines, no digital-art sheen."
)


def load_fal_key():
    for path in ("/home/chino/hermes-workspace/studio-api/.env",
                 "/home/chino/video_output/.fal_real"):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        os.environ["FAL_KEY"] = key
                        return key
                if path.endswith(".fal_real") and line.strip():
                    raw = line.strip()
                    key = raw.split("|", 1)[1] if "|" in raw else raw
                    os.environ["FAL_KEY"] = key
                    return key
    return os.environ.get("FAL_KEY")


def build_prompt(subject, label, details):
    parts = [STYLE, subject.strip().rstrip(".") + "."]
    if details:
        parts.append(details.strip().rstrip(".") + ".")
    if label:
        word = label.strip()
        spelled = " ".join(word)
        parts.append(
            'A single crooked sign on the building carries exactly the %d '
            'characters "%s" (%s) and nothing else — large, clean, correctly '
            "spelled, no doubled or extra letters." % (len(word), word, spelled)
        )
    else:
        parts.append("No text, no lettering, no signage anywhere in the image.")
    parts.append(
        "Wide 16:9 composition, the running figure or central subject as the "
        "clear focal point, onlookers reacting in the foreground. "
        "Absolutely no artist signature, no initials, no stamp, no logo and no "
        "handwritten marks in any corner — the paper margins stay blank. No "
        "watermark, no caption, no border text."
    )
    return "\n\n".join(parts)


def normalize(img):
    w, h = img.size
    target = W / H
    cur = w / h
    if abs(cur - target) > 1e-3:
        if cur > target:
            new_w = int(h * target)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
    img = img.convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img


def save_capped(img, path):
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74, 72):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print("Saved %s q=%d bytes=%d" % (path, q, size))
            return size
    print("WARN: %s still %d bytes at q=72" % (path, os.path.getsize(path)))
    return os.path.getsize(path)


def generate(prompt, out_path, seed=None):
    import fal_client

    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    if seed is not None:
        args["seed"] = int(seed)
    print("Generating cartoon with fal flux/schnell...")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
    url = (result.get("images") or [{}])[0].get("url")
    if not url:
        print("ERROR: no image URL in result: %s" % result)
        sys.exit(1)
    print("Image URL: %s" % url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: %s size=%s bytes=%d" % (out_path, img.size, len(r.content)))
    return img


def main():
    slug = os.environ.get("SLUG", "").strip()
    subject = os.environ.get("SUBJECT", "").strip()
    label = os.environ.get("LABEL", "").strip()
    details = os.environ.get("DETAILS", "").strip()
    seed = os.environ.get("SEED") or None
    if not slug or not subject:
        print("ERROR: SLUG and SUBJECT are required (see docstring)")
        sys.exit(1)
    prompt = build_prompt(subject, label, details)
    if os.environ.get("DRY_RUN") == "1":
        print(prompt)
        return
    out = os.path.join(OUT_DIR, slug + ".jpg")
    backup = os.path.join(BACKUP_DIR, slug + ".jpg")
    img = generate(prompt, out, seed)
    img = normalize(img)
    save_capped(img, out)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    save_capped(img, backup)
    print("VERIFY %s dims=%dx%d bytes=%d" % (out, W, H, os.path.getsize(out)))
    if os.environ.get("UPLOAD_R2") == "1":
        rc = subprocess.call(
            [sys.executable, "/home/chino/thesignal/scripts/r2_upload.py",
             "hero", slug]
        )
        print("R2 upload rc=%d" % rc)
        if rc != 0:
            sys.exit(rc)


if __name__ == "__main__":
    main()
