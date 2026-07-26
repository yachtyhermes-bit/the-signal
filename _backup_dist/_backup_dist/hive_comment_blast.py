#!/usr/bin/env python3
"""
Hive Comment Swarm — Posts Reddit-style comments on The Signal articles.
"""
import json
import subprocess
import sys
import re
import random
import time

API_BASE = "https://readthesignal.net"
TOKEN = "hive-comment-blast-2026"

PERSONAS = [
    {"id":"first_time_caller99","style":"newbie","outlook":"nervous"},
    {"id":"noob_investor42","style":"newbie","outlook":"confused"},
    {"id":"help_me_pls77","style":"newbie","outlook":"nervous"},
    {"id":"yolo_my_401k","style":"newbie","outlook":"reckless"},
    {"id":"just_lurking_69","style":"newbie","outlook":"neutral"},
    {"id":"mom_of_3_trading","style":"newbie","outlook":"steady"},
    {"id":"bought_at_the_top","style":"newbie","outlook":"hopeful"},
    {"id":"crypto_refugee_88","style":"newbie","outlook":"confused"},
    {"id":"night_shift_trader","style":"newbie","outlook":"neutral"},
    {"id":"fomo_king_420","style":"newbie","outlook":"anxious"},
    {"id":"sharp315","style":"intermediate","outlook":"neutral"},
    {"id":"whohebe123","style":"intermediate","outlook":"contrarian"},
    {"id":"CarrotAwesome","style":"intermediate","outlook":"skeptical"},
    {"id":"RN_Geo","style":"intermediate","outlook":"cautious"},
    {"id":"Shdwrptr","style":"intermediate","outlook":"neutral"},
    {"id":"CCWaterBug","style":"intermediate","outlook":"steady"},
    {"id":"SheriffBartholomew","style":"intermediate","outlook":"bearish"},
    {"id":"Minimum-Criticism763","style":"intermediate","outlook":"skeptical"},
    {"id":"westcoastcouch","style":"intermediate","outlook":"chill"},
    {"id":"tacotuesdaytrader","style":"intermediate","outlook":"neutral"},
    {"id":"paycheck2paycheck","style":"intermediate","outlook":"steady"},
    {"id":"still_holding_2021","style":"intermediate","outlook":"hopeful"},
    {"id":"grillmaster_finance","style":"intermediate","outlook":"steady"},
    {"id":"whats_a_stop_loss","style":"intermediate","outlook":"reckless"},
    {"id":"turned_into_a_newt","style":"advanced","outlook":"neutral"},
    {"id":"FEMA_Camp_Survivor","style":"advanced","outlook":"bearish"},
    {"id":"Latrodectus1990","style":"advanced","outlook":"bearish"},
    {"id":"Latter-Possibility","style":"advanced","outlook":"bullish"},
    {"id":"ragnaroksunset","style":"advanced","outlook":"neutral"},
    {"id":"data_dependent_1","style":"advanced","outlook":"neutral"},
    {"id":"option_flow_watcher","style":"advanced","outlook":"neutral"},
    {"id":"macro_dad_energy","style":"advanced","outlook":"neutral"},
    {"id":"contango_cowboy","style":"advanced","outlook":"neutral"},
    {"id":"this_time_is_different","style":"advanced","outlook":"skeptical"},
    {"id":"thesis_driven_dan","style":"advanced","outlook":"neutral"},
    {"id":"work_from_zoom","style":"advanced","outlook":"bullish"},
]

REPLY_SPECIALISTS = [
    {"id":"hype_man","style":"advanced","outlook":"bullish"},
    {"id":"market_debater","style":"advanced","outlook":"skeptical"},
    {"id":"quiet_observer","style":"advanced","outlook":"neutral"},
]


def fetch(url):
    r = subprocess.run(["curl", "-sL", url], capture_output=True, text=True, timeout=20)
    return r.stdout


