# ADVANCED MICRO DEVICES (AMD) - Deep Research Brief
## Date: July 4, 2026 | Ticker: AMD (NASDAQ)

---

## 1. KEY FINANCIAL METRICS (yfinance verified)

| Metric | Value | Source |
|--------|-------|--------|
| **Market Cap** | $844.36B | yfinance |
| **Enterprise Value** | $835.88B | yfinance |
| **Current Price** | $517.82 | yfinance |
| **52-Week High** | $584.73 | yfinance |
| **52-Week Low** | $133.50 | yfinance |
| **Previous Close** | $540.88 | yfinance |
| **YTD Return** | +136.56% | yfinance (start: $218.90) |
| **50-Day Moving Avg** | $460.38 | yfinance |
| **200-Day Moving Avg** | $278.19 | yfinance |

### VALUATION
| Metric | Value |
|--------|-------|
| **Trailing P/E** | 172.6x |
| **Forward P/E** | 39.3x |
| **Price/Book** | 13.09x |
| **Trailing EPS** | $3.00 |
| **Forward EPS** | $13.18 |

### PROFITABILITY
| Metric | Value |
|--------|-------|
| **Gross Margin (TTM)** | 53.06% |
| **Operating Margin** | 14.40% |
| **Net Profit Margin** | 13.37% |
| **Return on Equity** | 8.06% |
| **Return on Assets** | 3.65% |

### REVENUE (Annual Trend)
| Fiscal Year | Revenue | YoY Growth |
|-------------|---------|------------|
| FY2022 | $23.60B | — |
| FY2023 | $22.68B | -3.9% |
| FY2024 | $25.79B | +13.7% |
| FY2025 | $34.64B | +34.3% |
| **TTM (Q1 2026)** | **$37.45B** | **+37.8%** |

**3-Year Revenue CAGR (FY2022→FY2025): 13.6%**

### QUARTERLY REVENUE TREND
| Quarter | Revenue | Gross Margin |
|---------|---------|-------------|
| Q1 2025 | $7.44B | 50.2% |
| Q2 2025 | $7.69B | 39.8% |
| Q3 2025 | $9.25B | 51.7% |
| Q4 2025 | $10.27B | 54.3% |
| Q1 2026 | $10.25B | 52.8% |

### BALANCE SHEET
| Metric | Value |
|--------|-------|
| Total Cash | $12.35B |
| Total Debt | $3.87B |
| Stockholders' Equity | $63.00B |
| Debt-to-Equity | 6.01 (includes lease obligations) |
| Shares Outstanding | 1.631B |
| Free Float | 1.622B |
| Short Ratio | 1.46 |
| Insider Ownership | 0.40% |
| Institutional Ownership | 72.08% |

### ANALYST CONSENSUS
| Metric | Value |
|--------|-------|
| **Recommendation** | **STRONG BUY** |
| Number of Analysts | 48 |
| Mean Target Price | $508.31 |
| High Target | $700.00 |
| Low Target | $320.00 |
| Recent Upgrades (0-2mo) | 5 Strong Buy + 37 Buy + 9 Hold |

Notable recent upgrades:
- **Wells Fargo** (Jun 30, 2026): PT $615 — lifted server CPU revenue forecasts to $25B by 2028, citing AI-driven CPU demand and 2nm EPYC Venice ramp
- **BofA** (Jun 11, 2026): PT $560 (from $500), maintained Buy
- **Evercore ISI** (May 19, 2026): PT $579 (from $358), Outperform
- **DA Davidson** (Apr 25, 2026): Upgraded to Buy, PT $375
- **24/7 Wall St.** (Jul 3, 2026): PT $589.73, ~9% upside from current price

---

## 2. COMPETITIVE POSITIONING vs NVIDIA

