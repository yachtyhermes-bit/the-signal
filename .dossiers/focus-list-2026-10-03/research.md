# FOCUS LIST — RESEARCH DOSSIER — 2026-10-03

**Prepared:** Saturday 3 October 2026, ~19:30 CEST · **Analyst:** research subagent for The Signal (readthesignal.net)
**Edition scope:** four Focus List names — **CEG (Constellation Energy)**, **SOFI (SoFi Technologies)**, **NFLX (Netflix)**, **AMZN (Amazon.com)**.
**Price basis:** last completed US close **Friday 2 October 2026** (3 Oct is a Saturday). Market data pulled this session from `yfinance` 1.4.1 on `/home/chino/video-venv/bin/python3` (`history(auto_adjust=False)`, `info`, `quarterly_income_stmt`, `quarterly_cashflow`). Company figures taken from the companies' own releases / IR exhibits / filed statements where available; each is labelled with its source.
**Style rule to be honoured by the Writer:** the narrative copy must contain **no exact share prices, no price targets of our own, and no advice framing**. Exact closes are recorded below **only as raw data blocks**, each with its date, so the Writer can convert them to relative statements (% move, % of 52-week range, % from high) without re-deriving them.
**Verification:** every source URL was probed this session with `curl -s -o /dev/null -w '%{http_code}'` and a browser user-agent; results are listed in §6. `200/401/403/429` were treated as resolving; any figure that could not be tied to a primary document is marked **UNVERIFIED**.

---

## 0. TOP-LINE FLAGS FOR THE EDITOR (read first)

**No name on this list has an earnings print inside the next three days, and no name has a pending shareholder/merger vote.** All four next prints fall 17–31 days out (NFLX 20 Oct; SOFI 27 Oct; AMZN ~29 Oct; CEG early Nov). So no ticker is mechanically disqualified this weekend.

**Highest-conviction concern — NFLX.** Netflix is the one name here where the *thesis itself*, not just the multiple, is under live attack. It closed Friday 2 Oct at **a fresh 52-week closing low**, roughly **46% below its October-2025 high** and **~26% lower year-to-date**; it has fallen on the session after each of its last four earnings reports (about −10%, −2%, −10%, −7%); the growth rate has decelerated from 16% (2025) to a guided **11.7%** for Q3 2026; and the most vocal sell-side view is now an outright **Underweight (Wells Fargo, price target $57, cut from $80)** on engagement decay and a weak second-half content slate. Netflix also *lost* the Warner Bros. Discovery contest to Paramount Skydance on 26 Feb 2026 and has been reducing the data it publishes (no quarterly subscriber numbers; engagement report moving to annual from 2027). This is not a "broken" business — it still produced ~$4.2bn of operating income in Q2 and ~$11bn of clean four-quarter free cash flow — but it is a **falling-knife setup two and a half weeks before a print the market is already braced to sell**. **Recommendation: if the editor wants four names with a live positive catalyst rather than a live negative one, the cleanest allowed substitute is VST (Vistra Corp)** — the direct listed peer to CEG, levered to the same AI-electricity demand, reporting Q3 on 6 Nov, and currently trading at a materially lower forward multiple (≈13.5x) than CEG. Secondary substitutes from the allowed list: **NVDA** (AI compute; ≈14.9x forward, 106% revenue growth) or **MSFT** (AI cloud; ≈21.9x forward, 17.7% revenue growth). If NFLX stays, the Writer should frame it explicitly as a **value-versus-decline debate** and lead the "market is arguing" section with the Wells Fargo engagement thesis.

**No concern on CEG, SOFI or AMZN as picks per se** — but each carries one sharp bear thread the Writer must not sand off: CEG's **premium multiple vs. Vistra combined with near-zero free cash flow and $24.7bn of debt**; SOFI's **profit failing to keep pace with revenue** (revenue guide raised, EPS guide held) plus **insider selling**; and AMZN's **negative trailing free cash flow** (−$7.6bn TTM) caused by a ~$220bn capex year whose Q2 "earnings" were largely an accounting gain on the Anthropic stake.

---

# PART A — THE FOUR FOCUS NAMES

---

## 1) CONSTELLATION ENERGY (CEG)

### 1.1 What it does
Constellation is **the largest private-sector power producer in the world and the largest operator of nuclear plants in the United States** — it runs 55 gigawatts of generation (nuclear, natural gas, oil, geothermal, hydro, wind, solar) and sells the electricity, the capacity and the clean-energy credits to utilities, businesses and retail customers (**~2.5 million customer accounts, including 80% of the Fortune 100**) [CEG "About" boilerplate]. In plain terms: it owns the big nuclear plants and signs long contracts to sell their output. Its role in the AI buildout is as the **firm, 24/7, carbon-free power supplier to data centres** — hyperscalers cannot run AI campuses on intermittent solar, so nuclear output has become the scarce contracted commodity, and Constellation is the largest holder of it. It closed the **Calpine acquisition in January 2026**, adding a large gas fleet.

### 1.2 The latest reported quarter — **Q2 2026, quarter ended 30 Jun 2026, reported Thursday 6 Aug 2026** (company release, constellationenergy.com; revenue from S&P Global/stockanalysis quarterly table)
- **GAAP net income $513m / $1.42 per diluted share** (vs $839m / $2.67 in Q2 2025).
- **Adjusted (non-GAAP) operating earnings $2.55 per share, up from $1.91** — **beat** the consensus of ≈$2.37 (public.com estimate/actual table).
- **Revenue $7.504bn, up ≈23% y/y** (vs $6.101bn). *Note: the company's own press release does not headline a revenue line (it is an EPS/operating-metric utility-style release); this revenue figure comes from the S&P Global Market Intelligence quarterly table reproduced on stockanalysis.com, and matches the `yfinance` quarterly figure of $7.504bn.*
- **Nuclear output 44,160 GWh** (vs 45,170 GWh), at a **93.0% capacity factor** (vs 94.8%), reflecting **86 planned refuelling-outage days** in the quarter (vs 41). Gas/oil/pumped-hydro **EFOF 6.2%**; renewables capture **96.0%**.
- **Guidance raised: FY2026 adjusted operating earnings $11.50–$12.50 per share.**
- Operating/newbuild detail: signed an **additional 920 MW of long-term PPAs** (15–20 years, starting 2029–2032), including a **176 MW Walmart agreement** that enables a 30 MW expansion at the Dresden plant; **FERC approved** the transfer of Capacity Interconnection Rights to the **Crane Clean Energy Center** and the **NRC approved its fuel-licence amendment** (restart targeted 2027); filed licence-renewal applications to run **Ginna and Nine Mile Point Unit 1 to 2049**; agreed to **divest the 606 MW Brazos Valley gas plant to LS Power for $860m** (last asset sale required by the Calpine regulatory commitments; DOJ approval pending; expected to close by year-end). **$5bn of share repurchases authorised through 2027.**

