#!/usr/bin/env python3
"""Better heroes for two articles, via fal flux/schnell.

amzn-nvidia-chip-sale-leaseback-2026 — $8B of Nvidia Grace Blackwell chips moved into an
investor-funded vehicle and leased back. The old hero was a flat bench-top product shot with
legible "10 10 10" port markings. New: a wide, low-key hyperscale data hall — the asset at
the scale the number implies, and the environment a leased asset actually sits in.

smci-export-control-guilty-plea-2026 — a contractor pleaded guilty to diverting ~$2.5B of
Nvidia-powered AI servers to China. The old hero had painterly wood grain, an unnatural
cable coil and a fake red logo placeholder. New: a dim warehouse at night, an open export
crate holding a rack server, unmarked transit cases receding into shadow. Deliberately zero
markings — container/port scenes generate garbled lettering, so no containers and no signage.

Both: NO people, NO hands, NO text/lettering/numbers/logos, NO neon, photorealistic only.
"""
import os
import sys
import requests
from PIL import Image

OUTDIR = "/home/chino/thesignal/public/img/articles"
BACKUP_DIR = "/home/chino/thesignal/_backup_dist/img/articles"
W, H = 1440, 810
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every surface is deliberately free of legible writing: no readable words, no letters, "
    "no numbers, no symbols, no logos, no branding, no watermarks, no signage, no flags, "
    "no placards, no labels, no stickers, no adhesive tags, no paper slips, no stencilled "
    "markings, no crate stamps, no markings of any kind on any case or rack. "
    "No people, no hands, no faces, no human figures, no silhouettes, no workers. "
    "No neon lights, no synthwave, no glowing laser lines, no digital fantasy effects, no 3D render sheen. "
    "Real location photography with genuine real-world imperfections, asymmetry and wear — "
    "not CGI, not a 3D render, not a showroom, not a flawless computer-generated visualisation."
)

HEROES = {
    "amzn-nvidia-chip-sale-leaseback-2026": (
        20261020,
        "Documentary photograph shot on 35mm film inside a working data hall at night. The camera "
        "is close in and slightly off-axis, hand-held: a single rack-height drawer of AI "
        "accelerator compute trays is slid out on its rails at the left of frame, its cooling "
        "fans, dense circuit boards and copper heat pipes catching a hard cool light, while the "
        "long aisle of racks behind falls away into blurred darkness on the right. Cool "
        "blue-white light rakes across brushed metal and matte black plastic; a tangle of black "
        "fibre-optic cords loops down loosely from the open drawer. The floor is bare scuffed "
        "concrete with dust, tape residue and a coiled unused cable lying where someone left it. "
        "Visible 35mm film grain, slight colour shift, natural lens vignette, imperfect focus, "
        "dust in the air, no symmetry, unbalanced casual framing as if taken quickly by a "
        "passing technician. Deep saturated navy and charcoal shadows with cool cyan highlights "
        "and a single warm amber pool of light far in the background. Real photograph, not CGI, "
        "not a rendered visualisation. 16:9 landscape aspect ratio. " + NO_TEXT
    ),
    "smci-export-control-guilty-plea-2026": (
        20261030,
        "Documentary photograph shot on 35mm film inside a dim freight warehouse late at night. "
        "Shot hand-held from slightly above and to one side: a rack-mount AI server chassis sits "
        "alone on a scuffed wooden pallet at the left of frame, a lid of grey foam padding folded "
        "back and its rows of cooling fans and blank drive bays facing the light. The pallet's "
        "bare plywood and the surrounding floor are completely plain and unbroken — no panel, no "
        "plate, no rectangle of lighter colour, no paper, no tape, no printed mark of any kind. "
        "One hard industrial lamp rakes in from the upper left, throwing the right half of the "
        "frame into deep shadow, where tiers of bare rusted steel shelving and a loose stack of "
        "plain wooden pallets disappear into blackness. Fine sawdust and a few wood offcuts lie "
        "on stained concrete marked with worn tape. Deep charcoal and cold steel tones against "
        "one warm amber pool of light. Visible 35mm film grain, slight colour shift, natural "
        "lens vignette, imperfect focus, casual unbalanced framing, obvious real-world wear and "
        "grime. Real photograph, not CGI, not a rendered visualisation. 16:9 landscape aspect "
        "ratio. " + NO_TEXT
    ),
}


def load_fal_key():
    env_path = "/home/chino/hermes-workspace/studio-api/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FAL_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["FAL_KEY"] = key
                    return key
    real_path = "/home/chino/video_output/.fal_real"
    if os.path.exists(real_path):
        with open(real_path) as f:
            raw = f.read().strip().split("\n")[0]
            key = raw.split("|", 1)[1] if "|" in raw else raw
            if key:
                os.environ["FAL_KEY"] = key
                return key
    return os.environ.get("FAL_KEY")


def cover_resize(img, tw, th):
    """Scale to cover the target box, then centre-crop. Never stretches."""
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def main():
    import fal_client
    if not load_fal_key():
        print("ERROR: FAL_KEY not found")
        sys.exit(1)

    failures = []
    only = sys.argv[1:]
    for slug, (seed, prompt) in HEROES.items():
        if only and slug not in only:
            continue
        out = f"{OUTDIR}/{slug}.jpg"
        print(f"\n=== {slug}")
        try:
            result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
                "prompt": prompt,
                "image_size": {"width": W, "height": H},
                "num_inference_steps": 4,
                "enable_safety_checker": False,
                "seed": seed,
            })
            url = None
            if result.get("images"):
                url = result["images"][0]["url"]
            elif result.get("image"):
                url = result["image"]
            if not url:
                failures.append((slug, f"no image url: {result}"))
                continue

            r = requests.get(url, timeout=90)
            r.raise_for_status()
            os.makedirs(OUTDIR, exist_ok=True)
            tmp = out + ".raw"
            with open(tmp, "wb") as f:
                f.write(r.content)

            img = Image.open(tmp)
            print(f"  fal returned {img.size} {len(r.content)} bytes")
            final = cover_resize(img.convert("RGB"), FINAL_W, FINAL_H)
            final.save(out, "JPEG", quality=92)
            os.unlink(tmp)
            os.makedirs(BACKUP_DIR, exist_ok=True)
            final.save(f"{BACKUP_DIR}/{slug}.jpg", "JPEG", quality=92)
            print(f"  wrote {out} {final.size} {os.path.getsize(out)} bytes (centre-cropped, not stretched)")
        except Exception as e:
            failures.append((slug, repr(e)))

    print()
    if failures:
        for s, e in failures:
            print(f"FAILED {s}: {e}")
        sys.exit(1)
    print("Done! All heroes regenerated.")


if __name__ == "__main__":
    main()
