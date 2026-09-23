#!/usr/bin/env python3
import json

paras = [
    "Australia just bought the brain of its air defences. Lockheed Martin is the world's largest defence contractor: it builds the F-35 fighter, missiles and missile-defence systems, helicopters, and the software that ties them together. Its main customer is the Pentagon, plus allied governments like Australia.",
    "Lockheed sells hardware, and increasingly the command layer above it. About 123,000 employees. When a country needs a system to run its entire air battle, only a handful of companies on earth can build one. Lockheed is on that list.",
    "On 9 September, Australia handed Lockheed Martin Australia the next phase of Project AIR6500. That is the Joint Air Battle Management System, or JABMS. The award is worth A$1.32 billion, roughly US$950 million, and sits inside a wider A$2.4 billion six-year push into air and missile defence.",
    "So what is AIR6500? Mostly software. It fuses feeds from warships, aircraft, ground radars and allied networks into one unified picture of the battlespace. Commanders use it to detect, track and counter air and missile threats at various ranges.",
    "Think of it as the brain sitting above the shooters. A destroyer fires the missile. A fighter flies the sortie. The brain decides which threat to engage, with which asset, in seconds.",
    "Tranche 2B adds advanced command-and-control aids, expanded comms and cybersecurity. Lockheed says it establishes a scalable path for rapidly integrating future technology. It must plug into the ADF's targeting enterprise, allies and partners. Platforms in scope include Hobart-class destroyers, the F-35A Lightning II and Australia's accelerated Medium-Range Ground-Based Air Defence system.",
    "The last two years built the foundation. Under Tranche 2A, Lockheed Martin Australia produced the JABMS prototype, two joint tactical operations centres and a single persistent operations node for testing and evaluation. It trained Royal Australian Air Force personnel on the system and completed fit-out of an Air 6500 integration lab in Adelaide.",
    "The scale keeps climbing. Australia has promised A$30 billion over the coming decade for integrated air and missile defence. Lockheed Martin Australia's workforce grows from 360 employees to more than 400 within 18 months. The company has also spent A$85.9 million of its own money on an Air Power Precinct in the Hunter region of New South Wales, operational by 2028.",
    "Here is why the AI sector should care. Modern air defence is turning into a software problem. The hard part is no longer the interceptor. It is fusing radar, ship, aircraft and satellite feeds into one picture and deciding what to shoot, in seconds, faster than a human can.",
    "That is exactly the command-and-control and sensor-fusion layer where AI is moving into defence. It is the same battle-network race Palantir, Anduril and the primes are all fighting over, exported to allies through programs like AIR6500. Lockheed is repositioning as a software-and-systems integrator, not just a metal-bender.",
    "Now the part nobody is talking about. <strong>Australia is buying the brain before it has the ammunition.</strong> Dr Malcom Davis of the Australian Strategic Policy Institute says a JABMS with nothing to shoot still does not add up to real air and missile defence. Not against near-term threats.",
    "Those threats have names: China's DF-26 intermediate-range ballistic missile and its DF-27 hypersonic glide vehicle. Australia's current interceptors are SM-6 missiles on three Hobart-class destroyers, plus short-range NASAMS. Brain first. Bullets later.",
    "The missile side is moving, just slowly. In June, Australia ran a ground-based test firing an SM-2 missile using the Aegis combat system, a CEA Technologies radar and a Lockheed Martin Derringer launcher. That is a prototype for a future medium-range ground-based air defence option. Separately that day, the Army's NASAMS capability reached Final Operational Capability.",
    "Lockheed's framing is confident. Jeremy King, chief executive of Lockheed Martin Australia and New Zealand, says this phase fortifies the core of Australia's IAMD. AIR6500, he says, enhances the joint force by bringing all ADF defence assets together on a scalable, resilient and collaborative platform.",
    "Stephanie C. Hill, president of Lockheed Martin Rotary and Mission Systems, calls the company the strategic partner for Air 6500. She says Lockheed will keep working with the Department of Defence to rapidly evolve an advanced IAMD system that safeguards the Indo-Pacific.",
    "Australian Defence Minister Richard Marles called Project AIR6500 a landmark investment in Australia's air defence capability. Note the word: investment. The money is real and the commitment is long. The interceptors are still catching up.",
    "That is the bet. If air defence is being won in software, Lockheed just locked in the layer that matters, for a customer with an A$30 billion appetite. The brain ships first. The ammunition is the variable.",
]

DISCLOSURE = '<p class="disclosure">Disclosure: The Signal holds no position in LMT. Positions may change. This is not financial advice.</p>'

