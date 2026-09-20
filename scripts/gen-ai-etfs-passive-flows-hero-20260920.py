#!/usr/bin/env python3
"""Generate hero for ai-etfs-passive-flows-explainer-2026 (fal flux/schnell).

Subject: an evergreen explainer on how AI-focused ETFs and passive index funds
mechanically buy and sell AI stocks — index weighting rules, creation/redemption
by authorized participants, fund flows, concentration. Sector: FINANCIAL MARKETS
/ ASSET MANAGEMENT.

The story is MECHANICAL BUYING AND SELLING OF AI STOCKS INSIDE A FUND, so the
picture is an institutional asset-management dealing desk / ETF trading floor at
the market open — a human, physical, ordinary-workplace scene, NOT a data center,
NOT a factory, NOT a server aisle, NOT a glowing abstract of "flows".

Scene set for the three attempts (all inside these bounds):
  1 — wide documentary frame of a row of curved dealing-desk workstations at the
      open, an empty ergonomic chair pushed back, a standing trader seen from
      behind, and a far wall of large monitors blurred into flat washes of blue,
      teal and amber light.
  2 — tighter three-quarter crop of one trader at a multi-monitor dealing desk,
      screens rendered as abstract out-of-focus colour, seen from behind/side.
  3 — high angle looking down over a trading floor of workstations with people
      at some desks and the screens a soft glow.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / cable-run
composition (banned), NOT neon / synthwave, NOT glowing lines, NOT geometric
patterns, NOT digital art / 3D render / CGI / HUD overlay, NOT abstract, and NOT
the recently used scenes on this site (semiconductor cleanroom, wafer carrier,
quartz photomask, hard-drive platters, generator yard, satellite antennas, ship's
bridge, coffee and notebook on a cafe table, staged enterprise laptops, AI
data-center construction, accelerator board on a bench).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: trading floors are wall-to-wall with tickers, prices, charts, CNBC,
  Bloomberg terminals, screensavers, badges and desk placards, so all lettering,
  numbers, tickers, prices, logos and UI are explicitly forbidden. Every monitor
  in frame is switched off or so far out of focus it reads as a flat wash of
  colour with nothing drawn on it.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-ai-etfs-passive-flows-hero-20260920.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ai-etfs-passive-flows-explainer-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene contains no legible lettering of any kind: no text, no "
    "letters, no words, no numbers, no digits, no prices, no tickers, no stock "
    "symbols, no ticker tape, no scrolling quotes, no percentage signs, no "
    "charts with axes or labels, no candlestick chart with readable values, no "
    "line graphs with figures, no tables, no spreadsheets, no order tickets, no "
    "trade tickets, no blotter printouts, no printed sheets, no documents, no "
    "newspapers, no financial broadsheets, no magazines, no paper with writing, "
    "no handwritten notes, no sticky notes, no legal pads, no clipboards, no "
    "whiteboards, no flip charts, no signage, no wall signs, no placards, no "
    "desk nameplates, no institutional plaques, no wall clocks with numerals, "
    "no dials, no gauges, no meters, no calculators with displays, no phones "
    "with readable screens, no keyboards with legible key legends, no blotters "
    "or mousepads with branding, no coffee mugs with printing, no clothing "
    "logos, no embroidered logos, no lanyards, no badges or ID cards, no "
    "company names, no bank names, no fund names, no brand names, no "
    "trademarks, no watermarks, no user interface, no software windows, no "
    "toolbars, no menus, no icons, no desktop widgets, no dashboards, no "
    "terminal software, no Bloomberg terminal, no Reuters screen, no CNBC or "
    "television broadcast with any on-screen graphics, no market-data display "
    "showing content, no chart of any kind drawn on any surface, no arrows, no "
    "crosshairs, no grids with numbers, no barcodes, no QR codes, no "
    "holograms, no projected data. Every monitor, display and screen in the "
    "frame is either switched off — a plain dark grey panel with nothing on it "
    "— or so far out of focus that it renders as a soft flat abstract wash of "
    "blue, teal or amber light with absolutely nothing readable, drawn or "
    "plotted on it, exactly like an out-of-focus colour field photograph. "
    "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
    "neon, no glowing lines, no light trails, no synthwave, no geometric "
    "patterns, no circuit graphics, no network diagram, no word clouds, no "
    "glowing candlestick graphics, no futuristic HUD, no hologram, no overlay "
    "elements, no augmented-reality graphics, no data center server room, no "
    "server racks, no server aisles, no cable-run composition, no server "
    "lights, no GPU hardware, no factory, no industrial plant, no cleanroom, "
    "no laboratory, no spaceship, no space, no satellites."
)

PROMPTS = {
    # 1 — wide documentary frame of the dealing-desk row at the market open.
    "1": (
        "Photo-realistic editorial press photograph, a genuine documentary "
        "newsroom frame shot on a 35mm lens at f/2.8 on a full-frame camera, "
        "inside the dealing floor of an institutional asset management firm at "
        "the market open. The frame looks down a row of curved modern dealing "
        "workstations: dark grey and pale oak curved desks with low screens, "
        "arranged in a long sweeping line that recedes across the mid-ground "
        "from left toward the right, a long low dividing screen running between "
        "the desks, and the far side of the room closed off by a tall dark "
        "partition wall rather than windows. Desk clutter is modest and "
        "ordinary blurred trade-floor paraphernalia — a plain black telephone "
        "handset, a mouse, a coffee cup, a rolled-up jacket over the back of a "
        "chair. In the left foreground, tack sharp, an empty ergonomic mesh "
        "office chair is pushed back from its desk and turned a quarter away "
        "from it, its armrest and headrest catching the room light. Just beyond "
        "it, in the centre-left of the sharp mid-ground, a man in a plain dark "
        "navy short-sleeved shirt stands at his workstation, seen from behind "
        "and slightly three-quarters, weight on one leg, leaning a little "
        "toward his screens, one hand resting near the desk surface, unposed "
        "and mid-thought. His shirt is plain unmarked fabric with no logo and "
        "no badge. Across the far wall runs a wide band of large flat-panel "
        "monitors mounted side by side and glowing softly; every one of them is "
        "far out of focus and reads only as a broad soft flat wash of blue, "
        "teal and amber light spilling gently onto the desks in front of them, "
        "with nothing plotted, written, drawn or charted on any of them, no "
        "lines and no shapes, just a smooth out-of-focus colour field like a "
        "photograph of distant coloured lights. Several smaller monitors on the "
        "near desks are plain switched-off dark grey panels. The floor is dark "
        "grey carpet tile; the ceiling is a plain acoustic grid with recessed "
        "warm panels and a couple of dark ceiling speakers. Cool blue light "
        "from the blurred monitor wall mixed with warm ceiling light, honest "
        "available-light editorial exposure, deep but gentle shadows between "
        "the desks, a soft sheen on the curved desk edges, faint scuff marks on "
        "the carpet and a cable curling loosely under one desk. Moderate depth "
        "of field — the chair and the standing trader crisp, the further desks "
        "and the monitor wall melting into creamy bokeh. Real optical lens "
        "blur, natural camera noise, clearly visible fine film grain in the "
        "midtones and shadows, subtle optical vignette, mild chromatic "
        "aberration on high-contrast edges, slightly off-level hand-held "
        "framing with the trader placed off centre, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # 2 — tighter three-quarter crop of one trader at a multi-monitor desk.
    "2": (
        "A real photograph taken on a working institutional trading floor, not "
        "a render and not computer generated: a tighter three-quarter crop shot "
        "on an 85mm lens at f/2 of one trader at his multi-monitor dealing "
        "desk. He sits in a dark ergonomic chair, seen three-quarters from "
        "behind and to the side, torso turned slightly toward the screens, one "
        "elbow on the desk, chin propped near his hand, mid-shift and unposed; "
        "he wears a plain light blue business shirt with the sleeves rolled and "
        "a plain dark tie, no logo, no badge, no lanyard, his face mostly "
        "averted and partly lost in shadow. In front of him a row of three or "
        "four flat-panel monitors stands on slim arms, and every one of them is "
        "so far out of focus that it reduces to a soft flat abstract field of "
        "blue, teal and amber glow with nothing readable, plotted or drawn on "
        "it — pure out-of-focus colour, not a screen displaying content. On the "
        "desk surface near his hand lie a plain black telephone handset, a "
        "matte mouse and a plain unmarked coffee cup; the desk is otherwise "
        "bare. Behind him, heavily blurred, the dim mass of the dealing floor "
        "recedes — a neighbouring desk, the back of a colleague's chair, dark "
        "partition panels — all reduced to soft shapes and colour. Warm desk "
        "lamp light on the near shoulder and the shirt fabric, cool blue glow "
        "spilling from the out-of-focus screens, honest available-light "
        "editorial exposure, delicate specular highlight along the monitor "
        "bezels. Extremely shallow depth of field — his shoulder and the near "
        "chair arm crisp, the screens already reduced to colour, the room "
        "behind in heavy creamy bokeh. Real optical blur, natural camera noise, "
        "very slight film grain, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional editorial "
        "stock photography, 16:9 landscape composition. " + NO_TEXT
    ),
    # 3 — high angle down over the trading floor.
    "3": (
        "A real documentary photograph, not a render and not computer "
        "generated, shot on a 24mm lens at f/4 from a raised vantage point "
        "looking down at roughly forty-five degrees over an institutional "
        "trading floor during the market open. Below the camera the floor "
        "spreads out in rows of modern dealing workstations — long pale desks "
        "with banks of screens on slim arms, ergonomic chairs at varying "
        "angles, a low central partition here and there, and a wide aisle "
        "running away between the rows. People are at some of the desks: two "
        "figures at the near left workstation, one standing and leaning over a "
        "seated colleague's shoulder mid-conversation; a woman seated alone a "
        "row further back, seen from directly above, hunched slightly forward; "
        "one empty workstation with a chair pushed back; a man in a plain "
        "unmarked grey shirt standing at the far right watching his screens. "
        "All of them are ordinary office workers in plain unmarked business "
        "clothing, no logos, no badges, no lanyards, no readable writing "
        "anywhere on their clothing or their desks. Every screen on the floor "
        "is either a plain switched-off dark grey panel or a soft out-of-focus "
        "glow of blue, teal and amber with nothing drawn, plotted or written on "
        "it — the whole floor reads as scattered patches of warm and cool light "
        "rather than readable data. The floor surface is dark grey carpet tile "
        "with visible faint traffic wear; the ceiling above the far edge of the "
        "frame is a plain acoustic grid with recessed light panels. Cool "
        "overhead mixed lighting with warm pools at the desks, honest "
        "available-light editorial exposure, gentle shadows falling on the "
        "carpet. Moderate depth of field with the nearest desks and the "
        "standing pair crisp and the far rows softening into creamy haze; real "
        "optical blur, natural camera noise, very slight film grain, subtle "
        "lens vignette, slightly off-kilter hand-held high framing, no plastic "
        "CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. " + NO_TEXT
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


def generate(prompt, out_path):
    import fal_client
    key = load_fal_key()
    if not key:
        print("ERROR: FAL_KEY not found")
        sys.exit(1)
    print("Generating image with fal flux/schnell...")
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": {"width": W, "height": H},
            "num_inference_steps": 4,
            "enable_safety_checker": False,
        },
    )
    image_url = None
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]
    if not image_url:
        print(f"ERROR: Could not find image URL in result: {result}")
        sys.exit(1)
    print(f"Image URL: {image_url}")
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print(f"Downloaded: {out_path}  size={img.size}  bytes={len(r.content)}")
    return img


def crop_to_16x9(img):
    """Center-crop to 16:9, then resize to 1920x1080."""
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H  # 16/9
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((FINAL_W, FINAL_H), Image.LANCZOS)
    return img


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 81920:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")
    # VERIFY both paths on disk
    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(
            f"VERIFY {p} dimensions={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}"
        )


if __name__ == "__main__":
    main()
