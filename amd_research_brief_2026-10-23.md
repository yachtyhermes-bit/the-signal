# AMD RESEARCH BRIEF — compiled Fri 2026-10-23, 10:00 ET
**PROPOSED SLUG: `amd-helios-rack-margin-test-2026`** (verified free: no `amd-helios*` in articles/posts, 543 posts scanned; article count grep clean)

Last completed close: **$507.93 (Thu 2026-10-22)**, −8.10% from $552.72. Session low $502.60. Volume ~27.9M.
(2026-10-23 is in progress at compile time — yfinance returns an intraday $516.72. Do not use it as a close.)

---

## 1. THE TAPE — 22 October 2026 (verified)

| | Move | Close |
|---|---|---|
| AMD | **−8.10%** | $507.93 |
| SOX | **−6.72%** | 10,731.98 |
| Nasdaq Comp | −2.60% | 26,008.86 |
| S&P 500 | −1.21% | 7,663.43 |
| NVDA | −4.40% | $212.21 |
| MRVL | −8.0% | $223.47 |
| INTC | −8.04% | $85.49 |
| LRCX | −11.76% | $230.15 |
| META | ≈−7% | — |

- Reuters (via The Circuitry): "The Philadelphia SE Semiconductor Index plunged 6.7%, its biggest daily drop since June 23, and is now more than 26% below its June 22 record close." Intel, AMD, SanDisk and Marvell each fell more than 8%.
- My own index math on ^SOX closes: record close **14,634.72 (Jun 22, 2026)**; Oct 22 close = **−26.7%** off it. SOX still **+51.5% YTD**.
- AMD context: **+137.2% YTD** (from $214.16 on 2025-12-31), **−21.8%** off its record close $649.42 (Oct 6, 2026); **−22.9%** off the $658.52 52-week intraday high. 1-month **−17.4%**. NVDA is only **+13.8% YTD** and −11.3% off its own Oct 6 high — AMD is the high-beta leg of the trade, not a proxy for it.
- Same-day, larger frame: 10-year Treasury yield −18.5bp to ~4.96%; Brent +4% to $113.17; Dow flat. This was a *rate/AI-financing* scare expressed through chips, not an AMD-specific event.

## 2. THE TRIGGER — two separate things got welded together

**(a) Lam Research, Q1 FY2027 call, Wed Oct 21 after the close.** Numbers: revenue $8.22B (cons. $8.14B), non-GAAP EPS $2.20 (cons. $2.18), record GM 52.4%. December guide $8.6B ±$400M, EPS $2.33 ±$0.15, GM 52.5%. The line that moved the tape, CFO Doug Bettinger, verbatim from the LSEG transcript:

> "I would mention that this revenue guide would have been a bit higher, if not for some near-term supply chain constraints that we are actively managing."

- CEO Tim Archer, prepared remarks, verbatim: *"As we move into calendar year 2027, we see clean room space availability and supply chain constraints for certain components continuing to limit chip makers and equipment companies' ability to fully meet end demand."*
- Archer defused it on the Q&A, verbatim: *"for those of us who were around during the COVID shortages, this is nothing like that… I think we'll be caught up very shortly."* Bettinger declined to quantify; he said affected December shipments move into March.
- **Why it hit AMD:** the market read a *supplier* constraint as a *ceiling on AI silicon output*. Lam also guided 2027 WFE "more than $200 billion" (vs mid-$150B for 2026) — a bullish number that got ignored.

**(b) Meta Q3 2026, reported Wed Oct 21 after the close.** Revenue $64.60B (+26%); **capex $34.91B in the quarter**; FY26 capex narrowed to **$135–145B, raising the low end from $130B**; **free cash flow −$2.12B vs +$10.63B a year earlier** — first negative FCF in more than a decade; new **Class C non-voting shares** (a 2-for-1 in economic effect, trading from late January 2027) explicitly to build capital-raising capacity; **no 2027 capex number given** — "still developing our budget and capacity plans." Meta's 5-year CDS spread hit an all-time wide.
- This is the "AI payback" leg: the largest capex spenders are now funding buildouts with negative FCF and equity, which reprices every supplier whose order book depends on that spend.

## 3. WHAT AMD ACTUALLY DOES (plain English)

AMD designs chips and the software/systems blueprint around them; it owns no fabs (TSMC makes its leading-edge silicon). Four revenue lines:

