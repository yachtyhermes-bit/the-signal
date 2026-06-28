#!/usr/bin/env python3
"""Generate a podcast-style conversation between Andrew and Brian discussing a Signal article."""
import asyncio, json, os, re, subprocess, sys, tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTICLE_SLUG = "palantir-surges-ai-factory-dell-partnership"
ANDREW = "en-US-AndrewNeural"
BRIAN = "en-US-BrianNeural"
BRIAN_SPEED = 1.05

OUTPUT = PROJECT_ROOT / "public" / "audio" / f"{ARTICLE_SLUG}-podcast.mp3"

with open(PROJECT_ROOT / "articles" / "posts" / f"{ARTICLE_SLUG}.json") as f:
    art = json.load(f)
title = art.get("title", "")
body_html = art.get("bodyHtml", "")
body_text = re.sub(r"<[^>]+>", " ", body_html)
body_text = re.sub(r"\s+", " ", body_text).strip()

script = [
    (ANDREW, "Welcome back to The Signal. I'm Andrew, and today we're digging into Palantir's big move — up 10 percent after Dell's blowout earnings. Brian, you've been watching this one."),
    (BRIAN, "Yeah Andrew, this is interesting because Dell just posted their Q1 results and shares surged 33 percent. They're projecting 60 billion dollars in AI server sales alone. That's not a typo — sixty billion. And Palantir rode that wave straight up."),
    (ANDREW, "So this isn't just sympathy trading — there's a real connection here. The Dell AI Factory partnership. Dell provides the hardware, Palantir provides the AIP operating system layer. Turnkey AI deployment."),
    (BRIAN, "Exactly. And Alex Karp — Palantir's CEO — described the US commercial business as erupting. The numbers back it up. Revenue hit 1.63 billion dollars, up 85 percent year over year. US commercial revenue crossed 100 percent growth for the first time ever."),
    (ANDREW, "That's the stat that jumps out. 100 percent growth in commercial. Palantir used to be known as the government contractor — all CIA and Pentagon contracts. But commercial is now the accelerant."),
    (BRIAN, "Right. And the Dell partnership removes the biggest friction point in enterprise AI adoption: deployment complexity. Enterprises don't want to piece together servers, networking, and AI software from a dozen vendors. Dell and Palantir give them one box."),
    (ANDREW, "Market cap is around 375 billion. Twenty-seven analysts rate it a Buy with a mean target of 183 dollars. The TTM revenue of 5.2 billion represents 85 percent growth — and that's accelerating, not slowing down. Brian, is this valuation justified?"),
    (BRIAN, "Look, the valuation is rich — it's Palantir, it's always been priced for perfection. But when you have revenue growth accelerating, not decelerating, and a partnership with Dell that gives you enterprise distribution at scale, the premium starts to make more sense. The question is whether they can sustain this pace."),
    (ANDREW, "Net income of 871 million dollars in a single quarter. That's real profit, not just revenue hype. Operating leverage is finally kicking in. For listeners who've been following Palantir since the direct listing, this is the thesis playing out in real time."),
    (BRIAN, "Bottom line — the AI capex cycle hasn't peaked. Dell's guidance proved that. And Palantir is one of the purest ways to play enterprise AI deployment without buying the hardware names. That's The Signal. Thanks for listening."),
    (ANDREW, "Disclosure: The Signal holds no position in Palantir. This is not financial advice. See you next time."),
]

async def gen_segment(voice, text, idx):
    import edge_tts
    tmp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    tmp_path = tmp.name
    tmp.close()
    communicate = edge_tts.Communicate(text, voice)
    with open(tmp_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
    size = os.path.getsize(tmp_path)
    print(f"  Seg {idx}: {voice.split('-')[1]} ({size/1024:.0f} KB)")
    if voice == BRIAN and BRIAN_SPEED != 1.0:
        sped_path = tmp_path.replace(".mp3", "_sped.mp3")
        subprocess.run(["ffmpeg", "-y", "-i", tmp_path, "-filter:a", f"atempo={BRIAN_SPEED}", "-q:a", "2", sped_path],
                       capture_output=True, timeout=30)
        os.unlink(tmp_path)
        sped_size = os.path.getsize(sped_path)
        print(f"  Seg {idx}: sped up ({sped_size/1024:.0f} KB)")
        return sped_path
    return tmp_path

async def main():
    print(f"Generating podcast: {title}\n")
    segments = []
    for i, (voice, text) in enumerate(script):
        path = await gen_segment(voice, text, i)
        segments.append(path)
    print(f"\n  Concatenating...")
    list_path = "/tmp/podcast_segments.txt"
    with open(list_path, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")
    result = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path, "-c", "copy", str(OUTPUT)],
                           capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        size = os.path.getsize(OUTPUT)
        print(f"\n✅ Podcast: {OUTPUT} ({size/1024:.0f} KB)")
    else:
        print(f"✗ Error: {result.stderr[:200]}")
    for seg in segments:
        os.unlink(seg)
    os.unlink(list_path)

asyncio.run(main())
