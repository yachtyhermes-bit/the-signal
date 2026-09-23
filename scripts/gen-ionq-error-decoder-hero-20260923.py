#!/usr/bin/env python3
"""Generate hero for ionq-quantum-error-decoder-nvidia-2026 (fal flux/schnell).

Subject: IonQ (IONQ) — trapped-ion quantum computing. IonQ demonstrated an
end-to-end REAL-TIME quantum error decoder (a classical CPU correcting quantum
errors in the background while the quantum processor keeps running), and put the
first on-premise quantum computer (Superion 256) inside NVIDIA's Accelerated
Quantum Research Center, wired to an NVIDIA GB200 NVL72 over NVQLink and driven
by CUDA-Q. Sector: QUANTUM COMPUTING HARDWARE.

The picture is therefore QUANTUM COMPUTING HARDWARE IN A PHYSICS LAB —
cryogenics, control electronics, ion traps. Built around a cryogenic dilution
refrigerator, the gold-plated copper and silver coaxial wiring stack (the
"chandelier") inside the cryostat's vacuum can.

Scene set for the three attempts (all inside these bounds):
  1 — a gold-plated cryostat wiring stack being assembled on a lab bench, held
      in a clean white glove, plain unmarked copper and silver metal.
  2 — a researcher at a rack of RF control electronics feeding a cryostat via
      thick coaxial cable bundles.
  3 — a close three-quarter crop of the copper chandelier plates inside the
      opened cryostat with a white-gloved hand guiding a coaxial cable.

Deliberately NOT a data-center / server-room / server-aisle / GPU-rack / rack
aisle / long-hallway cable-run composition (banned and overused on this site),
NOT neon / synthwave, NOT glowing lines, NOT light trails, NOT geometric
patterns, NOT digital art / 3D render / CGI / hologram / HUD overlay / AR
graphics, NOT a glowing qubit graphic, and NOT the recently used scenes on this
site (high-voltage substation, generator yard, optics / laser lab, cleanroom
wafer fab, chip-design desk, boutique checkout counter, night cityscape).

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial press photograph ONLY.
- TEXT-FREE: cryostats, RF racks, control panels and part labels are covered in
  part numbers, branding and UI screens, so all lettering, numbers, serial
  numbers, part numbers, logos, brand names, signage, badges, printed documents,
  charts and readouts are explicitly forbidden. Any monitor, screen, control
  panel or instrument display in frame is switched off, angled away, or so far
  out of focus it reads as a flat dark rectangle. Copper and silver wiring is
  plain unmarked metal.
- Generate 1440x810, finalize 1920x1080 center-crop, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-ionq-error-decoder-hero-20260923.py
"""
import os
import sys
import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "ionq-quantum-error-decoder-nvidia-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_DISPLAYS = (
    " Critically, there is not one single lit or active display anywhere in "
    "this photograph: no glowing red or green digital numbers, no "
    "seven-segment numerals, no LED digits, no backlit LCD, no lit instrument "
    "window, no lit panel meter, no glowing indicator lamp, no illuminated "
    "button, no status light, no blinking LEDs, no lit power switch, no "
    "control panel showing values, no readout of any kind glowing in the "
    "scene. Every instrument, control panel and electronic housing in the "
    "frame has a plain flat unlit blank face: continuous smooth unmarked "
    "metal or matte plastic, with no window, no screen, no glass, no display, "
    "no digits, no dial face and no lit element anywhere on it. Anything that "
    "could be mistaken for a screen is dark, dead and switched off, reading "
    "only as a flat unlit rectangle of dark material. The only light in the "
    "image comes from the room's own lamps and windows, never from the "
    "equipment. "
)

