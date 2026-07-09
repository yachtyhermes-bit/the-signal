#!/usr/bin/env python3
"""Generate a dark, moody CRDO hero image — purple data center / AI connectivity theme."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, os

W, H = 1200, 675
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ─── 1. Dark gradient background (dark purple/blue tones) ───
for y in range(H):
    t = y / H  # 0 top, 1 bottom
    r = int(10 + t * 6)
    g = int(6 + t * 8)
    b = int(20 + t * 12)
    # Add purple gradient falloff
    purple_intensity = 1.0 - abs(t - 0.5) * 1.2
    purple_intensity = max(0, purple_intensity)
    r += int(8 * purple_intensity)
    g += int(4 * purple_intensity)
    b += int(20 * purple_intensity)
    draw.line([(0, y), (W, y)], fill=(min(r, 255), min(g, 255), min(b, 255)))

# ─── 2. Subtle server rack shapes (abstract silhouettes) ───
rack_color = (25, 20, 45)
rack_accent = (40, 30, 70)
# Left cluster
for i in range(4):
    rx = 50 + i * 85
    ry = 120 + random.randint(0, 30)
    rw = 60
    rh = 380
    # Rack body
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=rack_color, outline=rack_accent, width=1)
    # Server slots (horizontal lines)
    for slot_y in range(ry + 18, ry + rh - 10, 28):
        draw.line([(rx + 6, slot_y), (rx + rw - 6, slot_y)], fill=(35, 28, 55), width=2)
        # Tiny LED dots
        if random.random() > 0.4:
            led_color = (120, 60, 180) if random.random() > 0.3 else (60, 180, 120)
            draw.ellipse([(rx + rw - 14, slot_y - 3), (rx + rw - 8, slot_y + 3)], fill=led_color)

# Right cluster
for i in range(4):
    rx = 700 + i * 85
    ry = 150 + random.randint(0, 40)
    rw = 60
    rh = 350
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=rack_color, outline=rack_accent, width=1)
    for slot_y in range(ry + 18, ry + rh - 10, 28):
        draw.line([(rx + 6, slot_y), (rx + rw - 6, slot_y)], fill=(35, 28, 55), width=2)
        if random.random() > 0.4:
            led_color = (120, 60, 180) if random.random() > 0.3 else (60, 180, 120)
            draw.ellipse([(rx + rw - 14, slot_y - 3), (rx + rw - 8, slot_y + 3)], fill=led_color)

# ─── 3. Glowing purple cables connecting racks ───
def draw_glowing_line(draw, pts, color, width=3, glow_steps=6):
    """Draw a line with outer glow."""
    # Outer glow layers
    for g in range(glow_steps, 0, -1):
        a = max(5, 30 // g)
        gw = width + g * 4
        draw.line(pts, fill=(color[0], color[1], color[2], a), width=gw)
    # Core bright line
    draw.line(pts, fill=color, width=width)

# Cable paths — connecting left racks to right racks
cable_colors = [
    (160, 60, 220),   # bright purple
    (130, 40, 200),   # medium purple
    (180, 80, 240),   # light purple
    (100, 50, 180),   # deep purple
]

for ci in range(12):
    left_rack_x = 80 + random.randint(0, 4) * 85
    right_rack_x = 730 + random.randint(0, 4) * 85
    mid_y = random.randint(200, 500)
    
    # S-curve cable connecting left to right
    ctrl1_x = left_rack_x + 50 + random.randint(0, 60)
    ctrl1_y = mid_y - random.randint(30, 80)
    ctrl2_x = right_rack_x - 50 - random.randint(0, 60)
    ctrl2_y = mid_y + random.randint(30, 80)
    
    # Approximate bezier with line segments
    pts = []
    for t_i in range(0, 21):
        t = t_i / 20
        u = 1 - t
        # Cubic bezier: start → ctrl1 → ctrl2 → end
        x = u**3 * left_rack_x + 3*u**2*t * ctrl1_x + 3*u*t**2 * ctrl2_x + t**3 * right_rack_x
        y = u**3 * mid_y + 3*u**2*t * ctrl1_y + 3*u*t**2 * ctrl2_y + t**3 * mid_y
        pts.append((int(x), int(y)))
    
    color = cable_colors[ci % len(cable_colors)]
    brightness = random.uniform(0.6, 1.0)
    adj_color = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))
    
    if random.random() > 0.2:
        # Glowing cable
        draw_glowing_line(draw, pts, adj_color, width=2, glow_steps=4)
    else:
        # Thin data cable
        draw.line(pts, fill=adj_color, width=1)

# ─── 4. Fiber/data stream particles along cable paths ───
random.seed(42)
for p in range(60):
    # Random position in the connection zone
    x = random.randint(200, 1000)
    y = random.randint(180, 520)
    # Draw as small glowing dots
    r = random.randint(1, 3)
    glow_r = r + 4
    dot_color = (180, 100, 255) if random.random() > 0.3 else (100, 200, 255)
    # Glow
    for gr in range(glow_r, 0, -1):
        alpha_val = max(5, 25 - gr * 3)
        draw.ellipse([x - gr, y - gr, x + gr, y + gr], 
                      fill=(dot_color[0], dot_color[1], dot_color[2], alpha_val))
    draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_color)

# ─── 5. Abstract data flow lines (horizontal) ───
random.seed(99)
for li in range(8):
    y = random.randint(200, 500)
    x_start = random.randint(50, 200)
    x_end = random.randint(900, W - 50)
    alpha = random.randint(15, 40)
    draw.line([(x_start, y), (x_end, y)], fill=(90, 50, 140, alpha), width=1)

# ─── 6. Subtle scan lines / data stream ───
random.seed(123)
for _ in range(200):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    c = random.randint(15, 35)
    img.putpixel((x, y), (c + 8, c + 4, c + 20))

# ─── 7. Vignette (darker edges) ───
cx, cy = W // 2, H // 2
max_dist = math.sqrt(cx**2 + cy**2)
for x in range(W):
    for y in range(H):
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        t = min(1.0, dist / max_dist)
        darken = int(30 * t * t)
        r_px, g_px, b_px = img.getpixel((x, y))
        nr = max(0, r_px - darken)
        ng = max(0, g_px - darken)
        nb = max(0, b_px - darken)
        img.putpixel((x, y), (nr, ng, nb))

# ─── 8. Purple accent glow in center ───
accent_mask = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(accent_mask)
center_x, center_y = W // 2, H // 2
for r in range(250, 0, -8):
    a = max(3, 12 - r // 30)
    ad.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
               fill=(120, 40, 200, a))
img.paste(Image.alpha_composite(img.convert('RGBA'), accent_mask), (0, 0))

# ─── 9. Save ───
out1 = '/home/chino/thesignal/public/img/articles/credo-ai-connectivity-chips-2026.jpg'
os.makedirs(os.path.dirname(out1), exist_ok=True)
img.save(out1, quality=92)
print(f"Generated {out1} ({W}x{H})")

out2 = '/home/chino/thesignal/_backup_dist/img/articles/credo-ai-connectivity-chips-2026.jpg'
os.makedirs(os.path.dirname(out2), exist_ok=True)
img.save(out2, quality=92)
print(f"Copied to {out2}")

# Verify
size1 = os.path.getsize(out1)
size2 = os.path.getsize(out2)
print(f"Size: {out1}: {size1} bytes, {out2}: {size2} bytes")
if size1 >= 10000 and size2 >= 10000:
    print("✅ Both images are >= 10KB")
else:
    print("⚠️  Image size check failed!")
