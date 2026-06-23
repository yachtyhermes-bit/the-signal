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
    # ── 1. ARM — Ghost in Every AI Server (ARM) ──
    {
        "article": "arm-ai-server-architecture-2026",
        "comments": [
            # ROOTS
            ("work_from_zoom", "i work at a hyperscaler and arm is in literally every new server we deploy. the efficiency advantage over x86 for ai inference workloads is massive. this is the standard now. $ARM", None),
            ("CarrotAwesome", "ok but arm is a licensing company not a chip company. if any of the hyperscalers decide to build their own arm cores the royalty stream dries up fast. the math aint mathing for the current valuation.", None),
            ("whohebe123", "everyone loves arm now after the ipo hype cycle. fading the crowd here. the licensing model means they capture a tiny fraction of the value they create. the hyperscalers will squeeze them over time.", None),
            ("CCWaterBug", "arm in the data center is a decade long story. they went from zero to everywhere in servers and it is still early days. playing the long game. check back when every ai server runs on arm.", None),
            ("first_time_caller99", "so arm doesnt actually make chips they just design the blueprints and collect royalties? and every ai server uses them? trying to understand the business model. learning as i go.", None),
        ],
    },
    # ── 2. KTOS — Valkyrie Drone Army (KTOS) ──
    {
        "article": "kratos-valkyrie-drone-army-2026",
        "comments": [
            # ROOTS
            ("Latrodectus1990", "ktos dropping while revenue keeps growing tells me the market has already priced in a drone buildout that hasnt materialized yet. watch what happens when the next pentagon budget gets cut. generational bagholders incoming.", None),
            ("sharp315", "the valkyrie program is real but drone swarms are still a concept not a production program. kratos has backlog sure but execution risk on defense contracts is always higher than people expect. solid company long term but be patient.", None),
            ("help_me_pls77", "down on this one and i keep buying the dip and it keeps dipping. the business looks good on paper but my portfolio disagrees. is this normal for defense stocks. talk me off the ledge.", None),
            ("thesis_driven_dan", "my thesis is simple. kratos is the only pure play on the drone warfare shift and the pentagon is committed to loitering munitions and autonomous systems. the backlog converts at steady state if execution holds. three things need to happen — valkyrie goes production, margins stabilize, and the market re-rates defense growth.", None),
            ("option_flow_watcher", "ktos options have been picking up volume lately. decent call flow for a beaten down defense name. someone might know something about a valkyrie production decision coming.", None),
        ],
    },
    # ── 3. Broadcom — $22B Quarter Sold Off (AVGO) ──
    {
        "article": "broadcom-ai-asic-dominance",
        "comments": [
            # ROOTS
            ("macro_dad_energy", "avgo selling off on a record quarter tells you everything about the macro environment. the company is firing on all cylinders but rates and inflation fear are the real story here. the fed put is not back on the menu yet. $AVGO", None),
            ("noob_investor42", "bought avgo last week and it immediately dropped. just my luck. everyone says the quarter was amazing though and the ai semi business is exploding. bought the top lol.", None),
            ("ragnaroksunset", "avgo. the selloff on this kind of quarter is interesting. watching.", None),
            ("FEMA_Camp_Survivor", "record quarter with ai semi revenue surging and the stock gets destroyed. wall street always finds a reason to punish even the best companies. regular people always get wrecked on these reactionary drops.", None),
            ("SheriffBartholomew", "avgo beat and the stock gets punished. same story different ticker. retail always the exit liquidity when institutions decide semis are too crowded.", None),
        ],
    },
    # ── 4. Google — Quiet Military Pivot (GOOGL) ──
    {
        "article": "google-gemini-military-pivot-2026",
        "comments": [
            # ROOTS
            ("turned_into_a_newt", "the read team contract structure is the detail everyone is glossing over. moving gemini into classified il6 and il7 military networks is a whole different security posture than standard google cloud. the lockup periods on those contracts are multi year. $GOOGL", None),
            ("grillmaster_finance", "google getting deeper into defense contracts is a big deal. they have been way behind aws and azure in government cloud for years. finally catching up. bought some for the kids college fund.", None),
            ("Minimum-Criticism763", "follow the incentives. google has been trying to win pentagon business forever and employees have pushed back hard every time. something doesnt add up if they are going this deep now. the ceo is betting big on military revenue and insiders are watching.", None),
            ("Latter-Possibility", "the market is sleeping on goog moving into tier one defense ai. this opens up a whole new revenue stream that nobody has in their models. actually this is healthy for the long term thesis.", None),
            ("whats_a_stop_loss", "google with top secret military ai contracts is a massive catalyst. they have the best ai talent and the infrastructure to beat aws in government cloud. what could go wrong. update: everything could go wrong but im buying anyway.", None),
        ],
    },
    # ── 5. Rocket Lab — Invisible Rocket Company (RKLB) ──
    {
        "article": "rocket-lab-space-systems-cash-cow-2026",
        "comments": [
            # ROOTS
            ("data_dependent_1", "the space systems division is where the actual revenue lives and the growth rate there is impressive. balance sheet looks solid for a company at this stage. this isnt a narrative stock — the backlog is real and converting. $RKLB", None),
            ("RN_Geo", "rklb is interesting but the market is paying for growth like it is a software company. space systems revenue is real but the margins are structurally lower than launch once neutron scales. im staying cautious. no rush to buy here.", None),
            ("night_shift_trader", "rklb premarket has been looking interesting lately. space systems revenue is the part everyone overlooks while obsessing over electron launches. night shift checking in.", None),
            ("westcoastcouch", "threw a small position in rklb for the space systems story. launch is exciting but the real business is the satellites and components. not checking til neutron flies. whatever happens happens.", None),
            ("still_holding_2021", "been holding rklb since before it went public via spac. averaged down through the whole space bear market. one day neutron launches, the space systems margins expand, and everyone wakes up. this stock owes me money.", None),
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
