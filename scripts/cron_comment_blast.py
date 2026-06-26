#!/usr/bin/env python3
"""Cron job: Generate and post Reddit-style comments for the latest Signal articles."""

import json
import random
import subprocess
import sys
import time

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
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  ✗ JSON PARSE ERROR: {result.stdout[:200]}")
        return None
    if data.get("status") == "success":
        cid = data["comment"]["id"]
        print(f"  ✓ [{cid}] {author}")
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
    try:
        data = json.loads(result.stdout)
        return [c["id"] for c in data.get("comments", [])]
    except (json.JSONDecodeError, KeyError):
        return []

# ── FRESH COMMENT PLANS for the 5 most recent articles ──
# No numbers. No emojis. No "this article"/"the author". Punchy 1-3 sentences.
# Mix of bullish, skeptical, confused, advanced, newbie voices.

PLANS = [
    # ════════════════════════════════════════════════════════
    # 1. AMD MI400 — AMD's $839B AI Chip Comeback (Jun 25)
    # ════════════════════════════════════════════════════════
    {
        "article": "amd-mi400-ai-chip-comeback",
        "comments": [
            ("Latrodestus1990", "amd went from getting laughed out of the ai space to having serious mi400 momentum. the data center crossover past epyc was the real tell. watch what happens when hyperscalers start building amd clusters at scale. this is just the beginning.", None),
            ("work_from_zoom", "we run mi350s in our inference stack at work and the perf per watt is legit. the mi400 rumors have our infra team seriously considering a second vendor. amd isnt nvidia kryptonite but they dont have to be. enterprise procurement loves competition.", None),
            ("whohebe123", "everyone talking about amd finally being a threat. i remember when the same narrative got priced in and then execution faltered. the mi400 paper specs look good but so did the mi300. ill believe it when rack deployments hit scale. fading the hype.", None),
            ("noob_investor42", "bought amd because my friend said they make chips for everything. didnt realize they were going after nvidia too. the chart looks like a rocketship. learning as i go. diamond hands on this one i guess.", None),
            ("option_flow_watcher", "noticing some deep otm call building in amd weeklys ahead of the mi400 event. someone knows something or just a yolo. either way the flow is suggesting conviction. gamma could get interesting into the announcement.", None),
            ("CCWaterBug", "amds market cap is finally reflecting what theyve been building for years. data center is now the main character and the trajectory is clear. playing the long game here. check back in a few years and this looks cheap.", None),
        ],
    },
    # ════════════════════════════════════════════════════════
    # 2. CrowdStrike — Lazarus Trade / 4-for-1 Split (Jun 24)
    # ════════════════════════════════════════════════════════
    {
        "article": "crowdstrike-falcon-ai-security-moat-2026",
        "comments": [
            ("thesis_driven_dan", "my thesis is simple. cybersecurity spend is nondiscretionary in an ai-driven threat landscape. crowdstrike has the platform lock-in with charlotte ai and the renewal metrics speak for themselves. the split makes it accessible. valuation doesnt matter if the moat widens with every new threat.", None),
            ("sharp315", "post-outage recovery was impressive. most companies would have lost trust permanently but crwd used it to rebrand around ai security. retention numbers dont lie. solid company long term for anyone who needs sleep at night.", None),
            ("Minimum-Criticism763", "the outage was the best thing that ever happened to them. turned a catastrophe into a marketing opportunity. smart play but something doesnt add up about how they positioned it. always follow the incentives. insiders still selling into strength.", None),
            ("Latter-Possibility", "turning the worst it disaster in history into a stronger moat is actually impressive. the charlotte ai layer makes the platform harder to leave. corrections are normal. buying opportunity tbh.", None),
            ("first_time_caller99", "my first stock ever and i picked crowdstrike because i heard they stop hackers. is now a good time with the split happening or should i wait. learning as i go. the concept makes sense to my non finance brain.", None),
            ("ragnaroksunset", "yep", None),
        ],
    },
    # ════════════════════════════════════════════════════════
    # 3. Meta Killed Open-Source AI (Jun 24 — bearish META)
    # ════════════════════════════════════════════════════════
    {
        "article": "meta-ai-pivot-proprietary-2026",
        "comments": [
            ("bought_at_the_top", "bought meta for the llama narrative and paid some absurd amount. now they killed open source. my timing is legendary. you are welcome for the dip guys. bagholder reporting in. this is fine. everything is fine.", None),
            ("FEMA_Camp_Survivor", "the open source community just got used and discarded. meta cultivated goodwill for years then pulled the rug the second results got soft. american capitalism has become a joke. regular people always get wrecked when wall street demands returns.", None),
            ("CarrotAwesome", "so they spent years being the open source heroes and now theyre paying some random founder an absurd amount to build closed models. ok but seriously though someone explain the strategic vision here because it looks like panic.", None),
            ("crypto_refugee_88", "this is literally every defi project that promised decentralization then went permissioned. spent years building community trust then rug pulled. at least meta has actual revenue unlike most of the crypto junk i used to hold. stocks are so slow though", None),
            ("this_time_is_different", "zuck spent years telling developers open source was the future of ai. famous last words. ive seen this movie before with every tech company that pivots the second monetization gets real. nothing ever changes on planet zuck.", None),
            ("westcoastcouch", "meta is still a cash machine. dont care about the open source drama. they have instagram and whatsapp printing money. whatever happens happens with their ai strategy. not checking til next quarter.", None),
        ],
    },
    # ════════════════════════════════════════════════════════
    # 4. Palantir — 85% Revenue Growth, Market Doesn't Care (Jun 24)
    # ════════════════════════════════════════════════════════
    {
        "article": "palantir-commercial-ai-revenue-inflection-2026",
        "comments": [
            ("data_dependent_1", "commercial revenue acceleration is the headline nobody is talking about. the us commercial segment growing faster than most saas companies entire revenue base. margins are expanding while they reinvest. balance sheet looks clean. pe is actually reasonable here on a growth-adjusted basis.", None),
            ("fomo_king_420", "kicking myself for watching this all year. the numbers are absurd and the stock keeps getting cheaper. should have bought the last dip. too late to get in now or is this another chance. my timing is always one step behind on this ticker.", None),
            ("Latrodestus1990", "the market is actively ignoring this growth because of eurozone noise. when the street rotates back to fundamentals this rerates hard. commercial contracts are the real story not the government drama. watch what happens next quarter when ailsa proves out at scale.", None),
            ("still_holding_2021", "been holding pltr bags since the spac days. this is the first time the fundamentals actually justify the valuation. commercial adoption is real not just a narrative. one day this pays off and i can finally tell my wife i was right.", None),
            ("turned_into_a_newt", "the us commercial bookings trajectory is the detail everyone glosses over. government contracts are sticky but the commercial pipeline is where the multiple expansion comes from. check the actual contract durations and renewal terms before dismissing this. the math works.", None),
            ("grillmaster_finance", "good company good product. my buddy works at a logistics firm that switched to palantir and says its the best software theyve ever used. bought some for the long haul. sipping a beer while the market figures it out.", None),
        ],
    },
    # ════════════════════════════════════════════════════════
    # 5. GOOGL — Alphabet Talent Bleed Reality Check (Jun 23)
    # ════════════════════════════════════════════════════════
    {
        "article": "googl-ai-everything-strategy-2026",
        "comments": [
            ("macro_dad_energy", "everyone is hyperventilating about talent leaving but google has the deepest bench in tech. losing a couple rockstars to anthropic is noise. the real story is cloud backlog growth and the fed environment supporting mega cap valuations. rates are the real story here.", None),
            ("SheriffBartholomew", "googles ai strategy has no clear monetization path. they spend tons on capex and lose top talent to competitors. were all about to get shafted when the market realizes search moat doesnt protect against an ai-native competitor. retail always the exit liquidity on this narrative.", None),
            ("night_shift_trader", "premarket was rough on the talent bleed headlines but the selling looks exhausted. quiet in here tonight. someone is going to step in and buy this dip. the berkshire position creates a floor that doesnt exist for other mega caps. watching futures for a reversal signal.", None),
            ("paycheck2paycheck", "just doing my weekly buy. google isnt going anywhere. search revenue alone funds everything they do. set it and forget it. boring but it works and i sleep fine at night.", None),
            ("help_me_pls77", "should i be worried about google losing their ai people. my entire portfolio is googl and some boring index fund. is this normal or is the stock going to crash. my heart cant take another red week. ok im holding. talk me off the ledge someone.", None),
            ("contango_cowboy", "the curve on googl options is telling a different story than the headlines. puts are expensive but calls are still flowing. spot vs implied vol suggests the market is pricing in a recovery. yeehaw the vix is up but not panicking on this one.", None),
        ],
    },
]

# ── EXECUTION ──

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
            time.sleep(0.3)  # gentle pacing

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
