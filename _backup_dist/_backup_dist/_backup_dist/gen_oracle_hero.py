#!/usr/bin/env python3
"""Generate a dark, moody Oracle (ORCL) hero image — red data center / cloud infra aesthetic."""
from PIL import Image, ImageDraw, ImageFilter
import math, random, os

W, H = 1200, 675
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ─── 1. Dark gradient background (deep crimson/charcoal tones) ───
for y in range(H):
    t = y / H  # 0 top, 1 bottom
    r = int(8 + t * 10)
    g = int(6 + t * 8)
    b = int(8 + t * 10)
    # Red accent gradient in center
    red_intensity = 1.0 - abs(t - 0.4) * 1.4
    red_intensity = max(0, red_intensity)
    r += int(18 * red_intensity)
    g += int(4 * red_intensity)
    b += int(3 * red_intensity)
    draw.line([(0, y), (W, y)], fill=(min(r, 255), min(g, 255), min(b, 255)))

# ─── 2. Server rack shapes (abstract silhouettes) ───
rack_color = (22, 18, 20)
rack_accent = (40, 28, 30)

# Left cluster
for i in range(4):
    rx = 40 + i * 90
    ry = 100 + random.randint(0, 30)
    rw = 65
    rh = 400
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=rack_color, outline=rack_accent, width=1)
    # Server slots (horizontal lines)
    for slot_y in range(ry + 18, ry + rh - 10, 28):
        draw.line([(rx + 6, slot_y), (rx + rw - 6, slot_y)], fill=(35, 28, 30), width=2)
        # Tiny LED dots — Oracle red
        if random.random() > 0.35:
            led_color = (220, 40, 30) if random.random() > 0.3 else (200, 80, 20)
            draw.ellipse([(rx + rw - 14, slot_y - 3), (rx + rw - 8, slot_y + 3)], fill=led_color)

# Center cluster
for i in range(4):
    rx = 460 + i * 75
    ry = 120 + random.randint(0, 25)
    rw = 60
    rh = 420
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=rack_color, outline=rack_accent, width=1)
    for slot_y in range(ry + 18, ry + rh - 10, 28):
        draw.line([(rx + 6, slot_y), (rx + rw - 6, slot_y)], fill=(35, 28, 30), width=2)
        if random.random() > 0.35:
            led_color = (220, 40, 30) if random.random() > 0.3 else (200, 80, 20)
            draw.ellipse([(rx + rw - 14, slot_y - 3), (rx + rw - 8, slot_y + 3)], fill=led_color)

# Right cluster
for i in range(4):
    rx = 780 + i * 85
    ry = 110 + random.randint(0, 35)
    rw = 60
    rh = 390
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=rack_color, outline=rack_accent, width=1)
    for slot_y in range(ry + 18, ry + rh - 10, 28):
        draw.line([(rx + 6, slot_y), (rx + rw - 6, slot_y)], fill=(35, 28, 30), width=2)
        if random.random() > 0.35:
            led_color = (220, 40, 30) if random.random() > 0.3 else (200, 80, 20)
            draw.ellipse([(rx + rw - 14, slot_y - 3), (rx + rw - 8, slot_y + 3)], fill=led_color)

