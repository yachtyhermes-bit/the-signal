# NBIS (Nebius Group) — Deep Research Brief
**Date:** July 29, 2026 | **Purpose:** Thematic analysis on competitive moat in GPU-as-a-service + European sovereign AI

---

## 1. COMPANY OVERVIEW

Nebius Group N.V. (NASDAQ: NBIS) is a full-stack AI cloud infrastructure company — a "neocloud" — spun off from Yandex's international assets in July 2024. HQ in Schiphol, Netherlands. CEO Arkady Volozh (Yandex founder). Traded under Yandex ticker YNDX until Feb 2022; resumed trading Oct 2024 at ~$18.94 under NBIS. Added to Nasdaq-100 in June 2026. Core businesses: Nebius AI cloud (98% of rev), TripleTen (edtech), Avride (autonomous driving). The AI cloud segment provides GPU clusters, cloud platform, inference services (Token Factory), agentic AI tools (Aether), and developer tooling across Europe and North America.

---

## 2. FINANCIAL DATA (yfinance / SEC filings, as of late July 2026)

### Revenue Growth Trajectory
| Period | Revenue | YoY Growth | Notes |
|--------|---------|------------|-------|
| FY2022 | $13.5M | — | Pre-spin-off, minimal AI cloud |
| FY2023 | $9.8M | -27% | Restructuring year |
| FY2024 | $91.5M | +834% | First full year as Nebius |
| FY2025 | $529.8M | +479% | Meta/Microsoft deals begin ramping |
| Q1 2026 | $399.0M | +684% | AI cloud rev $389.7M (+841% YoY) |
| FY2026 guidance | $3.0–3.4B | +466–542% | Management target |
| ARR target YE2026 | $7–9B | — | Implies Q4 run-rate ~$7-9B annualized |

Wall Street consensus: $8.3B FY2026 revenue expected; 206% growth projected for FY2027.

### Margins
- **Gross margin (Q1 2026):** ~74% (cost of revenue fell to 26% of rev from 49% a year earlier)
- **Adj. EBITDA margin, Group (Q1 2026):** 32% ($129.5M)
- **Adj. EBITDA margin, AI Cloud (Q1 2026):** 45% ($174.0M) — nearly doubled QoQ
- **GAAP operating margin (TTM):** -32% (still loss-making on operations)
- **GAAP net income (Q1 2026):** $621.2M (driven by ~$781M non-cash gain on ClickHouse equity stake)
- **ROE:** 14.1% | **ROA:** -3.0%

### Cash & Balance Sheet
- **Cash & equivalents (Q1 2026):** $9.3B
- **Total debt (Q1 2026):** $9.5B (of which $8.4B long-term)
- **Net debt:** ~$200M (essentially levered-neutral)
- **Shareholders' equity:** $7.2B
- **Debt/Equity:** 132% (rapidly levering to fund buildout)
- **Current ratio:** 8.3x | **Quick ratio:** 8.1x
- **Book value per share:** $28.27 | **Price/Book:** 6.0x

### Cash Flow & Capex
- **Operating CF (Q1 2026):** +$2.26B (driven by hyperscaler prepayments)
- **Capex (Q1 2026):** $2.5B
- **Free Cash Flow (Q1 2026):** -$215M (FCF deeply negative at annual scale)
- **FY2025 total capex:** $4.1B
- **FY2026 capex guidance:** $20–25B
- **Funding path:** ~70% of 2026 capex covered by Meta/Microsoft prepayments + Nvidia $2B investment

### Valuation
- **Market cap:** ~$43.1B (info data) / ~$47.7B (Yahoo as of 7/27)
- **Enterprise value:** ~$43.7B–47.9B
- **Trailing P/E:** 65.5x | **Forward P/E:** negative (earnings not expected near-term)
- **Price/Sales (TTM):** ~57x (based on trailing); forward P/S ~5-6x on FY2026 guide
- **PEG ratio:** 0.63
- **Stock price:** ~$170 (data pull); 52-week range: ~$33–$299
- **Analyst consensus:** 15 analysts — Strong Buy; mean price target $258 (implies ~52% upside)
- **Stock YTD return (as of late July):** ~345%+

---

## 3. GPU FLEET & INFRASTRUCTURE SCALE