- **Data Center** (58% of Q2'26 revenue): **EPYC** server CPUs and **Instinct** GPU accelerators, plus Pensando DPUs/NICs and adaptive SoC. $6.718B in the June 2026 quarter.
- **Client** — Ryzen PC/laptop CPUs ($3.062B, +23%).
- **Gaming** — Radeon GPUs and semi-custom console chips ($779M, **−31%**, console cycle trough).
- **Embedded** — Xilinx-derived FPGAs/adaptive SoC ($977M, +19%).

**The AI stack, 2025–2026 datapoints only:**
- **Instinct MI350/MI355X** — the volume product now. AMD called MI350 "the fastest ramping product in company history" (Nov 11, 2025 Financial Analyst Day). Instinct sales "more than doubled year over year" in Q2'26.
- **Instinct MI400 Series** — launched at Advancing AI, **July 23, 2026**: **MI455X** (flagship; 432GB HBM4, 12 stacks, 23.3TB/s, 320B transistors, CDNA 5, direct liquid cooling) and **MI430X** (HPC/sovereign). AMD's own comparison table on the product page puts MI455X at 432GB vs **NVIDIA Vera Rubin 288GB**, 23.3 vs 22.0 TB/s. Note the naming overlap: the family is "MI400 Series," while customer commitments and the Q2 release also say "MI450 Series" — same silicon generation, two labels. Do not treat them as different products.
- **Helios** — rack-scale reference system: **72 MI455X** GPUs per rack (AMD spec, per launch materials), EPYC "Venice" CPUs, Pensando networking, ROCm. **In production**; Su said on the Aug 4 call initial shipments begin "later this quarter" (Q3'26), ramping through Q4 into 2027. On Oct 6 in Taipei she said Helios "began shipping on schedule in Q3." AMD says Helios delivers "up to 15% more throughput at the same rack power and up to 30% more tokens per dollar than the competition."
- **ROCm** — the open software stack (HIP/HIPIFY for CUDA porting; PyTorch/TensorFlow/JAX/vLLM/SGLang support). **ROCm.ai** launched July 2026 as an AI-native developer layer. AMD says open-source contributions to ROCm rose tenfold in a year.
- **MI500** — planned 2027.

**CRITICAL for the article:** AMD's 10-Q says, verbatim: *"Although we supply certain products used in Helios-based system, we do not manufacture or sell the completed Helios rack systems."* Helios is a design AMD *"develop[s] and license[s] for implementation by customers and their manufacturing partners."* So AMD books **silicon content**, not rack-level revenue at system-integrator margins. "Rack-scale dilutes gross margin because AMD sells whole racks" is **not** AMD's disclosed mechanism. The real mechanism is mix: data-center AI gross margin runs "slightly below corporate average" (CFO Jean Hu, Q2'26 call), and HBM4-heavy MI455X is the reason.

## 4. DISCLOSED NUMBERS (Q2'26, reported Aug 4, 2026)

| | Q2'26 | Y/Y |
|---|---|---|
| Revenue | $11.536B | +50% |
| GAAP gross margin | 54% | +14pts |
| Non-GAAP gross margin | 56% | +13pts (vs 55% in Q1) |
| GAAP operating income | $1.990B | from −$134M |
| Non-GAAP operating income | $3.094B (27%) | +245% |
| Data Center | **$6.718B** | **+107%** (+16% q/q) |
| — DC operating income | $2.103B (**31.3%**) | from −$155M |
| Client / Gaming / Embedded | $3.062B / $779M / $977M | +23% / −31% / +19% |
| FCF | $1.558B | — |
| Cash + STI | $13.111B | — |
| Total debt (principal) | $3.226B | — |
| Inventory | $8.5B | up sequentially "to support expected demand" |

Data Center trajectory: **+22%** (Q3'25, $4.341B) → **+39%** (Q4'25, $5.380B) → **+57%** (Q1'26, $5.775B) → **+107%** (Q2'26). Note the +107% laps a quarter distorted by the $800M MI308 China export-control charge.

**Guidance:** Q3'26 revenue **~$13B ±$300M** (+41% y/y, +13% q/q), non-GAAP GM **~56%**, opex ~$3.65B, tax 13%, diluted shares ~1.66B. Consensus sits at **$13.078B / EPS $1.934** — i.e. only +0.6% above the revenue midpoint. The Street is not positioned for a big beat.

**2027 framework (Aug 4 call):** data center segment revenue **to more than double**; server CPU revenue **+70%+** (after +80% in H2'26); AI accelerator growth "accelerating in 2027"; data-center AI TAM **$1.4T by 2030** at >45% CAGR; total AI compute TAM approaching **$2T**. Revenue per gigawatt: Su, verbatim — *"in terms of the revenue per gigawatt, I think we've said double-digit billions. We're still in that range."* (The "$15B/GW" figure in that exchange is BofA analyst Vivek Arya's assumption, **not** AMD's.)

## 5. THE DEALS, AT THEIR STATED SCALE

- **OpenAI — 6GW, Oct 6, 2025.** First 1GW of MI450-series starts 2H 2026. **Warrant for up to 160M shares at $0.01**, vesting in tranches tied to 1GW→6GW purchases, with stock-price hurdles that **escalate to $600/share for the final tranche**; expires Oct 5, 2030. 8-K confirms OpenAI signed a **binding commitment for the first 1GW**. AMD's CFO: expected "to deliver tens of billions of dollars in revenue."
- **Meta — 6GW, Feb 24, 2026.** Custom MI450-based GPU + Venice EPYC + ROCm on Helios; first 1GW shipments 2H 2026. Second **160M-share, $0.01 warrant**, same milestone structure. **No dollar value was disclosed.** — ⚠️ The site's May 24, 2026 article is titled "AMD Locks Down Meta With a **$100 Billion** Chips-for-Stock AI Deal." Neither AMD's release nor the 8-K states $100B; CNBC reported terms were not disclosed and cited an analyst estimating "tens of billions." **Do not repeat $100B as fact.**
- **Anthropic — up to 2GW of MI450 in Helios**, first 1GW beginning **H1 2027**, plus a multiyear engineering tie-up using Claude to optimize Instinct/ROCm. AMD is also investing up to $5B in Anthropic (per DCD, secondary).
- **Microsoft** — Helios at scale on Azure for frontier-model inference, plus two EPYC VM series and broader Pensando DPU deployment. **Oracle** — first publicly available MI450 supercluster, **initial 50,000 GPUs from Q3 2026**.
- Named Helios deployers in AMD's own release: Anthropic, Cirrascale, HUMAIN, Meta, Microsoft, OpenAI, Oracle, Tensorwave, Vultr.
- **As of June 27, 2026, no warrant tranche had vested** (10-Q). The first OpenAI/Meta tranche vests on the initial 1GW of shipments — so Q3/Q4 is when dilution starts, not before.

## 6. BULL CASE IN NUMBERS (for balance)

- Data Center at $6.718B/quarter and 31.3% segment operating margin, growing 107%.
- Non-GAAP gross margin *expanded* 200bp y/y to 56% and is guided flat at ~56% through the Helios ramp — the dilution thesis has no evidence in the reported numbers yet.
- Balance sheet: $13.1B cash vs $3.2B debt; positive FCF every quarter.
- Unconditional purchase commitments **$30.3B** (from $12.2B at FY25 year-end), of which **$17.4B due in the remainder of FY2026** — capacity is booked, not hoped for. Plus $4.5B of leases not yet commenced and $4.1B of data-center lease guarantees.
- AMD's own spec sheet: 432GB HBM4 / 23.3TB/s vs Vera Rubin's 288GB / 22.0TB/s.

## 7. BEAR CASE, WITH NUMBERS

1. **Scale, not share, is the problem.** NVIDIA's July-2026 quarter: revenue **$96.2B**, Data Center **$89.0B** (+117% y/y), GAAP gross margin **75.0%**. AMD's entire Data Center segment was **$6.718B** — **7.5%** of NVIDIA's DC revenue — at 56% non-GAAP GM. In one quarter NVIDIA added **$47.9B** of data-center revenue year-over-year ($89.023B vs $41.096B); AMD added **$3.48B** ($6.718B vs $3.240B).
2. **Valuation on the forward number, with the basis stated.** At $507.93: **66.9x CY2026E EPS $7.59** and **32.2x CY2027E EPS $15.76**. (The widely quoted 32.8x is the same field computed at the intraday $517.17.) Against that, **NVIDIA trades at 22.9x its current fiscal year ($9.31) and 13.4x the next ($15.91)** — AMD carries roughly 3x the multiple of the company with 13x its data-center revenue. And the FY27 AMD estimate has a **$9.60–$20.25 range across 50 analysts** — a 2:1 spread. At the low end, "32x forward" is 52.9x.
3. **The demand is bought with equity.** Two 160M-share warrants at $0.01 = up to **320M shares, ~19.6% of the 1.632B share count**, vesting only if customers actually take 6GW each and the stock clears escalating price hurdles to $600. Either the milestones hit (dilution) or they don't (the backlog was never real).
4. **Customer concentration is now explicit in the model.** Three customers (OpenAI, Meta, Anthropic) = 14GW of stated commitments. AMD's 10-Q: *"We depend on a small number of customers for a substantial portion of our business."* On Oct 8, 2026 a Financial Times report that OpenAI's annualized revenue was ~$50B rather than the ~$70B previously reported knocked AMD −4% in a day — the market is already trading AMD as a levered bet on three balance sheets.
5. **Software.** CUDA has roughly a decade's head start; independent benchmark work puts CUDA 10–30% ahead on equivalently powered GPUs, and HIPIFY translation still leaves manual tuning. ROCm downloads/contributions are growing fast but are a lagging indicator of production adoption.
6. **AMD doesn't control the rack.** It licenses the Helios design and ships silicon; ODM partners build the racks. Every gigawatt commitment depends on someone else's manufacturing execution — the same failure mode that hit NVIDIA's GB200 ramp. 10-Q risk factor: constraints "could reduce demand for, or delay shipments of our products."
7. **The CPU moat is being attacked from above.** NVIDIA's Vera (Arm, 88 custom cores) is now a standalone product: ~$20B of FY revenue targeted, ~$200B TAM claimed, a Modal design win (Oct 19), and a 256-CPU Supermicro rack (Oct 22). EPYC is reportedly sold out through 2027 with >30-week lead times — good for pricing, bad if a customer decides to design around it.
8. **Commitments cut both ways.** $30.3B unconditional, $8.5B inventory, and prepayments — if a customer slips a quarter, that's a write-down, not a delay. Q4'25 already showed the pattern: a $360M MI308 reserve release flattered GM by ~2pts (55% ex-items vs 57% reported).

**Short interest is NOT the bear case:** 39.3M shares, **2.42% of float**, 1.83 days to cover. This is a valuation/positioning selloff, not a short raid. Say so.

## 8. METRIC CORRECTIONS THE PARENT NEEDS

| Given | Verified | Note |
|---|---|---|
| TTM revenue $41.305B | ✅ $41.305B | 9.246 + 10.270 + 10.253 + 11.536; matches filings |
| TTM FCF **$8.403B** | ❌ **$7.736B** | Sum of *AMD-reported* FCF: 1.530 (Q3'25) + 2.082 (Q4'25) + 2.566 (Q1'26) + 1.558 (Q2'26). The $8.403B comes from yfinance's `quarterly_cashflow` row, which uses OCF−capex only and omits principal payments on finance leases (it overstates Sep-25 by $371M and Dec-25 by $296M). Use $7.74B, or quote H1'26 FCF $4.124B. |
| Total debt **$4.28B** | ⚠️ **$3.226B** principal debt (10-Q: "aggregate principal short-term and long-term debt obligations were $3.3 billion"). yfinance's $4.276B appears to include finance/operating lease obligations | If you print $4.28B, label it "total debt including leases"; the company's own number is $3.2B |
| Cash+STI $13.11B | ✅ $13,111M | exact |
| 52w range $188.22–$658.52 | ✅ | high on Oct 6, 2026; closing high $649.42 |
| Forward P/E ~32.8 | ⚠️ **32.2x at the close** | 32.8x is the provider field at the intraday $517.17. Also state the basis: FY2027E EPS $15.76, not NTM. CY2026E basis is 66.9x. |
| 50 analysts, mean target $637.61, "strong buy" | ✅ yfinance (recMean 1.49) | Cross-check: MarketBeat **"Moderate Buy," $606.76, 43 ratings (3 Strong Buy / 31 Buy / 8 Hold / 1 Sell)**. Target range $365 (−28%) to $1,250. Dispersion is enormous — cite the range, and prefer "consensus Buy" over "strong buy" if you want a defensible label. |
| Next earnings Tue 2026-11-03 | ✅ | Company PR Oct 6: after the close, call 5:00pm ET |

## 9. WHAT NOV 3 HAS TO SHOW

1. **First Helios revenue recognized** (guide implies Q3 is "the very beginning of the ramp") — and the first warrant tranche vesting trigger (1GW shipped).
2. **Data Center ≈ $8B** to hit the $13B guide (arithmetic from guidance: DC ~$8B implies ~+19% q/q) — derived, not company-guided.
3. **Non-GAAP GM ≥56%.** A miss here is the only hard evidence for the dilution thesis.
4. **Reaffirmation of "data center more than double in 2027"** and of HBM4 supply adequacy.
5. Whether management addresses the supply-chain read-through from Lam at all (they were not asked about it in August).

## 10. SOURCES (all fetched HTTP 200, full text)

1. https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results — DC $6.718B/+107%, Q3 guide $13B/56%, Helios in production, Anthropic 2GW, cash $13.111B, debt $3.226B
2. https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm — "we do not manufacture or sell the completed Helios rack systems"; $30.3B commitments; $3.3B debt; warrants unvested
3. https://filecache.investorroom.com/mr5ir_lamresearch2/1525/LRCX-USQ_Transcript_2026-10-21.pdf — verbatim Bettinger "would have been a bit higher if not for some near-term supply chain constraints…"; Archer 2027 clean-room language; "nothing like that"
4. https://www.cnbc.com/2026/10/22/meta-stock-q3-earnings-free-cash-flow.html — Meta FCF −$2.12B, capex floor raised to $135B, record CDS spread
5. https://thecircuitry.to/article/nasdaq-has-its-worst-day-since-june-as-chip-stocks-plunge-67-mvk7webu — Reuters-sourced Oct 22 tape: SOX −6.7%, AMD/INTC/MRVL/SanDisk >−8%, LRCX −11.75%, Nasdaq −2.60%
6. https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm — NVIDIA Q2 FY27: revenue $96.2B, DC $89.0B, GM 75.0%

Also fetched and verified (available if you want more than six): Motley Fool AMD Q2'26 transcript (2027 guidance, "double-digit billions" per GW, Hu margin commentary); AMD/OpenAI 8-K d28189d8k.htm (160M warrants, $0.01, $600 final tranche); AMD Q3'26 earnings-date PR (Nov 3, 5pm ET); AMD MI455X product page (432GB HBM4 / 23.3TB/s vs Vera Rubin 288GB); AMD Q3'25 and Q4'25 releases (segment history, FCF $1.530B / $2.082B); IR Meta Q3 release (403 to curl, read via CNBC + Motley Fool transcript).

## 11. NOT VERIFIED — do not print as fact

- **KeyBanc's Helios rack cut** ("<1,000 racks in 2026 vs 4,000 expected; 20,000 in 2027"): originates in an X post attributed to KeyBanc, relayed by an aggregator that itself says "none of these numbers have been checked by anyone outside the sources." Single-source, second-hand. Usable only as "supply-chain chatter reported on Oct 17," never as a KeyBanc fact.
- **Any dollar value on the Meta deal.** None was disclosed. The site's own May article's "$100B" is unsupported.
- **Standalone Instinct/AI accelerator revenue.** AMD does not disclose it. Only "more than doubled y/y" and the segment total. Do not back into a number and present it as reported.
- **A 2027 capex guide from Meta.** None was given.
- **Any Lam comment specifically about AMD or GPUs.** Lam spoke about components and clean rooms generally; the AMD read-through is the market's inference, not a Lam statement.
- **Yahoo Finance quote pages** — bot-hostile (403/empty). All price data here is from yfinance's API and cross-checked against MarketBeat's Oct 22 print ($507.93, low $502.60).
- **The 22 October figures for META's exact close** — reported as "about −7%" by Reuters; I did not pull a META close.

## 12. SUGGESTED ANGLE

The interesting thing about Oct 22 is that AMD fell 8% on a supplier's *supply* warning and a customer's *cash-flow* print, three weeks before it reports the first quarter in which Helios revenue exists. But AMD doesn't sell racks — it licenses the design and sells the silicon into them, which is why its gross margin is guided flat at 56% while the rack ramp begins. The margin test is real, but it's a mix test (HBM4-heavy accelerators vs EPYC), not a systems-integration test; the *schedule* test is the one AMD doesn't fully control, because ODM partners build the racks. That's the article: the rack ramp is a supply-chain bet dressed as a margin story.
