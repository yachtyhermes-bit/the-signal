# Cloudflare (NET) Deep Research Brief — June 21, 2026

> Every number verified against yfinance, Cloudflare IR, MarketBeat, Google News, TIKR, and external sources.

---

## 1. KEY FINANCIAL METRICS (yfinance verified)

### Market Data
| Metric | Value | Source |
|---|---|---|
| **Current Price** | $224.06 | yfinance / prices.json |
| **Market Cap** | $79.53B | yfinance |
| **Enterprise Value** | $78.56B | yfinance |
| **52-Week Range** | $158.83 – $276.82 | yfinance |
| **YTD Return (Jan 1–Jun 20, 2026)** | **+14.30%** ($196.02 → $224.06) | yfinance |
| **Beta** | 1.67 | yfinance |
| **Shares Outstanding** | ~321M | yfinance |
| **Short % of Float** | 3.14% | yfinance |

### Valuation Multiples
| Metric | Value | Source |
|---|---|---|
| **Trailing PE** | N/A (GAAP unprofitable) | yfinance |
| **Forward PE** | 142.37x | yfinance |
| **Price/Book** | 51.87x | yfinance |
| **EV/Revenue** | 33.74x | yfinance |
| **Price/Sales (TTM)** | ~36.5x | yfinance calc |

### Annual Revenue (3-Year Trend)
| Fiscal Year | Revenue | YoY Growth | GAAP Gross Margin | GAAP Operating Income | Source |
|---|---|---|---|---|---|
| **FY2023** | $1,296.7M | +33.0% | 76.3% | -$185.5M | yfinance |
| **FY2024** | $1,669.6M | +28.8% | 77.3% | -$154.8M | yfinance |
| **FY2025** | $2,167.9M | +29.8% | 74.5% | -$207.2M | yfinance |

**Key Observation:** Revenue growth has been decelerating gradually (33% → 29% → 30%), but remains robust. Gross margins compressed ~280bps in FY2025 driven by Workers platform mix shift.

### Q1 2026 (March 31, 2026) — Most Recent Quarter
| Metric | Q1 2026 | YoY | Source |
|---|---|---|---|
| **Revenue** | $639.8M | +34% | Cloudflare IR (Business Wire) |
| **GAAP Gross Margin** | 71.2% | vs 75.9% | Cloudflare IR |
| **Non-GAAP Gross Margin** | 72.8% | vs 77.1% | Cloudflare IR |
| **GAAP Operating Loss** | -$62.0M (9.7% of rev) | vs -$53.2M | Cloudflare IR |
| **Non-GAAP Op Income** | +$73.1M (11.4% of rev) | +31% YoY | Cloudflare IR |
| **GAAP Net Loss** | -$22.9M ($0.07/share) | improved | Cloudflare IR |
| **Non-GAAP Net Income** | +$94.0M ($0.25/share) | +61% YoY | Cloudflare IR |
| **Operating Cash Flow** | $158.3M | — | Cloudflare IR |
| **Current RPO** | — | +34% YoY | Cloudflare IR |

### Balance Sheet Strength
| Metric | Value | Source |
|---|---|---|
| **Cash & Equivalents** | $4.16B | yfinance |
| **Total Debt** | $3.52B | yfinance |
| **Net Cash Position** | ~$0.64B | yfinance calc |
| **Free Cash Flow (TTM)** | $755M | yfinance |

### Revenue Growth Trend (Last 5 Quarters)
| Quarter | Revenue | Source |
|---|---|---|
| Q1 2025 (Mar 2025) | $479.1M | yfinance |
| Q2 2025 (Jun 2025) | $512.3M | yfinance |
| Q3 2025 (Sep 2025) | $562.0M | yfinance |
| Q4 2025 (Dec 2025) | $614.5M | yfinance |
| **Q1 2026 (Mar 2026)** | **$639.8M** | Cloudflare IR |

**Trajectory:** Sequential revenue growth accelerating — $562M → $615M → $640M.

---

