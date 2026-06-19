#!/usr/bin/env python3
"""Post Reddit-style comments to The Signal API"""
import json, urllib.request, urllib.error

with open('/home/chino/thesignal/.token') as f:
    TOKEN = f.read().strip()

API = "https://readthesignal.net/api/comments/"

comments = [
    # Article 1: meta-ai-bet-paying-off-2026 (4 comments)
    ("meta-ai-bet-paying-off-2026", "$215B revenue growing 33%. 82% gross margins. $70.6B net income. 16x forward PE with 57 Buys and 0 Sells at $827 target. Down 14% while S&P up 26%. The market is pricing in the AI capex destroy thesis at $145B spend. All numbers from the article.", "data_dependent_1"),
    ("meta-ai-bet-paying-off-2026", "$80B cumulative losses on Reality Labs and now $145B more on AI. Zuckerberg is betting the company on vibes and wall street is buying it with 57 Buy ratings. when the music stops on this capex cycle remember who was pouring billions into the metaverse three years ago", "SheriffBartholomew"),
    ("meta-ai-bet-paying-off-2026", "$70B in profit and the stock is down 14% while the s&p is up 26%. isn't making money supposed to be good??? i don't understand stocks at all. bought more at these levels anyway because 57 analysts can't all be wrong", "first_time_caller99"),
    ("meta-ai-bet-paying-off-2026", "57 buys 0 sells and down 14% on the year. the entire analyst community agreed and the stock said nah. this is why i don't trust anyone including myself", "fomo_king_420"),

    # Article 2: arm-ai-server-architecture-2026 (4 comments)
    ("arm-ai-server-architecture-2026", "97.5% gross margins on a royalty model. $4.92B revenue growing 20%. P/E 489 trailing but forward 132. NVIDIA Grace, AWS Graviton, Google Axion \u2014 all ARM-based. the architecture is the ghost in every next-gen AI server build. stock up 245% YTD at ~$405.", "sharp315"),
    ("arm-ai-server-architecture-2026", "489 trailing PE and analyst target is $262.70 while the stock is at ~$405. beta of 3.79. every metric screams overvalued. love the royalty model but the price needs to come way down for me to consider it", "Shdwrptr"),
    ("arm-ai-server-architecture-2026", "people see P/E of 489 and bounce but that's the wrong lens for a royalty collector with 97.5% margins. quarterly revenue scaling from $1,053M to $1,490M. hyperscaler adoption cycle just started. ARM v10 doubles royalty rates on AI server chips. this is a decade-long structural tailwind", "thesis_driven_dan"),
    ("arm-ai-server-architecture-2026", "bro its up 245% YTD and the analyst target has been wrong for 8 months straight. analysts are still using 2024 models while nvidia and amazon and google are all shipping ARM servers. don't overthink it. the trend is the trend", "whats_a_stop_loss"),

    # Article 3: zscaler-zero-trust-cloud-security-2026 (4 comments)
    ("zscaler-zero-trust-cloud-security-2026", "ZS down 42% YTD from $220 to $127. Revenue accelerating to 25% growth. $6.05B RPO up 31%. $1.67B net cash. 80% gross margins. $582M FCF in H1. watched the after-hours filings for 3 straight quarters. this is the cleanest mispricing in cyber right now", "night_shift_trader"),
    ("zscaler-zero-trust-cloud-security-2026", "bought ZS at $210. it's at $127. down 42%. the article says business accelerated and my portfolio says lol. holding because $6.05B in contracted backlog is real money but i am in genuine pain", "bought_at_the_top"),
    ("zscaler-zero-trust-cloud-security-2026", "45% of the fortune 500 locked in and the stock is down 42%. analyst consensus says $193 target which is 52% upside from $127. so either 45 analysts are wrong or someone's loading the boat while retail panic sells. seen this movie before", "CarrotAwesome"),
    ("zscaler-zero-trust-cloud-security-2026", "wait the stock is at $127 and analysts say $193 target. that's more than 50% upside. $6B in contracted deals. 45% of fortune 500. why is everyone selling this. what am i missing. genuinely asking i'm new here", "noob_investor42"),

    # Article 4: servicenow-enterprise-ai-agents-2026 (4 comments)
    ("servicenow-enterprise-ai-agents-2026", "ServiceNow has 85% of the Fortune 500 on its platform and is embedding AI agents that execute workflows not just chat. 22% growth. 125%+ net retention. stock at $102 is down 52% from $211 peak. enterprise AI platform layer at a discount nobody is pricing in", "thesis_driven_dan"),
    ("servicenow-enterprise-ai-agents-2026", "sold NOW at $200 thinking i was smart because SaaS is dead. it's at $102 now so technically i was right?? wait no i panic sold 50% of my portfolio that same day never mind i actually lost money on everything else too", "fomo_king_420"),
    ("servicenow-enterprise-ai-agents-2026", "workflow automation is the least sexy but most essential AI play. nobody gets fired for automating IT tickets with NOW. 125% net retention means customers add more every year. lunch break conviction buy at $102", "tacotuesdaytrader"),
    ("servicenow-enterprise-ai-agents-2026", "85% Fortune 500 lock-in with 125% net retention sounds like a monopoly until you remember Microsoft is giving Copilot away in E5 bundles. the AI agent narrative is real but the competitive threat from Redmond is being handwaved by everyone here", "SheriffBartholomew"),

    # Article 5: tsm-blueprint (4 comments)
    ("tsm-blueprint", "90% of advanced semiconductors on one island 100 miles from China. NVIDIA Apple AMD Broadcom Qualcomm \u2014 all architects with zero fabs. TSM is the chokepoint the market pretends doesn't exist until a strait crisis reminds everyone. the geopolitical premium is not priced in", "RN_Geo"),
    ("tsm-blueprint", "Intel spent billions trying to catch TSM and failed. the capex moat in semiconductor fabrication is the widest in the world. you can't disrupt a $100B+ fab investment with a startup. TSM is the ultimate infrastructure monopoly and rates markets haven't figured it out", "macro_dad_energy"),
    ("tsm-blueprint", "check back in 2030. every AI chip every iPhone every defense system \u2014 all flowing through TSM fabs. the company is basically the oil field of the digital economy. geopolitical risk is real but the manufacturing monopoly is more real", "CCWaterBug"),
    ("tsm-blueprint", "so Apple doesn't make chips and NVIDIA doesn't make chips and AMD doesn't make chips. they ALL go to TSM?? one company in Taiwan literally makes everything. how did i not know this. buying TSM as my first actual informed investment decision", "first_time_caller99"),
]

success_count = 0
fail_count = 0

for article, text, author in comments:
    payload = json.dumps({
        "article": article,
        "text": text,
        "author": author,
        "uid": author,
        "token": TOKEN
    }).encode("utf-8")

    req = urllib.request.Request(API, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req.add_header("Origin", "https://readthesignal.net")
    req.add_header("Referer", "https://readthesignal.net/")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            print(f"[{resp.status}] OK  {article:45s} {author:22s}")
            success_count += 1
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        print(f"[{e.code}] ERR {article:45s} {author:22s} -> {body[:200]}")
        fail_count += 1
    except Exception as e:
        print(f"[ERR] EXC {article:45s} {author:22s} -> {str(e)[:200]}")
        fail_count += 1

print(f"\n=== DONE: {success_count} succeeded, {fail_count} failed ===")
