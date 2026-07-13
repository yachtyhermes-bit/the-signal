#!/usr/bin/env python3
"""Generate a moody SpaceX-themed hero image for The Signal.
Dark navy/purple financial tone, abstract rocket/Starlink/space visualization.
No text, no logos, no model numbers. 1200x675 landscape."""

import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

random.seed(42)

W, H = 1200, 675
OUTPUT = "/home/chino/thesignal/public/img/articles/spcx-spacex-starlink-ipo-analysis-2026.jpg"

# === The Signal brand palette ===
DARK_NAVY = (10, 8, 28)
DARK_PURPLE = (25, 15, 45)
MID_NAVY = (18, 14, 38)
GOLD = (212, 175, 55)
AMBER = (255, 191, 71)
DIM_GOLD = (120, 95, 40)
STAR_BLUE = (100, 140, 220)
TRAIL_PURPLE = (140, 60, 200)
GREEN_GLOW = (60, 200, 120)

# === Helper: draw a gradient ===
def gradient(size, top_color, bottom_color):
    """Vertical linear gradient."""
    base = Image.new('RGB', size, top_color)
    draw = ImageDraw.Draw(base)
    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color
    for y in range(size[1]):
        t = y / size[1]
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    return base

# === Create base image ===
img = gradient((W, H), DARK_NAVY, DARK_PURPLE)
draw = ImageDraw.Draw(img)

# === 1. Starfield ===
random.seed(99)
stars = []
for _ in range(300):
    x = random.randint(0, W - 1)
    y = random.randint(0, int(H * 0.6))
    r = random.choice([1, 1, 1, 2])
    b = random.randint(150, 255)
    stars.append((x, y, r, b))

# Add some brighter stars
for _ in range(40):
    x = random.randint(0, W - 1)
    y = random.randint(0, int(H * 0.5))
    r = random.randint(2, 3)
    stars.append((x, y, r, 255))

for x, y, r, b in stars:
    alpha = random.randint(80, 255)
    color = (b, b, b) if b > 200 else (b // 2, b // 2, b)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color + (alpha,))

# === 2. Starlink Constellation ===
# Create satellite constellation with connecting lines
constellation_points = []
random.seed(42)
cx, cy = W * 0.6, H * 0.28

# Generate constellation nodes in a web pattern
for i in range(60):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(30, 250) * (0.5 + 0.5 * random.random())
    x = cx + dist * math.cos(angle) + random.uniform(-40, 40)
    y = cy + dist * math.sin(angle) * 0.5 + random.uniform(-20, 20)  # Flatten vertically
    if 50 < x < W - 50 and 20 < y < H * 0.55:
        constellation_points.append((int(x), int(y)))

# Connect nearby nodes
for i, (x1, y1) in enumerate(constellation_points):
    for j, (x2, y2) in enumerate(constellation_points):
        if j <= i:
            continue
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if dist < 60:
            opacity = max(0, int(60 * (1 - dist / 60)))
            draw.line([(x1, y1), (x2, y2)],
                      fill=(STAR_BLUE[0], STAR_BLUE[1], STAR_BLUE[2], opacity),
                      width=1)

# Draw constellation nodes
for x, y in constellation_points:
    draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=STAR_BLUE + (220,))
    draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(200, 220, 255))

# === 3. Rocket trail (ascending line with glow) ===
trail_points = []
start_x, start_y = W * 0.5, H * 0.65
end_x, end_y = W * 0.55, H * 0.15

for t_int in range(100):
    t = t_int / 100
    x = start_x + (end_x - start_x) * t
    y = start_y + (end_y - start_y) * t
    # Add some wobble
    wobble = 12 * math.sin(t * 8) * (1 - t * 0.5)
    x += wobble
    trail_points.append((int(x), int(y)))

# Draw glow trail (thick to thin)
for i, (x, y) in enumerate(trail_points):
    t = i / len(trail_points)
    width = max(1, int(12 * (1 - t * 0.7)))
    alpha = int(200 * (1 - t * 0.4))
    # Multi-layer glow
    for g in range(3):
        gw = width + g * 6
        opacity = max(0, alpha - g * 50)
        r = int(TRAIL_PURPLE[0] * (1 - t * 0.3) + GOLD[0] * t * 0.3)
        g_c = int(TRAIL_PURPLE[1] * (1 - t * 0.5) + GOLD[1] * t * 0.5)
        b = int(TRAIL_PURPLE[2] * (1 - t * 0.7) + GOLD[2] * t * 0.7)
        draw.ellipse([x - gw, y - gw, x + gw, y + gw],
                     fill=(r, g_c, b, opacity))

