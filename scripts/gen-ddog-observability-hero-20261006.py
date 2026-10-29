#!/usr/bin/env python3
"""Generate hero for ddog-agentic-ai-observability-tollbooth-2026 (fal flux/schnell).

Subject: Datadog (NASDAQ: DDOG) — the observability platform becoming the metered
"tollbooth" for agentic AI. Thesis: every AI-agent action, tool call and MCP call
flows through Datadog's telemetry pipeline and is observed, secured and billed —
and reliability engineers now watch agent decision paths the way they once watched
APM service maps.

Scene chosen (per task brief): an authentic MODERN ENTERPRISE ENGINEERING
OPERATIONS CENTER / office — reliability engineers monitoring multi-screen
dashboards of trace graphs and workflow telemetry. Human, documentary, warm
natural ambient light, shallow depth of field. Deliberately NOT a data centre,
server room, glowing neon lines, or abstract digital art.

Deliberately DISTINCT from recent Signal heroes that must not repeat:
  (1) snps-eda-ai-chip-design-toll (20261006): EDA/chip design workstation.
  (2) crwd-agentic-security-perimeter (20261006): security ops backdrop.
  (3) axp-agentic-commerce-playbook (20261006): retail/card checkout.
  (4) pltr-enterprise-ai-bootcamps (20261005): AI training room.
  (5) mrvl-custom-silicon-investor-day (20261002): server/rack silicon.
  (6) orcl-tencent-offshore-compute-lease (20261002): data-center campus.
  (7) onsemi-synaptics-edge-ai (20261002): chip acquisition product shot.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY. No digital art, neon, synthwave,
  CGI, 3D render, cartoon, glowing lines, light trails, HUD, holograms.
- NO data-center hallway / server aisle / server racks / cable runs (banned).
- TEXT-FREE / no legible text: dashboards shown as abstract traces, no readable
  words, no numbers, no logos, no brand names, no gibberish lettering.
- FACES NOT clearly readable (side/behind, out of focus) or anonymous.
- Generate 1440x810, finalize 1920x1080 center-crop.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
    scripts/gen-ddog-observability-hero-20261006.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ddog-agentic-ai-observability-tollbooth-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "Every screen and surface is deliberately free of legible writing: no readable words, no "
    "letters, no numbers, no glyphs, no code, no captions, no labels, no legends, no menus, no "
    "menu bars, no file names, no browser chrome, no logos, no brand names, no company marks, no "
    "icons with text, no watermarks, no signatures. Any on-screen charts appear only as abstract "
    "smooth line traces, soft area fills, small dots and simple rectangles with no legible "
    "annotation and no garbled lettering. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no video-game look, no neon, no synthwave, no glowing holographic lines, no "
    "light trails, no futuristic HUD graphics, no augmented-reality overlays. Not a data-center "
    "hallway, no server aisle, no server racks, no cable runs, no rack of network gear, no "
    "cleanroom, no abstract cyberspace."
)

PROMPTS = {
    "1": (
        "Professional editorial stock photograph, shot on a full-frame camera with a 35mm lens, "
        "not a render: the interior of a modern high-tech enterprise engineering operations "
        "center at dusk. A group of software reliability engineers sit at a row of desks facing a "
        "large curved video wall made of several seamless screens. The screens glow softly with "
        "abstract observability dashboards — smooth line charts of request latency, stacked "
        "timeline spans, small scatter dots and simple bar shapes — all rendered as clean abstract "
        "graphics with no legible text. The engineers are seen from behind and from the side, "
        "shoulders and backs of heads, faces turned away or softly out of the near focus, wearing "
        "plain everyday clothing; one person is pointing at the wall, another types at a keyboard. "
        "The room is warm and human: natural oak desks, dark matte monitor bezels, a few potted "
        "plants, acoustic ceiling panels, soft warm-white ambient lighting mixed with the gentle "
        "cool glow off the screen wall, large windows on the right showing a deep blue evening sky "
        "with distant city lights softly bokeh'd. Shot at f/2.8, shallow depth of field: the "
        "nearest desk and its monitor sharp, the video wall and the people falling gently into "
        "blur. Honest realistic textures — fabric, wood, matte plastic, glass, metal chair frames; "
        "natural sensor noise, very slight film grain, subtle vignette; no CGI sheen, no perfect "
        "symmetry. Photorealistic, extremely high detail, 8k resolution, authentic editorial "
        "photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "2": (
        "A real photograph taken on a real camera, 50mm lens at f/2, shallow depth of field, not "
        "computer generated: an over-the-shoulder view of a single reliability engineer working at "
        "a tidy modern workstation in a softly lit engineering office late in the day. The sharp "
        "focal point is the engineer's monitor, which displays an abstract distributed-trace "
        "waterfall — horizontal bars of varying length stacked in a timeline, thin connecting "
        "lines and a few tiny dots — rendered as clean abstract graphics with no legible text, no "
        "numbers and no labels. Two smaller side monitors show a smooth latency line chart and a "
        "simple scatter of dots, both abstract. A second monitor is dark. The engineer is seen "
        "from behind and slightly to the side so the face is not visible, plain shirt, seated in a "
        "matte office chair, one hand resting near the keyboard, the other holding a coffee mug. "
        "The desk is plain: a notebook, a pair of earphones, a small plant, a warm desk lamp "
        "casting a soft golden pool of light. In the far background the open-plan office dissolves "
        "into soft warm blur — plain desks, framed windows with the last of the daylight, a hint "
        "of another seated colleague out of focus. Warm natural ambient lighting, gentle contrast, "
        "nothing self-lit except the screens and the lamp, no neon, no glowing lines. Honest "
        "realistic texture on wood, fabric, glass and matte plastic; natural sensor noise, very "
        "slight film grain, subtle vignette; no CGI sheen. Photorealistic, extremely high detail, "
        "8k resolution, authentic editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "3": (
        "Photo-realistic documentary stock photograph, real camera, 24mm lens, not a render: a "
        "bright modern open-plan software engineering office in the afternoon. Two reliability "
        "engineers stand together in front of a large wall-mounted flat screen, discussing the "
        "abstract telemetry displayed on it — a clean service-dependency diagram of simple circles "
        "and lines, a smooth request-rate curve and stacked timeline bars, all rendered as plain "
        "abstract graphics with no legible text and no labels. One engineer gestures toward the "
        "screen; both are shown from behind and in three-quarter profile so faces are turned away "
        "from the camera and softly out of focus. Beyond them the office is alive and human: "
        "engineers at standing desks, a whiteboard covered only in blank magnets and plain blue "
        "sticky notes, exposed-but-plain ceiling with warm recessed lighting, large windows "
        "flooding the room with soft natural daylight, a few potted plants, plain wooden and grey "
        "surfaces. Shot at f/2.8 with the two foreground engineers slightly soft and the mid-ground "
        "office in gentle blur; warm natural daylight is the dominant light with a soft cool spill "
        "from the screen, nothing self-lit, no neon, no glowing lines. Honest realistic textures — "
        "wood, fabric, glass, brushed metal, matte plastic; natural sensor noise, very slight film "
        "grain, subtle vignette; no CGI look, no illustration, no perfect symmetry. Photorealistic, "
        "extremely high detail, 8k resolution, authentic editorial photography, 16:9 landscape "
        "composition. " + NO_TEXT
    ),
    "4": (
        "Photojournalistic candid documentary photograph, shot on a Fujifilm X-T5 with a 23mm lens "
        "at f/2, real available light, unretouched, not a render and not CGI: a modern open-plan "
        "software engineering office on a bright afternoon. In the sharp foreground a reliability "
        "engineer stands beside a sit-stand desk in three-quarter profile, seen from behind and to "
        "the side so the face is not identifiable, focused on a laptop whose screen shows only "
        "faint abstract line traces at an oblique angle. Behind them, in soft focus, two colleagues "
        "talk near a monitor; the monitors along the desk row are angled away from the camera so "
        "their contents read only as indistinct glowing rectangles, nothing legible. The room is "
        "richly human and textured: worn wooden desks, tidy cables, a coffee cup, plain sticky "
        "notes, potted plants, a paper notebook, a jumper over a chair; large windows flood "
        "everything with soft natural daylight and gentle real shadows. Genuinely imperfect candid "
        "composition, natural sensor grain, faint chromatic aberration at the frame edges, subtle "
        "motion blur on one passing colleague, realistic fabric and skin texture, no studio "
        "lighting, no neon, no glowing lines, no perfect symmetry. Photorealistic, extremely high "
        "detail, authentic editorial photography, 16:9 landscape composition. " + NO_TEXT
    ),
    "5": (
        "Photo-realistic editorial stock photograph taken on a real camera, 28mm lens at f/4, not "
        "a render: inside a modern enterprise engineering operations center during the daytime. A "
        "row of plain workstations curves along the room; each monitor shows only soft abstract "
        "chart shapes — line traces and timeline bars — seen at an oblique angle from behind so "
        "nothing on any screen is legible. The human focus is one reliability engineer in a plain "
        "shirt seated in the foreground, seen from behind and slightly to the side, typing, face "
        "not visible, the sharp element in the frame. Further down the row another engineer stands "
        "in front of a monitor, out of focus. Plain desks, ergonomic chairs, a whiteboard bearing "
        "only blank sticky notes, a ceiling with simple recessed lights, and large windows on one "
        "side admitting soft daylight. Understated, documentary, realistic materials — brushed "
        "metal, wood, fabric, matte plastic — natural sensor grain, very slight film grain, subtle "
        "vignette, no neon, no glowing lines, no perfect symmetry. Photorealistic, extremely high "
        "detail, 8k resolution, authentic editorial photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    "6": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at f/2.0 on a full-frame "
        "camera, of a software reliability engineer at work at their desk in a modern engineering "
        "office. In the sharp centre of frame a large desktop monitor is angled three-quarters "
        "toward the camera, and its dark screen is filled edge to edge with an abstract service "
        "topology map: dozens of small uniform dots (nodes) of muted teal, slate blue and soft "
        "amber, joined by fine hairline straight and gently curved connector lines, a few small "
        "clusters denser than the rest, drawn on a plain near-black ground — a pure geometric field "
        "of dots and lines, like a constellation diagram, with nothing written, labelled or "
        "numbered on it. In front of the monitor, seen from the side and slightly behind, a "
        "reliability engineer in a plain dark knit sweater sits turned toward the screen, both "
        "hands resting on a plain keyboard on a pale wooden desk, one hand lifted mid-keystroke, "
        "focused and calm, mid-task and not posing; the face is in near-profile, softly lit by the "
        "screen from the front and by daylight from a window on the left, sharp from shoulders to "
        "hands. The desk is uncluttered: a plain white ceramic mug, a small blank notebook, a thin "
        "pen, a second smaller monitor behind turned away with its screen dark. The office behind "
        "is soft and modern: pale grey walls, a warm oak desk surface, a muted green potted plant "
        "out of focus at the edge of frame, blurred silhouettes of other desks and daylight "
        "through a large window in the far background. Warm natural key light from the window on "
        "the left with cool screen glow filling the shadow side, gentle falloff into the room, "
        "soft realistic shadows across the desk. Very shallow depth of field: the screen map and "
        "her hands are tack sharp while the office behind melts into creamy bokeh. Real optical "
        "lens blur, honest available-light editorial exposure, natural camera noise, very slight "
        "film grain, subtle lens vignette, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT + (
            " The large monitor shows ONLY the abstract node-and-link topology field described — "
            "not a dashboard, not a chart, not a graph, not a plot, no axes, no legends, no "
            "readouts, no gauges, no numbers, no tables, no terminal, no code, no software user "
            "interface, no menus, no window chrome."
        )
    ),
    "7": (
        "Photo-realistic editorial press photograph, shot on a 35mm lens at f/2.2 on a full-frame "
        "camera, of two software reliability engineers standing together in a modern engineering "
        "office in front of a large wall-mounted display. In the sharp centre of frame the display "
        "is filled edge to edge with an abstract agentic-workflow topology map: a wide field of "
        "small uniform dots (nodes) in muted teal, slate blue and soft amber, joined by fine "
        "hairline straight and gently curved connector lines that fan out into a branching "
        "network, a few clusters denser than the rest, drawn on a plain near-black ground — purely "
        "geometric dots and lines, a constellation of connected points, with nothing written, "
        "labelled or numbered on it. The two engineers — a man and a woman in their thirties in "
        "plain shirts, no badges — are seen from behind and in three-quarter profile so their "
        "faces are turned away from the camera, absorbed in the display, one of them raising a "
        "hand to point at a cluster, mid-conversation and not posing; their heads and shoulders "
        "are softly lit by the display's glow. Around them the office is soft and human: plain "
        "wooden desks, a few matte chairs, a muted green plant, a large window on the right "
        "flooding the room with warm, soft natural daylight, the mid-ground office and other "
        "colleagues blurred into creamy bokeh. Warm daylight is the dominant key light with a "
        "gentle cool spill from the display, soft realistic shadows, nothing self-lit except the "
        "display, no neon, no glowing lines. Very shallow depth of field with the display and the "
        "pointing hand sharp and the room behind melting into blur. Real optical lens blur, honest "
        "available-light editorial exposure, natural camera noise, very slight film grain, subtle "
        "lens vignette, no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT + (
            " The wall display shows ONLY the abstract node-and-link topology field described — "
            "not a dashboard, not a chart, not a graph, not a plot, no axes, no legends, no "
            "readouts, no gauges, no numbers, no tables, no terminal, no code, no software user "
            "interface, no menus, no window chrome."
        )
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
    args = {
        "prompt": prompt,
        "image_size": {"width": W, "height": H},
        "num_inference_steps": 4,
        "enable_safety_checker": False,
    }
    seed = os.environ.get("SEED")
    if seed:
        args["seed"] = int(seed)
        print(f"  seed={seed}")
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments=args)
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
    w, h = img.size
    target_ratio = FINAL_W / FINAL_H
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif cur_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((FINAL_W, FINAL_H), Image.LANCZOS)


def main():
    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print(f"Saved final hero: {OUTPUT}  dimensions={img.size}  bytes={size}")
    if size < 51200:
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print(f"Re-saved with higher quality: {os.path.getsize(OUTPUT)} bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    img.save(BACKUP, "JPEG", quality=92, optimize=True)
    print(f"Mirrored to {BACKUP}")


if __name__ == "__main__":
    main()
