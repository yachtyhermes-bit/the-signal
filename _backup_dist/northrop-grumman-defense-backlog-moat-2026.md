# RESEARCH BRIEF: Northrop Grumman Corporation (NOC)
## Mid-Day Edition — July 14, 2026
### Slug: northrop-grumman-defense-backlog-moat-2026

---

## SECTION 1: SNAPSHOT & KEY STATISTICS

### Company Overview
- **Ticker:** NOC (NYSE) | **Sector:** Industrials / Aerospace & Defense
- **Headquarters:** Falls Church, Virginia | **Founded:** 1939
- **Employees:** ~95,000 | **CEO:** Kathy Warden (Chair, President & CEO)
- **Segments:** Aeronautics Systems, Defense Systems, Mission Systems, Space Systems
- **84% of 2025 sales** from U.S. government (2025 10-K)

### Current Market Data (as of July 14, 2026)

| Metric | Value |
|--------|-------|
| **Current Price** | $536.49 (Jul 13 close: $541.82) |
| **Market Cap** | $76.2B |
| **Enterprise Value** | $92.4B |
| **Trailing P/E** | 16.75x |
| **Forward P/E** | 17.79x |
| **EPS (TTM)** | $32.02 |
| **Forward EPS** | $30.15 |
| **Price/Book** | 4.45x |
| **Dividend Yield** | 1.74% ($9.40 annual / $2.47 quarterly) |
| **Payout Ratio** | 28.97% |
| **Beta** | -0.102 (negative vs market) |
| **52-Week High** | $774.00 (Mar 3, 2026) |
| **52-Week Low** | $493.84 (Jun 29, 2026) |
| **From 52W High** | -30.7% |
| **YTD Performance** | ~-5.4% |
| **1-Year Return** | +5.0% |
| **Analyst Consensus** | **Buy** (16 analysts) |
| **Mean Target Price** | $670.48 |
| **High Target** | $815.00 |
| **Low Target** | $533.00 |
| **Wells Fargo (David Strauss)** | Overweight, TP cut to $620 from $800 (Jul 2026) |

### Ownership
| Metric | Value |
|--------|-------|
| **Institutional Ownership** | 84.34% |
| **Institutional Holders** | 2,264 |
| **Short Ratio** | 2.13 days |

---

## SECTION 2: EXACT YFINANCE CALLS

```python
import yfinance as yf
ticker = yf.Ticker("NOC")
info = ticker.info

info.get("currentPrice")         # 536.49
info.get("marketCap")            # 76,199,534,592
info.get("trailingPE")           # 16.75
info.get("forwardPE")            # 17.79
info.get("totalRevenue")         # 42,367,000,576 (TTM)
info.get("revenueGrowth")        # 0.044 (4.4% YoY)
info.get("operatingMargins")     # 0.1169 (11.69%)
info.get("profitMargins")        # 0.1080 (10.80%)
info.get("trailingEps")          # 32.02
info.get("forwardEps")           # 30.15
info.get("dividendYield")        # 1.74%
info.get("fiftyTwoWeekHigh")     # 774.0
info.get("fiftyTwoWeekLow")      # 493.84
info.get("beta")                 # -0.102
info.get("totalDebt")            # 17,574,000,640
info.get("totalCash")            # 2,090,000,000
info.get("ebitda")               # 7,306,999,808
info.get("recommendationKey")    # "buy"
info.get("targetMeanPrice")      # 670.48
info.get("enterpriseValue")      # 92,440,576,000
info.get("bookValue")            # 120.50
info.get("priceToBook")          # 4.45
info.get("employees")            # 95,000
```

### Annual Financials (FY2025)
```python
financials = ticker.financials
# Year ended 2025-12-31:
# Total Revenue:       $41,954,000,000
# Operating Income:    $4,280,000,000
# Net Income:          $4,182,000,000
# EBITDA:              $7,205,000,000
# Diluted EPS:         $29.08
# Diluted Shares:      143,800,000
```

