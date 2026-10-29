# OKLO — Verified Fact Dossier

**Subject:** Oklo Inc. (NYSE: OKLO)
**Hook:** FERC rejects Oklo's complaint seeking reinstatement of its 750 MW Virginia project into PJM's interconnection study cycle (order issued Thu 2026-09-24; reported Fri 2026-09-25 by Utility Dive). Same day, UBS cut its OKLO price target.
**Dossier date:** Sunday 2026-09-27 (markets closed — baseline = Friday 2026-09-25 close)
**Proposed slug:** `oklo-ferc-pjm-interconnection-queue-2026` (already verified unique)
**Data sources:** yfinance (`/home/chino/video-venv/bin/python3`), Utility Dive, FERC eLibrary API, SEC EDGAR (10-Q / 8-K / 424B5), Oklo newsroom, MarketBeat, Google News RSS.

> **ARTICLE BODY RULE:** No exact share prices and no market-cap dollar figures in the article body. All prices/market-cap numbers below are for the stats card and for *relative* framing only.

---

## 1. YFINANCE DATA (as of Fri 2026-09-25 close)

### Price (stats card)
| Field | Value |
|---|---|
| **Fri 2026-09-25 close** | **$38.04** (open 38.60, high 39.12, low 37.54, volume 6,763,000) |
| Prior close 2026-09-24 | $38.29 |
| Day change | −$0.25 (−0.65%) |
| 52-week low | $34.38 |
| 52-week high | $193.84 |
| 2026 high | $115.72 (2026-01-09 — the Meta announcement day) |
| 50-day avg / 200-day avg | $41.25 / $60.93 |

### Last 6 closes (`history(period='10d', auto_adjust=False)`)
```
Date         Open    High    Low     Close   AdjClose  Volume
2026-09-18   39.90   40.30   37.51   38.00   38.00     13,843,900
2026-09-21   39.15   40.86   39.08   40.18   40.18     11,447,600
2026-09-22   40.10   41.29   39.33   40.45   40.45      8,240,500
2026-09-23   40.21   40.37   38.76   38.82   38.82      7,280,000
2026-09-24   38.35   38.63   37.56   38.29   38.29      7,352,300
2026-09-25   38.60   39.12   37.54   38.04   38.04      6,763,000   <-- FRIDAY CLOSE
```
**Friday 2026-09-25 close = $38.04 CONFIRMED.**

### How far off the high (RELATIVE framing — safe for article body)
- **−80.4% from the 52-week high** ($193.84, set 2025-10-15) → less than one-fifth of its peak.
- **−67.1% from the 2026 high** ($115.72 on 2026-01-09).
- **−47.0% year-to-date** (2025-12-31 close $71.76 → $38.04). Cross-checks against EBC Financial Group's "down 47% in 2026" (2026-09-25).
- Only **+10.7% above its 52-week low** ($34.38, set 2026-09-14 — eleven days before the FERC ruling).

### Peer context (1-year, same yfinance pull) — article-safe relative framing
| Ticker | Off 1-yr high |
|---|---|
| OKLO | −80.4% |
| SMR (NuScale) | −85.3% |
| NNE (Nano Nuclear) | −72.1% |
| LEU (Centrus) | −68.3% |
| XE (X-Energy) | −59.4% |
| UEC (Uranium Energy) | −53.7% |
| CEG (Constellation) | −36.2% |
| VST (Vistra) | −36.2% |

**Read:** advanced-nuclear/SMR names are down far harder than the merchant/utility AI-power names. OKLO sits in the middle-bottom of the nuclear complex, not alone — but it is one of the few that just lost a regulatory ruling *and* a price target on the same day.

### Valuation / consensus (stats card)
| Field | yfinance | MarketBeat (cross-check) |
|---|---|---|
| Market cap | **$7,076,111,576** (≈$7.08B) | — |
| Shares outstanding | 186,017,650 | — |
| Forward P/E | **−36.78** (negative — no forward earnings; must be reported as n/a) | — |
| Trailing P/E | None (no earnings) | — |
| **TTM revenue** | **$1,210,000** (≈$1.21M) | — |
| Total cash (yf) | $2,465,157,888 | — |
| Total debt | $4,146,000 | — |
| Free cash flow (yf field) | −$239,324,880 | — |
| Recommendation key | `buy` | "Moderate Buy" |
| Recommendation mean | 2.08 (buy) | — |
| Number of analysts | 20 | 23 |
| Target mean | **$76.43** | **$82.44** (116.8% upside) |
| Target low | $14.00 | $41.00 |
| Target high | $130.00 | $130.00 |

**⚠️ Discrepancy to note explicitly:** yfinance's target **low of $14.00** conflicts with MarketBeat's low of **$41.00** (which is the fresh UBS target). yfinance's low is likely a stale outlier target inside its 20-analyst window. MarketBeat's rating mix: 1 sell / 9 hold / 12 buy / 1 strong buy (23 analysts, past 12 months).

**P/S on TTM revenue ≈ 5,850×** ($7.08B ÷ $1.21M). Market cap is **2.35× the company's total cash**.

### Quarterly income statement (thousands of USD)
| | Q2-2026 | Q1-2026 | Q4-2025 | Q3-2025 | Q2-2025 |
|---|---|---|---|---|---|
| **Total revenue** | **1,210** | 0 | 0 | 0 | 0 |
| Cost of revenue | 721 | — | — | — | 0 |
| R&D | 39,474 | 27,049 | 24,593 | 14,945 | 11,468 |
| SG&A | 34,205 | 24,200 | 32,503 | 21,364 | 16,547 |
| Operating income | −73,190 | −51,249 | −57,096 | −36,309 | −28,015 |
| Net income | −48,536 | −33,065 | −41,446 | −29,722 | −24,685 |
| Diluted EPS | −0.28 | −0.19 | — | −0.20 | −0.18 |
| Diluted avg shares | 176,224,404 | 170,333,700 | — | 150,364,900 | 140,085,498 |

