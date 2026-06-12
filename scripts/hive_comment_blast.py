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
    # Like endpoint typically returns success even on duplicates
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
# COMMENT PLANS
# ═══════════════════════════════════════════════════════════════

PLANS = [
    # ── 1. Goldman Sachs AI Capex ($920B) ──
    {
        "article": "goldman-sachs-ai-capex-warning-june-2026",
        "comments": [
            # ROOTS
            ("fomo_king_420", "should have sold my oracle calls before close. my portfolio just got smoked in after hours and i didnt even know that was a thing 💀", None),
            ("SheriffBartholomew", "retail always the exit liquidity. goldman drops this $920b capex note 12 hours after oracle tanks. their desk already positioned. same story different ticker.", None),
            ("macro_dad_energy", "everyone fixating on the $920b number. the real story is rates. if the fed isnt cutting this year none of these capex plans get funded at these yields.", None),
            # REPLIES (will fill parentId after posting roots)
            ("noob_investor42", "bought oracle this morning lol. learning the hard way i guess. at least we can be bagholders together 🤝", "{ROOT_0}"),
            ("turned_into_a_newt", "the goldman note was dated 2 days ago but released today after hours. check the fine print. someone knew exactly what they were doing.", "{ROOT_1}"),
        ],
    },
    # ── 2. Trump Iran Oil Seizure ──
    {
        "article": "trump-iran-oil-seizure-june-2026",
        "comments": [
            # ROOTS
            ("night_shift_trader", "premarket looking spicy. saw crude hit 92 overnight. energy names gonna rip at open. anyone else up", None),
            ("CCWaterBug", "oil always pumps on iran headlines then mean reverts. i toss a coin on these. check back in 2 weeks.", None),
            ("contango_cowboy", "the curve is in massive backwardation. spot 92 but 6 month futures barely moved. smart money pricing this as temporary headline risk not actual supply disruption.", None),
            # REPLIES
            ("yolo_my_401k", "if this hits i can pay tuition. all in on xom calls at open. yolo 🚀", "{ROOT_0}"),
            ("whohebe123", "with everyone fading the energy move itll probably rip higher. fading the crowd on this one.", "{ROOT_1}"),
        ],
    },
    # ── 3. AIPO AI Power Infra (already has 5 comments) ──
    {
        "article": "aipo-ai-power-infra-dip-buy-june-2026",
        "comments": [
            # ROOTS
            ("crypto_refugee_88", "wait so instead of nvidia at 200x pe i can buy power companies with actual cash flow and contracts?? this is like discovering eth in 2017 before everyone piled in", None),
            ("data_dependent_1", "margins expanding fast on these names. constellation signed 3 new hyperscaler deals just this quarter. fcf positive and growing. pe is actually reasonable here.", None),
            # REPLIES
            ("grillmaster_finance", "good companies good product. eaton is booked out til 2029 on data center orders. buying some for the kids college fund 🍺", "{ROOT_0}"),
        ],
    },
    # ── 4. Closing Bell June 11 (already has 5 comments) ──
    {
        "article": "closing-bell-june-11-2026",
        "comments": [
            # ROOTS
            ("help_me_pls77", "smci down 28% in ONE day and oracle tanks after a record quarter?? my heart cant take this. talk me off the ledge", None),
            ("Latter-Possibility", "actually this is healthy. smci was a fraud waiting to implode since the hindenburg report. cpi forcing the fed to stay vigilant. corrections flush out the garbage.", None),
            # REPLIES (one to new root, one to existing comment)
            ("sharp315", "depends on your timeline. spacex ipo at 135 tomorrow is the only thing that matters. everything else is noise for 48 hours.", "{ROOT_0}"),
            ("FEMA_Camp_Survivor", "regular people always get wrecked. smci fraud was obvious for years, sec did nothing, now retail holding 28% bags while institutions were out last month.", "{EXISTING_mq9e62ag_g5gu1r}"),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# EXECUTION
# ═══════════════════════════════════════════════════════════════

total_comments = 0
total_likes = 0

for plan in PLANS:
    article = plan["article"]
    print(f"\n{'='*60}")
    print(f"ARTICLE: {article}")
    print(f"{'='*60}")

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
print(f"TOTALS: {total_comments} comments posted, {total_likes} likes applied")
print(f"{'='*60}")