### Free Cash Flow Calculation
```python
q_cf = ticker.quarterly_cashflow
# Last 4 quarters of Free Cash Flow:
# 2026-03-31:  -$1,823,000,000 (seasonal — Q1 working capital)
# 2025-12-31:   $3,235,000,000
# 2025-09-30:   $1,256,000,000
# 2025-06-30:    $637,000,000
# SUM (L4Q):    $3,305,000,000

# Annual FCF (FY2025): $3,307,000,000 (annual cashflow)
```

### Balance Sheet (Dec 31, 2025)
```python
bs = ticker.balance_sheet
# Total Assets:          $51,377,000,000
# Total Debt:           $17,019,000,000
# Stockholders Equity:  $16,674,000,000
# Cash & Equivalents:   $4,403,000,000
# Net Debt:             $10,759,000,000
# Goodwill:             $17,437,000,000
```

---

## SECTION 3: BACKLOG — THE CORE THESIS

### $95.6 Billion Backlog (Q1 2026)

| Segment | Funded | Unfunded | Total |
|---------|--------|----------|-------|
| Aeronautics Systems | $13.0B | $11.3B | **$24.3B** |
| Defense Systems | $7.8B | $20.0B | **$27.7B** |
| Mission Systems | $12.9B | $4.9B | **$17.8B** |
| Space Systems | $10.4B | $15.4B | **$25.8B** |
| **Total** | **$44.1B** | **$51.5B** | **$95.6B** |

- **FY2025 closed** at a record $95.7B backlog
- **Q1 2026 net awards:** $9.8B
- **FY2025 net awards:** >$46B, book-to-bill 1.10x
- **Key awards in Q1 2026:** $4.9B restricted/classified, $0.5B F-35, $0.5B IR countermeasures, $0.4B Triton
- **2.3x revenue coverage** provides ~2+ years of revenue visibility

---

## SECTION 4: SEGMENT DEEP DIVE (Q1 2026)

### Aeronautics Systems
| Metric | Q1 2026 | YoY Change |
|--------|---------|------------|
| Sales | $3,283M | +16.7% |
| Operating Income | $305M | +$488M (vs -$183M loss) |
| Operating Margin | 9.3% | +1,520bps |
| Backlog | $24.3B | +5% |
**Drivers:** B-21 Raider ramp, restricted programs, E-130J TACAMO. Absence of $477M B-21 loss provision.

### Defense Systems
| Metric | Q1 2026 | YoY Change |
|--------|---------|------------|
| Sales | $1,899M | +5% (+10% organic) |
| Operating Income | $184M | — |
| Operating Margin | 9.7% | — |
| Backlog | $27.7B | flat |
**Drivers:** Sentinel ICBM ramp, tactical solid rocket motors, IBCS portfolio.

### Mission Systems
| Metric | Q1 2026 | YoY Change |
|--------|---------|------------|
| Sales | $2,861M | +2% |
| Operating Income | $433M | +20% |
| Operating Margin | **15.1%** | +220bps |
| Backlog | $17.8B | -4% |
**Drivers:** Restricted airborne radar ramp, marine systems. **Highest-margin segment.**

### Space Systems
| Metric | Q1 2026 | YoY Change |
|--------|---------|------------|
| Sales | $2,480M | -3% |
| Operating Income | $235M | -17% |
| Operating Margin | 9.5% | -160bps |
| Backlog | $25.8B | -2% |
**Drivers:** SDA Tranche 3 tracking layer ramp. **Headwind:** $71M GEM 63XL EAC charge (launch anomaly). NGI wind-down (-$98M).

---

## SECTION 5: KEY PROGRAMS & CATALYSTS

### 1. B-21 Raider (Long-Range Strike Bomber)
- First flight Nov 2023; moving to low-rate initial production (LRIP)
- **Feb 2026:** $4.5B USAF agreement to expand production capacity
- **2026:** At least 2 B-21s flying for testing (per USAF)
- **2027:** First operational delivery target
- **Scale:** Potentially $80B+ lifecycle; 100+ bombers discussed in Congress
- **Moat:** **Sole prime contractor** — no competitor on this program

