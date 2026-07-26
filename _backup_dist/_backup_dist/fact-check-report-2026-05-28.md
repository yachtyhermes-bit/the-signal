# Fact-Check Report — The Signal Articles
**Date:** 2026-05-28  
**Reviewer:** Hermes Agent (automated fact-check)

---

## ARTICLE 1: "Nebius Just Dropped Q1 Earnings — Europe's AI Cloud Dark Horse Is Scaling Fast"
**File:** `/home/chino/thesignal/articles/posts/nebius-q1-earnings-ai-cloud-2026.json`  
**Published:** 2026-05-26T14:00:00Z  
**Ticker:** NBIS

### 1. Key Metrics Verification

| Claim | Claimed Value | Live Source Value | Status |
|---|---|---|---|
| TTM Revenue | $878M | $877.9M (yfinance totalRevenue) | ✅ **CORRECT** |
| YoY Revenue Growth | 684% | 683.9% (yfinance revenueGrowth) / Futurum confirms 684% | ✅ **CORRECT** |
| Market Cap | $52.8B | $52.9B (yfinance) | ✅ **CORRECT** (rounding) |
| Stock Price | $208 | $208.37 (yfinance) | ✅ **CORRECT** |
| Forward P/S | 11.7x | 11.76x if using $4.5B guidance; **16.5x using actual $3.2B guidance** | ❌ **INCORRECT** (based on wrong guidance) |

### 2. Critical Claims Verification

| Claim | Verification | Status |
|---|---|---|
| **"Q1 revenue up 340%" (subtitle)** | Futurum Group article confirms Q1 revenue of $399M, **up 684% YoY** — not 340%. The body of the article itself says 684%. The subtitle 340% figure is inconsistent with all other sources. | ❌ **FALSE** (should be 684%) |
| **"Raised full-year guidance to $4.5B"** | Futurum Group article (same date, from the embedded link) states: *"Nebius reiterated FY 2026 guidance for revenue between $3.0 billion and $3.4 billion"* — guidance was **reiterated**, not raised, and the range is $3.0B–$3.4B, not $4.5B. | ❌ **FALSE** — Major error. Off by $1.1B–$1.5B |
| **"$700M investment from Accel in March"** | TechCrunch article (Dec 2, 2024, not March 2026): *"European AI infra company Nebius nabs $700M from Nvidia, Accel, others"* — The round was from **multiple investors** (Nvidia, Accel, and others), not just Accel. It closed **December 2024**, not March 2026. | ❌ **FALSE** — Wrong date (Dec 2024 ≠ March 2026), wrong investor attribution (not just Accel) |
| **"NVIDIA as both investor and hardware partner"** | NVIDIA was indeed an investor in the Dec 2024 $700M round. Futurum also mentions *"NVIDIA's $2.0 billion strategic investment"*. The investor claim is true but the timing is conflated. | ⚠️ **TECHNICALLY TRUE** but framed incorrectly with wrong timing |
| **"GPU capacity... Paris, Finland, and new Icelandic facility"** | Futurum mentions Finland, Iceland, and new US sites (Pennsylvania). Paris is plausible given Nebius's European footprint. | ✅ **LIKELY CORRECT** (geography consistent) |
| **"20,000 additional GPUs by Q3"** | No source found confirming this specific figure. Futurum discusses capacity buildout but doesn't cite 20K GPUs. | ❓ **UNVERIFIABLE** |
| **"Europe's answer to CoreWeave"** | Editorial framing — TechCrunch and Futurum both compare Nebius to CoreWeave. | ✅ **REASONABLE CLAIM** |

### 3. Link Verification

| Link | Status | Content Match |
|---|---|---|
| https://futurumgroup.com/insights/nebius-q1-fy-2026-earnings-show-ai-cloud-capacity-scaling/ | **200 ✅** | Title: "Nebius Q1 FY 2026 Earnings Show AI Cloud Capacity Scaling". Article confirms $399M Q1 revenue, 684% YoY growth, $3.0B–$3.4B guidance, NVIDIA partnership. |
| https://www.youtube.com/watch?v=1tcBegY_lJU | **200 ✅** | Video exists ("Tevis - The Best Earnings of 2026... NBIS Q1 Breakdown") |

### Article 1 — SEVERITY: CRITICAL ERRORS
- **Guidance is wrong by $1.1B–$1.5B** (wrote $4.5B, actual $3.0–$3.4B)
- **$700M "Accel" investment** is a Dec 2024 event from multiple investors, misdated and misattributed
- **Subtitle contradicts body** (340% vs 684% growth)

---

## ARTICLE 2: "Google Just Launched a $1 Billion AI Price War — Here's What It Means for $GOOGL"
**File:** `/home/chino/thesignal/articles/posts/google-ai-price-war-2026.json`  
**Published:** 2026-05-26T12:00:00Z  
**Ticker:** GOOGL

