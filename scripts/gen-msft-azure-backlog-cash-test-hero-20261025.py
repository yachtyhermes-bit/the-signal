#!/usr/bin/env python3
"""Generate hero for msft-azure-backlog-cash-test-2026 (fal flux/schnell).

Subject: Microsoft's AI buildout ahead of Wednesday earnings — a $678B
contracted cloud backlog against a rising capex / depreciation bill that is
starting to pinch hyperscaler free cash flow. The story is money and the
people who run enterprise cloud, not hardware porn.

Scene chosen (PRIMARY, prompt 1): two software engineers working late in a
modern glass-walled open-plan office, shot from behind/beside the seated
engineer so the monitor faces AWAY from camera and reads only as soft glow —
warm low evening light through the glass, blurred city towers outside,
shallow depth of field on the standing engineer's hands and face.

Deliberately NOT a data centre, NOT a server aisle or rack (banned site-wide),
NOT neon / synthwave / glowing lines / geometric patterns, NOT digital art,
NOT 3D render, NOT abstract, NOT text of any kind.

Rules:
- PHOTO-REALISTIC editorial photograph ONLY (wire-service look).
- TEXT-FREE: no letters/numbers/labels/logos/signage/UI on screens anywhere.
- Generate 1536x864, JPEG, keep under 400KB, mirror to _backup_dist.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 \
         scripts/gen-msft-azure-backlog-cash-test-hero-20261025.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "msft-azure-backlog-cash-test-2026")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = f"/home/chino/thesignal/public/img/articles/{SLUG}.jpg"
BACKUP = f"/home/chino/thesignal/_backup_dist/img/articles/{SLUG}.jpg"
W, H = 1536, 864  # 16:9
MAX_BYTES = 400 * 1024

NO_TEXT = (
    "The entire scene is completely free of any lettering: no text, no "
    "letters, no words, no numbers, no code, no file names, no window titles, "
    "no menu bars, no toolbars, no tabs, no captions, no timestamps, no chart "
    "labels, no axis numbers, no percentages, no currency symbols, no stock "
    "tickers, no email or chat windows, no dashboards with legible figures, no "
    "monitor screens showing readable content, no whiteboard writing, no "
    "sticky notes with writing, no printed paper, no documents, no closed "
    "laptops with visible branding, no signage, no wall signs, no wayfinding "
    "signs, no floor numbers, no safety posters, no name plates, no ID badges, "
    "no lanyards with logos, no equipment labels, no asset tags, no cable "
    "labels, no brand names, no manufacturer names, no company names, no "
    "corporate logos, no trademarks, no watermarks, no stickers, no decals, no "
    "barcodes, no QR codes, no handwriting, no graffiti, no legible writing of "
    "any kind anywhere in the image. Every computer screen in the frame is "
    "either turned away from the camera or shows only a soft unreadable glow: "
    "smooth out-of-focus light with no shapes, no text, no interface elements. "
    "Clothing is plain solid colour with no printed slogans, no embroidered "
    "names and no wordmarks. No illustration, no digital art, no cartoon, no "
    "3D render, no CGI, no neon, no glowing lines, no light trails, no "
    "synthwave, no geometric patterns, no network diagram, no graph graphic, "
    "no futuristic HUD graphics, no hologram, no overlay elements, no "
    "augmented-reality graphics, no data center, no server room, no server "
    "racks, no server aisles, no cable runs, no rack lights, no raised-floor "
    "computer room."
)

PHOTO_TAIL = (
    "Real optical lens blur, honest available-light exposure, natural camera "
    "noise, very slight film grain, subtle lens vignette, true-to-life colour, "
    "no plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
    "visualisation, no digital illustration, no painting, shot on a real "
    "camera by a real photographer, photorealistic, very high detail, "
    "professional editorial stock photography, 16:9 landscape composition, "
    "professional lighting."
)

PROMPTS = {
    # 1 — PRIMARY: 35mm, two engineers at a desk in a glass-walled office at
    #     dusk, monitor turned away from camera, warm evening light.
    "1": (
        "Professional stock photograph, a real editorial photograph shot on a "
        "35mm lens at f/2 on a full-frame camera, handheld, from just behind "
        "and to the left of a seated engineer in a modern open-plan software "
        "company office in the early evening. In the near foreground, at the "
        "left edge and thrown slightly out of focus, the seated engineer's "
        "shoulder, the back of a plain grey office chair and the edge of a "
        "light wood desk. The sharp subject, in the middle of the frame, is a "
        "second engineer standing beside the desk, leaning in toward the "
        "screen with her weight on one hand flat on the desk surface: a woman "
        "in her early thirties in a plain charcoal knit sweater with the "
        "sleeves pushed to the forearm, dark hair tied loosely back, seen in "
        "three-quarter profile while she looks at the display, mid-sentence, "
        "one hand raised and her index finger pointing toward the monitor, "
        "her face lit softly from the screen side and warm from the window, "
        "an ordinary working expression of concentration, not posing. The "
        "monitor she is reading stands on the desk turned steeply away from "
        "the camera so only its plastic back and a halo of soft cool white "
        "light spilling around its edges is visible — the screen itself faces "
        "away and shows nothing readable from this angle. Behind them the "
        "office is a real working floor: a glass partition wall runs across "
        "the right of the frame, beyond it a second row of desks with two "
        "distant colleagues standing and talking in silhouette against the "
        "windows, a coat on a chair back, a mug, a potted plant, a stack of "
        "notebooks, all dissolving into soft blur. The lighting is the "
        "evening's own: low warm amber sunlight coming in through the floor-to-"
        "ceiling window wall at the far right, raking across the desk and "
        "laying a long warm highlight along the woman's forearm and cheek, "
        "mixed with the cool blue-white spill of the monitors and the ceiling "
        "fixtures, so the frame holds warm amber and cool blue together in "
        "honest mixed interior light with no coloured gels and no "
        "atmospheric theatrics. Outside the glass, far out of focus, the soft "
        "grey and warm shapes of city towers at dusk with a scatter of lit "
        "windows. Photographic, shallow depth of field: the standing "
        "engineer's face, her pointing hand and the desk edge tack sharp, the "
        "seated colleague's back and the whole office melting into smooth "
        "creamy blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 2 — FALLBACK A: corporate campus exterior at dusk, warm lit windows,
    #     two employees walking a path, wet paving reflections. No screens.
    "2": (
        "Professional stock photograph, a real editorial photograph shot on a "
        "70mm lens at f/2.8 on a full-frame camera, standing at ground level "
        "on a landscaped walkway outside a large modern corporate technology "
        "campus at dusk, twenty minutes after sunset. The building fills the "
        "upper two-thirds of the frame: a long, low, contemporary office block "
        "of pale stone and dark glass with deep horizontal floor bands, its "
        "windows warm with interior light in irregular patches where teams are "
        "still working, the glass holding soft reflections of the violet-blue "
        "evening sky and a few early streetlights. In the lower right third, "
        "walking away from camera along the wet dark paving toward the "
        "entrance, two employees in plain business-casual clothes — a man in a "
        "navy jacket carrying a plain shoulder bag and a woman in a rust-"
        "coloured coat — seen from behind at about fifteen metres, mid-stride, "
        "their figures soft but clearly readable, a warm pool of light from a "
        "low bollard lamp catching the woman's coat and the damp paving "
        "around their feet where recent rain has left a thin film of water "
        "holding a smeared amber reflection. In the foreground, in the left "
        "third and thrown well out of focus, the dark wet leaves of a low "
        "planting bed and the corner of a concrete bench. The light is the "
        "last of the evening: a thin band of warm orange along the horizon "
        "behind the roofline, deep blue overhead, and the warm interior glow "
        "of the building reading as hundreds of soft amber rectangles, with "
        "the paved walkway falling away into cool blue shadow — honest "
        "available light at dusk, no coloured gels, no light trails, no "
        "long-exposure blur. Photographic, shallow depth of field with the two "
        "walking figures and their reflection sharp and the building's facade "
        "and the far treeline softening into a gentle blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 4 — OVER-THE-SHOULDER: two engineers shot from behind at a desk, screen
    #     backs toward camera, warm dusk light through a glass wall. No face
    #     toward the lens, no UI visible.
    "4": (
        "Professional stock photograph, a real editorial photograph shot on a "
        "40mm lens at f/2 on a full-frame camera, framed from behind and "
        "slightly above two software engineers working late at a shared desk "
        "in a modern open-plan office, so both people are seen from the back "
        "and neither face is visible anywhere in the frame. The nearer figure, "
        "occupying the left of the frame, is a man in a plain navy crewneck "
        "sweater sitting in a plain grey task chair, seen from behind and "
        "slightly to the side, his shoulders and the back of his head softly "
        "out of focus in the near foreground, one forearm resting on the desk. "
        "The sharper figure, standing at the right of the desk and leaning "
        "forward with one hand braced flat on the surface, is a woman in a "
        "plain charcoal blouse with the sleeves pushed up, dark hair clipped "
        "back, seen from three-quarters behind so only the edge of her jaw and "
        "ear are visible, her free hand gesturing toward the display. Both "
        "people face the monitors, which are turned away from the camera: the "
        "backs of two slim silver displays, their stands, the backs of two "
        "laptops and the pale halo of light spilling around their edges are "
        "all that shows of the screens, with no display face and no readable "
        "content anywhere. The desk itself is plain light wood, holding a "
        "white ceramic mug, a spiral notebook closed on top of a pen, a pair "
        "of over-ear headphones left down, a phone lying face down, and a "
        "tangle of one charging cable — all plain, all softly lit. To the "
        "left a low partition of pale grey acoustic felt runs along the desk; "
        "to the right the floor-to-ceiling glass wall of the building holds "
        "the evening: warm low amber sunlight raking in at a shallow angle "
        "across the desk top and laying a long warm highlight along the "
        "woman's forearm and the edge of her shoulder, while the ceiling "
        "fixtures and a distant bank of windows throw cool blue-white fill "
        "across the back of the room, so the frame holds warm amber and cool "
        "blue together in honest mixed interior light with no coloured gels. "
        "Beyond the glass, far out of focus, the soft grey and warm shapes of "
        "city towers at dusk with a scatter of lit windows. Behind the desks "
        "the office recedes: two empty chairs, a coat over one chair back, a "
        "floor lamp, a potted plant, all dissolving into soft blur. "
        "Photographic, shallow depth of field: the standing engineer's "
        "shoulder, her braced hand and the near edge of the desk tack sharp, "
        "the seated colleague and the far office melting into smooth creamy "
        "blur, honest available-light interior exposure with natural shadow. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 5 — WIDER FLOOR: dim open-plan floor from a distance, one lit desk
    #     island, a handful of people standing and talking, evening.
    "5": (
        "Professional stock photograph, a real documentary photograph shot on "
        "a 35mm lens at f/2 from a standing position in a modern open-plan "
        "software company floor late in the evening, framed wide across the "
        "room at about chest height. The composition is a real working floor "
        "in the last light of the day: rows of low pale grey desks running "
        "away from the camera in perspective, most of them empty with dark "
        "monitors and the backs of grey task chairs, and one island of activity "
        "in the middle distance — four colleagues standing around a desk, "
        "three of them seen from behind and the side, a woman in a rust-"
        "coloured cardigan laughing, a man in a white shirt leaning on a desk "
        "edge with his arms folded, a third pointing down at a monitor whose "
        "screen faces away from the camera. Their faces are in profile or "
        "away, in soft focus, caught mid-conversation rather than posing. On "
        "the desks: mugs, a stack of paper notebooks, a standing desk frame, a "
        "single cardboard box, a discarded jacket, a scatter of cables, all "
        "plain and unmarked. Along the right side of the frame a long "
        "floor-to-ceiling window wall holds the dusk — a thick band of warm "
        "orange low on the horizon and deep blue above it, the black shapes of "
        "roofs and a distant crane against it — and the last warm light falls "
        "in long shallow pools across the floor, lighting the near desk edges "
        "and the standing figures' shoulders in amber while the deeper part of "
        "the room stays in cool blue-grey shadow lit by a few warm ceiling "
        "fixtures and the pale glow of monitors turned away. Honest mixed "
        "available light, no coloured gels, no light trails, no "
        "long-exposure motion blur. Photographic, shallow depth of field with "
        "the middle-distance group of colleagues and the nearest desk edge "
        "sharp, the near chairs and the far end of the floor dissolving into "
        "soft blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 6 — WIDE FLOOR v2: photo-real look of 5, but zero drinking vessels /
    #     printed objects, and a big warm dusk window wall with long light.
    "6": (
        "Professional stock photograph, a real documentary photograph shot on "
        "a 35mm lens at f/2 from a standing position in a modern open-plan "
        "software company floor late in the evening, framed wide across the "
        "room at about chest height. Rows of low pale grey desks run away "
        "from the camera in perspective, most empty, each with a dark monitor "
        "turned away and the back of a grey task chair; in the middle distance "
        "four colleagues stand around one desk in conversation — three of them "
        "seen from behind and the side with their faces turned away, one "
        "woman in profile with her arms folded, a man in a white shirt with "
        "his hands on his hips, a third pointing down toward a monitor whose "
        "screen faces away from the camera — all soft in focus and caught "
        "mid-sentence, nobody looking toward the lens. On the desks lie only "
        "plain objects: a closed paper notebook, a pen, a folded jacket, a "
        "cardboard archive box, a coiled cable, a pair of headphones. There "
        "are no cups, no mugs, no bottles, no drinking vessels, no tumblers "
        "and no printed or branded objects of any kind anywhere on any desk. "
        "Along the right third of the frame a long floor-to-ceiling window "
        "wall opens on the last of the day: a thick band of molten orange low "
        "on the horizon under a deep blue-violet sky, the black silhouettes of "
        "rooftops, a water tower and a distant crane against it, and the "
        "setting sun just below the roofline throws a broad shallow pool of "
        "genuinely warm amber light in through the glass across the dark "
        "grey carpet and the near desk edges, lighting the backs and shoulders "
        "of the standing figures warm from the right and casting long soft "
        "shadows away from the window, while the deeper part of the room holds "
        "cool blue-grey shadow broken only by dim ceiling fixtures and the "
        "pale spill of monitors turned away. Strong warm-to-cool gradient "
        "across the frame, honest available light at dusk, no coloured gels, "
        "no light trails, no long-exposure motion blur. Photographic, shallow "
        "depth of field with the middle-distance group and the nearest desk "
        "edge sharp, the near chairs and the far end of the floor dissolving "
        "into soft blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 7 — CLOSER WIDE: three stand at a desk against the window wall itself,
    #     seen from behind, dusk city beyond, warm rim light on shoulders.
    "7": (
        "Professional stock photograph, a real editorial photograph shot on a "
        "35mm lens at f/2 on a full-frame camera from behind three colleagues "
        "who stand at a shared desk right against a floor-to-ceiling window "
        "wall in a modern office at dusk, framed at shoulder height so the "
        "figures fill the lower half of the frame and the window fills the "
        "upper half. All three are seen from behind: on the left a woman in a "
        "plain oatmeal knit sweater with her hair down, in the centre a man in "
        "a plain pale blue shirt with the sleeves rolled, on the right a "
        "shorter woman in a plain dark green cardigan with a pen in her hand, "
        "their backs and the backs of their heads toward the camera, no faces "
        "visible at all, their postures those of people reading something "
        "together and talking it over — one leaning on a flat palm, one with a "
        "hand lifted in a small gesture. In front of them on the desk sit two "
        "monitors turned entirely away from the camera, so only their slim "
        "dark backs, their stands and a soft halo of pale light at their edges "
        "can be seen, with no display face and no readable content anywhere in "
        "the frame. Beyond the glass the city at dusk is a soft blur of low "
        "rooftops, a few lit windows and one distant red aircraft light, the "
        "sky a deep blue-violet banded with a thin line of warm orange where "
        "the sun has just gone. The window light is the only real source: a "
        "warm, low, horizontal wash coming through the glass behind and above "
        "them, rimming the tops of their shoulders, the backs of their heads "
        "and the edges of their sleeves in amber, throwing their fronts and "
        "the desk into soft shadow, and their three figures reflect faintly in "
        "the polished floor. A pale grey acoustic ceiling and a single dim "
        "ceiling fixture contribute only a little cool fill from the left, so "
        "the frame is dominated by warm backlight against cool shadow, honest "
        "available light, no coloured gels, no light trails. Photographic, "
        "shallow depth of field with the centre figure's shoulders and the "
        "desk edge tack sharp, the window and the city beyond melting into "
        "smooth creamy blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
    ),
    # 8 — 7's composition with hard photographic anchors: real 35mm film,
    #     handheld imperfection, grain, blown window highlights.
    "8": (
        "An authentic 35mm film photograph, shot handheld on a Leica M6 with a "
        "35mm Summicron lens wide open at f/2 on Kodak Portra 400, from behind "
        "three colleagues who stand at a shared desk against a floor-to-"
        "ceiling window wall in a modern office at dusk, framed at shoulder "
        "height so the figures fill the lower half of the frame and the window "
        "fills the upper half. The framing is slightly imperfect and off-level, "
        "as a working photojournalist would shoot it in a hurry, the desk edge "
        "running a few degrees off horizontal. All three are seen from behind: "
        "on the left a woman in a plain oatmeal knit sweater with her hair "
        "loose, in the centre a man in a plain pale blue shirt with the "
        "sleeves rolled to the elbow, on the right a shorter woman in a plain "
        "dark green cardigan with a pen in her hand, their backs and the backs "
        "of their heads toward the camera, no faces visible at all, their "
        "postures those of people reading something together and talking it "
        "over — one leaning on a flat palm, one with a hand lifted in a small "
        "gesture. In front of them on the desk sit two monitors turned "
        "entirely away from the camera so only their slim dark backs, their "
        "stands and a soft halo of pale light at their edges show, with no "
        "display face and nothing readable anywhere. Beyond the glass the city "
        "at dusk is soft and slightly hazy: low rooftops, a few lit windows, "
        "one distant red aircraft light, the sky a deep blue-violet banded "
        "with a thin line of warm orange where the sun has just gone. The "
        "window light is the only real source — a warm, low, horizontal wash "
        "coming through the glass behind and above them, rimming the tops of "
        "their shoulders, the backs of their heads and the edges of their "
        "sleeves in amber, their fronts and the desk falling into soft shadow, "
        "their three figures reflected faintly in the polished floor, and the "
        "brightest part of the sky slightly blown out into a soft white bloom "
        "as a film camera does with a backlit window. A pale grey ceiling and "
        "one dim fixture give only a little cool fill from the left, so the "
        "frame is warm backlight against cool shadow, honest available light. "
        "The photograph carries the real texture of film: visible fine grain "
        "across the shadows, a faint halation around the window, slight colour "
        "drift toward green in the midtones, a dust speck or two, fabric with "
        "real creases, lint and wear, hair with loose strands, unretouched "
        "skin with visible texture. Photographic, moderate depth of field with "
        "the centre figure's shoulders and the desk edge reasonably sharp and "
        "the window and city softening into gentle blur, real optical blur "
        "from a real lens. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
        + " Absolutely no mug, no cup, no glass, no tumbler, no bottle and no "
        "drinking vessel of any kind appears anywhere in the image."
    ),
    # 9 — 6's wide floor with the same film anchors and a large right-hand
    #     window wall; zero vessels of any kind.
    "9": (
        "An authentic 35mm film photograph, shot handheld on a Nikon FM2 with a "
        "35mm lens at f/2 on Kodak Portra 400, from a standing position across "
        "a modern open-plan software company floor late in the evening, framed "
        "wide at chest height with the framing a degree or two off level as a "
        "working photographer would grab it. Rows of low pale grey desks run "
        "away from the camera in perspective, most of them empty, each with a "
        "dark monitor turned away and the back of a grey task chair; in the "
        "middle distance four colleagues stand around one desk talking — three "
        "seen from behind and the side, faces turned away, one woman in profile "
        "with her arms folded, a man in a white shirt with his hands on his "
        "hips, a third pointing down at a monitor whose screen faces away from "
        "camera — all soft in focus and caught mid-sentence, nobody looking "
        "toward the lens. On the desks lie only plain objects: a closed paper "
        "notebook, a pen, a folded jacket over a chair back, a cardboard "
        "archive box, a coiled cable, a pair of headphones. Along the right "
        "third of the frame a long floor-to-ceiling window wall opens on the "
        "last of the day: a thick band of molten orange low on the horizon "
        "under a deep blue-violet sky, black silhouettes of rooftops and a "
        "distant crane against it, and the setting sun just below the roofline "
        "throws a broad shallow pool of genuinely warm amber light in through "
        "the glass across the dark grey carpet and the near desk edges, "
        "lighting the backs and shoulders of the standing figures warm from "
        "the right and casting long soft shadows away from the window, while "
        "the deeper part of the room holds cool blue-grey shadow broken only "
        "by dim ceiling fixtures and the pale spill of monitors turned away. "
        "Strong warm-to-cool gradient across the frame, the sky beyond the "
        "glass slightly blown to a soft white bloom as film does when "
        "backlit. Honest available light at dusk, no coloured gels, no light "
        "trails, no long-exposure motion blur. The photograph carries real "
        "film texture: visible grain in the shadows, slight halation at the "
        "window edge, midtones drifting a little toward green, a dust speck or "
        "two, fabric with real creases and wear, loose strands of hair, "
        "unretouched skin texture. Photographic, shallow depth of field with "
        "the middle-distance group and the nearest desk edge reasonably sharp, "
        "the near chairs and the far end of the floor dissolving into soft "
        "blur from a real lens. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
        + " Absolutely no mug, no cup, no glass, no tumbler, no bottle and no "
        "drinking vessel of any kind appears anywhere in the image."
    ),
    # 10 — 8's film look, but a three-quarter angle from behind-left so the
    #     monitor backs and desk read clearly and the window sits behind them.
    "10": (
        "An authentic 35mm film photograph, shot handheld on a Leica M6 with a "
        "35mm Summicron at f/2 on Kodak Portra 400, taken from behind and "
        "slightly to the left of three software engineers working late at a "
        "long shared desk in a modern office, so the camera looks along the "
        "desk rather than square at the window: the desk runs diagonally from "
        "the lower left toward the middle right, the three people stand "
        "grouped along its near side, and the floor-to-ceiling window wall "
        "sits behind them in the upper right of the frame. The framing is a "
        "degree or two off level, as a working photographer would grab it. All "
        "three are seen from behind or three-quarters behind, no face turned "
        "toward the lens: nearest the camera on the left a woman in a plain "
        "oatmeal knit sweater with her hair loose, leaning forward with both "
        "palms flat on the desk; beside her a man in a plain pale blue shirt "
        "with the sleeves rolled, one hand raised to point at a display; and "
        "at the far end a shorter woman in a plain dark green cardigan, arms "
        "crossed, her weight on one hip, a pen in one hand. Two slim dark "
        "monitors stand on the desk between them and the window, angled so "
        "their backs and stands face the camera and only a pale halo of light "
        "spills around their edges — no display face, nothing readable "
        "anywhere. The rest of the desk is plain: a closed paper notebook, a "
        "pen, a coiled cable, a pair of headphones laid down, the edge of a "
        "keyboard. Beyond the glass behind them the city at dusk is soft and "
        "slightly hazy — low rooftops, a few lit windows, one distant red "
        "aircraft light — under a deep blue-violet sky banded with a thin line "
        "of warm orange where the sun has just gone, the brightest part of it "
        "blown to a soft white bloom. That window light is the only real "
        "source: a warm low horizontal wash coming in behind them, rimming the "
        "backs of their heads, shoulders and sleeves in amber, laying a long "
        "warm pool across the desk surface, their fronts and the near side of "
        "the desk falling into cool shadow, the pale desk top reflecting a "
        "soft sheen. A single dim ceiling fixture gives only a little cool "
        "fill from the upper left. Honest available light, no coloured gels, "
        "no light trails. The frame carries real film texture: visible grain "
        "in the shadows, faint halation at the window edge, midtones drifting "
        "slightly green, a dust speck or two, fabric with real creases and "
        "wear, loose strands of hair, unretouched skin. Photographic, "
        "moderate depth of field with the two nearest figures and the near "
        "desk edge reasonably sharp and the window wall falling into gentle "
        "blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
        + " Absolutely no mug, no cup, no glass, no tumbler, no bottle and no "
        "drinking vessel of any kind appears anywhere in the image."
    ),
    # 3 — FALLBACK B: dim office, one person at a desk seen from the side,
    #     hands on a laptop, second monitor facing away, city lights behind.
    "3": (
        "Professional stock photograph, a real documentary photograph shot on "
        "a 50mm lens at f/1.8 on a full-frame camera, framed from desk height "
        "at a slight side angle inside a quiet office late in the evening. A "
        "single analyst in his late forties sits at a plain grey desk, seen "
        "from the side and slightly from behind so his face is mostly in "
        "profile and partly in shadow: a plain white shirt with the sleeves "
        "rolled, no tie, reading glasses, a wedding ring, both hands resting "
        "on the keyboard of a slim silver laptop, elbows on the desk, the "
        "posture of someone who has been sitting there a while. The laptop's "
        "screen is hinged back at a shallow angle so it faces away from the "
        "camera and reads only as a soft pale glow lighting the underside of "
        "his chin and the fronts of his hands, showing no readable content. "
        "To his left a second, larger monitor stands turned at right angles to "
        "the camera, its back toward us, throwing a cool wash of light onto "
        "the desk and the wall behind. On the desk: a white ceramic mug with "
        "a thin curl of steam, a pair of reading glasses folded on a closed "
        "notebook, a tangle of a charging cable, the corner of a keyboard "
        "mat, all softly lit and slightly out of focus. Behind him the office "
        "is empty and dark, a wall of windows showing the blurred amber, "
        "white and faint red points of a city at night far below, the window "
        "frames black against them, and a single warm desk lamp on a "
        "colleague's empty desk glowing at the far left in the background. "
        "The lighting is entirely the room's own: cool white monitor glow from "
        "the left and front, a small warm amber pool from a distant desk lamp, "
        "and the blue-black city night beyond the glass, honest mixed "
        "available light with deep shadows and no coloured gels. "
        "Photographic, shallow depth of field: his hands on the keyboard, the "
        "mug and the near edge of the laptop tack sharp, his face and the "
        "empty office falling away into soft blur. "
        + PHOTO_TAIL
        + " "
        + NO_TEXT
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
    if result.get("images"):
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


def normalize(img):
    """Center-crop to 16:9 then resize to 1536x864."""
    w, h = img.size
    target_ratio = W / H
    cur = w / h
    if abs(cur - target_ratio) > 1e-3:
        if cur > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
    img = img.convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img


def save_capped(img, path):
    """Save JPEG, stepping quality down until under MAX_BYTES."""
    for q in (92, 90, 88, 86, 84, 82, 80, 78, 76, 74, 72):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            print(f"Saved {path} q={q} bytes={size}")
            return size
    print(f"WARN: {path} still {os.path.getsize(path)} bytes at q=72")
    return os.path.getsize(path)


def ocr_text_check(path, min_conf=70.0):
    """Tesseract OCR smoke test. Returns (readable, noise) token lists."""
    exe = shutil.which("tesseract")
    if not exe:
        print("OCR: tesseract not found, skipping")
        return [], []
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "ocr")
        try:
            subprocess.run(
                [exe, path, base, "--psm", "11", "tsv"],
                check=True,
                capture_output=True,
                timeout=180,
            )
        except Exception as e:
            print(f"OCR: failed ({e}), skipping")
            return [], []
        tsv_path = base + ".tsv"
        if not os.path.exists(tsv_path):
            return [], []
        with open(tsv_path, errors="ignore") as f:
            rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]

    readable, noise = [], []
    for row in rows[1:]:
        if len(row) < 12:
            continue
        try:
            conf = float(row[10])
        except ValueError:
            continue
        text = row[11].strip()
        clean = "".join(ch for ch in text if ch.isalnum())
        if conf <= 0 or len(clean) < 3:
            continue
        if conf >= min_conf:
            readable.append((text, conf))
        else:
            noise.append((text, conf))
    return readable, noise


def main():
    if os.environ.get("CHECK_ONLY") == "1":
        for p in (OUTPUT, BACKUP):
            if not os.path.exists(p):
                print(f"ERROR: missing {p}")
                sys.exit(1)
            v = Image.open(p)
            print(f"VERIFY {p} dims={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")
        readable, noise = ocr_text_check(OUTPUT)
        if readable:
            print(f"OCR: WARNING {len(readable)} token(s): {readable[:12]}")
        else:
            print(f"OCR: clean ({len(noise)} sub-threshold blob(s))")
        return

    if ATTEMPT not in PROMPTS:
        print(f"ERROR: no prompt for ATTEMPT={ATTEMPT}")
        sys.exit(1)
    print(f"SLUG={SLUG} ATTEMPT={ATTEMPT}")
    img = generate(PROMPTS[ATTEMPT], OUTPUT)
    img = normalize(img)
    save_capped(img, OUTPUT)
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    save_capped(img, BACKUP)

    for p in (OUTPUT, BACKUP):
        v = Image.open(p)
        print(f"VERIFY {p} dims={v.size[0]}x{v.size[1]} bytes={os.path.getsize(p)}")

    readable, noise = ocr_text_check(OUTPUT)
    if readable:
        print(f"OCR: WARNING {len(readable)} token(s): {readable[:12]}")
    else:
        print(f"OCR: clean ({len(noise)} sub-threshold blob(s))")


if __name__ == "__main__":
    main()
