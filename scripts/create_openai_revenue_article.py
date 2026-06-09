#!/usr/bin/env python3
"""Create the OpenAI revenue miss article JSON for The Signal."""
import json
import os

article = {
    "slug": "openai-revenue-miss-june-2026",
    "title": "OpenAI Can't Hit Its Own Numbers — Right Before the Biggest AI IPO Since Facebook",
    "subtitle": "The WSJ dropped a bomb: OpenAI missed revenue and user targets. The Nasdaq was already bleeding $1.3 trillion. And Anthropic just filed at a $965B valuation. The contrast is brutal.",
    "summary": "OpenAI missed key revenue and user growth targets as it races toward an IPO, the WSJ reports. With $1.3T wiped out in semis last week and Anthropic filing at $965B, the AI emperor is looking exposed.",
    "ticker": "MSFT",
    "sector": "ai",
    "sentiment": "bearish",
    "date": "2026-06-08T10:00:00.000Z",
    "tags": ["OpenAI", "Artificial Intelligence", "IPO", "Microsoft", "Anthropic", "AI Bubble"],
    "image": {
        "src": "/img/articles/openai-revenue-miss.jpg",
        "caption": "OpenAI's revenue miss casts a shadow over the AI IPO pipeline"
    },
    "links": [
        {"label": "WSJ Report →", "url": "https://www.wsj.com/tech/ai/openai-revenue-targets-ipo-miss-2026"},
        {"label": "Microsoft Stock →", "url": "https://finance.yahoo.com/quote/MSFT"}
    ],
    "videos": [],
    "bodyHtml": (
        "<p>Everyone's been looking at last week's AI bloodbath and pointing at the jobs report. Or Broadcom's guidance miss. Or whatever macro excuse was handy. But the real story dropped late Sunday — and it's way uglier than anyone wants to admit.</p>"
        "<p><strong>OpenAI missed its own revenue and user growth targets.</strong> The WSJ broke it. The company that <em>is</em> the AI revolution — the one every VC pitch deck references, the one every SaaS company is racing to build on top of — can't even hit the numbers it set for itself. This isn't a rounding error. This is the emperor showing up naked right before the biggest tech IPO in a decade.</p>"

        "<h2>The Timing Couldn't Be Worse</h2>"
        "<p>Let's rewind 72 hours. The Nasdaq just got <strong>obliterated</strong>. <strong>$1.3 trillion</strong> erased in two sessions. Broadcom <strong>-13%</strong> on a guidance flub that made everyone recalculate what \"AI demand\" actually means. The entire semiconductor complex got dragged into a crater. Nvidia, AMD, the whole crew — tossed.</p>"
        "<p>And then Sunday night, the WSJ drops <em>this</em>: OpenAI, the crown jewel of the AI IPO pipeline, missed its targets. Revenue targets. User growth targets. Both. In the middle of the most important fundraising sprint in the company's history.</p>"

        "<blockquote>If the company that <strong>IS</strong> the AI revolution can't hit its own numbers, what does that say about every company building on top of it?</blockquote>"

        "<h2>Anthropic Makes It Look Easy</h2>"
        "<p>Here's where it gets genuinely awkward. While OpenAI is stumbling toward an IPO that Barron's now calls <strong>\"no sure thing,\"</strong> Anthropic just casually filed for a public offering at a <strong>$965 billion valuation</strong> with <strong>$47 billion in annualized revenue</strong>. Morgan Stanley and Goldman are running the books. They're not missing targets — they're blowing past them.</p>"
        "<p>The contrast is brutal. OpenAI had first-mover advantage, the Microsoft partnership, the brand recognition. ChatGPT is a verb. And yet Anthropic is the one filing for an IPO that makes OpenAI's look... uncertain.</p>"

        "<h2>Microsoft's $13 Billion Problem</h2>"
        "<p>Nobody's talking about this enough: <strong>Microsoft</strong> is OpenAI's biggest investor. They've poured something like <strong>$13 billion</strong> into this relationship. Every Azure AI product is built on OpenAI's models. Every Copilot feature. Every enterprise pitch.</p>"
        "<p>If OpenAI's growth is stalling, Microsoft's AI narrative takes a direct hit. The stock's already getting dragged by the broader tech sell-off. Now the crown jewel of their AI strategy looks tarnished. <a href=\"/ticker/MSFT\">$MSFT</a> shareholders should be watching this one closely.</p>"

        "<h2>The Narrative Just Flipped</h2>"
        "<p>For two years, the story was simple: \"AI is the future, buy everything.\" Nvidia sells the picks and shovels, OpenAI builds the brains, everyone else rides the wave. Last week the picks-and-shovels trade cracked. This week, the brains trade just cracked too.</p>"
        "<p>We're now watching \"AI is the future\" collide with \"AI can't even hit its own numbers\" — in real time. That's the narrative flip that matters. Not the Fed. Not CPI. <em>This.</em></p>"
        "<p>The AI trade isn't dead. But for the first time since ChatGPT launched, the valuation story doesn't have clean financials backing it up. And markets hate uncertainty more than they love a good story.</p>"
        "<p><em>— The Signal</em></p>"
    )
}

output_path = "/home/chino/thesignal/articles/posts/openai-revenue-miss-june-2026.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(article, f, indent=2, ensure_ascii=False)

# Verify
with open(output_path, "r", encoding="utf-8") as f:
    verified = json.load(f)

assert verified["slug"] == "openai-revenue-miss-june-2026", "Slug mismatch"
assert verified["bodyHtml"], "bodyHtml is empty!"
assert len(verified["bodyHtml"]) > 500, f"bodyHtml too short: {len(verified['bodyHtml'])} chars"

# Approximate word count (HTML tags stripped roughly)
import re
text = re.sub(r'<[^>]+>', ' ', verified["bodyHtml"])
words = len(text.split())
print(f"✓ Article created successfully")
print(f"  Path: {output_path}")
print(f"  bodyHtml length: {len(verified['bodyHtml'])} chars")
print(f"  Approximate word count: {words}")
print(f"  Slug: {verified['slug']}")
print(f"  Sentiment: {verified['sentiment']}")
