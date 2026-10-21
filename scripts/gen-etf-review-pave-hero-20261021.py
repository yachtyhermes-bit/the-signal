#!/usr/bin/env python3
"""Generate hero for etf-review-pave-2026-10-21 (fal flux/schnell).

Article: "The ETF Review: PAVE — Global X U.S. Infrastructure Development ETF"
A passive, rules-based fund holding US companies that build, repair and
maintain physical infrastructure: roads, bridges, water, electrical grids,
heavy equipment, steel and concrete. The picture must read as a sober
editorial still life about the physical business of building things — NOT a
construction-site advert, NOT a data centre, NOT a trading screen.

Scene chosen (deliberately different from previous ETF Review heroes):
a worn wooden drafting table in soft morning window light with a rolled-up
blueprint (abstract line-work only), a plain metal engineer's straightedge,
a small brass plumb bob, and a plain pale concrete/steel structural scale
model of a simple portal frame. Tidy, editorial, magazine-grade, shallow
depth of field.

Deliberately NOT a repeat of:
- etf-review-spmo-2026-09-23 — top-down card stacks + brass paperweight.
- etf-review-shld-2026-09-30 — olive canvas pouch + brass rod + paper roll.
- the brass balance scale hero, the plain unmarked booklets with coffee hero.
- any data-centre hallway, server aisle, neon/synthwave, abstract art or
  legible chart.

Rules (per repo regen lessons):
- PHOTO-REALISTIC editorial stock photograph ONLY.
- NO people at all: no faces, no hands, no arms, no fingers, no body parts.
- TEXT-FREE: blueprints are the classic flux trap and get fake lettering and
  dimension callouts. Every blueprint in every prompt is specified as pure
  abstract line-work — straight and curved construction lines, arcs and
  simple geometric shapes only, with no annotations, no dimensions, no
  title block, no border lettering.
- No graduated ruler (flux draws tick marks and unit labels): the straightedge
  is a plain smooth unmarked bar of matte steel.
- Generate 1440x810, finalize 1920x1080 center-crop, JPEG q92.

Usage: ATTEMPT=1 /home/chino/video-venv/bin/python3 scripts/gen-etf-review-pave-hero-20261021.py
"""
import os
import shutil
import sys

import requests
from PIL import Image

SLUG = os.environ.get("SLUG", "etf-review-pave-2026-10-21")
ATTEMPT = os.environ.get("ATTEMPT", "1")
OUTPUT = "/home/chino/thesignal/public/img/articles/" + SLUG + ".jpg"
BACKUP = "/home/chino/thesignal/_backup_dist/img/articles/" + SLUG + ".jpg"
W, H = 1440, 810  # 16:9 generation size
FINAL_W, FINAL_H = 1920, 1080

NO_TEXT = (
    "The entire scene is completely free of any lettering and free of any "
    "person: no people at all, no person, no human, no face, no head, no "
    "hands, no fingers, no arms, no wrists, no shoulders, no body parts of "
    "any kind anywhere in the frame or at the edges of the frame. No text, "
    "no letters, no words, no numbers, no digits, no prices, no percentages, "
    "no currency symbols, no ticker symbols, no charts, no graphs, no axis "
    "labels, no brand names, no company names, no fund names, no catalogue "
    "numbers, no part numbers, no serial numbers, no logos, no trademarks, "
    "no monograms, no watermarks, no signatures, no barcodes, no QR codes, "
    "no labels, no tags, no stickers, no stamps, no seals, no newspaper, no "
    "magazine, no headlines, no book spines, no titles, no handwriting, no "
    "print, no printed marks, no engraved marks, no embossed marks, no ruled "
    "lines, no lined paper, no grid paper, no graph paper, no squared paper, "
    "no legible or illegible writing and no drawn symbols of any kind "
    "anywhere in the image. "
    "The blueprint drawings are pure abstract line-work only: plain thin "
    "straight construction lines, simple curves and arcs, and a few blunt "
    "geometric shapes such as rectangles and circles, drawn in pale blue "
    "ink on plain paper, with absolutely no annotation, no dimension lines, "
    "no leader lines, no arrows, no lettering, no numerals, no title block, "
    "no border text, no reference grid and no notes of any kind — lines and "
    "shapes only, reading as quiet abstract geometry. "
    "The metal straightedge is a plain smooth solid bar of matte steel with "
    "no graduations, no tick marks, no hash marks, no measurement scale, no "
    "numerals, no unit abbreviations such as CM, MM or INCH, no engraved "
    "marks and no lettering of any kind, never a graduated ruler and never a "
    "measuring instrument with markings. "
    "There is no readable or unreadable typography anywhere on any surface, "
    "no writing on the wooden table, no names carved into the wood, no "
    "stencilled characters on the concrete model. "
    "No illustration, no digital art, no cartoon, no calligraphy, no "
    "typographic pattern, no 3D render, no CGI, no neon, no glowing lines, "
    "no light trails, no synthwave, no geometric pattern wallpaper, no chart "
    "graphics, no futuristic HUD graphics, no hologram, no floating overlay "
    "elements, no augmented reality graphics, no data center, no server room, "
    "no server racks, no cable runs, no server lights, no trading floor, no "
    "ticker screen, no stock chart display, no construction site, no "
    "scaffolding, no cranes, no excavators, no hard hats, no high-visibility "
    "vests, no safety signage, no vehicles, no flags."
)

