# RESEARCH BRIEF: NuScale Power Corporation (NYSE: SMR)
## Institutional Deep-Dive — AI Power / Advanced Nuclear Sector
**Date:** October 6, 2026
**Proposed Slug:** `smr-nuscale-nuclear-licensing-moat-ai-power-2026`

---

## SECTION 1: SNAPSHOT & KEY STATISTICS

### Company Overview
- **Ticker:** SMR (NYSE) | **Sector:** Utilities / Advanced Nuclear (pre-revenue)
- **HQ:** Corvallis, Oregon | **Founded:** 2007 | **CEO:** John L. Hopkins (President & CEO)
- **CTO:** Dr. José Reyes | **CFO:** Robert Ramsey Hamady
- **Product:** NuScale Power Module™ (NPM) — light-water SMR, **77 MWe / 250 MWth (gross)** per module; scalable to **924 MWe (12 modules)**
- **Structure:** Up-C (Class A + Class B units); NuScale Power, LLC is the operating entity
- **Positioning:** The **first and only company with NRC-approved SMR designs**

### Current Market Data (yfinance, as of Oct 6, 2026)

| Metric | Value |
|--------|-------|
| **Current Price** | $8.175 (prior close $7.68) |
| **Market Cap** | $3.355B |
| **Enterprise Value** | $2.039B |
| **52-Week High** | $57.42 (Oct 16, 2025) |
| **52-Week Low** | $7.21 (Jul 17, 2026) |
| **From 52W High** | **-85.7%** |
| **50-Day MA / 200-Day MA** | $9.00 / $11.90 |
| **Beta (5Y monthly)** | 2.371 |
| **Revenue (TTM)** | $10.69M |
| **Revenue Growth (YoY)** | **-99.1%** |
| **Gross Margin** | 23.5% |
| **Operating Margin** | -853.4% |
| **EBITDA (TTM)** | -$224.1M |
| **Net Income (TTM)** | -$415.7M |
| **EPS (TTM)** | -$2.92 |
| **Forward EPS** | -$0.66 |
| **Price/Sales (TTM)** | 313.8x |
| **Price/Book** | 1.63x (Book value $5.02/share) |
| **Free Cash Flow (TTM)** | -$204.6M |
| **Total Cash & ST Investments** | **$1.072B** |
| **Total Liquidity (incl. LT investments)** | **$1.9B** (Q2'26) |
| **Total Debt** | $6.69M (incl. leases; $0.76M on balance sheet) |
| **Current Ratio** | 37.88 |
| **Cash Per Share** | $2.613 |
| **Shares Outstanding / Float** | 410.4M / 403.5M |
| **Institutional / Insider** | 58.8% / 1.7% |
| **Short % of Float / Short Ratio** | 20.64% / 2.08 days |
| **Avg Volume (3M / 10D)** | 33.2M / 30.1M |
| **Next Earnings** | Nov 5, 2026 (Q3 2026) |

### Performance
| Period | Return |
|--------|--------|
| 1-Year | **-80.5%** |
| YTD (from $14.17 on 12/31/25) | **-42.2%** |
| 6-Month | -10.5% |
| 3-Month | -8.5% |
| All-time high | $57.42 (Oct 16, 2025) |

---

## SECTION 2: EXACT YFINANCE CALLS

```python
import yfinance as yf
ticker = yf.Ticker("SMR")
info = ticker.info

info.get("currentPrice")                  # 8.175
info.get("previousClose")                 # 7.68
info.get("marketCap")                     # 3,354,934,528
info.get("enterpriseValue")               # 2,038,683,520
info.get("fiftyTwoWeekHigh")              # 57.42
info.get("fiftyTwoWeekLow")               # 7.21
info.get("fiftyDayAverage")               # 9.0016
info.get("twoHundredDayAverage")          # 11.8985
info.get("totalRevenue")                  # 10,690,000 (TTM)
info.get("revenueGrowth")                 # -0.991 (-99.1%)
info.get("grossMargins")                  # 0.23545
info.get("operatingMargins")              # -8.5337  (-853.4%)
info.get("ebitda")                        # -224,090,000
info.get("netIncomeToCommon")             # -415,702,016
info.get("trailingEps")                   # -2.92
info.get("forwardEps")                    # -0.6601
info.get("totalCash")                     # 1,072,147,968  (cash + ST investments)
info.get("totalDebt")                     # 6,692,000
info.get("debtToEquity")                  # 0.332
info.get("currentRatio")                  # 37.88
info.get("bookValue")                     # 5.023
info.get("priceToBook")                   # 1.6275
info.get("priceToSalesTrailing12Months")  # 313.84
info.get("freeCashflow")                  # -204,594,000
info.get("sharesOutstanding")             # 410,389,522
info.get("floatShares")                   # 403,544,225
info.get("totalCashPerShare")             # 2.613
info.get("beta")                          # 2.371
info.get("targetMeanPrice")               # 11.96667
info.get("targetMedianPrice")             # 11.0
info.get("targetHighPrice")               # 20.0
info.get("targetLowPrice")                # 6.0
info.get("numberOfAnalystOpinions")       # 15
info.get("heldPercentInstitutions")       # 0.58831
info.get("heldPercentInsiders")           # 0.017
info.get("shortPercentOfFloat")           # 0.2064
info.get("shortRatio")                    # 2.08
info.get("averageVolume")                 # 33,246,215
```

---

## SECTION 3: THE REGULATORY MOAT — NRC STANDARD DESIGN APPROVAL (SDA)

NuScale's defining asset is regulatory. It is **the only company whose SMR designs have been approved by the U.S. Nuclear Regulatory Commission** — a multi-year, hundreds-of-millions-of-dollars barrier that competitors have not crossed.

- **2020:** NRC issued its **Standard Design Approval (SDA)** for NuScale's SMR design (initial module generation), confirming compliance with **Subpart E of 10 CFR Part 52**. NuScale was the first SMR developer to complete the full Design Certification Application review (Phase 6 / Final Safety Evaluation Report).
- **May 29, 2025:** NRC issued a **second SDA**, this time for the **uprated NuScale US460 design** — 6-module VOYGR-6 configuration using **77 MWe (250 MWth)** modules. Published at **90 FR 23716** (Docket **NRC-2023-0027**). This made NuScale the only company with two NRC-approved SMR designs.
- **Legal mechanics:** An SDA permits the design to be **referenced in a 10 CFR Part 50 construction permit / operating license application**, or a **Part 52 combined license (COL) / manufacturing license application**. This is a referenceable, pre-cleared design — it removes the single largest schedule and cost risk from a customer's licensing path.
- **Marketing claim (company language):** NuScale describes itself as "the first and only SMR to have its designs certified by the U.S. Nuclear Regulatory Commission."

> **Nuance for the analysis:** NuScale's approvals are technically a **Standard Design Approval (SDA)** under 10 CFR Part 52 Subpart E, not a **Design Certification (DC)** under Subpart B. The company's press language often says "certified." The distinction matters for the mooted claim that NuScale holds NRC "certification."

---

## SECTION 4: FINANCIALS

### Quarterly Trend (yfinance)

| Quarter | Revenue | Gross Profit | Operating Income | Net Income | R&D | SG&A |
|---------|---------|-------------|------------------|------------|-----|------|
| Q2 2026 (6/30/26) | **$75K** | -$152K | -$64.0M | -$47.5M | $18.4M | $26.9M |
| Q1 2026 (3/31/26) | $565K | $21K | -$57.5M | -$44.0M | $12.8M | $24.8M |
| Q4 2025 (12/31/25) | $1.81M | -$61K | -$72.7M | -$50.8M | $13.5M | $44.8M |
| Q3 2025 (9/30/25) | $8.24M | $2.71M | -$538.4M | -$273.3M | $11.1M | $519.2M |
| Q2 2025 (6/30/25) | $8.05M | $1.78M | -$43.1M | -$17.6M | $11.8M | $22.5M |

- **Q2 2026 revenue of $75,000** = **-99% YoY** from $8.05M. Cause: the **Fluor FEED Phase 2 engineering services** for Romania **completed in late 2025** — no comparable engineering-fee activity in 2026.
- **Q3 2025 blowup:** SG&A of $519.2M and a **$273.3M net loss** (net figure varies by source; some report ~$532M on a total-entity basis) driven by a large **ENTRA1 Partnership Milestones Agreement (PMA)** charge tied to the TVA agreement. Company disclosed a **$128.5M cash PMA milestone payment**; class-action filings cite a **~$495M** figure. This quarter is the inflection that broke the stock.
- Q2 2026 net loss: **-$47.5M** per yfinance income statement; the earnings transcript cites **$50.1M, or $0.13 per Class A share**, on a total-entity basis.

### Fiscal Year History

| FY | Revenue | Gross Margin | Loss from Ops | G&A |
|----|---------|-------------|---------------|-----|
| FY 2025 | **$31.48M** | $11.43M | -$689.57M | $609.83M |
| FY 2024 | $37.05M | $32.11M | — | $75.9M |
| FY 2023 | $22.81M | $3.85M | — | $65.4M |

- FY2025 revenue **fell to $31.5M** (from $37.0M) as the 2024 RoPower technology-license revenue gave way to the FEED-2 engineering revenue that began winding down late 2025.
- FY2025 investment income **$25.3M** (vs. $8.4M in 2024) — interest on the large cash pile.

### Balance Sheet (6/30/26)

| Item | 6/30/2026 | 12/31/2025 |
|------|-----------|------------|
| Cash & equivalents | $766.5M | $836.4M |
| Cash + ST investments | **$1.072B** | $1.254B |
| **Total liquidity (incl. LT investments)** | **$1.9B** | — |
| Total debt | $0.76M (bs) / $6.69M (yf) | — |
| Total assets | $2.049B | $1.413B |
| Total liabilities | $35.5M | $299.0M |
| Stockholders' equity | $2.061B | $1.169B |

- **Q2 2026 liquidity rose ~$900M sequentially** to $1.9B — driven by **$984.5M of net equity proceeds in H1 2026**, not operations. Class A share count rose from **318.5M (12/31/25) → 410.4M (6/30/26)**.
- **$1.0B ATM completed in 2026** (~89.7M shares at avg $11.14). A **new $750M ATM became effective Aug 11, 2026**.
- **Debt is de minimis** ($6.7M), so the balance sheet is unlevered; the funding risk is **equity dilution**, not leverage.
- **Cash burn:** UBS estimates **~$700M cumulative FCF burn 2026–2028** (~65% of cash); S&P Global consensus estimates closer to **~$1B** over the same window.

---

## SECTION 5: KEY PROJECTS & PARTNERS

### 1. RoPower Doicești — Romania (462 MWe; most advanced SMR project in the EU)
- **Location:** Doicești, ~90 km NW of Bucharest, on a **former coal plant site** (replaces 600 MW of retired coal).
- **Configuration:** **6 × 77 MWe NPMs = 462 MWe** (uprated US460 design).
- **Project company:** **RoPower Nuclear S.A.** — jointly owned by **S.N. Nuclearelectrica S.A.** (Romanian state nuclear utility) and **Nova Power & Gas** (part of **E-INFRA**).
- **Fluor FEED timeline:** Phase 1 FEED completed **Q4 2023**; **Phase 2 FEED contract signed 2024**; **FEED Phase 2 completed late 2025** (this is the revenue that vanished from NuScale's P&L in 2026). Fluor is the lead contractor / EPFC with NuScale technology.
- **FID:** Nuclearelectrica shareholders approved the **Final Investment Decision in February 2026** (announced ~Feb 12–13, 2026). Romania's Energy Minister **Bogdan Ivan** called it "the transition from the analysis phase to the implementation phase."
- **Next milestones (per Nuclearelectrica, Feb 2026):** by **May 2026** — complete geotechnical investigations, advance licensing, finalize a **pre-EPC contract**, negotiate **long-lead equipment**, define supply chains. **Stage 3 (pre-EPC)** ~15 months → **Class 2 cost estimate**, contractor shortlist.
- **Schedule:** first module commercial operation target **~2033** (slipped from earlier ~2030 aspirations); subject to financing and regulatory approvals.
- **Financing:** U.S. **EXIM Bank approved a $99M loan** (Engineering Multiplier Program) in 2024; **EXIM + DFC** support announced 2024.
- **Economic impact (WNN):** ~200 permanent jobs, ~1,500 construction jobs, ~2,300 manufacturing/component jobs over a 60-year plant life.
- **Q2 2026 status:** NuScale working with Nuclearelectrica/RoPower to **satisfy conditions attached to the shareholder FID vote**.

### 2. ENTRA1 Energy — Exclusive Global Commercialization Partner
- **Since 2022**, **ENTRA1 Energy LLC** is NuScale's **exclusive global strategic partner** for commercializing, distributing, and deploying NuScale SMR technology. ENTRA1 develops, finances, owns, and operates power plants; NuScale supplies the technology.
- Structure offers customers a single integrated solution (development + financing + ownership + O&M), addressing the biggest bottleneck in advanced nuclear: **bankability**.

### 3. TVA / ENTRA1 6-GW Program — largest U.S. SMR deployment
- **Sept 2, 2025:** **Tennessee Valley Authority (TVA)** + **ENTRA1 Energy** announced a **collaborative agreement** for up to **6 GW** of new nuclear across TVA's **seven-state** service territory — **six ENTRA1 Energy Plants** totaling **~72 NuScale Power Modules** (12 modules per plant).
- Equates to power for **~4.5 million homes or ~60 new data centers** — the AI/data-center demand thesis.
- **Status as of Q2 2026 (Aug 5, 2026): still NOT a definitive PPA.** ENTRA1 and TVA "continue to advance discussions"; site visits and engineering evaluations done; potential first-plant locations identified.
- Revenue pathway: management expects service revenues (COL application work, FEED) once a **definitive PPA is signed** and financing secured.
- A **major multi-billion-dollar payment/milestone** to ENTRA1 was triggered by this agreement (the Q3 2025 charge). Future milestone payments are a flagged capital-allocation risk.

### 4. MillenniTEK — Safety-Component Manufacturing (Sept 1, 2026)
- **Sept 1, 2026:** NuScale + **MillenniTEK** (Knoxville, TN; acquired by Houston-based **Pelican Energy Partners** in 2024) announced **successful fabrication of first-of-a-kind boron-oxide pellets** for NuScale's **passive Emergency Core Cooling System (ECCS)**.
- Pellets dissolve into reactor coolant on ECCS actuation to control core reactivity **without operator intervention**.
- Signals maturing supply chain and production-ready manufacturing for first customer deployments.

### 5. NPX + Nuclearn — Nuclear-Specific AI (Aug 25, 2026)
- **Aug 25, 2026:** NuScale is deploying **purpose-built nuclear AI tools** combining NuScale's reactor expertise, **Nuclearn's AtomAssist** nuclear AI platform, and **NPX's** nuclear project/AI implementation experience.
- Target: engineering and knowledge management — faster, traceable retrieval of engineering methods, licensing evidence, and technical standards.
- **Initial proof of concept showed up to 80% reduction in time to find relevant information.** Per CTO Dr. José Reyes and Nuclearn CFO Jerrold Vincent. On-premise-ready, traceable to controlled sources.

### 6. Paragon (Mirion Technologies) — HIPS Protection System
- NuScale awarded **Paragon** (a **Mirion Technologies** company, Fort Worth, TX) a contract to **complete final design development of the Highly Integrated Protection System (HIPS)** for the NPM — a key supply-chain-readiness milestone (announced with Q2 2026 results).
- HIPS underpins the NPM's **reactor protection, safety display/indication, and plant protection systems**.

### 7. Other Strategic Partners
- **Fluor Corporation** — engineering/EPFC partner and former majority investor; **unwinding its stake via a structured monetization program agreed Nov 2025, beginning by end of Q2 2026** (a technical overhang).
- **Samsung C&T** (investor/contractor), **JGC Holdings** ($40M cash investment + Asia deployment partnership), **IHI** (steel composite isolation wall modules).
- **Supply chain:** management cites **60+ specialized partners with 30+ agreements already executed** (Q2 2026).

---

## SECTION 6: CATALYSTS (dated)

| Date | Catalyst |
|------|----------|
| Sept 2, 2025 | TVA + ENTRA1 announce 6-GW / 72-module collaborative agreement |
| Late 2025 | Fluor FEED Phase 2 for RoPower completed |
| Nov 2025 | Fluor–NuScale structured stake-monetization agreement |
| **Feb 2026** | **Romania Doicești FID approved** (462 MWe, 6 modules) |
| May 2026 | RoPower pre-EPC milestone set (geotech, licensing, long-lead equipment) |
| **Aug 5, 2026** | Q2 2026 results — **$1.9B liquidity**, revenue $75K |
| Aug 11, 2026 | New **$750M ATM** effective |
| Aug 25, 2026 | **NPX + Nuclearn** nuclear-specific AI deployment (80% info-retrieval speedup) |
| **Sept 1, 2026** | **MillenniTEK** first-of-a-kind boron-oxide ECCS pellets |
| Sept 11, 2026 | UBS downgrade Neutral→**Sell**, PT $10→$6 |
| **Nov 5, 2026** | **Q3 2026 earnings** |
| Pending | **Definitive TVA/ENTRA1 PPA** (largest U.S. nuclear deployment) |
| Pending | Fluor stake monetization by end of Q2 2026 → rolling overhang |
| ~2033 | First Romania module commercial operation |

---

## SECTION 7: RISKS / BEAR CASE

1. **Pre-revenue reality:** Q2 2026 revenue $75,000; no signed definitive PPA; no firm customer commitments. Revenue depends entirely on future licensing/FEED/service fees.
2. **Cash burn & dilution:** ~$700M (UBS) to ~$1B (consensus) cumulative burn 2026–2028; share count +29% in six months (318.5M→410.4M); new $750M ATM live; further dilution likely.
3. **ENTRA1 dependency + litigation:** securities class action alleges NuScale misrepresented ENTRA1's experience — that ENTRA1 had **never built, financed, or operated a significant nuclear project**. Defendants: NuScale, CEO **John L. Hopkins**, CFO **Robert Ramsey Hamady**, and **Fluor**. Lead-plaintiff deadline ~April 20, 2026. NuScale's entire commercialization channel runs through one unproven counterparty.
4. **Timeline slippage:** Romania first module now ~2033; UBS assumes only **one** project begins construction by 2028.
5. **Valuation:** P/S ~314x TTM on collapsing revenue; negative EPS (-$2.92 TTM).
6. **Competition:** Oklo and peers approaching construction; NuScale risks falling behind on deployment speed.
7. **Sentiment/shorts:** **20.6% of float short**; short sellers reportedly profited ~$2B across SMR, Oklo, and Nano Nuclear over the past year (FT/S3 Partners).
8. **Insider & insider-adjacent selling:** insider ownership only 1.7%; Fluor stake monetization adds supply.

---

## SECTION 8: ANALYST VIEWS

### Consensus (yfinance)
- **Mean target: $11.97** | Median: $11.00 | **High: $20.00** | **Low: $6.00** | **15 analysts**
- Implied upside from ~$8.18: **~+46%**

### Other aggregators
- **MarketBeat:** avg **$12.96** (17 analysts), range **$6–$25**, consensus **Hold**
- **Zacks:** avg **$13.63**, range **$6–$25**

### Recent Rating Actions
| Date | Firm | Action | Target |
|------|------|--------|--------|
| **Sept 11, 2026** | **UBS** (Jon Windham) | **Downgrade Neutral → Sell** | **$10 → $6** |
| Apr 24, 2026 | B. Riley | Maintain Buy | $24 → $19 |
| Apr 23, 2026 | HSBC | Initiate Hold | $13 |
| Feb 24, 2026 | Cantor Fitzgerald (D. Soderberg) | Lower Overweight | $55 → $20 |
| Feb 20, 2026 | Zacks Research | Upgrade Strong Sell → Hold | — |
| Dec 22, 2025 | B. Riley | Maintain Buy | $38 → $24 |
| Nov 25, 2025 | UBS | Maintain Neutral | $38 → $20 |
| Nov 10, 2025 | RBC | Maintain Sector Perform | $35 → $32 |

UBS's bear case: 5+ year build timeline, no firm customer commitments, and ~$700M cumulative cash burn 2026–2028.

---

## SECTION 9: OWNERSHIP & TRADING

| Metric | Value |
|--------|-------|
| Institutional Ownership | 58.8% |
| Insider Ownership | 1.7% |
| Short % of Float | **20.64%** |
| Short Ratio | 2.08 days |
| Avg Volume (3M) | 33.2M |
| Beta | 2.371 |

---

## SECTION 10: BULL vs BEAR SUMMARY

**Bull case:** Only NRC-approved SMR design (two designs: ~50/60 MWe and 77 MWe US460) = a durable, hard-to-replicate licensing moat. $1.9B liquidity fully funds near-term commercialization with **zero meaningful debt**. Three-tiered demand funnel: (1) **TVA/ENTRA1 6-GW, 72-module** program (largest U.S. nuclear deployment, AI/data-center driven); (2) **Romania Doicești** — EU's most advanced SMR project with FID secured; (3) global partner pipeline. Supply chain clearly maturing (60+ partners, 30+ agreements; MillenniTEK safety component; Paragon HIPS final design), plus AI-driven engineering efficiency (NPX/Nuclearn). Analyst mean target ~$12 vs. ~$8 spot.

**Bear case:** Effectively pre-revenue ($75K in Q2 2026) with no signed definitive PPA; hockey-stick dilution (share count +29% in six months, $750M ATM pending) to fund ~$700M–$1B of burn through 2028; commercialization channel concentrated in an **untested ENTRA1** now subject to securities litigation; deployment not until **~2033**; P/S ~314x; 20.6% short interest; and a stock down ~86% from its Oct 2025 high.

**Key swing factor:** a **definitive TVA/ENTRA1 power purchase agreement** — the single event most likely to re-rate the equity, still unsigned as of Oct 6, 2026.

---

## SECTION 11: SOURCES

- NuScale Q2 2026 results press release (Aug 5, 2026): nuscalepower.com
- NuScale FY2025 results press release (Feb 2026): nuscalepower.com
- NuScale + MillenniTEK press release (Sept 1, 2026)
- NuScale NPX + Nuclearn press release (Aug 25, 2026)
- NuScale + Paragon HIPS contract press release (2026)
- NuScale 10-K (FY2025, filed Feb 26, 2026) and 10-Q (Q2 2025 / Q2 2026)
- NRC Standard Design Approval — NuScale US460, 90 FR 23716 (Docket NRC-2023-0027), May 29, 2025
- NRC SDA for NuScale SMR (2020): nuscalepower.com
- TVA + ENTRA1 6-GW announcement (PRNewswire, Sept 2, 2025)
- World Nuclear News / POWER Magazine — Romania FID (Feb 2026)
- RoPower Nuclear (ropowernuclear.com); Fluor newsroom
- UBS downgrade coverage (Investing.com / Motley Fool / Financial Modeling Prep, Sept 11, 2026)
- Levi & Korsinsky securities class action summary; Rosen / Faruqi & Faruqi
- yfinance 1.7.0 (data pull Oct 6, 2026)
- MarketBeat / Zacks / MarketScreener analyst aggregators
- Motley Fool: "NuScale's Revenue Fell 99%. Its Cash Pile Grew By $900 Million." (Aug 17, 2026)

---

**End of brief.**
**Proposed slug:** `smr-nuscale-nuclear-licensing-moat-ai-power-2026`
