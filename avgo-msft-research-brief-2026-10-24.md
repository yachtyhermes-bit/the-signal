# AVGO + MSFT — Research Brief
**Prepared for The Signal · Saturday, October 24, 2026 · Analyst: Nelly**
Prices = Friday, October 23, 2026 close. Financials = freshest reported quarter + TTM computed from quarterly statements.

**Central tension, stated up front:** these two are the same trade told at opposite points in the cycle. AVGO's fundamentals are accelerating faster than any large-cap in the market and its stock is down 33% from June. MSFT's fundamentals are decelerating on the metric that matters (free cash flow) and its stock is 3.5% off an all-time high. Both gaps come down to one question: who pays for the buildout, and who eats it if the answer is wrong.

---

# 1. BROADCOM (AVGO)

## 1.1 What it does, in plain English
Broadcom designs the custom AI chips that a handful of the largest technology companies order to their own specifications — plus the high-speed networking that connects those chips into working clusters — and separately sells the infrastructure software (VMware, mainframe tools, Symantec) that runs big corporate data centers.

## 1.2 Its exact role in the AI buildout
Broadcom is the **merchant alternative to Nvidia for hyperscaler-owned silicon**. When a company decides it does not want to buy Nvidia GPUs at Nvidia's price, it hires Broadcom to co-design an application-specific accelerator (an "XPU") tuned to its own model architecture, then manufactures it at TSMC. Broadcom also supplies the Ethernet/networking fabric that makes thousands of those chips behave as one computer.

