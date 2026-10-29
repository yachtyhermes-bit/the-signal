# VERIFIED RESEARCH DOSSIER — Marvell Technology (MRVL)

**Article slug:** `mrvl-custom-silicon-investor-day-2026`
**Sector:** `ai` · **Ticker:** MRVL · **Article timestamp:** 2026-10-02T23:00:00Z (post-close)
**Compiled:** 2026-10-02 (UTC) by The Signal analyst desk
**Price baseline:** $272.29 = MRVL regular-session close, Friday **October 2, 2026** (verified via yfinance `history(period='10d')`)

**Rule applied throughout:** every number below traces to a primary source (company press release / IR deck / SEC filing) or a named wire story. Anything not verifiable is marked **UNVERIFIED**. Nothing in this dossier is inferred from memory.

---

## 0. ONE-PARAGRAPH FRAME

Marvell is a data-infrastructure chip company with two halves: (1) **custom silicon** (XPU/ASIC design services for hyperscalers, plus "XPU attach" — NICs, CXL memory, die-to-die I/O, custom HBM), and (2) the **connectivity "nervous system"** of the data centre — electro-optics (PAM4 DSPs, coherent DSPs, COLORZ DCI pluggables, 224G SerDes, co-packaged optics, silicon photonics), Ethernet switching (Teralynx), storage/HDD & SSD controllers (Bravera), and CXL memory expansion (Structera). The Oct 6, 2026 Investor Day in New York City is the company's own scheduled catalyst to reframe the long-term model.

---

## 1. Q2 FY27 RESULTS (reported August 27, 2026)

**Primary source:** Marvell press release, "Marvell Technology, Inc. Reports Second Quarter of Fiscal Year 2027 Financial Results," Aug 27, 2026 → https://investor.marvell.com/news-events/press-releases/detail/1031/marvell-technology-inc-reports-second-quarter-of-fiscal-year-2027-financial-results **(HTTP 200)**
**Quarter ended:** August 1, 2026.

### Headline (company figures, verbatim from PR)
| Metric | Q2 FY27 | Q2 FY26 | YoY |
|---|---|---|---|
| Net revenue | **$2,739.3M** (record) | $2,006.1M | **+37%** |
| Data center revenue | **$2,171.5M** (record) | $1,490.5M | **+46%** |
| Communications & other | $567.8M | $515.6M | +10% |
| Data center as % of total | **79%** | 74% | — |
| GAAP gross margin | **53.1%** | 50.4% | +270bp |
| Non-GAAP gross margin | **58.9%** | 59.4%* | — |
| GAAP net income | $308.0M | $194.8M | — |
| GAAP diluted EPS | **$0.33** | $0.22 | — |
| Non-GAAP net income | $865.9M | $585.5M | — |
| Non-GAAP diluted EPS | **$0.94** | $0.67 | — |
| Cash flow from operations | **$605.5M** | $461.6M | — |

\* Q2 FY26 non-GAAP GM derived from PR reconciliation: non-GAAP gross profit $1,191.4M / $2,006.1M = 59.4%. Company did not headline this figure in the PR.
**Verified internally:** Q2 FY27 non-GAAP GM = $1,614.0M non-GAAP gross profit ÷ $2,739.3M = **58.92%** (matches headline 58.9%).

- Revenue came in **$39.0M above the midpoint** of guidance given May 27, 2026.
- QoQ: revenue +13%, data center +18%, comms & other −3%.
- Six months ended Aug 1, 2026 (H1 FY27): revenue $5,157.1M; GAAP net income $342.5M; non-GAAP EPS $1.75.
- GAAP operating income Q2 FY27 $459.7M (vs $290.1M in Q2 FY26). GAAP operating margin 16.8% (10-Q MD&A table).
- **Non-GAAP operating margin 36.6%** (Q2 FY27, per company "Financial and Business Results" deck) — expanded 180bp YoY and 160bp sequentially.

### Data center quarterly revenue series (company deck, official)
| Q3 FY25 | Q4 FY25 | Q1 FY26 | Q2 FY26 | Q3 FY26 | Q4 FY26 | Q1 FY27 | Q2 FY27 |
|---|---|---|---|---|---|---|---|
| $1,101.1M | $1,365.8M | $1,440.6M | $1,490.5M | $1,517.9M | $1,651.3M | $1,832.7M | **$2,171.5M** |

Source: "Q2 FY27 Additional Information" PDF (Marvell IR, Aug 27, 2026) → https://d1io3yog0oux5.cloudfront.net/_6b3a348c4b3086f910c6504b5c8068c0/marvell/db/3734/35391/additional_earnings_information/MRVL+Q2%2727+Additional+Information_FINAL+v2.pdf **(HTTP 200)**

