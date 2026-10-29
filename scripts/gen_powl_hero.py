#!/usr/bin/env python3
"""Generate photo-realistic hero image for Powell Industries switchgear article."""
import os
import io
import sys
import requests
import fal_client
from PIL import Image

SLUG = 'powl-electrical-switchgear-backlog-ai-power-2026'
ENV_PATH = '/home/chino/hermes-workspace/studio-api/.env'
OUT1 = f'/home/chino/thesignal/public/img/articles/{SLUG}.jpg'
OUT2 = f'/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg'


def load_fal_key():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line.startswith('FAL_KEY='):
                val = line.split('=', 1)[1].strip().strip('"').strip("'")
                return val
    raise SystemExit('FAL_KEY not found')


PROMPT = (
    "Photo-realistic editorial stock photograph of a large industrial electrical "
    "switchgear manufacturing facility. Wide interior view of an expansive, clean, "
    "well-lit factory floor where technicians in hard hats and high-visibility safety "
    "vests assemble massive gray steel low-voltage and medium-voltage electrical "
    "switchgear enclosures and power control rooms. Rows of tall metal electrical "
    "cabinets, exposed copper bus bars, heavy industrial circuit breakers, cable "
    "trays and steel structural framing. A technician kneeling with a torque wrench "
    "tightening bolted busbar connections inside an open switchgear section. Natural "
    "industrial daylight from high clerestory windows, realistic metal textures, "
    "authentic manufacturing atmosphere, shallow depth of field, 35mm documentary "
    "photography, high detail. Real industrial equipment only. No text, no labels, "
    "no logos, no readable writing anywhere. Not a data center, no server racks, no "
    "blinking LEDs, no glowing neon lines, no digital or abstract graphics."
)


def generate():
    os.environ['FAL_KEY'] = load_fal_key()
    print('Generating via fal flux/schnell ...')
    result = fal_client.subscribe(
        'fal-ai/flux/schnell',
        arguments={
            'prompt': PROMPT,
            'image_size': {'width': 1440, 'height': 810},
            'num_inference_steps': 4,
            'num_images': 1,
            'enable_safety_checker': False,
        },
    )
    url = result['images'][0]['url']
    print('Generated:', url)
    data = requests.get(url, timeout=120).content
    img = Image.open(io.BytesIO(data)).convert('RGB')
    print('Raw size:', img.size)

    # Center-crop to 16:9 already (1440x810), then resize to 1920x1080 LANCZOS
    target_ratio = 1920 / 1080
    w, h = img.size
    cur = w / h
    if cur > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((1920, 1080), Image.LANCZOS)

    for out in (OUT1, OUT2):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img.save(out, 'JPEG', quality=90, optimize=True)
        print('Saved:', out, img.size, os.path.getsize(out), 'bytes')
    return OUT1


if __name__ == '__main__':
    generate()
