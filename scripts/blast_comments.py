#!/usr/bin/env python3
"""Generate and post Reddit-style comments for The Signal articles.
Posts top-level comments first, captures server IDs, then posts replies.
"""
import json
import random
import string
import requests
from datetime import datetime, timezone

SERVICE_TOKEN = "hive-comment-blast-2026"
COMMENTS_FILE = "/home/chino/thesignal/data/comments.json"
API_URL = "https://readthesignal.net/api/comments"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SERVICE_TOKEN}"
}

def gen_id():
    p1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    p2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{p1}_{p2}"

def gen_uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Define all comments. Top-level have parentId=None.
# Replies reference a local key; we'll resolve to server IDs after posting top-levels.
# Format: (article, text, author, parent_key_or_None)
# parent_key is a string like "a1_c1" for local resolution.
comments_spec = [
    # === ARTICLE 1: iridium-satellite-iot-defense-june-2026 ===
    ("iridium-satellite-iot-defense-june-2026",
     "66 crosslinked LEO birds, $738.5M DoD contract, and full Aireon ownership for space-based air traffic surveillance. SpaceX gets the headlines but IRDM owns the constellation the Pentagon actually relies on when comms go dark. That's the real moat.",
     "RN_Geo", None),
    ("iridium-satellite-iot-defense-june-2026",
     "bro its already up 168% YTD and i just found out about it. classic me catching a runner at the top pray for my bags",
     "fomo_king_420", "a1_c1"),
    ("iridium-satellite-iot-defense-june-2026",
     "$875.8M TTM revenue, 71.6% gross margins, $253M free cash flow, and a $0.60/share dividend. 1.9% revenue growth isnt exciting but the Aireon buy gives them a space-based air traffic monopoly nobody can replicate. Forward PE of 34.2x means you're paying for growth that hasnt shown up yet.",
     "data_dependent_1", None),

    # === ARTICLE 2: nvidia-windows-pc-chip-2026 ===
    ("nvidia-windows-pc-chip-2026",
     "nvda making windows pc chips now?? jensen said TAM expansion and he wasnt kidding. INTC in absolute shambles rn",
     "whats_a_stop_loss", None),
    ("nvidia-windows-pc-chip-2026",
     "so nvidia builds a chip with RTX 5070 graphics AND CUDA cores on one die for windows laptops and the stock is down 17% from ATH. the math aint mathing",
     "CarrotAwesome", "a2_c1"),
    ("nvidia-windows-pc-chip-2026",
     "CUDA on a laptop is the whole story. Every dev running local LLMs or image gen picks this over x86. INTC at $114 and AMD at $516 are pricing in PC dominance that might not last. NVDA entering at $211 is platform expansion that compounds for a decade.",
     "thesis_driven_dan", None),

    # === ARTICLE 3: iran-threatens-tech-defense-2026 ===
    ("iran-threatens-tech-defense-2026",
     "The IRGC demonstrated strike capability with 300+ drones and missiles at Israel in one salvo. Middle East cloud data centers and subsea cables are soft targets. This isn't posturing — it's a real operational threat vector. RTX, LMT, and NOC gapping up is the market pricing in sustained elevated defense spend.",
     "RN_Geo", None),
    ("iran-threatens-tech-defense-2026",
     "loaded up on RTX calls this morning. if iran is threatening our tech infrastructure the defense budget is only going one direction and its not down",
     "first_time_caller99", "a3_c1"),
    ("iran-threatens-tech-defense-2026",
     "iran threatening to hit us data centers and the market response is buying defense stocks. nobody learned anything from the last 20 years. regular people always get wrecked when this stuff escalates.",
     "FEMA_Camp_Survivor", None),

    # === ARTICLE 4: google-pentagon-classified-ai-deal ===
    ("google-pentagon-classified-ai-deal",
     "Anthropic locked out of Pentagon AI because they wouldn't play ball on military applications. Google learned from Project Maven 2018 — you don't walk away from defense contracts. Gemini on SIPRNet and JWICS is a multi-decade moat. At 26x forward PE and $160.2B net income, this isn't priced in yet.",
     "thesis_driven_dan", None),
    ("google-pentagon-classified-ai-deal",
     "bought googl at 400 and been watching it bleed. this pentagon deal was supposed to be the catalyst. still waiting lmao",
     "bought_at_the_top", None),
    ("google-pentagon-classified-ai-deal",
     "$4.56T market cap and 80% of revenue is still ads. pentagon AI is a rounding error at that scale. wake me up when PE drops below 20",
     "Shdwrptr", "a4_c2"),

    # === ARTICLE 5: if-i-could-hold-one-stock-for-5-years-id-pick-google ===
    ("if-i-could-hold-one-stock-for-5-years-id-pick-google",
     "22x forward earnings, $110B net cash, cloud growing 63% YoY. the market is pricing google like it's dying when it's actually accelerating. check back in 2030.",
     "CCWaterBug", None),
    ("if-i-could-hold-one-stock-for-5-years-id-pick-google",
     "$39.7B in operating income in a single quarter at 36% margins. that's not a search company — that's a cash furnace. everyone obsessing over AI chatbots is missing the forest.",
     "macro_dad_energy", "a5_c1"),
    ("if-i-could-hold-one-stock-for-5-years-id-pick-google",
     "third google-is-undervalued article this month. institutions loading up while retail buys mag 7 etfs. the trade is getting crowded and nobody wants to admit it.",
     "SheriffBartholomew", None),
]