### Market Share in AI Accelerators (2026)
| Company | Market Share | Notes |
|---------|-------------|-------|
| NVIDIA | ~80-85% | Dominant; FY2026 data center revenue $193.7B |
| AMD | ~5-7% | MI300X/MI325X inference adoption driving share gains |
| Custom Silicon (Google TPU, AWS Trainium, etc.) | ~5% collectively | Growing share from hyperscalers |
| Intel | <1% (discrete GPU) | ~22% if CPUs included |

- NVIDIA generated **$215.9B** in fiscal 2026 revenue vs AMD's **$34.6B**
- AMD's Instinct GPU line generated an estimated **$7-8B** in 2025
- AMD's data center segment now contributes **over half** of total revenue

### Product Competition
| Factor | NVIDIA | AMD |
|--------|--------|-----|
| **Current Flagship** | Blackwell B200/B100 | MI350X / MI325X |
| **Ecosystem** | CUDA (entrenched moat) | ROCm (improving but still gap) |
| **Performance (FP8)** | Similar TFLOPS MI350X matches B200 | Competitive on raw compute |
| **HBM** | HBM3e (B200) | HBM4 (MI400, shipping H2 2026) |
| **Software Moat** | Massive CUDA ecosystem | ROCm 7+ gaining PyTorch/JAX support |
| **Key Customers** | All hyperscalers | Meta, Microsoft, OpenAI multi-year deals |
| **TCO Position** | Premium pricing | Lower cost-per-token for inference |

### AMD's Competitive Advantages:
1. **Price/Performance**: Lower cost-per-token for AI inference workloads
2. **Hyperscaler Diversification**: Meta and OpenAI multi-year multi-GW deals
3. **CPU + GPU Bundle**: EPYC server CPUs gaining share alongside Instinct GPUs
4. **Open Software Stack**: ROCm improving — but CUDA dominance is the primary moat NVIDIA holds
5. **2nm Technology**: Venice CPU (H2 2026) and MI400 GPU on 2nm

### AMD's Competitive Weaknesses:
1. **CUDA Software Moat**: Most AI frameworks optimized for CUDA first
2. **Market Share Gap**: 5-7% vs 80-85% — absolute revenue gap widening
3. **Gaming Segment Weakness**: Declining relevance vs NVIDIA GeForce
4. **Margin Pressure**: Gross margins ~53% vs NVIDIA's ~75%+

---

## 3. MI400 DATACENTER GPU LAUNCH STATUS

### Key Findings:
- **Launch Timeline**: Expected H2 2026 (per multiple sources)
- **Process Node**: 2nm GPU technology
- **Memory**: 432 GB HBM4 with 19.6 TB/s bandwidth
- **Transistors**: 320B transistors
- **Platform**: Part of the **Helios** rack-scale AI platform (announced CES 2026)
- **Target**: Directly challenging NVIDIA Blackwell and upcoming Vera Rubin
- **Estimated Revenue Impact**: $7.2B projected from MI400 series

### MI400 Series Specifications (from tech-insider.org):
- 432 GB HBM4
- 320B transistors
- Helios rack-scale platform for exascale AI
- 2nm GPU die

### Roadmap Beyond MI400:
- **MI500**: Expected 2027 — next-generation accelerator
- **Venice CPU** (EPYC): 2nm server CPU launching H2 2026

### Sources:
- tech-insider.org/amd-mi400-series-ai-gpu-data-center-2026/ (Apr 13, 2026)
- techtimes.com — CES 2026: AMD Details Helios AI Rack (Jan 6, 2026)
- gpuinsights.net — NVIDIA AMD AI chips compared: Blackwell B200 vs MI400 (May 13, 2026)
- buildmvpfast.com — AMD MI400 vs NVIDIA GPU Economics for AI Inference 2026 (May 17, 2026)
- wccftech.com — AMD's 2026-2027 AI Roadmap: MI400 & MI500 (Nov 11, 2025)

---

## 4. MARKET SHARE IN AI ACCELERATORS