### Q3 FY27 guidance (company figures)
- Net revenue **$3.150B ± 5%**
- GAAP gross margin **52.9%–53.9%**; **non-GAAP gross margin 57.5%–58.5%** (midpoint 58.0% = **~90bp sequential compression** from Q2's 58.9%)
- GAAP opex ~$1.015B; non-GAAP opex ~$655M
- Basic shares 900M; diluted shares 921M
- GAAP diluted EPS **$0.53 ± $0.05**; **non-GAAP diluted EPS $1.10 ± $0.05**
- Q3 data center revenue guided **>20% q/q and ~75% y/y**; FY27 data center **~+60% y/y** (raised from prior ~+50%)
- Company: "the forecasted acceleration of our custom business creating the sequential headwind in the fiscal third quarter" — CFO Dan Durn, Q2 FY27 call (quoted via Roic AI transcript, see §7).

### Balance sheet & cash at Aug 1, 2026 (company figures)
| Item | Aug 1, 2026 | Jan 31, 2026 |
|---|---|---|
| Cash & cash equivalents | **$3,932.8M** | $2,638.8M |
| Short-term debt | **$0** | $499.8M |
| Long-term debt | **$4,962.9M** | $3,970.8M |
| **Total debt** | **$4,962.9M** | $4,470.6M |
| **Net debt (total debt − cash)** | **$1,030.1M** | $1,831.8M |
| Goodwill | $13,873.9M | $11,062.2M |
| Total assets | $27,554.6M | $22,285.3M |
| Total stockholders' equity | $18,531.6M | $14,308.4M |

Source: Q2 FY27 PR condensed balance sheet (URL above) + 10-Q.

### Free cash flow — VERIFIED BOTH WAYS
- **Trailing-twelve-month FCF = $1,722.8M** (sum of last 4 quarterly yfinance `Free Cash Flow` rows: Q2 FY27 $474.3M + Q1 FY27 $482.6M + Q4 FY26 $258.3M + Q3 FY26 $507.6M).
- TTM operating cash flow **$2,200.3M**; TTM capital expenditure **$477.5M**.
- Confirmed convention: yfinance Capex rows are negative; FCF = OCF + capex. Cross-check: $605.5M − $131.2M = $474.3M ✓.
- Q2 FY27 capex was $126.7M "purchases of property and equipment" per the cash-flow statement (yfinance rows include intangibles, hence $131.2M).
- Company notes Q2 OCF "reflects higher supplier capacity prepayments in support of future growth"; Marvell is "on pace to make approximately $1 billion of capacity prepayments to suppliers in fiscal 2027."
- Capital return Q2 FY27: **$253.8M** ($200M buybacks + ~$53.8M dividends). H1 FY27 returned $507.7M. **$5.1 billion** remained available for repurchase as of Aug 1, 2026.

### FY27 / FY28 full-year outlook (raised at Q2 FY27, company deck)
- **FY27 revenue: ~+45% y/y to ~$12B** (prior outlook ~$11.5B)
- **FY28 revenue: ~+50% y/y to ~$18B** (~$1.5B above prior outlook)
- **FY28 custom business expected to grow >2x y/y**
- Q3 revenue at guidance midpoint = 15% q/q, >50% y/y
- Source: "Q2 FY27 Financial and Business Results" deck (Marvell IR) → https://d1io3yog0oux5.cloudfront.net/_6b3a348c4b3086f910c6504b5c8068c0/marvell/db/3734/35391/presentation/2026_08_27_Marvell_Q2_FY27_financial_business_results_FINAL+%281%29.pdf **(HTTP 200)**

---

## 2. CUSTOM SILICON ECONOMICS

### Current size and growth (management-guiding figures)
| Figure | Value | Source |
|---|---|---|
| Custom silicon revenue, FY26 | **~$1.5B** | Q4 FY26 earnings call (Murphy: "to $1.5 billion in fiscal 2026"); corroborated by AInvest ("Marvell's custom ASIC business doubled to roughly $1.5 billion in fiscal 2026") |
| Custom as % of FY26 revenue | **~18%** (of $8.195B FY26 revenue) | Investing.com analysis, Aug 14, 2026 |
| FY27 custom growth | **">20% y/y", i.e. ≥~$1.8B** | Management, Q4 FY26 call + Investing.com Aug 14, 2026 |
| FY28 custom growth | **">2x y/y" / "more than double"** | Company Q2 FY27 FBR deck ("Expect custom business to grow >2x y/y in FY28"); Reuters Aug 27, 2026 (Murphy) |
| FY26 total revenue (context) | **$8,195M** | Q4 FY26 release / 10-K |

- **Investing.com (Emeline Ozhan, Aug 14, 2026):** "Custom silicon already generates approximately $1.5 billion of annual revenue, representing close to **18% of Marvell's FY26 sales**. Management expects the business to grow by **more than 20% in FY27** and **more than double in FY28**, supported by programs already secured with the **four largest hyperscalers**."
  → https://www.investing.com/analysis/marvells-investor-day-is-custom-silicon-the-next-multibilliondollar-business-200685832
  **(NOTE: the task brief dated this "~Oct 2026". It is actually dated Aug 14, 2026. Correct the date in the article.)**
- **Reuters (Aug 27, 2026):** "The company now expects revenue to grow about **45% in fiscal 2027 to roughly $12 billion**, up from its prior forecast of about $11.5 billion… It also forecast **fiscal 2028 revenue of about $18 billion**, up from its prior target of about $16.5 billion." Murphy said custom-chip revenue would **more than double next year** and there was **"upside bias"** to its prior **$10 billion-plus fiscal 2029 target**; he declined to give a new target, **deferring details to its Investor Day scheduled for October 6**.
  → https://www.reuters.com/technology/marvell-technology-forecasts-quarterly-revenue-above-estimates-2026-08-27 **(HTTP 401 — paywalled/bot-blocked; headline + body verified via Yahoo/Quartz syndication)**

### CY2028 TAM — VERIFIED
From the **June 17, 2025 "Custom AI Investor Event"** deck (Marvell):
- **Marvell data center TAM → $94B by CY2028**, **+26% larger** than its prior CY28 estimate ($75B)
- Largest driver: **accelerated custom compute = $55.4B by CY28** (up from $21B in CY23; **53% CAGR**)
  - **Custom XPU: $40.8B** (47% CAGR)
  - **Custom XPU attach: $14.6B**
- **"Custom silicon on track for 25% share of market by 2028"** — i.e. $55.4B custom accelerated compute vs a **$221B** total accelerated-compute market (up from a prior $172B CY28 view)
- Marvell's other CY28 DC TAM components: **interconnect $19.0B** (35% CAGR), **storage $13.2B** (9% CAGR), **switching $6.5B** (17% CAGR)
- Sources: deck PDF → https://www.marvell.com/content/dam/marvell/en/company/assets/marvell-custom-ai-investor-event-2025.pdf **(HTTP 403 to curl — Cloudflare bot-block; contents verified via search-engine index of the deck)**; Marvell blog "Inside Marvell's Expanding Custom Silicon Opportunity" → https://www.marvell.com/blogs/inside-marvell-expanding-custom-silicon-opportunity.html **(HTTP 403 to curl)**

### Pipeline / share ambition
- **>50 custom opportunities (sockets) across >10 customers, ~$75B lifetime revenue pipeline** — company, Custom AI Investor Event (June 2025); repeated by Barclays: "a $75 billion revenue pipeline consisting of >50 sockets across over 10 customers," but "these potential wins won't contribute to revenue until 2028 at the earliest" (Yahoo Finance/Investing.com, June 2025).
- **Marvell share of its DC TAM: ~13% in 2024 → targeting 20% of the $94B CY28 TAM.** Morgan Stanley: company is "targeting 20% share, with >50% of data center revenue eventually from custom." A mechanical 20% of $55.4B ≈ **$11B+** potential annual custom-compute revenue (Investing.com). **Treat as market-share ambition, not guidance.**
- Company previously shelved an earlier **investor day** (press release: "Marvell to Host Webinar on the Future of Custom Silicon Technology for AI Infrastructure; **Postpones Investor Day**") — https://investor.marvell.com/news-events/press-releases/detail/98/... — hence Oct 6, 2026 is a **rescheduled** event, not the first.

### IP stack Marvell says underpins custom silicon
Company deck, Q2 FY27: "**Die-to-die I/O · SerDes · Dense SRAM · Custom HBM · Packaging · PIVR · Photonics**" — the differentiated blocks Marvell contributes to XPU and XPU-attach designs, spanning 100s of km (DCI) → ~1 km → meters → millimetres (D2D).

---

## 3. COMPETITIVE DYNAMICS: MARVELL vs BROADCOM

### Market share in custom AI ASIC design services
| Source | Broadcom | Marvell |
|---|---|---|
| Bloomberg Intelligence (via AIMultiple) | **60%–80%** | **20%–25%** |
| Hashrate Index (2026) | **~70%** | **20–25%** |
| 24/7 Wall St (Aug 17, 2026) | ~70% | ~20% |

- **Broadcom + Marvell together control roughly 95% of the custom AI ASIC co-design market** — Tom's Hardware, "The custom AI ASIC state of play (May 2026)" → https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia

### Customer map (as of 2026)
- **Broadcom XPU customers:** Google (TPU, since 2016, long-term supply agreement through **2031**), Meta (MTIA — multi-year partnership announced **April 14, 2026**, initial commitment >1 GW), OpenAI, **Anthropic**, and new in 2026, **Apple**.
- **Marvell:** **AWS (Trainium)**, **Microsoft (Maia)** — and, new in 2026, **Google** (see §4).
- Structural read (Hashrate Index): "Both of Marvell's primary hyperscaler customers are in catch-up mode relative to Google TPU — which is Broadcom's. … Broadcom enables the leader, Marvell enables the chasers."
- Competitive flare-up: **Broadcom secured an exclusive OpenAI networking deal**, with analysts flagging near-term pressure on Marvell's networking business (Hashrate Index).

### Scale gap — the numbers
| Metric | Broadcom (Q3 FY26, rpt Sept 2, 2026) | Marvell (Q2 FY27, rpt Aug 27, 2026) |
|---|---|---|
| Total quarterly revenue | **$29.591B** (+86% y/y) | **$2.739B** (+37% y/y) |
| AI/custom-related quarterly revenue | **$16.7B AI semis** (+221% y/y) | Custom embedded inside **$2.1715B** data center |
| Gross margin (recent) | **67.3%** | **52.1%** (Q1 FY27) / **53.1%** (Q2 FY27) GAAP |
| Operating margin | **~49% TTM** | **~14.5–16.8% TTM/quarter** |
| Quarterly FCF | **$10.26B** | **$474.3M** |
| AI revenue roadmap | FY26 $58B → **FY27 ~$115B** → **FY28 ~$230B** | Marvell FY27 ~$12B total, FY28 ~$18B total |
| AI backlog | $73B (last explicit disclosure, Q4 FY25); "order backlog stretching to 2028" (Q3 FY26) | Not disclosed |

Sources: Broadcom Q3 FY26 release (https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial); The Signal internal AVGO dossier (`.dossiers/avgo-anthropic-42b-2026/brief.md`); Tom's Hardware; 24/7 Wall St.

### The ACTUAL differentiator Marvell claims
Marvell's claimed edge is **not** scale — it is **interconnect physics/IP depth**, vertically integrated across the link:
1. **SerDes & analog**: 224G SerDes leadership; PIVR (integrated voltage regulation) for multi-kilowatt XPUs.
2. **Optics**: 2nm coherent + PAM4 DSPs (Nova → Ara → **Libra 800G 2nm** → **Electra 1.6T 2nm**), COLORZ 1600 (industry-first 1.6T ZR/ZR+ pluggable), **102.4T CPO platform**, silicon photonics, and now **plasmonics** (Polariton).
3. **Memory/storage adjacent**: Structera CXL, Bravera SSD controllers, custom HBM, die-to-die I/O, dense SRAM.
4. **Switching**: Teralynx T100 (102 Tbps), UALink scale-up switches, PCIe 6.0 CXL switches (XConn).
5. **Ecosystem compatibility**: NVLink Fusion-compatible custom XPUs (NVIDIA).

**Matt Murphy**, NVLink Fusion release (March 31, 2026): *"Our expanded partnership with NVIDIA reflects the growing importance of high-speed connectivity, optical interconnect and accelerated infrastructure in scaling AI. By connecting **Marvell's leadership in high-performance analog, optical DSP, silicon photonics and custom silicon** to NVIDIA's expanding AI ecosystem through NVLink Fusion, we are enabling customers to build scalable, efficient AI infrastructure."*

**Sandeep Bharathi**, President, Data Center Group (Celestial AI announcement, Dec 2, 2025): *"By combining our **UALink scale-up switch roadmap** and Celestial AI's breakthrough optical scale-up interconnect, we will enable customers to build AI systems that scale beyond the limits of copper…"*

**Will Chu**, EVP/GM Custom Cloud Solutions (Aug 4, 2026): *"AI infrastructure is moving beyond isolated servers to systems where compute, memory and connectivity operate seamlessly together… memory must scale more independently of compute…"*

**The honest framing:** Broadcom sells breadth of platform + scale + software annuity; Marvell sells **attach economics** — it monetises the *chips around the XPU* (optics, SerDes, CXL, NICs, memory, switching) as much as the XPU itself. The company's own model splits custom into **XPU** and **XPU attach**, and its CY28 XPU-attach TAM ($14.6B) is the piece Broadcom does not dominate.

---

## 4. CELESTIAL AI — STATUS: **CLOSED** (verified, primary source)

| Item | Value | Verification |
|---|---|---|
| Announced | **Dec 2, 2025** — definitive agreement ("Agreement and Plan of Reorganization dated December 2, 2025") | SEC EX-99.1 → https://www.sec.gov/Archives/edgar/data/1835632/000119312525305289/d34367dex991.htm **(HTTP 200)** |
| **Closed** | **February 2, 2026** | **10-Q, Note 4:** "On February 2, 2026, the Company completed the acquisition of Celestial AI, Inc. … for a total purchase consideration of **$3.5 billion**." (HTTP 200, SEC) |
| Announced upfront value | **~$3.25B** = $1.0B cash + ~27.2M shares valued at $2.25B | EX-99.1, Dec 2, 2025 |
| **Accounting value at close** | **$3.5B** total purchase consideration | 10-Q Note 4 |
| Earnout / contingent consideration | **up to ~27.2M shares (~$2.25B)** at announcement; booked at **$315.8M** fair value at acquisition date; **max settlement ~$233.0M cash + ~22.4M shares**. Milestones: 1/3 vests at **$500M cumulative revenue by end of FY29**; full earnout if **cumulative revenue by end FY29 exceeds $2.0B** | EX-99.1 + 10-Q Note 4/Note 6 |
| Revenue expectation | Meaningful contributions from **2H FY28**; **$500M annualised run-rate by Q4 FY28**; **doubling to $1B run-rate by Q4 FY29** | EX-99.1, Dec 2, 2025 |
| First-gen product | **Photonic Fabric chiplet**: **16 Tbps** in a single chiplet = **10x** today's state-of-the-art 1.6T scale-out ports; co-packaged with XPUs and scale-up switches | EX-99.1 |
| Technology | Optical I/O to any point on the die (not just die edge) using 3D co-packaged photonics; >2x power efficiency vs copper; nanosecond-class latency; thermal stability enabling vertical 3D integration and freeing die-edge beachfront for more HBM | EX-99.1 |
| Customer signal | **AWS**, Dave Brown, VP Compute & ML Services: *"At AWS, we aim to be at the forefront of major technology transitions, and we believe optical interconnects will play an important role in the future of AI infrastructure."* | EX-99.1 |
| Leadership retained | David Lazovsky (Celestial co-founder/CEO) now **EVP/GM of the Data Center Networking Business Group at Marvell**; Preet Virk, Philip Winterbottom also joined | Celestial deal deck (Dec 2025); Marvell AI Infra Summit PR (Sept 9, 2026) |
| Related — **XConn Technologies** | Closed **February 10, 2026** for **$469.0M**; PCIe/CXL switching silicon; augments Marvell's UALink scale-up switch team | 10-Q Note 4 (HTTP 200) |
| Related — **Polariton Technologies** | Acquired **April 22, 2026**, undisclosed terms; Swiss ETH Zurich spin-off, plasmonics-based silicon photonics for 3.2T+ optical | Marvell newsroom → https://www.marvell.com/company/newsroom/marvell-acquires-polariton-advancing-future-of-optical-connectivity.html |
| Related — **Goodwill** | Celestial + XConn + one immaterial deal collectively added **~$2.8B** to goodwill in Q1 FY27 | 10-Q Note 5 (HTTP 200) |
| Related — **forward stock purchase contract** | April 2026, **$300M notional, 12-month term**, to hedge stock-price exposure on the Celestial contingent consideration. Unrealised gain of $49.9M (Q2) / $131.0M (H1) FY27, booked in Other expense, net | 10-Q Note 6 (HTTP 200) |

**Answer to the research question: Marvell ACQUIRED Celestial AI (not merely partnered). Announced Dec 2, 2025; CLOSED Feb 2, 2026; announced value ~$3.25B ($1.0B cash + ~$2.25B stock) plus up to ~$2.25B earnout; $3.5B total purchase consideration on the balance sheet at close.**
Note: the marvell.com "Marvell Completes Acquisition of Celestial AI" newsroom page (Feb 2, 2026) returns **HTTP 403** to curl (Cloudflare); the SEC 10-Q is the clean primary source.

---

## 5. GOOGLE CUSTOM-CHIP RELATIONSHIP (incl. warrant)

**Primary source:** Form 8-K, event date **Aug 18, 2026**, filed Aug 19, 2026 → https://www.sec.gov/Archives/edgar/data/1835632/000119312526356217/d412696d8k.htm **(HTTP 200)**

Verbatim key terms:
- Commercial agreement between Marvell and **Google LLC dated July 29, 2026** relating to development of custom semiconductor products. "The expanded partnership spans a **comprehensive range of custom silicon programs that attach to the TPU ecosystem, including AI inference accelerators, storage controllers, network interface controllers, memory interface controllers, and near-memory compute.**"
- Marvell issued Google a **warrant to purchase up to 58,970,907 shares** at **$206.58/share** = **$12.18B** if fully exercised (**6.72%** of the 876.9M shares outstanding).
- **1,360,867** "Time-Based Warrant Shares" vest in equal quarterly instalments during the first year.
- The **remaining 57,610,040** shares vest in **240 equal tranches — one tranche per $500M of Custom Products revenue** — based on purchases from Q3 FY27 through the end of FY2033. (240 × $500M = **$120B** implied maximum.)
- Exercisable until **August 18, 2033**; transfer restricted (no transfer other than to controlled affiliates without consent); registration rights granted.

**Corroborating wire coverage:**
- **Reuters (Aug 19, 2026):** deal "could bring roughly **$120 billion in revenue through fiscal 2033**, if Google hits the targets its stake option depends on." Marvell shares jumped nearly 8%; **Broadcom — Google's main custom chip partner until now — fell more than 5%.** → https://www.reuters.com/technology/marvell-grants-google-122-billion-stock-warrant-custom-chip-deal-2026-08-19 **(HTTP 401)**
- **CNBC (Aug 19, 2026):** stock rallied nearly 10%; "That is worth $12.18 billion if fully exercised and will make **Google the fifth-largest investor of Marvell**." → https://www.cnbc.com/2026/08/19/marvell-google-ai-chips.html **(HTTP 200)**
- **Morningstar:** warrant "**fully vesting if it spends a cumulative $120 billion through fiscal 2033**"; reads it as "landing a brand-new blue-chip customer" alongside **existing programs at AWS and Microsoft**.
- **Murphy on the Q2 FY27 call (Reuters, Aug 27):** pressed on why Google revenue would not contribute more materially in FY28, he said the FY28 custom targets **already reflected some** of that revenue; it would contribute **much more significantly in fiscal 2029**. Reuters headlined the session "shares fall as Google deal questions linger."

**Prior internal sourcing:** `articles/posts/mrvl-google-custom-chip-warrant-2026.json` (Aug 19, 2026) — consistent with the 8-K; that article quoted a $189B market cap and $216.00 price, both now stale.

---

## 6. NVIDIA NVLink FUSION ALLIANCE — **CORRECTION TO BRIEF**

- The brief said "Aug 2026 press release." **That is wrong.** Two relevant releases:
  1. **May 19, 2025** — initial "Marvell and NVIDIA to Provide Custom Solutions for Advanced AI Infrastructure" (detail/97). NVIDIA's Shar Narasimhan quote: *"NVLink Fusion extends NVIDIA's open platform to partners like Marvell, enabling hyperscalers to scale out AI factories to millions of GPUs, using custom silicon…"*
  2. **March 31, 2026** — "NVIDIA AI Ecosystem Expands as Marvell Joins Forces Through NVLink Fusion" (detail/1019). **"In addition, NVIDIA has invested $2 billion in Marvell."** → https://investor.marvell.com/news-events/press-releases/detail/1019/nvidia-ai-ecosystem-expands-as-marvell-joins-forces-through-nvlink-fusion **(HTTP 200)**
- **Jensen Huang, March 31, 2026:** *"The inference inflection has arrived. Token generation demand is surging, and the world is racing to build AI factories. Together with Marvell, we are enabling customers to leverage NVIDIA's AI infrastructure ecosystem and scale to build specialized AI compute."*
- **Structure of the $2B — VERIFIED via 10-Q:** On **March 31, 2026** Marvell issued and sold **2.0 million shares of Series A Convertible Preferred Stock** to NVIDIA for **$2.0 billion** (stated value $1,000/share), convertible at **~$91.84/share** into a maximum of **~21.8 million common shares**; **no shares had converted as of Aug 1, 2026**. Dividends paid on an as-converted basis; pro-rata liquidation participation; **no redemption or preemptive rights.** 10-Q also flags governance-adjacent risk: *"because the Series A Preferred Stock was issued to a single significant holder, the concentration of ownership could increase NVIDIA's influence over matters submitted to our stockholders…"*
- Partnership scope: Marvell provides **custom XPUs and NVLink Fusion-compatible scale-up networking**; NVIDIA provides Vera CPU, ConnectX NICs, Bluefield DPUs, NVLink interconnect, Spectrum-X switches, rack-scale AI compute. Also AI-RAN (NVIDIA Aerial) for 5G/6G and joint silicon-photonics work.
- **Canton Fitzgerald** lists "Marvell's exposure to NVIDIA's NVLink Fusion" among the contributors to its expanded $625B addressable-opportunity framing (Sept 28, 2026).

---

## 7. RECENT NEWS (last ~3 weeks, Sept 2026)

| Date | Item | Source / status |
|---|---|---|
| **Sept 9, 2026** | "Marvell to Showcase End-to-End AI Data Center Connectivity Portfolio at AI Infra Summit 2026" (Sept 15–17, Santa Clara). Highlights: **Marvell Photonic Fabric** memory sharing across racks; **RELIANT** interconnect telemetry; **Teralynx T100 102 Tbps** switch; **256-lane PCIe 6.0 switch**; CXL memory solutions; PCIe 6.0 NVMe SSD controller. Keynote "AI Inference at Scale" by **Dave Lazovsky**, EVP/GM Data Center Networking | investor.marvell.com detail/1032 **(HTTP 200)** |
| **Sept 21, 2026** | "Marvell to Showcase Industry-First 2nm Optical Technology Demos … at ECOC 2026" (Málaga, Sept 20–24). Industry-firsts: **2nm 400G/lane optical PAM4**; first live **2nm 800G ZR/ZR+ with MACsec** (Libra DSP); first **2nm 1.6T ZR and coherent-lite O-band**. **102.4T CPO platform** demo with 200G-per-lane silicon photonics, 38 demos total. Quote: **Xi Wang**, SVP/GM Connectivity BU | investor.marvell.com detail/1034 **(HTTP 200)** |
| **Sept 22, 2026** | **AT&S expands long-term agreement with Marvell** to increase advanced IC-substrate capacity at its Kulim, Malaysia site (Plant 2 fit-out + new facility for IC substrate cores and advanced packaging). **Marvell is the previously-unnamed customer** behind AT&S's Kulim expansion. Quote: Michael Mertin, CEO of AT&S | ats.net **(HTTP 200)**; evertiq.com; Financial Times Deutschland/ad-hoc-news |
| **Sept 25, 2026** | Board declares quarterly dividend **$0.06/share**, payable **Oct 29, 2026** to holders of record Oct 9, 2026 (incl. preferred on an as-converted basis) | Form 8-K mrvl-20260925.htm **(HTTP 200)** |
| **Sept 28, 2026** | **Cantor Fitzgerald** (C.J. Muse) raises PT to **$330** from $300, keeps **Neutral**: Investor Day could reframe Marvell's DC opportunity at **up to $625B by 2030**, supporting a **40–45% revenue CAGR** and **at least $20 EPS in calendar 2030**. Drivers: XPU attach, Celestial AI/CPO, 1.6T optics, Ethernet switching, NVLink Fusion. **Morgan Stanley** raises PT to **$268** from $246, stays **Equal Weight**, expects the event to frame **FY2030 revenue above $40B**. **RBC** expects Marvell to lift its **FY29 AI revenue estimate by at least $2B**, largely on the Google deal | Yahoo Finance/Stocktwits; The Inference; Finimize |
| **Sept 28, 2026** | "Marvell Technology (MRVL) Starts Custom AI Chip Shipments And Eyes Higher Forecasts" | Yahoo Finance (Google News) |
| **Sept 29, 2026** | **Marvell wins 2026 EDGE Award** (Electronic Design) — **COLORZ 1600 2nm 1.6T ZR/ZR+ pluggable optical platform**, Machine Vision and Optical Components & Systems category | Marvell blog dated Sept 29, 2026 → https://www.marvell.com/blogs/marvell-wins-edge-award-for-colorz-1600-2nm-16t-zrzr-pluggable-optical-platform.html **(HTTP 403 to curl — Cloudflare; date + content verified via search index and Marvell's own social posts)** |
| **Sept 30, 2026** | **Citi upgrade** ahead of Investor Day; stock +5% | FXLeaders |
| **Oct 2, 2026** | "Marvell expands AT&S deal. Marvell Technology stock gains 2.87 percent" (Xetra/Lang & Schwarz EUR quote €245.18) | ad-hoc-news.de |
| **Aug 4, 2026** | "Marvell Advances AI Memory Infrastructure Portfolio to Accelerate Agentic AI Inference" (FMS 2026) — **Bravera SC6 PCIe 6.0 SSD controller** (2x SC5, sampling Q4 2026, NAND-agnostic); **Structera X** CXL memory expansion; **Photonic Fabric** memory modules/NIC/chiplets enabling **up to 32TB warm KV-cache offload across racks up to 50 metres**, **2–3x higher token throughput**. Quote: Will Chu, EVP/GM Custom Cloud Solutions; Alan Weckel, 650 Group | investor.marvell.com detail/1030 **(HTTP 200)** |

### PRODUCT LINE VERIFICATION (marvell.com nav + releases)
Compute: CXL (Structera), DPUs, Security. Networking: Coherent DSPs (Electra/Libra), Coherent-lite DSPs, Data Center Switches (Teralynx), DCI Optical Modules (COLORZ 400/800/1600), Enterprise Switches, Ethernet Controllers, Ethernet PHYs, Linear Drivers, PAM DSPs, PCIe Retimers, TIAs. Storage: Fibre Channel, HDD, Storage Accelerators, SSD Controllers (Bravera). Custom: ASIC, Marvell Government Solutions. Markets: Data Center, Enterprise, Carrier. Photonic Fabric™ is now a Marvell product page (https://www.marvell.com/ai/photonic-fabric-technology.html).

---

## 8. BEAR CASE MATERIAL (short-seller-grade, sourced)

### 8.1 Customer concentration — **the single strongest bear datum (verbatim)**
**10-Q for Q2 FY27 (period ended Aug 1, 2026), "Sales and Customer Composition":**
> "Our accounts receivable were concentrated with **four customers at August 1, 2026, who represented a total of 72% of gross accounts receivable**, compared with five customers at August 2, 2025, who represented a total of 73%… Net revenue attributable to significant customers including both distributor and direct customers whose revenues represented 10% or more of total net revenue is presented in the following table:"

| Customer | Q2 FY27 | Q2 FY26 | H1 FY27 | H1 FY26 |
|---|---|---|---|---|
| **Customer A (Direct)** | **16%** | 16% | 16% | 16% |
| **Distributor A** | **44%** | 34% | **45%** | 35% |

→ **Two relationships = 60% of Q2 FY27 net revenue; Distributor A alone jumped from 34% to 44% of revenue in a single year.** (Marvell routes much of its hyper-scale business through distributors; the "diverse end customers" defence is the company's own framing — quoted in the same paragraph.)

**10-K risk-factor disclosure (FY26):**
> "during fiscal 2026, there were **two customers (one distributor and one direct customer) whose revenues represented 10% or more of total net revenue**. In addition, net revenue from our **ten (10) largest customers, inclusive of our distributor and direct customers, represented 82% of our total net revenue for fiscal 2026**."

Also: **84% of net revenue in H1 FY27 shipped to customers with operations in Asia** (vs 75–76% a year earlier) — geographic concentration risk on top of customer concentration.

### 8.2 Custom ASIC is structurally lower-margin than Broadcom's platform — already compressing GM
- **Guidance embeds dilution:** Q2 FY27 non-GAAP GM **58.9%** → Q3 FY27 guide midpoint **58.0%** = **~90bp sequential decline**. CFO Dan Durn on the Q2 call: *"the forecasted acceleration of our custom business creating the sequential headwind in the fiscal third quarter."*
- **Needham's Quinn Bolton** asked on the call: *"with margins coming down 90 basis points quarter-on-quarter, is custom the fastest-growing segment within data center that drives that lower margin?"*
- **Zacks (TradingView):** "Marvell Technology's custom AI silicon, including XPUs, which are driving its revenue growth, comes with higher costs associated with manufacturing these chips. **The margin in the AI-focused custom silicon semiconductor business is fundamentally lower, which might further slow down the rate of growth in MRVL's gross margin.**"
- **The gap vs Broadcom:** GAAP gross margin **Marvell 52.1% (Q1 FY27) / 53.1% (Q2 FY27) vs Broadcom 67.3%**; operating margin **~14.5–16.8% vs ~49% TTM**; quarterly FCF **$474M vs $10.26B**. AInvest: *"That 17-percentage-point gap in gross margin … is the difference between a business that is fundamentally a **design-and-integration shop** and one that owns the full IP stack and prices accordingly."* AOL/Yahoo: *"That is the structural reality of bespoke silicon: **hyperscalers hold the leverage.**"*

### 8.3 Vertical-integration / in-housing risk (verbatim from Marvell's own risk factors)
> "risks that **our customers develop their own solutions, vertically integrate which may reduce the need for our products, or acquire fully developed solutions from third parties**; our ability to secure design wins…" — forward-looking statements, Q2 FY27 PR (repeated in the 10-Q risk factors)

Lexical note: Marvell's own description of the custom model concedes IP dependence: *"risks related to the **ASIC business model which requires us to use third-party IP** including the risk that we may lose business or experience reputational harm if third parties, including customers, lose confidence in our ability to protect their IP rights."*

### 8.4 Valuation after a ~205% YTD move
| Metric | MRVL | Context |
|---|---|---|
| Price Oct 2, 2026 close | **$272.29** | +205.1% vs Jan 2, 2026 close ($89.26); +220.9% vs Dec 31, 2025 ($84.86) |
| 52-week range | **$70.69 – $329.88** | currently **17.5% below the high**, **285% above the low** |
| Market cap | **$244.7B** | on 876.93M shares |
| Trailing P/E | **89.6x** | trailing EPS $3.04 |
| Forward P/E | **40.2x** | forward EPS $6.769 |
| Price/Sales (TTM) | **25.9x** | on $9.45B TTM revenue |
| Analyst consensus | **strong_buy**, n=43 opinions | mean PT **$290.97** (+6.9%); high $400; low $210 |
| Beta | **2.253** | |

- Peer comparison, earlier in the cycle (post-AVGO-Q2 FY26): "MRVL trades at a richer **68x forward P/E than AVGO's 33x**, despite posting gross margins of 52% versus Broadcom's 67%" (AOL/Yahoo). **Note the date sensitivity — this snapshot predates the summer drawdown.**
- Barclays caveat: the $75B pipeline wins **"won't contribute to revenue until 2028 at the earliest."**
- Morningstar (post-Q2 FY27): *"We expect longer-term targets through calendar 2030 and more detail on the Google ramp. There could be further upside to our model, **as we don't model in the full $120 billion from Google through 2032.**"*
- Bears' compounding worry: the **NVIDIA $2B preferred** (21.8M shares at $91.84) plus the **Google warrant** (up to 58.97M shares, 6.7%) plus the **Celestial earnout** (up to ~22.4M shares / $233M cash) = **substantial potential dilution** that layers on top of a premium multiple. Marvell says it "intend[s] to continue repurchasing shares to manage dilution."

### 8.5 Macro/structural risk flags in the 10-Q (all verbatim themes)
- "the current level of capital expenditure (capex) on AI infrastructure may not be sustainable over the long term and a significant reduction in AI-related spending will likely harm our financial results"
- Data-centre **siting opposition** (grid/water/noise/rezoning/litigation) could delay deployments
- "**TSMC is currently our sole source foundry for all of our advanced process-node wafers**"; assembly/test/packaging concentrated in Malaysia, Singapore, Taiwan, Canada
- Post-Synopsys–Ansys merger, "**three companies are expected to control approximately 75% of the global EDA market**," raising vendor-concentration risk
- July 2026: "**bipartisan AI oversight legislation was introduced**, which could establish U.S. government oversight over 'cutting-edge AI models' in a manner that may encompass our products"

---

## 9. THE HONEST "WHAT HAS TO HAPPEN TO RE-RATE" DRIVER

**The single cleanest driver: proof that Marvell's custom silicon franchise converts design wins into *revenue and gross margin simultaneously* — i.e. that the FY28 ">2x custom" ramp lands on time without the gross-margin line breaking.**

Concretely, the market needs the **Oct 6 Investor Day** to deliver three things the company has so far declined to give:
1. A **new FY29 revenue target** replacing the "$10B+" placeholder — Murphy himself said there is **"upside bias"** and deferred the number to Oct 6 (Reuters, Aug 27).
2. **Timing detail on the Google ramp** — management says Google contributes "much more significantly in fiscal 2029" than FY28 (Reuters). The $120B / 240-tranche warrant is a *maximum*, not a schedule.
3. **A credible margin bridge** — the bull case only works if gross margin holds ~58% while custom (the lower-margin mix) doubles, which is precisely what the current setup has **not** yet demonstrated (Q3 guide already embeds −90bp).

The mechanical re-rate math the sell side is using: **Cantor** — DC TAM up to **$625B by 2030**, **40–45% revenue CAGR**, **≥$20 EPS in 2030** (PT $330, Neutral). **Morgan Stanley** — event to frame **FY2030 revenue above $40B** (PT $268, Equal Weight). Note that **both houses raised targets without raising ratings** — which is itself the tell that the Street believes the story but not yet the margin.

**One-line framing for the writer:** Marvell has proven the demand (bookings, TAM, warrant-vesting math); what it has *not* proven is that a design-services business can price like a platform business.

---

## 10. yfinance DATA (run with `/home/chino/video-venv/bin/python3`, yfinance 1.4.1, pulled ~2026-10-02 23:0x UTC)

**Last 10 closes (`history(period='10d')`), exact values:**
| Date | Close |
|---|---|
| 2026-09-21 | $257.38 |
| 2026-09-22 | $262.36 |
| 2026-09-23 | $260.90 |
| 2026-09-24 | $258.95 |
| 2026-09-25 | $261.94 |
| 2026-09-28 | $251.90 |
| 2026-09-29 | $263.27 |
| 2026-09-30 | $264.21 |
| 2026-10-01 | $268.08 |
| **2026-10-02** | **$272.29** ← **CONFIRMED article price baseline (Friday close)** |

| Field (exact yfinance name) | Value |
|---|---|
| `currentPrice` / `regularMarketPrice` | 272.29 |
| `regularMarketPreviousClose` | 268.08 |
| `marketCap` | **244,708,294,656** ($244.7B) |
| `sharesOutstanding` | **876,926,613** |
| `trailingPE` | **89.569** |
| `forwardPE` | **40.225** |
| `forwardEps` | **6.769** |
| `trailingEps` | **3.04** |
| `grossMargins` (TTM) | **0.52216 → 52.22%** |
| `operatingMargins` (TTM) | **0.16679 → 16.68%** |
| `profitMargins` (TTM) | 0.27935 → 27.94% |
| `ebitdaMargins` | 0.30161 → 30.16% |
| `totalRevenue` (TTM) | **9,450,300,416** ($9.450B) |
| **TTM revenue, cross-check = sum of last 4 quarterly revenues** | 2,739.3 + 2,417.8 + 2,218.7 + 2,074.5 = **9,450.3M → MATCHES exactly** |
| `fiftyTwoWeekLow` | **70.69** |
| `fiftyTwoWeekHigh` | **329.88** |
| `recommendationKey` | **"strong_buy"** |
| `numberOfAnalystOpinions` | **43** |
| `targetMeanPrice` | **290.9704** |
| `targetHighPrice` | **400.0** |
| `targetLowPrice` | **210.0** |
| `enterpriseValue` | 236,432,654,336 ($236.4B) |
| `beta` | **2.253** |
| `dividendYield` | 0.09% (declared $0.06/qtr) |
| `priceToSalesTrailing12Months` | **25.894** |
| `sector` / `industry` | Technology / Semiconductors |

**FCF TTM (sum of last 4 `quarterly_cashflow` `Free Cash Flow` rows) = $1,722.8M.** Convention verified: the `Free Cash Flow` row = `Operating Cash Flow` + `Capital Expenditure` where Capex is **negative**, e.g. Q2 FY27: 605.5 + (−131.2) = **474.3M** ✓.

| Quarter | OCF ($M) | Capex ($M) | FCF ($M) |
|---|---|---|---|
| Q2 FY27 (2026-07-31) | 605.5 | −131.2 | **474.3** |
| Q1 FY27 (2026-04-30) | 638.8 | −156.2 | **482.6** |
| Q4 FY26 (2026-01-31) | 373.7 | −115.4 | **258.3** |
| Q3 FY26 (2025-10-31) | 582.3 | −74.7 | **507.6** |
| **TTM** | **2,200.3** | **−477.5** | **1,722.8** |

**Price-performance math (computed):**
- vs Jan 2, 2026 close ($89.259): **+205.1%**
- vs Dec 31, 2025 close ($84.855): **+220.9%**
- vs 52-wk high $329.88: **−17.5%**
- vs 52-wk low $70.69: **+285.2%**

**Cross-check against third party:** StockAnalysis.com showed (same day) market cap $241.40B, revenue (ttm) $9.45B, shares out 876.93M, PE 92.56, forward PE 50.49, beta 2.25, analysts "Strong Buy", PT $290.97, 52-wk 70.69–329.88. **Revenue, share count, 52-week range and PT match yfinance exactly; market cap and P/E differ slightly due to intraday snapshot timing — use the yfinance values above as the baseline.**

**Note on the Google warrant's accounting:** The warrant was issued Aug 18, 2026, i.e. inside Q3 FY27 — so it does **not** appear in the Q2 FY27 balance sheet. The 10-Q's diluted share count (921.2M) does not include it.

---

## 11. QUOTE BANK (each with its source)

| Speaker | Quote | Source |
|---|---|---|
| Matt Murphy, Chairman & CEO | "Marvell delivered record second-quarter fiscal 2027 revenue of $2.739 billion, up 37% year over year… where revenue growth accelerated to 46% year over year… **AI-related bookings remain exceptionally robust**… we are again raising our revenue outlook for both fiscal 2027 and fiscal 2028… **a significant acceleration in our Custom business beginning in the second half of fiscal 2027.**" | Q2 FY27 PR, Aug 27, 2026 |
| Matt Murphy | "custom-chip revenue would **more than double next year**"; "**upside bias**" to the prior $10B+ FY29 target; declined a new number, **deferring to Investor Day Oct 6** | Reuters, Aug 27, 2026 |
| Matt Murphy (on Google timing) | FY28 custom targets already reflected some Google revenue; it would contribute **much more significantly in fiscal 2029** | Reuters, Aug 27, 2026 |
| Dan Durn, CFO | "the forecasted **acceleration of our custom business creating the sequential headwind in the fiscal third quarter**" | Q2 FY27 earnings call |
| Jensen Huang, NVIDIA | "The inference inflection has arrived. Token generation demand is surging, and the world is racing to build AI factories. Together with Marvell, we are enabling customers to leverage NVIDIA's AI infrastructure ecosystem and scale to build specialized AI compute." | NVLink Fusion PR, Mar 31, 2026 |
| Matt Murphy | "By connecting **Marvell's leadership in high-performance analog, optical DSP, silicon photonics and custom silicon** to NVIDIA's expanding AI ecosystem through NVLink Fusion, we are enabling customers to build scalable, efficient AI infrastructure." | NVLink Fusion PR, Mar 31, 2026 |
| Matt Murphy | "The acquisition of Celestial AI is a **transformative step** in Marvell's evolution and expands our leadership in AI connectivity, as **scale-up becomes the next frontier** in AI infrastructure." | EX-99.1, Dec 2, 2025 |
| Sandeep Bharathi, President, Data Center Group | "By combining our UALink scale-up switch roadmap and Celestial AI's breakthrough optical scale-up interconnect, we will enable customers to build AI systems that **scale beyond the limits of copper**." | EX-99.1, Dec 2, 2025 |
| David Lazovsky, Celestial AI co-founder/CEO | "Marvell is the ideal home for our Photonic Fabric, with the scale, customer relationships, and connectivity leadership to take this platform into high-volume production." | EX-99.1, Dec 2, 2025 |
| Dave Brown, VP Compute & ML Services, AWS | "At AWS, we aim to be at the forefront of major technology inflections, and we believe **optical interconnects will play an important role** in the future of AI infrastructure." | EX-99.1, Dec 2, 2025 |
| Will Chu, EVP/GM Custom Cloud Solutions | "AI infrastructure is moving beyond isolated servers to systems where compute, memory and connectivity operate seamlessly together… **memory must scale more independently of compute**." | Memory Infra PR, Aug 4, 2026 |
| Xi Wang, SVP/GM Connectivity BU | "AI data center operators need optical interconnect technologies that deliver higher bandwidth, lower power and greater security across every part of the network." | ECOC PR, Sept 21, 2026 |
| Michael Mertin, CEO, AT&S | "Marvell Technology is one of the semiconductor industry's leading innovators in AI and data infrastructure, and together we are well positioned to capture the significant opportunities created by the global build-out of AI infrastructure." | AT&S release, Sept 22, 2026 |
| Robert O'Donnell, chief analyst, TECHnalysis Research | "I believe expectations around custom AI accelerator projects are **riding very high**, especially given the recent news about the Broadcom and OpenAI work on Jalapeno." | Reuters, Aug 27, 2026 |
| Quinn Bolton, Needham (analyst) | "with margins coming down 90 basis points quarter-on-quarter, is custom the fastest-growing segment within data center that drives that lower margin?" | Q2 FY27 call |

---

## 12. VERIFIED LINK LIST (HTTP status as tested 2026-10-02)

**HTTP 200 — safe to cite**
1. Marvell Q2 FY27 results PR — https://investor.marvell.com/news-events/press-releases/detail/1031/marvell-technology-inc-reports-second-quarter-of-fiscal-year-2027-financial-results
2. Marvell Investor Day announcement PR (Aug 3, 2026) — https://investor.marvell.com/news-events/press-releases/detail/1029/marvell-technology-inc-announces-conference-call-to-review-second-quarter-of-fiscal-year-2027-financial-results-announces-investor-day-on-october-6-2026
3. MRVL 10-Q (period ended 2026-08-01) — https://www.sec.gov/Archives/edgar/data/1835632/000183563226000025/mrvl-20260801.htm
4. MRVL 8-K, Google warrant (Aug 18/19, 2026) — https://www.sec.gov/Archives/edgar/data/1835632/000119312526356217/d412696d8k.htm
5. Celestial AI EX-99.1 (Dec 2, 2025) — https://www.sec.gov/Archives/edgar/data/1835632/000119312525305289/d34367dex991.htm
6. NVIDIA/Marvell NVLink Fusion + $2B PR (Mar 31, 2026) — https://investor.marvell.com/news-events/press-releases/detail/1019/nvidia-ai-ecosystem-expands-as-marvell-joins-forces-through-nvlink-fusion
7. Marvell AI Memory Infrastructure PR (Aug 4, 2026) — https://investor.marvell.com/news-events/press-releases/detail/1030/marvell-advances-ai-memory-infrastructure-portfolio-to-accelerate-agentic-ai-inference
8. Marvell AI Infra Summit PR (Sept 9, 2026) — https://investor.marvell.com/news-events/press-releases/detail/1032/marvell-to-showcase-end-to-end-ai-data-center-connectivity-portfolio-at-ai-infra-summit-2026
9. Marvell ECOC 2nm PR (Sept 21, 2026) — https://investor.marvell.com/news-events/press-releases/detail/1034/marvell-to-showcase-industry-first-2nm-optical-technology-demos-for-ai-data-center-infrastructure-at-ecoc-2026
10. CNBC, Marvell/Google warrant (Aug 19, 2026) — https://www.cnbc.com/2026/08/19/marvell-google-ai-chips.html
11. AT&S–Marvell expanded agreement (Sept 22, 2026) — https://ats.net/en/ir-news/ats-and-marvell-technology-expand-collaboration-to-support-next-generation-ai-infrastructure
12. Marvell IR calendar / Investor Day event — https://investor.marvell.com/news-events/ir-calendar/detail/20261006-marvell-investor-day-2026

**HTTP 401/403 — paywalled or Cloudflare bot-block (fine for a link list, cannot be curl-verified)**
13. Reuters, "Marvell raises annual forecasts, but shares fall as Google deal questions linger" (Aug 27, 2026) — https://www.reuters.com/technology/marvell-technology-forecasts-quarterly-revenue-above-estimates-2026-08-27 — **401**
14. Reuters, "Marvell gives Google option to buy $12.2 billion stake in custom AI chip deal" (Aug 19, 2026) — https://www.reuters.com/technology/marvell-grants-google-122-billion-stock-warrant-custom-chip-deal-2026-08-19 — **401**
15. Marvell Custom AI Investor Event deck (June 17, 2025) — https://www.marvell.com/content/dam/marvell/en/company/assets/marvell-custom-ai-investor-event-2025.pdf — **403**
16. Marvell blog, "Inside Marvell's Expanding Custom Silicon Opportunity" — https://www.marvell.com/blogs/inside-marvell-expanding-custom-silicon-opportunity.html — **403**
17. Marvell blog, COLORZ 1600 EDGE Award (Sept 29, 2026) — https://www.marvell.com/blogs/marvell-wins-edge-award-for-colorz-1600-2nm-16t-zrzr-pluggable-optical-platform.html — **403**
18. Marvell newsroom, Polariton acquisition (Apr 22, 2026) — https://www.marvell.com/company/newsroom/marvell-acquires-polariton-advancing-future-of-optical-connectivity.html — **403**
19. Marvell newsroom, Celestial AI completion (Feb 2, 2026) — https://www.marvell.com/company/newsroom/marvell-completes-acquisition-of-celestial-ai.html — **403**

**No 404s encountered — no link needs to be excluded.**

---

## 13. UNVERIFIED / CAVEATS — READ BEFORE WRITING

1. **The Investor Day has not happened yet.** Everything about Oct 6 is *expectation*, not result. Cantor's $625B/2030 TAM, Morgan Stanley's "FY2030 revenue above $40B," and RBC's "+$2B FY29 AI revenue" are **analyst forecasts**, not Marvell guidance. Label them as such.
2. **Custom silicon revenue is never broken out by Marvell.** The ~$1.5B / ~18% of FY26 figures come from management's verbal Q4 FY26 call commentary as reported by third parties (Investing.com, AInvest). Marvell reports only "Data center" ($2,171.5M in Q2 FY27) and "Communications and other." Do **not** present custom revenue as a company-reported line item.
3. **The "$120B from Google"** is the *maximum* implied by 240 vesting tranches × $500M of Custom Products revenue through FY2033. It is a warrant-vesting threshold, not a purchase order, backlog, or guidance. Morningstar explicitly says it does **not** model the full $120B.
4. **Celestial AI headline value is ambiguous by design.** Announced upfront ≈$3.25B (Dec 2025); **$3.5B total purchase consideration recorded at close** (10-Q). Use $3.5B for balance-sheet accuracy and note $3.25B as the announcement figure. Earnout booked at $315.8M fair value but has a **maximum settlement of ~$233.0M cash + ~22.4M shares** — the announced "up to $2.25B" is a ceiling, not a liability.
5. **Marvell's market share in custom ASIC (20–25%)** comes from **Bloomberg Intelligence estimates as relayed by third parties** (AIMultiple, Hashrate Index) — not from Marvell or Broadcom filings.
6. **The exact date of the 52-week high ($329.88)** was not isolated. **UNVERIFIED.** Report the range only.
7. **Marvell's Investor Day agenda/content is not public in advance.** What will be announced is unknown. **UNVERIFIED.**
8. **"Four largest hyperscalers"** as Marvell custom customers (Investing.com, Aug 14, 2026) — names not given by Marvell. Marvell's publicly confirmed/named programs are **Google, AWS (Trainium), Microsoft (Maia)**. A fourth is **UNVERIFIED** (some coverage implies Meta; not confirmed by any primary source I located).
9. **The brief's premise that the NVLink Fusion press release was Aug 2026 is incorrect.** It was **May 19, 2025** (initial) and **March 31, 2026** ($2B investment). Use the March 2026 date.
10. **The brief's dating of the Investing.com custom-silicon analysis as "~Oct 2026" is incorrect** — it is **August 14, 2026**.
11. **The "$75B lifetime revenue pipeline" / ">50 opportunities"** figures are from the **June 2025** Custom AI Investor Event. No fresher company-disclosed pipeline number was found. **There is a risk these are stale** — a new number may come at the Oct 6 Investor Day.
12. **Custom-silicon-specific gross margin** is not disclosed by Marvell. The "custom is lower-margin" claim is supported by (a) the guided 90bp sequential GM decline attributed by the CFO to custom ramp, and (b) third-party (Zacks) characterisation — not by a company-disclosed segment margin.
13. **Marvell's fiscal year ends late January/early February.** FY27 ends ~Jan 29, 2027; FY28 ends ~Jan 28, 2028. Do not conflate FY27 with calendar 2026 in the article.
14. **Marvell's Q2 FY27 dividend/quarterly figures** were cross-checked between the PR and the 10-Q; the PR's balance sheet omits the "January 31, 2026 total debt" line ($4,470.6M) shown in the FBR deck — both are correct as of their own snapshot.
15. **StockAnalysis.com and ad-hoc-news market caps ($241.4B, $234.8B)** differ from yfinance's $244.7B. Use yfinance ($244.7B at the $272.29 close) and note the discrepancy is snapshot timing.

---

## 14. SUGGESTED "KEY METRICS" BLOCK FOR THE ARTICLE JSON

| Metric | Value |
|---|---|
| MRVL Price | $272.29 (Oct 2, 2026 close) |
| Market Cap | $244.7B |
| Forward P/E | 40.2x |
| Total Revenue (TTM) | $9.45B |
| Q2 FY27 Revenue | $2.739B (+37% y/y) |
| Data Center Revenue | $2.172B (+46% y/y, 79% of total) |
| Non-GAAP Gross Margin | 58.9% |
| Q3 FY27 Non-GAAP EPS Guide | $1.10 ± $0.05 |
| FY27 / FY28 Revenue Outlook | ~$12B / ~$18B |
| 52-Week Range | $70.69 – $329.88 |
| Analyst Consensus | Strong Buy (43 opinions) |
| Analyst Target Mean | $290.97 |

*All figures as of the Oct 2, 2026 close unless labelled as company guidance.*