# Separate top-level and replies
top_levels = []
replies = []
for i, (article, text, author, parent_key) in enumerate(comments_spec):
    entry = {
        "idx": i,
        "article": article,
        "text": text,
        "author": author,
        "parent_key": parent_key,
    }
    if parent_key is None:
        top_levels.append(entry)
    else:
        replies.append(entry)

# Map local key -> server ID
key_to_server_id = {}

# Assign local keys to top-level entries
for i, tl in enumerate(top_levels):
    art_slug = tl["article"]
    art_num = art_slug.split("-")[0] if art_slug else f"art{i}"
    local_key = f"a{['iridium','nvidia','iran','google','if'][i // 3 + (0 if i < 6 else 1)]}_c{i+1}"  # simple mapping
    # Better: derive from index position in original spec
    local_key = chr(97 + tl["idx"] // 3) + str((tl["idx"] % 3) + 1) + "_c" + str((tl["idx"] % 3) + 1)  # generic

# Reset with proper key mapping by looking up from comments_spec
for i, (article, text, author, parent_key) in enumerate(comments_spec):
    art_prefix = ["a1", "a2", "a3", "a4", "a5"][i // 3]
    c_num = (i % 3) + 1
    this_key = f"{art_prefix}_c{c_num}"
    if parent_key is None:
        # This is a top-level
        pass  # will assign server ID later
    # We'll store key assignments in the entry

print("=== POSTing top-level comments first ===")
success = 0
fail = 0

for i, (article, text, author, parent_key) in enumerate(comments_spec):
    if parent_key is not None:
        continue  # skip replies for now
    
    art_prefix = ["a1", "a2", "a3", "a4", "a5"][i // 3]
    c_num = (i % 3) + 1
    local_key = f"{art_prefix}_c{c_num}"
    
    payload = {
        "article": article,
        "text": text,
        "author": author,
        "uid": gen_uid(),
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            server_id = data["comment"]["id"]
            key_to_server_id[local_key] = server_id
            success += 1
            print(f"  OK  [{author}] {local_key} -> server_id={server_id}")
        else:
            fail += 1
            print(f"  FAIL [{author}] {local_key} -> {resp.status_code}: {resp.text[:150]}")
    except Exception as e:
        fail += 1
        print(f"  ERR [{author}] {local_key} -> {e}")

print(f"\nTop-levels: {success} OK, {fail} FAIL")
print(f"Server ID map: {json.dumps(key_to_server_id, indent=2)}")

# Now post replies
print("\n=== POSTing reply comments ===")
for i, (article, text, author, parent_key) in enumerate(comments_spec):
    if parent_key is None:
        continue
    
    server_parent_id = key_to_server_id.get(parent_key)
    if not server_parent_id:
        print(f"  SKIP [{author}] parent_key={parent_key} has no server ID, skipping")
        fail += 1
        continue
    
    payload = {
        "article": article,
        "text": text,
        "author": author,
        "uid": gen_uid(),
        "parentId": server_parent_id,
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            success += 1
            print(f"  OK  [{author}] reply to {parent_key} (server={server_parent_id})")
        else:
            fail += 1
            print(f"  FAIL [{author}] reply to {parent_key} -> {resp.status_code}: {resp.text[:150]}")
    except Exception as e:
        fail += 1
        print(f"  ERR [{author}] reply to {parent_key} -> {e}")

print(f"\n=== FINAL RESULTS: {success} succeeded, {fail} failed out of {len(comments_spec)} ===")

# Now build final comments list for JSON file with server IDs
# (We'll use server IDs where available, local IDs as fallback)
final_comments = []
for i, (article, text, author, parent_key) in enumerate(comments_spec):
    art_prefix = ["a1", "a2", "a3", "a4", "a5"][i // 3]
    c_num = (i % 3) + 1
    local_key = f"{art_prefix}_c{c_num}"
    
    server_parent = key_to_server_id.get(parent_key) if parent_key else None
    
    cmt = {
        "id": key_to_server_id.get(local_key, gen_id()),
        "article": article,
        "text": text,
        "author": author,
        "photoURL": None,
        "uid": gen_uid(),
        "parentId": server_parent if parent_key else None,
        "createdAt": now,
        "likes": []
    }
    final_comments.append(cmt)

# Append to comments.json
with open(COMMENTS_FILE, 'r') as f:
    existing = json.load(f)

existing.extend(final_comments)

with open(COMMENTS_FILE, 'w') as f:
    json.dump(existing, f, indent=2)

print(f"\nAppended {len(final_comments)} comments to {COMMENTS_FILE}")
print(f"Total comments now: {len(existing)}")
