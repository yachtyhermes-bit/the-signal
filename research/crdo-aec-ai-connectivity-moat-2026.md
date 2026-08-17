# Nelly's Research Brief — Credo Technology Group (CRDO) — Closing Bell Deep Dive
**Theme:** The "plumbing" of AI data centers — data movement as the bottleneck; AEC copper vs. optics; patent moat
**Date:** 2026-08-17 | **Sector:** Semiconductors | **Article target:** ~700–800 words

---

## LATEST QUARTER
- **Quarter:** Fiscal Q4 2026 (quarter ended **May 2, 2026**)
- **Reported:** **June 1, 2026** (after market close; FY2026 = fiscal year ended May 2, 2026)
- **Revenue:** **$437.0M** — +7.4% QoQ, **+157.0% YoY** (record; Q4 alone exceeded Credo's entire FY2025 revenue of $436.8M)
- **Margins:** GAAP GM 68.2% / non-GAAP GM 68.3%; FY26 full-year GM 68.1% (+310bps YoY)
- **Profit:** GAAP net income $169.1M ($0.88 diluted); non-GAAP net income $226.7M ($1.16 diluted)
- **Balance sheet:** ended FY26 with ~$1.4B cash + short-term investments; total debt ~$25M
- **FY2026 full year:** revenue **$1,335.1M, +206% YoY** (vs $436.8M in FY25); non-GAAP net income **$661.5M** (~5x); non-GAAP EPS $3.46
- **Guidance (Q1 FY27, quarter ending Aug 1, 2026):** revenue **$465M–$475M**; non-GAAP GM 67–69%; non-GAAP opex $86–90M
- **FY27 outlook:** management guided **>80% revenue growth** for FY27 (per Q4 call coverage); Street FY27 consensus ≈ $2.15B (+~61%) — note the spread; growth decelerates sharply in % terms vs +206%, but absolute dollar growth stays large
- **Status check:** Q1 FY27 (ended Aug 1, 2026) has NOT been reported as of Aug 17, 2026 (call scheduled early Sept 2026). Q4 FY26 is the latest reported quarter.
- **⚠️ Correction to parent's brief:** the "$268M / +272% YoY" figure is **Q2 FY26** (quarter ended Nov 1, 2025, reported Dec 1, 2025), NOT Q3. Q3 FY26 was $407.0M (+201.5% YoY), reported Mar 2, 2026.

## FUNDAMENTALS SNAPSHOT (yfinance, 2026-08-17)
- **TTM revenue:** $1,335.1M (sum of Q1–Q4 FY26 = 223.1 + 268.0 + 407.0 + 437.0; equals FY26 total — verified vs annual income statement and press release)
- **Cash + short-term investments:** ~$1.4B ($1,443M per yfinance totalCash; $1.4B per FY26 press release)
- **Total debt:** $25.4M (essentially net cash ~$1.4B)
- **Shares outstanding:** ~186.5M
- **Market cap:** ~$48.5B
- **Forward P/E:** ~28.6x | Trailing P/E: ~103x | Price/Sales (TTM): ~36x
- **52-week low / high:** $86.49 / $308.67 (currently well off the high; beta ~3.2)
- **Analyst consensus:** **Strong Buy** — 19 analysts: 4 Strong Buy / 14 Buy / 1 Hold / 0 Sell
- **Target mean:** $279.29 (median $290; range $184–$350); recent raises: BofA $340 (Jun), Barclays $300 (Jul), Susquehanna $250 (Jul)
- **Current price:** $259.90 (yfinance 2026-08-17 — stats card only; use relative language in prose)

## MOAT / COMPETITIVE DYNAMICS
**AEC patent moat (the core data point) — timeline:**
- **Mar 13, 2025:** Credo filed ITC + district-court infringement complaints vs **Amphenol, Molex, TE Connectivity, Volex** over its foundational AEC patents (engineering dating to 2017; asserted patents incl. US 10,877,233)
- **Aug 14, 2025:** settlement + license with **Amphenol** (confidential terms)
- **Nov 24, 2025:** **Siemon** license (AEC patents; joint statement; terms confidential) — stock +~13% next day
- **Jan 2026:** license + mutual covenant with **3M** (AEC patents; terms confidential)
- **Mar 26, 2026:** cross-license + settlement with **Molex**; **TE Connectivity** settlement also announced (~Mar 2026); **Volex** likewise settled — all four original defendants now licensees
- **Read:** the entire cable-manufacturing supply chain chose to license rather than litigate — a Qualcomm-style IP validation. Caveat: settlements were cross-licenses (mutual), and terms are confidential, so royalty economics are unproven; may be mutual disarmament as much as toll-booth.

**Competitor set:** Broadcom (AVGO — switching silicon, optical DSPs, CPO, custom ASICs), Marvell (MRVL — PAM4 optical DSPs, retimers, custom silicon), Astera Labs (ALAB — most direct niche rival: AECs/Taurus SCM, PCIe/CXL retimers), plus Spectra7, Montage, Point2, Kandou in AECs; transceiver makers (Coherent, Innolight, Eoptolink) in optics. Nvidia (via Mellanox) shapes the networking stack it controls. Now that Amphenol/Molex/TE/Volex/Siemon/3M license instead of compete, the direct AEC rival set is effectively ALAB + smaller players.

**Bull case (copper/AECs win in-rack):**
- GPU clusters are link-dense; for short in-rack/back-end reaches (~≤2m), AECs beat optics on **cost (~50% less), power (~half), latency, reliability** (no lasers to fail); Credo's ZeroFlap tech attacks link-flap, the #1 GPU-underutilization cause
- AEC TAM scales with GPU count, not just switch ports; 1.6T transition extends copper economics; hyperscaler scale-up architectures (NVL72-style) favor short copper
- Foundational patents → every cable giant licensed within ~12 months; new TAM expansions: ZeroFlap optics, OmniConnect (memory), ALCs, PCIe Gen6 retimers
- **Credo now plays BOTH sides of the copper-vs-optics debate:** optical DSPs, ZeroFlap optical transceivers, and silicon photonics via the **DustPhotonics acquisition ($750M cash + ~0.92M sh; closed May 28, 2026; SiPho PICs to 1.6T/3.2T, NPO/CPO; >$500M optical revenue projected FY27)** — the bear's displacement scenario is partly Credo's own growth story

**Bear case (optics displace; growth decelerates):**
- Physics: copper reach shrinks as lane rates climb (112G/lane at 1.6T); linear-drive pluggables, NPO and CPO silicon photonics erode the AEC zone over time — and Credo's own $500M+ FY27 optics target concedes the direction of travel
- **Growth deceleration:** +206% (FY26) → >80% guided (FY27) → Street ~+61%; "mid-single-digit sequential" cadence into FY27; Q1 guide ($465–475M) was only "inline" and the stock sold off post-Q4 despite record results
- **Customer concentration:** FY26 10-K — top customer **49%**, second **32%** (81% combined); top-10 ≈ 90%; Q4 largest customer 34%. Two-customer dependence is the single biggest structural risk
- Valuation: P/S ~36x TTM, trailing P/E ~100x+, forward ~29x — prices in flawless execution; beta ~3.2
- Competition: ALAB in AECs/retimers, AVGO/MRVL in DSPs; TSMC-only foundry dependency; insider selling flagged (~$220M+ over the period per earlier research note)

## THESIS + BOTTOM LINE (for the Writer — relative language only)
The structural thesis holds: as GPUs get faster, moving data becomes the bottleneck, and Credo is the purest publicly traded bet on AI-cluster interconnect — the "nervous system of the AI buildout." The copper-vs-optics framing is a false binary: the real story is that Credo has become a vertically integrated connectivity franchise spanning copper AECs, optical DSPs, transceivers and silicon photonics, and its patent moat just forced every major cable manufacturer (Amphenol, Molex, TE, Volex, Siemon, 3M) to license rather than fight — inside roughly 12 months. The honest caveats: growth is decelerating from +206% to a guided >80% (still elite), two customers drive ~80% of revenue, and the multiple is demanding. **Bottom line: constructive — the moat is real and the optics-displacement bear case is largely already hedged by Credo's own optical roadmap; but this is a high-beta execution story, so frame it as "the plumbing company of the AI buildout, priced for near-perfect execution."** Own it for the structural thesis, size for volatility, watch customer concentration and FY27 optics ramp as the tell signals.

## REFERENCE LINKS
- Credo IR — Q4 & FY2026 results (Jun 1, 2026): https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Fourth-Quarter-and-Fiscal-Year-2026-Financial-Results/default.aspx
- Credo IR — Q3 FY2026 results (Mar 2, 2026): https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Credo IR — Q2 FY2026 results, $268M +272% YoY (Dec 1, 2025): https://investors.credosemi.com/news-events/news/news-details/2025/Credo-Technology-Group-Holding-Ltd-Reports-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Credo IR — Siemon AEC patent license (Nov 24, 2025): https://investors.credosemi.com/news-events/news/news-details/2025/Credo-Licenses-Its-Active-Electrical-Cable-Patents-To-The-Siemon-Company/default.aspx
- Credo IR — 3M patent license (Jan 2026): https://investors.credosemi.com/news-events/news/news-details/2026/Credo-and-3M-Enter-Into-Patent-License-Agreement/default.aspx
- Credo IR — Amphenol settlement (Aug 14, 2025): https://investors.credosemi.com/news-events/news/news-details/2025/Credo-and-Amphenol-Reach-Settlement-in-Active-Electrical-Cable-Patent-Infringement-Disputes/default.aspx
- Credo IR — Molex settlement (Mar 26, 2026): https://investors.credosemi.com/news-events/news/news-details/2026/Credo-and-Molex-Reach-Settlement-in-Active-Electrical-Cable-Patent-Infringement-Disputes/default.aspx
- Credo IR — DustPhotonics acquisition completed (May 28, 2026): https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Completes-Acquisition-of-DustPhotonics/default.aspx
- SEC EDGAR — FY2026 10-K (customer concentration 49%/32%, top-10 ~90%): https://www.sec.gov/Archives/edgar/data/1807794/000162828026043303/crdo-20260502.htm
- Nasdaq — ITC complaint vs Amphenol/Molex/TE/Volex (Mar 13, 2025): https://www.nasdaq.com/press-release/credo-files-aec-patent-infringement-complaint-against-amphenol-molex-te-connectivity
- Lightwave — DustPhotonics deal details ($750M, >$500M FY27 optical revenue): https://www.lightwaveonline.com/home/article/55370917/credos-dustphotonics-acquisition-solidifies-its-ai-interconnect-position
- MarketBeat — Q4 FY26 earnings report/transcript (guidance, customer concentration 34%/27%/16%/10%): https://www.marketbeat.com/earnings/reports/2026-6-1-credo-technology-group-holding-ltd-stock

## NOTES / CAVEATS FOR THE WRITER
- Do NOT use exact share prices in prose — relative language only ("near its 52-week high," "roughly triple its 52-week low," "down double digits from its June record"). Stats card can use: price $259.90, 52w range $86.49–$308.67, mkt cap ~$48.5B, fwd P/E ~29x.
- The old `nelly_crdo_research.md` in repo root has stale June-era valuation figures (mkt cap ~$39.7B, fwd P/E ~23x) — superseded by this brief.
- "~88% AEC market share per 650 Group" appears in the old note but was NOT re-verified; flag or drop unless verified.
- Q4 FY26 quarterly revenue beat the pre-announced range and Q1 FY27 guidance was in-line → post-earnings sell-off from ~$308 high to ~$260 (relative framing only).
