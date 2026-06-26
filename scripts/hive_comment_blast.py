#!/usr/bin/env python3
"""Hive Comment Blast — post Reddit-style comments + likes on The Signal articles."""

import json
import random
import subprocess
import sys

BASE_URL = "https://readthesignal.net/api/comments"
TOKEN = "hive-comment-blast-2026"

# ── Liker IDs for the like-blast phase ──
LIKER_IDS = ["usr_a1", "usr_b2", "usr_c3", "usr_d4", "usr_e5"]

def post_comment(article, author, text, parent_id=None):
    """POST a comment. Returns the full JSON response dict."""
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
    """POST a like. Returns True if successful."""
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
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return True

def get_all_comment_ids(article_slug):
    """Fetch all comment IDs for an article."""
    cmd = [
        "curl", "-s", f"{BASE_URL}/?article={article_slug}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    data = json.loads(result.stdout)
    return [c["id"] for c in data.get("comments", [])]

# ═══════════════════════════════════════════════════════════════
# COMMENT PLANS — dynamically generated for homepage articles
# ═══════════════════════════════════════════════════════════════

PLANS = [
    # ── 1. AMD — MI400 AI Chip Comeback ──
    {
        "article": "amd-mi400-ai-chip-comeback",
        "comments": [
            ("FEMA_Camp_Survivor", "lisa su is doing what every underdog ceo dreams of. nvidias moat is real but hyperscalers hate being locked in. amd just needs to be good enough at a better price and the market share flows. retail gets front run again when the rotation happens.", None),
            ("sharp315", "the mi400 architecture sounds legit but amd always promises and nvidia always delivers. im watching but not buying yet. cdna needs to actually ship and benchmark before i believe.", None),
            ("Latrodectus1990", "everybody sleeping on amd right now. the second source narrative is the strongest its ever been and the data center ramp is real. this is going to be one of those stocks people look back at and say i should have bought when nobody cared. watch what happens when mi400 benchmarks drop.", None),
            ("work_from_zoom", "we run some amd instances at work for specific inference workloads and they work fine. nobody talks about it but the ecosystem is maturing fast. cuda is still the standard but rocm is catching up quicker than people admit.", None),
            ("noob_investor42", "bought amd because someone on reddit said its the ai chip underdog. no idea what cdna means but the charts look like its finding a bottom. learning as i go lol.", None),
            ("CCWaterBug", "the market is pricing amd like its still the old amd that couldnt execute. the new amd under lisa su has a totally different track record. playing the long game here. check back when mi400 is actually in production.", None),
        ],
    },
    # ── 2. CRWD — CrowdStrike Lazarus Trade ──
    {
        "article": "crowdstrike-falcon-ai-security-moat-2026",
        "comments": [
            ("whohebe123", "everyone thought crowdstrike was dead after that outage. i was bearish too. but they came back stronger and that charlotte ai product sounds like the real moat. fading the negativity here feels right. the split is just icing.", None),
            ("data_dependent_1", "renewal rates holding strong through the worst crisis in company history tells you everything. customers actually stayed. the charlotte automation play is widening margins too. balance sheet is clean and the ai security tailwind is just getting started.", None),
            ("bought_at_the_top", "bought crwd right before the outage. of course i did. my timing is legendary. but i held and somehow im back in the green. bagholder who accidentally diamond handed into a winner. you are welcome for the dip.", None),
            ("thesis_driven_dan", "my thesis is simple. cybersecurity is a non-discretionary spend that compounds with ai threats. crowdstrike has the installed base and the automation layer. the split brings in retail demand. valuation doesnt matter if the recurring revenue keeps compounding.", None),
            ("RN_Geo", "crowdstrike is a great company but at this valuation after the bounce im staying in cash for now. too much good news already priced in. id wait for a pullback after the split euphoria fades.", None),
            ("option_flow_watcher", "call volume has been building steadily into the split announcement. max pain moved up significantly. someone is accumulating ahead of the july date. flow looks bullish through the split event horizon.", None),
        ],
    },
    # ── 3. META — Meta Killed Open-Source AI ──
    {
        "article": "meta-ai-pivot-proprietary-2026",
        "comments": [
            ("Minimum-Criticism763", "the llama open source strategy was always about collecting free developer feedback and data. now that they have what they need theyre locking it down. something doesnt add up with the alexandr wang deal either. follow the incentives. insiders are trimming for a reason.", None),
            ("grillmaster_finance", "my daughter uses facebook and my son uses instagram. the family still spends time there. bought some meta for the kids college fund. zuck makes weird decisions but the ad business is a cash machine. good company good product.", None),
            ("macro_dad_energy", "everyone is missing the big picture on meta. the ad business prints money and the wearables pipeline is a real catalyst nobody is pricing in. the ai pivot drama is noise. rates are supportive and the buyback is massive. meta will be fine.", None),
            ("turned_into_a_newt", "the llama flop was worse than people realize internally. look at the talent migration out of the ai org. paying that much for muse spark suggests internal models were way behind. the s-1 for the debt issuance tells a different story than zucks public messaging.", None),
            ("westcoastcouch", "meta up, meta down, whatever. i bought some shares a while back and im not checking. the ad revenue is real and thats enough for me. market does what it does. see yall next quarter.", None),
            ("ragnaroksunset", "yikes", None),
        ],
    },
    # ── 4. PLTR — Palantir Growing Fast, Market Ignores ──
    {
        "article": "palantir-commercial-ai-revenue-inflection-2026",
        "comments": [
            ("first_time_caller99", "i just started investing and palantir keeps dropping even though the revenue is going up. is this normal. should i buy the dip or is something wrong with the company. learning as i go and this one confuses me the most.", None),
            ("Latter-Possibility", "the disconnect between the growth and the stock price is actually a gift for patient buyers. commercial adoption is accelerating and government contracts are as sticky as it gets. the europe headline noise is temporary. buying opportunity tbh.", None),
            ("SheriffBartholomew", "this is classic wall street. company crushes earnings, grows faster than anyone, and the stock gets punished. retail always the exit liquidity for the big boys. palantir is the most obvious long term winner that nobody can hold because of the volatility.", None),
            ("contango_cowboy", "the vix is telling us something about the broader risk off mood thats dragging every growth stock down with it. palantir is getting caught in the macro washout. when the curve normalizes this thing rips. yeehaw the setup is actually improving here.", None),
            ("mom_of_3_trading", "i buy palantir for my kids future because they use aip at school and their teachers say its amazing. boring stock picks are my thing. just buying what i understand and dca during carpool line.", None),
            ("whats_a_stop_loss", "palantir down again. what could go wrong if i double down? this is either genius or stupid. update from last quarter: it was genius because i averaged down and now im green. but this time? who knows. yolo.", None),
        ],
    },
    # ── 5. GOOGL — Alphabet Talent Bleed Reality Check ──
    {
        "article": "googl-ai-everything-strategy-2026",
        "comments": [
            ("CarrotAwesome", "so they lost a nobel laureate and a gemini co-lead in the same week and the stock dropped a quarter trillion in a day. ok but seriously though google still has the best ai infrastructure on earth and the cloud backlog is massive. the math aint mathing on the panic sell.", None),
            ("still_holding_2021", "still holding googl since way before the split. ive seen this movie before. talent leaves, stock drops, then they figure it out and rip higher. the search moat and cloud pipeline are too strong. one day this position pays off and i sell covered calls until then.", None),
            ("night_shift_trader", "premarket was a bloodbath on the jumper news but the selling looks exhausted now. volume is drying up and the bid support feels like institutions are catching the knife. quiet in here tonight but that usually means the panic is over.", None),
            ("tacotuesdaytrader", "quick buy on googl while i eat my lunch. the berkshire backing gives this a massive floor and the cloud numbers are ridiculous. people are overreacting to the talent news. back to work see yall. taking the family out if this bounces.", None),
            ("fomo_king_420", "watched google drop all day yesterday and didnt buy. now im kicking myself because its already bouncing. too late to get in?? should have bought the panic. next time i swear i will actually click the button.", None),
            ("paycheck2paycheck", "just bought another batch of googl with this weeks paycheck. talent leaves, business stays. cloud is growing like crazy and search prints money. boring and steady is exactly what i want in my taxable. set it and forget it.", None),
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
        # PHASE 1: Post comments, tracking root IDs
        root_ids = {}  # index -> id
        all_my_ids = []

        for i, (author, text, parent_marker) in enumerate(plan["comments"]):
            # Resolve parent markers
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

    # PHASE 2: Fetch all comment IDs (including old ones) and like ~60%
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