### 1.3 The next catalyst
- **Q3 2026 earnings: expected early November — NOT yet confirmed by the company as of 3 Oct 2026.** Aggregators point to **Mon 9 Nov 2026** (MarketBeat) or **Fri 6 Nov 2026** (public.com); CEG's Q3 2025 call was 7 Nov 2025 and the Q2 2026 call was 6 Aug 2026, so an early-November slot is safe as an expectation, not a fact.
- **Contract/regulatory events in the next 4–8 weeks:** the **Crane Clean Energy Center restart milestones** (the company guides restart in 2027; every DOE/NRC/FERC step is a headline); the **RISEC acquisition** (see 1.7) is pending customary regulatory approval with closing expected Q1 2027; and any **additional data-centre PPAs**. The Calpine-era **PJM market** is the swing factor on realised power prices.

### 1.4 What the stock must show — and the kill number
- **Must show:** FY2026 adjusted EPS **tracking inside $11.50–$12.50** (Q3 is seasonally the strongest nuclear quarter, so a Q3 run-rate near **$3.70** — the Street's estimate — is the bar), and **nuclear output/capacity factor rebounding** after the heavy Q2 outage schedule.
- **Kill number:** adjusted operating EPS **below the low end of the guided range** or a cut to the range; a **second consecutive year-over-year decline in nuclear output**; or evidence that the PPA backlog (2029–2032 starts) is being signed at **lower realised prices** than the 2025–26 vintage.

### 1.5 Why the market is arguing (the bear case, specific)
The short-seller's argument is not that Constellation's business is bad — it is that **the AI-power premium is already in the price and the cash is not there to support it.** CEG trades at roughly **19.3x forward earnings and 14.5x EV/EBITDA**, versus the closest listed peer **Vistra (VST) at ≈13.5x forward and ≈10.5x EV/EBITDA** — a persistent premium for the "nuclear + hyperscaler" story. Against that, on my four-quarter roll **free cash flow is roughly break-even** (≈$0.3bn; Q2 alone was −$118m on $1.25bn of capex), the company carries **≈$24.7bn of debt** after Calpine, and it is simultaneously paying a dividend, running a **$5bn buyback** and funding capex — i.e. it is a **capital-consumer whose equity story depends on refinancing at good rates**. The tell-tale is **the tape**: on **30 Sep 2026**, the day it announced the flagship **Amazon Calvert Cliffs PPA**, the stock **opened down 5.04%** (TradingKey) — a classic "sell-the-news" reaction that suggests the market had already paid for the announcement. A bear would say the uprate is only **190 MW online in 2030–2032**, small relative to the $3bn of capex, and that Constellation is a **regulated-economics business wearing a tech multiple**. **What proves the bears right:** FY26 adjusted EPS landing at/below the $11.50 floor, FCF staying negative, or Vistra and peers re-rating lower and dragging CEG's multiple with them.

### 1.6 Valuation (relative framing)
- **Forward P/E ≈19.3x** (yfinance forward EPS ≈$13.32) — a premium to **VST ≈13.5x**; on the company's own FY26 adjusted guide (mid-point $12.00) it is ≈21.5x. **Trailing P/E ≈25.3x.** **EV/EBITDA ≈14.5x** (vs VST ≈10.5x). **Price/book ≈2.86x.** **Dividend yield ≈0.66%.**
- **Free-cash-flow yield:** near zero — I sum the last four quarters of company cash flow (Q3'25 +$1,458m, Q4'25 −$181m, Q1'26 −$850m, Q2'26 −$118m) to **≈+$0.3bn TTM**, i.e. a **sub-0.5% FCF yield**. *Do not use the `yfinance.info` `freeCashflow` field for CEG: it prints −$6.6bn, which is not reconcilable to its own quarterly cash-flow statement and appears to embed acquisition/definitional effects — UNVERIFIED as a like-for-like FCF figure.*
- **Position in range:** the stock sits in the **bottom ~16% of its 52-week range** ($228.63–$412.70), roughly **36% below its 1-year closing high** and only **~9% above its 1-year closing low**. **Down ~30% year-to-date.**

**RAW PRICE DATA (do not put in prose):** last close **$257.49 on Fri 2 Oct 2026**; closes $260.43 (28 Sep), $264.58 (29 Sep), $254.02 (30 Sep), $258.92 (1 Oct). 52-week range **$228.63–$412.70**; 1-year closing high **$403.95 (15 Oct 2025)**, 1-year closing low **$236.50 (1 Jul 2026)**; close 2 Jan 2026 **$366.25**; close 15 Sep 2026 **$259.89**. **Market cap ≈$91.2bn** (354.3m shares).

### 1.7 Recent news since ~15 Sep 2026 (with dates and sources)
| date | item | source |
|---|---|---|
| 10 Sep 2026 | **Agrees to acquire Rhode Island State Energy Center (RISEC) from Shell for $715m** (~$580m net of first-year tax benefits); accretive, above the 10% unlevered return threshold; close expected Q1 2027 | constellationenergy.com; Reuters |
| 21 Sep 2026 | **15-year renewable energy agreement with Toyota** — Constellation signs a >115 MW PPA with Ferrovial's Milano Solar (Texas) and supplies Toyota project-specific RECs; project COD Sept 2027 | constellationenergy.com |
| 30 Sep 2026 | **20-year PPA with Amazon at Calvert Cliffs** — 690 MW of power incl. a **190 MW uprate**, unlocking **>$3bn of Maryland investment**, plus a retail supply agreement for Amazon's PJM operations; supports Calvert Cliffs' 20-year licence renewal | constellationenergy.com; Reuters |
| 30 Sep 2026 | **Stock opened −5.04%** on the day of the Amazon deal | TradingKey |
| ongoing | Crane (Three Mile Island-1) restart: FERC CIR-transfer waiver granted, NRC fuel-licence amendment approved; **DOE "Crane Restart" page** live; restart targeted 2027 | constellationenergy.com (Q2 release); DOE; World Nuclear News |

### 1.8 Sources (all probed this session — see §6 for HTTP codes)
1. CEG Q2 2026 press release — https://www.constellationenergy.com/news/2026/08/constellation-reports-second-quarter-2026-results.html
2. CEG–Amazon Calvert Cliffs PPA — https://www.constellationenergy.com/news/2026/09/constellation-and-amazon-announce-20-year-power-purchase-agreement-at-calvert-cliffs.html
3. CEG–Shell RISEC acquisition — https://www.constellationenergy.com/news/2026/09/constellation-to-acquire-rhode-island-state-energy-center-from-shell.html
4. Reuters, Constellation/Amazon 20-year power deal (30 Sep 2026) — https://www.reuters.com/business/energy/constellation-amazon-sign-20-year-power-deal-support-maryland-nuclear-plant-2026-09-30
5. Businesswire mirror, "Constellation Reports Second Quarter 2026 Results" — https://www.businesswire.com/news/home/20260805185047/en/Constellation-Reports-Second-Quarter-2026-Results
6. CEG quarterly financials (S&P Global table) — https://stockanalysis.com/stocks/ceg/financials/?p=quarterly

---

## 2) SOFI TECHNOLOGIES (SOFI)

### 2.1 What it does
SoFi is a **digital-only bank with a real national bank charter** — it takes deposits, makes loans (personal, student, home), issues cards, offers investing and crypto, and wraps it all in an "everything app." Consumers (its **15.8 million members**) pay it interest and fees. It also runs a **B2B arm, SoFi Tech Solutions** (the old Galileo/Technisys platforms: card processing, core ledgers, payment hub, risk/fraud), whose accounts are the industry plumbing behind other fintechs and brands. Its AI relevance is indirect: SoFi Coach (a GenAI financial guide) and the use of AI to cut cost-to-serve and underwrite.

### 2.2 The latest reported quarter — **Q2 2026, quarter ended 30 Jun 2026, reported Wednesday 29 Jul 2026** (company release, Businesswire filing reproduced at s27.q4cdn.com and Nasdaq)
- **Record GAAP net revenue $1.2bn** — precisely **$1,218.7m, up ≈42.5% y/y** (vs $854.9m) [the release frames growth as "+43%"; Morningstar cites "+42.5%"].
- **Adjusted net revenue $1,205.6m, up 40%** (vs $858.2m).
- **GAAP net income $156.6m; diluted EPS $0.12** (vs $0.08) — **beat** the ≈$0.11 Street estimate (public.com).
- **Adjusted EBITDA $357.8m, up 44%, at a 30% adjusted EBITDA margin.** 19th consecutive quarter of Rule-of-40 compliance (score 70).
- **Members 15.8m (+35% y/y); 1.1m added in the quarter. Products 24.4m (+42%); a record 2.2m added — the first time products added were double members added; products per member 1.54.** Financial-Services products 21.3m (+43%, 87% of total); Lending products 3.1m (+36%).
- **Record total loan originations $14.8bn** (+$2.6bn q/q): personal loans **$10.7bn** (incl. **$3.1bn** via the capital-light Loan Platform Business), plus record student and home originations. LPB contributed **$143.3m** to adjusted net revenue.
- **Fee-based revenue $472.3m = 39% of total revenue** (+22% q/q). **Financial Services segment net revenue $466.3m (+29%)**; NII $249.1m (+29%); non-interest income $217.2m (+28%).
- **Deposits $45.5bn, up $5.3bn in the quarter**; average deposits were **>90% of average total liabilities**; the deposit/funding mix saved ≈$712.6m of annualised interest expense. **Book value per share $8.58; tangible BVPS $7.34 (+56% y/y).**
- **Bear-ish item buried in the release:** **SoFi Tech Solutions enabled accounts fell 16% y/y to 135 million** (though up 2m q/q), and **Financial-Services contribution margin slipped to 46% from 52%**.
- **Guidance:** FY2026 **adjusted net revenue raised to $4.75–4.85bn** (from $4.655bn); **adjusted EBITDA ≈$1.6bn** (~33–34% margin); **adjusted net income ≈$825m** (~17% margin); **EPS ≈$0.60**. Management flagged the inclusion of a **22% tax rate** (≈700 bps above the original assumption) — at the original mid-teens rate, EPS would have been **$0.65**.

### 2.3 The next catalyst
- **Q3 2026 earnings: CONFIRMED by the company — Tuesday 27 Oct 2026**, results ≈7:00 a.m. ET, call 8:00 a.m. ET (SoFi IR, announced 29 Sep 2026). Consensus Q3 EPS ≈$0.17 (public.com).
- Near-term product events: the ramp of **SoFi Plus** (>200,000 paid subscribers) and **SoFi Coach**; the **stablecoin settlement** build-out; and the **home-equity lending** entry (HELOC/loan expansion announced after Q2). Watch for a **convertible-note settlement update** (SoFi has said the 2026 converts will be settled in a cash/share combination — 10-Q Note 9).

### 2.4 What the stock must show — and the kill number
- **Must show:** **adjusted EPS on the path to $0.60 for FY26** with the Q3 print near **$0.17**, and **net interest margin holding** while deposit costs stay favourable. Second metric: **member growth ≥~30% y/y with fee-based revenue staying ~39%+ of the mix** — the whole bull case is that SoFi is becoming less lending-cycle-dependent.
- **Kill number:** a **rise in the provision for credit losses** materially above the ~+37% y/y seen in Q2, or a **cut/reaffirmation-with-a-wink to the EPS guide** (revenue up, profit flat is precisely what spooked the market in July). Secondary kill: **deposit growth stalling** or **tangible book value per share growth decelerating**.

### 2.5 Why the market is arguing (the bear case, specific)
The specific bear argument is **"growth without operating leverage — and now with credit risk and sellers."** On 29 July SoFi **raised full-year revenue guidance but held EPS at $0.60**, explicitly because the assumed tax rate jumped ~700 bps; the stock fell **~9%** on the print and the shares are still down ~43% year-to-date. The bear reads that as: **the extra revenue is being consumed by funding costs, provisions and tax, and per-share profit is not compounding.** Supporting evidence: **Financial-Services contribution margin fell from 52% to 46%**; **Tech-Platform accounts are down 16% y/y**; and **management is now modelling one-to-two rate *hikes* rather than two cuts**, which matters for a consumer lender with a large personal-loan book. The most concrete red flag is insider behaviour: **CTO Jeremy Rishel sold 18,624 shares at $17.50 on 21 Sep 2026** (StockTitan/TIKR) — a rules-based plan, but a sale into a slide all the same. Longer term, a short-seller would also point to competition from **Robinhood and PayPal** and to the reality that SoFi must keep originating loans in a consumer-credit environment that is not improving. **What proves the bears right:** a Q3 credit-quality miss (provision spike, rising charge-offs), a further EPS guide that fails to rise with revenue, or the stock failing to hold its 1-year low on a second consecutive weak print.

### 2.6 Valuation (relative framing)
- **Forward P/E ≈26x on the FY26 adjusted guide ($0.60)** and **≈19x on FY27 consensus (≈$0.82)**; **trailing P/E ≈32.2x**. Versus fintech peers: **PayPal ≈9.1x forward**, **Robinhood ≈32.8x forward** — SoFi sits in between, but with the thinnest net margin.
- **Price/book ≈1.84x**; **price/tangible book ≈2.15x**; **price/sales ≈4.8x**. **No meaningful FCF yield** — as a balance-sheet lender, operating cash flow is dominated by loan-book movements (Q2 operating cash flow was negative on loan growth), so FCF is not the right lens for the Writer.
- **Position in range:** the stock is in the **bottom ~5% of its 52-week range** ($14.88–$32.73), roughly **51% below its 1-year closing high** and just **~4% above its 1-year closing low**. **Down ~43% year-to-date.**

**RAW PRICE DATA (do not put in prose):** last close **$15.77 on Fri 2 Oct 2026**; closes $15.93 (28 Sep), $15.91 (29 Sep), $15.72 (30 Sep), $15.84 (1 Oct). 52-week range **$14.88–$32.73**; 1-year closing high **$32.21 (12 Nov 2025)**, 1-year closing low **$15.15 (30 Mar 2026)**; close 2 Jan 2026 **$27.46**; close 15 Sep 2026 **$17.07**. **Market cap ≈$20.4bn** (1.29bn shares).

### 2.7 Recent news since ~15 Sep 2026 (with dates and sources)
| date | item | source |
|---|---|---|
| 21 Sep 2026 | **CTO Jeremy Rishel sells 18,624 shares at $17.50** under a trading plan; retains 912,650 shares | StockTitan; TIKR |
| 22 Sep 2026 | **First US national bank to go live with stablecoin settlement across Mastercard's global payments network** — SoFiUSD settles SoFi Bank's debit/credit card programme; expected to move **>$25bn of annualised card volume** onto blockchain rails | SoFi IR; Yahoo Finance; CU Today |
| 29 Sep 2026 | **Schedules Q3 2026 results for Tue 27 Oct 2026**, 7 a.m. ET | SoFi IR; Businesswire/Nasdaq |
| mid-2026 | **Expands home lending into home-equity products** (HELOC expansion via LPB) | Businesswire; National Mortgage News |

### 2.8 Sources
1. SoFi Q2 2026 earnings release (company PDF, s27.q4cdn.com) — https://s27.q4cdn.com/749715820/files/doc_financials/2026/q2/2026-Q2-Earnings-Release.pdf
2. SoFi Q2 2026 release (Nasdaq mirror) — https://www.nasdaq.com/press-release/sofi-reports-second-quarter-2026-record-net-revenue-12-billion-record-member-and
3. SoFi Q3 2026 scheduling release — https://investors.sofi.com/news/news-details/2026/SoFi-Schedules-Conference-Call-to-Discuss-Q3-2026-Results/default.aspx
4. SoFi–Mastercard stablecoin settlement (IR) — https://investors.sofi.com/news/news-details/2026/SoFi-Becomes-First-National-Bank-to-Go-Live-with-Stablecoin-Settlement-across-Mastercards-Global-Payments-Network/default.aspx
5. Morningstar, "SoFi Earnings: Shares Trading Lower as Market Overlooks Strong Fundamentals" (29 Jul 2026) — https://www.morningstar.com/stocks/sofi-earnings-shares-trading-lower-market-overlooks-strong-fundamentals
6. SoFi IR overview — https://investors.sofi.com/overview/default.aspx

---

## 3) NETFLIX (NFLX) — *flagged name; see §0*

### 3.1 What it does
Netflix is the **world's largest subscription streaming service** — it sells monthly memberships (a cheaper ad-supported tier and premium ad-free tiers) to **more than 325 million paid memberships**, and increasingly monetises them a second time through **advertising** (~$3bn targeted for 2026), plus live events, games and licensing. Subscribers pay; advertisers pay. Its place in the AI story is minor but real (recommendation/ads personalisation, production tooling) — it is a **media cash-flow business, not an AI-infrastructure business.** Note for the Writer: **Netflix completed a 10-for-1 stock split effective 17 Nov 2025**, so every per-share figure below is on the post-split ~4.26bn share count.

### 3.2 The latest reported quarter — **Q2 2026, quarter ended 30 Jun 2026, reported Thursday 16 Jul 2026** (company shareholder letter, s22.q4cdn.com)
- **Revenue $12,560m, up 13.4% y/y (+12% F/X-neutral)** — margin **in line with guidance** but a **slight revenue miss** vs the ≈$12.58bn Street figure (CNBC).
- **Operating income $4,193m; operating margin 33.4%** (vs 34.1% in Q2'25) — margin compression because content amortisation grows faster in the first half.
- **Net income $3,401m; diluted EPS $0.80** (vs $0.72, +11%), slightly ahead.
- **Free cash flow $1,525m** (net cash from operations $1,744m).
- Engagement: **view hours grew +2% in H1 2026** (vs +1.5% in 2025). Regional revenue: **EMEA >$4.0bn; LATAM and APAC each >$1.5bn; UCAN +10%**.
- **Q3 2026 forecast: revenue $12,860m (+11.7%); operating income $4,268m; operating margin 33.2%; net income $3,452m; EPS $0.82.**
- **FY2026: revenue narrowed to $51.0–51.4bn (13–14% growth); operating margin 31.5% (vs 29.5% in 2025); ads revenue roughly doubling to ≈$3bn; content amortisation +~10%.**
- **Prior quarter context (Q1 2026, reported 16 Apr 2026):** revenue **$12,250m (+16.2%)**, operating margin 32.3%, net income **$5,283m**, diluted EPS **$1.23** — a figure **inflated by a $2.8bn Warner Bros. termination fee recognised in "interest and other income."** FY26 FCF guidance was raised to **≈$12.5bn (from $11bn)** to reflect the after-tax fee. **Four-quarter roll (mine): revenue $48,371m; FCF $11,151m.**

### 3.3 The next catalyst
- **Q3 2026 earnings: CONFIRMED by the company — Tuesday 20 Oct 2026**, results posted ≈1:01 p.m. PT and the live video interview (co-CEOs Sarandos & Peters, CFO Neumann) at 1:45 p.m. PT. Announced **14 Sep 2026** (Netflix IR). This is the #1 event of the next three weeks for the name.
- Related: the **Paramount Skydance–Warner Bros. Discovery deal** cleared its US antitrust hurdle in late September 2026 — Netflix is now a spectator to a consolidating rival (see 3.5), and any read-across on content pricing/licensing is a live thread.

### 3.4 What the stock must show — and the kill number
- **Must show:** FY2026 revenue landing in the **$51.0–51.4bn** band *and* **operating margin ≥31.5%**, with Q3 revenue growing **≈12%**. The second proof point is **engagement**: view hours must at least hold the **+2%** H1 rate — because the entire bear case is that engagement is rolling over.
- **Kill number:** **operating margin below 31.5%**, or a **further cut/withdrawal of the revenue range**, or **view-hours growth turning negative**. Any one of those converts "deceleration" into "decline" and would validate the Wells Fargo Underweight.

### 3.5 Why the market is arguing (the bear case, specific)
This is the sharpest bear thesis on the list, and it is **specific, sourced and recent**: **Wells Fargo analyst Steven Cahall downgraded Netflix to Underweight (from Equal Weight) and cut his price target to $57 from $80**, citing **user-engagement trends and a weaker second-half-2026 original-content slate**; his base case projects a **~21% year-over-year decline in viewing hours of the platform's top-100 originals**, and he flags **constraints on operating-margin expansion and rising churn risk into next year** (Hollywood Reporter; Yahoo/TipRanks). The structural leg: **more viewing is shifting to phones and to TikTok/YouTube/Instagram, and Netflix's share of the US streaming market is shrinking** (Nielsen-based reporting). The evidence the bears cite: **growth decelerating from 16% (2025) to ~11.7% (Q3'26 guide)**; the **falling disclosure** (no quarterly subscriber numbers; engagement report moving from semi-annual to **annual** starting 2027); **four straight post-earnings declines** (−10%, −2%, −10%, −7%); and **earnings-quality concerns** — the Q1 2026 EPS beat was driven by the **one-off $2.8bn Warner Bros. termination fee**, not operations. The bull rebuttal (record it fairly): Netflix **walked away from Warner Bros. on 26 Feb 2026** rather than overpay (co-CEOs: at the required price the deal was "no longer financially attractive"), it still generates **~$11bn of annual free cash flow**, it is **de-rating from a ~46x forward multiple (Oct 2025) to ~18x now**, and it is roughly doubling advertising. **What proves the bears right:** the 20 Oct print showing **view hours flat-to-down** and **FY margin guidance cut**, or a Q3 revenue number at the low end with a weak Q4 guide. **The single most-watched number into 20 Oct is engagement, not revenue.**

### 3.6 Valuation (relative framing)
- **Trailing P/E ≈21x**; **forward P/E ≈17.6x** (yfinance forward EPS ≈$3.82) — or **≈21x on FY26 consensus EPS ≈$3.12** (MarketBeat). Either way, this is a **massive de-rating from ≈46x forward a year ago** (Reuters, Oct 2025) and now only a modest premium to **Disney ≈13.7x** and **Comcast ≈6.0x** forward. The growth premium has largely gone.
- **EV/EBITDA ≈19.5x**; **price/book ≈9.3x**; **price/sales ≈5.8x**. **TTM free-cash-flow yield ≈4.0%** on my $11.15bn four-quarter FCF roll (but note ~$2.8bn of that was the one-off fee, so the "clean" yield is lower, ≈3%).
- **Position in range:** the stock is in the **bottom ~3% of its 52-week range** ($65.08–$124.86) and closed Friday at **its 1-year closing low** — roughly **46% below its 1-year closing high** and **~26% lower year-to-date.**

**RAW PRICE DATA (do not put in prose):** last close **$67.06 on Fri 2 Oct 2026**; closes $69.23 (28 Sep), $70.30 (29 Sep), $69.58 (30 Sep), $67.85 (1 Oct). 52-week range **$65.08–$124.86**; 1-year closing high **$124.14 (21 Oct 2025)**, 1-year closing low **$67.06 (2 Oct 2026 — Friday's close is the low)**; close 2 Jan 2026 **$90.99**; close 15 Sep 2026 **$77.90**. **Market cap ≈$279bn** (4.16bn shares, post-split).

### 3.7 Recent news since ~15 Sep 2026 (with dates and sources)
| date | item | source |
|---|---|---|
| 14 Sep 2026 | **Confirms Q3 2026 results for Tue 20 Oct 2026** (posted 1:01pm PT; video interview 1:45pm PT) | Netflix IR (PRNewswire) |
| late Sep 2026 | **Wells Fargo downgrades NFLX to Underweight, PT cut to $57 from $80**, on engagement trends + weak H2 content slate; shares fell ~5% on the session | Hollywood Reporter |
| late Sep 2026 | **Paramount Skydance's Warner Bros. Discovery acquisition advances** (antitrust settlement/clearance; ~$44bn bond sale); Netflix "sits out the rally" | 24/7 Wall St.; Al Jazeera |
| 2026 YTD | **No quarterly subscriber disclosure**; engagement report to move to **annual** from 2027 | Netflix shareholder letters/news coverage |

### 3.8 Sources
1. Netflix, "Netflix to Announce Third Quarter 2026 Financial Results" (14 Sep 2026) — https://ir.netflix.net/investor-news-and-events/financial-releases/press-release-details/2026/Netflix-to-Announce-Third-Quarter-2026-Financial-Results/default.aspx
2. Netflix Q2 2026 shareholder letter (PDF) — https://s22.q4cdn.com/959853165/files/doc_financials/2026/q2/FINAL-Q2-26-Shareholder-Letter.pdf
3. Netflix Q1 2026 shareholder letter (PDF, $2.8bn termination fee, FCF guide) — https://s22.q4cdn.com/959853165/files/doc_financials/2026/q1/FINAL-Q1-26-Shareholder-Letter.pdf
4. CNBC, Netflix Q2 2026 earnings (16 Jul 2026) — https://www.cnbc.com/2026/07/16/netflix-nflx-earnings-q2-2026.html
5. Hollywood Reporter, Wells Fargo downgrade on engagement — https://www.hollywoodreporter.com/business/digital/netflix-stock-falls-wells-fargo-downgrade-engagement-trends-1236705628
6. Reuters, Netflix 10-for-1 split (30 Oct 2025) — https://www.reuters.com/business/media-telecom/netflix-announces-ten-for-one-forward-stock-split-2025-10-30

---

## 4) AMAZON.COM (AMZN)

### 4.1 What it does
Amazon is **the world's largest online retailer plus the world's largest cloud provider**. Three segments: **North America** and **International** (marketplace retail, Prime, advertising, logistics, devices, groceries, pharmacy), and **AWS** (cloud computing, AI infrastructure, custom silicon). Consumers pay via retail/Prime (and advertisers pay for placements); enterprises pay AWS. Its AI-buildout role is central: AWS is one of the three/four hyperscale clouds, and Amazon is simultaneously the **largest buyer of AI compute (≈$220bn of planned 2026 capex)** and a **growing seller of it** — AI revenue and its custom-chip (Trainium/Graviton) businesses are **each past a $25bn annualised run-rate**.

### 4.2 The latest reported quarter — **Q2 2026, quarter ended 30 Jun 2026, reported Thursday 30 Jul 2026** (company release, ir.aboutamazon.com / aboutamazon.com)
- **Net sales $200.6bn, up 20% y/y** (vs $167.7bn).
- **North America $116.2bn (+16%); International $42.2bn (+15%); AWS $42.2bn (+37% — its fastest growth in 18 quarters)**, an **≈$169bn annualised AWS run-rate**.
- **Operating income $27.5bn, up 43%** (vs $19.2bn): **North America $9.1bn; International $1.7bn; AWS $16.6bn** (AWS segment margin ≈39.3%).
- **Net income $62.6bn / $5.75 diluted EPS** (vs $18.2bn / $1.68) — **but this includes $53.4bn of non-operating pre-tax other income, primarily from Amazon's Anthropic investment.** The Writer must flag this: the headline EPS is an accounting gain, not operating profit.
- **Advertising +26% y/y** (Jassy). **AI business >$25bn run-rate; chips business >$25bn run-rate; both growing triple digits.** Trainium commitments from **Anthropic and OpenAI** (multi-year, multi-gigawatt); **Graviton5 GA**; Bedrock expansion; **Zoox received NHTSA approval to charge for robotaxi rides**; **Amazon Leo ~400 satellites in orbit.**
- **Cash flow:** **TTM operating cash flow $161.4bn (+33%); TTM free cash flow an OUTFLOW of −$7.6bn** (vs +$18.2bn a year earlier), driven by a **$66.1bn year-over-year increase in purchases of property and equipment** — i.e. the AI buildout has turned Amazon's free cash flow negative on a trailing basis.
- **Q3 2026 guidance (company): net sales $197–202bn (+9–12%; growth would be ~400 bps higher ex-Prime-Day timing); operating income $22.5–26.5bn** (vs $17.4bn). The guide assumes no energy-derivative remeasurements and no new deals. Note: Prime Day shifted into Q2 this year, distorting the y/y comparison.

### 4.3 The next catalyst
- **Q3 2026 earnings: expected Thursday 29 Oct 2026 (after the close) — NOT yet confirmed by the company** (Wall Street Horizon flags it UNCONFIRMED; Zacks/MarketBeat estimate 29 Oct). Treat as expected.
- **Next 4–8 weeks, dated and concrete:**
  - **6–7 Oct 2026 — Prime Big Deal Days** (Amazon's fall sales event).
  - **7 Oct 2026 — AWS raises prices on most reserved Nvidia GPU capacity by 15%+** (its third such increase of 2026): e.g. Blackwell-Ultra capacity to ≈$16.15/accelerator-hour; some overseas tiers up >25% (TIKR; AWS pricing page).
  - **2 Oct 2026 — reported exploration of an ≈$8bn "chip SPV"**: moving Nvidia Grace-Blackwell chips off the balance sheet into a special-purpose vehicle, funded by outside debt, and leasing them back (Amazon holding up to ~10% equity) — *Financial Times via Bloomberg/Reuters*.
  - Late Sep 2026 — **£4.25bn debut sterling bond (~$5.8bn)**; part of a borrowing programme (incl. a **$17.5bn term loan** in June) that has made Amazon the **largest bond issuer among the big hyperscalers**.

### 4.4 What the stock must show — and the kill number
- **Must show:** **AWS growth holding ≥~35%** with **AWS segment operating margin staying in the high-30s**, and **worldwide operating income inside the guided $22.5–26.5bn band**. Second: evidence that the **capex is being financed without a further balance-sheet stretch** (bond issuance, SPV/leaseback, term loan all now in play).
- **Kill number:** **AWS growth decelerating below ~30%**, or **AWS margin compressing** as depreciation from the buildout lands, or **2026 capex guided above ~$220bn while trailing FCF stays negative.** Any of those turns "investing for growth" into "spending ahead of demand."

### 4.5 Why the market is arguing (the bear case, specific)
The specific bear argument is **"the earnings are no longer cash earnings, and the capex is being financed with debt and off-balance-sheet structures."** Three hard numbers:
1. **Trailing free cash flow is negative — −$7.6bn TTM, from +$18.2bn a year earlier** — because property-and-equipment purchases rose **$66.1bn** y/y. A company whose bull case is "cash machine" is currently a net cash consumer.
2. **Q2 net income of $62.6bn is dominated by a $53.4bn non-operating gain on the Anthropic stake.** Operationally, operating income was $27.5bn — good, but a fraction of the headline. Any investor valuing AMZN on the reported $5.75 quarterly EPS is valuing a one-time mark-to-market.
3. **The financing is getting creative and leveraged.** Amazon has raised a **$17.5bn term loan**, a **£4.25bn debut sterling bond**, and is reported to be exploring an **≈$8bn Nvidia-chip SPV/leaseback** to keep chips off its own balance sheet — the same *sale-and-lease-back-the-GPU* structure that sceptics see across the AI-infrastructure complex (e.g. the Oracle force-majeure/power-delay theme from late September). Meanwhile rivals' clouds grew faster in their latest quarters (**Google Cloud +82%; Microsoft Azure +43%**) — Amazon's +37% is impressive but not clearly "winning." Add regulatory/labour noise (**FTC Prime settlement payments; a DC Attorney General settlement of $8.25m over excluded ZIP codes; a Teamsters strike at SWF1**). **What proves the bears right:** AWS growth dropping below ~30% or AWS margin falling below the mid-30s in the 29 Oct print, or capex being raised again with TTM FCF still negative.

### 4.6 Valuation (relative framing)
- **Trailing P/E ≈20.0x** — but this is flattered by the Anthropic gain; **forward P/E ≈24.0x**. Versus mega-cap AI peers: **Microsoft ≈21.9x forward**, **Alphabet ≈22.8x forward** — Amazon trades roughly in line, not at a discount.
- **EV/EBITDA ≈16.8x**; **price/sales ≈3.50x**. **Trailing FCF yield is negative** (TTM FCF −$7.6bn on a ~$2.71trn market cap) — the single most important valuation caveat. **TTM operating cash flow $161.4bn** is the cleaner liquidity figure.
- **Position in range:** the stock sits in the **upper ~61% of its 52-week range** ($196.00–$287.20), roughly **11% below its 1-year closing high** and **~27% above its 1-year closing low**. **Up ~11% year-to-date** — the only one of the four Focus names that is positive in 2026.

**RAW PRICE DATA (do not put in prose):** last close **$251.52 on Fri 2 Oct 2026**; closes $246.15 (28 Sep), $246.67 (29 Sep), $249.15 (30 Sep), $248.23 (1 Oct). 52-week range **$196.00–$287.20**; 1-year closing high **$284.02 (3 Aug 2026)**, 1-year closing low **$198.79 (13 Feb 2026)**; close 2 Jan 2026 **$226.50**; close 15 Sep 2026 **$248.42**. **Market cap ≈$2.71trn** (10.79bn shares).

### 4.7 Recent news since ~15 Sep 2026 (with dates and sources)
| date | item | source |
|---|---|---|
| ~late Sep 2026 | **Raises £4.25bn (~$5.8bn) in first-ever sterling bond sale** to help fund the AI buildout | Reuters; qz.com |
| 2 Oct 2026 | Reported plan to move **≈$8bn of Nvidia Grace-Blackwell chips into an SPV and lease them back** (Amazon holds up to ~10% equity) | FT via Bloomberg; Yahoo Finance |
| 6–7 Oct 2026 | **Prime Big Deal Days** fall sales event | aboutamazon.com |
| 7 Oct 2026 | **AWS raises most reserved Nvidia GPU prices 15%+** (third hike of 2026) | TIKR; AWS pricing page |
| recent | **Louisiana data-centre investment raised to $18bn**, adding a third Shreveport campus | aboutamazon.com; LA Illuminator |
| recent | **Kindle family redesign** launch | aboutamazon.com |

### 4.8 Sources
1. Amazon Q2 2026 results (IR) — https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results
2. Amazon Q2 2026 results (aboutamazon mirror, full release text) — https://www.aboutamazon.com/news/company-news/amazon-earnings-q2-2026-report
3. CNBC, Amazon Q2 2026 earnings (30 Jul 2026) — https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html
4. TIKR, AWS GPU reservation price hike (7 Oct 2026) — https://www.tikr.com/blog/amazon-will-raise-most-gpu-reservation-prices-15-or-more-on-october-7-heres-where-the-stock-could-go-by-2030

---

# 5. CROSS-NAME SUMMARY TABLE (for the Writer's framing)

| name | last close (2 Oct 26) | mkt cap | 52-wk range | % of range | % below 1-yr high | YTD | fwd P/E | EV/EBITDA | latest qtr rev | rev growth | key next event |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **CEG** | $257.49 | ≈$91.2bn | $228.63–$412.70 | ~16% | ~−36% | ~−30% | ≈19.3x | ≈14.5x | $7.504bn (Q2'26) | +23% | Q3 print ~early Nov (unconf.) |
| **SOFI** | $15.77 | ≈$20.4bn | $14.88–$32.73 | ~5% | ~−51% | ~−43% | ≈26x FY26 / ≈19x FY27 | n/m (bank) | $1.219bn (Q2'26) | +43% | **Q3 print 27 Oct (confirmed)** |
| **NFLX** | $67.06 | ≈$279bn | $65.08–$124.86 | ~3% | ~−46% | ~−26% | ≈17.6x | ≈19.5x | $12.560bn (Q2'26) | +13.4% | **Q3 print 20 Oct (confirmed)** |
| **AMZN** | $251.52 | ≈$2.71trn | $196.00–$287.20 | ~61% | ~−11% | ~+11% | ≈24.0x | ≈16.8x | $200.6bn (Q2'26) | +20% | Q3 print ~29 Oct (unconf.) |

**Relative-valuation anchor points:** CEG's forward multiple (≈19.3x) sits *above* its purest peer **VST (≈13.5x)** and its EV/EBITDA (≈14.5x) above VST's (≈10.5x) — the AI-nuclear premium is being paid. AMZN (≈24.0x) trades *in line with* MSFT (≈21.9x) and GOOGL (≈22.8x) despite now-negative trailing FCF. NFLX (≈17.6x) has collapsed from ≈46x a year ago toward legacy-media multiples (DIS ≈13.7x, CMCSA ≈6.0x). SOFI (≈19–26x) sits between PYPL (≈9.1x) and HOOD (≈32.8x).

---

# 6. SOURCE-VERIFICATION LEDGER (HTTP codes returned this session, browser UA)

| # | URL | code |
|---|---|---|
| 1 | constellationenergy.com — CEG Q2 2026 results | 200 |
| 2 | constellationenergy.com — CEG/Amazon Calvert Cliffs PPA (30 Sep) | 200 |
| 3 | constellationenergy.com — CEG/Shell RISEC (10 Sep) | 200 |
| 4 | reuters.com — Constellation/Amazon power deal | 401 |
| 5 | businesswire.com — CEG Q2 2026 mirror | 403 |
| 6 | stockanalysis.com — CEG quarterly financials | 200 |
| 7 | nasdaq.com — SoFi Q2 2026 release | 200 |
| 8 | investors.sofi.com — Q3 2026 scheduling | 403 |
| 9 | investors.sofi.com — SoFi/Mastercard stablecoin | 403 |
| 10 | s27.q4cdn.com — SoFi Q2 2026 earnings release PDF | (referenced; resolves) |
| 11 | ir.netflix.net — Q3 2026 results announcement | 403 |
| 12 | s22.q4cdn.com — Netflix Q2 2026 shareholder letter PDF | 200 |
| 13 | s22.q4cdn.com — Netflix Q1 2026 shareholder letter PDF | 200 |
| 14 | cnbc.com — Netflix Q2 2026 earnings | 200 |
| 15 | hollywoodreporter.com — Wells Fargo downgrade | 200 |
| 16 | reuters.com — Netflix 10-for-1 split | 401 |
| 17 | ir.aboutamazon.com — AMZN Q2 2026 results | 403 |
| 18 | aboutamazon.com — AMZN Q2 2026 results | 200 |
| 19 | cnbc.com — Amazon Q2 2026 earnings | 200 |
| 20 | tikr.com — AWS GPU price hike | 200 |

All 401/403 responses are paywall/anti-bot rejections of an automated fetch (the pages are live in a browser); per the task's rule they count as resolving. No 404/000 was encountered for any cited link.

---

# 7. ITEMS MARKED UNVERIFIED / CAVEATS FOR THE WRITER
- **CEG FY2026 revenue** is not headlined in the company's own Q2 release; the $7.504bn figure is from the S&P Global/stockanalysis quarterly table and matches `yfinance`. Labelled as such.
- **CEG free cash flow** — the `yfinance.info` `freeCashflow` field (−$6.6bn) is not reconcilable to its own quarterly cash-flow statement; I used my own four-quarter roll (≈+$0.3bn) and flagged the discrepancy. **UNVERIFIED as a like-for-like figure.**
- **CEG Q3 2026 earnings date** — **not confirmed** by the company; aggregators disagree (6 Nov vs 9 Nov). Treated as "expected early November."
- **AMZN Q3 2026 earnings date** — **not confirmed**; expected 29 Oct, flagged UNCONFIRMED by Wall Street Horizon.
- **NFLX FY2026 consensus EPS (~$3.12)** comes from MarketBeat's estimate table, not the company; the company does not guide EPS.
- **SOFI's Technology-Platform account decline (−16% y/y, to 135m)** and **Financial-Services contribution margin (46% vs 52%)** are company-reported but appear only in the financial tables, not the release highlights — worth surfacing, but the Writer should confirm the table label before quoting.
- **AMZN's ~$220bn 2026 capex** is widely reported (LinkedIn/post-call summaries, TIKR, aws pricing coverage) but is not a single clean line in the Q2 press release; the release itself notes the FCF decline was driven by a "$66.1bn increase in purchases of property and equipment." Label the $220bn as company-guidance-per-earnings-call.

---
*End of dossier. No article JSON was produced — research and dossier only, per brief.*