**The entire Q2-2026 revenue line ($1.21M) came from the June 2026 acquisitions of ARMEC and Creative Engineers** — engineering/machining services, per the 10-Q. **Oklo has booked $0 of power revenue in its history.** For the six months ended 2026-06-30: revenue $1.21M vs loss from operations $124.2M.

### Quarterly balance sheet (key rows, thousands)
| | 2026-06-30 | 2026-03-31 | 2025-12-31 | 2025-09-30 | 2025-06-30 |
|---|---|---|---|---|---|
| Cash + ST investments (yf) | 2,465,158 | 2,208,609 | 1,227,971 | 921,600 | 534,425 |
| Total debt | 3,959 | 2,620 | 1,450 | 1,944 | 2,139 |
| Stockholders' equity | 3,273,557 | 2,638,629 | 1,476,210 | 1,205,586 | 696,411 |
| Net PPE | 179,355 | 98,143 | 43,696 | 13,075 | 5,501 |
| Construction in progress | 165,117 | 89,032 | 35,748 | 10,530 | 2,645 |
| Share issued | 185,090,200 | 173,867,800 | 160,514,100 | 156,186,500 | 147,595,514 |
| Accumulated deficit | −322,373 | −273,837 | −240,772 | −199,326 | −169,604 |

**Per the 10-Q (primary source):** as of 2026-06-30, cash + cash equivalents + marketable debt securities = **$3,006.3M**. The yfinance "cash" figure understates this by ~$541M (it excludes longer-dated marketable debt securities). **Use $3.0B as the company-reported liquidity figure**; note yfinance's narrower $2.47B measure.

### Quarterly cash flow (thousands)
| | Q2-2026 | Q1-2026 | Q4-2025 | Q3-2025 | Q2-2025 |
|---|---|---|---|---|---|
| Operating cash flow | −47,592 | −17,867 | −33,429 | −18,031 | −18,471 |
| Capital expenditure | −94,091 | −32,810 | −26,950 | −5,046 | −877 |
| **Free cash flow** | **−141,683** | **−50,677** | **−60,379** | **−23,077** | **−19,348** |
| Issuance of capital stock | 670,047 | 1,181,897 | 295,500 | 526,499 | 441,600 |

