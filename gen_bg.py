#!/usr/bin/env python3
"""Generate a dark, professional financial hero background for Signal vs. The Street."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, os

W, H = 1920, 1080
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# --- 1. Dark gradient background ---
# Top: #08080e (very dark), bottom: #0d1117 (slightly lighter dark blue-gray)
for y in range(H):
    t = y / H  # 0 top, 1 bottom
    r = int(8 + t * 5)
    g = int(8 + t * 9)
    b = int(14 + t * 9)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- 2. Subtle grid lines ---
grid_color = (30, 40, 60, 30)  # very subtle
# Horizontal grid lines
for y in range(0, H, 60):
    draw.line([(0, y), (W, y)], fill=(20, 28, 46), width=1)
# Vertical grid lines
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=(20, 28, 46), width=1)

# --- 3. Abstract stock chart (line chart) ---
# Generate a realistic-looking stock chart path
def generate_chart_points(start_x, start_y, segments, amp, seed=42):
    random.seed(seed)
    points = [(start_x, start_y)]
    x = start_x
    y = start_y
    for i in range(segments):
        dx = W // segments + random.randint(-20, 20)
        x += dx
        # Random walk with upward bias
        dy = random.randint(-amp, amp)
        y += dy
        # Keep within bounds
        y = max(60, min(H - 60, y))
        points.append((x, y))
    return points

# Main chart line (SIGNAL portfolio)
pts1 = generate_chart_points(50, H - 300, 24, 35, seed=42)
# SPY comparison line (flatter)
pts2 = generate_chart_points(50, H - 250, 24, 20, seed=7)

# Draw the chart area (subtle filled shape under the line)
def draw_chart_fill(draw, points, color, H):
    poly = points + [(points[-1][0], H - 20), (points[0][0], H - 20)]
    draw.polygon(poly, fill=color)

# Glow/fill under signal line
fill_color = (59, 130, 246, 20)  # blue with low opacity
draw_chart_fill(draw, pts1, (10, 22, 50), H)

# Draw the lines (thicker glow + thin line)
def draw_chart_line(draw, points, color, width, glow=False):
    if glow:
        # Draw glow (wider, more transparent)
        for w in range(width + 6, width + 16, 2):
            draw.line(points, fill=(color[0], color[1], color[2], 15), width=w)
    draw.line(points, fill=color, width=width)

# Signal line - blue glow
draw_chart_line(draw, pts1, (59, 130, 246), 3, glow=True)
# SPY line - subtle green-gray
draw_chart_line(draw, pts2, (74, 168, 120), 2, glow=True)

# --- 4. Abstract candlestick patterns (subtle) ---
random.seed(99)
for i in range(15):
    cx = random.randint(100, W - 100)
    cy = random.randint(100, H - 150)
    h = random.randint(10, 35)
    w = random.randint(4, 10)
    # Wick
    draw.line([(cx, cy - h//2 - 5), (cx, cy + h//2 + 5)], 
              fill=(30, 50, 80), width=1)
    # Body (up or down)
    is_up = random.choice([True, False])
    body_color = (0, 120, 60) if is_up else (120, 30, 30)
    draw.rectangle([cx - w//2, cy - h//4, cx + w//2, cy + h//4], 
                   fill=body_color)

# --- 5. Subtle scan line / data stream effect ---
random.seed(123)
for _ in range(120):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    c = random.randint(20, 45)
    img.putpixel((x, y), (c, c + 5, c + 10))

# --- 6. Vignette (darker edges) ---
vignette = Image.new('RGB', (W, H))
vd = ImageDraw.Draw(vignette)
# radial gradient for vignette
cx, cy = W // 2, H // 2
max_dist = math.sqrt(cx**2 + cy**2)
for x in range(W):
    for y in range(H):
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        t = min(1.0, dist / max_dist)
        # Darker at edges
        darken = int(25 * t * t)
        r, g, b = img.getpixel((x, y))
        nr = max(0, r - darken)
        ng = max(0, g - darken)
        nb = max(0, b - darken)
        img.putpixel((x, y), (nr, ng, nb))

# --- 7. Subtle brand gradient accent at top ---
accent = Image.new('RGBA', (W, 3))
ad = ImageDraw.Draw(accent)
for x in range(W):
    t = x / W
    r = int(59 + t * (167 - 59))
    g = int(130 + t * (139 - 130))
    b = int(246 + t * (250 - 246))
    ad.line([(x, 0), (x, 2)], fill=(r, g, b, 60))
img.paste(accent, (0, 0), accent)

# Save
out = '/home/chino/thesignal/public/img/svs-hero-bg.jpg'
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, quality=92)
print(f"Generated {out} ({W}x{H})")

# Also copy to backup
backup = '/home/chino/thesignal/_backup_dist/img/svs-hero-bg.jpg'
os.makedirs(os.path.dirname(backup), exist_ok=True)
img.save(backup, quality=92)
print(f"Copied to {backup}")