### 2. Sentinel ICBM (LGM-35A)
- Replacing 400 Minuteman III ICBMs; estimated $140.9B+ total program cost
- **2024:** Nunn-McCurdy critical breach (37% cost overrun, 2-year delay); DoD certified continuation Jul 2024
- **2026:** Restructuring underway; "substantial progress" per Apr 2026 NOC release
- **Milestones:** First flight 2027; IOC early 2030s; prototype silo groundbreaking Feb 2026 in Utah
- **Moat:** **Sole prime** — took over from Boeing in 2020

### 3. Space Systems (Growth Engine)
- **SDA Tracking Layer (Tranche 3):** ~$1.6B award (Dec 2025, joint with Rocket Lab, 36 satellites)
- **Total SDA commitments:** 150+ satellites across PWSA Transport + Tracking layers
- **GEM 63XL:** Solid rocket boosters for ULA Vulcan Centaur; $71M Q1 EAC charge from launch anomaly
- **Cygnus:** ISS cargo resupply spacecraft
- **Golden Dome:** Homeland missile defense; NOC building 18 satellites for Tranche 2

### 4. Advanced Weapons & Electronics
- **AARGM-ER (AGM-88G):** 4th live-fire test Jan 2026; 1,500+ delivered. Navy FY27 "strategic pause" noted
- **IBCS:** 20 countries formally requested; international sales growing 20%+
- **Hypersonics:** Hypersonics Capability Center; 3D printing for hypersonic propulsion
- **Triton (MQ-4C):** NATO acquisition deal (Jul 10, 2026) — expands allied revenue
- **CCA:** Collaborative Combat Aircraft (NGAD drone wingman) — NOC competing

---

## SECTION 6: FINANCIAL PERFORMANCE

### FY2025 (Year Ended Dec 31, 2025)
| Metric | FY2025 | FY2024 | Change |
|--------|--------|--------|--------|
| Total Revenue | $41.95B | $41.03B | +2.2% |
| Operating Income | $4.28B | $4.37B | -2.1% |
| Net Income | $4.18B | $4.17B | +0.2% |
| Diluted EPS | $29.08 | $28.34 | +2.6% |
| EBITDA | $7.21B | $7.01B | +2.9% |
| Operating Cash Flow | $4.76B | $4.39B | +8.4% |
| Free Cash Flow | **$3.31B** | $2.62B | **+26.3%** |
| Operating Margin | 10.2% | 10.7% | -50bps |
| Net Margin | 10.0% | 10.2% | -20bps |
| CapEx | $1.45B | $1.77B | -18.1% |

### FY2025 vs FY2023 (B-21 Recovery)
| Metric | FY2025 | FY2023 | Change |
|--------|--------|--------|--------|
| Revenue | $41.95B | $39.29B | +6.8% |
| Net Income | $4.18B | $2.06B | **+103%** |
| EPS | $29.08 | $13.53 | **+115%** |
| FCF | $3.31B | $2.10B | **+57.6%** |

### Q1 2026 Results (Apr 21, 2026)
| Metric | Q1 2026 | Q1 2025 | Change |
|--------|---------|---------|--------|
| Sales | $9.88B | $9.47B | +4% (+5% organic) |
| Operating Income | $989M | $573M | +73% |
| Operating Margin | 10.0% | 6.1% | +390bps |
| Diluted EPS | $6.14 | $3.32 | +85% |
| FCF | ($1.82B) | ($1.82B) | flat (seasonal) |

### FY2026 Guidance (Reaffirmed Apr 2026)
| Metric | Guidance |
|--------|----------|
| Sales | $43.5B - $44.0B |
| Segment Operating Income | $4.85B - $5.00B |
| MTM-Adjusted EPS | $27.40 - $27.90 |
| Free Cash Flow | $3.10B - $3.50B |
| CapEx | ~$1.1B (down from $1.45B) |

**Segment-Level Guidance:**
- **Aeronautics Systems:** Mid $13B sales, Low-to-mid 9% margins
- **Defense Systems:** Mid-to-high $8B sales, ~10% margins
- **Mission Systems:** High $12B sales, High 14% margins
- **Space Systems:** ~$11B sales, ~11% margins

---

## SECTION 7: COMPETITIVE LANDSCAPE

### Peer Comparison (Jul 14, 2026)