# ─── 3. Glowing red/orange cables connecting racks ───
def draw_glowing_line(draw, pts, color, width=3, glow_steps=6):
    """Draw a line with outer glow."""
    for g in range(glow_steps, 0, -1):
        a = max(5, 30 // g)
        gw = width + g * 3
        draw.line(pts, fill=(color[0], color[1], color[2], a), width=gw)
    draw.line(pts, fill=color, width=width)

cable_colors = [
    (220, 45, 30),    # bright Oracle red
    (200, 60, 25),    # orange-red
    (180, 35, 20),    # deep red
    (230, 80, 40),    # warm red-orange
]

for ci in range(14):
    # Pick racks from different clusters
    src_cluster = random.choice([(40, 380), (460, 740), (780, 1060)])
    dst_cluster = random.choice([(40, 380), (460, 740), (780, 1060)])
    left_rack_x = random.randint(src_cluster[0], src_cluster[1])
    right_rack_x = random.randint(dst_cluster[0], dst_cluster[1])
    if right_rack_x < left_rack_x:
        left_rack_x, right_rack_x = right_rack_x, left_rack_x
    mid_y = random.randint(200, 500)
    
    ctrl1_x = left_rack_x + 50 + random.randint(0, 60)
    ctrl1_y = mid_y - random.randint(30, 80)
    ctrl2_x = right_rack_x - 50 - random.randint(0, 60)
    ctrl2_y = mid_y + random.randint(30, 80)
    
    pts = []
    for t_i in range(0, 21):
        t = t_i / 20
        u = 1 - t
        x = u**3 * left_rack_x + 3*u**2*t * ctrl1_x + 3*u*t**2 * ctrl2_x + t**3 * right_rack_x
        y = u**3 * mid_y + 3*u**2*t * ctrl1_y + 3*u*t**2 * ctrl2_y + t**3 * mid_y
        pts.append((int(x), int(y)))
    
    color = cable_colors[ci % len(cable_colors)]
    brightness = random.uniform(0.6, 1.0)
    adj_color = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))
    
    if random.random() > 0.2:
        draw_glowing_line(draw, pts, adj_color, width=2, glow_steps=4)
    else:
        draw.line(pts, fill=adj_color, width=1)

# ─── 4. Fiber/data stream particles ───
random.seed(42)
for p in range(70):
    x = random.randint(100, 1100)
    y = random.randint(150, 550)
    r = random.randint(1, 3)
    glow_r = r + 4
    dot_color = (255, 80, 50) if random.random() > 0.3 else (200, 120, 40)
    for gr in range(glow_r, 0, -1):
        alpha_val = max(5, 25 - gr * 3)
        draw.ellipse([x - gr, y - gr, x + gr, y + gr],
                      fill=(dot_color[0], dot_color[1], dot_color[2], alpha_val))
    draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_color)

# ─── 5. Abstract data flow lines (horizontal, red-tinted) ───
random.seed(99)
for li in range(10):
    y = random.randint(180, 520)
    x_start = random.randint(50, 200)
    x_end = random.randint(900, W - 50)
    alpha = random.randint(12, 35)
    draw.line([(x_start, y), (x_end, y)], fill=(180, 40, 30, alpha), width=1)

# ─── 6. Subtle scan lines / data stream ───
random.seed(123)
for _ in range(250):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    c = random.randint(12, 30)
    img.putpixel((x, y), (c + 10, c + 3, c + 5))

# ─── 7. Vignette (darker edges) ───
cx, cy = W // 2, H // 2
max_dist = math.sqrt(cx**2 + cy**2)
for x in range(W):
    for y in range(H):
        dist = math.sqrt((x - cx)**2 + (y - cy)**2)
        t = min(1.0, dist / max_dist)
        darken = int(35 * t * t)
        r_px, g_px, b_px = img.getpixel((x, y))
        nr = max(0, r_px - darken)
        ng = max(0, g_px - darken)
        nb = max(0, b_px - darken)
        img.putpixel((x, y), (nr, ng, nb))

# ─── 8. Oracle red accent glow in center ───
accent_mask = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(accent_mask)
center_x, center_y = W // 2, H // 2
for r in range(280, 0, -8):
    a = max(3, 10 - r // 35)
    ad.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
               fill=(200, 35, 20, a))
img.paste(Image.alpha_composite(img.convert('RGBA'), accent_mask), (0, 0))

# ─── 9. Subtle grid overlay (data center floor tile aesthetic) ───
grid_mask = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid_mask)
tile_size = 60
for gx in range(0, W, tile_size):
    gd.line([(gx, 0), (gx, H)], fill=(255, 60, 40, 3), width=1)
for gy in range(0, H, tile_size):
    gd.line([(0, gy), (W, gy)], fill=(255, 60, 40, 3), width=1)
img.paste(Image.alpha_composite(img.convert('RGBA'), grid_mask), (0, 0))

# ─── 10. Save ───
out1 = '/home/chino/thesignal/public/img/articles/oracle-ai-cloud-capex-bet-2026.jpg'
os.makedirs(os.path.dirname(out1), exist_ok=True)
img.save(out1, quality=92)
print(f"Generated {out1} ({W}x{H})")

out2 = '/home/chino/thesignal/_backup_dist/img/articles/oracle-ai-cloud-capex-bet-2026.jpg'
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
