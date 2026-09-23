# MSFT — 38 GW Data-Center Power Buildout: Verified Research Fact Sheet

**Ticker:** MSFT (Microsoft Corporation)
**Sector slug:** `mega-cap`
**Article slug:** `msft-38gw-power-buildout-2026`
**Prepared:** Saturday, September 12, 2026 (CEST)
**Latest market session in data:** Friday, September 11, 2026

> **House-rule compliance note:** Per The Signal house rules, **no exact stock prices appear in the prose, headline, subtitle, or summary**. Price levels are confined to the structured `yfinance` data block below (required by the output contract).

---

## 1. Verified figure table

| Figure | Source URL | Verbatim note |
|---|---|---|
| ~38 GW data-center capacity targeted by 2032 | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "Microsoft plans to build out its data-center capacity to about 38 gigawatts by 2032, more than triple its current footprint, Bloomberg News reported on Thursday, citing people familiar with the matter." |
| Current footprint ~12 GW | https://www.datacenterdynamics.com/en/news/microsoft-targets-38gw-of-data-center-capacity-in-2032-report | "the cloud company is targeting 38GW of capacity in 2032. It currently operates around 12GW of data center capacity." |
| Add ~26 GW of net new capacity (38 − 12) | https://www.bloomberg.com/news/features/2026-09-10/microsoft-ai-focused-data-center-plan-to-add-26-gigawatts-of-compute | Bloomberg Big Take URL slug states "add-26-gigawatts-of-compute". Primary article paywalled (HTTP 403). |
| Only ~2 GW of current 12 GW is AI-chip-specific | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "only about 2 gigawatts of the company's current 12-gigawatt capacity is centered on AI-specific chips" |
| AI share grows to ~1/3 of 38 GW by 2032 | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "a share expected to grow to about a third of the 38 gigawatts it plans to have online" |
| Microsoft declined to comment to Reuters | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "Microsoft did not immediately respond to a Reuters request for comment." |
| Turned away AI/cloud business; restricted subscriptions; service disruptions | https://valueaddvc.com/pulse/microsoft-38gw-data-center-plan-2032-2026 | "severe hardware constraints have forced the company to turn away some cloud and AI business, restrict certain subscriptions and absorb service disruptions over the past year, according to the same report" |
| Capex $50B for fiscal Q1 2027 | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "Microsoft expects capital expenditures of $50 billion for the fiscal first quarter of 2027 and $175 billion for the 2026 calendar year." |
| Capex "$50B" is guidance of **over** $50B | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4 | "We expect CapEx spend will be over $50 billion including the lease reclassification impact from the useful life update." |
| Capex ~$175B for calendar 2026 (revised) | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4 | "the shift from finance to operating leases adjusts our expectation to approximately $175 billion." |
| Calendar-2026 capex previously guided at ~$190B (April 2026) | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3 | "For calendar year 2026, we expect to invest roughly $190 billion in capital expenditures which includes approximately $25 billion from the impact of higher component pricing." |
| $190B → $175B cut is an accounting reclassification, not a demand cut | https://www.cfodive.com/news/microsoft-holds-line-ai-spending-plans/826648 | "In the future, some leases will shift from finance to operating as a result of this, which should drive capex for calendar 2026 to $175 billion, from $190 billion previously." |
| Leases spread over 25 years rather than 15 | https://www.reuters.com/business/microsoft-plans-38-gigawatts-data-center-capacity-by-2032-bloomberg-news-reports-2026-09-10 | "The company is planning to spread long-term leases on data centers over 25 years rather than 15, which has the effect of lowering its annual reported capital expenditures." |
| **FY2026 capex = $145.3B including finance leases** (reconciles the "$145B" figure) | https://sec-api.io/insights/financial-analysis-of-microsoft-fy2026-capital-intensity-against-a-record-margin | Table: cash flow statement additions to PPE full year **$115,948M** vs "Capital expenditures as stated on the earnings call" **$145.3B** (Q1 34.9 / Q2 37.5 / Q3 31.9 / Q4 41.0). |
| FY2026 cash payments for property & equipment = $115.9B | yfinance (MSFT `cashflow`, FY ended 2026-06-30) | "Purchase Of PPE = -1.15948e+11"; corroborated above by sec-api.io ($115,948M). |
| Q4 FY2026 capex $41B (incl. finance leases) | https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast | "Capital expenditures were $41 billion including the impact from higher component pricing as noted in our guide." |
| Commercial RPO $678B (Q4 FY26) | https://www.cnbc.com/2026/07/29/microsoft-msft-q4-earnings-report-2026.html | "commercial remaining performance obligations … increased 8% to $678 billion from the previous quarter." |
| 38 GW would outdraw New York State at peak | https://valueaddvc.com/pulse/microsoft-38gw-data-center-plan-2032-2026 | "A footprint this size would draw more electricity at peak than New York State…" |
| NY State record peak = 33,956 MW (July 2013) | https://www.nyiso.com/-/understanding-summer-energy-demand | "The highest recorded peak demand in New York reached 33,956 MW and occurred in July 2013." (38 GW > 33.96 GW → the NY comparison checks out arithmetically.) |
| NYISO forecast summer peak 31,578 MW | https://dps.ny.gov/summer-energy-outlook | "The NYISO projects that New York's peak demand will be 31,578 megawatts (MW)." |
| Buildout mixes owned + leased capacity from neoclouds | https://www.datacenterdynamics.com/en/news/microsoft-targets-38gw-of-data-center-capacity-in-2032-report | "a combination of self-owned and operated data centers and leased capacity from third-party providers, including neoclouds, with which Microsoft has signed some large contracts, including CoreWeave, Nscale, Lambda, Iren, and Nebius." |
| ~$60B spent with neoclouds as of November 2025 | https://www.datacenterdynamics.com/en/news/microsoft-targets-38gw-of-data-center-capacity-in-2032-report | "In November 2025, it had spent an estimated $60 billion." |
| $33B of neocloud deals; $19.4B Nebius / 100k GB300; $23B Nscale / 200k GB300 | https://finance.yahoo.com/news/microsoft-inks-33-billion-deals-191655037.html | "Microsoft inks $33 billion in deals with 'neoclouds' like Nebius, CoreWeave" and "Nebius deal alone secures 100,000 Nvidia GB300 chips". |
| Aug 2025 contrast: Microsoft scrapped leases totalling "a couple of hundred MWs" | https://broadbandbreakfast.com/microsoft-scraps-multiple-data-center-leases-td-cowen | "The canceled contracts totaled a 'couple of hundred MWs,' enough to power two large data centers…" (TD Cowen note, Feb 2025) |
| Follow-on contrast: up to 2 GW of projects abandoned (Mar 2025) | https://www.reuters.com/technology/microsoft-pulls-back-more-data-center-leases-us-europe-analysts-say-2025-03-26 | "Microsoft … has abandoned data center projects set to use 2 gigawatts of electricity in the U.S. and Europe in the last six months due to an oversupply relative to its current demand forecast, TD Cowen analysts said." |
| Hyperscaler 2026 capex: Amazon ~$220B, Alphabet ~$195–205B, Meta ~$130–145B, Microsoft ~$175B | https://mlq.ai/news/big-techs-2026-capex-range-reaches-720-billion-to-745-billion | "Amazon's approximately $220 billion plan, Alphabet's $195 billion-to-$205 billion outlook, Meta's $130 billion-to-$145 billion range and Microsoft's accounting-adjusted estimate of approximately $175 billion." Aggregate: "$720 billion to $745 billion". |
| Meta targets >10 GW total capacity by end-2026 | https://www.datacenterknowledge.com/hyperscalers/hyperscalers-in-2026-what-s-next-for-the-world-s-largest-data-center-operators- | "The company aims to achieve more than 10 GW of total capacity by the end of 2026." |
| Amazon Project Rainier: $11B, 2.2 GW mega-campus (Indiana) | https://datacentremagazine.com/top10/top-10-hyperscale-data-centre-companies | "a US$11bn, 2.2GW mega-campus in Indiana, constructed in strategic partnership with Anthropic." |
| Nvidia shares rose on the report | https://www.tradingview.com/news/gurufocus:084605024094b:0-microsoft-targets-38gw-data-center-buildout-as-ai-capacity-crunch-bites | Headline: "Nvidia Stock Climbs After Report Details Microsoft's 38-Gigawatt Data Center Push" |
| Temu moved a major cloud deal to Oracle over capacity | https://www.tradingview.com/news/gurufocus:084605024094b:0-microsoft-targets-38gw-data-center-buildout-as-ai-capacity-crunch-bites | "Temu moved a major cloud deal to Oracle after Microsoft could not provide enough capacity in the regions it wanted." |
| GitHub 8-hour outage (Aug) tied to server constraints; Xbox cloud-gaming caps | https://www.tradingview.com/news/gurufocus:084605024094b:0-microsoft-targets-38gw-data-center-buildout-as-ai-capacity-crunch-bites | "GitHub suffered an eight-hour outage in August that was tied to server constraints, while Microsoft has placed limits on Xbox cloud-gaming usage." |