**Cash burn analysis (computed):**
- Q2-2026 standalone FCF burn: **−$141.7M/quarter** (a 7.3× YoY increase vs Q2-2025's −$19.3M)
- H1-2026 FCF burn: **−$192.4M** (matches the two quarters summed)
- Trailing-4-quarter average FCF burn: **−$68.95M/quarter**
- Operating cash outflow for H1-2026 per 10-Q: **−$65.46M** (excluding capex)

**Runway on $3.006B of liquidity:**
| Burn assumption | Annual burn | Runway |
|---|---|---|
| Q2-2026 rate (most conservative / most current) | ~$567M | **~5.3 years** |
| H1-2026 rate | ~$385M | **~7.8 years** |
| Trailing-4-quarter average | ~$276M | ~10.9 years |

**Caveat to state in the article:** capex is inflecting hard (Q2-2026 capex $94.1M vs $0.9M a year earlier; construction-in-progress nearly doubled sequentially to $165M) as the company builds Aurora-INL, the fuel fabrication facility and the Pike County, OH site. The Q2-2026 rate is the only one that reflects the current build. **Runway ≈ 5 years at the current burn rate**, not 10.

### Dilution — central to the bear case (all from the 10-Q share roll-forward)
| Date | Class A shares issued & outstanding |
|---|---|
| 2025-01-01 | 137,706,596 |
| 2025-06-30 | 147,595,514 |
| 2025-12-31 | 160,514,103 |
| 2026-06-30 | **185,090,155** |
| 2026-08-04 (10-Q cover) | 186,017,650 (yfinance `sharesOutstanding`) |

- **+34.4%** from 2025-01-01 to 2026-06-30 (18 months)
- **+25.4%** YoY (2025-06-30 → 2026-06-30)
- **+15.3%** in a single half-year (2025-12-31 → 2026-06-30) → ~33%/yr annualised pace
- **ATM programs:** 2025 ATM $1.5B (completed in Q1-2026; 1.5% agent commission); **May 2026 ATM $1.0B** (ongoing as of 2026-06-30); **Sept 11, 2026 new $1.0B ATM** equity distribution agreement with 10 banks (Goldman Sachs, BofA, Citigroup, JPMorgan, Morgan Stanley, Barclays, Cantor Fitzgerald, Guggenheim, Canaccord, B. Riley) under a $3.5B shelf.
- **A fully-drawn $1B ATM at the Friday close ≈ 26.3M new shares ≈ +14.1% of the current share count.** That is the dilution math to quote (no dollar price needed in the body: "a fresh $1 billion at-the-market program ≈ 14% of the current share count").

---

## 2. THE GRID / PJM / FERC FACTS

### What an interconnection study cycle is, and why missing one is expensive
A grid operator (PJM) studies every proposed generator in a "queue" in batches — a *study cycle*. To be studied, a project must be in the cycle when it opens; there is no rolling admission. If a project is dropped from a cycle, it cannot be studied until the **next** cycle opens months later, then waits out the study itself. **PJM itself says it expects to complete interconnection reviews in one to two years**, depending on a project's grid impact (Utility Dive, 2026-08-31). Oklo's own complaint quantified the cost of missing the cycle:
- **On 2026-08-31 Utility Dive reported Oklo said the delay was "at least 14 months."**
- **On 2026-09-25 Utility Dive reported Oklo said the delay was "at least 18 months."** The "18 months" figure appears 5× in that story.
**Both figures are in the record and trace to Oklo's own FERC filings — report the delta, do not silently pick one.**

### PJM's reformed queue — the backlog in numbers (Utility Dive, 2026-08-31)
- PJM **cleared out its legacy backlogged queue**, then launched a **reformed queue process**. The first cycle of the reformed process opened in 2026.
- **811 new service requests** were submitted in the first reformed cycle (POWER Magazine headlined it as **811 projects / ~220 GW**).
- **More than 200 GW of capacity qualified to be studied** in the first cycle. Composition: **100 GW natural gas, 60 GW storage, 17.3 GW nuclear, 11.8 GW solar, 7.5 GW hybrid solar-storage, 3.9 GW wind.**
- PJM spokesperson: **"nearly 90% of the 811 projects that submitted new service requests met the application requirements."** → **≈80+ projects (10%) failed the application gate**, which is the population from which the FERC complaint wave came.
- **Six complaints** are now at FERC from developers PJM dropped from this same cycle (five pending + Oklo's). Dockets confirmed directly from the FERC eLibrary API:
  - **EL26-99** — Advantage Capital Renewables
  - **EL26-101** — **Oklo Inc. v. PJM Interconnection, L.L.C.** (the one at issue)
  - **EL26-102** — Current Hydro LLC
  - **EL26-105** — Agilitas Energy, Inc. o/b/o Tygart, LLC
  - **EL26-106** — RWE Americas, LLC
  - **EL26-107** — Lanyard Power Holdings, LLC
  PJM filed an **"Emergency Motion … Opposing Shortened Comment Periods"** across EL26-105 et al. (2026-09-09), a sign of how many of these are moving at once.

### The Oklo docket — FERC's actual holding
**Docket: EL26-101-000** (Oklo Inc. v. PJM Interconnection, L.L.C.)

| Date | Filing (FERC eLibrary accession) |
|---|---|
| 2026-08-27 (posted 08-28) | **Complaint of Oklo Inc. v. PJM** — accession 20260828-5050 |
| 2026-09-01 | **Revised Complaint of Oklo Inc. v. PJM** — accession 20260901-5278 (public) / 20260901-5279 (privileged). Filed as an **expedited/fast-track complaint** (Oklo asked FERC to order PJM to respond by Sept 4) |
| 2026-09-04 | **PJM Response to Complaint** — accession 20260904-5205 (public) |
| 2026-09-14 | **Oklo Motion for Leave to Answer + Answer to PJM's Response** — accession 20260914-5081 (public) |
| 2026-09-18 | **PJM Motion for Leave to Answer + Answer to Oklo's Answer** — accession 20260918-5273 |
| **2026-09-24** | **"Order Denying Complaint re Oklo Inc. v. PJM Interconnection, L.L.C. under EL26-101."** Commission Order/Opinion. **Accession 20260924-3089.** |

**FERC's holding (per Utility Dive's read of the order, 2026-09-25):**
- FERC **rejected** the complaint.
- "Oklo failed to show that PJM violated any of its rules when it withdrew the project in early August."
- "Oklo didn't resolve flaws in its application identified by PJM staff."
- FERC's own qualifying language: *"Although we find that Oklo failed to demonstrate PJM violated its tariff, we note that, in order to meet growing demand in the PJM region, it is critical that PJM collaborate with project developers before, during, and after the interconnection application process to ensure guidance and expectations are clearly understood and properly implemented."* — i.e. FERC admonished PJM's process while denying the relief.

**Can Oklo re-apply? YES — two explicit paths, per the order as reported:**
1. **Fix the application errors and submit to PJM's next study cycle.**
2. **Submit to PJM's Expedited Interconnection Track**, which FERC noted is **open until 2027-12-31**, if Oklo wants to move quickly.

### The project Oklo lost (from its complaint, via Utility Dive)
- **750 MW**, described by Oklo as of **"critical national importance."**
- **Mixed technology: 150 MW advanced nuclear + 300 MW fuel cells + 300 MW gas-fired.** Oklo argued PJM's rules "weren't designed to handle" a multifuel project mixing synchronous (gas + nuclear) and inverter-based (fuel cells) resources under two different synchronous fuel types.
- **Interconnection point: two Dominion Energy substations between Washington, D.C. and Richmond, Virginia.** (The project was **not publicly identified by name** — it is NOT the Ohio/Meta campus.)
- Procedural history from the complaint: Oklo submitted into the queue **2026-04-27**; PJM issued a **deficiency notice 2026-05-15**; Oklo says it responded; **2026-06-24** PJM staff posted problems on the project's **NextGen** page without sending a deficiency notice (Oklo alleges this violated PJM's tariff); **2026-08-03** PJM told Oklo it was withdrawing the project, in part because Oklo never showed the project could **ride through a sudden drop in grid voltage**.
- Oklo's argument: *"PJM's decision to withdraw the project is the capstone to an unjust, unreasonable, and unduly discriminatory review process."*

**Note the timing asymmetry:** PJM dropped the project on **2026-08-03**; Oklo's *first* complaint was filed **2026-08-27** — 24 days later — and then had to be **revised on 2026-09-01**. Utility Dive's 2026-08-31 headline mis-frames it as Oklo filing on Aug 28/31 "against" an Aug-31 event; the withdrawal was Aug 3.