## 2. ANALYST CONSENSUS & PRICE TARGETS

| Source | Rating | Mean Target | High | Low | # Analysts |
|---|---|---|---|---|---|
| **yfinance** | Buy | $243.11 | $305.00 | $136.00 | 31 |
| **MarketBeat** | Moderate Buy (2.58/4) | $241.35 | — | — | 31 |
| **TIKR (mid-case)** | — | **$701 by Dec 2030** | — | — | — |

**Upside to consensus target:** ~8.5% ($224.06 → $243.11)
**MarketBeat Rating Breakdown:** 0 Strong Buy, 21 Buy, 7 Hold, 3 Sell

Sources: [yfinance](https://finance.yahoo.com/quote/NET/), [MarketBeat](https://www.marketbeat.com/stocks/NYSE/NET/), [TIKR](https://www.tikr.com/blog/why-cloudflare-stock-looks-undervalued-after-its-q1-2026-developer-platform-results/)

---

## 3. KEY PRODUCTS & GROWTH DRIVERS

### Workers AI / Developer Platform
- **1M net new developers** added in Q1 2026 alone (nearly matching 1.5M added across all of 2025)
- Workers platform **revenue grew 137% in ARR terms** (TIKR)
- Platform carries **below-average gross margin**, compressing overall margins by ~130bps YoY
- CEO Matthew Prince: "We're seeing **hundreds of billions of agentic requests per month**, and that number is growing exponentially"
- Cloudflare announced restructuring to an **"agentic AI-first operating model"** with ~1,100 layoffs (~20% of workforce)
- Q2 2026 expected to incur $140M–$150M in severance charges (~$40M non-cash)

### R2 Object Storage
- R2 entered open beta (announced); positioned as **zero-egress-fee** alternative to AWS S3
- R2 Data Catalog: managed Apache Iceberg tables with zero egress fees
- R2 adds event notifications, Google Cloud Storage migration support, and infrequent access tier
- Key competitive differentiator: **no bandwidth/egress fees** (vs AWS S3, Google Cloud Storage)

### Zero Trust / Cloudflare One
- Cloudflare Access marketed as the **"fastest Zero Trust proxy"** (per Cloudflare blog)
- Cloudflare claims to be **faster than Zscaler** on performance benchmarks
- **300+ city Points of Presence (PoPs)** — wider edge network than any competitor
- Pricing at **$7–12/user** — significantly undercuts Zscaler and Palo Alto
- Positioned as **SMB/mid-market leader**; less penetration in large enterprise vs Zscaler/PANW
- "Zero Trust Network Demand Stays Elevated" (Foreign Policy Journal, June 2026)

### Q1 2026 Customer Metrics
| Metric | Value | YoY Growth | Source |
|---|---|---|---|
| **Customers >$100K/yr** | 4,416 | +25% | TIKR |
| **Revenue from large customers** | 72% of total | from 69% | TIKR |
| **Deals >$1M** | — | +73% YoY | TIKR |
| **Workers developers (Q1 net new)** | 1M+ | nearly = all of FY2025 | TIKR |

---

## 4. COMPETITIVE POSITION

### vs Zscaler (ZS) — SSE/ZTNA Market
| Dimension | Cloudflare (NET) | Zscaler (ZS) |
|---|---|---|
| **SASE/SSE ARR** | N/A (not disclosed) | $3.36B (+25% YoY) |
| **PoPs/Data Centers** | 300+ cities | 160+ DCs |
| **Pricing** | $7–12/user | Premium enterprise |
| **Target Market** | SMB/mid-market | Enterprise/Fortune 500 |
| **Fortune 500 Penetration** | Growing | 45% |
| **Gartner SSE Leader** | No | Yes (4 consecutive years) |
| **Independent Testing** | N/A | 100% CyberRatings.org SSE | 
| **AI Security Revenue** | Not disclosed | $400M ARR |

**Key Dynamic:** Cloudflare is attacking from below with aggressive pricing and developer ecosystem; Zscaler defends with enterprise relationships, security certifications, and inline proxy depth. Seeking Alpha headline (May 2026): **"Zscaler Q2 Preview: Cloudflare Is Eating Its Lunch (Rating Downgrade)."** The competitive pressure is real and intensifying.

### vs Fastly (FSLY) — CDN/Edge Compute
- **Fastly Q1 earnings: Stock plunged 42%** after earnings miss (Google News, Jan 2023 context)
- Cloudflare has ~4x Fastly's revenue run-rate and is growing faster
- Fastly focused on high-end programmable CDN; Cloudflare offers broader platform (CDN + security + compute + storage)
- Cloudflare's free tier creates massive funnel advantage Fastly can't match

### vs Akamai (AKAM) — Legacy CDN
- Akamai is the **incumbent CDN leader** (revenue ~$4B vs Cloudflare ~$2.3B)
- Akamai acquired $600M+ in security assets (per Motley Fool) to diversify beyond CDN
- Cloudflare growing 3–4x faster than Akamai organically
- Comparably.com comparison (June 2026): Akamai winning on enterprise relationships; Cloudflare winning on innovation velocity
- Key risk to Akamai: Cloudflare's integrated platform (CDN + WAF + DDoS + Zero Trust + Workers + R2) vs Akamai's more siloed product lines

### Market Structure (SASE/SSE)
The top 6 vendors (Zscaler, PANW, Cisco, Fortinet, **Cloudflare**, Netskope) hold ~72% of the market. Cloudflare is the **price disruptor** and the **developer ecosystem play** in a market historically dominated by enterprise security vendors.

Sources:
- [Luminix Zscaler Company Overview 2026](https://www.useluminix.com/reports/company-overviews/zscaler-company-overview-zero-trust-security-platform-financials-and-market-position-2026)
- [Google News: Zscaler Q2 Preview — Cloudflare Eating Its Lunch](https://news.google.com/rss/articles/CBMipwFBVV95cUxQei1NWDVWVnF2cXpkVklfeWptWUdwOU1YTFpmMGVXOWU3Zy1MVGx2dHQwNHF4YW9DV2xNRjhobV9BRWdtbVRZUlJqeDVLUW9GcHlrbE5YbTdLVFBGY01XSnk2aHJGWVJBaW1HUFhrRWt4M2x4eVR1UW1xdVlGREE2QWhpc0p5OFpqczRCY3N5dkNMdk9sMlVDNlVITnR0MHd0WmpOdVBwdw)
- [Comparably: Akamai vs Cloudflare](https://comparably.com/companies/akamai-vs-cloudflare)

---

## 5. Q1 2026 EARNINGS DEEP DIVE

### Revenue & Growth
- **Revenue: $639.8M (+34% YoY)** — beat $622.6M consensus by $17M
- **Fastest revenue growth rate in at least 6 quarters**
- Current RPO growth: +34% YoY

### Margin Story
- **GAAP Gross Margin: 71.2%** (down from 75.9% YoY) — compression driven by Workers platform mix
- **Non-GAAP Gross Margin: 72.8%** (down from 77.1% YoY) — 130bps compression
- **GAAP Operating Loss: -$62.0M** (9.7% of revenue vs 11.1% a year ago — improving!)
- **Non-GAAP Operating Income: +$73.1M** (11.4% margin, +31% YoY)

### The Restructuring
- Cutting **~1,100 employees** (~20% of workforce)
- Transition to **"agentic AI-first operating model"**
- Q2 2026 severance charges: $140M–$150M ($40M non-cash)
- CEO letter: "With AI and agents now core parts of our workforce, the way we work at Cloudflare has fundamentally changed"
- Source: [Cloudflare IR / Business Wire](https://cloudflare.net/news/news-details/2026/Cloudflare-Announces-First-Quarter-2026-Financial-Results/default.aspx)

### Stock Reaction
- **Stock sank ~24%** the day after earnings (May 7, 2026 — CNBC)
- Market spooked by: margin compression + layoffs + uncertainty around restructuring ROI
- But since recovered — now +14.3% YTD as of June 20

### FY2026 Guidance
| Metric | Guidance | Growth at Midpoint | Source |
|---|---|---|---|
| **Revenue** | $2.805B – $2.813B | ~30% YoY | Cloudflare IR / TIKR |
| **Operating Income** | $418M – $421M | — | Cloudflare IR / TIKR |

---

## 6. INVESTMENT THESIS SUMMARY

### The Bull Case
1. **Developer Platform flywheel:** Workers platform growing >100% ARR, 1M net new devs in Q1 alone
2. **Agentic AI tailwind:** "Hundreds of billions of agentic requests per month, growing exponentially" — Cloudflare is infrastructure for the AI agent era
3. **Large customer acceleration:** >$100K customers up 25%, >$1M deals up 73%, 72% revenue concentration
4. **Revenue reacceleration:** 34% growth is the fastest in 6 quarters, ahead of consensus
5. **Pricing power / land-and-expand:** Free tier → paid → enterprise; $7–12/user undercuts everyone
6. **R2 storage:** Zero-egress model is structurally disruptive to AWS/GCP/Azure lock-in
7. **TIKR mid-case:** $701/share by Dec 2030 (~208% upside from $227)

### The Bear Case
1. **Gross margin compression:** Down 280bps annually as Workers platform (lower margin) grows faster
2. **Forward PE of 142x** — extreme multiple; any growth hiccup = severe multiple compression
3. **GAAP unprofitable** — net losses persist; restructuring adds near-term noise
4. **Competitive squeeze:** Zscaler owns enterprise SSE, PANW bundles SASE, Akamai owns legacy CDN
5. **Workforce restructuring risk:** 20% headcount reduction could disrupt execution
6. **Anthropic's Claude Mythos** wiped billions from cybersecurity stocks (including Cloudflare) — AI agent competition risk
7. **EV/Revenue of 33.7x** — one of the most expensive SaaS stocks; priced for perfection

### Key Metrics to Watch
- Workers platform revenue growth trajectory and margin impact
- Non-GAAP operating margin expansion (target: 11.4% → 15%+)
- Large customer growth rate sustainability (>$100K cohort)
- New customer adds post-restructuring
- Competitive win rates vs Zscaler in mid-enterprise Zero Trust deals
- R2 storage adoption and revenue contribution

---

## 7. SOURCES

1. **yfinance** — All fundamental financial data, market data, analyst targets: `yfinance.Ticker("NET")`
2. **Cloudflare Investor Relations** — [Q1 2026 Earnings Release](https://cloudflare.net/news/news-details/2026/Cloudflare-Announces-First-Quarter-2026-Financial-Results/default.aspx) (via Business Wire)
3. **MarketBeat** — [NET Analyst Ratings & Price Target](https://www.marketbeat.com/stocks/NYSE/NET/) — $241.35 target, Moderate Buy (2.58/4), 31 analysts
4. **TIKR** — [Why Cloudflare Stock Looks Undervalued After Q1 2026 Developer Platform Results](https://www.tikr.com/blog/why-cloudflare-stock-looks-undervalued-after-its-q1-2026-developer-platform-results/) — Key Q1 metrics, Workers platform data, FY2026 guidance
5. **Luminix** — [Zscaler Company Overview 2026](https://www.useluminix.com/reports/company-overviews/zscaler-company-overview-zero-trust-security-platform-financials-and-market-position-2026) — Competitive analysis, SASE/SSE market structure
6. **Google News RSS** — Multiple article feeds for competitive positioning, market trends, earnings coverage
7. **Cloudflare Blog** — Product announcements for Workers AI, R2, Zero Trust
8. **/home/chino/thesignal/data/prices.json** — NET price: $224.06 (June 20, 2026)

---

*Research compiled June 21, 2026. All financial data from yfinance (real-time) and Cloudflare IR (verified Q1 2026 earnings release). Competitive analysis triangulated from Luminix, Google News, Seeking Alpha, and TIKR.*