def fetch_and_save(url, path):
    """Fetch a URL and save to a file, return content."""
    r = subprocess.run(["curl", "-sL", url, "-o", path], capture_output=True, text=True, timeout=20)
    with open(path) as f:
        return f.read()


def post_comment(slug, text, author, parent_id=None):
    payload = json.dumps({
        "article": slug, "text": text, "author": author,
        "parentId": parent_id, "token": TOKEN,
    })
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", f"{API_BASE}/api/comments/",
         "-H", "Content-Type: application/json", "-d", payload],
        capture_output=True, text=True, timeout=20,
    )
    try:
        data = json.loads(r.stdout)
        # The response has comment nested under "comment" key
        if "comment" in data and "id" in data["comment"]:
            return data["comment"]["id"]
        elif "id" in data:
            return data["id"]
        return None
    except json.JSONDecodeError:
        print(f"  PARSE ERROR: {r.stdout[:500]}")
        return None


def get_article_slugs():
    html = fetch(f"{API_BASE}/")
    slugs = re.findall(r'href="/article/([^"]+)"', html)
    seen = set()
    uniq = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq[:8]


def get_comment_count(slug):
    data = fetch(f"{API_BASE}/api/comments/?article={slug}")
    try:
        return len(json.loads(data))
    except json.JSONDecodeError:
        return 0


def get_article_info(slug):
    """Get ticker and title for an article by fetching its page."""
    html = fetch(f"{API_BASE}/article/{slug}")
    # Try ticker badge on article page
    m = re.search(r'ticker-badge[^>]*>([^<]+)<', html, re.IGNORECASE)
    ticker = m.group(1).strip() if m else ""
    # Title from h1
    m2 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', "", (m2.group(1) if m2 else slug)).strip()
    return ticker, title


def gen_comment(persona, ticker):
    t = ticker.upper() if ticker else "this"
    style = persona["style"]

    newbie = [
        f"just opened a position in {t} hope im not too late",
        f"been watching {t} for a bit. thinking about pulling the trigger",
        f"is {t} a buy here or should i wait for a better entry",
        f"my first time buying something like this. learning as i go",
        f"heard about this and decided to look into it. interesting stuff",
        f"i literally just started investing last month. this seems legit",
        f"bought a tiny bit of {t} to start. baby steps",
        f"what do you guys think about {t} long term",
        f"my cousin told me about {t}. got a small position now",
        f"nervous about jumping into {t} but the fomo is real",
        f"only down a bit on {t} so far. should i add more or wait",
        f"new to this whole thing but this makes sense to me",
        f"been saving up to buy some {t}. hope the dip holds",
    ]
    inter = [
        f"depends on your timeline but {t} seems solid long term",
        f"everyone sleeping on {t} rn. typical setup for a runner",
        f"something feels off here. gonna sit this one out",
        f"not touching {t} at these levels. waiting for a better setup",
        f"slow and steady wins the race. dca into {t} and forget it",
        f"still holding my {t} bags. one day this works out",
        f"went in heavy on {t}. either genius or stupid we will see",
        f"neutral on {t} right now. waiting to see next quarter",
        f"good company good product. i use their stuff every day",
        f"the setup on {t} is interesting but im cautious here",
    ]
    adv = [
        f"this sector is going to get obliterated. been saying it for months",
        f"actually think this is healthy. corrections create buying opportunities",
        f"the macro picture matters more than any single ticker here",
        f"balance sheet looks clean on {t}. worth keeping an eye on",
        f"margins are expanding but need to see sustained growth first",
        f"unusual options flow on {t} today. someone knows something",
        f"rates are the real story here. {t} is just a symptom",
        f"this time is different they said. famous last words",
        f"generational bagholders incoming on this sector",
    ]
    pool = {"newbie": newbie, "intermediate": inter, "advanced": adv}
    return random.choice(pool.get(style, inter))


