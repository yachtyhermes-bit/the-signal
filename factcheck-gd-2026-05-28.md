# Fact-Check Report: General Dynamics Monster Earnings Beat
**File:** articles/posts/gd-defense-contracts-earnings.json
**Date:** 2026-05-26
**Ticker:** GD

## Verdict: ✅ CLEAN (Minor Issues)

---

## Verification Results by Claim

### 1. Q1 2026 EPS: $4.10 vs $3.69 consensus (11% beat)
- **✅ CONFIRMED** — yfinance earnings_dates: Estimate=$3.69, Reported=$4.10, Surprise=11.02%
- Quarterly financials show Diluted EPS for 2026-03-31 = $4.10
- Matches exactly.

### 2. TTM Revenue: $53.8B, growing 10.3% YoY
- **✅ CONFIRMED** — Calculated TTM = Q2'25 ($13.041B) + Q3'25 ($12.907B) + Q4'25 ($14.379B) + Q1'26 ($13.481B) = **$53.808B ≈ $53.8B**
- Revenue growth from yfinance info: **10.3%** ✓

### 3. Net Income: $4.34B
- **✅ CONFIRMED** — netIncomeToCommon from yfinance: **$4.341B ≈ $4.34B** (TTM basis)
- Q2'25 NI=$1.014B + Q3'25 NI=$1.059B + Q4'25 NI=$1.143B + Q1'26 NI=$1.125B = **$4.341B**

### 4. Operating Cash Flow: $7.41B
- **✅ CONFIRMED (minor rounding)** — TTM OCF = Q2'25 ($1.598B) + Q3'25 ($2.109B) + Q4'25 ($1.561B) + Q1'26 ($2.155B) = **$7.423B**
- Article says $7.41B — difference of $13M (0.18%), acceptable rounding.

### 5. Free Cash Flow: $3.96B
- **⚠️ MINOR ISSUE — Time period mismatch**
- The $3.96B matches **FY2025 annual FCF** ($3.959B), NOT TTM
- TTM FCF = Q2'25 ($1.400B) + Q3'25 ($1.897B) + Q4'25 ($0.952B) + Q1'26 ($1.952B) = **$6.201B**
- Article's $3.96B is factually correct for FY2025 but presented alongside TTM metrics (revenue, net income, OCF), creating a time-period inconsistency.

### 6. Stock Price: $342.89
- **✅ CONFIRMED (as of May 22 close)** — Historical data shows GD closed at **$342.89** on May 22, 2026 (last trading day before article publication)
- Article published May 26 — stock closed at $344.64 that day. Using May 22 close is standard practice (most recent available at time of writing).
- Current live price (May 27): $342.69

### 7. Market Cap: $92.7B
- **✅ CONFIRMED** — sharesOutstanding (270,430,187) × $342.69 (current) = **$92.67B**, rounds to $92.7B
- Same calculation using article's $342.89: $92.74B ≈ $92.7B

### 8. Trailing P/E: 21.6x
- **✅ CONFIRMED** — trailingPE from yfinance: **21.55 ≈ 21.6x**
- TTM EPS sum: $15.89 → $342.89/$15.89 = 21.58x

### 9. Forward P/E: 18.9x
- **✅ CONFIRMED** — forwardPE from yfinance: **18.89 ≈ 18.9x**
- forwardEps: $18.15 → $342.69/$18.15 = 18.89x

### 10. Analyst Target: $391.55 mean, $444 high — 21 analysts, consensus Buy
- **⚠️ MINOR ISSUE — Mean target slightly off**
- Live data: **mean=$392.22** (article says $391.55 — difference of $0.67, 0.17%)
- High target: **$444.00** ✓ (exact match)
- Number of analysts: **21** ✓
- Consensus rating: **Buy** (recommendationKey="buy", recommendationMean=2.17 on 1-5 scale) ✓
- Breakdown: 4 Strong Buy, 9 Buy, 10 Hold, 1 Sell, 0 Strong Sell

### 11. Dividend: $6.09 per share (1.78% yield)
- **✅ CONFIRMED** — dividendRate=$6.09, dividendYield=1.78% ✓ (exact match)

### 12. Historical Beats (Four Consecutive)
- **✅ ALL CONFIRMED**
  - Q4 2025: **$4.17** vs $4.11 est (surprise 1.54%) ✓
  - Q3 2025: **$3.88** vs $3.71 est (surprise 4.57%) ✓
  - Q2 2025: **$3.74** vs $3.54 est (surprise 5.59%) ✓
  - Q1 2025: **$3.66** vs $3.46 est (surprise 5.72%) ✓
- Note: Including Q1 2026, the beat streak is actually **5 consecutive quarters**

### 13. Next Report: July 22, 2026 with $3.94 expected
- **✅ CONFIRMED** — earnings_dates shows **2026-07-22** with estimate of **$3.94** ✓

### 14. FY2025 Full-Year Results
- **✅ ALL CONFIRMED**
  - Revenue: **$52.55B** ✓ (from annual financials)
  - Operating Income: **$5.356B ≈ $5.36B** ✓
  - Net Income: **$4.21B** ✓
  - Diluted EPS: **$15.45** ✓

### 15. Linked Sources
- **✅ ALL RESOLVE** — HTTP 200 for all three:
  - https://www.gd.com/ ✓
  - https://investorrelations.gd.com/ ✓
  - https://finance.yahoo.com/quote/GD/ ✓

### 16. Submarine/Virginia-Class Contract Boosts
- **✅ SUPPORTED BY NEWS** — Bing News search confirms multiple relevant headlines:
  - "US Navy awards Electric Boat $2.3 billion contract for Virginia-class work"
  - "Pentagon awards $197M AUKUS contract, boosting Australia sub program"
  - "General Dynamics Contract Win And Cybersecurity Push Shape Valuation Story"

### 17. Gulfstream Delivery Ramp
- **✅ SUPPORTED BY NEWS** — Multiple analyst articles reference Gulfstream as a growth driver:
  - "General Dynamics: The Submarine Anchor And The Gulfstream Engine"
  - "General Dynamics Reports First-Quarter 2026 Financial Results"
  - "General Dynamics Is Soaring on a Beat-and-Raise Quarter"

---

## Summary of Issues

| # | Severity | Claim | Issue |
|---|----------|-------|-------|
| 1 | ⚠️ Minor | FCF $3.96B | Matches FY2025 annual ($3.959B) but article context implies TTM. Actual TTM FCF is $6.20B. Time-period mismatch. |
| 2 | ⚠️ Minor | Analyst mean target $391.55 | Live data shows $392.22 — $0.67 difference (0.17%). Likely the mean shifted slightly between writing and verification. |
| 3 | ✅ No issue | Stock price $342.89 | Accurate as of May 22 close. Article published May 26 when close was $344.64. Standard practice to use latest close. |
| 4 | ⚠️ Minor | "Four-year streak of conservatism" | Editorial claim. Data shows 3 consecutive earnings misses in 2024 (Q2-Q4), undermining the "conservatism" narrative for that period. Subjective/interpretive. |

## Verdict: ✅ CLEAN (Minor Issues)

The article is well-researched and factually accurate for a finance/analysis piece. All hard data claims (EPS, revenue, P/E, analyst targets, dividend, FY2025 results) are verified correct or within acceptable rounding. The two minor issues are:
1. Mixing TTM and annual FCF metrics
2. Analyst mean target off by $0.67
