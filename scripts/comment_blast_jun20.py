#!/usr/bin/env python3
"""Dynamic comment blast for The Signal's 5 most recent articles — Jun 20, 2026."""

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
        print(f"  ✓ [{cid}] {author}: {text[:70]}...")
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

# ── COMMENT PLANS ──────────────────────────────────────────────
# Each article gets 3-6 root comments, some with replies.
# Format: (author, text, parent_marker or None)
# parent_marker can be "{ROOT_N}" referencing the Nth root comment (0-indexed)

PLANS = [
    # ── 1. ServiceNow (NOW) – SaaS/AI Agent play ──
    {
        "article": "servicenow-ai-agent-enterprise-moat-2026",
        "comments": [
            # ROOTS
            ("work_from_zoom", "i work in this industry and every enterprise i know is doubling down on servicenow. the platform is the standard now for ai agent orchestration. companies arent ripping this out.", None),
            ("Latrodectus1990", "the sasspocalypse crowd was dead wrong. generative ai needs a governance layer and now has the strongest hand. watch what happens when the next earnings hit.", None),
            ("whohebe123", "market hates enterprise saas rn which means this is probably the buy signal. fading the crowd on now while everyone piles into semis.", None),
            ("noob_investor42", "bought a few shares last week after the dip. learning as i go but this seems like a solid company that makes software businesses actually use.", None),
            ("sharp315", "depends on your timeline but now at these levels with the ai agent pivot is interesting. solid company long term if they execute on the ai play.", None),
            ("ragnaroksunset", "watching", None),
            # REPLIES
            ("first_time_caller99", "is this a good time to buy into now?? my first stock ever was a tech stock and it went down immediately so im nervous", "{ROOT_3}"),
        ],
    },
    # ── 2. SoFi (SOFI) – Fintech value play ──
    {
        "article": "sofi-the-fintech-that-quietly-figured-out-profits",
        "comments": [
            # ROOTS
            ("data_dependent_1", "actual revenue growth is accelerating and the balance sheet looks clean. ten straight profitable quarters with the stock getting hammered. something has to give.", None),
            ("SheriffBartholomew", "retail always the exit liquidity in fintech. sofi prints money and the market yawns. this ends with the stock ripping when nobody expects it.", None),
            ("mom_of_3_trading", "bought some for the kids college fund. my oldest uses their app for her student loans. just buying what i understand and i understand a good user experience.", None),
            ("grillmaster_finance", "good company good product. sipping a beer watching this ticker. my buddy refinanced his student loans through them and said it was painless.", None),
            ("CarrotAwesome", "ok but seriously though. member count growing fast and deposits are piling up. the market is pricing them like a crypto exchange when the business model is basically a digital bank.", None),
            ("still_holding_2021", "been holding sofi since the spac days. one day this pays off. the financials keep getting better every quarter.", None),
        ],
    },
    # ── 3. Palantir (PLTR) – Defense AI ──
    {
        "article": "palantir-aip-defense-contracts-2026",
        "comments": [
            # ROOTS
            ("FEMA_Camp_Survivor", "palantir is the pentagon's brain now. love it or hate it theyre embedded in every major defense decision. the market wants to hate the valuation but the revenue is catching up fast.", None),
            ("option_flow_watcher", "unusual call activity on pltr this week despite the downtrend. someone is positioning for a move. gamma could push this up if we break resistance.", None),
            ("bought_at_the_top", "bought pltr near the high of course. you're welcome for the dip guys. but im not selling. the government contract growth speaks for itself.", None),
            ("macro_dad_energy", "defense spending is the real story here. the geopolitical environment means these contracts keep getting bigger. everyone is missing the structural tailwind for pltr.", None),
            ("Minimum-Criticism763", "thirteen billion in contract ceilings is impressive but follow the incentives. insiders have been selling chunks and the valuation is still rich. something doesnt add up.", None),
            ("Latter-Possibility", "corrections are normal in growth stocks. palantir doubled revenue and the stock goes down a quarter. buying opportunity tbh when you look at the trajectory.", None),
        ],
    },
    # ── 4. AMD (AMD) – AI Chip Underdog ──
    {
        "article": "amd-mi400-ai-chip-underdog-2026",
        "comments": [
            # ROOTS
            ("thesis_driven_dan", "my thesis is simple. inference will be most of ai compute long term and amd's memory architecture is better suited for it. the bull case rests on mi400 closing the software gap.", None),
            ("turned_into_a_newt", "the openai deal is the key detail everyone glosses over. a multi-gigawatt partnership means amd isnt just a supplier anymore. theyre an infrastructure partner.", None),
            ("contango_cowboy", "the curve is telling us something. gpu supply chains are loosening and nvda's premium isnt guaranteed forever. amd at a discount to nvda is the spread trade of the decade.", None),
            ("westcoastcouch", "amd has been on a heater all year. whatever happens happens. im not checking my positions til the mi400 launch news drops.", None),
            ("fomo_king_420", "should have bought amd when it was under three digits. kicking myself rn. too late to get into amd now that its up this much??", None),
            ("CCWaterBug", "playing the long game on amd. second place in a massive tam is still a fortune. check back in a few years when the inference wave really hits.", None),
        ],
    },
    # ── 5. TSMC (TSM) – Semi Monopoly ──
    {
        "article": "tsmc-advanced-chip-monopoly-2026",
        "comments": [
            # ROOTS
            ("this_time_is_different", "ive seen this movie before. the monopoly thesis is compelling until geopolitics hits. taiwan strait risk is the elephant in every room that nobody wants to talk about. famous last words.", None),
            ("RN_Geo", "no rush to buy tsmc here after the run up. playing it safe this year. valuation is reasonable but the geopolitical tail risk is real and i cant quantify it.", None),
            ("night_shift_trader", "premarket looking good. night shift checking in from the warehouse. tsmc seems like the only game in town for advanced chips. hard to bet against that.", None),
            ("paycheck2paycheck", "just doing my weekly buy. set it and forget it. been adding tsm every paycheck for the last year and not stopping. boring but it works.", None),
            ("Shdwrptr", "pass at this valuation. too expensive for me even if the moat is real. ill wait for a pullback.", None),
            ("whats_a_stop_loss", "stop loss?? never heard of her. all in on the semiconductor etf proxy play. this is either genius or stupid betting on a country instead of a company.", None),
            # REPLIES
            ("help_me_pls77", "should i be worried about taiwan stuff with my tsmc shares?? my heart cant take another geopolitical crisis. talk me off the ledge.", "{ROOT_0}"),
        ],
    },
]

# ── EXECUTION ──────────────────────────────────────────────────

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
            elif parent_marker:
                actual_parent = parent_marker

            cid = post_comment(article, author, text, actual_parent)
            if cid:
                all_my_ids.append(cid)
                if parent_marker is None:
                    root_ids[i] = cid
                total_comments += 1

    # Likes
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