NO_TEXT = (
    "This is not a digital illustration and not a 3D render: it is an "
    "ordinary available-light documentary photograph made with a real camera "
    "in a working laboratory, with the imperfect framing, uneven exposure, "
    "slight dust, faint fingerprints, scuffs and small asymmetries of a real "
    "photo. The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no serial numbers, no part numbers, no "
    "model numbers, no engraved or stamped markings on the metal, no "
    "instrument markings, no labels, no sticker labels, no equipment "
    "nameplates, no manufacturer names, no company names, no brand names, no "
    "corporate logos, no trademarks, no user interface, no software windows, "
    "no code, no terminal windows, no oscilloscope traces with axis numbers, "
    "no spectrum analyser content, no signal generator readouts, no digital "
    "readouts, no seven-segment displays, no dial faces with numerals, no "
    "gauges with numbers, no meters, no charts, no graphs, no plots, no "
    "dashboards, no monitor content, no control-panel content, no signage, no "
    "warning signs, no placards, no safety stickers, no hazard tape lettering, "
    "no lab-coat lettering, no name badges, no lanyards, no printed documents, "
    "no clipboards with writing, no lab notebooks, no whiteboards with "
    "writing, no posters, no wall charts, no barcodes, no QR codes, no "
    "handwriting, no watermarks, no legible writing of any kind anywhere in "
    "the image. Every display, monitor, screen, oscilloscope, control panel or "
    "instrument face in the frame is switched off, angled away, or so far out "
    "of focus that it shows only a soft flat wash of dark colour with "
    "absolutely nothing readable or drawn on it, like an out-of-focus colour "
    "field photograph, not a screen with content. The copper, gold-plated and "
    "silver metal surfaces are plain smooth unmarked metal with no printing or "
    "engraving on them. No illustration, no digital art, no cartoon, no 3D "
    "render, no CGI, no neon, no glowing lines, no light trails, no synthwave, "
    "no geometric patterns, no circuit-board graphics, no glowing qubit "
    "graphic, no atom or orbital graphic, no network diagram, no futuristic "
    "HUD graphics, no hologram, no overlay elements, no augmented-reality "
    "graphics, no floating UI, no data center, no server room, no server "
    "racks, no server aisles, no GPU racks, no rack aisle, no long hallway of "
    "cabinets, no cable-run perspective down an aisle, no server lights, no "
    "blinking network switch LEDs, no computer screen with text."
)