---

## 3. THE COMPANY FACTS (Oklo Inc., NYSE: OKLO, Santa Clara, CA)

**What it does** (Oklo's own boilerplate, verbatim from its newsroom): "developing fast fission power plants to deliver clean, reliable, affordable energy at global scale; establishing a domestic supply chain for critical isotopes; and advancing nuclear fuel recycling to convert used nuclear fuel into clean energy."
- **Designs and builds "Aurora" powerhouses** — metal-fueled **fast reactors**, sized **15 MW to 75 MW** each (Utility Dive, 2026-09-25). Business lines on oklo.com: `/business-lines/power`, `/business-lines/fuel`, `/business-lines/isotopes`.
- **Oklo claims three "firsts"**: first to receive a **DOE site use permit** for a commercial advanced fission plant; awarded fuel from **Idaho National Laboratory**; **submitted the first custom combined license application (COLA) for an advanced reactor to the NRC**.
- **Fuel recycling** is a second revenue vector: converting used nuclear fuel into usable fuel, in collaboration with DOE and the national labs.

### Aurora-INL (Idaho National Laboratory) — the lead project
- Proposed on land Oklo bought (206 acres) / DOE site; **Kiewit selected as lead constructor** for the first Aurora powerhouse in Idaho (10-Q).
- **DOE regulatory pathway has 5 steps**; Oklo has cleared two:
  - **Early 2026** — DOE approved the **Nuclear Safety Design Agreement (NSDA)** (PR 2026-03-17, oklo.com).
  - **2026-06-11** — DOE approved the **Preliminary Documented Safety Analysis (PDSA)** for Aurora-INL under the DOE **Reactor Pilot Program** (PR 2026-06-11, oklo.com). Confirmed in the 10-Q.
- **INL/DOE completed environmental compliance → Environmental Compliance Permit issued** (10-Q) — a milestone toward "the first commercial advanced fission power plant in the U.S."
- **Fuel award:** five metric tons of HALEU produced from recovered uranium from previously irradiated **EBR-II** fuel, from INL, for a commercial Aurora powerhouse in Idaho (10-Q).
- **Siemens Energy** turbine package advancing for Aurora-INL (POWER Magazine, 2026-06-18).
- **Earlier Utility Dive headline (2025-03-26): Oklo revealed a 75-MW reactor design and targeted "late 2027 commercial deployment."** ⚠️ Treat that date as *aspirational and now stale* — it predates every 2026 delay.

### NRC licensing status
- **2026-05-06** — **Oklo's NRC Principal Design Criteria (PDC) Topical Report was APPROVED** for the Aurora powerhouse in Idaho (oklo.com PR; verified 200). This is a real, dated licensing milestone.
- Previously accepted for review under an **accelerated timeline** (2025-09-30).
- **The 2022 NRC rejection is the historical overhang**: the NRC **denied Oklo's original license application** (World Nuclear News, 2022-01-07). NucNet (2026-03-31) reported Oklo is "continuing extensive pre-application work" after that rejection. Oklo has since completed an NRC readiness assessment (2025-07-17).
- **⚠️ NOT verified:** whether a formal, docketed **combined license application (COLA)** is currently under active NRC review and on what schedule. The PDC topical report is a *pre-application/topical* item, not a COLA approval. Do not imply Oklo has an NRC operating license.

### Groves Reactor — what the June 2026 "first criticality" news actually was
Verified from Oklo's own PR (2026-08-06, "Oklo's Groves Reactor Achieves First Criticality in Under a Year"):
- **Groves** is an **Isotope Test Reactor** — a **low-power test reactor**, built by **Oklo's subsidiary Atomic Alchemy** for **radioisotope production for healthcare, industry, research, space and national security**. **It is NOT an Aurora power reactor and produces no commercial power.**
- Reached **first criticality (a controlled, self-sustaining chain reaction at low power) less than a year after groundbreaking**, after DOE authorization through the **DOE Reactor Pilot Program (RPP)**.
- **The first RPP reactor to reach criticality on private land / a greenfield site.** (Antares Mark-0 was the first RPP reactor overall, 2026-06-05; Valar Atomics' Ward 250 second; Aalo third — per POWER Magazine / NucNet / DCD. **Oklo's Groves was not first in the program.**) POWER Magazine (2026-08-06) framed Groves as the **fifth DOE pilot reactor to reach criticality, first on private land.**
- ⚠️ **Date conflict to flag:** StockTitan's RSS and Google News both carry an Oklo-sourced **"Oklo's Groves Reactor Achieves First Criticality in Under a Year" dated Mon 08 Jun 2026**, while oklo.com's own newsroom PR and the ANS/World Nuclear News coverage put **DOE startup authorization on 2026-07-23** and criticality on **~2026-08-06**. The June date appears to be a feed/date artefact. **Use the August 6, 2026 criticality date** (oklo.com PR, ANS 2026-08-06, POWER Magazine 2026-08-06). Gov. Greg Abbott's congratulatory quote in the PR places the reactor in **Texas**.
- Separately, **Atomic Alchemy was granted an NRC license for isotope material** (2026-03-17) and received **DOE approval of its Nuclear Safety Design Agreement** (2026-03-17).
- Oklo also has an **isotope pilot facility partnership with DOE** (2026-01-07) and was **selected by DOE for advanced negotiations under the Surplus Plutonium Utilization Program** (2026-05-26).

### Meta 1.2 GW Pike County, Ohio campus (PR 2026-01-09 — verified, oklo.com returns 200)
- Agreement with **Meta Platforms (Nasdaq: META)** to develop a **1.2 GW power campus in Pike County, Ohio** to support Meta data centers in the region (Meta's AI supercluster in New Albany).
- Mechanism: **Meta prepays for power and provides funding** to advance project certainty; Oklo uses the funds to **secure nuclear fuel** and advance Phase 1. (10-Q confirms a **Prepayment Agreement dated 2026-01-05**.)
- Land: **206 acres in Pike County owned by Oklo**, formerly DOE land at the former **Portsmouth Gaseous Diffusion Plant**, facilitated by the **Southern Ohio Diversification Initiative (SODI)**.
- **Timeline (Oklo's own words): pre-construction and site characterization slated to begin in 2026; first phase targeted to come online AS EARLY AS 2030; scale to the full 1.2 GW by 2034.**
- **This is a PJM-footprint project** — Utility Dive noted Ohio/PJM connection explicitly. **The FERC/PJM rejection is about the separate, unnamed 750 MW Virginia project, not Pike County — but Pike County lives in the same queue.**
- **⚠️ This is a prepayment/funding agreement plus an intent to develop, NOT a signed, fixed-price PPA with a delivery date.**

### Other announced sites / customers / pipeline
From the 10-Q, prospective customers named by Oklo itself: **Meta, Equinix, Diamondback Energy, Prometheus Hyperscale, and Switch**.
- **Switch** — Oklo describes its agreement as "**one of the largest corporate PPAs in history**"; POWER Magazine headlined it as a **12 GW deal** (2024-12-18). **This is an anchor-name, non-binding-style pipeline figure, not contracted revenue.**
- **Equinix** — deal to procure up to **500 MW** of nuclear power with a **$25M prepayment** (2024-04; Data Center Dynamics, Neutron Bytes). Oklo is one of several advanced-nuclear providers in Equinix's 2025 procurement group (Equinix newsroom / Reuters, 2025-08-14).
- **Eielson Air Force Base, Alaska** — a **Notice of Intent to Award** has been issued by the **Defense Logistics Agency-Energy on behalf of the Department of the Air Force**, tentatively selecting Oklo to provide electricity and heat to Eielson AFB outside Fairbanks (10-Q). Oklo announced this as "intended awardee" on 2025-11-06. **This is the catalyst UBS is pointing to** (per multiple 2026-09-25 analyst headlines: "This Government-Backed Nuclear Project Could Be Key Catalyst"). ⚠️ **A Notice of Intent to Award is not a signed contract.**
- **Tennessee / Oak Ridge** — Oklo selected Tennessee for an advanced fuel center anchored by the **nation's first privately funded nuclear fuel recycling facility**, ~**$1.6-1.68B** (Tennessee ECD, 2025-09-04; World Nuclear News 2025-09-08; NucNet ~$1.6B; Neutron Bytes $1.68B). ⚠️ **Could not verify with a primary Oklo PR for the $ figure.**
- **HALEU fuel supply:** **Letter of Intent with Centrus Energy** (2026-06-18) to purchase nuclear fuel for the Aurora powerhouse in southern Ohio; a **planned joint venture with Centrus** (2026-03-09) on HALEU deconversion/enrichment in Ohio; a **strategic alliance with Standard Nuclear** (2026-06-16) on the advanced-nuclear fuel supply chain. Pulse 2.0 (2026-08-17) says the Centrus deal could supply HALEU for **five Aurora powerhouses**, with fuel fabrication startup activities targeting **2027**. ⚠️ All LOIs/MOUs unless proven otherwise.
- **Vertical integration via M&A (all 2026):** ARMEC (June, precision manufacturing), Creative Engineers (June, sodium/alkali-metal), and earlier Atomic Alchemy (radioisotopes). These acquisitions are the source of the first revenue line.
- **Other partners:** NVIDIA + Los Alamos on nuclear fuel validation (2026-04-23); Idaho National Laboratory on AI-enabled reactor design using INL's Prometheus AI platform (2026-05-12); Blykalla partnership expansion (2026-03-30); ABB MOU + monitoring room (2025-08-21); Siemens Energy steam-cycle equipment (2025-11-19).

### Cash position (confirmed twice)
- **$3,006.3M** cash + cash equivalents + marketable debt securities at **2026-06-30** (10-Q, primary).
- **$3,273.6M** total stockholders' equity; **$4.0M** total debt; accumulated deficit **−$322.4M**.
- Financed almost entirely by equity: **Q2-2026 alone raised $670M of capital stock; Q1-2026 raised $1.18B.**

---

## 4. BEAR-CASE FACTS (hard numbers only)

### Bear case
1. **Revenue is ~$0.** TTM revenue **$1.21M** — and *all of it* came from June-2026 engineering acquisitions (ARMEC, Creative Engineers), not from power. Oklo has **never booked commercial power revenue**. Against a **$7.08B market cap**, that's a price/sales ratio of roughly **5,850×**.
2. **Relentless, accelerating dilution.** Shares: 137.7M (2025-01-01) → 185.1M (2026-06-30) = **+34.4% in 18 months**, **+15.3% in the last six months alone**. Three ATM programs stacked: **$1.5B (2025, completed) + $1.0B (May 2026, ongoing) + a fresh $1.0B (2026-09-11)** under a $3.5B shelf. **A fully-drawn $1B ATM ≈ +14% share count at current prices.** Equity issuance, not operations, is the funding model: $670M issued in Q2-2026.
3. **Burn is inflecting, and the runway is shorter than the headline cash number suggests.** FCF: −$19.3M (Q2-25) → −$23.1M (Q3-25) → −$60.4M (Q4-25) → −$50.7M (Q1-26) → **−$141.7M (Q2-26)**. Capex went from **$0.9M (Q2-25) to $94.1M (Q2-26)**. At the current rate, **~5 years of runway on $3.0B** — against a first-power target of **2030** and first commercial *revenue* that most analysts do not expect before 2028.
4. **Timeline risk is now regulatory, not just engineering.** Oklo's 750 MW Virginia project — 150 MW nuclear + 300 MW fuel cells + 300 MW gas — is out of the current PJM cycle and FERC declined to order it back in. CEO-adjacent framing in Oklo's own complaint: **delay of "at least 14 months" (as reported 2026-08-31) / "at least 18 months" (as reported 2026-09-25), plus significantly increased development costs.** The Pike County 1.2 GW campus lives in the same PJM queue and its first phase is only targeted "as early as 2030."
5. **FERC found Oklo, not PJM, at fault.** The order holds that Oklo "failed to show that PJM violated any of its rules" and "didn't resolve flaws in its application identified by PJM staff" — including an unexplained **voltage ride-through** deficiency. Oklo's first complaint had to be **revised on 2026-09-01**, and **five other developers' complaints are stacked behind it**, so a favourable precedent for Oklo is not coming cheaply or soon.
6. **Competition that can be built faster.** **GE Vernova's BWRX-300** (already through Canadian licensing), **NuScale's** light-water SMR (the first NRC-approved SMR design), **X-energy** (backed by Dow/Amazon, DOE Advanced Reactor Demonstration Program funding), and **Centrus/LEU** as a supplier to all of them. And the base case competitor is not a reactor at all: **a gas turbine can be permitted and built in roughly two years**, against Oklo's 2030+ first power. Oklo's 15–75 MW module size means the Pike County 1.2 GW campus requires **dozens of reactors**, not one.
7. **Fuel dependency.** Oklo's fast reactors need **HALEU**, and the domestic HALEU chain is immature: Oklo's supply position is an **LOI with Centrus** (2026-06-18) and a **planned JV** (2026-03-09), with fabrication startup "targeting 2027." The 10-Q lists HALEU access risk explicitly ("risks related to accessing high-assay low-enriched uranium, plutonium, and other fuels … at acceptable costs and under acceptable timelines").
8. **Wall Street is resetting.** **UBS cut OKLO to $41 from $55, maintaining Neutral, on 2026-09-25** (analyst Jon Windham) — its new $41 target is **the lowest target on the street**. Analyst coverage aggregates around "Moderate Buy" but with **9 holds and 1 sell out of 23**, and the target dispersion is extreme ($41 low per MarketBeat — $14 low on yfinance — vs $130 high). At the Friday close the stock trades **~80% below its 52-week high** and only **~11% above its 52-week low**.

### Bull case (what the bulls actually point to — also hard facts)
1. **It shipped something.** Groves reached **first criticality less than a year after groundbreaking**, the first DOE Reactor Pilot Program reactor to reach criticality on private land/greenfield — Oklo's own proof point that "American nuclear deployment timelines can be measured in months rather than years."
2. **A top-tier commercial anchor.** The **Meta** agreement is a **prepayment/funding** structure — Meta puts up cash to secure nuclear fuel and advance Phase 1 — i.e. the customer funds the build instead of Oklo raising all of it. Oklo also has a **Switch** agreement it calls one of the largest corporate PPAs in history and up to **500 MW** with **Equinix**.
3. **DOE is clearing the path, not blocking it.** Oklo holds a DOE **site use permit** (first for a commercial advanced fission plant), a **5 metric ton HALEU award** from INL, an approved **Nuclear Safety Design Agreement** and an approved **Preliminary Documented Safety Analysis** for Aurora-INL, and an **Environmental Compliance Permit**. And **FERC's denial pointed Oklo to PJM's Expedited Interconnection Track, open through 2027-12-31** — a faster lane than the study cycle.
4. **NRC is making real progress.** The **Principal Design Criteria Topical Report was approved in May 2026** on an accelerated timeline — a genuine de-risking step for the Aurora design, after the 2022 rejection.
5. **First-mover in fast reactors + fuel-recycling optionality.** No competitor has an operating fast reactor in the U.S.; the Tennessee fuel-recycling centre is a **~$1.6B** private investment and recycling is a potential second, non-power revenue line. Also, **DOE selected Oklo for advanced negotiations under the Surplus Plutonium Utilization Program** (2026-05-26) — plutonium fuel is another feedstock.
6. **Optionality on government demand.** The **Eielson Air Force Base, Alaska** Notice of Intent to Award (DLA-Energy on behalf of the Air Force) is an entirely separate, non-PJM, non-data-center revenue channel — and it's the catalyst UBS itself flagged on 2026-09-25.
7. **The cash is real and the balance sheet is clean.** **$3.006B** of liquidity against **$4M of debt** — funded ahead of the build, on an equity-fueled basis that leaves Oklo with no meaningful refinancing risk before 2030.

---

## 5. LINKS FOR `links[]` — all curl-verified

| # | Label (outlet + date) | URL | HTTP |
|---|---|---|---|
| 1 | **Utility Dive, Sept 25, 2026** — "FERC rejects Oklo complaint seeking to reinstate project to PJM's interconnection study cycle" | `https://www.utilitydive.com/news/ferc-rejects-oklo-complaint-pjm-interconnection/` | **200** |
| 2 | **Utility Dive, Aug 31, 2026** — "PJM drops Oklo advanced nuclear project from interconnection study cycle" | `https://www.utilitydive.com/news/pjm-oklo-advanced-nuclear-ferc-interconnection/` | **200** |
| 3 | **FERC eLibrary, Sept 24, 2026** — Order Denying Complaint, Oklo Inc. v. PJM Interconnection (Docket EL26-101-000; accession 20260924-3089) | `https://elibrary.ferc.gov/eLibrary/filelist?accession_number=20260924-3089` | **200** |
| 4 | **Oklo newsroom, Aug 6, 2026** — "Oklo's Groves Reactor Achieves First Criticality in Under a Year" | `https://oklo.com/newsroom/oklos-groves-reactor-achieves-first-criticality-in-under-a-year` | **200** |
| 5 | **Oklo newsroom, Jan 9, 2026** — "Oklo, Meta Announce Agreement in Support of 1.2 GW Nuclear Energy Development in Southern Ohio" | `https://oklo.com/newsroom/oklo-meta-announce-agreement-in-support-of-1-2-gw-nuclear-energy-development-in-southern-ohio` | **200** |
| 6 | **Oklo newsroom, Aug 7, 2026** — Q2 2026 financial results & business update | `https://oklo.com/newsroom/oklo-publishes-second-quarter-2026-financial-results-and-business-update` | **200** |
| 7 | **Oklo newsroom, May 6, 2026** — "Oklo's NRC Principal Design Criteria Topical Report Approved for Aurora Powerhouse in Idaho" | `https://oklo.com/newsroom/oklos-nrc-principal-design-criteria-topical-report-approved-for-aurora-powerhouse-in-idaho` | **200** |
| 8 | **Oklo newsroom, June 18, 2026** — "Oklo, Centrus Sign Letter of Intent to Purchase Nuclear Fuel for Aurora Powerhouse Deployment" | `https://oklo.com/newsroom/oklo-centrus-sign-letter-of-intent-to-purchase-nuclear-fuel-for-aurora-powerhouse-deployment-in-` | **200** |
| 9 | **MarketBeat, updated Sept 25, 2026** — Oklo analyst ratings: UBS (Jon Windham) lowers target $55.00 → $41.00, Neutral | `https://www.marketbeat.com/stocks/NYSE/OKLO/analyst-ratings/` | **200** |
| 10 | **SEC EDGAR, Sept 11, 2026** — Oklo 8-K: $1.0B at-the-market equity distribution agreement with 10 sales agents | `https://www.sec.gov/Archives/edgar/data/1849056/000110465926106897/tm2625056d1_8k.htm` | **403** w/ generic browser UA, **200** w/ a declared research UA. Verified 200 against a declared UA. Use as a footnote link, not a headline link. |
| 11 | **SEC EDGAR, Aug 7, 2026** — Oklo 10-Q for the quarter ended June 30, 2026 ($3.006B liquidity; 185,090,155 shares; $1.21M revenue) | `https://www.sec.gov/Archives/edgar/data/1849056/000162828026054571/oklo-20260630.htm` | **403** w/ generic browser UA, **200** w/ a declared research UA. Same caveat. |

**Recommended 8 for the article's `links[]`:** #1, #2, #3, #4, #5, #6, #7, #9. Add #8 or #11 as a ninth if the body cites HALEU/Centrus or the balance sheet.

⚠️ **Rejected URLs (do NOT use — these return 404):** `https://www.rtoinsider.com/oklo-ferc-complaint`, `https://oklo.com/newsroom/oklo-selected-as-intended-awardee-to-provide-clean-reliable-power-to-eielson-air-force-base-in-alaska`, `https://www.utilitydive.com/news/meta-nuclear-deals-oklo-vistra-terrapower/`. **StockTitan article pages return 403** to curl (the `/rss/news/OKLO/` feed is the only StockTitan endpoint that returns 200) — usable per the 403 rule, but prefer oklo.com PRs which return 200.

---

## 6. THESIS + ANGLE + WHAT TO WATCH

### Thesis (3–4 sentences)
Oklo is the market's most expensive bet on a nuclear build-out and one of the only advanced-nuclear names whose near-term funding comes from its customers rather than the grid: Meta is prepaying for fuel and development on a 1.2 GW Ohio campus, Groves went critical in under a year, and the NRC approved the Aurora design criteria — real hardware and real process, not a slide deck. But FERC's Sept 24 order denying Oklo's complaint over its 750 MW Virginia project — six complaints from PJM-dropped developers are now stacked at the agency — shows that the binding constraint on Oklo is not reactor engineering but the queue it has to sit in: miss a study cycle and the project slips roughly a year and a half, and the Pike County campus targets first power only "as early as 2030." With TTM revenue of about a million dollars, a roughly $3 billion cash pile being consumed at an accelerating ~$140M per quarter, and a fresh $1 billion at-the-market program that could add ~14% to the share count, the stock sits near the bottom of a very wide analyst range — and roughly 80% below where it traded a year ago. UBS cutting to $41 on the same day FERC ruled captures the tension exactly: the value is long-dated, and the off-ramp to whatever comes next is a regulatory calendar, not a construction calendar.

### The single strongest angle nobody is talking about
**Oklo's FERC loss isn't a company story, it's a queue-administration story — and it's about to become a precedent cascade.** PJM's first reformed study cycle admitted **811 projects totaling more than 200 GW**; PJM's own spokesperson says "**nearly 90%**" of them met the application bar. That means roughly **80 projects failed the gate**, and **six of them have now taken PJM to FERC** (EL26-99, EL26-101, EL26-102, EL26-105, EL26-106, EL26-107) — Oklo being just the highest-profile one. FERC's order is the first ruling in that wave and it sided with the RTO on process while explicitly warning PJM to "collaborate with project developers before, during, and after the interconnection application process." Every one of those five remaining dockets now reads Oklo's loss as its precedent. The corollary nobody has drawn: FERC also handed Oklo — and the other five — the actual remedy, **PJM's Expedited Interconnection Track, open through Dec 31, 2027**, a door Oklo's own coverage has almost entirely ignored in favour of the denial headline.

### What an investor should watch next (event + number + timeframe)
**Event:** whether Oklo files the 750 MW Virginia project into **PJM's Expedited Interconnection Track** (or, failing that, into PJM's next interconnection study cycle).
**Number:** the **750 MW** at two **Dominion Energy** Virginia substations — 150 MW advanced nuclear + 300 MW fuel cells + 300 MW gas.
**Timeframe:** the Expedited Track window closes **2027-12-31**; a re-filing would most plausibly land with the next queue window, i.e. **by Q1–Q2 2027**. If that project is not visible in either PJM lane by then, the "at least 18 months" delay becomes structural rather than a one-cycle miss, and the Meta-backed Pike County campus' "as early as 2030" first-phase date — the single number the whole $7 billion valuation rests on — starts sliding with it.
**Secondary watch:** the **Q3 2026 10-Q (~early Nov 2026)** for how much of the new **$1 billion ATM** has already been drawn — the fastest read on how much dilution shareholders absorbed to keep the build on schedule.

---

## 7. THINGS I COULD NOT VERIFY (state plainly; do not paper over)

1. **The FERC order's docket-number language was not read verbatim from the order document itself.** The docket (**EL26-101-000**), the order's existence, its title ("Order Denying Complaint"), its issue date (**2026-09-24**) and its accession number (**20260924-3089**) are all confirmed from the **FERC eLibrary API** (primary). The *holdings* (failure to show tariff violation; unresolved application flaws; the two re-application paths; the Expedited Track date of 2027-12-31) are sourced to **Utility Dive's** reporting of the order. The order text is filed as a `.docx` on eLibrary (`EL26-101-000.docx`) and I did not extract and read it.
2. **The 14-month vs 18-month delay discrepancy is unresolved.** Utility Dive reported Oklo claiming "at least 14 months" on 2026-08-31 and "at least 18 months" on 2026-09-25, both attributed to Oklo's complaint. Either the revised Sept 1 complaint raised the figure or one story is loose. **Attribute each figure to its story; do not present a single number as fact.**
3. **Oklo's current NRC combined license application (COLA) status is NOT verified.** Oklo's boilerplate claims it "submitted the first custom combined license application for an advanced reactor to the U.S. Nuclear Regulatory Commission," and the **Principal Design Criteria Topical Report was approved in May 2026**. I could **not** confirm a live, docketed COLA under active NRC review or any review schedule. Do not state that Oklo has an NRC licence or a COLA approval.
4. **No signed, fixed-price power purchase agreement with a delivery date was verified** — for Meta (a prepayment/funding agreement), Switch (12 GW, described by Oklo as a PPA), Equinix (up to 500 MW with a $25M prepayment), or Eielson AFB (a **Notice of Intent to Award**, not a contract). All should be characterised as agreements/LOIs/intents in the article.
5. **The Tennessee fuel-recycling facility capex figure (~$1.6B vs $1.68B) is not sourced to an Oklo PR.** It comes from Tennessee ECD (2025-09-04), World Nuclear News (2025-09-08), NucNet (~$1.6B) and Neutron Bytes ($1.68B) — three different numbers. Either cite a range or attribute to the Tennessee governor's office.
6. **The "Groves first criticality" dated June 8, 2026** in StockTitan's RSS and Google News is contradicted by oklo.com's own newsroom and by ANS, World Nuclear News and POWER Magazine, which place DOE startup authorization at **2026-07-23** and criticality at **2026-08-06**. Use **Aug 6, 2026**. The June date looks like a feed artefact.
7. **Analyst-count and target disagreement between providers is unresolved.** yfinance: **20 analysts, target mean $76.43, low $14.00, high $130.00**, rating "buy" (mean 2.08). MarketBeat: **23 analysts, mean $82.44, low $41.00, high $130.00**, "Moderate Buy" (1 sell / 9 hold / 12 buy / 1 strong buy). The **$14 low on yfinance is likely stale** and should not be quoted. Use MarketBeat's mix, or cite yfinance, but don't blend them.
8. **PJM's total legacy interconnection backlog in GW was NOT verified from a primary PJM source.** The verified figures are: the first reformed cycle drew **811 requests / ~220 GW** (POWER Magazine, 2026-04-30; RTO Insider 2026-04-29) with **more than 200 GW qualified** and a stated **100 GW gas / 60 GW storage / 17.3 GW nuclear / 11.8 GW solar / 7.5 GW hybrid / 3.9 GW wind** split (Utility Dive, 2026-08-31). A widely-circulated **"438 GW queue"** figure comes only from a low-quality aggregator and should not be used. pjm.com Inside Lines returned **403** to curl.
9. **Oklo's exact Pike County Phase 1 MW figure is not public** — Oklo says "up to 1.2 GW" total with Phase 1 coming online "as early as 2030" and full scale "by 2034," without stating Phase 1's capacity.
10. **Tavily `web_search` was out of quota** and `web_extract` was misconfigured for this session; everything above was gathered with **curl** (Google News RSS, Utility Dive, oklo.com, MarketBeat, FERC eLibrary API, SEC EDGAR) and **yfinance** via `/home/chino/video-venv/bin/python3`. **rtoinsider.com, tipranks.com, benzinga.com, investing.com, marketscreener.com, seekingalpha.com, gurufocus.com and pjm.com/insidelines all returned 403 to curl** and could not be used.