### Current Landscape (2026 estimates):
| Vendor | AI Accelerator Share | Key Product |
|--------|---------------------|-------------|
| NVIDIA | 80-86% | B200, B100, H200 |
| AMD | 5-7% (~10% by Q4 2026 est.) | MI300X, MI325X, MI350X |
| Google (TPU) | ~3% | Trillium / v6e |
| Amazon (Trainium) | ~1.5% | Trainium2 |
| Intel | <1% | Gaudi 3 |
| Broadcom (custom) | Expanding | XPU for hyperscalers |

### Market Size:
- AI Accelerators market worth **$174.69B** in 2026 (Mordor Intelligence)
- Growing at **24.3% CAGR** to reach $518.12B by 2031
- NVIDIA FY2026 data center revenue: **$193.7B** (includes non-accelerator)
- AMD data center revenue growing **+40% YoY** expected for 2026 to ~$12.8B (server revenue)

### Growth Trajectory:
- AMD's AI GPU share: ~5% (2024) → ~5-7% (2025) → growing toward ~10% by late 2026
- Key deployments: Meta, Microsoft, OpenAI as largest AMD AI deployers
- Gartner named AMD **"The Company to Beat for Enterprise AI Server CPUs"** (Jun 25, 2026)

---

## 5. RECENT NEWS (Last 7 Days / July 2026)

### July 3, 2026
1. **"Up 140% YTD, Three Catalysts Will Take AMD to New Highs In 2026"** — 24/7 Wall St. PT $589.73. Shares up 152.56% YTD driven by AI infrastructure buildout expanding faster than market can price in.
   - URL: https://247wallst.com/investing/2026/07/03/up-140-ytd-three-catalysts-will-take-amd-to-new-highs-in-2026/

2. **"AMD's Valuation is Stretched at 54.08X P/E: Buy, Sell or Hold?"** — Zacks. Data center momentum strong, but stretched valuation, competition, gaming weakness and margin pressure cloud near-term upside.
   - URL: https://finance.yahoo.com/markets/stocks/articles/amds-valuation-stretched-54-08x-165000812.html

3. **"Top Invesco Analyst: The AI Trade That 'Lifted All Boats' Is Over"** — 24/7 Wall St. Invesco's Fiona Lim warns stock-picking phase begins; profitability now decides winners.
   - URL: https://247wallst.com/investing/2026/07/03/top-invesco-analyst-the-ai-trade-that-lifted-all-boats-is-over-now-profitability-decides-winners-as-capacity-will-catch-up/

4. **"Broadcom Has Barely Moved in 2026. Should You Switch to AMD or Intel Now?"** — 24/7 Wall St. Comparing semi performance as AMD rips +137% YTD.
   - URL: https://247wallst.com/investing/2026/07/03/broadcom-has-barely-moved-in-2026-should-you-switch-to-amd-or-intel-now/

5. **"Intel, Marvell Technology, and AMD Stocks Trade Down"** — StockStory. Broad chip pullback.
   - URL: https://finance.yahoo.com/markets/stocks/articles/intel-marvell-technology-amd-stocks-030024777.html

### July 2, 2026
6. **"Intel Sinks 6% ... AMD Slides 5% as Chip Stocks Pull Back"** — 24/7 Wall St. AMD to $511.67, HSBC sees 60% upside on Intel.
   - URL: https://247wallst.com/investing/2026/07/02/intel-sinks-6-even-as-hsbc-sees-60-upside-amd-slides-5-as-chip-stocks-pull-back/

### June 30, 2026
7. **"Record chip rally adds $2 trillion in combined value to Micron, Intel and AMD in Q2"** — CNBC. Wall Street poured into chipmakers not named Nvidia as AI boom expanded.
   - URL: https://www.cnbc.com/2026/06/30/ai-chip-rally-in-q2-adds-2-trillion-in-value-to-micron-intel-amd-.html

