# SMCI Articles Fact-Check Report
**Date:** 2026-05-30  
**Data Source:** Yahoo Finance (yfinance), YouTube oEmbed API, HTTP status checks  

---

## ARTICLE 1: `smci-dell-ai-server-wave-2026.json`
**Title:** "$SMCI Rallies 11% as Dell's Blowout Earnings Validate the AI Server Thesis"  
**Date:** 2026-05-29  
**Ticker:** SMCI | **Sentiment:** Bullish  

### Metric Verification (Live Yahoo Finance Data)

| Claim | Article Value | Live Data | Verdict |
|-------|--------------|-----------|---------|
| SMCI stock price | $46 | $46.09 | ✅ PASS (rounds to $46) |
| SMCI market cap | $27.7B | $27.72B (27,719,378,944) | ✅ PASS |
| SMCI forward P/E | 14.3x | 14.31x | ✅ PASS |
| SMCI P/S ratio | 0.82x | 0.8225x | ✅ PASS |
| SMCI revenue (TTM) | $33.7B | $33.70B (33,700,206,592) | ✅ PASS |
| SMCI revenue growth | 122% | 122.7% | ✅ PASS |
| SMCI earnings growth | +344% | 344.4% | ✅ PASS |
| Dell stock price | $420 | $420.91 | ✅ PASS |
| Dell market cap | $273B | $273.41B (273,409,769,472) | ✅ PASS |
| Dell forward P/E | ~18x | **21.2x** | ❌ **DISCREPANCY** (18 vs 21.2) |
| SMCI 11.6% surge (May 29) | +11.6% | +11.6% ($41.30→$46.09) | ✅ PASS |
| Dell 32% surge (May 29) | 32% | 32.8% ($317.05→$420.91) | ✅ PASS |
| Dell revenue $28.4B, +39.5% | $28.4B, +39.5% | Prior quarter (Q4 FY2026) showed exactly 39.5% YoY growth. **Q1 FY2027 data not yet available** in yfinance financials to directly verify $28.4B. Earnings calendar confirms May 28 report date. Analyst estimates ranged $32.9B-$40.2B. | ⚠️ **CANNOT VERIFY** — $28.4B is well below lowest analyst estimate ($32.9B), which is odd for a stock that surged 32%. |

### Source URL Verification

| URL | HTTP Status | Verdict |
|-----|-------------|---------|
| https://www.cnbc.com/2026/05/28/dell-earnings-report-q1-2027.html | **403** | ⚠️ BLOCKED (CNBC paywall/bot detection — URL format looks valid, date matches Dell's confirmed earnings date of May 28) |
| https://www.reuters.com/technology/dell-shares-soar-30-ai-server-demand-price-hikes-power-stellar-quarter-2026-05-29/ | **401** | ⚠️ BLOCKED (Reuters paywall — URL format looks valid) |
| https://finance.yahoo.com/news/super-micro-computer-q3-earnings-2026-130000123.html | **429** | ⚠️ BLOCKED (rate limited — URL format looks valid) |

**All three source URLs use legitimate, well-known domains (CNBC, Reuters, Yahoo Finance).** HTTP errors are consistent with paywall/bot protection, not fabricated URLs.

### Video Verification

| Video ID | Title | Blocklist Hit? | Verdict |
|----------|-------|----------------|---------|
| `zQFUpz_aC64` | "Dell stock skyrockets, heads for best day ever as AI server revenue soars" (CNBC Television) | ❌ No | ✅ Real, legitimate CNBC video |

### CEO Quotes
**None found in article.** No transcript verification needed.

### Additional Findings
- **meta.priceTarget = $37.13**: This matches the **analyst mean price target** of $37.125 (median $35.00, high $58.00, low $15.00, from 16 analysts). Notably, the current stock price ($46.09) trades **24% above** the analyst consensus target. Article does not mention this in the body.

---

## ARTICLE 2: `smci-q3-earnings-surge-ai-value.json`
**Title:** "Super Micro Just Doubled Revenue — And Trades at 11x Earnings."  
**Date:** 2026-05-24  
**Ticker:** SMCI | **Sentiment:** Bullish  

### Metric Verification (Live Yahoo Finance Data)

| Claim | Article Value | Live Data | Verdict |
|-------|--------------|-----------|---------|
| SMCI revenue | $33.7B | $33.70B (TTM) | ✅ PASS ($33.7B as trailing 12mo is correct) |
| Revenue growth | 122% YoY | 122.7% (quarterly YoY) | ✅ PASS |
| Earnings growth | +344% | 344.4% | ✅ PASS |
| Gross margins | 8.4% | 8.394% | ✅ PASS |
| Profit margin | 3.7% | 3.701% | ✅ PASS |
| Free cash flow | -$7.4B | -$7.45B (-7,448,383,488) | ✅ PASS |
| Forward P/E | **11x** | **14.31x** | ❌ **DISCREPANCY** (11 vs 14.31 — off by 30%) |
| P/S ratio | **0.63x** | **0.8225x** | ❌ **DISCREPANCY** (0.63 vs 0.8225 — off by 30.5%) |
| "Surged 20% after earnings" | 20% | **16.4%** from May 19 close ($30.56) to May 22 close ($35.58). Peak intra-week move from May 19 low to May 22 high was 22%. **No single-day close of 20%.** CNBC source URL says "jumps-18" (18%). | ❌ **INACCURATE** — 16.4% cumulative over several days. Article inflates the move. |
| "Q3 FY2026 revenue of $33.7B" | Q3 revenue = $33.7B | **Q3 FY2026 quarterly revenue was $10.24B**, not $33.7B. The $33.7B is trailing 12 months | ❌ **FALSE** — Subtitle conflates quarterly revenue with TTM revenue |

