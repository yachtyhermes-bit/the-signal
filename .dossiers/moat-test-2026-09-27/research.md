# THE MOAT TEST — Deep Research Dossier
**Article format:** `explainer` (evergreen, educational) · **Sector:** ai (cross-sector)
**Compiled:** Sunday 2026-09-27 (CEST) · **Latest completed US session:** Friday 2026-09-25
**Proposed slug:** `economic-moat-test-ai-durability-2026`
**Prepared by:** Analyst subagent. Every figure below is traced to a primary source (SEC filing, company IR release) or a named reputable outlet. Anything not verified is listed in §10.

---

## 0. HARD RULES FOR THE WRITER (read first)

1. **EVERGREEN ONLY.** No date-stamped claims, no "this week", no exact stock prices, no P/E or P/S multiples, no YTD returns, no market caps as article content. Use only: revenue (TTM / FY), gross & operating margin, ARR, NRR/DBNRR, customer counts, developer counts, ROIC/ROIC-vs-WACC *concepts*, contract values, capacity, market share.
2. **The Signal's curated moat ratings are authoritative — do not contradict them.**
   - **NVDA = Wide, 5 stars, High confidence** (`data/moat-NVDA.json`)
   - **AMD = Narrow, 3 stars, Medium confidence** (`data/moat-AMD.json`)
   - **ZS = Wide, 4★, High** · **RBRK = Wide, 4★, High** · **AXON = Wide, 4★, Medium** · **MU = Wide, 5★, High** · **AMZN = Wide, 4★, High**
   This article's spine is exactly that pair of ratings: **NVDA is the Wide, AMD is the Narrow**, and the piece teaches the reader *how to test* that gap rather than asserting it.
3. **Tone:** institutional/explanatory (Morningstar × Morgan Stanley Counterpoint × SemiAnalysis register). Teach the method, then apply it.
4. Where a number is a **cycle peak** (memory margins), say so — do not present it as a durable moat spread.

---

## 1. WHAT AN ECONOMIC MOAT ACTUALLY IS (the definition beat)