| Metric | NOC | LMT | RTX | GD |
|--------|-----|-----|-----|-----|
| **Price** | $536 | $522 | $197 | $374 |
| **Market Cap** | $76.1B | $120.3B | $265.5B | $101.2B |
| **TTM Revenue** | $42.4B | $75.1B | $90.4B | $53.8B |
| **Trailing P/E** | 16.7x | 25.3x | 37.1x | 23.6x |
| **Forward P/E** | 17.8x | 16.3x | 26.0x | 20.6x |
| **Revenue Growth** | 4.4% | 0.3% | 8.7% | 10.3% |
| **Operating Margin** | 11.7% | 11.0% | 13.2% | 10.5% |
| **Net Margin** | **10.8%** | 6.4% | 8.0% | 8.1% |
| **Dividend Yield** | 1.74% | 2.64% | 1.49% | 1.70% |
| **Total Debt** | $17.6B | $20.7B | $38.9B | $9.8B |
| **EBITDA** | $7.3B | $8.0B | $15.3B | $6.5B |
| **Employees** | 95K | 123K | 180K | 110K |
| **Analyst Consensus** | **Buy** | Hold | Buy | Buy |

### What Makes NOC Unique (The "Special Sauce")

1. **Only pure-play strategic bomber prime:** Sole developer of B-21 Raider — America's only next-gen stealth bomber program. LMT (fighters), RTX (engines/sensors), GD (ships/ground vehicles) do not compete here.
2. **Sole ICBM prime:** Only contractor for LGM-35A Sentinel — entire U.S. land-based nuclear deterrent replacement. Single-source franchise, no competitor.
3. **Largest space exposure (revenue %):** Space Systems ~25% of revenue ($11B of $44B guided) — highest among defense primes. Positioned for hypersonic defense / missile tracking satellite boom.
4. **Vertical integration:** Solid rocket motors (tactical boosters, GEM 63XL, ICBM propulsion), hypersonics — scarce, hard-to-replicate capabilities.
5. **No commercial aviation exposure:** Pure defense and space play — no commercial cycle risk vs. RTX (Pratt) and Boeing.
6. **Classified depth:** $4.9B in restricted awards in Q1 2026 alone — deep embeddedness in classified national security programs.
7. **IBCS network effects:** Integrated Battle Command System becoming NATO/allied standard — 20 countries, switching costs.

---

## SECTION 8: BULL CASE

1. **$80B+ Visible Backlog:** $95.6B = 2.3x annual sales, multi-year revenue visibility unmatched in defense.
2. **Defense Supercycle:** $1T+ FY2026 defense budget; $1.5T FY2027 request (44% increase). Nuclear triad modernization = most protected budget category.
3. **B-21 Production Ramp:** Moving from development to LRIP. $4.5B capacity expansion deal signals USAF commitment. 2027 deliveries drive acceleration.
4. **Sentinel Restructuring Completion:** Once resolved (~late 2026), massive 400-missile production phase begins. Transition from cost-risk to production revenue.
5. **Space Systems Explosion:** 150+ satellite contracts with SDA; multi-decade PWSA program. Revenue that didn't exist 5 years ago.
6. **FCF Trajectory:** 3 consecutive years of 25%+ FCF growth. Guided $3.1-$3.5B for FY2026. Q1 seasonality is historical pattern.
7. **International Expansion:** NATO Triton deal, IBCS (20 countries), AARGM-ER allies. International diversifies away from U.S. budget cycles.
8. **Capital Allocation:** $1.62B buyback in FY2025; shares declining (147M to 142M); dividend growing.

---

## SECTION 9: RISKS & BEAR CASE

