#!/usr/bin/env python3
"""Generate a dark, moody Micron (MU) hero image — semiconductor fab / AI memory chip aesthetic."""
from PIL import Image, ImageDraw
import math, random, os

W, H = 1200, 675
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ─── 1. Dark gradient background (deep blue/charcoal tones — Micron brand) ───
for y in range(H):
    t = y / H  # 0 top, 1 bottom
    r = int(8 + t * 8)
    g = int(12 + t * 10)
    b = int(22 + t * 14)
    # Blue accent gradient in center (Micron blue)
    blue_intensity = 1.0 - abs(t - 0.45) * 1.4
    blue_intensity = max(0, blue_intensity)
    r += int(6 * blue_intensity)
    g += int(14 * blue_intensity)
    b += int(30 * blue_intensity)
    draw.line([(0, y), (W, y)], fill=(min(r, 255), min(g, 255), min(b, 255)))

# ─── 2. Wafer / chip die shapes (circular wafer patterns) ───
wafer_color = (18, 30, 50)
wafer_highlight = (45, 70, 100)

# Large wafer silhouette (left side)
cx1, cy1 = 250, 320
for r_w in range(160, 0, -6):
    a = max(8, 30 - (160 - r_w) // 8)
    draw.ellipse([cx1 - r_w, cy1 - r_w, cx1 + r_w, cy1 + r_w],
                 fill=(12 + (160 - r_w) // 15, 22 + (160 - r_w) // 12, 40 + (160 - r_w) // 10, a))
draw.ellipse([cx1 - 160, cy1 - 160, cx1 + 160, cy1 + 160], outline=(40, 70, 110), width=2)

# Wafer die pattern — tiny rectangles arranged in rings (like chip dies on a wafer)
for ring in range(3, 8):
    num_dies = ring * 10
    for di in range(num_dies):
        angle = (di / num_dies) * 2 * math.pi + ring * 0.3
        dist = ring * 18 + 15
        dx = int(cx1 + dist * math.cos(angle))
        dy = int(cy1 + dist * math.sin(angle))
        if 0 < dx < W and 0 < dy < H:
            die_w, die_h = 4, 4
            brightness = random.uniform(0.6, 1.0)
            die_color = (int(50 * brightness), int(100 * brightness), int(180 * brightness))
            draw.rectangle([dx - die_w//2, dy - die_h//2, dx + die_w//2, dy + die_h//2],
                           fill=die_color)

# Smaller wafer silhouette (right side)
cx2, cy2 = 920, 380
for r_w in range(120, 0, -6):
    a = max(6, 25 - (120 - r_w) // 6)
    draw.ellipse([cx2 - r_w, cy2 - r_w, cx2 + r_w, cy2 + r_w],
                 fill=(10 + (120 - r_w) // 12, 18 + (120 - r_w) // 10, 35 + (120 - r_w) // 8, a))
draw.ellipse([cx2 - 120, cy2 - 120, cx2 + 120, cy2 + 120], outline=(35, 60, 95), width=2)

# Dies on smaller wafer
for ring in range(2, 6):
    num_dies = ring * 8
    for di in range(num_dies):
        angle = (di / num_dies) * 2 * math.pi + ring * 0.5
        dist = ring * 16 + 10
        dx = int(cx2 + dist * math.cos(angle))
        dy = int(cy2 + dist * math.sin(angle))
        if 0 < dx < W and 0 < dy < H:
            die_w, die_h = 3, 3
            brightness = random.uniform(0.5, 0.9)
            die_color = (int(40 * brightness), int(80 * brightness), int(160 * brightness))
            draw.rectangle([dx - die_w//2, dy - die_h//2, dx + die_w//2, dy + die_h//2],
                           fill=die_color)

# ─── 3. Abstract chip fab / clean room elements (horizontal bands / equipment silhouettes) ───
# Fab equipment silhouettes at bottom
equip_color = (15, 25, 35)
for eq in range(6):
    ex = 60 + eq * 200
    ey = 450 + random.randint(0, 40)
    ew = 140 + random.randint(-30, 30)
    eh = 150 + random.randint(-20, 20)
    draw.rectangle([ex, ey, ex + ew, min(ey + eh, H)], fill=equip_color, outline=(25, 40, 55), width=1)
    # Equipment details — horizontal slots
    for slot_y in range(ey + 15, min(ey + eh, H - 5), 22):
        draw.line([(ex + 10, slot_y), (ex + ew - 10, slot_y)], fill=(30, 45, 62), width=2)
        # Status LEDs — Micron blue
        if random.random() > 0.35:
            led_color = (60, 140, 220) if random.random() > 0.3 else (40, 100, 180)
            draw.ellipse([(ex + ew - 18, slot_y - 3), (ex + ew - 10, slot_y + 3)], fill=led_color)

# ─── 4. Glowing blue/teal circuit trace / data lines ───
def draw_glowing_line(draw, pts, color, width=3, glow_steps=6):
    for g in range(glow_steps, 0, -1):
        a = max(5, 30 // g)
        gw = width + g * 4
        draw.line(pts, fill=(color[0], color[1], color[2], a), width=gw)
    draw.line(pts, fill=color, width=width)

# Circuit-like traces between wafer and fab equipment
trace_colors = [
    (60, 140, 220),   # Micron blue
    (80, 180, 240),   # light blue
    (40, 100, 200),   # deep blue
    (60, 200, 180),   # teal accent
]

for ci in range(16):
    # Connect wafer areas to equipment
    src_x = random.choice([cx1, cx1 - 80, cx1 + 80, cx2, cx2 - 60, cx2 + 60])
    src_y = random.choice([cy1, cy1 - 40, cy1 + 40, cy2, cy2 - 30, cy2 + 30])
    dst_x = random.randint(100, W - 100)
    dst_y = random.randint(420, H - 40)
    
    mid_y = random.randint(250, 450)
    ctrl1_x = src_x + (dst_x - src_x) * 0.3 + random.randint(-40, 40)
    ctrl1_y = mid_y - random.randint(20, 60)
    ctrl2_x = src_x + (dst_x - src_x) * 0.7 + random.randint(-40, 40)
    ctrl2_y = mid_y + random.randint(20, 60)
    
    pts = []
    for t_i in range(0, 21):
        t = t_i / 20
        u = 1 - t
        x = u**3 * src_x + 3*u**2*t * ctrl1_x + 3*u*t**2 * ctrl2_x + t**3 * dst_x
        y = u**3 * src_y + 3*u**2*t * ctrl1_y + 3*u*t**2 * ctrl2_y + t**3 * dst_y
        pts.append((int(x), int(y)))
    
    color = trace_colors[ci % len(trace_colors)]
    brightness = random.uniform(0.5, 0.9)
    adj_color = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))
    
    if random.random() > 0.25:
        draw_glowing_line(draw, pts, adj_color, width=2, glow_steps=3)
    else:
        draw.line(pts, fill=adj_color, width=1)

# ─── 5. AI / data flow particles ───
random.seed(42)
for p in range(65):
    x = random.randint(100, 1100)
    y = random.randint(100, 500)
    r = random.randint(1, 3)
    glow_r = r + 4
    dot_color = (80, 180, 255) if random.random() > 0.3 else (60, 220, 200)
    for gr in range(glow_r, 0, -1):
        alpha_val = max(5, 25 - gr * 3)
        draw.ellipse([x - gr, y - gr, x + gr, y + gr],
                      fill=(dot_color[0], dot_color[1], dot_color[2], alpha_val))
    draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_color)

# ─── 6. Data flow lines (horizontal, blue-tinted) ───
random.seed(99)
for li in range(12):
    y = random.randint(150, 480)
    x_start = random.randint(30, 250)
    x_end = random.randint(800, W - 30)
    alpha = random.randint(10, 30)
    draw.line([(x_start, y), (x_end, y)], fill=(60, 130, 200, alpha), width=1)

# ─── 7. Subtle scan lines / data stream ───
random.seed(123)
for _ in range(250):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    c = random.randint(10, 30)
    img.putpixel((x, y), (c + 5, c + 10, c + 25))

# ─── 8. Vignette (darker edges) ───
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

# ─── 9. Micron blue accent glow in center ───
accent_mask = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(accent_mask)
center_x, center_y = W // 2, H // 2
for r in range(300, 0, -8):
    a = max(3, 10 - r // 35)
    ad.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
               fill=(40, 120, 220, a))
img.paste(Image.alpha_composite(img.convert('RGBA'), accent_mask), (0, 0))

# ─── 10. Subtle grid overlay (fab clean room floor tile aesthetic) ───
grid_mask = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid_mask)
tile_size = 55
for gx in range(0, W, tile_size):
    gd.line([(gx, 0), (gx, H)], fill=(60, 130, 200, 3), width=1)
for gy in range(0, H, tile_size):
    gd.line([(0, gy), (W, gy)], fill=(60, 130, 200, 3), width=1)
img.paste(Image.alpha_composite(img.convert('RGBA'), grid_mask), (0, 0))

# ─── 11. Save ───
out = '/home/chino/thesignal/public/img/articles/micron-us-chip-investment-surge-2026.jpg'
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, quality=92)
print(f"Generated {out} ({W}x{H})")

# Verify
size = os.path.getsize(out)
print(f"Size: {size} bytes")
if size >= 10000:
    print("✅ Image is >= 10KB")
else:
    print("⚠️  Image size check failed!")