body = "".join("<p>%s</p>" % p for p in paras) + DISCLOSURE

article = {
    "slug": "lmt-australia-air-battle-management-2026",
    "title": "Lockheed's AIR6500 Award Gives Australia a Brain Without Ammunition",
    "subtitle": "Lockheed Martin won A$1.32 billion to build the software that fuses Australia's sensors into one air-defence picture. The interceptors it would direct, against China's DF-26 and DF-27, are still behind it.",
    "summary": "Lockheed Martin Australia won a A$1.32 billion contract from the Australian Government for Tranche 2B of Project AIR6500, the Joint Air Battle Management System that fuses sensor and data feeds into one picture of the battlespace, part of a wider A$2.4 billion six-year air and missile defence investment. The win locks in the command-and-control and sensor-fusion layer where AI is moving into defence, the same battle-network race Palantir and Anduril are fighting. But Australia is buying the brain before it has the ammunition: against China's DF-26 and DF-27, its interceptors are still SM-6s on three destroyers and short-range NASAMS.",
    "ticker": "LMT",
    "sector": "defense",
    "sentiment": "bullish",
    "date": "2026-09-10T17:00:00Z",
    "price": 524.46,
    "image": {
        "src": "/img/articles/lmt-australia-air-battle-management-2026.jpg",
        "fit": "cover",
        "caption": "An air battle management operations centre fuses radar, ship and aircraft feeds into a single picture of the battlespace. Photo: The Signal / AI-generated.",
        "alt": "Air battle management operators at consoles showing a unified air and missile defence picture"
    },
    "tags": [
        "Lockheed Martin",
        "LMT",
        "Australia",
        "Project AIR6500",
        "Air Battle Management",
        "Missile Defence",
        "Defense AI",
        "Command and Control",
        "ASPI",
        "Indo-Pacific",
        "Geopolitics"
    ],
    "videos": [],
    "links": [
        {"label": "Lockheed Martin Secures US$950M Australian Air Battle Management Contract →", "url": "https://breakingdefense.com/2026/09/lockheed-martin-secures-950m-australian-air-battle-management-contract/"},
        {"label": "Australia Extends the Capability of Its Air 6500 IAMD System →", "url": "https://www.asianmilitaryreview.com/2026/09/australia-extends-the-capability-of-its-air-6500-iamd-system-foc"},
        {"label": "Lockheed Martin Wins AIR6500 Tranche 2B Contract →", "url": "https://www.australiandefence.com.au/news/news/lockheed-martin-wins-air-6500-tranche-2b-contract"},
        {"label": "A$2.4 Billion Investment in Air and Missile Defence (Minister for Defence) →", "url": "https://www.minister.defence.gov.au/media-releases/2026-09-09/24-billion-investment-air-missile-defence"},
        {"label": "Lockheed Martin Australia AIR6500 Announcement →", "url": "https://lockheedmartinau.mediaroom.com/index.php?s=2429&item=122734"},
        {"label": "Lockheed Martin: Project AIR6500 →", "url": "https://www.lockheedmartin.com/en-au/products/air-6500.html"}
    ],
    "meta": {
        "author": "The Signal Editorial Team",
        "estimatedReadTime": "5 minutes",
        "editorialTags": [
            "lockheed-martin",
            "lmt",
            "australia",
            "air6500",
            "missile-defense",
            "defense-ai",
            "command-and-control",
            "indo-pacific"
        ],
        "seoKeywords": [
            "LMT stock",
            "Lockheed Martin Australia",
            "Project AIR6500",
            "AIR6500 Tranche 2B",
            "Joint Air Battle Management System",
            "Australia missile defence",
            "defense AI",
            "SM-6",
            "DF-27 hypersonic"
        ],
        "relatedTickers": ["NOC", "RTX", "PLTR", "LDOS", "BA"],
        "keyMetrics": {
            "Price": "$524.46",
            "Market Cap": "$121.7B",
            "Forward P/E": "16.1",
            "Total Revenue (TTM)": "$77.0B",
            "52-Week Low": "$437.25",
            "52-Week High": "$692.00",
            "Analyst Consensus": "Buy",
            "Analyst Target Mean": "$637.84"
        }
    },
    "bodyHtml": body
}

out = "/home/chino/thesignal/articles/posts/lmt-australia-air-battle-management-2026.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(article, f, ensure_ascii=False, indent=2)
print("wrote", out)
print("body words (prose only, excl disclosure):", len(" ".join(paras).split()))
print("body words incl disclosure:", len(body.replace("<p>", " ").replace("</p>", " ").split()))