PROMPTS = {
    # 1 — gold-plated cryostat wiring stack being assembled on a lab bench in a clean glove.
    "1": (
        "Photo-realistic editorial press photograph, shot on an 85mm macro "
        "lens at f/2.8 on a full-frame camera, inside a quantum computing "
        "research laboratory. The sharp subject filling the centre of frame, "
        "in the mid-ground, is the circular top section of a cryogenic "
        "dilution refrigerator's internal wiring stack: a heavy machined "
        "gold-plated copper plate, roughly a hand-span across, whose underside "
        "carries concentric rings of thin gold-plated semi-rigid coaxial "
        "cables and fine twisted-pair looms that sweep down in smooth "
        "arching bundles, hundreds of hair-fine silver wires fanning out of "
        "each connector block, all of it plain unmarked polished metal "
        "gleaming under the bench light. In the left foreground, tack sharp, a "
        "researcher's hands in clean white lint-free gloves hold the plate "
        "steady from below and guide one of the thin coaxial cables into a "
        "small machined connector with a pair of fine tweezers, fingertips "
        "pressing carefully, mid-assembly and unposed; a plain grey "
        "long-sleeve cuff and a wrist of a bare forearm enter the frame from "
        "the near edge. The bench beneath is a plain unmarked brushed "
        "stainless surface, holding only a plain white lint-free cloth, a "
        "small plain stainless tray and the coiled end of a grey cable "
        "sweeping out of focus toward the bottom-left corner. Behind, well "
        "out of focus, the pale grey mass of a lab bench and instrument "
        "housings dissolve into a soft wash; every screen and panel back "
        "there is dark, switched off or angled away. Warm tungsten task-lamp "
        "light from the upper left mixed with cool diffuse daylight from a "
        "window behind the camera, honest available-light editorial exposure, "
        "delicate specular highlights sliding along the gold-plated metal and "
        "the fine wires, deep soft shadows underneath the plate. Extremely "
        "shallow depth of field — the connector, the tweezers, the gloved "
        "fingertips and the nearest wiring rings are tack sharp while the "
        "sleeves, the bench and the room behind melt into creamy bokeh. Real "
        "optical lens blur, natural camera noise, clearly visible fine film "
        "grain in the midtones and shadows, subtle optical vignette, mild "
        "chromatic aberration on high-contrast edges, no plastic CGI sheen, "
        "no glossy render, no perfect symmetry, no 3D visualisation, no "
        "digital illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 2 — researcher at a rack of RF control electronics feeding a cryostat via coaxial bundles.
    "2": (
        "A real documentary photograph taken inside a quantum computing "
        "physics lab, not a render and not computer generated: three-quarter "
        "view, shot on a 35mm lens at f/2.0 on a full-frame camera. In the "
        "sharp mid-ground on the left stand the open front bays of a tall "
        "laboratory electronics rack carrying a column of plain brushed "
        "aluminium instrument housings with completely blank flat unmarked "
        "faces — plain continuous vented panels and a few small unmarked "
        "controls, each front panel a single uninterrupted sheet of matte "
        "metal with no window, no screen, no glass, no dial face and no lit "
        "element of any kind. From the "
        "bottom of the bays a dense bundle of thick grey and black coaxial "
        "cables and ribbon looms sweeps across the frame in a heavy gentle "
        "curve, gathering into the base of the cryostat on the right. The "
        "cryostat itself is a large vertical cylindrical aluminium vacuum can "
        "on a wheeled frame, its top flange ringed with a dozen polished brass "
        "and stainless connector collars; one of its side ports stands open "
        "and a slender copper rod with a small machined plate on its end is "
        "being lowered into it. A researcher in a plain grey long-sleeve "
        "shirt, seen three-quarters from behind and to the side, stands "
        "between the rack and the cryostat with both hands on the cable "
        "bundle, shoulders squared to the task, face mostly turned away, "
        "mid-task and unposed. The floor is plain sealed grey lab flooring "
        "with a soft sheen and a few faint scuffs; the wall behind is plain "
        "pale grey with a plain shelf of unmarked metal cans. Warm overhead "
        "tungsten lab lighting from the left mixed with a cool blue-white "
        "spill from a distant window, gentle warm highlights along the "
        "aluminium and the cable jackets, soft realistic shadows pooling "
        "under the rack and the cryostat frame. Moderate depth of field: the "
        "cables, the rack bays and the researcher's hands crisp, while the "
        "far wall and the room's back corner dissolve into creamy bokeh. Real "
        "optical lens blur, honest available-light editorial exposure, "
        "natural camera noise, clearly visible fine film grain in the "
        "midtones and shadows, subtle lens vignette, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
        + NO_DISPLAYS
    ),
    # 3 — close three-quarter crop of the copper chandelier plates inside the opened cryostat.
    "3": (
        "A genuine photograph taken in a quantum computing laboratory, not a "
        "render and not computer generated: a tight three-quarter crop, shot "
        "on a 50mm lens at f/2.0 on a full-frame camera, looking down into the "
        "opened vacuum can of a cryogenic dilution refrigerator. The frame is "
        "dominated by the internal wiring stack: three or four stacked "
        "circular gold-plated copper plates of decreasing diameter, mounted on "
        "a central column, each ringed with fine machined holes, from the "
        "underside of each plate dozens of thin gold-plated semi-rigid coaxial "
        "cables and fine silver wires hang down in smooth parallel arcs to the "
        "plate below, layer after layer, a dense shimmering curtain of plain "
        "unmarked polished metal catching the light. The cryostat walls are "
        "plain unmarked polished aluminium rising out of frame at the edges, "
        "with the bright circular lip of the top flange framing the crop. In "
        "the lower right foreground, tack sharp, one white-gloved hand with "
        "fingers and a slim stainless tool guides a single thin coaxial cable "
        "into a small machined connector on the top plate; a plain grey cuff "
        "enters from the bottom edge. Warm tungsten task light rakes in from "
        "the upper right, cool daylight fills from the left, mixed light "
        "skimming across the gold plating and the fine wires with delicate "
        "specular highlights and deep soft shadow in the gaps between plates. "
        "Honest available-light editorial exposure, gentle highlight clipping "
        "on the brightest metal edges. Extremely shallow depth of field — the "
        "connector, the gloved fingertips and the nearest wiring layer are "
        "tack sharp while the lower plates and the inside of the can melt "
        "away into creamy bokeh. Real optical lens blur, natural camera noise, "
        "clearly visible fine film grain in the midtones and shadows, subtle "
        "optical vignette, mild chromatic aberration on the high-contrast "
        "metal edges, no plastic CGI sheen, no glossy render, no perfect "
        "symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
        + NO_DISPLAYS
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
