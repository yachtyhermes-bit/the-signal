# LRCX FACT SHEET — Fiscal Q1 2027 (Sept 2026 quarter), print after close Wed Oct 21, 2026
Compiled 12:0x pm ET, Oct 21, 2026. Prices: yfinance, auto_adjust=False. ALL figures verified below unless marked ⚠️.

---

## 1. Price / performance
- **Last completed close: $263.45 (Tue Oct 20, 2026)** — https://finance.yahoo.com/quote/LRCX/history
- Intraday now (12:03 pm ET, session in progress): **$266.56, +1.18%**; day range $264.00–$270.90 — yfinance `info.regularMarketPrice` (same API, timestamp 2026-10-21 18:03 CEST / 12:03 ET)
- **1-week (5 sessions, Oct 14 close $286.92 → Oct 20): −8.18%**
- **1-week (6 sessions, Oct 13 close $301.11 → Oct 20): −12.51%** ← the "~12% in a week" framing
- Week ended Fri Oct 16 (the SOX streak week): Oct 9 close $318.84 → $263.94 = **−17.22%** (Benzinga independently prints −17.2% for last week — https://www.benzinga.com/markets/tech/26/10/62436201/chip-stocks-bounce-longest-losing-streak-since-2008)
- **YTD: +53.9%** (Dec 31, 2025 close $171.18 → $263.45). Corroborated by Seeking Alpha headline "Lam Research nears Q1 earnings with 53% YTD rally," Oct 20 — https://seekingalpha.com/news/... (headline only; body paywalled)
- **52-week range: $135.50 – $438.50** (low Nov 20, 2025; high intraday Jun 30, 2026) — yfinance `info.fiftyTwoWeekLow/High`; 1y OHLC confirms same extremes
- Down **−39.9% from the 52-week high** (263.45/438.50−1)

## 2. Size / valuation / TTM
- **Market cap $333.8B** (266.755 × 1.2514B shares) — yfinance `info.marketCap` = $333,823,705,088
- **Shares out 1,251.4M** — yfinance `info.sharesOutstanding`. Primary: "1,251,321 thousand outstanding shares" as of Aug 4, 2026 — https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm (10-K cover)
- **Forward P/E — BASIS MATTERS:**
  - **28.2x on FY2027 consensus EPS $9.49** (= 266.755/9.48746). Cross-check: StockAnalysis prints forward PE **28.20** — https://stockanalysis.com/stocks/lrcx/statistics/
  - **22.7x on FY2028 consensus EPS $11.77** ← this is what yfinance `info.forwardPE` = 22.672 actually reports (266.755/11.76569). ⚠️ Do not use 22.7x as "next-12-month" without stating it's FY2028.
  - Trailing P/E **45.8x** on FY2026 actual GAAP EPS $5.82 (StockAnalysis: 46.45)
- **TTM revenue $23,232.7M** — sum of last 4 reported quarters: 6,722.238 (Jun-26) + 5,841.488 (Mar-26) + 5,344.791 (Dec-25) + 5,324.173 (Sep-25). Equals 10-K FY2026 revenue of $23,232,690K — https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm
  - ⚠️ yfinance `info.totalRevenue` = $23,232,690,176 — coincidentally correct here, but I used the quarterly sum, not the field.

## 3. Guidance (Sept 2026 qtr) and June 2026 actuals
**Guided Sept quarter, given Jul 29, 2026 (non-GAAP unless noted):**
- **Revenue $8.10B ± $400M** (range $7.70B–$8.50B)
- **Non-GAAP gross margin 52.0% ± 1pt** (GAAP same, ±$2.7M amortization)
- **Non-GAAP operating margin 39.5% ± 1pt**
- **Non-GAAP diluted EPS $2.15 ± $0.15** (range $2.00–$2.30)
- Diluted share count 1.255B
Source: https://investor.lamresearch.com/2026-07-29-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-June-28,-2026
(Implied: **+20.5% QoQ**, **+52.1% YoY**, and a new all-time quarterly revenue record; EPS +70.6% YoY.)

**June 2026 quarter (fiscal Q4 2026) actuals:**
| Metric | GAAP | Non-GAAP |
|---|---|---|
| Revenue | $6,722.2M (+15.1% QoQ, +30.0% YoY) | $6,722.2M |
| Gross margin | 51.7% ($3,478.7M) | **52.0%** ($3,500M) |
| Operating margin | 37.4% ($2,513.5M) | **38.4%** |
| Diluted EPS | $1.81 | **$1.82** (vs $1.68–1.69 consensus, +8.1% beat) |
Source: same press release above. FY2026 totals: revenue $23.2B, GM 50.5% GAAP / 50.6% non-GAAP, EPS $5.82 (record) — 10-K + Q4 call transcript https://stockanalysis.com/stocks/lrcx/transcripts/653168-q4-2026/

## 4. Consensus for tonight
- **EPS $2.18; revenue $8.14B — MarketBeat** (consensus EPS $2.18, expected revenue $8.14B) — https://www.marketbeat.com/earnings/reports/2026-10-21-lam-research-co-stock/
- **EPS $2.17; revenue $8.12B — Zacks** (via Yahoo Finance preview) — https://finance.yahoo.com/markets/stocks/articles/lam-research-lrcx-q1-earnings-121517064.html
- **EPS $2.1795 (25 analysts); revenue $8.142B (24 analysts) — yfinance/`earnings_estimate`+`revenue_estimate`**
- **EPS ~$2.18; revenue $8.14B — TipRanks** — https://www.tipranks.com/news/lam-research-stock-jumps-ahead-of-this-weeks-earnings-heres-why
- Read-through: consensus revenue sits **+0.5% above the guide midpoint** and EPS **+1.4% above** — i.e. the Street already assumes a beat. FY2027 consensus EPS $9.49, revenue $34.95B; **next-quarter (Dec-26) consensus revenue $8.538B — only +5.4% QoQ vs +20.5% guided for Sept** (yfinance estimates).

## 5. Analyst consensus
- **yfinance: recommendationMean 1.457 → "strong_buy"; 31 analysts; mean PT $374.61; median $380; high $500; low $290** (`info` fields). Note the mean PT is ~40% above the current price while the *low* target ($290) is also above it — the distribution is stale relative to the selloff.
- **Cross-check 1 — MarketBeat: "Moderate Buy," average PT $364.59** (1 Strong Buy / 26 Buy / 5 Hold) — https://www.marketbeat.com/instant-alerts/upcoming-lam-research-lrcx-expected-to-post-earnings-on-wednesday-2026-10-14/
- **Cross-check 2 — FactSet (via MT Newswires, Oct 20): average rating "buy," mean PT $384.93** — https://finance.yahoo.com/markets/stocks/articles/evercore-isi-adjusts-price-target-093504323.html
- **Cross-check 3 — TipRanks: "Strong Buy," avg PT $399.86** (21 Buy / 3 Hold over 3 months) — tipranks URL above
⚠️ PT dispersion is wide ($364.59 → $399.86 across aggregators) because several targets predate the October drawdown. Cite the range, not a single number.
- Direction of travel is down: Evercore ISI $355→$315 (Oct 20), Mizuho $370→$365 (Aug 25), Wells Fargo $450→$350 (Jul 30). Up: Morgan Stanley $367→$385 (Oct 5), B. Riley $350→$390 (Oct 1), Deutsche Bank $320→$375 (Oct 19–20) — yfinance `upgrades_downgrades`.

## 6. Segment mix (June 2026 quarter — last reported)
- **Systems revenue $4,249.8M (63.2%); Customer support-related & other $2,472.4M (36.8%)** — press release, "revenue disaggregated between systems and customer support-related revenue" (investor.lamresearch.com URL above). CSBG was a record, +17% QoQ.
- **By end-market (% of systems revenue): Memory 46%** (from 39% in March); within that **NAND/non-volatile 23%** (from 12%) and **DRAM 23%**; **Foundry 44%** (from 54%); logic/IDM the balance (~10%) — Doug Bettinger, Q4 FY26 call: https://stockanalysis.com/stocks/lrcx/transcripts/653168-q4-2026/
- **China 26% of total revenue** (down from 34% in the March quarter); Taiwan 27% (record), Korea 20%, Japan 9%, US 9%, SE Asia 5%, Europe 4% — press release geographic table + call
- FY2026 full-year mix (10-K): China 34%, Taiwan 22%, Korea 19%, Japan 9%, US 7%, SEA 6%, Europe 3%; Foundry 54%, Memory 39%, Logic 7%
- 10-K FY26: Systems $14,885.5M, CSBG $8,347.2M — https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm

## 7. WFE outlook
- **CY2026 WFE: "low $150 billion range, up from our prior outlook of $140 billion with upside bias"** — Tim Archer, Q4 FY26 call, Jul 29, 2026 (transcript URL above)
- **2027, verbatim:** *"Looking into 2027, we see an extraordinary setup for WFE growth. AI is driving record revenue and profitability for our customers, who have signaled unprecedented long-term demand visibility."* — same transcript
- Doug Bettinger, same call: *"we believe 2027 looks like a great setup, not only for the industry, but for Lam… next year we still see DRAM being the fastest grower, foundry logic being the second fastest grower, and NAND being third."*
- Archer on 2027 quantification: *"we're not going to get into talking specifically about next year, at least not numerically… the industry is still meaningfully undersupplied."* (**no numeric 2027 WFE guide exists — do not attribute one to Lam**)
- Lam SAM: **"~36%, 36.5% this year"** of WFE, vs "high 30s" target (Bettinger, same call)
- Third-party 2027 number (label as such): **Cantor Fitzgerald's C.J. Muse models 2027 WFE at $215B, +39%, with $225B possible** — https://www.benzinga.com/markets/tech/26/10/62436201/chip-stocks-bounce-longest-losing-streak-since-2008

## 8. Non-GAAP gross margin trend (last 4 quarters)
| Quarter | Non-GAAP GM | QoQ |
|---|---|---|
| Sep 2025 (Q1 FY26) | **50.6%** | — |
| Dec 2025 (Q2 FY26) | **49.7%** | −90 bps |
| Mar 2026 (Q3 FY26) | **49.9%** | +20 bps |
| Jun 2026 (Q4 FY26) | **52.0%** | +210 bps (highest in 20 years, per CFO) |
| Sep 2026 (Q1 FY27) | **52.0% ±1 guided** | — |
Sources: Sep/Dec from https://www.sec.gov/Archives/edgar/data/707549/000070754926000006/lrcx_exhibitx991xq2x2026.htm ; Mar/Jun from the Jul 29 release. Trend is up but non-monotonic — the 52% is a 2-quarter-old high, not a fresh acceleration.

## 9. Bear case, with numbers
- **China = 34% of FY2026 revenue** (34% FY25, 42% FY24); 26% in the June quarter; ~37% of revenue in the first nine months of FY2026 — 10-K: https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm
- **Export controls explicitly favor non-U.S. rivals**, per the 10-K's own competition section: controls "provid[e] an advantage to our international competitors that are not subject to these restrictions," and Lam competes with "companies that exist in a more favorable legal or regulatory environment… able to sell products for certain applications at certain customers that we are prohibited from selling to."
- **Customer concentration: 4 customers = 55% of FY2026 revenue** (16% / 15% / 12% / 12%). Named key customers: Micron, Samsung, SK hynix, TSMC — 10-K Note 9 / Item 1
- **Memory cyclicality:** 46% of June-quarter systems revenue was memory, and NAND revenue **doubled sequentially** (23% of systems revenue vs 12%). A doubled base is the hardest comp in the model. On the Q4 call an analyst cited **TrendForce forecasting 2027 NAND oversupply** (Archer declined to engage on 2028).
- **Named bear datapoint — Evercore ISI's Mark Lipacis, Oct 20, 2026:** cut PT to **$315 from $355** (kept Outperform), arguing Lam is set for a beat-and-raise but that **"late-cycle dynamics could result in P/E multiple compression,"** and he would **"wait to add."** — https://www.tipranks.com/news/the-fly/lam-research-price-target-lowered-to-315-from-355-at-evercore-isi-thefly-news
- **Cash conversion / working capital:** June-quarter operating cash flow **$1.457B vs net income $2.277B = 64% conversion**; receivables **+29.2% QoQ to $5.340B** vs revenue +15.1% — press release balance sheet & cash-flow tables; flagged by https://www.gurufocus.com/news/9132193/lam-research-stocks-fall-32-as-evercore-cuts-target-before-earnings
- **Sequential deceleration is the mechanical bear case:** +20.5% QoQ guided for Sept vs **+5.4% QoQ implied by Dec-quarter consensus** ($8.538B). If December guidance lands at "only" +5%, the "peak sequential growth" argument gets its first hard evidence.
- **Valuation:** 45.8x trailing, 28.2x FY27, with the stock still +53.9% YTD and only −40% off a 52-week high of $438.50 — the multiple, not the growth, is what repriced in October.

## 10. Earnings date/time (primary)
- **Wednesday, October 21, 2026; call 2:00 pm PT / 5:00 pm ET**; release after market close; webcast replay ~3 hours after — company release dated Sep 30, 2026: https://investor.lamresearch.com/2026-09-30-Lam-Research-Corporation-Announces-September-Quarter-Financial-Conference-Call (and https://www.stocktitan.net/news/LRCX/lam-research-corporation-announces-september-quarter-financial-y2q96a8bfuhr.html)
- yfinance `earningsTimestamp` = 2026-10-21 20:00 UTC (16:00 ET) — that is a data-provider default for "after close," **not** a company-stated release time. Use "after the close" + "call at 5:00 pm ET."

## 11. Sector context — claim verified (with a caveat)
- **VERIFIED, but it already ended.** The Philadelphia Semiconductor Index fell **eight consecutive sessions, Oct 7–16, 2026, −15.7%**, closing at **11,137.29** on Fri Oct 16 — its **longest losing streak since October 2008 ("18 years")**. Benzinga: *"On Oct. 10, 2008, the PHLX Semiconductor Index closed lower for an eighth straight session… It took 18 years for the index to repeat that streak."* — https://www.benzinga.com/markets/tech/26/10/62436201/chip-stocks-bounce-longest-losing-streak-since-2008
  - Independent confirmation: Investing.com/Yahoo — "longest losing streak since 2008… fell 3.83% to 11,137.29, extending its decline to eight consecutive sessions… lost 16% since its last advance on October 6" — https://finance.yahoo.com/technology/ai/articles/chip-index-sox-posts-longest-123436535.html
  - Inc./Phil Rosen, Oct 20: "SOX rose 1.6% to start the week, snapping an eight-session losing streak and its longest string of declines since October 2008… Since 1994, the SOX has fallen eight days in a row or more just eight times." — https://www.inc.com/phil-rosen/stock-market-chip-stocks-nasdaq-100-etfs-investors/91422573
  - **Caveat for the article: the streak snapped Monday Oct 19 (+1.6%).** Index has since rallied: Oct 19 11,316.34, Oct 20 11,283.81, **Oct 21 intraday 11,502.15 (+1.93%) at 12:03 pm ET** (yfinance ^SOX). Writing "eight straight down days" in present tense tonight would be wrong.
  - ⚠️ Not verified from the index owner (Nasdaq/S&P); the "18 years / since Oct 2008" characterisation rests on multiple independent financial-media reports, which agree with each other and with the OHLC data.
- LRCX over that same stretch: **−17.2% for the week ended Oct 16**; **−12.5% over the six sessions to Oct 20**; worst-hit in the group alongside AMAT (−19.3%), KLAC (−15.3%), TER (−19.3%) that week (Benzinga table).
- **Today intraday: $266.56, +1.18% at 12:03 pm ET** (range $264.00–$270.90). MarketBeat printed $267.30, **+1.46% as of 11:07 am ET**. Stock is bouncing into the print, not sliding.

## 12. Competitive position
- **Dry etch: Lam 41.1% share** of a **$21.9B** 2025 market; Tokyo Electron 23.4%; Applied Materials 17.4% — CSET count of TechInsights data, via https://chipsupplychain.org/deposition-and-etch/
- **Conductor etch: Lam 51.2%**; **dielectric etch: TEL 55.9%** (Lam's weak spot); **PVD: AMAT 82.4%**; **CVD: AMAT 47%**; **ALD: ASM International 54.5%** of a $4.1B market — same source
- **Deposition market $26.2B (2025)**, dry etch $21.9B. AMAT and Lam are the two largest deposition/etch suppliers; no single firm dominates the way ASML does in litho — same source
- Top-5 WFE suppliers in 2025 by revenue: ASML $27.5B, then Applied Materials, Lam, Tokyo Electron, KLA — https://www.techinsights.com/blog/top-ic-manufacturing-equipment-suppliers-2025
- Lam's own framing is about **SAM**, not share: **~36–36.5% of WFE** in CY2026 vs a "high 30s" target (see §7). Conductor-etch installed base "more than 40,000 chambers" (Archer, Q4 call).
- ⚠️ I did not find a Tier-1 (Gartner/TechInsights) primary table for *total* deposition share for Lam; the per-tool numbers above are the best sourced figures available.

---

## STRONGEST BEAR CASE
Lam is being repriced for a cycle turn it cannot yet see, and October's −17% week was the market voting on the *shape* of 2027 rather than the size of the September quarter. The numbers behind that: memory was 46% of June-quarter systems revenue and NAND revenue literally doubled sequentially (12% → 23% of systems revenue), so the September guide of $8.1B is being lapped off the easiest comp in the model — and consensus already has sequential growth collapsing from **+20.5% QoQ in September to +5.4% QoQ in December** ($8.538B). China is still **34% of fiscal 2026 revenue** (26% in the June quarter, and the domestic-Chinese portion is the piece that fell), and Lam's own 10-K concedes that U.S. export controls hand "an advantage to our international competitors that are not subject to these restrictions." Four customers are **55% of revenue** (16/15/12/12) — Micron, Samsung, SK hynix, TSMC — which means one memory capex pause is a guidance event, not a mix shift. And the quality-of-earnings tell is real: June-quarter operating cash flow was **$1.457B against $2.277B of net income — 64% conversion — with receivables up 29.2% QoQ against 15.1% revenue growth.** Evercore's Mark Lipacis cut his target to $315 from $355 on October 20 while keeping Outperform, on exactly this logic: a beat-and-raise is likely, but "late-cycle dynamics could result in P/E multiple compression," and he would "wait to add." At 45.8x trailing and 28.2x FY2027 — with the stock still +54% YTD — the multiple, not the order book, is what has room to fall.

---

## SOURCES (for links[])
1. https://investor.lamresearch.com/2026-07-29-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-June-28,-2026
2. https://investor.lamresearch.com/2026-09-30-Lam-Research-Corporation-Announces-September-Quarter-Financial-Conference-Call
3. https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm
4. https://stockanalysis.com/stocks/lrcx/transcripts/653168-q4-2026/
5. https://www.benzinga.com/markets/tech/26/10/62436201/chip-stocks-bounce-longest-losing-streak-since-2008
6. https://www.inc.com/phil-rosen/stock-market-chip-stocks-nasdaq-100-etfs-investors/91422573
7. https://www.tipranks.com/news/the-fly/lam-research-price-target-lowered-to-315-from-355-at-evercore-isi-thefly-news
8. https://www.marketbeat.com/earnings/reports/2026-10-21-lam-research-co-stock/
9. https://chipsupplychain.org/deposition-and-etch/
10. https://stockanalysis.com/stocks/lrcx/statistics/

---

**PROPOSED SLUG: lrcx-september-quarter-memory-capex-2026**
Uniqueness: **verified free.** `https://readthesignal.net/article/lrcx-september-quarter-memory-capex-2026/` returns 404 (control: an existing article URL returns 200), and the sitemap's only LRCX page is `/article/lrcx-ai-memory-3d-stacking-moat-2026/` — no collision.

## FLAGGED / NOT VERIFIED
- Exact release time (e.g. 4:00 pm ET) — company PR only says call at 5:00 pm ET, "after market close."
- A numeric 2027 WFE forecast from Lam — **none exists**; only qualitative "extraordinary setup." Cantor's $215B is third-party.
- A formal rating *downgrade* on LRCX in October — none found; the bear tape is PT cuts + maintained ratings.
- Lam's total deposition market share from a Tier-1 primary table.
- "18 years" from the index owner (Nasdaq) — supported by three independent media sources plus index OHLC, which agree.
- YTD +53.9% corroborated only by a paywalled Seeking Alpha headline ("53% YTD rally"); the arithmetic from yfinance closes is exact.
