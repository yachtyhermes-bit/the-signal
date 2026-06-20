#!/usr/bin/env python3
"""Dynamic Comment Blast — generates and posts Reddit-style comments for latest articles."""

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
        print(f"  OK [{cid}] {author}: {text[:70]}...")
        return cid
    else:
        print(f"  FAIL: {data}")
        return None

def like_comment(comment_id, uid):
    payload = {"commentId": comment_id, "uid": uid, "token": TOKEN}
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

# ============================================================
# COMMENT PLANS - 5 most recent articles, June 18-19 2026
# ============================================================

PLANS = [
    # -- 1. CrowdStrike Impossible Comeback (Jun 19) --
    {
        "article": "crowdstrike-post-outage-comeback-2026",
        "comments": [
            ("noob_investor42", "sold my crwd during that blue screen panic. learning the hard way that bad news is usually the best time to buy. diamond hands next time i guess", None),
            ("work_from_zoom", "we run falcon across our whole stack at work. the switching costs are insane once youre in crowdstrikes ecosystem. outage was a buying opp hiding in plain sight for anyone who actually uses the product", None),
            ("SheriffBartholomew", "retail panic sold during the outage and now the stock is ripping higher while institutions feasted on the fear. same story different ticker. were all about to get shafted on the next cyber name too", None),
            ("this_time_is_different", "this time is different guys. an outage that should have killed them just handed them the deepest threat telemetry dataset in the industry. ive seen this movie before and it ends with crwd owning the enterprise", None),
            ("option_flow_watcher", "someone bought a ton of crwd calls expiring next month. flow looks very bullish. gamma could push this way higher than people expect", None),
        ],
    },
    # -- 2. ServiceNow SaaSpocalypse Bet (Jun 19) --
    {
        "article": "servicenow-ai-agent-enterprise-moat-2026",
        "comments": [
            ("first_time_caller99", "is this a good time to buy servicenow? my first stock ever was pltr and that didnt go great lol. this seems like a real business though. learning as i go", None),
            ("CarrotAwesome", "so the business is accelerating and the stock is getting crushed. someone explain this to me like im 5. the math aint mathing on this one", None),
            ("Latter-Possibility", "actually this is healthy. when growth companies are smashing numbers but the stock sells off on sector rotation thats the signal. corrections are normal and this is good long term", None),
            ("thesis_driven_dan", "my thesis on $NOW is simple. enterprise ai agents are the next wave and servicenow owns the workflow layer. the bull case rests on them being the integration fabric for every enterprise ai deployment", None),
            ("ragnaroksunset", "yep", None),
            ("tacotuesdaytrader", "taking the fam to chipotle on this when it bounces. quick play while i eat lunch. back to work see yall", None),
        ],
    },
    # -- 3. SoFi Record Profits (Jun 19) --
    {
        "article": "sofi-the-fintech-that-quietly-figured-out-profits",
        "comments": [
            ("help_me_pls77", "should i be worried about sofi? down this much while actually making money doesnt make any sense. my heart cant take this but ok im holding", None),
            ("Minimum-Criticism763", "something doesnt add up. a profitable fintech growing users and deposits gets punished while unprofitable ai startups get premium valuations. follow the incentives", None),
            ("data_dependent_1", "balance sheet looks clean and deposits are growing fast. margins expanding. the market is pricing this like a regional bank when its a tech platform with bank economics. actual revenue growth is strong", None),
            ("westcoastcouch", "whatever happens happens. im not checking til august. this is my fun money and market does what it does", None),
            ("crypto_refugee_88", "wait sofi actually makes money and has real users?? after getting rugged in crypto this feels like discovering a cheat code. at least it wont rug and stocks are so slow", None),
        ],
    },
    # -- 4. Palantir $13.7B Government Contracts (Jun 18) --
    {
        "article": "palantir-aip-defense-contracts-2026",
        "comments": [
            ("FEMA_Camp_Survivor", "the system is designed this way. pltr literally runs pentagon ai infrastructure and the stock gets destroyed while spacs with no revenue pump. american capitalism has become a joke", None),
            ("Latrodectus1990", "ive been saying this for months. palantir is the most misunderstood company in the market right now. watch what happens when those government contracts start converting to revenue at scale", None),
            ("whohebe123", "with all this negative sentiment on $PLTR itll probably rip higher. everyone is too bearish rn. fading the crowd hard on this one", None),
            ("bought_at_the_top", "of course it dropped after i bought. youre welcome for the dip guys. bagholder reporting in. my timing is legendary", None),
            ("grillmaster_finance", "good company good product. my father in law is a contractor and says everyone uses palantir now. bought some for the kids college fund", None),
            ("Shdwrptr", "not at this valuation. if it was cheaper id buy but too pricey for me rn. pass", None),
        ],
    },
    # -- 5. AMD Quiet AI Empire (Jun 18) --
    {
        "article": "amd-mi400-ai-chip-underdog-2026",
        "comments": [
            ("yolo_my_401k", "all in on amd. if this hits i can pay off my loans. this is my rent money jk but seriously lisa su is building something special here", None),
            ("contango_cowboy", "the curve is telling us something. amd chips are in every hyperscaler now and nobodys pricing in the mi400 ramp. yeehaw the calls are cheap and spot demand is surging", None),
            ("paycheck2paycheck", "just doing my weekly buy into amd. set it and forget it. not checking til friday. boring but it works", None),
            ("CCWaterBug", "playing the long game on amd. 2030 for me maybe longer. check back in 5 years when the ai chip duopoly is fully priced in", None),
            ("still_holding_2021", "been holding amd since 2021 and finally in the green. one day this pays off even bigger. im not crying youre crying", None),
            ("whats_a_stop_loss", "stop loss?? never heard of her. yolo. this is either genius or stupid but with lisa su at the helm i like my odds", None),
        ],
    },
]

# ============================================================
# EXECUTION
# ============================================================

total_comments = 0
total_likes = 0

for plan in PLANS:
    article = plan["article"]
    print(f"\n{'='*60}")
    print(f"ARTICLE: {article}")
    print(f"{'='*60}")

    # PHASE 1: Post comments
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

    # PHASE 2: Like ~60% of all comments on the article
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