BLUEPRINT = (
    "The rolled blueprint shows only abstract drafting line-work: faint pale "
    "blue lines forming simple geometric construction shapes, a few plain "
    "rectangles and one or two gentle arcs, no annotations of any kind, no "
    "dimensions, no arrows, no lettering and no title block, the lines "
    "fading softly where the paper curls away. "
)

PROMPTS = {
    # 9 — SHIPPED (2026-10-21). This is the prompt behind the delivered hero.
    #
    # What the earlier attempts taught, in order:
    #  1,4,5,6,7,8  flat unrolled paper on a desk => flux invents fake dimension
    #               text / squiggles / red marks and inserts a pencil or stylus.
    #  7            paper filling the frame => the plumb bob disappears entirely.
    #  A,B,D,E,F    concrete scale models read as decorative pedestals/benches,
    #               never as infrastructure (2-5/10 from the QA pass).
    #  G,H,I        steel/overpass close-ups => plate stencils, a road sign
    #               arrow, a stray "spider" scribble.
    #  J,N,N2       wide bridge scene => silhouetted figures on the deck, then
    #               an impossible truss-through-pier joint at the left pier.
    #  Q,Q2,Q3      overpass underside => utility boxes, signs, cars, lane paint.
    #  T2           coherent, but a yellow diamond warning sign on the pier.
    #
    # T1 (below) won: the truss is framed with NO ends, piers or abutments in
    # shot, so there is no joint to get wrong, no ground plane for cars or
    # signs, and the lattice dissolves into mist at the right edge.
    "9": (
        "Editorial landscape photograph, fine 35mm film grain, soft flat dawn "
        "light behind thin high overcast, a long riveted steel truss bridge "
        "over a calm misty river. The bridge is shown close and continuous: "
        "the lattice of diagonal steel members and gusset plates runs unbroken "
        "right across the frame from the left edge to the right edge with no "
        "bridge ends, no piers and no abutments visible, filling the upper "
        "half of the frame, weathered dark grey-green paint worn thin with "
        "warm rust at the rivet heads. Below it still pale water holds a soft "
        "dissolving reflection in the mist, and beyond, bare trees fade into "
        "cool grey haze under a pale even sky. Deep tonal detail in the steel, "
        "quiet and monumental, no people, no figures, no text, no signs, no "
        "vehicles, photorealistic, 16:9."
    ),
    # 8 — balanced two-object composition: brass plumb bob sharp in the left
    # foreground, unrolled blueprint running diagonally through the right two
    # thirds, objects nearly touching so there is no bare desk for flux to
    # populate with a pencil. Film-stock language kept for realism.
    "8": (
        "A real 35mm film photograph shot on Kodak Portra 400, scanned from "
        "the negative with its natural grain and gentle halation, an editorial "
        "still life photographed at a low three-quarter angle just above the "
        "surface of a worn wooden drafting table on a 50mm lens at f/2.0, in "
        "an empty quiet studio. In the sharp left foreground lies a small "
        "brass plumb bob on its side: a solid pointed teardrop of dull "
        "tarnished brass, its flat end toward the camera with a short thin "
        "cotton cord trailing away from it, a single soft highlight along its "
        "curve, its small shadow on the pale oak. Immediately beside it, "
        "almost touching the brass, a partly unrolled sheet of drawing paper "
        "runs diagonally through the right two thirds of the frame, its roll "
        "still curled at the far end; the flat sheet carries sparse clean "
        "drafting line-work in thin pale-blue ink — one long plain rectangle, "
        "one plain circle and a single straight line — drawn precisely and "
        "evenly, with the rest of the sheet entirely blank: no annotations, "
        "no dimensions, no arrows, no numerals, no title block, no "
        "handwriting, no scribbles, no shading and no stains. The two objects "
        "sit close together at a natural angle with only narrow slivers of "
        "bare wood showing between and around them, and nothing else at all "
        "on the table. Soft diffused morning window light from the left, "
        "quiet and even, no hard shadow edges, the pale oak matte, softly "
        "worn and lightly scratched with honest age. Shallow depth of field "
        "with the brass bob and the near paper crisp, the paper fibres "
        "visible, everything beyond dissolving into smooth creamy optical "
        "blur. Honest available-light exposure, natural film grain "
        "throughout, slight halation in the highlights, faint dust, subtle "
        "vignette, calm sober financial editorial mood, photorealistic, very "
        "high detail, professional editorial stock photography, 16:9 "
        "landscape composition. Absolutely no people and no hands anywhere in "
        "the frame, no body parts. No pencil, no pen, no stylus, no brush, no "
        "marker, no chalk, no straightedge, no ruler, no tools of any kind, "
        "no compass, no protractor, no coffee cup, no mug, no phone, no "
        "notebook, no glasses, no plant, no window frame, no chair, no "
        "second sheet of paper. No text of any kind anywhere in the image: no "
        "letters, no words, no numbers, no digits, no logos, no watermarks, no "
        "labels, no stickers, no printed marks, no handwriting, no scribbles, "
        "no squiggles, no symbols, no signatures, no stamps, no barcodes, no "
        "graduation or tick marks, no measuring scale, no numerals, no unit "
        "abbreviations, no chart, no graphs, no axis labels. No illustration, "
        "no digital art, no cartoon, no 3D render, no CGI, no plastic sheen, "
        "no glossy surface, no neon, no glowing lines, no synthwave, no "
        "geometric pattern, no HUD, no hologram, no data center, no server "
        "room, no trading floor, no construction site, no hard hats, no "
        "high-visibility vests, no vehicles, no flags, no military insignia."
    ),
    # 7 — frame filled edge-to-edge by the paper itself (no empty desk = no
    # pencil reflex), plumb bob resting on the sheet in the sharp foreground,
    # film-stock language to kill the digital sheen.
    "7": (
        "A real 35mm film photograph shot on Kodak Portra 400, scanned from "
        "the negative with its natural grain and gentle halation, an extreme "
        "close-up taken at a low raking angle almost level with the surface of "
        "a worn wooden drafting table, on a 50mm lens at f/2.0. The unrolled "
        "sheet of drawing paper fills the frame edge to edge, its pale surface "
        "running from the sharp foreground away into soft blur, with its "
        "rolled end lifting and curling up in the out-of-focus background and "
        "only a thin sliver of pale worn oak visible at the bottom right "
        "corner. The sheet carries sparse clean drafting line-work drawn in "
        "thin pale-blue ink: one long plain rectangle, one single plain "
        "circle, and two straight lines running off the edge of the paper, "
        "precise and perfectly even, with the rest of the sheet completely "
        "blank and empty — no annotations, no dimensions, no arrows, no "
        "numerals, no title block, no handwriting, no scribbles, no shading, "
        "no stains, nothing else at all. Resting directly on the paper in the "
        "sharp foreground, a small brass plumb bob lying on its side: a solid "
        "pointed teardrop of dull tarnished brass with a short thin cotton "
        "cord trailing from its flat end, one soft highlight along its curve, "
        "its small shadow falling across the blue lines beside it. Soft "
        "diffused morning window light from the left, quiet and even, no hard "
        "edges. Shallow depth of field with the brass bob and the near paper "
        "texture crisp, the fibres and faint tooth of the paper clearly "
        "visible, falling into smooth creamy optical blur behind. Honest "
        "available-light exposure, natural film grain throughout, slight "
        "halation in the highlights, faint dust, subtle vignette, calm sober "
        "financial editorial mood, photorealistic, very high detail, "
        "professional editorial stock photography, 16:9 landscape composition. "
        "Absolutely no people and no hands anywhere in the frame, no body "
        "parts. No pencil, no pen, no stylus, no brush, no marker, no chalk, "
        "no straightedge, no ruler, no tools of any kind, no compass, no "
        "protractor, no coffee cup, no mug, no phone, no notebook, no glasses, "
        "no plant, no window frame, no chair. No text of any kind anywhere in "
        "the image: no letters, no words, no numbers, no digits, no logos, no "
        "watermarks, no labels, no stickers, no printed marks, no handwriting, "
        "no scribbles, no squiggles, no symbols, no signatures, no stamps, no "
        "barcodes, no graduation or tick marks, no measuring scale, no "
        "numerals, no unit abbreviations, no chart, no graphs, no axis labels. "
        "No illustration, no digital art, no cartoon, no 3D render, no CGI, no "
        "plastic sheen, no glossy surface, no neon, no glowing lines, no "
        "synthwave, no geometric pattern, no HUD, no hologram, no data center, "
        "no server room, no trading floor, no construction site, no hard hats, "
        "no high-visibility vests, no vehicles, no flags, no military insignia."
    ),
    # 6 — plumb bob described FIRST and in the sharp foreground (flux keeps
    # replacing it with a pencil/pen when paper is on a desk), explicit ban on
    # pens, pencils, utensils and in-frame windows, rectangular table only.
    "6": (
        "Photo-realistic editorial stock photograph of a bare wooden drafting "
        "table in soft diffused morning light, shot from a low three-quarter "
        "angle on a 50mm lens at f/2.0 in an empty quiet studio, the plain "
        "straight front edge of the rectangular table crossing the bottom of "
        "the frame and a matte plaster wall behind it falling out of focus, "
        "no window in the frame. In the sharp foreground, lying on its side "
        "on the bare wood, a small brass plumb bob: a solid pointed teardrop "
        "of dull tarnished brass with a short thin cotton cord trailing from "
        "the flat end, its metal catching one soft highlight. Behind it, a "
        "partly unrolled sheet of drafting paper lies flat on the table with "
        "its roll still curled up behind, the flat sheet showing only four "
        "thin even pale-blue drafting lines that form one long plain "
        "rectangle and one single soft arc, clean precise geometric line-work "
        "on an otherwise completely blank sheet, and nothing else at all on "
        "the paper. Beside the paper lies a plain solid bar of brushed steel, "
        "a smooth matte metal straightedge with a featureless unmarked "
        "surface. The three objects sit loosely grouped at natural angles "
        "with wide calm empty wood around them and never in a perfect line. "
        "The wood is pale oak, matte, softly worn and lightly scratched with "
        "honest age. Soft even morning daylight from the left, one gentle "
        "soft shadow to the right, honest available-light exposure, real "
        "optical lens blur behind, natural camera noise, very slight film "
        "grain, subtle vignette, calm sober financial editorial mood, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. Absolutely no people and no "
        "hands anywhere in the frame, no body parts. No pencil, no pen, no "
        "stylus, no brush, no marker, no chalk, no carving tool, no knife, no "
        "scissors, no tools of any kind, no desk utensils, no coffee cup, no "
        "mug, no glass, no phone, no notebook, no glasses, no plant, no "
        "window frame. No text of any kind anywhere in the image: no letters, "
        "no words, no numbers, no digits, no logos, no watermarks, no labels, "
        "no stickers, no printed marks, no handwriting, no scribbles, no "
        "squiggles, no signatures, no stamps, no barcodes, no graduation or "
        "tick marks on the steel bar, no measuring scale, no numerals, no "
        "unit abbreviations, no chart, no graphs, no axis labels. No "
        "illustration, no digital art, no cartoon, no 3D render, no CGI, no "
        "neon, no glowing lines, no synthwave, no geometric pattern, no HUD, "
        "no hologram, no data center, no server room, no trading floor, no "
        "construction site, no hard hats, no high-visibility vests, no "
        "vehicles, no flags, no military insignia."
    ),
    # 5 — short, front-loaded scene text (schnell dilutes long prompts and
    # drops objects), explicit ban on scribbles/squiggles on the paper.
    "5": (
        "Photo-realistic editorial stock photograph, shot from a low "
        "three-quarter angle on a 50mm lens at f/2.0, of a worn pale oak "
        "drafting table in an empty studio in soft morning window light from "
        "the left, the rounded front edge of the table crossing the lower "
        "frame and a plain plaster wall far behind it out of focus. Three "
        "plain unlabelled objects rest on the bare wood, loosely grouped and "
        "not touching, with calm empty table around them. First, a partly "
        "unrolled roll of drawing paper, its outer sheet lying flat on the "
        "wood with the roll still curled behind it; the flat sheet carries "
        "only six or seven clean thin pale-blue ruled drafting lines forming "
        "one long rectangle and one plain circle, crisp geometric line-work "
        "and nothing else at all, no handwriting, no scribbles, no squiggles, "
        "no pencil shading, no dimension lines, no arrows, no numerals, no "
        "title block, the rest of the sheet completely blank. Second, a solid "
        "plain steel straightedge bar of matte brushed metal with a smooth "
        "featureless unmarked surface. Third, a small tarnished brass plumb "
        "bob, a solid teardrop of dull warm brass with a short cotton cord, "
        "resting on its side in the sharp foreground. Soft even morning "
        "daylight, gentle shadows to the right, honest available-light "
        "exposure, real optical lens blur behind, natural camera noise, very "
        "slight film grain, subtle vignette, calm sober financial editorial "
        "mood, photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition, absolutely no people and no "
        "hands anywhere in frame, no text of any kind anywhere in the image, "
        "no letters, no words, no numbers, no logos, no watermarks, no "
        "labels, no stickers, no printed marks, no wood-burning, no carved "
        "names, no graduation or tick marks on the steel bar, no measuring "
        "scale, no unit abbreviations, no illustration, no digital art, no "
        "cartoon, no 3D render, no CGI, no neon, no glowing lines, no "
        "synthwave, no geometric pattern, no chart graphics, no HUD, no "
        "hologram, no data center, no server room, no trading floor, no "
        "construction site, no hard hats, no high-visibility vests, no "
        "vehicles, no flags, no military insignia."
    ),
    # 4 — anti-floorplan variant: fewer objects, camera low enough that the
    # worn table edge reads clearly, paper mostly still rolled with only a
    # small corner unrolled.
    "4": (
        "A genuine photograph, not a render and not computer generated, shot "
        "hand-held by an editorial photographer from a low side angle about "
        "twenty centimetres above a worn wooden drafting table, on a 35mm "
        "lens at f/2.8, in a quiet empty room with nobody present. The front "
        "edge of the table runs across the bottom of the frame so the picture "
        "is clearly of a table standing in a room, not a flat top-down scan, "
        "and the pale oak surface is matte, softly rounded, lightly scratched "
        "and dull with age, with a plain out-of-focus plaster wall behind it. "
        "Resting on the table, small in the frame and loosely grouped in the "
        "lower left with a wide calm expanse of bare wood around them, are "
        "three completely unlabelled objects: a thick roll of drawing paper "
        "lying on its side with only a small corner of the sheet loosened and "
        "curling up, the visible paper carrying just a handful of very faint "
        "pale blue freehand drafting lines and one soft curve — quiet "
        "abstract line-work on an otherwise blank sheet, not a plan view, not "
        "a floor plan, not an architectural drawing, not a technical diagram, "
        "with no dimension lines, no arrows, no annotations, no numerals, no "
        "lettering and no title block anywhere on it; beside the roll a "
        "plain smooth matte steel straightedge, a simple solid bar of brushed "
        "steel with no ticks, no graduations, no scale and no engraving of "
        "any kind; and just in front of it a small tarnished brass plumb bob "
        "lying on its side, a solid teardrop of warm dull brass with a short "
        "plain cotton cord trailing from its top. Soft diffused morning "
        "daylight comes in gently from the left through an unseen window, "
        "even and undramatic, softly modelling the curl of the paper, the "
        "satin steel and the tarnished brass and casting one soft diffuse "
        "shadow to the right. The far end of the table and the wall behind "
        "dissolve into smooth creamy out-of-focus daylight and shadow. "
        "Shallow depth of field with the paper curl, the steel edge and the "
        "brass bob crisp and everything behind softening into real optical "
        "blur, honest available-light editorial exposure, natural camera "
        "noise, very slight film grain, subtle lens vignette, calm unhurried "
        "financial editorial mood, no plastic CGI sheen, no glossy render, no "
        "perfect symmetry, no 3D visualisation, no digital illustration, "
        "photorealistic, very high detail, professional editorial stock "
        "photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 1 — low three-quarter across a worn drafting table, morning light from
    # the left, blueprint roll + steel straightedge + plumb bob + concrete
    # portal-frame model.
    "1": (
        "Photo-realistic editorial stock photograph, not a render and not "
        "computer generated, shot at eye level in a low three-quarter view "
        "across a worn wooden drafting table on a 50mm lens at f/2.0 on a "
        "full-frame camera, in a quiet empty studio room with nobody present. "
        "The table is old and honest: pale worn oak with a fine matte grain, "
        "softly rounded edges, faint ink smudges and light scratches from "
        "decades of use, and a shallow angled drawing surface tilted just "
        "slightly toward the camera. On it sit four quiet, completely "
        "unlabelled objects: a rolled-up blueprint lying diagonally across "
        "the middle of the table with its paper curling open at one end, "
        "showing " + BLUEPRINT + "a plain smooth matte steel straightedge "
        "lying flat beside it, a simple featureless solid bar of dull brushed "
        "steel with no markings of any kind, a small brass plumb bob resting "
        "on its side near the front edge, a solid teardrop of warm tarnished "
        "brass with a short plain cotton cord trailing from its top, and at "
        "the back right a small plain structural scale model of a simple "
        "portal frame — two uprights and one beam in pale matte concrete and "
        "unpainted steel, geometric and completely blank, casting a small "
        "soft shadow. The objects sit at natural, slightly varied angles, "
        "close together but not touching, with calm empty table around them. "
        "Soft morning window light falls in low and warm from the left, "
        "quiet early daylight through an unseen window, grazing the curled "
        "edge of the blueprint and laying one long soft shadow to the right "
        "across the wood. Behind the table the room dissolves into smooth "
        "creamy out-of-focus daylight and shadow. Shallow depth of field, "
        "the paper curl, the steel bar and the brass plumb bob crisply sharp "
        "nearest the camera and the concrete model already softening, real "
        "optical lens blur, honest available-light editorial exposure, "
        "natural camera noise, very slight film grain, subtle lens vignette, "
        "calm unhurried financial editorial mood, no plastic CGI sheen, no "
        "glossy render, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
        + NO_TEXT
    ),
    # 2 — slightly higher three-quarter, light from the right, tighter on the
    # blueprint and plumb bob, more negative space.
    "2": (
        "A genuine photograph, not a render and not computer generated: a "
        "medium close three-quarter view from slightly above the surface of "
        "a worn wooden drafting table, shot on an 85mm lens at f/1.8, in an "
        "empty room with no one in frame. The table is pale aged oak, matte "
        "and slightly scuffed with honest wear, its rounded front edge "
        "crossing the lower frame. Four plain unlabelled objects rest on it: "
        "a partially unrolled blueprint filling the centre of the table with "
        "its far edge curling up off the wood, the paper showing only "
        "abstract pale blue drafting line-work — thin straight lines, a few "
        "rectangles, one gentle arc, no lettering, no dimensions, no arrows, "
        "no title block — a plain smooth matte steel straightedge lying at a "
        "slight diagonal in front of it, a solid featureless bar of brushed "
        "steel with no graduations, no ticks and no numbers, a small tarnished "
        "brass plumb bob standing on its pointed tip beside the paper with a "
        "short cotton cord coiled loosely around it, and in the right third "
        "of the frame a small blank concrete and steel scale model of a "
        "simple two-post frame, plain and geometric, its surfaces matte and "
        "unmarked. Warm low morning window light comes in from the right, "
        "softly grazing the curl of the paper and catching the satin metal of "
        "the straightedge, casting one soft long shadow to the left. The "
        "background falls away into an out-of-focus wash of quiet warm "
        "daylight and blurred dark wood. Extremely shallow depth of field "
        "with the paper edge and the brass bob sharp and real optical blur "
        "everywhere else, honest editorial exposure, natural camera noise, "
        "very slight film grain, subtle lens vignette, sober calm mood, no "
        "plastic CGI sheen, no glossy render, no perfect symmetry, no 3D "
        "visualisation, no digital illustration, photorealistic, very high "
        "detail, professional editorial stock photography, 16:9 landscape "
        "composition. "
        + NO_TEXT
    ),
    # 3 — scanned 35mm film feel, low angle along the table, wide calm empty
    # wood, objects small in the lower left, diffused overcast light.
    "3": (
        "An ordinary unretouched 35mm film photograph, scanned straight from "
        "the negative with its natural grain, not a render and not computer "
        "generated and not a digital illustration, shot hand-held from a low "
        "three-quarter angle just above the surface of a worn wooden drafting "
        "table on a 35mm lens at f/2.8, in a quiet empty room with nobody "
        "present. The table is clearly a work table: its softly rounded front "
        "edge crosses the lower part of the frame, the pale oak is matte, "
        "slightly scuffed and dull with age and honest wear, and behind it a "
        "plain plaster wall falls away out of focus. On the table lie four "
        "completely unlabelled objects: a rolled blueprint lying flat with "
        "one end unrolled and curling open, its surface carrying only "
        "abstract pale blue drafting lines and a couple of plain geometric "
        "shapes with no lettering, no numbers and no annotations at all, a "
        "plain smooth matte steel straightedge lying flat alongside it, a "
        "simple featureless solid bar of dull steel with no ticks, no scale "
        "and no engraving, a small warm brass plumb bob resting on its side "
        "with a short loose cotton cord, and a small pale concrete and steel "
        "scale model of a simple rectangular frame standing quietly at the "
        "back. The objects sit small and quiet in the lower left of frame, "
        "loosely grouped and natural, with a large calm expanse of bare matte "
        "wood around them and never arranged in a perfect line. Soft diffused "
        "overcast morning daylight falls in from the left through an unseen "
        "window, gentle and even with no hard focused window-pane shapes, "
        "softly modelling the dull paper, the matte steel and the tarnished "
        "brass and leaving one soft diffuse shadow to the right. The far end "
        "of the table and the wall behind dissolve into smooth creamy "
        "out-of-focus daylight and shadow. Moderate shallow depth of field "
        "with the paper and the straightedge crisp and the model and the "
        "table edge softening, real optical blur, honest available-light "
        "exposure with visible 35mm film grain throughout, matte surfaces "
        "with no gloss or sheen, subtle lens vignette, unhurried sober "
        "financial editorial mood, empty room with no human figure and no "
        "hands, no plastic CGI sheen, no glossy render, no hyper-real "
        "cleanliness, no perfect symmetry, no 3D visualisation, no digital "
        "illustration, photorealistic, very high detail, professional "
        "editorial stock photography, 16:9 landscape composition. "
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
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]
    elif "output" in result:
        image_url = result["output"]
    elif "image" in result:
        image_url = result["image"]
    if not image_url:
        print("ERROR: Could not find image URL in result: " + str(result))
        sys.exit(1)
    print("Image URL: " + image_url)
    r = requests.get(image_url, timeout=120)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    img = Image.open(out_path)
    print("Downloaded: " + out_path + "  size=" + str(img.size)
          + "  bytes=" + str(len(r.content)))
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
        print("ERROR: no prompt for ATTEMPT=" + ATTEMPT)
        sys.exit(1)
    prompt = PROMPTS[ATTEMPT]
    print("SLUG=" + SLUG + " ATTEMPT=" + ATTEMPT)
    img = generate(prompt, OUTPUT)
    img = crop_to_16x9(img)
    img.save(OUTPUT, "JPEG", quality=92, optimize=True)
    size = os.path.getsize(OUTPUT)
    print("Saved final hero: " + OUTPUT + "  dimensions=" + str(img.size)
          + "  bytes=" + str(size))
    if size < 102400:  # <100KB
        img.save(OUTPUT, "JPEG", quality=98, optimize=True)
        print("Re-saved with higher quality: " + str(os.path.getsize(OUTPUT))
              + " bytes")
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    shutil.copy(OUTPUT, BACKUP)
    print("Mirrored to " + BACKUP)

    for p in (OUTPUT, BACKUP):
        im = Image.open(p)
        print("VERIFY " + p + "  dims=" + str(im.size)
              + "  bytes=" + str(os.path.getsize(p)))


if __name__ == "__main__":
    main()
