# MSFT RESEARCH BRIEF — The Signal
Prepared Oct 25, 2026. Last close used: **Friday, Oct 23, 2026: $524.51** (yfinance daily history confirms 2026-10-23 close = 524.51; prior day 521.08).
Reports fiscal Q1 2027 **Wednesday, Oct 28, 2026 after the close** (MSFT IR events page); call 5:30pm ET.

---

## 1. WHAT MICROSOFT SELLS

Microsoft sells software subscriptions and rented computing. The subscription half is Microsoft 365 (Word/Excel/Teams/Outlook plus the Copilot AI add-on), LinkedIn, Dynamics business apps and Windows licences — high-margin, recurring, sold per seat. The renting half is Azure, its cloud: customers pay for compute, storage and AI model inference by consumption, and Microsoft buys the land, buildings, chips and power to serve it. It is simultaneously the biggest reseller of OpenAI's models (via Azure and Copilot) and a competitor to the AI labs and cloud customers it hosts — it now builds its own inference chips (Maia) partly to cut its dependence on Nvidia, and it sells capacity to frontier labs (OpenAI, Anthropic models) while competing with them for the same enterprise AI budgets.

Key primary facts on the AI buildout:
- Azure revenue **surpassed $100B for the first time in FY26** — Nadella, Q4 FY26 release: "This year, Azure revenue surpassed $100 billion for the first time, and Microsoft 365 Copilot reached over 30 million paid seats."
- Exact Azure dollars: **$29.42B in the June 2026 quarter; $101.9B for FY26** (Reuters, Sept 2, 2026; recast in Microsoft's Sept 2 segment presentation).
- Custom silicon: **Maia 200** announced Jan 26, 2026 (TSMC 3nm, 216GB HBM3e, 7 TB/s, >10 PFLOPS FP4; "30% better performance per dollar than the latest generation hardware in our fleet today"). **Maia 300** announced Oct 12, 2026, with Microsoft saying it "will scale our Azure Maia family to multi-gigawatt deployments starting in 2027, making Maia the primary inference system for Microsoft products and services" and that Maia 200 already serves "Microsoft Copilot" and runs "OpenAI models, Microsoft's own MAI models and leading open-source model families."

---

## 2. VERIFIED NUMBERS

### 2a. yfinance snapshot (raw prints, `/home/chino/video-venv/bin/python3`, run Oct 25, 2026)
Ticker.info:
```
currentPrice = 524.51
previousClose = 521.08
marketCap = 3894773022720          # $3.895T
trailingPE = 29.220612
forwardPE = 22.127527
totalRevenue = 331839012864         # $331.84B TTM
freeCashflow = 16545500160          # $16.55B  <-- INCONSISTENT, do not use (see note)
operatingCashflow = 182934994944    # $182.93B TTM
capitalExpenditures = None
totalDebt = 128812998656            # $128.81B  <-- includes leases; BS total debt is $56.83B
totalCash = 76842999808             # $76.84B
sharesOutstanding = 7425545491
fiftyTwoWeekLow = 349.2
fiftyTwoWeekHigh = 553.72
recommendationKey = strong_buy
recommendationMean = 1.33333
targetMeanPrice = 601.7281
numberOfAnalystOpinions = 53
trailingEps = 17.95
forwardEps = 23.70396
```
Computed by hand from `quarterly_cashflow` (last 4 quarters, all in $M):
```
Operating Cash Flow      55,441 + 46,679 + 35,758 + 45,057 = 182,935
Capital Expenditure     -35,802 + -30,876 + -29,876 + -19,394 = -115,948
TTM FCF (OCF + capex)                                        =  66,987
```
- **TTM FCF $66.99B** (matches FY26 full-year FCF; identical, since the 4 quarters are exactly FY26).
- **TTM capex (cash PP&E) $115.95B.** TTM FCF margin 20.2%.
- **Note on `info.freeCashflow` = $16.5B:** it does not reconcile with OCF minus capex ($67.0B) and appears to be a broken yfinance field. Do NOT quote it. Same caveat for `info.totalDebt` ($128.8B vs balance-sheet total debt $56.83B — the info field is evidently including operating-lease liabilities).
- Balance sheet at 6/30/26 (yfinance `quarterly_balance_sheet`): Total Debt 56,826; Cash & equivalents 20,935; **Cash + short-term investments 76,651**; Net Debt 19,359; Shares 7,428,434,704; Stockholders' equity 442,387.
- Analyst consensus: **strong buy, mean 1.33, 53 analysts, mean target $601.73** (+14.7% vs $524.51).

### 2b. Q4 FY26 (quarter ended June 30, 2026) — reported July 29, 2026
Source: Microsoft press release, https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast (verified verbatim)
- Revenue **$90.0B, +18%** (+17% cc)
- Operating income **$40.6B, +18%**; operating margin **45%** (Amy Hood: "Operating margins increased slightly year-over-year to 45%")
- Net income **$35.8B, +31% GAAP**; $35.3B non-GAAP (+22%)
- Diluted EPS **$4.81 GAAP (+32%)**; **$4.74 non-GAAP (+23%)**. Non-GAAP excludes OpenAI investment effects (OpenAI impact was **-$0.07** on Q4 EPS).
- **Microsoft Cloud revenue $59.3B, +27%**; Microsoft Cloud gross margin **65%** (down YoY)
- **Azure and other cloud services +43%** (43% cc)
- **Commercial RPO $678B, +84%** ("commercial remaining performance obligation increased 84% to $678 billion"). 10-K: commercial RPO **$678B** at 6/30/26, total-company RPO **$684B**, weighted-average duration **~2.3 years**, ~30% to be recognized in next 12 months.
- **Capex including finance leases: $41B** for the quarter. Hood: "Capital expenditures were $41 billion including the impact from higher component pricing... Roughly two thirds of our capex was for short-lived assets, primarily CPUs and GPUs... This quarter, total finance leases were $5.6 billion... And cash paid for P, P, and E was $35.8 billion." CNBC: capex + finance leases of $41B "jumped 69%" YoY.
- Q4 FCF **$19.64B, -23% YoY** (CNBC); OCF $55.4B, +30%.
- Discrete items: $3.2B gain on Anthropic investment; XBOX impairment/severance; net +$0.27 to EPS vs guidance.
- Headcount -2% YoY.

### 2c. FY26 full year (ended June 30, 2026)
10-K: https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm
- Revenue **$331.839B, +18%**; operating income **$155.237B, +21%**; net income **$133.749B**; diluted EPS **$17.95**
- OCF **$182.935B** (10-K: "Cash from operations increased $46.8 billion to $182.9 billion")
- Cash additions to PP&E **$115.948B** (FY25 $64.551B)
- **FCF $66.987B** — DOWN 6.5% from FY25's $71.611B (FY24: $74.071B)
- Capex including finance leases (sum of four disclosed quarters: Q1 $34.9B + Q2 $37.5B + Q3 $31.9B + Q4 $41.0B) = **$145.3B**, i.e. **~43.8% of revenue**. (This sum is my arithmetic, not a number Microsoft published as a full-year total.)
- Capex as % of revenue: **FY26 34.9% (cash basis) / ~43.8% (incl. finance leases); FY25 22.9%; FY24 18.1%** — computed from 10-K cash-flow and income statements.
- D&A ("Depreciation, amortization, and other"): **$38.534B FY26 vs $29.433B FY25 (+31%) vs $20.958B FY24 (+40%)**. As % of revenue: 11.6% / 10.4% / 8.6%.
- Microsoft Cloud revenue **$214.4B, +27%**; MS Cloud gross margin **66%** (FY25 69%); "nearly 90% from customers outside of frontier model companies" (Hood, Q4 call).
- FY26 GAAP EPS benefited **+$0.67** from OpenAI investment gains (10-K: net gains from OpenAI investments increased net income by $5.0B / $0.67 EPS; FY25 was a **-$0.49** drag). Read: **OpenAI is currently flattering Microsoft's EPS, not bleeding through it.**
- Cash + STI fell to **$76.8B** from $94.6B a year earlier (10-K).

### 2d. Guidance given with Q4 FY26 (July 29, 2026)
From the Q4 FY26 earnings call transcript (https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4):
- FY27: "another fiscal year of double-digit revenue and operating income growth"; opex "mid to high-single digits"; **"we expect FY27 capital expenditures will grow year-over-year"**; **"full fiscal year operating margins should be down less than a point"**; **"we expect to remain free cash flow positive in FY27"**; tax rate ~20%.
- Q1 FY27: total revenue **$89.85–90.95B (+16–17%)**; COGS $29.6–29.8B (+23–24%); opex $16.8–16.9B (+7–8%); **operating margins "relatively flat year-over-year"**; **capex "over $50 billion including the lease reclassification impact"**; Azure "approximately 45% in constant currency"; Microsoft Cloud GM% "relatively stable QoQ".
- Calendar 2026 capex: **~$175B** including finance leases, revised down from ~$190B purely because of a lease-accounting change ("Outside of this useful life impact, our calendar year 2026 CapEx investment expectations remain unchanged. However, the shift from finance to operating leases adjusts our expectation to approximately $175 billion"). NB: this is a reclassification, not a cut. (The ~$190B prior figure, set in April 2026, included ~$25B from higher component prices — Q3 FY26 call and CNBC.)
- Segment guidance as re-cut on Sept 2, 2026: Agents and Infra **$75.15–75.75B**, Devices and Consumer **$14.7–15.2B** for Q1 FY27 (CNBC, Sept 2).

### 2e. Azure disclosure change — VERIFIED via primary-adjacent sources
- **Yes.** Microsoft will report an exact quarterly Azure revenue dollar figure for the first time with Q1 FY27 results, and is collapsing three reporting segments (PBP, Intelligent Cloud, MPC) into two — **"Agents and Infra"** and **"Devices and Consumer"** — the first change since 2015.
- **Recast figures disclosed by the company on Sept 2, 2026:** Azure revenue **$29.42B in the June 2026 quarter (+42% under the new definition vs +43% old)**; **$101.9B for FY26**; Azure ≈ **33% of total revenue**.
- New Azure definition **excludes** GitHub cloud services, developer cloud services, Security Copilot, and healthcare/life-sciences cloud products (Nuance). Nadella in the deck: "Under this reporting structure, Azure becomes more purely our consumption-based platform and infrastructure business."
- Q1 FY27 Azure guide under new definition: **+44–45% cc** (vs 45% cc for old "Azure and other cloud services").
- Sources: CNBC https://www.cnbc.com/2026/09/02/microsoft-to-disclose-azure-revenue-as-part-of-segment-changes.html ; Reuters https://www.reuters.com/business/retail-consumer/microsoft-reveal-azure-cloud-sales-financial-reporting-shift-2026-09-02/ . **I did not find the underlying Sept 2 investor presentation itself** — treat the $29.42B/$101.9B/segment names as verified via CNBC + Reuters reporting of that deck, not from a Microsoft-hosted PDF I opened.

### 2f. Consensus for Wednesday Oct 28 (LSEG, via CNBC Investing Club, Oct 25, 2026)
- **Revenue $90.68B; EPS $4.72.** Source: https://www.cnbc.com/investingclub/2026/10/25/here-are-4-big-things-were-watching-in-the-stock-market-this-week.html ("all revenue and earnings estimates are courtesy of LSEG").
- Cross-checks (lower quality, but consistent): MarketBeat $90.63B / $4.71; TipRanks cites Street at $90.58B / $4.71. A tickerdaily.com piece quoting $4.82/$92.46B is **wrong** (its prior-quarter "actuals" don't match the filings) — ignore it.
- Context: Q1 FY26 actual was $77.67B revenue and $4.13 non-GAAP EPS ($4.25 GAAP incl. OpenAI gains). Consensus implies ~+17% revenue, ~+14% EPS.

### 2g. Depreciation and useful lives
- 10-K (FY26) property/equipment lives, verbatim: **"software developed or acquired for internal use, three years; servers and network equipment, two to six years; buildings and improvements, five to 15 years; leasehold improvements, three to 15 years; and furniture and equipment, one to 10 years."**
- **Change effective FY27** (Q4 call): "we are extending the estimated useful lives of our datacenters and office buildings, from 15 to 25 years." Hood: "This change affects only the timing of future depreciation and is expected to have a minimal benefit to FY27 operating income." Microsoft did **not** extend server/GPU lives — the short-lived asset category (roughly two-thirds of capex) is still depreciated over short schedules.
- Same change shifts future datacenter leases from finance to operating leases, which is why the CY2026 capex number moved from ~$190B to ~$175B.
- D&A growth: FY24 $21.0B → FY25 $29.4B (+40%) → FY26 $38.5B (+31%). Revenue grew +15%, +18% over the same years. D&A/revenue has gone 8.6% → 10.4% → 11.6%.
- Quarterly D&A prints from yfinance (`Reconciled Depreciation`, $B): 13.061 (Sep-25), 9.198 (Dec-25), 10.167 (Mar-26), 11.022 (Jun-26). **These four do not sum to the audited $38.534B annual figure — the quarterly series is unreliable; use the annual numbers.** (UNVERIFIED at quarterly granularity.)

### 2h. Microsoft's OpenAI exposure
Primary sources: Microsoft blog Oct 28, 2025 https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ ; OpenAI https://openai.com/index/next-chapter-of-microsoft-openai-partnership/ ; Microsoft FY26 10-K Note 1/Note 4; Microsoft FY25 10-K R26 (SEC).
- **Oct 2025 restructuring:** OpenAI formed a public benefit corporation (OpenAI Group PBC) and completed a recapitalization. "Following the recapitalization, Microsoft holds an investment in OpenAI Group PBC **valued at approximately $135 billion, representing roughly 27 percent on an as-converted diluted basis**" (32.5% before the recent funding rounds). Reuters, Oct 28, 2025, headline confirms "Microsoft holds 27% stake in OpenAI Group PBC."
- **Azure commitment: "OpenAI has contracted to purchase an incremental $250B of Azure services, and Microsoft will no longer have a right of first refusal to be OpenAI's compute provider."** ($250B is the incremental commitment, not total lifetime — do not write "$250B total".)
- **Revenue share:** "The revenue share agreement remains until the expert panel verifies AGI, though payments will be made over a longer period of time." (i.e., the same total, spread over more years.)
- IP: extended through 2032, now includes post-AGI models; excludes consumer hardware; API products built with third parties remain Azure-exclusive, non-API products can run anywhere.
- **By June 30, 2026 the stake had diluted:** 10-K says the equity-method investment "represents an **approximate 25% interest on an as-converted basis**," and FY26 ownership fell "due to the OpenAI Recapitalization and other funding activity," producing dilution gains.
- **Scale of the commercial relationship (10-K, Note — related party):** "For fiscal year 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of **$24.1 billion**, and accounts receivable from OpenAI as of June 30, 2026 was **$6.0 billion**." Total funding commitments **$13.0B**, of which **$11.9B** funded.
- **Concentration disclosure:** "Microsoft said in January that around **45% of its $625 billion in commercial remaining performance obligations were tied to OpenAI**" (CNBC, July 29, 2026, citing the Q2 FY26 call). ~$281B of the then-$625B.
- Hedge against that: Q4 FY26 RPO commentary — "All sequential commercial RPO growth was driven by commitments from customers outside of frontier model companies. And **RPO increased 25% when excluding OpenAI**." (vs +84% headline.)

---

## 3. INDUSTRY CONTEXT

**Meta's negative FCF and record CDS (week of Oct 19–23, 2026)**
- Meta reported Q3 on Oct 21–22; **free cash flow -$2.12B**, "turning cash flow negative for the first time since 2012" (Reuters, Oct 22) / "for the first time ever going back to its public debut" (CNBC).
- Meta raised the low end of 2026 capex to **$135–145B** (from $130–145B).
- **Five-year CDS widened 7.6bp to a record 114.79bp** (Markit data via Reuters, Oct 22). CNBC the next day put it at "over 124 basis points" — two different prints on two different days; cite the Reuters 114.79bp figure for the record-widening day and note CNBC's >124bp the following day.
- Meta also disclosed ~$825B of future leases/contracts, over $450B of them non-cancellable take-or-pay (CNBC, Oct 23).
- Stock fell ~7% on the day, >9% on the week (CNBC).
- CDS records elsewhere that week: **Nvidia 126bp, Oracle 343bp**; CoreWeave CDS past 11% ("distress level"); Oracle stock down more than one-third YTD and facing downgrade risk (CNBC, Oct 23: https://www.cnbc.com/2026/10/23/ai-turmoil-neoclouds-struggle-credit-risks-jump-solidigm-pulls-ipo.html). SK Hynix cancelled Solidigm's IPO citing market conditions.

**October semis/memory drawdown**
- CNBC week-ahead (Oct 23, 2026): "**Semiconductors have been crushed, down more than 15% this month. Memory stocks plunged more than 20%.** The Magnificent Seven companies are down more than 2%. But software stocks, and cybersecurity names in particular, are set to end the month with gains." Nasdaq was set to close October down more than 3%.
- SOX specifics: Philadelphia Semiconductor Index fell 3.83% to 11,137.29 on Oct 16, its **eighth straight decline — longest losing streak since October 2008** — and had "lost 16% since its last advance on October 6" (Investing.com, Oct 17). Trigger mix: AI financing costs, hotter inflation, and China's CXMT reporting a memory-density architecture advance (Reuters Oct 13; CNBC Oct 13/15). 20 of the largest global AI/semi names shed **more than $1 trillion in market value in the week to Oct 15** (CNBC).
- Nasdaq's worst session: the Oct 16 Friday decline of **-2.1%** was the sharpest single day in the stretch (Investing.com). [The brief that says "worst session since June" — I could not verify that exact superlative from a primary/major-wire source. UNVERIFIED as phrased.]

**2026 hyperscaler capex totals**
- Combined 2026 capex across the big four: **roughly $720–745B** based on latest company guidance — Amazon ~$220B, Alphabet $195–205B, Microsoft ~$175B (post-reclass), Meta $135–145B (compiled from company guidance; CNBC July 28 and Reuters). Reuters, Oct 23, 2026: "Capital spending from hyperscalers, **expected to be around $800 billion this year**."
- 2027: Evercore ISI's Mark Mahaney models **~$1 trillion** from just Google, Amazon, Meta and Microsoft (Yahoo Finance video, July 23, 2026: Google and Amazon "300 billion at a minimum" each, Meta ~$200B, Microsoft "at least 200 billion").

**Mahaney's "$100B more" call**
- CNBC, Oct 23, 2026 (week-ahead, by-line piece): "That has added to fear that the hyperscalers reporting next week will also disclose news of heightened capital spending, **perhaps by as much as $100 billion, according to Mark Mahaney, who heads Evercore's Internet research team**." He added that "the market fear is now in the stock," and that Alphabet was down >5% on the week while Amazon and Microsoft were each down ~1%. Source: https://www.cnbc.com/2026/10/23/next-week-brings-major-risks-for-the-stock-market-just-as-the-ai-trade-keeps-faltering.html

---

## 4. STRONGEST BEAR CASE (short-seller grade)

**Thesis: Microsoft is converting an 84%-growth backlog into revenue at a slower rate than depreciation and capex are compounding, and the backlog is concentrated in a single, loss-making counterparty that is no longer contractually tied to Azure.**

The specific markers, with actual numbers:

1. **FCF is already going backwards while revenue accelerates.** FY26 revenue +18%, but FCF **-6.5% to $67.0B** (from $71.6B), the second consecutive annual decline (FY24 $74.1B). Q4 FCF **-23% YoY to $19.6B**. Capex incl. finance leases reached **$145.3B, ~44% of revenue**, vs 23% in FY25 and 18% in FY24. Microsoft has guided FY27 capex to **grow again** — and Q1 FY27 capex alone is guided **">$50B"** vs $41B in Q4, which annualises above $200B against a $90.7B quarterly revenue base.
   *What proves the bears right:* FY27 FCF (ex-lease-adjusted) below FY26's $67B, or FCF margin below ~15%. Watch the "we expect to remain free cash flow positive in FY27" line — "positive" is a very low bar that management chose to set explicitly.

2. **Depreciation is outrunning revenue and margins are already cracking.** D&A $21.0B → $29.4B → $38.5B (FY24→FY26, +84% cumulative) vs revenue +35%. D&A is now 11.6% of revenue vs 8.6% two years ago. Company gross margin fell to **67% in Q4** and **Microsoft Cloud gross margin to 65%** (from 69% in FY25, 68% in Q4 FY25) — the AI mix is dilutive. FY27 guide: operating margin "down less than a point."
   *The tell:* extending building lives from 15 to 25 years is an accounting change that lowers future depreciation. It arrives in the same quarter management is guiding to a >$50B capex quarter. If D&A/revenue keeps rising *after* a life extension, the underlying asset base is compounding faster than the business.

3. **The backlog is one customer.** At Q2 FY26, **~45% of the $625B commercial RPO was tied to OpenAI** (~$281B). Headline RPO growth was +84%, but **RPO ex-OpenAI grew only 25%**. Duration is 2.3 years with only ~30% recognised in the next 12 months, so the "backlog" is mostly a promise about 2027–2029.
   *What proves the bears right:* a quarter where RPO ex-OpenAI growth decelerates below ~20%, or where Microsoft discloses that OpenAI's share of RPO has risen rather than fallen. Note also that OpenAI's $250B incremental Azure commitment came with Microsoft **giving up its right of first refusal** to be OpenAI's compute provider — the backlog is no longer defended by exclusivity.

4. **Earnings quality: the OpenAI line is currently a subsidy.** FY26 GAAP EPS of $17.95 included **+$0.67** from OpenAI-related gains (a $5.0B net gain, "primarily... the dilution gain from the OpenAI Recapitalization" — a non-cash mark). Strip it and FY26 EPS is ~$17.28. In Q4 the OpenAI impact was **-$0.07**, i.e., the sign already flipped once. FY25 was **-$0.49**.
   *What proves the bears right:* OpenAI-related losses returning to the equity-method line in a quarter where Azure decelerates — FY25 shows exactly what that looks like (-$3.6B / -$0.49).

5. **Azure decelerated twice inside FY26 before re-accelerating on capacity timing.** Azure growth: Q1 40% → Q2 39% → Q3 40% → Q4 43%; FY26 41%. The company itself attributes the Q4 acceleration to "efficiency gains across our CPU and GPU fleet as well as process improvements to enable earlier delivery of new capacity" — i.e., supply timing, not demand. Under the new (narrower) definition Azure grew **42%** in Q4, not 43%.
   *The line in the sand:* guidance is **44–45% cc for Q1 FY27**. Anything below ~44% breaks the acceleration story on the first print under the new disclosure regime, in the same week Meta burned cash. Q1 is also the quarter where Microsoft must show Azure's absolute dollars alongside the growth rate for the first time — an optically smaller, slower business than "Azure and other cloud services" was.

6. **Balance-sheet drift.** Cash + short-term investments fell to **$76.8B from $94.6B**; net debt is **$19.4B** (from $12.9B a year ago); interest expense is rising because of "higher finance lease interest expense" (10-K). Total debt $56.8B on the balance sheet. Not distressed — but the direction is the same one that took Meta's CDS to a record.

7. **Legacy businesses are shrinking into the story.** FY27 guidance: Windows OEM and Devices revenue to **decline high-teens**; M365 Commercial products and Server products each to **decline mid-single digits**. So all growth must come from Azure and Copilot, at lower gross margin.

---

## 5. BULL CASE (brief) + confirming numbers

- **Azure is accelerating at $100B+ scale.** FY26 Azure $101.9B (+41%); Q4 +43% (42% new basis); Q1 FY27 guided **+44–45% cc** — acceleration, not deceleration. Wedbush-adjacent sell side is above that: Wells Fargo's Michael Turrin models **~46% cc** for Q1 and ~46% for Q2 (TipRanks, Oct 2026).
- **Backlog quality is improving even as the headline slows.** $678B commercial RPO at 6/30/26, +84%; "all sequential commercial RPO growth was driven by commitments from customers outside of frontier model companies"; Microsoft Cloud revenue $214.4B with "nearly 90% from customers outside of frontier model companies." Ex-OpenAI RPO still +25%.
- **Copilot is inflecting on seats and price.** **30M+ paid M365 Copilot seats**, net paid seat adds **more than doubled QoQ**; customers with >50,000 seats up **7x YoY**; E7 (Copilot+E5+Entra+Agent 365) sold "millions of seats" to "hundreds of enterprise customers" in two months, including EY at 400,000 seats; GitHub Copilot at 50M users; AI business ARR **$37B, +123%** (Q3 FY26).
- **Cash generation is still enormous.** $67B of FCF, $182.9B of OCF, and management guides FCF-positive FY27 while funding a $175B+ capex programme internally plus $43B of shareholder returns.
- **Valuation is not stretched for the growth.** 22.1x forward EPS vs 29.2x trailing; 53 analysts at "strong buy," mean target $601.73 (+14.7%).
- **Unit economics may improve from here:** Maia 200 claims "30% better performance per dollar than the latest generation hardware in our fleet today," with Maia scaled to multi-gigawatt deployments from 2027 — the only real lever on gross margin in the model.

**Numbers that would confirm the bull case on Wednesday:** Azure ≥45% cc (new definition, absolute dollars ≈$30–31B); capex guide for FY27 that grows slower than revenue; RPO above $700B with ex-OpenAI growth ≥25%; Copilot seats ≥35M; FY27 operating margin guide no worse than "down less than a point"; and any statement that FY27 FCF grows rather than merely stays positive.

---

## 6. SOURCES (all fetched or confirmed to exist)

| URL | Supports |
|---|---|
| https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast | Q4 FY26 & FY26 revenue/op income/net income/EPS, MS Cloud $59.3B +27%, Azure +43%, RPO $678B +84%, Copilot 30M seats, Azure >$100B FY26 |
| https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4 | Q4/FY26 call transcript: capex $41B, finance leases $5.6B, cash PP&E $35.8B, FCF $19.6B, OCF $55.4B, 15→25yr life change, CY26 capex ~$175B, all FY27/Q1 FY27 guidance, RPO ex-OpenAI +25%, MS Cloud ~90% non-frontier |
| https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/metrics | Quarterly KPI table: RPO $368→$392→$625→$627→$678B; Azure growth 39/40/39/40/43%; MS Cloud GM 68/69/68/67/66/65% |
| https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm | FY26 10-K: revenue $331.8B, OCF $182.9B, PP&E $115.9B, D&A $38.5B, cash+STI $76.8B, RPO $678B/$684B & 2.3yr duration, useful lives (servers 2–6 yrs), OpenAI ~25% as-converted, $24.1B OpenAI revenue, $6.0B OpenAI AR, $13.0B/$11.9B funding, +$5.0B/+$0.67 OpenAI gains |
| https://www.cnbc.com/2026/07/29/microsoft-msft-q4-earnings-report-2026.html | Q4 capex+leases $41B "+69%", FCF $19.64B -23%, "45% of $625B RPO tied to OpenAI" (Jan disclosure), Azure FY26 >$100B +41%, IC segment $39.31B vs $38.16B consensus, 45% Q1 Azure guide, life extension |
| https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3 | Q3 FY26 capex $31.9B (finance leases $4.7B, cash PP&E $30.9B), CY2026 capex guide ~$190B incl ~$25B component pricing, Azure +40%, AI business $37B ARR +123% |
| https://www.cnbc.com/2026/04/29/microsoft-msft-q3-earnings-report-2026.html | Q3 capex+leases $31.9B +49% vs $34.9B consensus; gross margin 67.6% narrowest since 2022; $190B 2026 capex = +61% vs 2025 |
| https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2 | Q2 FY26 capex $37.5B, finance leases $6.7B, cash PP&E $29.9B, FCF $5.9B, RPO $625B +110%, "approximately 45% of our commercial RPO balance is from OpenAI", Azure +39% |
| https://www.cnbc.com/2026/01/28/microsoft-msft-q2-earnings-report-2026.html | Q2 capex+leases $37.5B +66% vs $34.3B consensus; 15M Copilot seats at that point; Azure +39% |
| https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q1 | Q1 FY26 capex $34.9B incl $11.1B finance leases, cash PP&E $19.4B, OCF $45.1B, FCF $25.7B |
| https://www.cnbc.com/2026/09/02/microsoft-to-disclose-azure-revenue-as-part-of-segment-changes.html | Azure $29.42B June qtr (+42% new def), Azure ~33% of revenue, segments collapse to Agents and Infra / Devices and Consumer, Azure excludes GitHub/Security Copilot/Nuance, Q1 Azure guide 44–45% cc |
| https://www.reuters.com/business/retail-consumer/microsoft-reveal-azure-cloud-sales-financial-reporting-shift-2026-09-02/ | Azure $29.4B quarterly / $101.9B FY26, first-ever dollar disclosure, slight Azure forecast cut after GitHub reclass |
| https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ | Primary: 27% stake (~$135B), $250B incremental Azure commitment, loss of right of first refusal, revenue share extended over longer period, IP to 2032 |
| https://openai.com/index/next-chapter-of-microsoft-openai-partnership/ | Same terms from OpenAI's side (verbatim bullet list) |
| https://www.reuters.com/business/microsoft-openai-reach-new-deal-allow-openai-restructure-2025-10-28/ | Wire confirmation: "Microsoft holds 27% stake in OpenAI Group PBC" |
| https://blogs.microsoft.com/blog/2026/10/12/microsoft-to-expand-azure-maia-system-to-multi-gigawatt-deployments/ | Maia 200 in production, Maia 300 in 2027, multi-gigawatt, primary inference system, 40% more tokens/MW |
| https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/ | Maia 200 specs, "30% better performance per dollar than the latest generation hardware in our fleet today", runs GPT-5.2 |
| https://www.cnbc.com/2026/10/23/next-week-brings-major-risks-for-the-stock-market-just-as-the-ai-trade-keeps-faltering.html | Week-ahead: 163 S&P reporters; Meta -9% week; semis -15% Oct, memory -20%; Mahaney "$100 billion" more capex; Nasdaq -3% Oct; Alphabet/Amazon/MSFT reporting dates |
| https://www.cnbc.com/2026/10/25/here-are-4-big-things-were-watching-in-the-stock-market-this-week.html | **LSEG consensus: MSFT revenue $90.68B, EPS $4.72**; "we'll also start to get an exact quarterly revenue figure, not just the growth rate"; RPO $678B +84% at end-June |
| https://www.cnbc.com/2026/10/22/meta-stock-q3-earnings-free-cash-flow.html | Meta FCF -$2.12B, capex floor raised to $135B, 5yr CDS all-time high, stock -7% |
| https://www.investing.com/news/stock-market-news/meta-falls-as-investors-balance-muse-growth-with-rising-ai-costs-4965902 (Reuters syndication) | Meta 5yr CDS record 114.79bp (+7.6bp), Markit data, first cash burn in more than a decade |
| https://www.streetinsider.com/Reuters/Metas+credit+risk+indicator+hits+record+high+on+increased+AI+spending+plan/27220533.html | Reuters: FCF deficit $2.12B, "turning cash flow negative for the first time since 2012" |
| https://www.cnbc.com/2026/10/23/ai-turmoil-neoclouds-struggle-credit-risks-jump-solidigm-pulls-ipo.html | Meta 5yr CDS ">124bp", Nvidia 126bp, Oracle 343bp, CoreWeave CDS >11%, Solidigm IPO pulled, Meta ~$825B leases / $450B take-or-pay |
| https://www.investing.com/news/stock-market-news/chip-index-sox-posts-longest-losing-streak-since-2008-as-ai-worries-deepen-4955401 | SOX -3.83% to 11,137.29 Oct 16, 8 straight losses (longest since Oct 2008), -16% since Oct 6, Nasdaq -2.1% that day |
| https://www.cnbc.com/2026/10/15/sk-hynix-samsung-softbank-stocks-asia-tech-rout-ai-funding-worries.html | 20 largest global AI/semi names shed >$1tn in value in the week to Oct 15; SK Hynix -10%+, Samsung -8.7% |
| https://www.investing.com/news/economy-news/earnings-flood-fed-meeting-will-test-rickety-ai-market-rally-4971185 (Reuters) | Hyperscaler capex "around $800 billion this year"; Alphabet and Microsoft report Wednesday, Amazon Thursday |
| https://www.cnbc.com/2026/07/28/hyperscalers-face-higher-capex-scrutiny-after-alphabet-report-panned.html | Per-company 2026 capex guides (AMZN ~$207–220B, GOOGL $205B top end, MSFT $190B April guide incl $25B component pricing, META $138.9B); Mahaney on "similar behavior" |
| https://www.tipranks.com/news/microsoft-stock-msft-why-wells-fargo-is-bullish-ahead-of-q1-2027-earnings | Wells Fargo Turrin: Azure +46% cc expected for Q1, PT $700→$725; Street $90.58B/$4.71; Azure new definition excludes Nuance/Security Copilot/GitHub |

---

## 7. CORRECTIONS TO THE BRIEFING I WAS GIVEN
- **"~27% stake" is only true as of Oct 2025.** The FY26 10-K (June 30, 2026) states **~25% on an as-converted basis**, after dilution from the recapitalization and later funding. Use "about 27% at the October 2025 restructuring, diluted to roughly 25% by June 2026."
- **"$678B, +84%" is correct** but is *commercial* RPO; total-company RPO is $684B. Growth ex-OpenAI is **+25%**, and at Q2 ~45% of RPO was OpenAI. The 84% is not an organic number.
- **Microsoft's OpenAI exposure is currently a GAAP earnings *tailwind*, not a drag** (+$0.67 to FY26 EPS). Any bear case built on "OpenAI losses flowing through the equity method" is factually wrong for FY26 — the honest version is "the sign has already flipped once (Q4 -$0.07; FY25 -$0.49), so the tailwind is not durable."
- **"Capex cuts to $175B" is a lease-accounting reclass, not a cut.** Total spending expectation unchanged; the reduction is because more future datacenter leases now sit in operating rather than finance leases.
- **Unverified claims:** the "Nasdaq's worst session since June" superlative (I verified a -2.1% Nasdaq day on Oct 16 and a -3% October, but not that specific ranking); quarterly D&A figures (yfinance series doesn't foot to the audited annual); the Sept 2 Azure recast deck itself (cited via CNBC and Reuters).