8. **"AMD stock gains as Wells Fargo boosts target, citing AI-driven CPU demand"** — Invezz. Wells Fargo lifted server CPU revenue forecasts sharply to $25B by 2028; 2nm EPYC Venice ramp beginning.
   - URL: https://invezz.com/news/2026/06/30/amd-shares-gain-as-wells-fargo-boosts-target-citing-ai-driven-cpu-demand/

9. **"Intel, AMD Jump 7% as Chip Stocks Catch a Risk-On Bid"** — AMD hit $577 intraday Jun 30.
   - URL: https://247wallst.com/investing/2026/06/30/intel-amd-jump-7-as-chip-stocks-catch-a-risk-on-bid/

### Earlier Notable
10. **"Gartner Names AMD 'The Company to Beat for Enterprise AI Server CPUs'"** — Jun 25, 2026. Stock posted 275.53% growth in past year.
    - URL: https://www.insidermonkey.com/blog/gartner-names-advanced-micro-devices-inc-amd-the-company-to-beat-for-enterprise-ai-server-cpus-1788813/

11. **"AMD Q1 2026 Earnings: Datacenter Sales Mark Shift In AI Purchase Cycles"** — Seeking Alpha (May 6, 2026). Datacenter now >50% of revenue, fueled by Meta deals.
    - URL: https://seekingalpha.com/article/4899495-amd-q1-2026-earnings-datacenter-sales-mark-shift-in-ai-purchase-cycles

12. **"Dell/AMD partnership: Hybrid Architecture for Enterprise AI"** — SiliconANGLE (Jun 23, 2026). Next-gen GPU and PCIe solutions for on-prem, cloud, edge.
    - URL: https://siliconangle.com/2026/06/23/dell-amd-partnership-hybrid-architecture-delltechworld/

13. **"Is It Too Late to Buy AMD Stock After Its 12-Month Gain of 300%?"** — Motley Fool (Jun 10, 2026).
    - URL: https://www.msn.com/en-us/money/other/is-it-too-late-to-buy-advanced-micro-devices-amd-stock-after-its-12-month-gain-of-300/ar-AA25jeQw

---

## 6. KEY BULL/BEAR THESIS

### BULL CASE
- Stock up +137% YTD, +300% in 12 months
- Data center revenue accelerating (+37.8% YoY), now >50% of total revenue
- MI400 (H2 2026): 432GB HBM4, 2nm — genuine NVIDIA competitor for first time
- Venice EPYC CPU (2nm, H2 2026) extends datacenter CPU share gains
- Meta, OpenAI, Microsoft multi-year multi-GW deals
- Forward P/E compressing from 172x trailing to 39x forward as earnings catch up
- 48 analysts: consensus STRONG BUY
- Wells Fargo forecasts $25B server CPU revenue by 2028

### BEAR CASE
- Trailing P/E of 172x means execution risk is priced in
- 80-85% NVIDIA market share vs 5-7% AMD shows moat depth (CUDA ecosystem)
- Gross margins (53%) far below NVIDIA (75%+)
- Gaming segment declining
- Recent chip stock pullback (-5% Jul 2) signals rotation risk
- Invesco warns "capacity will catch up" — AI infrastructure cycle maturing
- $700 target vs $518 price = only 35% upside in best case

---

## 7. DATA SOURCES

### yfinance Data (Financial Metrics)
- Ticker: AMD
- Pull date: July 4, 2026
- All financial numbers verified via yfinance Python library

### News & Analysis Sources
- Yahoo Finance / Zacks / 24/7 Wall St. / CNBC / Seeking Alpha
- Mordor Intelligence (market sizing)
- presenc.ai (market share statistics)
- siliconanalysts.com (competitive analysis)
- spglobal.com (datacenter growth analysis)
- tech-insider.org / techtimes.com (MI400 specifications)
- wccftech.com (roadmap coverage)
- Benzinga / MarketBeat / StockAnalysis.com (analyst targets)

---
*Research compiled July 4, 2026. All financial figures verified via yfinance.*
