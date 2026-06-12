#!/usr/bin/env python3
"""Reddit-style comment + like blast on The Signal articles."""
import json
import random
import subprocess
import sys
import time

BASE_URL = "https://readthesignal.net/api/comments"
TOKEN = "hive-comment-blast-2026"
LIKER_IDS = ["usr_a1", "usr_b2", "usr_c3", "usr_d4", "usr_e5", "usr_f6"]

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
    except:
        print(f"  ✗ PARSE ERROR: {result.stdout[:120]}")
        return None
    if data.get("status") == "success":
        cid = data["comment"]["id"]
        print(f"  ✓ [{cid}] {author}: {text[:70]}...")
        return cid
    else:
        print(f"  ✗ FAIL: {data}")
        return None

def like_comment(comment_id, uid):
    payload = {"commentId": comment_id, "uid": uid, "token": TOKEN}
    cmd = [
        "curl", "-s", "-X", "POST", f"{BASE_URL}/?action=like",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return True

def get_all_comment_ids(article_slug):
    cmd = ["curl", "-s", f"{BASE_URL}/?article={article_slug}"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    try:
        data = json.loads(result.stdout)
        return [c["id"] for c in data.get("comments", [])]
    except:
        return []

# ═══════════════════════════════════════════════════════════════
# COMMENT PLANS — 30% newbie / 40% everyday / 30% advanced
# ═══════════════════════════════════════════════════════════════

PLANS = [
    # ── 1. Goldman Sachs AI Capex ($920B) ── bearish, currently 6 comments
    {
        "article": "goldman-sachs-ai-capex-warning-june-2026",
        "comments": [
            # ROOTS
            ("whohebe123", "everyone panicking about $920b capex but with this much fear the semis probably bounce next week. fading the crowd on this one", None),
            ("FEMA_Camp_Survivor", "goldman drops this right after oracle got torched. they knew exactly what they were doing. regular people always the bagholders", None),
            ("help_me_pls77", "i just bought nvda last week and now this. should i sell?? my heart cant take this", None),
            # REPLIES
            ("just_lurking_69", "been watching this thread. what makes you think semis bounce when the big banks are literally telling everyone its overpriced though", "{ROOT_0}"),
            ("CCWaterBug", "goldmans been wrong plenty. 2030 for me maybe longer. check back in 5 years", "{ROOT_1}"),
        ],
    },
    # ── 2. Trump Iran Oil Seizure ── neutral, currently 5 comments
    {
        "article": "trump-iran-oil-seizure-june-2026",
        "comments": [
            # ROOTS
            ("RN_Geo", "oil at $92 and energy the only green on the board. been heavy XOM all year. dividends all day", None),
            ("crypto_refugee_88", "wait so oil stocks pump but tech is dying. stocks are so weird compared to crypto where everything moves together wtf", None),
            ("contango_cowboy", "WTI in backwardation getting spicy. the curve is screaming supply disruption risk. spot vs futures spread is wild rn", None),
            # REPLIES
            ("macro_dad_energy", "dollar strength is the real story here. everyones missing the macro. energy earnings gonna be wild next quarter", "{ROOT_0}"),
            ("yolo_my_401k", "idk what backwardation means but if oil keeps ripping im all in on XOM calls. this is my rent money jk", "{ROOT_2}"),
        ],
    },
    # ── 3. AIPO AI Power Infra ── bullish, currently 8 comments
    {
        "article": "aipo-ai-power-infra-dip-buy-june-2026",
        "comments": [
            # ROOTS
            ("Latter-Possibility", "finally someone talking about the power layer. chips are great but the grid is the real bottleneck. this is good long term tbh", None),
            ("sharp315", "been watching the defiance lineup for a while. AIPO actually makes sense not just a hype wrapper. depends on your timeline", None),
            ("mom_of_3_trading", "my kids are gonna need electricity whether its AI or not. just buying what i understand. boring but it works", None),
            # REPLIES
            ("thesis_driven_dan", "thesis is simple. every data center needs transformers switchgear cooling. eaton booked til 2029. valuation doesnt matter if the demand is real", "{ROOT_1}"),
            ("tacotuesdaytrader", "quick play while i eat lunch. love the power angle adding some AIPO shares. back to work see yall", "{ROOT_0}"),
        ],
    },
    # ── 4. Closing Bell June 11 ── bearish, currently 9 comments
    {
        "article": "closing-bell-june-11-2026",
        "comments": [
            # ROOTS
            ("this_time_is_different", "cpi 4.2% rate cuts dead semis in freefall. ive seen this movie before. nothing ever changes", None),
            ("SheriffBartholomew", "smci -28% in one day and oracle record quarter at -10%. retail always the exit liquidity. same story different ticker", None),
            ("bought_at_the_top", "of course smci drops 28% the day after i finally bought. youre welcome for the dip guys. this is fine 🔥", None),
            # REPLIES
            ("fomo_king_420", "kicking myself rn. almost bought smci puts yesterday. should have should have should have", "{ROOT_1}"),
            ("westcoastcouch", "whatever happens happens. not checking til june. market does what it does. see yall next month", "{ROOT_0}"),
        ],
    },
]

total_comments = 0
total_likes = 0

for plan in PLANS:
    article = plan["article"]
    print(f"\n{'='*60}")
    print(f"ARTICLE: {article}")
    print(f"{'='*60}")

    # Phase 1: Post comments, track root IDs
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
        time.sleep(0.3)

    print(f"  📊 Posted {len(all_my_ids)} comments")

    # Phase 2: Fetch all comment IDs and like ~60%
    time.sleep(1)
    print(f"\n  --- LIKES ---")
    all_ids = get_all_comment_ids(article)
    print(f"  Total comments on article: {len(all_ids)}")

    liked = 0
    for cid in all_ids:
        if random.random() < 0.6:
            # Each comment gets 1-2 likes from different users
            num_likes = random.randint(1, 2)
            likers = random.sample(LIKER_IDS, min(num_likes, len(LIKER_IDS)))
            for liker in likers:
                like_comment(cid, liker)
                liked += 1
                total_likes += 1
                time.sleep(0.12)

    print(f"  Liked {liked} times across {len(all_ids)} comments (~60%)")

print(f"\n{'='*60}")
print(f"TOTALS: {total_comments} comments posted, {total_likes} likes applied")
print(f"{'='*60}")