Named XPUs shipping as of the September 2 earnings call:
- **Google** — TPU v7 "Ironwood" in high volume, TPU v8i ramping (Broadcom says it shipped v8i *ahead of* MediaTek's competing v8T design)
- **Anthropic** — Ironwood TPU v7 in high volume; accelerating shipments in the December quarter
- **OpenAI** — "Jalapeño," OpenAI's first-generation custom accelerator
- **Meta** — MTIA accelerator optimized for inference and recommendation, entering production shipment in the December quarter

Broadcom says it has **six XPU customers** total; the other two are not publicly named. AI semiconductors were **56% of total company revenue** in the August quarter, up from 49% in the prior quarter.

## 1.3 THE NEAR-TERM CATALYST

**Fiscal Q4 2026 and full-year results — Wednesday, December 9, 2026, after market close.**
Conference call 2:00 p.m. Pacific / 5:00 p.m. Eastern.

Verified from the company: closing the Q3 call, Broadcom's head of investor relations Ji Yoo said verbatim, *"Broadcom currently plans to report its earnings for the fourth quarter and fiscal year 2026 after close of market on Wednesday, December 9, 2026."* (Motley Fool transcript of the Sept 2, 2026 call.)

- Dec 9, 2026 **is a Wednesday**. Confirmed by calendar arithmetic and by the company's own wording.
- **Caveat worth flagging for the fact-checker:** several aggregators list **Dec 10** (TipRanks labels it "Confirmed"; FinanceCalendar and MarketBeat list Dec 10 for the call). Broadcom has **not yet issued a formal press-release date notice** — historically it does so ~4 weeks ahead, so expect one in early November. If a hard date is needed for publication, write "December 9 (company guidance on the Q3 call; formal notice pending)" rather than asserting it as announced.
- Precedent that the call's stated date holds: on the Q2 call Broadcom named Wednesday, September 2 — and reported September 2.

**What the quarter must clear (company's own guide, from the Sept 2 release):**
| Metric | Q4 FY26 guide | Implied YoY |
|---|---|---|
| Revenue | ~$34.8B | +93% |
| Non-GAAP operating margin | ~66% of revenue | flat YoY |
| AI semiconductor revenue | $21.7B | +236% |

Consensus sits slightly above the guide: ~$34.90B revenue and $3.83 non-GAAP EPS (yfinance analyst aggregate, 2026-10-24); LSEG had expected a $35.03B guide.

**Secondary dated catalysts:**
- **Fiscal year 2026 ends November 1, 2026** — the December print closes the year at ~$58B of AI revenue (+186%), which management has already raised from a prior $56B guide.
- **Anthropic IPO** — bankers are reportedly targeting ~$100B of proceeds at a ~$2T valuation, which would be the largest IPO ever. This is the single biggest swing factor for AVGO's receivables quality (see bear case). Not yet priced, not yet dated.

## 1.4 THE NUMBERS

### Freshest quarter — Q3 FY2026, ended August 2, 2026 (reported Wed, Sept 2, 2026)
Source: Broadcom press release + 10-Q.

| | Q3 FY26 | Q3 FY25 | Change |
|---|---|---|---|
| Revenue | $29.591B | $15.952B | **+86%** |
| GAAP operating income | $15.955B | $5.887B | +171% |
| Non-GAAP operating income | $20.095B | $10.455B | +92% |
| GAAP diluted EPS | $2.68 | $0.85 | +215% |
| Non-GAAP diluted EPS | $3.32 | $1.69 | +96% |
| Operating cash flow | $14.197B | $7.166B | +98% |
| Capex | $0.532B | $0.142B | — |
| Free cash flow | $13.665B | $7.024B | +95% |

- **FCF was 46.2% of revenue** — a record. Non-GAAP operating margin 67.9%, up 240bp YoY.
- Segment split: **Semiconductor Solutions $20.839B (+127%)**, 70% of revenue; **Infrastructure Software $8.752B (+29%)**, 30%.
- Sequential revenue growth was **+33%** ($22.187B → $29.591B). That is not a typo and is the single most striking number in either company's report.
- Cash and equivalents $24.0B, up $4.3B QoQ. Repurchased $5.641B of senior notes in the quarter.

### TTM (newest quarter + prior three, computed from quarterly statements — not taken from a data-provider field)
| Metric | TTM |
|---|---|
| Revenue | **$89.10B** |
| Gross profit / margin | $61.28B / **68.8%** |
| Operating income / margin | $43.24B / **48.5%** (GAAP) |
| Net income / margin | $38.27B / **42.9%** |
| R&D | $11.84B (13.3% of revenue) |
| Operating cash flow | $40.65B |
| Capex | $1.25B (**1.4% of revenue**) |
| **Free cash flow** | **$39.40B (44.2% margin)** |
| Stock-based comp | $8.48B (9.5% of revenue) |
| FCF less SBC | $30.92B |
| Dividends + buybacks | $20.53B |

The 1.4%-of-revenue capex line is the structural point: Broadcom is fabless and outsources manufacturing to TSMC, so incremental AI revenue converts to cash at roughly 44 cents on the dollar. There is no fab to finance.

### Backlog / RPO — the number to quote precisely
From the 10-Q: **remaining performance obligations of approximately $179.2 billion** as of August 2, 2026, of which **only ~25% is expected to be recognized as revenue over the next 12 months.**

Broadcom's own footnote on that figure is unusually candid and should temper how it is described: the RPO number *"is not indicative of revenue for future periods"* because it excludes contracts terminable for convenience, contracts under one year, and usage-based royalties.

### Guidance ladder (management's, from the Sept 2 call)
- FY2026 AI semiconductor revenue: **$58B** (+186%), raised from $56B
- FY2027 AI semiconductor revenue: **~$115B** (raised from "over $100B"), supply secured
- FY2028 AI semiconductor revenue: **~$230B**, supply secured
- FY2028 non-GAAP EPS: management says it is **"on target to exceed $30"**

### Capital return
Quarterly dividend **$0.65/share** ($2.60 annualized, ~0.81% yield), declared for payment Sept 30, 2026. TTM payout $12.08B, ~32% of GAAP EPS.

## 1.5 THE STOCK'S CURRENT STATE (relative, not absolute)

| | Value |
|---|---|
| Last close (Oct 23, 2026) | $321.68 |
| 52-wk **closing** high | $481.57 (June 2, 2026) → **−33.2%** |
| 52-wk **intraday** high | $495.00 (June 3, 2026) → **−35.0%** |
| 52-wk low | $289.96 (intraday, March 30, 2026) → +10.9% above |
| 50-day SMA | $356.76 → price **−9.8% below** |
| 200-day SMA | $367.82 → price **−12.5% below** |
| Forward P/E | **16.6x** (FY27E EPS $19.43) |
| Trailing GAAP P/E | 41.1x |
| EV/EBITDA (TTM) | 30.1x |
| P/S (TTM) | 17.2x |

**The multiple has collapsed while earnings exploded.** Trailing GAAP P/E was 77.5x at FY2025 year-end and 49.7x as recently as July 31, 2026; it is 41.1x now on a stock down a third. On forward earnings AVGO trades at 16.6x — roughly **half of AMD (32.8x) and Marvell (31.2x)**, in line with TSMC (17.9x) and Qualcomm (17.3x), and above only Nvidia (13.3x) among large-cap AI semis. **Year-to-date the stock is down 7.1%** (2025 close $346.10), against a market that is up double digits — so the drawdown is not merely a pullback from a June spike.

**Peer forward P/E (yfinance, Oct 24, 2026):** NVDA 13.3 · **AVGO 16.6** · QCOM 17.3 · TSM 17.9 · META 18.5 · GOOGL 20.8 · **MSFT 22.1** · AMZN 23.8 · MRVL 31.2 · AMD 32.8 · ORCL 11.5 · MU 4.2

Technical read: the stock broke below its 200-day in mid-October and has not reclaimed it. It is in a downtrend on every intermediate measure while printing record results — a classic "multiple de-rating, not an earnings problem" setup, which is either the opportunity or the trap depending on the bear case below.

## 1.6 RECENT NEWS THAT MATTERS (last three weeks)

- **Oct 23 — NTT DOCOMO signs a 10-year VMware agreement.** Covers software licenses, maintenance and technical support; relationship dates to 2019; framed around preparing VMware Cloud Foundation for AI workloads. **Financial terms not disclosed** — no ACV, no earnings contribution. (Yahoo Finance / GuruFocus wire, Oct 23.)
- **Oct 22 — stock fell 4.3%** ($337.80 → $323.24) in a broad AI/semiconductor selloff tied to rising Treasury yields and the financing narrative below. Nasdaq and AI hardware names fell together; ORCL and AMD were hit harder on Oct 14.
- **Oct 14 — stock fell 3.1%** to $346.25 after CEO Hock Tan's remarks at the DBS Asia Future Forward Conference in Singapore (Monday, Oct 12) that **capital, not chips or power, may be the binding constraint on AI growth**, and that some AI investing "has come to resemble gambling" / "almost like they are in a casino." He simultaneously said demand for compute exceeds what Broadcom can supply and the imbalance could persist through 2029–2030.
- **Oct 1 — Reuters exclusive:** Broadcom agreed to lend Anthropic **up to $42 billion** to finance infrastructure, revealed in Anthropic's confidential IPO filing. Anthropic could become Broadcom's largest chip-design customer next year.
- **Oct 1 (same filing, via Reuters):** Anthropic carries **~$161.2B in Broadcom-related equipment lease obligations** within ~$518B of total compute commitments.

## 1.7 ANALYST CONTEXT

- **Consensus: Strong Buy** — mean recommendation 1.27 across **48 analysts**.
- **Mean price target $529.10; median $537.50** (+64.5% vs $321.68). Range **$660 high / $215.88 low** — an extreme 3x spread that itself signals genuine disagreement about the credit risk.
- (Google Finance's narrower 30-analyst panel shows a $522 average and a $350 low, excluding the outlier bear.)

**Notable recent target changes (firm + analyst + date):**
| Date | Firm | Analyst | Action | Target |
|---|---|---|---|---|
| Oct 22, 2026 | Tigress Financial | Ivan Feinseth | **Initiated Buy** | $600 |
| Oct 2, 2026 | UBS | Timothy Arcuri | Reiterated Buy | $470 |
| Sep 22, 2026 | Bernstein | Stacy Rasgon | Reiterated Buy | $575 |
| Sep 15, 2026 | Mizuho | Vijay Rakesh | Maintained Buy | $530 |
| Sep 10, 2026 | Piper Sandler | David O'Connor | Initiated Buy | $460 |
| Sep 4, 2026 | D.A. Davidson | Gil Luria | Maintained **Hold** | $350 |
| Sep 3, 2026 | J.P. Morgan | Harlan Sur | Reiterated Buy | $580 |
| Sep 2, 2026 | Robert W. Baird | Tristan Gerra | Maintained Buy | $630 |

## 1.8 THE STRONGEST BEAR CASE

> **"Broadcom stopped selling chips and started underwriting its customers. The revenue is real; the cash collection is not yet."**

A short seller's argument, in order:

1. **The company is now a lender to its own buyers.** In the August quarter Broadcom stood up the **AI XPV platform** with private-credit partners (Apollo, Blackstone) — a $35B initial tranche that buys Broadcom-designed AI racks and leases them to a frontier lab, sized to enable **more than 20 GW** of capacity through 2028.
2. **Broadcom wrote a backstop on the lease.** From the 10-Q, verbatim: if the customer defaults, Broadcom's liability equals the gap between **85% of the outstanding lease balance** and the value recovered on resale of the racks. **Maximum potential liability: approximately $29 billion, undiscounted.** Remedies are limited to assuming the lease, reselling racks back to the seller at a fixed price, or arranging a sale.
3. **There is a second, larger contingent facility.** The customer may issue Broadcom **up to $42 billion of convertible promissory notes**, restricted to paying lease obligations. **None had been issued as of August 2, 2026.**
4. **Broadcom marked all of this at "not material."** Its own fair-value conclusion on the $29B backstop is that it is immaterial, justified by *"the strong profitability trajectory of the leading frontier AI labs and the sustaining value of the underlying assets."* That is a judgment, not a fact — and it is the judgment a short seller is betting against.
5. **The counterparty is a company with $4.6B of 2025 revenue against a $42B net loss.** Per the IPO filing as reported: Anthropic holds ~$518B of compute commitments (~80% non-cancelable, ~$161.2B of it Broadcom-related) against ~$20.28B of cash. Depreciation on purpose-built racks for a proprietary architecture has essentially no secondary market — the "sustaining value of the underlying assets" assumption is the weakest link in the chain.
6. **Concentration makes the exposure non-diversifiable.** One distributor accounted for **50% of Q3 net revenue**, up from **32%** a year earlier. Top five end customers: **55%**, up from **40%**. Distributors overall: 56% of revenue for the nine months.
7. **The $179.2B backlog is a promise with a 25% near-term conversion rate.** If customers cannot clear their own debt hurdles, the backlog is a wishlist — and the RPO footnote says as much.

**What would prove the short right (the falsifiable triggers):**
- Any amount **drawn under the $29B backstop**, or the disclosed fair value moving off "not material" to a number in a future 10-Q. This is the cleanest single tell — it appears in every quarterly filing.
- A missed or restructured Anthropic lease payment, or an Anthropic IPO that prices well below the ~$2T target (starving the funding source for the $161.2B of leases).
- **Q4 revenue below $34.8B, or AI semiconductor revenue below $21.7B** on December 9. The guide implies +93% and +236% respectively; anything less is a demand crack at the exact moment the backstop matters most.
- FY2027 AI revenue tracking below the $115B "supply secured" number — management has pre-committed to it publicly, twice.

**Secondary bear (technical/competitive):** Google is dual-sourcing. On the Q3 call Tan noted Broadcom shipped TPU v8i *ahead of MediaTek's v8T*, which was initiated earlier in Q3 — i.e., Broadcom is publicly racing a lower-cost rival for its largest customer's next-generation socket. A six-customer XPU business where one customer is ~half of revenue and is actively qualifying a second supplier is a margin story waiting to break.

---

# 2. MICROSOFT (MSFT)

## 2.1 What it does, in plain English
Microsoft rents out computing power and AI models through its Azure cloud, sells subscriptions to Office, Windows, Teams and the Copilot AI assistant, and owns roughly a quarter of ChatGPT's maker, OpenAI.

## 2.2 Its exact role in the AI buildout
Microsoft plays **two roles at once, and they pull in opposite directions**:

1. **Landlord / utility.** Azure is the largest commercial seller of AI compute after AWS. Azure passed **$100B of annual revenue for the first time in FY2026** (+41%), and Microsoft Cloud hit **$214.4B** for the year (+27%). It rents capacity to everyone, including its own part-owned model lab.
2. **Chip designer, to lower its own bill.** Microsoft announced the **Maia 300** on Monday, October 12 — its third-generation custom AI chip — and said it plans to deploy **potentially more than a million units next year** in "multi-gigawatt deployments." Racks hold 96 Maia 300 chips at ~167 kW, versus 72 Nvidia GPUs at ~142 kW for a GB300 rack; Microsoft claims **~40% more useful compute per megawatt** than "leading GPU-based systems" (it did not name the comparison). This is a direct cost-of-goods play against Nvidia.

It also carries the single largest strategic stake in a frontier lab: **~27% of OpenAI**, with joint IP rights preserved **through 2032**. An April 27, 2026 amendment ended exclusivity — OpenAI can now sell through any cloud, and its revenue share to Microsoft runs through 2030 under a cap.

## 2.3 THE NEAR-TERM CATALYST

**Fiscal Q1 2027 results — Wednesday, October 28, 2026, after market close.**
Conference call 2:30 p.m. Pacific / 5:30 p.m. Eastern.

**This is company-confirmed, not estimated.** Microsoft's own newsroom, Oct 7, 2026: *"Microsoft Corp. will publish fiscal year 2027 first-quarter financial results after the close of the market on Wednesday, Oct. 28, 2026."* The Microsoft IR homepage carries the same date.

- Oct 28, 2026 **is a Wednesday**. (One preview site, TickerDaily, incorrectly calls it "Tuesday, October 28" — do not reproduce that.)
- **This is four days away.** It is the single most consequential near-term event for either name in this piece.

**Three things make this print structurally different from every prior one:**

1. **Segment reporting changes on this call.** Microsoft collapses three segments into two: **"Agents and Infra"** and **"Devices and Consumer."** Azure revenue will be disclosed in **dollars, excluding non-consumption components** — a cleaner read on underlying cloud demand that Wells Fargo argues could expose upside previously buried in the old format. First look at the new numbers is a genuine information event, not just a re-label.
2. **Guidance already on the table:** revenue **$89.85B–$90.95B** (+16–17%), Intelligent Cloud $40.95B–$41.25B, **Azure growth ~45% at constant currency** (accelerating from 43%), capex **above $50B in the quarter**.
3. **Consensus:** EPS **$4.71** on revenue **~$90.7B** (yfinance aggregate of 53 analysts; MarketBeat and TipRanks both cite $4.71 / ~$90.6B). Microsoft has beaten consensus EPS in each of the last eight quarters.

**Secondary dated catalysts:**
- **Microsoft Ignite — November 17–20, 2026, Moscone Center, San Francisco** (confirmed on microsoft.com/en-us/events). Wells Fargo expects detail on AI models, apps and custom silicon. The Maia 300 ramp gets its full technical airing here.
- **Fiscal Q2 2027 print — late January 2027** (not yet dated; Microsoft typically announces ~3 weeks ahead).

## 2.4 THE NUMBERS

### Freshest quarter — Q4 FY2026, ended June 30, 2026 (reported Wed, July 29, 2026)
Source: Microsoft press release / 10-K.

| | Q4 FY26 | Change |
|---|---|---|
| Revenue | $90.007B | **+18%** (+17% cc) |
| Operating income | $40.603B | +18% |
| Net income | $35.766B | +31% GAAP / +22% non-GAAP |
| Diluted EPS | $4.81 GAAP | +32% |
| Diluted EPS | $4.74 non-GAAP | +23% |
| Microsoft Cloud revenue | $59.3B | +27% |
| **Commercial RPO** | **$678B** | **+84%** |
| Azure & other cloud services | — | **+43%** |

- Segment detail: Intelligent Cloud $39.3B (+32%), Productivity & Business Processes $37.8B (+14%), More Personal Computing $12.9B (**−4%**).
- **Azure crossed $100B in annual revenue for the first time**, +41% for the full year. **M365 Copilot passed 30 million paid seats**, up from ~15M in December 2025.
- Note the GAAP/non-GAAP gap: non-GAAP excludes OpenAI investment marks. Discrete items (a **$3.2B gain on the Anthropic investment**, lower Voluntary Retirement Program costs, offset by XBOX severance/impairment) added **$0.27** to diluted EPS versus guidance.

### Full year FY2026 (ended June 30, 2026)
Revenue **$331.8B** (+18%) · Operating income **$155.2B** (+21%) · Net income **$133.7B** (+31%) · Diluted EPS **$17.95** (+32%)

### TTM (computed from quarterly statements, cross-checked against the FY2026 10-K)
| Metric | TTM / FY2026 |
|---|---|
| Revenue | **$331.84B** |
| Gross profit / margin | $225.47B / **67.9%** |
| Operating income / margin | $155.24B / **46.8%** |
| Net income / margin | $133.75B / **40.3%** |
| R&D | $35.56B (10.7% of revenue) |
| Operating cash flow | $182.94B |
| **Capex (cash PP&E)** | **$115.95B (34.9% of revenue)** |
| **Free cash flow** | **$66.99B (20.2% margin)** |
| Stock-based comp | $12.40B (3.7% of revenue) |
| FCF less SBC | $54.58B |
| Dividends + buybacks | $48.72B |

**The two numbers that define the story:**
- **Capex $115.95B, up 79.6% from $64.55B in FY2025.**
- **Free cash flow $66.99B, DOWN 6.5% year over year** — despite revenue growing 18%.

Including new finance leases, capital spending was **$145.3B, or 44% of revenue** (TradeandTell, working from the 10-K). Microsoft's own disclosed **depreciation expense was $34.3B in FY2026, versus $22.0B in FY2025 and $15.2B in FY2024** — a 56% step-up that is contractually locked in and will keep climbing for years regardless of what demand does next.

### Balance-sheet / off-P&L obligations (10-K, as of June 30, 2026) — do not omit these
| Obligation | Total | Due FY2027 |
|---|---|---|
| Purchase commitments (datacenters; open POs + take-or-pay) | **$194.06B** | **$169.01B** |
| Operating + finance leases incl. imputed interest | **$443.51B** | $32.41B ($411.10B thereafter) |
| Construction commitments | $34.57B | $29.85B |
| Long-term debt principal | $46.14B | $9.25B |
| **Total contractual obligations** | **$743.82B** | **$241.92B** |

Set that against **FY2026 free cash flow of $66.99B**. Roughly **$637.6B** of the total is lease + purchase commitments alone. RPO is $684B total ($678B commercial), ~30% expected to be recognized within 12 months, weighted-average duration ~2.3 years.

### Guidance and the accounting change
- **Calendar 2026 capex: ~$175B, revised down from ~$190B** — but *not* because Microsoft is spending less. On the July 29 call the company extended the estimated useful life of data centers and office buildings **from 15 to 25 years, effective the start of FY2027**, which pushes more data-center leases from finance to operating leases. Finance leases count as capex; operating leases do not. CFO Amy Hood: *"outside of this useful-life impact, our calendar year 2026 capex investment expectations remain unchanged."* **The $15B "cut" is a reclassification; the cash still leaves the building.** Lower annual depreciation also flatters reported operating income and EPS.
- **FQ1 FY2027 capex: >$50B.** BofA models $50.8B (+24% QoQ) and **$220.7B for the full fiscal year, +51.9% YoY**.
- **Microsoft Cloud gross margin: 65% in Q4 FY2026, down from 68% a year earlier** (and 69% for FY2025). AI revenue is structurally lower-margin than software, and the trend is three points in four quarters.

## 2.5 THE STOCK'S CURRENT STATE (relative, not absolute)

| | Value |
|---|---|
| Last close (Oct 23, 2026) | $524.51 |
| 52-wk **closing** high | $543.45 (**Oct 13, 2026**) → **−3.5%** |
| 52-wk **intraday** high | $553.72 → **−5.3%** |
| 52-wk low | $349.20 (intraday); lowest close $352.83 (June 25, 2026) |
| 50-day SMA | $508.43 → price **+3.2% above** |
| 200-day SMA | $436.51 → price **+20.2% above** |
| Forward P/E | **22.1x** (FY27E EPS $23.70) |
| Trailing GAAP P/E | 29.2x |
| EV/EBITDA (TTM) | 20.3x |
| P/S (TTM) | 11.7x |

**Seasonality/context that matters:** MSFT bottomed at $352.83 on June 25, 2026 and has rallied to $524.51 — a **+48.7% move in four months**, with the all-time closing high set ten days ago. That is a stock that has already re-rated hard off the June low, even though it is only **+8.5% year-to-date** (2025 close: $483.62) because it fell 23% in the first half. Both facts matter: the rally is real, and the stock is not extended versus where it started the year.

**On its own history:** MSFT's trailing P/E at each of the last four fiscal year-ends was **35.2x (FY23), 37.9x (FY24), 36.5x (FY25), 20.8x (FY26)** — a four-year average of **~32.6x**. At 22.1x forward, MSFT trades at a meaningful discount to that historical band, which the bulls read as room; the bears read as the market correctly anticipating that the earnings mix is about to get far more capital-intensive.

**Against peers**, 22.1x forward puts MSFT in the middle of mega-cap tech: below AMZN (23.8x) and AMD (32.8x), above GOOGL (20.8x) and META (18.5x), and roughly double ORCL (11.5x).

## 2.6 RECENT NEWS THAT MATTERS (last three weeks)

- **Oct 22 — shares fell 1.66% to $524.10**, reversing an early climb above $532, as the market digested FY2026 capex and the overnight AI-hardware selloff. (This was the same session AVGO fell 4.3%.)
- **Oct 12 — Maia 300 announced** (Reuters, Stephen Nellis & Max Cherney). Third-generation custom AI chip; **>1 million units planned for deployment next year**; 96-chip racks at ~167 kW; **~40% more useful compute per megawatt** than "leading GPU-based systems"; "multi-gigawatt deployments" starting 2027. Strategic read: Microsoft is trying to convert Nvidia's gross margin into its own.
- **Oct 7 — Microsoft confirmed Oct 28 as its Q1 FY2027 earnings date** (company newsroom).
- **All of October — a wall of price-target hikes** ahead of the print (see below), following a ~39% rally. Morgan Stanley warned on Oct 19 that the move has set a **"higher bar"**: Microsoft now needs Azure growth **in the mid-40s** to sustain momentum.
- **Sept 30 / Oct 14 — FTC opens an industry-wide AI probe** into OpenAI, Anthropic and others, then issues **civil investigative demands to OpenAI and Anthropic on Oct 14**, seeking documents on safety incidents, safeguards, marketing and privacy, with plans to compel executive testimony. **Direct relevance to MSFT:** a ~27% equity stake in OpenAI plus OpenAI as a major Azure customer. Materiality is unclear — this is an information-gathering stage, not a complaint.
- **RPO disclosure detail worth flagging:** commercial RPO rose 84% to $678B, but **about 45% of that backlog is OpenAI** (as of Dec 31, 2025), and growth outside OpenAI was **25%** to June 2026. Nearly **90% of annual Microsoft Cloud revenue comes from customers outside frontier model companies** — management is leaning hard on that stat precisely because the headline backlog number is heavily concentrated.

## 2.7 ANALYST CONTEXT

- **Consensus: Strong Buy** — mean recommendation **1.33** across **53 analysts**.
- **Mean price target $601.73; median $600.00** (+14.7% vs $524.51). Range **$870 high / $440 low**.

**Notable recent target changes (firm + analyst + date):**
| Date | Firm | Analyst | Action | Target |
|---|---|---|---|---|
| Oct 21, 2026 | Guggenheim | — | Reaffirmed Buy | $586 |
| Oct 20, 2026 | BMO Capital | — | Raised, Outperform | $515 → **$600** |
| Oct 19, 2026 | Bernstein | — | Raised, Outperform | $660 → **$662** |
| Oct 15, 2026 | **UBS** | **Karl Keirstead** | Raised, Buy | $525 → **$675** (+28.6%) |
| Oct 15, 2026 | TD Cowen | — | Raised, Buy | $540 → **$625** |
| Oct 15, 2026 | Mizuho | Gregg Moskowitz | Raised, Outperform | $510 → **$600** |
| Oct 15, 2026 | Citi | Tyler Radke | Raised, Buy | $600 → **$636** |
| Oct 14, 2026 | Jefferies | — | Raised, Buy | $575 → **$650** |
| Oct 13, 2026 | Barclays | — | Raised, Overweight | $512 → **$600** |
| Oct 1, 2026 | Wells Fargo | Michael Turrin | Raised, Overweight; added to Tactical Ideas | $700 → **$725** |

Keirstead's note is the most useful framing: the sharp rally had raised growth expectations, but Azure and M365 fundamentals supported the optimism and valuation "remained reasonable." Turrin's is the most specific: he flagged the segment reorg and the new dollar-denominated Azure disclosure as the reason the stock could re-rate further — i.e., **better disclosure, not better results, is the near-term bull lever.**

BofA's Tal Liani (Buy, $600) models **Azure +44.8% cc to $32.3B** in Q1 and capex of **$50.8B** for the quarter.

## 2.8 THE STRONGEST BEAR CASE

> **"Microsoft is spending more cash than the business generates, and it changed an accounting estimate to make the number look smaller. The AI revenue is lower-margin than the software it is replacing. This is a melting-ice-cube story wearing a growth multiple."**

A short seller's argument, in order:

1. **Free cash flow is going the wrong way while revenue accelerates.** FY2026 revenue +18%, **FCF −6.5% to $66.99B**. Capex went from $64.55B to $115.95B (+79.6%). The company is now converting 20 cents of every revenue dollar into free cash, down from ~25%. If FY2027 capex lands anywhere near BofA's **$220.7B**, FCF does not grow — it compresses further.
2. **The $15B capex "cut" was an accounting change, not discipline.** Extending building useful lives from 15 to 25 years moved leases from finance to operating and cut reported capex from ~$190B to ~$175B for calendar 2026. It also lowers annual depreciation, which **raises reported operating income and EPS**. Management conceded the cash spend is unchanged. A short seller calls that managed earnings.
3. **The depreciation bill is already enormous and is contractually locked.** $15.2B (FY24) → $22.0B (FY25) → **$34.3B (FY26)**, +56% in the latest year. Every dollar of the $115.95B capex converts to ~$15–20B of annual depreciation over the following 5–6 years on the short-lived GPU/CPU portion (roughly **two-thirds** of Q4 capex went to short-lived equipment). Earnings growth has to outrun a rising, non-discretionary cost line — and the useful-life extension is precisely what makes that easier to mask.
4. **The obligations outside the capex line are bigger than the capex line.** **$443.5B** of operating and finance lease commitments plus **$194.1B** of purchase commitments (take-or-pay, mostly datacenters) — **$637.6B** total, of which **$169.0B** of purchase commitments fall due in FY2027 alone against $66.99B of FCF. If AI demand slows, these become a drag with no off-ramp; the take-or-pay language means Microsoft pays for capacity it does not use.
5. **Margin mix is deteriorating and management admits it.** Microsoft Cloud gross margin fell from **68% to 65%** in a single year. AI infrastructure revenue is a commodity-adjacent, capital-heavy business bolted onto a 90%-gross-margin software franchise. The more the mix shifts to AI, the more the blended margin falls — structurally, not cyclically.
6. **The backlog is an OpenAI backlog.** Commercial RPO +84% to $678B sounds like demand visibility. But **~45% of it was OpenAI**, a company that lost money at scale and is now under FTC investigation. Ex-OpenAI, RPO grew **25%**. Management's own defense — "nearly 90% of cloud revenue is from non-frontier customers" — is an admission that the headline growth rate is concentrated in the one customer whose solvency is a live question.
7. **The stock has already priced the good news.** +48.7% off the June low and an all-time closing high ten days ago, for 18% revenue growth that requires $220B of annual capex to sustain. Morgan Stanley's own note concedes the bar is now "mid-40s" Azure growth — meaning **43% would be a disappointment** even though it was a blowout three months ago.

**What would prove the short right (the falsifiable triggers):**
- **Azure growth below ~44% cc on October 28.** The guide is ~45%; MS says mid-40s is the bar. A 42–43% print with capex above $50B is the exact combination that breaks the "capacity is immediately monetized" thesis.
- **FY2027 FCF guidance or disclosure showing another down year**, or capex guided materially above $220B without a corresponding Azure acceleration.
- **The new "Agents and Infra" segment disclosing Azure margins below the old Intelligent Cloud margin** — the reorg could expose precisely the dilution the bull case assumes away.
- **Microsoft Cloud gross margin below 65%**, extending a four-quarter slide.
- Any adverse FTC action touching OpenAI that impairs either the ~27% stake or OpenAI's Azure consumption.

---

# 3. THE COMPARISON, IN ONE TABLE

| | **AVGO** | **MSFT** |
|---|---|---|
| Freshest quarter | Q3 FY26, ended Aug 2, 2026 | Q4 FY26, ended Jun 30, 2026 |
| Reported | Wed, Sept 2, 2026 | Wed, July 29, 2026 |
| Next catalyst | **Wed, Dec 9, 2026** (after close) | **Wed, Oct 28, 2026** (after close) |
| Days to catalyst | ~46 | **4** |
| Revenue growth (latest Q) | **+86%** | +18% |
| TTM revenue | $89.10B | $331.84B |
| TTM operating margin | 48.5% (GAAP) | 46.8% |
| TTM FCF | **$39.40B** | $66.99B |
| FCF margin | **44.2%** | 20.2% |
| Capex / revenue | **1.4%** | **34.9%** |
| FCF YoY direction | **+95% (latest Q)** | **−6.5% (FY)** |
| Forward P/E | **16.6x** | 22.1x |
| % off 52-wk closing high | **−33.2%** | −3.5% |
| vs 200-day SMA | **−12.5%** | +20.2% |
| Consensus | Strong Buy (1.27, n=48) | Strong Buy (1.33, n=53) |
| Mean PT upside | **+64.5%** | +14.7% |
| Core bear | Broadcom is financing its own customers | Capex is outrunning cash flow |

**The one-sentence version for the piece:** AVGO is the high-margin, asset-light arms dealer whose customers can't afford the weapons, priced as if that doesn't matter. MSFT is the well-capitalized landlord whose tenants may not be able to pay rent, priced as if they always will.

---

# 4. WHAT I COULD NOT VERIFY

Be explicit about these in the piece:

1. **AVGO's formal Q4 earnings date notice has not been issued.** Dec 9 comes from the company's IR head on the Q3 call. Aggregators split between Dec 9 and Dec 10. A formal announcement is expected early November.
2. **Broadcom's IR site returns HTTP 403 to automated requests.** The press release content was verified via the identical PR Newswire distribution (HTTP 200) and the SEC 10-Q. The investors.broadcom.com URL is real but bot-blocked.
3. **Reuters, WSJ, Bloomberg and Axios URLs return 401/403** (paywall/bot-block). They are real and were returned by search with matching content, but I could not open them directly — figures attributed to them are corroborated by at least one other accessible source.
4. **AVGO's 5-year average forward P/E could not be computed cleanly** from free data. GAAP trailing P/E is unusable as an anchor for Broadcom because VMware acquisition amortization distorts FY2024 (138x) and FY2025 (77.5x). I substituted peer forward P/E and the multiple-compression history (77.5x → 49.7x → 41.1x). **Do not print a "5-year average P/E" figure for AVGO** — it would be misleading either way.
5. **MSFT's 5-year average P/E is really a four-year average** (FY2023–FY2026) because quarterly EPS history available to me starts in FY2025. Label it "four fiscal years" or source a longer series.
6. **Anthropic's $4.6B revenue / $42B net loss / $20.28B cash figures** come from secondary reporting on a *confidential* IPO prospectus. The $161.2B Broadcom lease obligation is Reuters reporting on the same document. Neither is in a public filing I could read.
7. **The "one distributor = 50% of revenue" claim** is verified directly from the AVGO 10-Q — but Broadcom does not name the distributor, and it is a distributor, not necessarily a single end customer. Do not conflate it with the "six XPU customers" concentration.
8. **MediaTek's competitive position** is sourced only from Hock Tan's own framing on the earnings call. No independent verification of MediaTek's TPU v8T timeline.
9. **AVGO Q4 consensus** ($34.90B / $3.83 EPS) is a yfinance aggregate; LSEG's revenue consensus was reported at $35.03B. Consensus figures differ by provider — attribute them.
10. **The Oct 23 DOCOMO VMware deal** has **no disclosed financial terms.** Do not imply a dollar value.

---

# 5. SOURCES

## Verified HTTP 200
- Broadcom Q3 FY2026 results (PR Newswire, identical to IR release): https://www.prnewswire.com/news-releases/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial-results-and-quarterly-dividend-302868129.html
- Broadcom Q3 FY2026 Form 10-Q (SEC, quarter ended Aug 2, 2026 — RPO $179.2B, $29B backstop, $42B convertible facility, 50% distributor concentration): https://www.sec.gov/Archives/edgar/data/1730168/000173016826000080/avgo-20260802.htm
- Broadcom Q3 FY2026 earnings call transcript (Motley Fool — source of the Dec 9 earnings date): https://www.fool.com/earnings/call-transcripts/2026/09/09/broadcom-avgo-q3-2026-earnings-call-transcript/
- Microsoft FY26 Q4 press release: https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast
- Microsoft FY26 Q4 investor metrics (cloud gross margin 68%→65%, RPO, Azure growth): https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/metrics
- Microsoft FY26 Q4 earnings call remarks (Azure 45% cc guide, capex): https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4
- Microsoft newsroom, Q4 FY2026 release: https://news.microsoft.com/source/2026/07/29/microsoft-cloud-and-ai-strength-fuels-fourth-quarter-results-4/
- **Microsoft newsroom, Oct 7 2026 — confirms Oct 28 earnings date**: https://news.microsoft.com/source/2026/10/07/microsoft-announces-quarterly-earnings-release-date-69/
- Microsoft FY2026 Form 10-K (contractual obligations $743.8B, purchase commitments $194.1B, leases $443.5B, depreciation $34.3B, RPO $684B): https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm
- Microsoft IR homepage (Oct 28, 2026 confirmed on page): https://www.microsoft.com/en-us/investor/default
- Microsoft events page (Ignite Nov 17–20, 2026, Moscone Center): https://www.microsoft.com/en-us/events
- Anthropic — expanded Google/Broadcom compute partnership: https://www.anthropic.com/news/google-broadcom-partnership-compute
- CNBC, Broadcom Q3 2026 earnings: https://www.cnbc.com/2026/09/02/broadcom-avgo-q3-earnings-report-2026.html
- CNBC, Microsoft Q4 FY2026 earnings: https://www.cnbc.com/2026/07/29/microsoft-msft-q4-earnings-report-2026.html
- IFR, "Broadcom backstops US$42bn funding for Anthropic" (loan structure, 187.5bp/150bp over SOFR, Sept 2033 maturity, $61.5B package): https://www.ifre.com/loans/2496132/chips-with-everything-broadcom-backstops-us42bn-funding-for-anthropic
- MarketBeat, "Broadcom's AI Growth Story Faces a $161 Billion Anthropic Test" (Anthropic $518B commitments, $35B AI XPV tranche, $29B backstop mechanics): https://www.marketbeat.com/articles/broadcoms-ai-growth-story-faces-a-161-billion-anthropic-test/

## Real but bot-blocked / paywalled (attempted, non-200)
- Broadcom IR, Q3 FY2026 release (**403 bot-block**): https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial
- Reuters, "Broadcom raises AI chip forecast..." Sept 2, 2026 (**401**): https://www.reuters.com/business/broadcom-forecasts-quarterly-revenue-below-estimates-2026-09-02/
- Reuters exclusive, "Broadcom to lend Anthropic up to $42 billion to lease its chips," Oct 1, 2026 (**401**): https://www.reuters.com/business/broadcom-lend-anthropic-up-42-billion-lease-its-chips-filing-says-2026-10-01/
- Reuters, "Microsoft says cash will keep flowing from AI," July 29, 2026 (**401**): https://www.reuters.com/business/microsoft-tops-quarterly-cloud-growth-estimates-easing-spending-concerns-2026-07-29/
- Reuters, Microsoft Maia 300 announcement, Oct 12, 2026 (**401**): https://www.reuters.com/business/microsoft-plans-huge-deployment-of-its-own-ai-chips-with-an-eye-on-saving-costs-2026-10-12/
- Reuters, FTC opens AI probe, Sept 30, 2026 (**401**): https://www.reuters.com/business/ftc-opens-probe-into-ai-giants-including-anthropic-openai-new-york-post-reports-2026-09-30/
- WSJ, Broadcom Q3 profit soars (**401**): https://www.wsj.com/business/earnings/broadcom-third-quarter-profit-soars-on-ai-driven-revenue-growth-c5add826
- Axios, FTC subpoenas OpenAI and Anthropic, Oct 15, 2026 (**403**): https://www.axios.com/2026/10/15/ftc-openai-anthropic-ai-safety-investigation
- Benzinga, "Capital Over Chips: Broadcom CEO Warns Financing Costs Could Slow AI Expansion," Oct 15, 2026 (**403**): https://www.benzinga.com/markets/tech/26/10/62379402/capital-over-chips-broadcom-ceo-warns-financing-costs-could-slow-ai-expansion
- Investing.com, Broadcom Q3 2026 earnings call transcript (**403**): https://www.investing.com/news/transcripts/earnings-call-transcript-broadcom-tops-q3-2026-estimates-as-ai-sales-surge-93CH-4886849
- CNBC AVGO quote page (52-wk high date 06/03/26, Fwd P/E NTM 18.57): https://www.cnbc.com/quotes/AVGO

## Data provenance
All prices, share counts, analyst aggregates, SMA values and quarterly statement line items were pulled from **yfinance 1.4.1** via `/home/chino/video-venv/bin/python3` on **Oct 24, 2026**. TTM figures were computed by summing the four most recent reported quarters rather than reading a provider's `totalRevenue`/`freeCashflow` field — note yfinance's `info["freeCashflow"]` for MSFT reports **$16.55B**, which is stale/incorrect; the correct computed TTM FCF is **$66.99B** and matches the 10-K and press coverage. Raw pull cached at `/home/chino/thesignal/tmp/avgo_msft_raw.json`; price series at `tmp/AVGO_px.csv` and `tmp/MSFT_px.csv`.