### Power Capacity
- **Contracted power:** >3.5 GW (Q1 2026); raised target to >4 GW by YE2026
- **Target:** 5 GW by end of 2030 (per Nvidia partnership announcement)
- **Active online capacity:** ~100 MW (Sep 2025); 220 MW connected power
- **Key owned sites in buildout:** Finland (310 MW expansion — one of Europe's largest dedicated AI factories), Pennsylvania (1.2 GW AI factory), UK (65 MW across 3 deployments, £1.7B investment)
- **Other sites:** Israel, Iceland, France, Spain, New Jersey, Missouri, Oklahoma, Alabama, Minnesota, Kansas City — 7 sites with >100 MW each

### GPU Deployments
- Primarily NVIDIA H100/H200 deployed; transitioning to Blackwell (B300/GB300) and Blackwell Ultra
- First UK deployment of NVIDIA Blackwell Ultra (Nov 2025)
- Designs own server racks in-house (OEM capability) — cuts out Dell/HPE/Supermicro middlemen
- Nvidia Exemplar Cloud status on GB300/Blackwell NVL72
- $2.6B Bloom Energy fuel cell deal for behind-the-meter power — mitigating grid bottlenecks

### Backlog & Key Contracts
- **Total contracted backlog:** ~$50B
- **Meta:** Up to $27B over 5 years ($12B base + $15B optional capacity); begins early 2027
- **Microsoft:** ~$17.4–19.4B through 2031 (multi-tranche GPU services)
- **Nvidia:** $2B investment (March 2026; ~9.3% passive stake disclosed July 2026); co-development on next-gen AI factories; early access to latest GPU architectures

---

## 4. COMPETITIVE POSITION

### vs CoreWeave (CRWV)
- CoreWeave is larger by active revenue (~$1B/quarter vs NBIS $399M); NBIS is ~1.5 years behind in capacity maturity
- NBIS advantage: higher gross margins (74% vs CoreWeave ~50-60% est.), OEM capability (builds own servers), European base
- CoreWeave advantage: closer Nvidia relationship (first on Vera Rubin NVL72), larger deployed fleet, more established enterprise sales
- Market cap: CRWV ~$33B vs NBIS ~$47B — NBIS trades at a premium reflecting higher growth expectations

### vs Lambda / Other Neoclouds
- Lambda is private, smaller scale; Crusoe focuses on low-carbon; Runpod serves SMBs. None approach NBIS's power contracts or hyperscaler deal sizes.
- Nscale (UK) announced $1.1B funding but has no track record; mainly benefits from UK sovereign AI hype.

### vs Hyperscalers (AWS/Azure/GCP)
- **NBIS structural advantages:** No ecosystem lock-in — provides pure compute without forcing customers into a broader cloud stack. Faster path to GPU access (no internal chip competing for allocation). European data sovereignty (GDPR-compliant, on-continent infrastructure). More flexible for AI-native workloads (training + inference optimized, not general-purpose cloud).
- **Hyperscaler advantages:** Immense capital, integrated AI services (Bedrock, Vertex, Azure AI), established enterprise relationships, internal ASIC/TPU development that reduces GPU dependency. Amazon's recent GPU price increase validates NBIS's pricing power but hyperscalers can also squeeze margins in a supply-normalized environment.
- **Market dynamic:** Hyperscalers cannot fully meet their own AI compute demand — hence they are NBIS's *customers* (Microsoft) as much as competitors. The market is supply-constrained, not demand-constrained.

### Moat Assessment
- **Narrow but credible moat.** Sources: (1) Privileged NVIDIA partnership + $2B equity stake aligns incentives and gives early GPU access. (2) OEM server design capability — structurally lower cost base vs peers using Dell/Supermicro. (3) Multi-GW contracted power — the real bottleneck is power, not GPUs; securing 3.5+ GW is a multi-year lead. (4) European sovereignty positioning — no other European neocloud offers full-stack AI cloud at this scale. (5) Software layer (Aether, Token Factory, Tavily) moving up the stack from commoditized bare-metal GPU rental toward sticky managed services. (6) Hyperscaler prepayment model de-risks capital structure.
- **Moat widens if:** software layer becomes deeply embedded; European governments mandate sovereign AI infrastructure; NBIS hits $7-9B ARR with 45%+ EBITDA margins.
- **Moat narrows if:** GPU supply normalizes and scarcity premium collapses; hyperscalers launch competitive neocloud products; execution slips on the multi-GW buildout.

---

## 5. EUROPEAN SOVEREIGN AI ANGLE

This is NBIS's most differentiated narrative hook. The EU's "Apply AI Strategy" and the broader EuroStack conversation highlight Europe's acute anxiety about AI dependency on US/China hyperscalers. NBIS is arguably the only European-based company that can deliver genuinely sovereign AI infrastructure — it owns the full hardware-software stack (OEM servers, cloud platform, inference tools), operates data centers on European soil (Finland, France, Netherlands, UK, Spain, Iceland), and is registered in the Netherlands under full Dutch/US regulatory oversight.

The company is *not* mentioned in the EuroStack report or EU sovereign AI white papers — possibly because: (a) it's a new name; (b) its Yandex heritage creates political awkwardness; (c) EU member-state nationalism favors local champions (OVH Cloud in France, Nscale in UK). Yet NBIS is the only one actually installing and operating AI infrastructure at scale.

Paradox: NBIS's credibility as a sovereign AI provider is *strengthened* by its competitiveness outside Europe — it won Meta and Microsoft as customers on merit, not regulatory preference. EU policymakers who want sovereignty should back the European company winning in global markets, not subsidizing local also-rans.

---

## 6. YANDEX SPIN-OFF & GEOPOLITICAL CONTEXT

- **1997:** Yandex founded as Russian search engine
- **2011:** Yandex NV IPOs on NASDAQ at $1.3B; Dutch-incorporated parent
- **Feb 2022:** Russia invades Ukraine; NASDAQ halts trading; EU sanctions Yandex founder Arkady Volozh
- **July 2024:** Yandex NV sells all Russian assets for $5.4B (largest corporate exit since invasion, at a discount); retains international businesses (AI cloud, edtech, autonomous driving, data labeling)
- **Aug 2024:** Renamed Nebius Group N.V.; ticker changes to NBIS; Volozh sanctions lifted
- **Oct 2024:** Trading resumes on NASDAQ at ~$18.94; stock gains 5.6% on day one
- **Key residual risk:** Some institutional investors and European government buyers may harbor caution about Yandex origins. Volozh's EU sanctions history and Russian ties remain a reputational shadow, though the company operates transparently under Dutch/US regulatory oversight. The tech cold war (US vs China) indirectly affects NBIS via tighter GPU export controls and supply chain constraints — a tailwind for prices but a headwind for supply assurance.

---

## 7. KEY RISKS

1. **GPU supply concentration:** Entirely dependent on NVIDIA. Any shift in allocation strategy, export controls affecting NVIDIA's ability to supply, or Blackwell/B300 production delays could stall capacity ramp. No GPU diversification strategy evident.

2. **Customer concentration risk:** Meta + Microsoft represent ~$46B of the ~$50B backlog (>90%). If either customer exercises utilization optionality downward or renegotiates, the thesis breaks. Until enterprise/diversified revenue reaches 30-35% of mix (targeted by 2028-2029), this is existential.

3. **Capital intensity & financing risk:** $20-25B FY2026 capex on ~$3B revenue is extraordinary. Relies on hyperscaler prepayments, Nvidia warrants, and debt markets remaining open. Rising interest rates increase cost of convertibles. Dilution risk from future equity raises.

4. **Execution risk:** Simultaneously building out multi-GW data centers across 10+ sites on two continents, while integrating 4 acquisitions (Tavily, Eigen, Clarifai) and scaling software layer — all with a team largely inherited from Yandex (~1,000 initial employees). Power connection timelines, construction delays, equipment availability all carry slippage risk.

5. **Hyperscaler competition:** If AWS/Azure/GCP build enough internal capacity to eliminate the neocloud supply gap, the scarcity premium NBIS enjoys could vanish. Microsoft is both customer and potential competitor — a fraught dynamic.

6. **Commoditization risk:** As GPU supply normalizes (Nvidia Blackwell/Hopper cycles mature), bare-metal GPU rental could commoditize. NBIS's moat defense is the software layer — but that software is early-stage and unproven at scale.

7. **Geopolitical/governance stigma:** Yandex origins create an overhang. Some EU governments may prefer homegrown alternatives for sovereign AI contracts, regardless of NBIS's technical superiority. Founder voting control (Volozh) concentrates decision-making — limits minority shareholder influence.

---

## 8. PROPOSED ARTICLE SLUG

`nbis-europe-sovereign-ai-moat-2026`

**Rationale:** Captures the two defining angles that differentiate this article from generic NBIS coverage — (1) the European sovereign AI positioning as a structural competitive advantage, and (2) the full-stack moat analysis (OEM, NVIDIA partnership, power contracts, software layer) that explains why NBIS is not just another GPU renter. The slug is searchable, keyword-rich, and signals the thematic depth.

**Alternative if the editor prefers shorter:**
`nbis-neocloud-moat-2026` — tighter but loses the sovereign AI hook.

**Primary recommendation:** `nbis-europe-sovereign-ai-moat-2026`

---

## 9. KEY DATA POINTS FOR ARTICLE BODY

- Revenue: $9.8M (FY23) → $91.5M (FY24) → $529.8M (FY25) → $3.0-3.4B guide (FY26) | AI cloud rev +841% YoY in Q1 2026
- Gross margin: 74% (Q1 2026, up from 51% a year earlier)
- AI cloud adj. EBITDA margin: 45% (Q1 2026)
- Backlog: ~$50B (Meta up to $27B, Microsoft $17-19B)
- Contracted power: >3.5 GW, targeting >4 GW by YE2026, 5 GW by 2030
- Cash: $9.3B | Debt: $9.5B
- Nvidia investment: $2B (9.3% stake) — disclosed July 2026
- Capex guide FY2026: $20-25B
- Market cap: ~$47B | Analysts: 15, Strong Buy, PT $258
- Stock YTD: +345% as of late July 2026
- Nasdaq-100 addition: June 2026
- Only European company designing own GPU server racks at scale
- 7 sites with >100 MW each; 10+ total locations across US and Europe
- UK investment: £1.7B for 65 MW across 3 sites
- Finland flagship: 310 MW expansion
- PA AI factory: 1.2 GW