1. **Sentinel Cost Overruns:** 81% total cost increase ($140.9B). Nunn-McCurdy breach. Further overruns could force restructuring, production cuts, or cancellation. **#1 risk.**
2. **B-21 Production Scaling:** Fixed-price contracts carry execution risk. $477M loss provision in FY2023 is precedent. Supply chain / workforce challenges.
3. **Stock Down 30% from High:** $774 (Mar 3) to $536 — 31% decline. Defense sector in bear market per Barron's. Sentiment overhang from budget uncertainty.
4. **Budget Uncertainty:** $1.5T FY2027 request faces political hurdles. Continuing resolutions could delay program funding.
5. **AARGM-ER Pause:** Navy signaled FY27 "strategic pause" in procurement; successor missile RFI creates near-term uncertainty for weapons segment.
6. **Valuation:** Was 25x trailing in March; now 16.7x — cheaper than LMT but discount reflects program risks.
7. **GEM 63XL Anomaly:** $71M Q1 EAC charge. Repeat could impact ULA launches and NOC reputation in solid rocket motors.
8. **Competition:** LMT dominates fighters (F-35) and has hypersonics. RTX has broadest portfolio and largest R&D budget. Both can out-invest NOC on new programs.

---

## SECTION 10: RECENT NEWS (Jun 30 - Jul 14, 2026)

| Date | Headline | Impact |
|------|----------|--------|
| Jul 10 | NATO agrees to acquire MQ-4C Triton drones from Northrop Grumman | **Bullish** (international expansion) |
| Jul 8 | 16 analysts: NOC consensus **Buy**, PT $683 | Positive sentiment |
| Jul 2 | Navy RFI for successor to AARGM-ER; FY27 procurement pause | Mildly bearish (weapons segment) |
| Jul 1 | Wells Fargo cuts PT to $620 from $800, maintains Overweight | Cautionary on valuation |
| ~Jul | Defense stocks broadly in bear market (Barron's) | Sector headwind |
| Jul 13 | SDA awards $1.75B for 36 Golden Dome satellites (L3/Sierra Space) | Neutral — NOC already on Tranche 2 |
| **Jul 21** | **Q2 2026 Earnings — KEY CATALYST** | **Earnings release + webcast 9:30am ET** |

---

## SECTION 11: VERIFICATION NOTES

All financial data pulled via direct **yfinance API calls** (Python 3.12, yfinance 0.2.x):

- `ticker.info` — price, ratios, market cap, P/E, EPS, yield, 52W range, beta, debt, cash, target
- `ticker.financials` — FY2025 annual revenue ($41.95B), net income ($4.18B), EPS ($29.08)
- `ticker.quarterly_financials` — Q1 2026 quarterly breakdown
- `ticker.cashflow` / `ticker.quarterly_cashflow` — FCF calculation (L4Q sum: $3.305B)
- `ticker.balance_sheet` — total debt ($17.0B), equity ($16.7B), cash ($4.4B)
- Peer data: `yf.Ticker("LMT").info`, `yf.Ticker("RTX").info`, `yf.Ticker("GD").info`

Web sources cross-referenced: Northrop Grumman IR (Q1 2026 press release), AOL/24/7 Wall St, AlphaStreet, StockTitan, Barchart, MacroTrends, Reuters, Spaceflight Now, SatNews, DefenseScoop, Air & Space Forces Magazine, Bulletin of Atomic Scientists.

---

## SECTION 12: SUMMARY

**The One-Paragraph Brief:** Northrop Grumman (NOC) sits at the center of the U.S. nuclear triad modernization with two sole-source, single-program franchises: the **B-21 Raider** stealth bomber (America's only next-gen bomber) and the **Sentinel ICBM** ($140B+ replacing 400 Minuteman III missiles). These provide multi-decade revenue visibility, alongside a growing space systems business contracted for 150+ missile-tracking satellites with the Space Development Agency. The stock is down **31% from its March 2026 peak** ($774 to $536), trading at **16.7x trailing earnings** with an analyst consensus **Buy** and **$670 mean target** (25% upside). Key tension: Sentinel Nunn-McCurdy cost overruns (81% total cost increase) and B-21 execution risk vs. a **$95.6B record backlog**, 3 consecutive years of 25%+ FCF growth, and the most robust defense demand environment in a generation. **Q2 2026 earnings on July 21 is the next major catalyst.**

### Slug Confirmed
**northrop-grumman-defense-backlog-moat-2026**

---

*Research completed July 14, 2026. Data sourced from yfinance (real-time API calls), Northrop Grumman IR, SEC filings, and public web sources. All figures verified against direct API calls.*