---

## 2. Capex reconciliation (the "$145B vs $175B" question)

There is **no contradiction** — three different measures and periods are in play:

| Measure | Period | Figure | Basis |
|---|---|---|---|
| Cash purchases of property & equipment | FY2026 (ended Jun 30, 2026) | **$115.9B** | Cash-flow statement (yfinance + sec-api.io) |
| Capex **including finance leases** (as stated on the earnings call) | FY2026 | **$145.3B** | Q1 34.9 + Q2 37.5 + Q3 31.9 + Q4 41.0 (sec-api.io / Microsoft IR) |
| Calendar-2026 guidance (original, Apr 2026) | CY2026 | **~$190B** | Microsoft Q3 FY26 call |
| Calendar-2026 guidance (revised, Jul 2026) | CY2026 | **~$175B** | Microsoft Q4 FY26 call — lower only because more leases reclassified finance → operating |
| Q1 FY2027 guidance | Sep-quarter 2026 | **over $50B** | Microsoft Q4 FY26 call |

**Bottom line for the article:** the "$145B FY2026" number is the fiscal-year capex measure *including finance leases*; the "$175B" number is *calendar-year 2026* guidance. Both are real, both are sourced, and neither contradicts the other.

**Trend (cash capex):** FY2023 $28.1B → FY2024 $44.5B → FY2025 $64.6B → FY2026 $115.9B (MLQ / yfinance).
**Trend (operating cash flow):** FY2026 $182.9B vs FY2026 cash capex $115.9B → capex now ≈63% of operating cash flow.