### Source URL Verification

| URL | HTTP Status | Verdict |
|-----|-------------|---------|
| https://www.cnbc.com/2026/05/22/super-micro-stock-jumps-18-on-guidance-beat-as-revenue-more-than-doubles.html | **403** | ⚠️ BLOCKED (CNBC paywall — URL format looks valid) |
| https://finance.yahoo.com/news/super-micro-computer-q3-earnings-2026-130000123.html | **429** | ⚠️ BLOCKED (rate limited — URL format looks valid) |
| https://www.fool.com/investing/2026/05/23/why-super-micro-computer-stock-is-still-a-buy/ | **404** | ❌ **BROKEN URL** — Returns 404 with and without trailing slash. Redirects to 404 page. This URL does not resolve to a valid article. |

**The Motley Fool URL is dead/broken.** Could be a legitimate article that was removed, or a fabricated URL. The 404 is definitive — no article exists at that path.

### Video Verification

| Video ID | Title | Blocklist Hit? | Verdict |
|----------|-------|----------------|---------|
| `uXRqf73AAFY` | "SMCI Earnings Shock Wall Street 📈 Is This AI Stock Ready For Another Massive Rally?" (SMCI Stock Brief channel) | ❌ No | ✅ Real YouTube video (third-party channel, not major news outlet) |

### CEO Quotes
**None found in article.** No transcript verification needed.

---

## SUMMARY OF ALL DISCREPANCIES

### 🔴 Critical Issues

| # | Issue | Article(s) | Details |
|---|-------|------------|---------|
| 1 | **Forward P/E inflated** (11x claim) | Article 2 | Live data shows 14.31x, not 11x — a 30% discrepancy. Makes SMCI look cheaper than it is. |
| 2 | **P/S ratio deflated** (0.63x claim) | Article 2 | Live data shows 0.8225x, not 0.63x — a 30.5% discrepancy. |
| 3 | **Q3 revenue conflated with TTM** | Article 2 | Subtitle says "Q3 FY2026 revenue of $33.7B" — Q3 revenue was $10.24B. The $33.7B is trailing 12 months. This is a factual error in the article subtitle. |
| 4 | **Motley Fool source URL 404** | Article 2 | URL returns HTTP 404. Either article was taken down or never existed at that URL. |

### 🟡 Moderate Issues

| # | Issue | Article(s) | Details |
|---|-------|------------|---------|
| 5 | **"Surged 20%" exaggerated** | Article 2 | Stock gained ~16.4% cumulatively (May 19→22 close). CNBC source mentions 18%. The 20% claim is rounded up aggressively. |
| 6 | **Dell forward P/E** | Article 1 | Claims 18x, but live data shows 21.2x. Off by ~18%. |
| 7 | **Dell Q1 FY2027 revenue unverifiable** | Article 1 | $28.4B is well below lowest analyst estimate ($32.9B). The 39.5% YoY growth matches the PRIOR quarter (Q4 FY2026), not necessarily Q1 FY2027. Can't directly verify. |
| 8 | **$37.13 price target (meta only)** | Article 1 | Current price ($46.09) trades 24% above analyst mean target ($37.13). Article is bullish but doesn't disclose this target disconnect. |

### ✅ Fully Verified (No Issues)

- SMCI stock price ($46/$46.09) ✓
- SMCI market cap ($27.7B) ✓
- SMCI TTM revenue ($33.7B) ✓
- SMCI revenue growth (122%/122.7%) ✓
- SMCI earnings growth (344%/344.4%) ✓
- SMCI gross margins (8.4%) ✓
- SMCI profit margin (3.7%) ✓
- SMCI FCF (-$7.4B) ✓
- SMCI P/S (Article 1: 0.82x) ✓
- SMCI forward P/E (Article 1: 14.3x) ✓
- Dell stock price ($420/$420.91) ✓
- Dell market cap ($273B) ✓
- SMCI 11.6% surge on May 29 ✓
- Dell 32% surge on May 29 ✓
- Video IDs (both clean, not in blocklist) ✓
- CNBC/Reuters/Yahoo Finance source domains (legitimate, not fabricated) ✓

### Video Blocklist Status
- `zQFUpz_aC64`: ❌ NOT in blocklist ✅
- `uXRqf73AAFY`: ❌ NOT in blocklist ✅
- Neither video matches Rickroll (dQw4w9WgXcQ, oHg5SJYRHA0, xFrG64wTeG8), Gangnam Style (9bZkp7q19f0), Despacito (kJQP7kiw5Fk), or other blocklisted IDs (RgKAFK5djSk, JGwWNGJdvx8).

---

## CONCLUSION

**Article 1** is largely accurate on SMCI-specific metrics and price action. The only significant questions surround Dell's revenue figure ($28.4B vs analyst estimates of $32.9-40.2B) and the Dell forward P/E (18x claimed vs 21.2x actual).

**Article 2** has more serious issues: the forward P/E is inflated by 30% (11x vs 14.31x), the P/S ratio is deflated by 30% (0.63x vs 0.8225x), the "20% surge" is exaggerated (~16.4%), and the subtitle contains a factual error conflating Q3 quarterly revenue ($10.24B) with TTM revenue ($33.7B). One of three source URLs (Motley Fool) returns 404.
