#!/usr/bin/env python3
"""Normalize British spellings to US in the LMT AIR6500 article + fix hero caption.

The Signal publishes US English (110 articles use 'defense', only a handful use
'defence'). aspell (scripts/aspell_check.py) flags British variants as
misspellings, so the fact-check crons would raise them.

Rule: replace 'defence' -> 'defense' and 'centre(s)' -> 'center(s)' in every
text field EXCEPT the proper noun 'Department of Defence' (official Australian
government department name, must stay spelled that way).

Also rewrites image.caption/alt to describe the ACTUAL hero image, which is a
ground-based air-defence radar array on a trailer on a coastal road at dawn
(not an operations centre with consoles).
"""
import json
import re

PATH = "/home/chino/thesignal/articles/posts/lmt-australia-air-battle-management-2026.json"

with open(PATH) as f:
    a = json.load(f)

PROTECT = "\x00DEPT\x00"


def fix(text):
    if not isinstance(text, str):
        return text
    t = text.replace("Department of Defence", PROTECT)
    t = t.replace("Defence", "Defense").replace("defence", "defense")
    t = t.replace("Centres", "Centers").replace("centres", "centers")
    t = t.replace("Centre", "Center").replace("centre", "center")
    t = t.replace(PROTECT, "Department of Defence")
    return t


changed = []
for key in ("title", "subtitle", "summary", "bodyHtml"):
    if key in a and isinstance(a[key], str):
        new = fix(a[key])
        if new != a[key]:
            changed.append(key)
            a[key] = new

if "image" in a:
    a["image"]["caption"] = (
        "A ground-based air-defence radar array on a coastal road at dawn - the "
        "sensor layer Australia's new battle-management software is built to fuse. "
        "Photo: The Signal / AI-generated."
    )
    a["image"]["alt"] = (
        "Ground-based military air-defence radar array on a trailer beside a coastal "
        "road at dawn, unmarked support vehicle nearby"
    )
    # keep US spelling in the caption/alt too
    a["image"]["caption"] = fix(a["image"]["caption"])
    a["image"]["alt"] = fix(a["image"]["alt"])

# tags / meta keyword spot check
for i, t in enumerate(a.get("tags", [])):
    a["tags"][i] = fix(t)

with open(PATH, "w") as f:
    json.dump(a, f, indent=2, ensure_ascii=False)
    f.write("\n")

# verify
with open(PATH) as f:
    b = json.load(f)

alltext = json.dumps(b)
print("changed fields:", changed)
print("remaining 'defence' occurrences:", alltext.count("defence"))
print("'Department of Defence' occurrences:", alltext.count("Department of Defence"))
print("'center'/'centers' now:", alltext.count("center") + alltext.count("centers"))
print("caption:", b["image"]["caption"])
print("alt:", b["image"]["alt"])
print("body has backslash-quote corruption:", chr(92) + chr(34) in b["bodyHtml"])
print("stats-card in body:", "stats-card" in b["bodyHtml"])
print("disclosure ok:", '<p class="disclosure">' in b["bodyHtml"])
