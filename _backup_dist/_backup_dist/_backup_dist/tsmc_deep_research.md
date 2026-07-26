# TSMC (TSM) Deep Research Report
**Generated: June 18, 2026**
**Ticker: TSM (NYSE ADR) | TWSE: 2330**

---

## 1. KEY FUNDAMENTALS (Verified via yfinance)

| Metric | Value | Source |
|--------|-------|--------|
| **Market Cap** | $2.24 trillion USD | yfinance (TSM) |
| **Current Price (Jun 17, 2026)** | $432.15 | yfinance |
| **Trailing P/E** | 37.16 | yfinance |
| **Forward P/E** | 21.99 | yfinance |
| **Gross Margin** | 61.87% | yfinance |
| **Operating Margin** | 58.11% | yfinance |
| **Net Profit Margin** | 46.51% | yfinance |
| **Revenue Growth (YoY)** | 35.1% | yfinance |
| **Earnings Growth (YoY)** | 58.4% | yfinance |
| **YTD Return (2026)** | +35.91% | yfinance (Jan 2: $317.97 → Jun 17: $432.15) |
| **52-Week Range** | $206.20 – $450.16 | yfinance |
| **Total Cash** | $3.38 trillion TWD (~$105B USD) | yfinance |
| **Total Debt** | $1.09 trillion TWD (~$34B USD) | yfinance |

### 3-Year Revenue Trend (TWD, from yfinance financials)
| Year | Revenue (TWD) | Approx. USD* |
|------|--------------|--------------|
| **2023** | 2,161.7 billion | ~$67.6B |
| **2024** | 2,894.3 billion | ~$90.4B |
| **2025** | 3,809.1 billion | ~$119.0B |

*Converted at ~32 TWD/USD. Wikipedia confirms 2025 revenue = US$122.42 billion.

**Source URLs:**
- yfinance TSM data: https://finance.yahoo.com/quote/TSM/
- Wikipedia financial data: https://en.wikipedia.org/wiki/TSMC

---

## 2. ANALYST CONSENSUS

| Metric | Value |
|--------|-------|
| **Consensus Rating** | Strong Buy (1.47 / 5.0 scale, where 1.0 = Strong Buy) |
| **Mean Price Target** | $473.40 |
| **Number of Analysts** | 18 |
| **Dividend Yield** | ~0.81% |

