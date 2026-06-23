#!/usr/bin/env python3
"""Hive Comment Blast — dynamic comments for today's articles."""

import json
import random
import subprocess
import sys

BASE_URL = "https://readthesignal.net/api/comments"
TOKEN = "hive-comment-blast-2026"

LIKER_IDS = ["usr_a1", "usr_b2", "usr_c3", "usr_d4", "usr_e5"]

def post_comment(article, author, text, parent_id=None):
    payload = {
        "article": article,
        "author": author,
        "text": text,
        "parentId": parent_id,
        "token": TOKEN
    }
    cmd = [
        "curl", "-s", "-X", "POST", f"{BASE_URL}/",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    data = json.loads(result.stdout)
    if data.get("status") == "success":
        cid = data["comment"]["id"]
        print(f"  ✓ [{cid}] {author}: {text[:60]}...")
        return cid
    else:
        print(f"  ✗ ERROR: {data}")
        return None

def like_comment(comment_id, uid):
    payload = {
        "commentId": comment_id,
        "uid": uid,
        "token": TOKEN
    }
    cmd = [
        "curl", "-s", "-X", "POST", f"{BASE_URL}/?action=like",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return True

def get_all_comment_ids(article_slug):
    cmd = ["curl", "-s", f"{BASE_URL}/?article={article_slug}"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    data = json.loads(result.stdout)
    return [c["id"] for c in data.get("comments", [])]

# ═══════════════════════════════════════════════════════════════
# TODAY'S COMMENT PLANS — June 22, 2026
# No numbers in comments. Real retail voices.
# ═══════════════════════════════════════════════════════════════

PLANS = [
    # ── 1. IREN — Bitcoin Miner to AI Cloud Pivot ──
    {
        "article": "iren-short-squeeze-ai-cloud-june-2026",
        "comments": [
            ("work_from_zoom", "we use IREN compute at our lab and their power infrastructure is legit. the nvidia partnership isnt vanity — they actually vetted the facilities and the rip-and-replace model works. this is the standard now for repurposed ai datacenter capacity. $IREN", None),
            ("CarrotAwesome", "ok so iren was a bitcoin miner and now everyone suddenly thinks its an ai infrastructure company. the nvidia deal is real business but the market is pricing in a transition that hasnt fully happened yet. someone explain the valuation math like im five.", None),
            ("whohebe123", "iren is getting hyped as the next big ai compute play after the nvidia deal. i get the cheap power thesis and the infrastructure conversion story but the short squeeze already happened and the easy money is gone. fading the crowd here.", None),
            ("noob_investor42", "bought iren because the story sounded cool and everyone was yelling about it. still dont really understand how bitcoin mining turns into ai cloud but the chart looks good. bought the top lol.", None),
            ("thesis_driven_dan", "my thesis is simple. iren owns power infrastructure in locations with cheap electricity. nvidia doesnt do vanity partnerships so the deal validates the facilities. the market still prices them as a crypto miner and the re-rating to ai infrastructure is the catalyst. three things need to convert for this to work.", None),
        ],
    },
    # ── 2. VRT — Data Center Cooling Dominance ──
    {
        "article": "vertiv-ai-data-center-cooling-2026",
        "comments": [
            ("macro_dad_energy", "vrt is the purest pick and shovel play in the ai infrastructure buildout. every gpu ever made needs cooling and vertiv owns the reference design slot for the nvidia factories. the backlog more than doubled and the macro backdrop of ai capex keeps expanding. $VRT", None),
            ("sharp315", "vertiv is up a ton already and the valuation gets harder to justify with each green candle. the backlog is impressive but execution risk at this scale is real and margins face pressure as liquid cooling becomes a commodity. solid company long term but i wouldnt chase here.", None),
            ("data_dependent_1", "backlog doubled year over year and the book to bill is well above one which means demand is accelerating not slowing. free cash flow surged and they just initiated a dividend which signals maturation. growth at this scale with expanding margins is rare in infrastructure.", None),
            ("help_me_pls77", "i bought vrt at the top and now im sitting red and panicking. the backlog stories sound amazing but my portfolio disagrees. everyone says hold but every red day makes me want to sell. is this normal for infrastructure stocks. talk me off the ledge.", None),
            ("turned_into_a_newt", "the nvidia vera rubin reference design lockin is the detail everyone is glossing over. vertiv isnt just another supplier they are architected into the spec sheet for the entire next gen ai factory. the thermokey and strategic thermal labs acquisitions fill the liquid cooling gap and strengthen the supplier moat. this detail matters.", None),
        ],
    },
    # ── 3. MDA Space — Arms Dealer of the Orbital Economy ──
    {
        "article": "mda-space-arms-dealer-orbital-economy",
        "comments": [
            ("option_flow_watcher", "mda options have been active on the tsx recently. call volume picked up noticeably before the blue canyon acquisition closed. someone was early on the satellite manufacturing thesis playing out.", None),
            ("RN_Geo", "mda space has real revenue growth and a fortress backlog but tsx companies always trade at a discount to us peers and the currency exposure is a real headwind. the business is solid and the backlog is real but i prefer waiting for a wider margin of safety.", None),
            ("Latter-Possibility", "actually like the arms dealer framing for mda. instead of gambling on which satellite direct to device company wins the consumer race you buy the manufacturer that builds satellites for all of them. this is the smart way to play the orbital economy without picking winners.", None),
            ("Minimum-Criticism763", "mda spent a pile of cash on blue canyon and everyone is cheering the acquisition. integrating a us defense contractor into a canadian company has real cultural and compliance friction that gets handwaved away. something doesnt add up if the integration is as easy as they claim.", None),
            ("westcoastcouch", "tossed some money at mda for the aurora satellite line story. two satellites a day with robotics and the prime chip sound like real technology. not checking the price til they hit full capacity. whatever happens happens.", None),
        ],
    },
    # ── 4. NET — Cloudflare AI Agent Pivot ──
    {
        "article": "cloudflare-edge-ai-zero-trust-2026",
        "comments": [
            ("FEMA_Camp_Survivor", "cloudflare laid off a big chunk of the workforce to chase agentic ai and the stock got hammered. the workers platform growth is real but the margin compression from running ai inference is structural not temporary. the ceo is betting the whole company on a narrative flip and wall street will turn on a dime.", None),
            ("SheriffBartholomew", "net beats on revenue, fires a big chunk of the workforce, stock gets crushed. same story different quarter. the margin story keeps deteriorating and the zero trust competition from zscaler isnt going anywhere. retail always ends up holding the narrative bag on these pivots.", None),
            ("CCWaterBug", "the selloff on net was the market reading layoff headlines instead of the growth numbers. a huge wave of new developers signing up for workers in a single quarter is a platform effect that takes time to monetize but the trajectory is unmistakable. check back when enterprise adoption catches up.", None),
            ("whats_a_stop_loss", "net drops hard on a beat because the market hates the ai agent bet. either this is the kind of bold capital allocation that defines a great ceo or a founder destroying a good company chasing hype. im buying the dip. update: it was stupid.", None),
            ("ragnaroksunset", "net. revenue accelerating and the stock drops. the workers number is the real story. watching.", None),
        ],
    },
    # ── 5. LMT — Lockheed Value Play ──
    {
        "article": "lockheed-martin-f35-defense-backlog-2026",
        "comments": [
            ("Latrodectus1990", "lmt sitting at a discount to the broader market with a backlog that guarantees years of locked in revenue and nobody cares because defense is boring. watch what happens when the next geopolitical flashpoint hits and the sector wakes up violently. generational value play.", None),
            ("grillmaster_finance", "lockheed at a lower valuation than the s and p with that much guaranteed revenue is something my father in law would call a no brainer. the f35 pipeline alone is a decade of production and the hypersonic program is just scaling. bought some for the kids.", None),
            ("still_holding_2021", "been holding lmt for years through every macro rotation. boringest position in my portfolio but it pays a real dividend and barely moves on most days. the defense supercycle is structural and people will rotate back when growth names correct. this stock owes me patience.", None),
            ("Shdwrptr", "lmt at these multiples with that backlog is worth a look. the hypersonic program is the kind of moat that takes decades to replicate and the f35 sustainment revenue is sticky for life. not buying yet but watching for a technical entry.", None),
            ("this_time_is_different", "lockheed at a cheap earnings multiple with a massive backlog while the world keeps spending more on defense every year. this time is different guys. no really. ive seen this movie before and the value trade works until the budget cycle turns. history says buy here though.", None),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# EXECUTION
# ═══════════════════════════════════════════════════════════════

LIKE_ONLY = "--like" in sys.argv

total_comments = 0
total_likes = 0

for plan in PLANS:
    article = plan["article"]
    print(f"\n{'='*60}")
    print(f"ARTICLE: {article}")
    print(f"{'='*60}")

    if not LIKE_ONLY:
        root_ids = {}
        all_my_ids = []

        for i, (author, text, parent_marker) in enumerate(plan["comments"]):
            actual_parent = None
            if parent_marker and parent_marker.startswith("{ROOT_"):
                idx = int(parent_marker.replace("{ROOT_", "").replace("}", ""))
                actual_parent = root_ids.get(idx)
            elif parent_marker and parent_marker.startswith("{EXISTING_"):
                actual_parent = parent_marker.replace("{EXISTING_", "").replace("}", "")
            elif parent_marker:
                actual_parent = parent_marker

            cid = post_comment(article, author, text, actual_parent)
            if cid:
                all_my_ids.append(cid)
                if parent_marker is None:
                    root_ids[i] = cid
                total_comments += 1

    # PHASE 2: Fetch all comment IDs and like ~60%
    print(f"\n  --- LIKES ---")
    all_ids = get_all_comment_ids(article)
    print(f"  Total comments on article: {len(all_ids)}")

    liked = 0
    for cid in all_ids:
        if random.random() < 0.6:
            uid = random.choice(LIKER_IDS)
            like_comment(cid, uid)
            liked += 1
            total_likes += 1
    print(f"  Liked {liked}/{len(all_ids)} comments (~60%)")

print(f"\n{'='*60}")
if LIKE_ONLY:
    print(f"LIKE-ONLY MODE: {total_likes} likes applied across all articles")
else:
    print(f"TOTALS: {total_comments} comments posted, {total_likes} likes applied")
print(f"{'='*60}")