# === 4. Launch pad silhouette (bottom) ===
pad_color = (15, 12, 35)
pad_light = (40, 35, 60)

# Main structure
draw.polygon([
    (0, H),
    (0, H - 80),
    (400, H - 120),
    (500, H - 100),
    (800, H - 100),
    (900, H - 120),
    (1200, H - 80),
    (1200, H),
], fill=pad_color)

# Tower structure
draw.rectangle([440, H - 180, 460, H - 100], fill=pad_light)
draw.rectangle([740, H - 160, 755, H - 100], fill=pad_light)

# Horizontal beams
draw.rectangle([420, H - 130, 480, H - 118], fill=GOLD if random.random() > 0.5 else pad_light)
draw.rectangle([720, H - 125, 775, H - 113], fill=GOLD if random.random() > 0.5 else pad_light)

# === 5. Grid lines (financial chart feel) ===
grid_color = (40, 35, 60, 60)
for y in range(0, H, 60):
    draw.line([(0, y), (W, y)], fill=grid_color, width=1)
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=grid_color, width=1)

# === 6. Financial chart line (ascending, gold) ===
chart_points = []
random.seed(7)
chart_y = H * 0.65
for x in range(0, W, 2):
    t = x / W
    base = chart_y - t * H * 0.4
    noise = 15 * math.sin(x * 0.03) + 8 * math.sin(x * 0.07) + 5 * math.sin(x * 0.13)
    y = base + noise
    chart_points.append((x, int(y)))

# Draw chart with glow
for i in range(len(chart_points) - 1):
    x1, y1 = chart_points[i]
    x2, y2 = chart_points[i + 1]
    # Outer glow
    draw.line([(x1, y1 - 2), (x2, y2 - 2)], fill=(GOLD[0]//3, GOLD[1]//3, GOLD[2]//3), width=3)
    draw.line([(x1, y1 + 2), (x2, y2 + 2)], fill=(GOLD[0]//3, GOLD[1]//3, GOLD[2]//3), width=3)
    # Main line
    draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)

# Area fill under chart
for x in range(0, W - 2, 2):
    y = chart_points[x // 2][1]
    draw.line([(x, y), (x, H)], fill=(GOLD[0]//8, GOLD[1]//8, GOLD[2]//8, 40), width=2)

# === 7. Amber accent glow spots ===
random.seed(12)
for _ in range(6):
    x = random.randint(100, W - 100)
    y = random.randint(int(H * 0.3), int(H * 0.8))
    r = random.randint(20, 50)
    for g in range(3):
        gr = r + g * 15
        alpha = max(0, 25 - g * 8)
        draw.ellipse([x - gr, y - gr, x + gr, y + gr],
                     fill=(AMBER[0]//3, AMBER[1]//3, AMBER[2]//3, alpha))

# === 8. Bottom vignette ===
vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for y in range(H - 100, H):
    t = (y - (H - 100)) / 100
    alpha = int(180 * t)
    vd.rectangle([(0, y), (W, y)], fill=(0, 0, 0, alpha))

img = Image.alpha_composite(img.convert('RGBA'), vignette).convert('RGB')
draw = ImageDraw.Draw(img)

# === 9. Soft blur for atmosphere ===
img = img.filter(ImageFilter.GaussianBlur(radius=1.5))

# Re-draw sharp elements over the blur
draw = ImageDraw.Draw(img)

# Re-draw chart line sharp
for i in range(len(chart_points) - 1):
    x1, y1 = chart_points[i]
    x2, y2 = chart_points[i + 1]
    draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)

# Re-draw constellation sharp
for x, y in constellation_points:
    draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(180, 200, 255))
    draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(220, 235, 255))

# Re-draw trail center
for i, (x, y) in enumerate(trail_points):
    t = i / len(trail_points)
    width = max(1, int(3 * (1 - t * 0.6)))
    draw.ellipse([x - width, y - width, x + width, y + width],
                 fill=(TRAIL_PURPLE[0], TRAIL_PURPLE[1], TRAIL_PURPLE[2]))

# === 10. Final polish - subtle brightness boost ===
from PIL import ImageEnhance
img = ImageEnhance.Contrast(img).enhance(1.15)
img = ImageEnhance.Color(img).enhance(1.1)

# === Save ===
img.save(OUTPUT, 'JPEG', quality=92, optimize=True)
print(f"✅ Saved hero image to {OUTPUT}")
print(f"   Size: {img.size}")