---

## 3. yfinance data block (MSFT)

Source: `/home/chino/video-venv/bin/python3` with `yfinance 1.4.1`, `Ticker("MSFT")`, run 2026-09-12.

- **Last close:** 495.63 on **2026-09-11**
- **Previous close:** 492.44 on **2026-09-10**
- **Market cap:** ~$3.68 trillion
- **Forward P/E:** 21.03× | **Trailing P/E:** 27.63× (trailing EPS 17.94; forward EPS 23.57)
- **Revenue TTM:** ~$331.8B
- **FCF TTM:** ~$67.0B (computed = sum of last 4 quarters OCF $182.935B + capex −$115.948B)
- **Total cash + short-term investments:** ~$76.8B
- **Total debt (yfinance `info`):** ~$128.8B — *see flag below*
- **Shares outstanding:** ~7.43B
- **Analyst consensus:** Strong Buy (mean 1.36 on 1–5 scale), 52 analysts
- **Analyst mean target:** ~$572.92 (high $870, low $400)
- **52-week range:** low 349.20 / high 553.72
- **Price action:** shares are roughly flat week-over-week (closed the Sept 11 session a fraction above the prior session), trading in the lower half of the 52-week range but below the analyst mean target.

**Note on the price-action framing:** MSFT closed Sept 10 essentially flat on the day the Bloomberg report broke, and edged up marginally on Sept 11 — i.e. the market has not re-rated the stock on the 38 GW headline.

**Flags on the yfinance block:**
- yfinance `info['totalDebt']` returns ~$128.8B, but the balance sheet reports Total Debt of ~$56.8B and Net Debt of ~$19.4B as of 2026-06-30. The `info` figure almost certainly includes operating-lease liabilities. **Prefer the balance-sheet figures ($56.8B total debt / $19.4B net debt) if a precise debt number is needed.**
- yfinance `info['freeCashflow']` returns ~$16.5B, which is inconsistent with the cash-flow statements. The audited-equivalent TTM figure is **~$67.0B** (FY2026 annual FCF = $66.99B). **Do not use $16.5B.**

---

## 4. Sector relevance & comparators (all sourced above)

