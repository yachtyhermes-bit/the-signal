#!/usr/bin/env python3
"""Generate a vibrant blue stock chart hero background for Signal vs. The Street.
Matches the reference: bright blue BG, prominent white candlesticks, grid, volume bars."""
import math, random, os
from PIL import Image, ImageDraw

W, H = 1920, 1080
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ── 1. Blue gradient background ──
# Top: vibrant medium blue → bottom: deep blue
for y in range(H):
    t = y / H
    r = int(10 + t * 5)
    g = int(40 + t * 20)
    b = int(100 + t * 30)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 2. Grid lines ──
grid = (35, 65, 120)
# Horizontal
for y in range(0, H, 50):
    draw.line([(0, y), (W, y)], fill=grid, width=1)
# Vertical
for x in range(0, W, 60):
    draw.line([(x, 0), (x, H)], fill=grid, width=1)

# ── 3. Moving average / trend lines ──
def smooth_curve(seed, start_y, segments, amp):
    random.seed(seed)
    pts = [(0, start_y)]
    x = 0
    y = start_y
    seg_w = W // segments
    for i in range(segments):
        x += seg_w + random.randint(-15, 15)
        dy = random.randint(-amp, amp)
        y += dy
        y = max(H//3, min(H - 80, y))
        pts.append((x, y))
    return pts

# Blue trend line (thick, like a moving average)
pts_ma = smooth_curve(42, H - 350, 30, 30)
for w in range(12, 4, -2):
    draw.line(pts_ma, fill=(80, 180, 255, 40 // ((12-w)//2+1)), width=w)
draw.line(pts_ma, fill=(100, 200, 255), width=4)

# Green/teal trend line (second MA)
pts_ma2 = smooth_curve(17, H - 280, 30, 20)
for w in range(10, 3, -2):
    draw.line(pts_ma2, fill=(60, 200, 120, 30 // ((10-w)//2+1)), width=w)
draw.line(pts_ma2, fill=(80, 230, 140), width=3)

# ── 4. Candlesticks ──
random.seed(99)
for i in range(90):
    cx = random.randint(60, W - 60)
    cy = random.randint(80, H - 120)
    body_h = random.randint(8, 28)
    body_w = random.randint(5, 12)
    wick_top = random.randint(5, 18)
    wick_bot = random.randint(5, 18)
    is_up = random.choice([True, False])

    # Wick
    draw.line([(cx, cy - wick_top), (cx, cy + body_h + wick_bot)],
              fill=(180, 210, 255), width=2)

    # Body
    if is_up:
        # Green/white candlestick (bullish)
        body_color = (0, 200, 100)
    else:
        # Red/rose candlestick (bearish)
        body_color = (200, 60, 60)
    
    draw.rectangle([cx - body_w//2, cy, cx + body_w//2, cy + body_h],
                   fill=body_color, outline=(220, 230, 255))

# ── 5. Volume bars at bottom ──
random.seed(200)
vol_base_y = H - 40
for i in range(160):
    vx = 20 + i * 12
    vh = random.randint(8, 60)
    is_green = random.choice([True, False])
    vol_color = (0, 180, 90, 100) if is_green else (180, 50, 50, 100)
    bar_color = (0, 200, 100) if is_green else (200, 60, 60)
    # Filled rectangle for volume
    draw.rectangle([vx, vol_base_y - vh, vx + 8, vol_base_y],
                   fill=bar_color)

# ── 6. Scan line / data noise overlay ──
random.seed(55)
for _ in range(200):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    intensity = random.randint(30, 60)
    img.putpixel((x, y), (intensity, intensity + 10, intensity + 30))

# ── 7. Soft vignette ──
cx, cy = W // 2, H // 2
max_dist = math.sqrt(cx**2 + cy**2)
for x in range(W):
    for y in range(H):
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        t = min(1.0, dist / max_dist)
        darken = int(18 * t * t)
        r, g, b = img.getpixel((x, y))
        img.putpixel((x, y), (max(0, r - darken), max(0, g - darken), max(0, b - darken)))

# Save
out = '/home/chino/thesignal/public/img/svs-hero-bg.jpg'
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, quality=95)
print(f"Generated {out} ({W}x{H})")
