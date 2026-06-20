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
    # ── 1. Ackman Microsoft AI Bet (MSFT) ──
    {
        "article": "ackman-microsoft-ai-bet",
        "comments": [
            # ROOTS
            ("whohebe123", "everyone piling into msft cause ackman tweeted a 13f. fading the crowd on this one. he established this position weeks ago and now retail is the exit strategy.", None),
            ("SheriffBartholomew", "classic wall street playbook. billionaire announces position after its already built. retail piles in at the peak. were all about to get shafted.", None),
            ("thesis_driven_dan", "my thesis is simple. enterprise software is the stickiest business on earth. companies dont switch off m365 for a cheaper alternative. the bull case rests on azure ai workloads compounding for years.", None),
            ("work_from_zoom", "i work in this industry and azure enterprise contracts have been accelerating. we just signed a multi year deal across our division. the ai copilot integration is the standard now.", None),
            # REPLIES
            ("first_time_caller99", "opened my robinhood account last month. is this a good time to buy msft?? only down a little from what ackman paid right", "{ROOT_0}"),
        ],
    },
    # ── 2. AI Inversion: White-Collar Wipeout (META) ──
    {
        "article": "ai-inversion-white-collar-blue-collar",
        "comments": [
            # ROOTS
            ("Latrodectus1990", "ive been saying this for months. the coding bootcamp pipeline is about to get obliterated. junior devs and paralegals are the coal miners of this decade.", None),
            ("Latter-Possibility", "actually this is healthy. every industrial revolution displaced workers and then created entirely new categories. the operator economy is the next frontier and nobody sees it yet.", None),
            ("CCWaterBug", "electrician was always the play. playing the long game. check back in a few years when a journeyman electrician makes more than a mid level engineer.", None),
            ("crypto_refugee_88", "wait so the same ai that i thought would make everyone rich is gonna take the high paying jobs?? this is like getting rugged in slow motion. at least it wont rug overnight though.", None),
            # REPLY
            ("noob_investor42", "bought meta at the top lol. learning the hard way. but if ai is replacing white collar workers shouldnt the company selling the ai be printing money??", "{ROOT_2}"),
        ],
    },
    # ── 3. AIPO AI Power Infra ETF ──
    {
        "article": "aipo-ai-power-infra-dip-buy-june-2026",
        "comments": [
            # ROOTS
            ("turned_into_a_newt", "check the constituent list. constellation energy and ge vernova are buried in here alongside broadcom. this is infrastructure arbitrage hidden in an etf wrapper.", None),
            ("contango_cowboy", "the curve is telling us something. forward power prices in pjm and ercot have been climbing for months while everyone was staring at nvidia. this etf is pricing in what the futures market already knows.", None),
            ("whats_a_stop_loss", "power companies are boring til theyre not. stop loss?? never heard of her. this is either genius or stupid going all in on the grid theme.", None),
            ("mom_of_3_trading", "bought some for their college fund. boring etfs are my thing. just buying what i understand and everyone needs electricity to run ai chips.", None),
            # REPLY
            ("sharp315", "depends on your timeline. the power infra theme is real but etfs always dilute your best holdings. not financial advice but id rather pick the top names directly.", "{ROOT_2}"),
        ],
    },
    # ── 4. Alphabet $4.64 Trillion Milestone (GOOGL) ──
    {
        "article": "alphabet-5-trillion-milestone",
        "comments": [
            # ROOTS
            ("Minimum-Criticism763", "something doesnt add up. google hitting multi trillion valuations while search revenue growth is decelerating. insiders are selling fyi. follow the incentives.", None),
            ("FEMA_Camp_Survivor", "american capitalism has become a joke. google monopoly prints money while regulators posture then do nothing. the system is designed this way.", None),
            ("data_dependent_1", "youtube revenue breaking records is the underrated story here. actual revenue diversification is happening across search cloud and subscriptions. balance sheet remains pristine.", None),
            ("grillmaster_finance", "good company good product. i use google maps and youtube practically every day. sipping a beer watching this ticker.", None),
            # REPLY
            ("fomo_king_420", "should have added more google shares last quarter. kicking myself rn. i always build positions after the run up.", "{ROOT_1}"),
        ],
    },
    # ── 5. Amazon Q1 2026 AWS Reacceleration (AMZN) ──
    {
        "article": "amazon-q1-2026-aws-reacceleration",
        "comments": [
            # ROOTS
            ("CarrotAwesome", "ok but seriously though. eps nearly tripling is great but aws growth is the only thing that actually matters here. without cloud acceleration this is just a retail company with an expensive tech division.", None),
            ("macro_dad_energy", "rates are the real story here. every basis point the fed cuts makes the dcf on these cloud businesses look better. everyone is missing the macro tailwind for amzn.", None),
            ("just_lurking_69", "been watching this thread for a while. what do you guys think about amzn at these levels after that shocker earnings beat? is now a bad time to start a position", None),
            ("westcoastcouch", "whatever happens happens. amzn will be bigger in the future than it is today. im not checking my positions til next month anyway.", None),
            # REPLY
            ("paycheck2paycheck", "just doing my weekly buy. set it and forget it. been adding amzn every paycheck since the split and not stopping now.", "{ROOT_2}"),
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