def gen_reply(specialist, ticker):
    t = ticker.upper() if ticker else "this"
    pid = specialist["id"]
    if pid == "hype_man":
        pool = [
            f"preach been saying this for weeks about {t}",
            f"this guy gets it. people are sleeping on the potential",
            f"finally someone talking sense about {t}",
            f"exactly what i was thinking. the setup is too clean to ignore",
        ]
    elif pid == "market_debater":
        pool = [
            f"hard disagree. the numbers dont support that thesis yet",
            f"id argue the opposite actually. wait for earnings first",
            f"respectfully youre looking at this wrong. check the cash flow",
            f"not so sure. the competitive landscape keeps shifting",
        ]
    else:
        pool = [
            f"interesting take. watching how this plays out",
            f"hmm hadnt thought of it that way. food for thought",
            f"both sides have valid points. time will tell whos right",
            f"curious where this goes. keeping an open mind",
        ]
    return random.choice(pool)


def run():
    print("=" * 60)
    print("HIVE COMMENT SWARM — Starting run")
    print("=" * 60)

    all_slugs = get_article_slugs()
    print(f"\nFound {len(all_slugs)} article slugs from homepage")

    articles = []
    for slug in all_slugs:
        count = get_comment_count(slug)
        ticker, title = get_article_info(slug)
        print(f"  [{slug}] ticker={ticker} comments={count}")
        if count < 5:
            articles.append({"slug":slug, "ticker":ticker, "title":title})
        if len(articles) >= 5:
            break
        time.sleep(0.3)

    if not articles:
        print("\nNo articles with <5 comments. Nothing to do.")
        return

    print(f"\nTargeting {len(articles)} articles:")
    for a in articles:
        print(f"  - {a['slug']} ({a['ticker']})")

    posted = 0
    failed = 0

    for art in articles:
        slug = art["slug"]
        ticker = art["ticker"]
        title = art["title"]

        print(f"\n{'─'*50}")
        print(f"ARTICLE: {title}")
        print(f"  Slug: {slug} | Ticker: {ticker}")

        # Pick 3 root personas: 2 newbies + 1 trader, shuffled
        all_p = PERSONAS.copy()
        random.shuffle(all_p)
        newbs = [p for p in all_p if p["style"] == "newbie"]
        trds = [p for p in all_p if p["style"] != "newbie"]
        roots = random.sample(newbs, min(2, len(newbs))) + random.sample(trds, min(1, len(trds)))
        random.shuffle(roots)

        print(f"  Root personas: {[p['id'] for p in roots]}")

        # Post root comments
        root_ids = []
        for p in roots:
            txt = gen_comment(p, ticker)
            if len(txt) > 297:
                txt = txt[:294] + "..."
            print(f"  -> Posting root by {p['id']}: {txt}")
            cid = post_comment(slug, txt, p["id"])
            if cid:
                root_ids.append(cid)
                posted += 1
                print(f"    OK ID: {cid}")
            else:
                failed += 1
                print(f"    FAILED")
            time.sleep(1.5)

        # Post 2 replies to the roots
        if root_ids:
            chosen = random.sample(REPLY_SPECIALISTS, min(2, len(REPLY_SPECIALISTS)))
            for i, rp in enumerate(chosen):
                pid = root_ids[i % len(root_ids)]
                txt = gen_reply(rp, ticker)
                if len(txt) > 297:
                    txt = txt[:294] + "..."
                print(f"  -> Posting reply by {rp['id']} (parent {pid}): {txt}")
                rid = post_comment(slug, txt, rp["id"], pid)
                if rid:
                    posted += 1
                    print(f"    OK Reply ID: {rid}")
                else:
                    failed += 1
                    print(f"    FAILED reply")
                time.sleep(1.5)
        else:
            print("  No root comments posted, skipping replies")

        time.sleep(1.0)

    print(f"\n{'='*60}")
    print(f"BLAST COMPLETE")
    print(f"  Posted: {posted}")
    print(f"  Failed: {failed}")
    print(f"{'='*60}")


if __name__ == "__main__":
    run()