**The Buffett/Morningstar definition (use this as the anchor):**
> "An economic moat … is what allows a company to earn excess returns on capital for a long period of time and keep competitors at bay."
> — [Morningstar, *Economic Moat* definition](https://www.morningstar.com/investing-terms/economic-moat)

**The precise analyst definition (the one that makes it testable):**
> "An economic moat is a structural feature that allows a firm to sustain excess profits over a long period of time. We define **excess profits as returns on invested capital, or ROICs, above our estimate of a firm's cost of capital, or WACC**."
> — [Morningstar Master Equity Research Methodology (PDF)](https://www.morningstar.com/content/dam/marketing/shared/research/methodology/705988Morningstar_Equity_Research_Methodology.pdf)

**The rating thresholds (use verbatim — they give the reader a yardstick):**
- **Wide moat** = competitive advantages expected to last **more than 20 years**
- **Narrow moat** = can fend off rivals for **about 10 years**
- **No moat** = no advantage, or one that dissipates quickly
> — [Morningstar](https://www.morningstar.com/investing-terms/economic-moat)

**The five sources (Morningstar's canonical list — use these five for §2):**
> "Network effect … Intangible assets … Cost advantage … Switching costs … Efficient scale"
> — [Morningstar](https://www.morningstar.com/investing-terms/economic-moat) · corroborated in [Morgan Stanley / Counterpoint Global, *Measuring the Moat* (PDF)](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

**The two-dimension framing (this is the article's method):**
> "One measures the **magnitude** of the positive spread between ROIC and the weighted average cost of capital (WACC) as well as how much the company can invest at that spread. The other reflects **how long** a company can earn that positive spread."
> — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

**Buffett's own warning — the moat is never static:**
> "Economic moats are almost never stable; competitive forces assure that they're either getting a little bit wider or a little bit narrower every day."
> — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

---

## 2. THE FIVE CLASSIC SOURCES, EACH WITH A CONCRETE AI-ERA EXAMPLE

### 2.1 Intangible assets / brand → **NVIDIA's CUDA software stack** (NVDA, Wide 5★)
The Signal's own rating file calls out Nvidia's intangible assets score of 4/5 driven by "premium gross margins 75% reflect brand/IP power; large revenue base (303B) enables sustained IP investment" (`data/moat-NVDA.json`).
Branded, sourced hard numbers:
- **"over 6 million developers and 40,000 companies building on our platforms"** — the CUDA ecosystem, described in Nvidia's own annual review as "one of the largest technical communities in the world, driving a flywheel of innovation, platform adoption, and long-term value creation." — [NVIDIA 2025 Annual Review, filed with the SEC (PDF)](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000098/finalforfiling-2025xannual.pdf)
- **"With over 400 libraries"** — the CUDA-X library stack spans math, deep learning, data processing, physics, quantum and communication libraries. — [NVIDIA CUDA-X technology page](https://www.nvidia.com/en-us/technologies/cuda-x/)
- **Time depth:** CUDA was introduced in **2006** — roughly two decades of accumulated libraries, tutorials and trained engineers. (Nvidia's own framing: "CUDA — our parallel computing programming model **introduced in 2006**.") — [NVIDIA Q1 FY26 Company Overview (PDF)](https://s201.q4cdn.com/141608511/files/doc_presentations/2025/05/Q126-NVDA_Company-Overview.pdf)
- **Teaching line:** a patent expires; a 20-year software ecosystem does not. That is why brand/IP in the AI era is mostly *compiled*, not trademarked.

### 2.2 Switching costs → **enterprise cyber (Zscaler, Rubrik)** (ZS Wide 4★, RBRK Wide 4★)
Full case in §4. One-line version: when security inspection sits inline in every session, "leaving" means re-architecting the network, not cancelling a licence.

### 2.3 Network effects → **Amazon's marketplace flywheel** (AMZN, Wide 4★)
- **"More than 60% of sales in the Amazon store are from independent sellers"**; **more than 75,000 independent sellers surpassed $1 million in sales** in 2025. — [Amazon, *Amazon selling stats*](https://sell.amazon.com/blog/amazon-stats) · the mechanical basis is in the [Amazon 10-K for FY2025 (SEC)](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm) ("We offer programs that enable sellers to grow their businesses… We are not the seller of record in these transactions.")
- **AI-era bridge:** the same flywheel logic now applies to *compute* — the platform with the most developers and the most workloads attracts the most tooling, which attracts more developers. Nvidia's own materials describe exactly this: "The NVIDIA accelerated computing platform has attracted the largest ecosystem of developers." — [NVIDIA Q1 FY26 Company Overview](https://s201.q4cdn.com/141608511/files/doc_presentations/2025/05/Q126-NVDA_Company-Overview.pdf)
- **Caveat to teach:** a network effect is about the *strength of the network*, not the technology. Morningstar found network-effect companies suffered the **fewest** moat downgrades in its AI stress test, precisely because network value is not purely technological. — [Morningstar, *AI Isn't an Economic Moat Killer, but It Will Disrupt Industries*](https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries)

### 2.4 Cost advantage → **Nvidia's scale economics vs AMD** (NVDA Wide 5★ vs AMD Narrow 3★)
The moat file scores Nvidia cost advantage 5/5 — "gross margins 75% well above 50% industry; operating margin 66% vs 25% industry … massive scale ($303B revenue) enables fixed-cost absorption" (`data/moat-NVDA.json`). Sourced hard numbers in §3.
**Teaching line:** a cost advantage is not "cheaper"; it is *structurally lower unit cost at the same price*, which shows up as a gross-margin gap that persists through a cycle.

### 2.5 Efficient scale → **HBM / DRAM oligopoly: Micron, SK hynix, Samsung** (MU, Wide 5★)
- **Three suppliers hold roughly 95% of global DRAM production** — a capital-intensive market where a fourth entrant cannot earn its cost of capital. — [Uncover Alpha, *Every Memory Cycle Ends the Same. Until It Doesn't.*](https://www.uncoveralpha.com/p/every-memory-cycle-ends-the-same)
- **HBM revenue share, Q2 2026:** SK hynix **50%**, Samsung **33%**, Micron **18%** (Q2 2025: 64 / 15 / 21). — [Counterpoint Research, *Global DRAM and HBM Market Share*](https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share) · tabulated at [CTOL Digital](https://www.ctol.digital/news/hbm-market-shift-samsung-rises-hynix-lead-narrows/)
- **All three suppliers' 2026 HBM capacity is fully booked**, with HBM4 a confirmed three-supplier market for Nvidia's Vera Rubin platform. — [CTOL Digital](https://www.ctol.digital/news/hbm-market-shift-samsung-rises-hynix-lead-narrows/)
- **The honest caveat (important, and it does not contradict the Wide rating):** memory is the *textbook* efficient-scale market but also the textbook cyclical one. Efficient scale protects the *structure*; it has historically not protected *margins* through the down-cycle. Nvidia's quarterly GAAP gross margin has ranged from **56.9% (FY2023)** to **75.0% (Q2 FY27)** — even the widest moat in the index is not a straight line. — [Nvidia FY2026 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026)

---

## 3. HOW A MOAT IS MEASURED, NOT ASSERTED

### 3.1 The core metric: ROIC vs cost of capital
> "The spread between ROIC and WACC is a good proxy for value creation, and the stock market tends to reflect this metric. ROIC is defined as net operating profit after taxes (NOPAT) divided by invested capital."
> — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

Economic profit formula for the reader:
> "Economic profit equals the spread between ROIC and WACC times invested capital (**Economic Profit = [ROIC − WACC] × Invested Capital**)."
> — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

**Why growth alone is not a moat:** "Growth only creates value when a company generates returns on investment that exceed the cost of capital." — [Counterpoint Global](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

### 3.2 The fade rate / competitive advantage period (the "how long" dimension)
> "This concept is also known as **fade rate, competitive advantage period (CAP), value growth duration, and T**." And: "High returns attract competition, generally causing economic returns to move toward the cost of capital." — [Counterpoint Global, *Measuring the Moat* (2016 update PDF)](https://sorfis.com/wp-content/uploads/2021/09/Measuring-the-Moat-Mauboussin-November-2016-update.pdf)

> "The time that an average company can sustain excess returns is **shrinking** … This reduction in the period of sustained value creation reflects the greater pace of innovation brought about in part by increased access to, and utilization of, information technology." — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)

### 3.3 THE HARD STAT — regression to the mean in ROIC (use this number)
> "**The spread between the highest and lowest quintile goes from 35 to 15 percentage points over the period** [2017–2022, five years]."
> i.e. the ROIC gap between the best and worst companies **more than halves in five years**. And: "Regression toward the mean (RTM) is a powerful force in business and finance… companies with high ROICs today will have lower ROICs tomorrow."
> — [Counterpoint Global, *ROIC and the Investment Process* (PDF)](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)

**Sector fade rates (nice texture, one sentence):** the five-year autocorrelation of ROIC is **r = 0.46 for consumer staples** vs **r = 0.15 for energy** — i.e. staples moats fade slowly, energy moats fade almost instantly. — [Counterpoint Global, *ROIC and the Investment Process*](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)

**What actually separates the survivors:** of 34 companies that held top-quintile ROIC in 2022, the average **NOPAT margin was 2.7x the universe** while invested-capital turnover was only **1.5x**. Pricing power beats asset efficiency. — [Counterpoint Global](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)

### 3.4 Sourced example — MARGIN PERSISTENCE, GOOD (Nvidia, Widening — but not smooth)
| Fiscal year | GAAP gross margin | Revenue |
|---|---|---|
| FY2022 | **64.9%** | $26,914M |
| FY2023 | **56.9%** (down 8.0 pts) | $26,974M (flat) |
| FY2024 | **72.7%** | $60.9B (+126%) |
| FY2025 | **75.0%** | $130.5B (+114%) |
| FY2026 (ended Jan 2026) | **71.1%** | **$215.9B (+65%)** |
| Q2 FY2027 (quarter ended Jul 26, 2026) | **75.0%** | $96.2B (+106% YoY) |

Sources — FY2022/FY2023 (both from the same table: FY23 56.9% vs FY22 64.9%; FY23 revenue $26,974M vs FY22 $26,914M): [Nvidia Q4/FY2023 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2023). FY2024 72.7% and FY2025 75.0%: [Nvidia Q4/FY2025 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025). FY2026 71.1% and revenue $215.9B: [Nvidia Q4/FY2026 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026). Q2 FY2027: [Nvidia Q2 FY2027 results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027).

**The nuance that makes this section good (do not skip it):** persistence ≠ smoothness. Between FY2022 and FY2023 Nvidia's revenue went **nowhere** ($26.914B → $26.974B) and its gross margin fell **800 basis points** — the crypto/gaming bust. Two years later it printed **75.0%**. A single bad year is not evidence that a moat failed; a *decade* of declining margin (Intel, §3.5) is. That distinction is the whole reason to measure over 5–10 years rather than 4 quarters.

**Nvidia operating margin:** Q2 FY27 GAAP operating income **$63.734B** on revenue **$96.221B** = **~66%**. Cross-checked against `data/financials.json` (NVDA `operatingMargins` = 66.2%). — [Nvidia Q2 FY27](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)

### 3.5 Sourced example — MARGIN EROSION, BAD (Intel, 15-year slide)
| Fiscal year | GAAP gross margin | Revenue |
|---|---|---|
| FY2017 | **62.3%** | — |
| FY2018 | **61.7%** | $70.8B |
| FY2021 | **55.4%** (record revenue **$79.0B**) | $79,024M |
| FY2022 | 42.6% | — |
| FY2023 | 40.0% | — |
| FY2024 | 32.7% | $53,101M |
| FY2025 | **34.8%** | **$52,853M** |

Sources: FY2018 gross margin & FY2021 detail — [Intel FY2021 results (intc.com)](https://www.intc.com/news-events/press-releases/detail/1522/intel-reports-fourth-quarter-and-full-year-2021-financial) and [Intel 2018 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/50863/000005086319000007/a12292018q4-10kdocument.htm); FY2025 revenue & gross profit ($18,375M gross profit ÷ $52,853M revenue = 34.8%) — [Intel Q4/FY2025 results (intc.com)](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial). FY2019/FY2020/FY2022–FY2024 gross-margin history cross-checked at [Billiver, Intel gross margin history](https://billiver.com/company/intel/gross-margin-history).
Full detail of the erosion in §5.

### 3.6 Market-share stability as a test (and how to spot instability live)
- HBM revenue share moved **SK hynix 64% → 50%** and **Samsung 15% → 33%** in a single year. Share *rotation* inside a three-player oligopoly is what an eroding (or forming) moat looks like in real time. — [Counterpoint Research](https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share)
- Morningstar's AI stress test downgraded **22 of 54 wide-moat companies** it reviewed in technology and tech-adjacent sectors — **~40% of the wide moats it examined**. — [Morningstar, *AI Isn't an Economic Moat Killer…*](https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries)

**The reader's measurement checklist (writer can render as a 5-point box):**
1. ROIC vs WACC, averaged over a full cycle (not one year).
2. **Five- and ten-year** gross-margin and operating-margin ranges, not the latest quarter.
3. Reinvestment: is the company finding places to invest at the spread, or just harvesting?
4. Market share direction over 3+ years.
5. The fade horizon: what specifically stops this in year 8–10?

---

## 4. THE TEACHING CONTRAST — NVIDIA (Wide) VS AMD (Narrow)

### 4.1 The Signal's curated ratings — the article must land here
| | NVDA | AMD |
|---|---|---|
| Rating (`data/moat-*.json`) | **Wide, 5★, High confidence** | **Narrow, 3★, Medium confidence** |
| Switching Costs | 5/5 — "dominant segment at 91% of revenue (deep ecosystem lock-in); operating margin 66% vs 25% industry" | **2/5 — "no strong switching-cost indicators detected"** |
| Intangible Assets | 4/5 | **2/5 — "limited intangible asset indicators available"** |
| Network Effect | 5/5 | 5/5 |
| Cost Advantage | 5/5 — "gross margins 75% well above 50% industry" | 4/5 — "gross margins slightly above industry average; significant scale ($41B revenue)" |
| Efficient Scale | 5/5 | 4/5 |
The rating gap is concentrated in **switching costs and intangible assets** — which is precisely the CUDA/ROCm question.

### 4.2 Nvidia's software lock-in — the sourced numbers
- **6 million+ developers** and **40,000 companies** building on Nvidia platforms. — [NVIDIA 2025 Annual Review (SEC)](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000098/finalforfiling-2025xannual.pdf)
- **400+ CUDA-X libraries.** — [NVIDIA CUDA-X](https://www.nvidia.com/en-us/technologies/cuda-x/)
- **CUDA introduced 2006** — ~20 years of accumulation. — [NVIDIA Q1 FY26 Company Overview](https://s201.q4cdn.com/141608511/files/doc_presentations/2025/05/Q126-NVDA_Company-Overview.pdf)
- **Scale of the prize (Q2 FY2027, quarter ended Jul 26, 2026):** total revenue **$96.2B (+106% YoY)**; Data Center revenue **$89.0B (+117% YoY)**; GAAP gross margin **75.0%**; GAAP operating income **$63.7B**; net income **$59.7B**; returned **~$26.0B** to shareholders in the quarter; Q3 FY27 guidance **$108.0B**. — [Nvidia Q2 FY2027](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)
- **Why customers can't cheaply switch:** the lock-in is *system-level*, not kernel-level — cuDNN (deep learning), TensorRT-LLM (inference), NCCL (multi-GPU communication) and NVLink have no full equivalents on the AMD side, so porting a large training stack is a multi-quarter engineering programme, not a driver swap. Conversely, inference is where the gap narrows fastest because vLLM/SGLang abstract hardware differences. — [GPUAdvisor, *CUDA vs ROCm in 2026*](https://gpuadvisor.com/blog/cuda-vs-rocm-2026) · [Servchip, *ROCm vs CUDA (2026)*](https://servchip.com/blog/rocm-vs-cuda-amd-nvidia-ai-stack-2026)

### 4.3 AMD's ROCm gap and where AMD wins
- **The gap is real and quantified:** a rigorous study (Celestial AI, arXiv:2510.27583, Oct 2025) found Nvidia H100/B200 reach **~93% of theoretical peak FLOPS** while the MI300X reaches **~45%** — driven by (a) clock throttling and (b) ROCm software efficiency of **80–85% vs Nvidia's ~93%**. — [Silicon Analysts, *AMD vs NVIDIA AI GPU Market Share 2026*](https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026) · primary paper: [arXiv 2510.27583](https://arxiv.org/abs/2510.27583)
- **Stated remaining gaps:** Linux-only full stack; installer more complex; profiling toolkit less polished than Nsight; **10–30% performance gap in compute-intensive workloads**; less mature multi-node training tooling; StackOverflow/tutorial knowledge base assumes CUDA. **TensorRT has no AMD equivalent.** — [Silicon Analysts](https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026) · [GPUAdvisor](https://gpuadvisor.com/blog/cuda-vs-rocm-2026)
- **What is closing the gap:** ROCm 7.x (up to 3.5x inference perf over ROCm 6.0), first-class PyTorch support, **OpenAI's Triton compiler** as "the great equalizer" (write-once GPU code, now the default in `torch.compile`), and vLLM/SGLang abstracting the stack away. — [Silicon Analysts](https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026)
- **Where AMD has won:** data center segment revenue **$6.718B in Q2 2026, up 107% YoY = 58% of company revenue**; record revenue **$11.536B, +50% YoY**; GAAP gross margin **54%** (from 40%), non-GAAP **56%**; GAAP operating margin **17%**, non-GAAP **27%**. — [AMD Q2 2026 results (ir.amd.com)](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results)
- **Where AMD has not won:** it remains a distant second in scale. **Nvidia's Data Center segment ($89.0B in a quarter) is ~13x AMD's ($6.718B in a quarter).** AMD's Instinct line is estimated at roughly **5–7% of AI accelerator revenue**. — [Nvidia Q2 FY27](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027) vs [AMD Q2 2026](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results); share estimate: [Silicon Analysts](https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026) *(secondary, attribute directionally)*

### 4.4 The margin comparison (the cleanest one-line moat test in the piece)
- **Nvidia: 75.0% GAAP gross margin, ~66% GAAP operating margin** — [Q2 FY27](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)
- **AMD: 54% GAAP gross margin, 17% GAAP operating margin** — [Q2 2026](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results)
- **~21 points of gross margin and ~49 points of operating margin separate them at the same moment in the same cycle.** That gap *is* the moat, measured. Both figures verified against `data/financials.json` (NVDA GM 74.7% / op margin 66.2%; AMD GM 55.7% / op margin 17.2%) — internal file and company filings agree within rounding.
- **And the honest bull note on AMD:** AMD's *direction of travel* is up — gross margin from **40% → 54%**, operating margin from **negative → 17%**, Data Center +107%. A Narrow moat that is *widening* is priced very differently from a Wide moat that is *narrowing* (see §7).

---

## 5. HISTORICAL MOAT EROSION — THE READER'S WARNING

### 5.1 Intel — the canonical case (still live)
- **Revenue:** all-time record **$79.0B (FY2021)** → **$52.9B (FY2025)** — a 15-year low. — [Intel FY2021](https://www.intc.com/news-events/press-releases/detail/1522/intel-reports-fourth-quarter-and-full-year-2021-financial) · [Intel FY2025](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)
- **Gross margin:** **61.7% (FY2018) → 32.7% (FY2024) → 34.8% (FY2025).** — [Intel 2018 10-K](https://www.sec.gov/Archives/edgar/data/50863/000005086319000007/a12292018q4-10kdocument.htm) · [Intel FY2025](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)
- **Profit:** GAAP net loss attributable to Intel of **$(18.8)B in FY2024**, narrowing to **$(0.3)B in FY2025**; FY2025 GAAP operating loss **$(2.2)B**. — [Intel FY2025](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)
- **The foundry bleed:** Intel Foundry segment operating loss **$(13.3)B in 2024** narrowing to **$(10.3)B in 2025**; management targets break-even around 2027, explicitly gated on winning external 14A customers. — [Intel FY2025 supplemental segment table](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial) · context: [Reuters, "Intel discloses $7 billion operating loss for chip-making unit"](https://www.reuters.com/technology/intel-discloses-financials-foundry-business-2024-04-02/)
- **Headcount:** **99.5K (Dec 2024) → 80.1K (Dec 2025).** — [Intel FY2025](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)
- **The teaching point:** Intel's moat was *manufacturing process leadership* — the most physical, most expensive moat there is. It was lost by missing one lithography decision. Intel's own CEO at the time attributed the foundry losses in part to the decision **against using ASML's EUV machines**. — [Reuters](https://www.reuters.com/technology/intel-discloses-financials-foundry-business-2024-04-02/)
- **⚠ Do NOT say Intel lost its foundry unit or was broken up — as of FY2025 it still owns and runs it; the moat *eroded*, the company did not die.**

### 5.2 Cisco — the multiple that broke even though the business didn't
- Revenue went **~$2B (1995) → ~$19B (FY2000)**; revenue was **~$19B (FY2000), $22B (FY2001), ~$19B (FY2002)**; by 2022 sales were **~$52B**, more than double the 2000 level. — [Harding Loevner, *Nvidia and the Cautionary Tale of Cisco Systems*](https://www.hardingloevner.com/insights/nvidia-and-the-cautionary-tale-of-cisco-systems/)
- At the March 2000 peak Cisco became the most valuable company in the world; the stock then **fell ~80–88%** and "on a total return basis, it took **20 years** for Cisco stock to recover." — same source; corroborated by [Wikipedia, Dot-com bubble](https://en.wikipedia.org/wiki/Dot-com_bubble) ("Cisco Systems lost… 80% of its stock value").
- **The teaching point — the single most important paragraph in the piece:** Cisco's *moat held*. Its *multiple didn't*. "That drop wasn't the result of any large change in the company's performance." — [Harding Loevner](https://www.hardingloevner.com/insights/nvidia-and-the-cautionary-tale-of-cisco-systems/)
- **Optional reinforcement:** Cisco's May 2001 **$2.25B inventory write-down** and elimination of **8,500 positions (~18% of the workforce)** — the moat was fine, the demand forecast wasn't. — [Meritshot, *Cisco case study*](https://www.meritshot.com/case-studies/cisco)

### 5.3 The cycle case (30-second version, use as a warning shot)
Memory is the efficient-scale poster child and the cyclical poster child at the same time: three players hold ~95% of DRAM, yet every memory cycle has historically ended the same way. — [Uncover Alpha](https://www.uncoveralpha.com/p/every-memory-cycle-ends-the-same)

---

## 6. THE BEAR CASE ON THE FRAMEWORK ITSELF (mandatory — full paragraph of substance for the writer)

Moat analysis assumes that excess returns persist because barriers persist. The short-seller's objection is that the barriers themselves are being repriced. Three sourced legs:

**(1) AI is attacking switching costs directly — and Morningstar measured it.** In its own AI stress test across **132 companies**, Morningstar downgraded **22 wide moats** (20 to narrow, 2 to none) and **18 narrow moats** — and found that **"switching costs were not as effective, and close to half the downgraded companies were classified as having switching-cost moats at one point."** Notably, "AI could automate key technological processes that were historically sources of switching costs (like data transfers)." The framework's most-used source of advantage is the one the AI era damaged most; **network effects survived best**. — [Morningstar, *AI Isn't an Economic Moat Killer, but It Will Disrupt Industries*](https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries)

**(2) Cheap capital and cheap equity let challengers buy their way in.** The clearest live example is in our own coverage: AMD has financed its challenge not with products alone but with equity — a **6 GW OpenAI partnership carrying a warrant for up to 160 million shares**, and a **6 GW Meta partnership carrying a warrant for up to 160 million shares** (vesting on shipment milestones and, in Meta's case, on AMD's own share price). Together that is **up to 320 million potential shares — roughly 19.6% of AMD's shares outstanding** — issued to buy a position in the market it could not out-engineer. The structural point for readers: when capital is cheap, "barriers to entry" get a price tag, and the incumbent's moat is only as good as the challenger's funding. — [AMD/Meta release (ir.amd.com)](https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus) · [AMD/OpenAI release](https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus) · share count vs [AMD 10-Q Q2 FY26 (SEC)](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm)

**(3) Capex cycles reset advantage — including for the winners.** The five largest hyperscalers are deploying **over $700 billion of aggregate capital expenditure** in a year, up more than 60% — which converts formerly asset-light, high-ROIC franchises into capital-intensive ones, and means today's margin structure is a *function of the current capex cycle*, not a permanent feature. Separately, AI-native startups took a record **~$150 billion of funding in 2025** and are pricing at steep discounts to incumbent subscriptions. — [Interactive Brokers, *Competitive Advantages in the AI Era*](https://www.interactivebrokers.com/campus/traders-insight/securities/macro/second-quarter-equity-outlook-competitive-advantages-in-the-ai-era/)

**(4) The killer example — a Wide-looking position that broke inside a few years.** Intel. In 2018 it printed a **61.7% gross margin** on **$70.8B** of revenue and an unassailable data-center franchise; seven years later its gross margin was **34.8%** on **$52.9B**, with a **$(18.8)B** net loss in FY2024 and a foundry unit still losing **$(10.3)B** a year. That is not a 20-year fade. — [Intel 2018 10-K](https://www.sec.gov/Archives/edgar/data/50863/000005086319000007/a12292018q4-10kdocument.htm) · [Intel FY2025](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)

**The balanced close (Critical — do not let the piece end bearish on the framework):** Morningstar's own conclusion was that the moat framework is degraded, not dead — it **upgraded two narrow moats to wide** on infrastructure-layer positioning and network effects, and found the most resilience in "complex engineering software workflows, cybersecurity, financial infrastructure firms, and offerings with unique data and/or network effect assets." — [Morningstar](https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries). And Counterpoint's framing is that moats are never static: they are "getting a little bit wider or a little bit narrower every day."

---

## 7. THE STOCK ANGLE — WHAT HAS TO HAPPEN FOR A MOATY STOCK TO RE-RATE

This is the article's payoff beat. Four mechanically distinct ideas, all sourced:

**(a) The multiple is a price for *duration*, and duration is the fade rate.**
> "Given the same spread between ROIC and WACC, an investor should pay a higher multiple for a consumer staples company than for an energy company."
> — [Counterpoint Global, *ROIC and the Investment Process*](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)
Translation for the reader: two companies with **identical ROIC-minus-WACC spreads** deserve **different multiples**, purely because one's spread lasts 15 years and the other's lasts 3. Re-rating happens when the market *revises the fade horizon*, not when the quarter beats.

**(b) Excess returns come from *revisions in expectations*, not from good results.**
> "Investors earn excess returns when they correctly anticipate revisions in expectations for a company's financial results."
> — [Counterpoint Global, *ROIC and the Investment Process*](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)
And from *Measuring the Moat*: "investors should expect to earn a market rate of return, adjusted for risk, if a company's share price already captures its prospects for sustainable value creation."
**Consequence:** a company that beats every quarter but whose fade horizon is already fully priced does **not** re-rate. A company the market has written off on fade can re-rate on a *small* improvement in perceived duration.

**(c) 50% growth without a moat vs 15% growth with one.** Do not put this as a formula in the article — teach it as a thought experiment grounded in the two sourced facts above. The mechanical version the reader can apply:
- Value created ≈ (ROIC − WACC) × Invested Capital, **for as long as the spread lasts**.
- Growth **above** WACC creates value; growth **below** WACC destroys it. "Growth only creates value when a company generates returns on investment that exceed the cost of capital." — [Counterpoint Global, *Measuring the Moat*](https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf)
- So: 50% growth funded at negative spread can be value-destructive; 15% growth funded at a wide, persistent spread compounds. The market pays for the second and eventually discounts the first — which is what Intel and Cisco show, from opposite directions.

**(d) Why the ratings gap *is* the re-rating upside.** Connect back to our own files: Nvidia is rated **Wide 5★** and AMD **Narrow 3★**, and the market already pays Nvidia ~21 points more gross margin and ~49 points more operating margin for it. AMD's re-rating case is not "AMD is cheap" — it is "AMD's Narrow moat is *widening*" (gross margin 40% → 54%, operating margin negative → 17%, Data Center +107% YoY). A rating that moves from Narrow toward Wide is the single largest re-rating event in this framework. — [AMD Q2 2026](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results) · `data/moat-AMD.json` vs `data/moat-NVDA.json`

**(e) The concrete test the reader can run on any ticker (render as a numbered box):**
1. **Spread** — What is ROIC vs WACC, averaged over 5–10 years? (Any positive spread is table stakes; magnitude is what matters.)
2. **Persistence** — Has gross margin and operating margin held in a tight band through a full cycle? Nvidia's FY23 56.9% → Q2 FY27 75.0% shows what a *widening* moat looks like; Intel's 61.7% → 34.8% shows a collapsing one. — [Nvidia](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026) · [Intel](https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial)
3. **Source audit** — Which of the five sources produces the spread, and is it the one Morningstar found AI damages most (**switching costs**) or the one it found most resilient (**network effects**)? — [Morningstar](https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries)
4. **Share stability** — Is market share flat or rotating? (HBM: SK hynix 64% → 50% in a year.) — [Counterpoint](https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share)
5. **Fade horizon** — Name the specific thing that stops the spread in year 8. If you cannot name it, you are not underwriting a moat; you are underwriting momentum.
6. **What's priced in** — Has the market already paid for the duration? The re-rating requires a *revision of the horizon*, not another beat. — [Counterpoint Global](https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf)

---

## 8. RECOMMENDED TICKERS

**constraint:** the article's `tickers[]` may only use symbols present in `data/financials.json` (26 total).
**Recommended 3 (Deep Digger pills):** `NVDA` · `AMD` · `ZS`
- **NVDA** — the Wide moat, all five sources, CUDA source data (`moat-NVDA.json`)
- **AMD** — the Narrow contrast; the rating gap the article exists to teach (`moat-AMD.json`)
- **ZS** — the switching-cost case, with the cleanest primary-source NRR/ARR disclosure in cyber (`moat-ZS.json`)

**Strong alternates (safe to swap in):** `MU` (Wide 5★; efficient-scale/HBM example + the cyclicality caveat), `RBRK` (Wide 4★; second switching-cost proof point), `AMZN` (Wide 4★; the network-effect example), `AVGO` / `ANET` (Wide 5★ if the writer wants a custom-silicon angle).
**Do not contradict:** NVDA Wide 5★, AMD Narrow 3★, ZS Wide 4★, RBRK Wide 4★, AXON Wide 4★, MU Wide 5★.

---

## 9. TITLE CANDIDATES (institutional register; none exceed 13 words)

1. **How to Test an AI Moat: Five Sources, ROIC Persistence, Nvidia Versus AMD**
2. **The Moat Test: Durable AI Winners Earn Excess Returns, Not Just Growth**
3. **Testing AI Moats With ROIC, Switching Costs, and the Nvidia-AMD Gap**
4. **Economic Moats Explained: Five Tests for the AI Trade and Where They Fail**
5. **Why Moats Fade: Testing AI Durability Through ROIC and Switching Costs**

**Proposed slug:** `economic-moat-test-ai-durability-2026`
*Alternates:* `moat-test-ai-trade-2026`, `testing-ai-moats-roic-fade-rate-2026`
*Collision check:* no existing slug in `articles/index.json` contains "moat" — no collision. (Nearest neighbours, all distinct: `rubrik-crushes-earnings-dip-2026`, `micron-trillion-dollar-hbm-2026`, `nvidia-vera-rubin-arizona-fab-2026`.)

---

## 10. UNVERIFIED / DO-NOT-PRINT-WITHOUT-CHECKING

1. **Nvidia's AI-accelerator market share percentage.** The "~80%" / "~85%" / "~90-95%" figures all come from secondary aggregators (Silicon Analysts, Compute Market, Servchip) and they disagree with each other. **Do not print a market-share percentage for Nvidia.** Use the primary, undisputed substitute: **Nvidia Data Center revenue $89.0B in a quarter vs AMD Data Center revenue $6.718B in a quarter (~13x)** — both from company releases.
2. **AMD's "5–7% of AI accelerator revenue."** Secondary estimate only (Silicon Analysts). Attribute explicitly if used, or drop.
3. **The Celestial AI arXiv paper (2510.27583)** is a third-party preprint, not a vendor or regulator filing. The ~45% vs ~93% MFU figures are widely cited but are one research group's benchmark. Label as "one independent benchmarking study."
4. **ROIC and WACC for individual companies.** I did **not** verify a company-published ROIC for NVDA, AMD, ZS or MU (issuers do not report ROIC). `data/financials.json` provides ROE and margins, not ROIC. **The article should teach the ROIC-minus-WACC method and cite Counterpoint's aggregate RTM statistic (35pp → 15pp over five years) — never assert a specific company ROIC or a specific WACC.**
5. **Cisco's exact peak market capitalisation and peak share price.** Sources give "$500B+", "$555B", "$569B" and "$79" vs "$80" vs "$82". Use "became the most valuable company in the world" and "fell roughly 80%" only — no precise figures.
6. **Intel Foundry FY2025 operating loss $(10.3)B.** This is straight from Intel's own supplemental segment table in the FY2025 release, but note it is a *segment* measure with intersegment allocations and is **not** additive to the consolidated result. Some third-party write-ups (e.g. The Teardown) report "~$2.5B in 2025" — that is Intel Foundry's **Q4 2025 only** figure (revenue $4,507M − costs $7,016M = $(2,509)M), misattributed as a full year. **Prefer the annual $(13.3)B → $(10.3)B** and describe it as Intel's segment disclosure.
7. **Nvidia's Q2 FY2027 operating margin of ~66%** is my arithmetic (GAAP operating income $63,734M ÷ revenue $96,221M). It matches `data/financials.json` NVDA `operatingMargins` = 66.2%, so it is safe — but if the writer prefers, quote the two disclosed line items and let the reader do the division.
8. **Rubrik's "~120% net revenue retention"** comes from the prior internal dossier (`rbrk-ai-data-security-moat-2026-research.md`, which cites Rubrik's Q1 FY27 10-Q). I could **not** re-verify it this session — `ir.rubrik.com` returns HTTP 403 to automated fetches and SEC EDGAR blocked the request. The **Q2 FY27 metrics I did verify** (via the company's Q2 FY27 press release reproduced at StorageNewsletter) are: **subscription ARR $1.66B, +33% YoY**; **revenue $427.3M, +38% YoY**; **GAAP gross margin 78.4%, non-GAAP 81.0%**; **subscription ARR contribution margin 14.0% vs 9.4%**. **Use these verified figures; treat the ~120% NRR as needing a fresh check.**
9. **Zscaler's Q4 FY26 press release URL** (`ir.zscaler.com/...`) returned HTTP 403 to automated fetch even though it is a live, indexed page. The figures below are cross-verified from the transcript and the SEC 8-K exhibit — see §11 for URLs. A human/browser check will load it fine.
10. **"OpenAI's Triton is the great equalizer of GPU programming"** — attributed to AMD VP Anush Elangovan by Silicon Analysts, but I did not find the original quote in an AMD-published source. Attribute to the outlet, or skip.
11. **Nasdaq/AMD market-cap and any 2026 YTD figures** — deliberately excluded. Evergreen only.
12. **Micron's HBM "sold out for 2026"** — reported consistently (CTOL, Gate, Uncover Alpha) but the underlying claim originates from Micron/SK hynix commentary relayed by third parties. Safe phrasing: "all three HBM suppliers' 2026 capacity has been reported as fully booked."

---

## 11. SOURCE LIST (every URL used above)

**Framework / measurement**
- Morningstar, *Economic Moat* (definition, five sources, 10/20-year thresholds) — https://www.morningstar.com/investing-terms/economic-moat
- Morningstar Master Equity Research Methodology (PDF) — https://www.morningstar.com/content/dam/marketing/shared/research/methodology/705988Morningstar_Equity_Research_Methodology.pdf
- Counterpoint Global / Mauboussin, *Measuring the Moat* (PDF) — https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf
- Counterpoint Global / Mauboussin, *Measuring the Moat*, 2016 update (fade rate / CAP, PDF) — https://sorfis.com/wp-content/uploads/2021/09/Measuring-the-Moat-Mauboussin-November-2016-update.pdf
- Counterpoint Global, *ROIC and the Investment Process* (PDF — RTM 35pp → 15pp; sector autocorrelations; NOPAT margin 2.7x) — https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf
- Morningstar, *AI Isn't an Economic Moat Killer, but It Will Disrupt Industries* (132-company AI moat review) — https://www.morningstar.com/stocks/ai-isnt-an-economic-moat-killer-it-will-disrupt-industries
- Morningstar, *AI and Economic Moats: Which Stocks Are Most at Risk?* — https://www.morningstar.com/markets/ai-economic-moats-which-stocks-are-most-risk

**Nvidia**
- Q2 FY2027 results (quarter ended 2026-07-26; rev $96.221B +106%, DC $89.0B +117%, GAAP GM 75.0%, GAAP op income $63.734B, net income $59.688B, Q3 guide $108.0B) — https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027
- Q4/FY2026 results (FY26 rev $215.9B +65%, GAAP GM 71.1%; Q4 GAAP GM 75.0%) — https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026
- Q4/FY2025 results (FY25 GAAP GM 75.0%, FY24 72.7%; FY25 rev $130.5B +114%) — https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025
- Q4/FY2023 results (FY23 GAAP GM 56.9% vs FY22 64.9%; FY23 rev $26,974M vs FY22 $26,914M) — https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2023
- NVIDIA 2025 Annual Review, SEC-filed (6M+ developers, 40,000 companies) — https://www.sec.gov/Archives/edgar/data/1045810/000104581025000098/finalforfiling-2025xannual.pdf
- CUDA-X (400+ libraries) — https://www.nvidia.com/en-us/technologies/cuda-x/
- Q1 FY26 Company Overview (CUDA introduced 2006; ~5.9M developers; ecosystem framing) — https://s201.q4cdn.com/141608511/files/doc_presentations/2025/05/Q126-NVDA_Company-Overview.pdf

**AMD**
- Q2 2026 results (rev $11.536B +50%; DC $6.718B +107% = 58% of revenue; GAAP GM 54%, NG 56%; GAAP op income $1.990B, 17% margin; NG op margin 27%) — https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results
- AMD + Meta, 6 GW, 160M-share warrant (2026-02-24) — https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus
- AMD + OpenAI, 6 GW, 160M-share warrant — https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus
- AMD Q2 FY26 10-Q (shares outstanding 1,632,475,042) — https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm
- ROCm gap analysis — https://siliconanalysts.com/analysis/amd-vs-nvidia-ai-gpu-market-share-2026 · https://gpuadvisor.com/blog/cuda-vs-rocm-2026 · https://servchip.com/blog/rocm-vs-cuda-amd-nvidia-ai-stack-2026 · preprint https://arxiv.org/abs/2510.27583

**Zscaler (switching-cost case)**
- Q4/FY2026 results (reported 2026-09-03): revenue **$898M +25%**, FY26 revenue **$3.4B +25%**, **ARR $3.771B +25%**, net new ARR $246M, **non-GAAP gross margin 80.2%**, **non-GAAP operating margin 24.3% (record)**, FY26 FCF **$779M (23% margin)**, **RPO ~$7.4B +27%**, **785 customers >$1M ARR (+18%)**, **4,182 customers >$100K ARR (+20%)**, **Z-Flex >$1.7B TCV in FY26 with an average ~30% ARR uplift**, non-seat metered ≈**30% of new/upsell ACV** with ARR on those offerings **+100%+ YoY**, FY27 guide ARR **$4.396–4.426B (+16.6–17.4%)**, **DBNRR 115% (consistent through FY26)** — https://ir.zscaler.com/news-releases/news-release-details/zscaler-announces-strong-fourth-quarter-and-fiscal-2026 (live page; 403s to bots) · transcript mirror: https://www.tradingkey.com/news/transcripts/262150882-tradingkey · SEC 8-K exhibit mirror: https://app.edgar.tools/filing/1713683/0001713683-26-000156/zs-07312026_991.htm

**Rubrik (second switching-cost proof point)**
- Q2 FY27 results (2026-08-27): subscription ARR **$1.66B +33%** (cloud ARR $1.48B, +39%), revenue **$427.3M +38%**, GAAP GM **78.4%**, non-GAAP GM **81.0%**, subscription ARR contribution margin **14.0% vs 9.4%** — https://www.storagenewsletter.com/2026/08/28/rubrik-fiscal-2q27-financial-results/ (company press release reproduced)

**Moat erosion / bear case**
- Intel FY2025 results (rev $52.853B, gross profit $18.375B = 34.8% GM, net loss attributable $(267)M, FY2024 net loss $(18,756)M, employees 80.1K vs 99.5K, Intel Foundry FY25 op loss $(10,318)M vs FY24 $(13,291)M) — https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial
- Intel FY2021 results (record rev $79.0B, GAAP GM 55.4%) — https://www.intc.com/news-events/press-releases/detail/1522/intel-reports-fourth-quarter-and-full-year-2021-financial
- Intel 2018 10-K (rev $70.8B, GAAP GM 61.7%; 10nm delays acknowledged by Intel) — https://www.sec.gov/Archives/edgar/data/50863/000005086319000007/a12292018q4-10kdocument.htm
- Intel gross-margin history FY2016–FY2025 — https://billiver.com/company/intel/gross-margin-history
- Reuters, *Intel discloses $7 billion operating loss for chip-making unit* (EUV decision) — https://www.reuters.com/technology/intel-discloses-financials-foundry-business-2024-04-02/
- Harding Loevner, *NVIDIA and the Cautionary Tale of Cisco Systems* — https://www.hardingloevner.com/insights/nvidia-and-the-cautionary-tale-of-cisco-systems/
- Wikipedia, *Dot-com bubble* (Cisco −80%) — https://en.wikipedia.org/wiki/Dot-com_bubble
- Interactive Brokers, *Second Quarter Equity Outlook: Competitive Advantages in the AI Era* (>$700B hyperscaler capex; ~$150B AI-native funding; ROIC erosion, switching-cost decay) — https://www.interactivebrokers.com/campus/traders-insight/securities/macro/second-quarter-equity-outlook-competitive-advantages-in-the-ai-era/

**Efficient scale / network effects**
- Counterpoint Research, *Global DRAM and HBM Market Share: Quarterly* — https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share
- CTOL Digital (HBM share table; HBM4 three-supplier qualification) — https://www.ctol.digital/news/hbm-market-shift-samsung-rises-hynix-lead-narrows/
- Uncover Alpha (three players ≈95% of DRAM) — https://www.uncoveralpha.com/p/every-memory-cycle-ends-the-same
- Amazon, *Amazon selling stats* (>60% of store sales from independent sellers) — https://sell.amazon.com/blog/amazon-stats
- Amazon FY2025 10-K (SEC) — https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm

**The Signal internal (authoritative — do not contradict)**
- `data/moat-NVDA.json` (Wide, 5★, High) · `data/moat-AMD.json` (Narrow, 3★, Medium) · `data/moat-ZS.json` (Wide, 4★) · `data/moat-RBRK.json` (Wide, 4★) · `data/moat-AXON.json` (Wide, 4★) · `data/moat-MU.json` (Wide, 5★) · `data/moat-AMZN.json` (Wide, 4★)
- `data/financials.json` — NVDA GM 74.7% / op margin 66.2%; AMD GM 55.7% / op margin 17.2%; ZS GM 76.9%; RBRK GM 80.2%; MU GM 72.6%

---

## 12. SUGGESTED STRUCTURE FOR THE WRITER (700–800 words)

1. **Open (~90w):** the question every AI investor is actually asking — "is this a durable winner or just momentum?" State that a moat is a measurable thing, not a vibe, and that the test has five parts.
2. **What a moat is (~110w):** Buffett/Morningstar definition; the ROIC-above-WACC core; the 10-year/20-year thresholds. Land the line: *a moat is not growth, it is a spread that persists.*
3. **The five sources with five AI examples (~180w):** Nvidia's 400 libraries and 6M developers (intangible/network); Zscaler's 115% net retention (switching costs); Amazon's 60% third-party units (network effects); Nvidia's 75% gross margin vs AMD's 54% (cost advantage); three suppliers holding ~95% of DRAM (efficient scale).
4. **How you measure it (~120w):** the 35pp→15pp ROIC regression-to-mean stat; Nvidia's 56.9%→75.0% margin path vs Intel's 61.7%→34.8%. The reader's five-check box.
5. **Nvidia vs AMD (~130w):** our Wide 5★ vs Narrow 3★ ratings; CUDA's switching cost (400 libraries, TensorRT/NCCL/NVLink with no full AMD equivalent); AMD's 45% vs 93% peak-FLOPS utilisation from one independent study; the ~21pt gross-margin and ~49pt operating-margin gap; and AMD's *widening* direction of travel.
6. **The case against the framework (~120w):** one dense paragraph from §6 — Morningstar's 22-of-54 wide-moat downgrades and the switching-cost finding; AMD buying share with 320M warrant shares; $700B of hyperscaler capex; Intel's seven-year collapse. Close with Morningstar's own two upgrades so the piece is not nihilistic.
7. **What has to happen to re-rate (~110w):** duration is the multiple; re-rating requires a *revision of the fade horizon*, not a beat; 50%-growth-no-moat vs 15%-growth-with-moat as a thought experiment; AMD's Narrow→Wide path as the biggest re-rating event in the framework.
8. **Close (~70w):** the reader's test in five questions. Final line should be a test, not a prediction.
