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
# Updated: Cron run — fresh batch of authentic comments
# ═══════════════════════════════════════════════════════════════

PLANS = [
    # ── 1. AXON — The AI Monopoly Nobody's Talking About Just Dropped 50% ──
    {
        "article": "axon-public-safety-ai-moat-2026",
        "comments": [
            ("work_from_zoom", "i know a few cops and they all say axon body cams are basically mandatory now but the real lock in is evidence.com. once a department stores all their footage there theyre never leaving. the ai transcription and auto redaction stuff is what gets chiefs to sign the upgrade contracts. the dip feels like people forgot the switching costs exist.", None),
            ("whohebe123", "everyone screaming about the drop means theres probably an opportunity. market is pricing this like a hardware cyclical when the revenue is mostly subscription now. fading the panic feels right here.", None),
            ("bought_at_the_top", "bought axon right at the high because i saw the taser 10 adoption numbers and got excited. of course it cratered the next week. youre welcome for the dip gang. bagholder reporting in but honestly the more i read the better i feel about holding.", None),
            ("CarrotAwesome", "so theyre basically a software company now with hardware margins but the market still values them like they sell plastic boxes. someone explain why the multiple compression makes sense when recurring revenue keeps going up. the math aint mathing on this selloff.", None),
            ("paycheck2paycheck", "just doing my weekly buy into axon. been dcaing for months and this drop just means i get more shares for the same money. set it and forget it. the ai policing trend isnt going anywhere.", None),
        ],
    },
    # ── 2. CBRS — Cerebras Stock Got Halved. CEO Says Everyone Missed The Point ──
    {
        "article": "cerebras-wafer-scale-ai-chip-challenger-2026",
        "comments": [
            ("Latter-Possibility", "ipos always overshoot then correct then find their real level. cerebras has the wafer scale architecture that literally nobody else has and theyre signing real partnership deals. the openai relationship alone changes the narrative. corrections are healthy. this is the shakeout before the real trend establishes.", None),
            ("turned_into_a_newt", "the gross margin compression people are freaking out about is from the business model transition to full system sales. the s-1 was explicit about this. the metric that matters is revenue growth trajectory and the wse-3 deployment pipeline. this detail matters and the market is ignoring it completely.", None),
            ("fomo_king_420", "kicking myself for not selling cbrs at ipo. watched it rip up then gave it all back. should have taken profits. now im wondering if this is the bottom or if theres more pain coming. next time i swear i will take some off the table.", None),
            ("help_me_pls77", "cerebras is my biggest position and i dont know what to do. everyone says its a bad sign when margins shrink but the ceo says its intentional. my heart cant take this. ok im holding but talk me off the ledge please.", None),
            ("CCWaterBug", "i tossed some money at cbrs on the ipo dip. not checking it again until q3 earnings when the business model transition should start showing in the margins. or thursday who knows. playing the long game on the ai silicon story.", None),
        ],
    },
    # ── 3. RTX — Quarter-Trillion Market Cap, Defense Backlog Keeps Growing ──
    {
        "article": "rtx-defense-spending-surge-2026",
        "comments": [
            ("option_flow_watcher", "unusual call volume on rtx for the back months. someone is building a really large position betting on a move higher into year end. the flow has been consistently bullish for the past week while the stock drifted sideways. the options market sees something the chart isnt showing yet.", None),
            ("RN_Geo", "rtx is the most boring position in my portfolio and i love it. huge backlog, actual dividend, geopolitical tailwinds that arent going away. everyone chasing the next ai moonshot while the steady money just compounds in defense. no rush to buy but no reason to sell either.", None),
            ("grillmaster_finance", "my neighbor works at the local rtx plant and theyve been running weekend shifts for the first time in years. hiring like crazy. bought a few more shares while grilling burgers last weekend. good company making things the world actually needs. simple investing.", None),
            ("just_lurking_69", "been watching the defense chatter for a while. looks like european countries are scrambling to increase their budgets and rtx seems like the safest way to bet on that. does the backlog actually translate to revenue or is there a risk of cancellations. finally made an account to ask.", None),
            ("thesis_driven_dan", "the bull case on rtx is straightforward. they have multiyear visibility on the defense side and commercial aerospace is recovering. the diversified revenue base means a slowdown in one segment gets offset by the other. three things need to hold — nato spending keeps rising, commercial air travel stays strong, and the pratt gtf issues stay contained. if all three hit, the compound math is attractive.", None),
        ],
    },
    # ── 4. AMD — MI400 and the AI Chip Comeback Nobody Saw Coming ──
    {
        "article": "amd-mi400-ai-chip-comeback",
        "comments": [
            ("Minimum-Criticism763", "amd fans have been saying 'next year is the year' since 2022 and nvidia keeps printing money. the mi400 benchmarks look competitive on paper but the software stack is still catching up. follow the actual hyperscaler purchase orders not the conference demos. something doesnt add up when every cloud provider says they want competition but keep signing nvidia mega-deals.", None),
            ("still_holding_2021", "my amd bags from 2021 have been collecting dust for so long i forgot i even had them. but looking at the data center segment finally growing like crazy makes me think maybe this time is different. not crying anymore. one day my patience pays off.", None),
            ("night_shift_trader", "premarket looking spicy on amd today. quiet in here but the futures volume tells a story. someone knows something about the mi400 benchmarks leaking or something. night shift checking in from the warehouse.", None),
            ("thesis_driven_dan", "my thesis is simple. hyperscalers absolutely hate single vendor lock in on ai silicon. nvidia has the moat today but the big cloud providers will dual source the moment theres a credible alternative. mi400 is the first architecture that actually forces that conversation. if amd executes on software and the benchmarks hold, the revenue ramp is structural not cyclical.", None),
            ("tacotuesdaytrader", "took a small position in amd on my lunch break today. if mi400 is real i buy myself a nice dinner. if it flops its whatever. this stock is a burrito — sometimes the filling is great sometimes its a mess. tendies or sadness, either way im back to work.", None),
        ],
    },
    # ── 5. CRWD — CrowdStrike Weaponized the Worst IT Disaster, Now Splitting 4-for-1 ──
    {
        "article": "crowdstrike-falcon-ai-security-moat-2026",
        "comments": [
            ("SheriffBartholomew", "crowdstrike surviving the outage and turning into a comeback story is impressive PR but the stock already recovered and then some. retail is going to pile in on the stock split news and the smart money that bought the dip is going to sell them the shares. same story different ticker. retail always the exit liquidity.", None),
            ("mom_of_3_trading", "my oldest kid is studying cybersecurity in college and she says crowdstrike is the gold standard. the charlotte ai product is apparently all anyone in her classes talks about. bought a few shares for the kids. boring companies with sticky products doing boring things while the world gets more dangerous. dca between soccer practice dropoffs.", None),
            ("contango_cowboy", "the options market on crwd is screaming something interesting. the put skew completely collapsed after the outage recovery and now call premiums are building again. the vol curve is suggesting the market thinks the worst risk is behind them but the upside potential is underpriced. yeehaw the derivatives are telling the real story here.", None),
            ("whats_a_stop_loss", "i actually bought crwd during the outage because i thought it was overdone. everyone called me an idiot. now im up a ridiculous amount and i still havent sold because i have no discipline. update: lack of discipline worked out this time. stop loss?? who needs em. yolo.", None),
            ("data_dependent_1", "the renewal rate held above where analysts expected even during the worst of the outage backlash. that tells you everything about the product stickiness. charlotte ai attach rates are accelerating and the platform economics keep improving. the balance sheet is clean and free cash flow conversion is best in class among cybersecurity peers.", None),
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