### 1. Key Metrics Verification

| Claim | Claimed Value | Live Source Value | Status |
|---|---|---|---|
| Stock Price | $388 | $388.83 (yfinance) | ✅ **CORRECT** |
| Market Cap | $4.71T | $4.71T (yfinance) | ✅ **CORRECT** |
| Revenue | $422.5B | $422.5B (yfinance totalRevenue) | ✅ **CORRECT** |
| Revenue Growth | 21.8% | 21.8% (yfinance revenueGrowth=0.218) | ✅ **CORRECT** |
| Net Income | $160.2B | $160.2B (yfinance netIncomeToCommon) | ✅ **CORRECT** |
| P/E Ratio | 29.7x | 29.68x (yfinance trailingPE) | ✅ **CORRECT** |

### 2. Critical Claims Verification

| Claim | Verification | Status |
|---|---|---|
| **"Gemini API pricing slashed up to 80%"** | Google News RSS shows multiple headlines confirming Google slashed AI model prices at I/O 2026 (e.g., TradingKey: "Facing OpenAI and Anthropic, Google Slashes AI Model Prices"). Specific 80% figure could not be independently verified from official sources (JavaScript-rendered pages). | ⚠️ **PRICE CUTS CONFIRMED** — 80% figure unverified from official source |
| **"$1 billion in cloud credits extended to startups"** | Google for Startups page shows up to **$350K per startup** in credits. The $1B total pool figure may be correct as a program-wide total, but could not be independently confirmed. | ⚠️ **PLAUSIBLE BUT UNVERIFIED** |
| **"Cloud revenue surged 35%"** | Could not independently verify this segment-level figure (yfinance doesn't break out Cloud revenue). Segment data not accessible via available APIs. | ❓ **UNVERIFIED** |
| **"$2.1 trillion balance sheet"** | yfinance shows Total Assets = **$703.9B** (Q1 2026 quarterly balance sheet) or $595.3B (FY 2025 annual). The $2.1T figure is **3x the actual value**. | ❌ **FALSE** — Actual total assets: $703.9B, not $2.1T |
| **GOOGL P/E = 29.7x** (in keyMetrics) | yfinance trailingPE = 29.68x | ✅ **CORRECT** |

### 3. Link Verification

| Link | Status | Content Match |
|---|---|---|
| https://ai.google/build | 302 → **200 ✅** | Redirects to working Google AI developer portal. No specific price cut article found on the page. |
| https://www.tikr.com | **200 ✅** | Generic financial analysis homepage (as expected — not article-specific) |

### 4. Google I/O 2026 Context (from Google News RSS)

The following credible outlets confirm a Google AI pricing event occurred at I/O 2026:
- **Yahoo Finance**: "Alphabet Bets On AI Glasses And Cheaper Gemini To Deepen Ecosystem"
- **TradingKey**: "Facing OpenAI and Anthropic, Google Slashes AI Model Prices, but the Market Isn't Buying It"
- **VentureBeat**: "Google unveils Gemini Omni 'any-to-any' AI model"
- **Google Official**: "100 things we announced at I/O 2026" (blog.google)

The broad strokes of the article (Google cutting AI prices, competing with OpenAI) are directionally accurate.

### Article 2 — SEVERITY: MODERATE ERRORS
- **"$2.1T balance sheet" is wrong** — actual is ~$704B, off by ~3x
- **"Cloud revenue surged 35%" is unverifiable** from available data
- **"80% price cut" and "$1B credits"** are plausible but could not be independently verified from official sources

---

## SUMMARY OF FINDINGS

| Severity | Count | Details |
|---|---|---|
| 🔴 **CRITICAL** | 3 | NBIS guidance ($4.5B vs $3.0-3.4B), NBIS Accel investment date/attribution, NBIS subtitle growth rate |
| 🟡 **MODERATE** | 1 | GOOGL balance sheet ($2.1T vs $704B) |
| ⚠️ **MINOR/UNVERIFIED** | 4 | NBIS 20K GPUs, GOOGL 80% price cut, GOOGL $1B credits, GOOGL cloud 35% growth |
| ✅ **CORRECT** | 11 | All stock prices, market caps, revenue figures, P/E ratios, growth rates, links |

### Files Modified
- **Created:** `/home/chino/thesignal/fact-check-report-2026-05-28.md` — This report

### Key Takeaways
1. **NBIS article has CRITICAL factual errors** — the guidance figure is inflated by $1.1-1.5B, and a December 2024 fundraising event is presented as a March 2026 event. These undermine the article's credibility.
2. **GOOGL article is mostly accurate on financial metrics** but has a major error on balance sheet size ($2.1T vs actual $704B). The core thesis (Google launched AI pricing changes at I/O 2026) is supported by external news coverage.
3. **All links are live** — no 404s or fabricated sources.