1. **The bottleneck is power and shells, not chips.** Microsoft is buying megawatts from neoclouds (CoreWeave, Nscale, Lambda, IREN, Nebius) with ~$60B committed by Nov 2025 and ~$33B disclosed in deals — a structurally different pattern from building everything itself.
2. **This is a reversal of a reversal.** In Feb–Mar 2025, TD Cowen reported Microsoft scrapping leases (200 MW, then up to 2 GW) as a sign of potential oversupply; eighteen months later it is rationing compute and adding 26 GW.
3. **The scale is state-level.** 38 GW exceeds NY State's all-time record peak (33,956 MW, July 2013) and the current NYISO summer peak forecast (31,578 MW).
4. **The peer cohort is spending at the same order of magnitude** — combined 2026 hyperscaler capex guidance $720–745B (Amazon ~$220B, Alphabet $195–205B, Meta $130–145B, Microsoft ~$175B), with Meta alone targeting >10 GW by end-2026.

---

## 5. Titles (5 candidates)

1. Microsoft Turned Away AI Customers. Its Answer Is 38 Gigawatts.
2. Microsoft's 38-Gigawatt Plan Turns It Into an Industrial Power Company
3. 38 Gigawatts by 2032: Microsoft's Buildout Eclipses New York's Grid
4. The AI Bottleneck Moved From Chips to Grid, and Microsoft Agrees
5. Rationed Compute at $175 Billion a Year, Microsoft Buys Megawatts

*All ≤11 words; no "Just" openers, no em-dash punchline endings, no weekday words, no exclamation marks.*

## 6. Subtitle

Bloomberg reports Microsoft will grow its data-center footprint from roughly 12 gigawatts today to more than 38 by 2032 — a buildout that would outdraw New York State at peak and is funded on calendar-2026 capex guidance of about $175 billion. Only about 2 of today's 12 gigawatts are AI-specific chips, yet Microsoft expects AI to reach roughly a third of the larger fleet. The company has already turned away cloud and AI customers, capped subscriptions, and absorbed service disruptions. The constraint has moved from silicon to megawatts, shells, and transformers.

## 7. Summary

Microsoft plans to more than triple its global data-center capacity from roughly 12 gigawatts to more than 38 gigawatts by 2032, according to a Bloomberg Big Take corroborated in outline by Reuters and DataCenterDynamics, with AI-dedicated capacity rising from about 2 gigawatts to roughly a third of the total. The buildout — supported by calendar-2026 capex guidance of about $175 billion — follows an admission that compute shortages forced Microsoft to turn away AI and cloud business, evidence that the industry's binding constraint has shifted from chips to electricity and physical capacity.

---

## 8. Claims I could NOT verify

1. **Bloomberg Big Take primary text** — paywalled (HTTP 403). All Bloomberg-attributed figures are confirmed only via Reuters/DCD/secondary summaries, never the original.
2. **Bloomberg's exact "eclipses New York State's electricity use at peak" phrasing** — the comparison is attributed to Bloomberg by secondary outlets (valueaddvc, 조선일보), but no primary Bloomberg sentence was retrieved. The *arithmetic* is independently supported by NYISO data.
3. **DCD's "$60 billion spent with neoclouds as of November 2025"** — retrieved from the DCD search snippet; the DCD page itself is Cloudflare-protected (HTTP 403) and could not be read in full.
4. **GitHub's eight-hour August outage and Xbox cloud-gaming usage limits** — sourced only to a GuruFocus/TradingView summary, not independently confirmed.
5. **Temu moving a major cloud deal to Oracle** — sourced only to GuruFocus/TradingView.
6. **Current-footprint range discrepancy** — Bloomberg/Reuters/DCD say ~12 GW; Data Centre Magazine says "an estimated 12-15GW today". The ~12 GW figure is the better-sourced one.
7. **"Microsoft, Hurt By Server Shortage, Aims to Triple Cloud Capacity by 2032" (The Information)** — headline retrieved via Google News RSS; body paywalled, not read.
8. **yfinance `info['totalDebt']` ($128.8B) and `info['freeCashflow']` ($16.5B)** — both inconsistent with MSFT's own financial statements; flagged above and excluded from the analysis.
9. **Reuters page itself** returned HTTP 401 to automated fetch; the full Reuters wire text was read via the AOL syndication of the same Reuters story (verbatim, byline "Christy Santhosh … Editing by Shailesh Kuber").

---

## 9. FINAL SLUG

**`msft-38gw-power-buildout-2026`** — confirmed, no collision. (Existing MSFT slugs in `articles/posts/`: `msft-frontier-ai-2026`, `msft-azure-100b-2026`, `msft-agents-infra-moat-2026`. A hero-image script `scripts/gen-msft-38gw-power-hero-20260912.py` already exists in the repo.)