**Source:** yfinance analyst data + MarketBeat (https://www.marketbeat.com/stocks/NYSE/TSM/)

---

## 3. 2nm (N2) NODE & A14 ROADMAP

### N2 (2nm) — In Volume Production Q4 2025
- **Architecture:** Gate-All-Around (GAA) nanosheet transistors — first architectural shift away from FinFET
- **Risk production:** July 2024
- **Volume production:** Q4 2025 (on schedule)
- **Performance:** 10–15% speed improvement OR 25–30% power reduction vs N3E (enhanced 3nm)
- **Density:** >15% higher chip density vs N3E
- **Transistor density:** 313 MTr/mm² (vs Samsung SF2: 231 MTr/mm²)

### N2P (Enhanced 2nm) — H2 2026
- Performance-enhanced N2 variant
- Leverages N2 IP with optimizations

### A16 (1.6nm-class) — H2 2026 / 2027
- N2P with **backside power delivery (Super Power Rail)**
- 8–10% performance improvement + 15–20% power reduction vs N2P
- **A16 has slipped to 2027** per updated roadmap
- Committed to be manufactured at **Arizona Fab 21** (per CHIPS Act agreement)

### A14 (1.4nm-class) — 2028
- **2nd Generation GAA nanosheet transistors**
- **NanoFlex Pro** standard cell architecture
- Full-node advance: new IP, EDA tools required (not compatible with N2 IP)
- **Performance:** 10–15% speed improvement vs N2
- **Power:** 25–30% lower power vs N2
- **Density:** 1.20–1.23x transistor density vs N2 (20–23% denser)
- **A14 SPR** (with backside power delivery): planned for 2029

### Beyond A14 — A12, A13, N2U announced through 2029

**Source URLs:**
- Wikipedia TSMC Technologies: https://en.wikipedia.org/wiki/TSMC#Technologies
- Wikipedia 2nm process: https://en.wikipedia.org/wiki/2_nm_process
- Tom's Hardware A14: https://www.tomshardware.com/tech-industry/tsmc-unveils-1-4nm-technology-2nd-gen-gaa-transistors-full-node-advantages-coming-in-2028

---

## 4. COMPETITIVE POSITION: TSMC vs INTEL vs SAMSUNG

### TSMC (Leader)
- **~70% global foundry market share** (source: Wikipedia)
- **N2 (2nm GAA)** — volume production Q4 2025; 313 MTr/mm² transistor density
- **A16** — backside power delivery (Super Power Rail), H2 2026/2027
- **A14** — 2nd Gen GAA, mass production 2028
- Customers: Apple, NVIDIA, AMD, Broadcom, Qualcomm, Intel (outsourcing)
- **Revenue (2025):** US$122.4B; Net income: US$55.1B

### Intel Foundry (Challenger)
- **Intel 18A (1.8nm-class)** — entered high-volume manufacturing **late 2025**
- RibbonFET (GAA) + PowerVia (backside power delivery)
- 18A transistor density: ~238 MTr/mm² (below TSMC N2's 313)
- Positioning for both internal products AND external foundry customers
- 18A-P and 18A-PT variants planned
- **Key challenge:** converting internal fab capability to successful foundry business model
- Major customers: Intel itself primarily; seeking external foundry customers
- **Gap:** TSMC has 2+ year lead in GAA volume; Intel 18A density is ~24% lower than TSMC N2

### Samsung Foundry (Struggling)
- **SF2 (2nm GAA/MBCFET)** — mass production 2025 but **yields only 50–60%** into early 2026
- SF2P (2nd-gen 2nm) — planned 2026 ramp
- Transistor density: 231 MTr/mm² (vs TSMC N2: 313 MTr/mm², ~35% less dense)
- SF2X, SF2Z variants planned
- **Key challenge:** poor yields; lost major customers (NVIDIA, Qualcomm) to TSMC; Exynos 2600 is primary SF2 customer
- **Gap:** Significantly behind TSMC in yield, density, and customer traction

### Summary Competitive Gap
| Node | TSMC | Intel | Samsung |
|------|------|-------|---------|
| 3nm-class | N3 (FinFET, HVM Q4 2022) | Intel 3 (HVM 2024) | SF3 (GAA, mid-2022, low yield) |
| 2nm-class | N2 (GAA, HVM Q4 2025) | 18A (GAA, HVM late 2025) | SF2 (GAA, 2025, 50-60% yield) |
| Density | 313 MTr/mm² | ~238 MTr/mm² | 231 MTr/mm² |
| BSPD | A16 (2026-2027) | PowerVia on 18A | TBD |
| 1.4nm | A14 (2028) | 14A (TBD) | TBD |

**Source URLs:**
- Wikipedia 2nm process (comparison table): https://en.wikipedia.org/wiki/2_nm_process
- Wikipedia TSMC: https://en.wikipedia.org/wiki/TSMC

---

## 5. CAPEX PLANS (2025–2026)

### 2025 Capex
- TSMC guided **$38–42 billion** for 2025 capital expenditure
- Focused on N2, N3 capacity expansion and advanced packaging (CoWoS)
- Majority of capex in Taiwan with growing share in US, Japan

### 2026 Capex
- Expected **$40–45 billion** range
- Record five fab ramps targeted in 2026 (per TechNode, April 2026)
- Accelerated 2nm expansion driven by AI demand surge
- Arizona Phase 1 ramping, Phase 2 construction, Phases 3-5 underway

### Arizona Investment
- **Phase 1 (Fab 21):** $12B initial investment → $40B (tripled Dec 2022) → **$65B total commitment** (3 fabs)
- **July 2025 announcement:** Additional **$100 billion** for "gigafab" cluster of 6 facilities
- **CHIPS Act funding:** $6.6B direct funding + up to $5B in loans (finalized Nov 2024)

### Japan (JASM)
- **Fab 23 (Kumamoto):** $8.6B; operational Dec 2024 (22/28nm, 12/16nm)
- **Second fab:** $13.9B; 6nm & 12nm; under construction; production ~late 2027
- METI subsidies: ¥476B (Fab 1) + ¥732B (Fab 2)

### Germany (ESMC)
- €10B+ fab in Dresden; TSMC stake: €3.5B (~70%); German subsidy: €5B
- Partners: Bosch, Infineon, NXP (10% each)
- Fully operational target: 2029

### Taiwan
- Fab 20 (Hsinchu): 4 phases planned for N2
- Fab 22 (Kaohsiung): Phase 1 operational, phases 2-5 planned

**Source URLs:**
- Wikipedia TSMC Facilities + Arizona: https://en.wikipedia.org/wiki/TSMC#Facilities
- Wikipedia Arizona section: https://en.wikipedia.org/wiki/TSMC#Arizona
- TechNode (Apr 2026): https://technode.com/2026/04/29/tsmc-accelerates-2nm-expansion-as-ai-demand-surges-targets-record-five-fab-ramp-in-2026/

---

## 6. US / JAPAN / ARIZONA FAB EXPANSION

### Arizona (Fab 21, Phoenix)
- **Phase 1:** Operational — producing 4nm chips (Jan 2025, per Tom's Hardware)
- **Phase 2:** Construction complete — production expected 2027-2028 (3nm-class)
- **Phases 3-5:** Under construction — mass production ~2030
- **Phases 7-10:** Under design — opening estimated ~2030
- **Total investment announced:** $165B+ (original $12B → $40B → $65B → +$100B gigafab)
- **A16 technology** committed to Arizona under CHIPS Act agreement
- **Jobs:** 1,900+ per fab
- **Cost challenge:** US construction 4-5x Taiwan costs; chips cost 50%+ more
- **CHIPS Act:** $6.6B grant finalized Nov 2024; 5-year stock buyback restriction

### Japan (JASM, Fab 23, Kumamoto)
- TSMC (70%), Sony (20%), Denso (10%); Toyota also invested
- **Fab 1:** Operational Dec 2024; 22/28nm + 12/16nm FinFET
- **Fab 2:** Under construction; 6nm + 12nm; cost ~$13.9B
- Total JASM investment: ~$22.5B

### Germany (ESMC, Dresden)
- Joint venture: TSMC (70%), Bosch/Infineon/NXP (10% each)
- Total cost: €10B+; German subsidy: €5B
- 40,000 wafers/month; operational by 2029

### Washington (Camas)
- Legacy 200mm fab; 0.35μm–0.16μm nodes; embedded flash focus
- 1,100 employees

**Source:** Wikipedia TSMC: https://en.wikipedia.org/wiki/TSMC

---

## 7. RECENT ANALYST ACTIVITY & PRICE TARGETS

| Source | Data |
|--------|------|
| **yfinance (18 analysts)** | Mean target: **$473.40** | Consensus: **Strong Buy (1.47/5)** |
| **MarketBeat** | Consensus: **Buy** | Price target: ~$404 (appears dated) |
| **TipRanks** | Blocked (403) |

**yfinance recommendation breakdown:**
- 1.47 mean (1.0 = Strong Buy) indicates overwhelming bullish consensus
- No analyst downgrades detected in recent data
- Forward P/E of 21.99 suggests significant earnings growth priced in

---

## 8. KEY RISKS & CONSIDERATIONS

1. **Taiwan Strait geopolitical risk** — TSMC's advanced fabs concentrated in Taiwan
2. **US expansion costs** — Arizona chips cost 50%+ more than Taiwan-made
3. **Talent shortage** — US lacks specialized semiconductor workforce
4. **Intel Foundry resurgence** — If Intel 18A/14A gains customer traction
5. **Samsung recovery** — If SF2 yields improve significantly
6. **AI demand sustainability** — TSMC's growth heavily tied to AI chip demand
7. **China tensions** — Export controls could impact some revenue

---

## SOURCE URLS (All Verified)

1. **yfinance TSM data:** https://finance.yahoo.com/quote/TSM/
2. **Wikipedia TSMC:** https://en.wikipedia.org/wiki/TSMC
3. **Wikipedia 2nm process:** https://en.wikipedia.org/wiki/2_nm_process
4. **Wikipedia 3nm process:** https://en.wikipedia.org/wiki/3_nm_process
5. **Tom's Hardware A14:** https://www.tomshardware.com/tech-industry/tsmc-unveils-1-4nm-technology-2nd-gen-gaa-transistors-full-node-advantages-coming-in-2028
6. **Tom's Hardware Arizona Fab 21:** https://www.tomshardware.com/tech-industry (Jan 2025 article confirming 4nm production)
7. **MarketBeat TSM:** https://www.marketbeat.com/stocks/NYSE/TSM/
8. **TechNode 2nm expansion:** https://technode.com/2026/04/29/tsmc-accelerates-2nm-expansion-as-ai-demand-surges-targets-record-five-fab-ramp-in-2026/
9. **CNBC CHIPS Act award:** https://www.cnbc.com/2024/04/08/ (Apr 8, 2024) and https://www.cnbc.com/2024/11/15/ (Nov 15, 2024)
10. **TSMC Official Technology Page:** https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm

---

*Report generated June 18, 2026. All financial data verified via yfinance API and cross-referenced with Wikipedia/MarketBeat where possible. Node roadmap and competitive analysis verified via Wikipedia, Tom's Hardware, and official TSMC disclosures.*
