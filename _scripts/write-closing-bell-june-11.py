#!/usr/bin/env python3
"""Write the closing bell article JSON for June 11, 2026."""

import json
import os

body_html = """<p>CPI hit 4.2%. Iran strikes escalated. Oracle reported a record quarter and still crashed 10% after hours. SMCI got deleted — -28% in a single session. Wednesday was the kind of day where you just close the app and walk away.</p>

<p>The macro grenade: <strong>CPI came in at 4.2%</strong> — hottest inflation in three years. Rate cuts are dead. The market cascaded from open to close. S&P 500 finished at its absolute low of <strong>7,266.99 (-1.62%)</strong>. Nasdaq torched <strong>-2.0%</strong>. Dow shed <strong>-1.88%</strong>. Four straight days of selling — the S&P has bled <strong>-4.4%</strong> from 7,598 to 7,267. This isn't a pullback. This is a reckoning.</p>

<h2>SMCI: -28% In One Session. Not a Typo.</h2>

<p>Super Micro Computer didn't just fall — it nuked. <a href="/ticker/SMCI">SMCI</a> crashed <strong>-27.98%</strong> in a single day, pushing its five-day total to <strong>-37%</strong>. Tuesday's $7B capital raise was the spark. Wednesday was the fire. Dilution fears vaporized the AI server narrative. The Street looked at a company that needs $7 billion just to build servers and said: we're out.</p>

<p>The chip massacre went way past SMCI. <a href="/ticker/QCOM">Qualcomm</a> got smoked <strong>-6.92%</strong> — <strong>-21%</strong> in five days. <a href="/ticker/ARM">ARM</a> cratered <strong>-5.37%</strong>, down <strong>-22%</strong> over the same stretch. AVGO -5.12%. AMD -4.86%. MU -4.70%. Even <a href="/ticker/NVDA">Nvidia</a> couldn't escape, dropping -3.73% to $200. The SMH ETF bled -3.40%. Day four of semiconductor Armageddon and nobody's catching the falling knife.</p>

<h2>Oracle: Record Quarter, Stock Implodes</h2>

<p>This one is genuinely unhinged. <a href="/ticker/ORCL">Oracle</a> reported a <strong>record quarter</strong> — $19.18B revenue (+21% YoY), EPS $2.11 beating by 7.6%, cloud revenue up 47% to $9.9B, IaaS screaming +93%. Any other year, this stock rips +5% after hours.</p>

<p>Instead it crashed <strong>-10.1% to $180.88</strong>. Buried in the report: <strong>$70 billion in FY2027 capex</strong> — $10 billion more than expected. They're raising $40B in debt and equity, including a <strong>$20B at-the-market offering</strong>. Wall Street read it as: the AI spending arms race has gone completely insane and shareholders are about to get diluted into oblivion. Record numbers. Stock wrecked. What a timeline.</p>

<h2>Bombs, Oil, and a Gold Panic</h2>

<p>Trump launched <strong>new strikes on Iran</strong> Wednesday, escalating from Tuesday. Oil ripped <strong>+5.06% to $92.66</strong>. Then the really weird thing: gold didn't rally — it <strong>crashed -4.41% to $4,072</strong>, shedding $188 in a single session. Nobody's fleeing to safety. They're selling gold to cover margin calls. Forced deleveraging in the middle of a war panic. Nothing's making sense. That's when you know the plumbing is breaking.</p>

<h2>The Survivors</h2>

<p>Two mega-caps found green. <a href="/ticker/AAPL">Apple</a> inched +0.35% after Morgan Stanley raised its PT post-WWDC. <a href="/ticker/NFLX">Netflix</a> managed +0.72%. That's the list. Everyone else bled: MSFT -1.50%, GOOGL -2.16%, META -2.33%, AMZN -2.53%, TSLA -3.80%. When AAPL and Netflix are your only lifeboats, the ship is already underwater.</p>

<h2>Forward Look: Can SpaceX Save the Week?</h2>

<p>SpaceX locked at <strong>$135/share</strong>, ticker <strong>SPCX</strong>, Nasdaq debut <strong>Friday June 12</strong>. The biggest IPO in history lands in 48 hours. <a href="/ticker/DXYZ">DXYZ</a> front-ran it +3.92%. Strategists warn it'll force massive portfolio repositioning — trillions in market cap landing while everything else burns. Either the catalyst that breaks the selling spiral or the final grenade.</p>

<p>VIX at 22.22. 10-year at 4.542%. Crypto miners obliterated: CLSK -6.7%, MARA -5.18%, RIOT -4.8%. Nobody's safe right now.</p>

<p><strong>VERDICT:</strong> Four straight days of selling. Semiconductors in freefall. Record Oracle quarter that somehow crashed the stock. Iran strikes. Gold getting liquidated for margin calls. This isn't a rotation — it's a deleveraging event. Friday's SpaceX IPO is the next big test. Buckle up.</p>

<p><em>— The Signal</em></p>"""

article = {
    "slug": "closing-bell-june-11-2026",
    "title": "CPI Dropped a 4.2% Bomb — Oracle Crashed 10% After Hours and SMCI Just Got Deleted",
    "subtitle": "Inflation came in at its hottest in three years. Trump bombed Iran again. Oracle reported a record quarter and still imploded. SMCI collapsed 28% in a single session. And SpaceX is 48 hours from landing on Nasdaq.",
    "summary": "CPI hit 4.2% — hottest inflation in 3 years — as Trump escalated Iran strikes. SMCI cratered 28% in a single day. Oracle crashed 10% after-hours despite a record quarter on $70B capex fears. S&P 500 closed at session low (-1.62%). SpaceX IPO locked for Friday at $135.",
    "ticker": "QQQ",
    "sector": "mega-cap",
    "sentiment": "bearish",
    "date": "2026-06-11T04:00:00.000Z",
    "tags": ["CPI", "inflation", "SMCI", "Oracle", "ORCL", "Iran", "semiconductors", "Nasdaq", "SpaceX IPO", "market wrap"],
    "image": {
        "src": "/img/articles/closing-bell-june-11-2026.jpg",
        "caption": "Traders on the floor react as CPI comes in at 4.2% — the hottest inflation reading in three years — sending markets into a tailspin."
    },
    "links": [
        {"label": "Nasdaq 100 (QQQ) →", "url": "https://finance.yahoo.com/quote/QQQ/"},
        {"label": "Super Micro (SMCI) on Yahoo Finance →", "url": "https://finance.yahoo.com/quote/SMCI/"},
        {"label": "Oracle (ORCL) on Yahoo Finance →", "url": "https://finance.yahoo.com/quote/ORCL/"},
        {"label": "CPI Report — BLS →", "url": "https://www.bls.gov/news.release/cpi.nr0.htm"},
        {"label": "SpaceX IPO Coverage →", "url": "https://www.cnbc.com/2026/06/03/spacex-ipo-stock-price-roadshow-musk.html"}
    ],
    "videos": [],
    "bodyHtml": body_html
}

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "articles", "posts")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "closing-bell-june-11-2026.json")

with open(out_path, "w") as f:
    json.dump(article, f, indent=2, ensure_ascii=False)

word_count = len(body_html.split())
print(f"Article written to: {out_path}")
print(f"Word count: {word_count}")
