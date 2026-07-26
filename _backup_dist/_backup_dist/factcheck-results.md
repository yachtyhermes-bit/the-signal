# Fact-Check Report — May 30, 2026

## ARTICLE 7: Tesla/SpaceX Merger Chatter (`tesla-spacex-merger-chatter-2026.json`)

### Source Link Verification

| Source | Claimed URL | HTTP Status | Verdict |
|--------|------------|-------------|---------|
| CNBC | https://www.cnbc.com/2026/05/29/spacex-tesla-merger.html | **404** | ❌ **FABRICATED URL** — Actual article exists at: https://www.cnbc.com/2026/05/26/spacex-tesla-merger-chatter-reignites-as-musk-rocket-company-nears-ipo.html (200 ✅) |
| Bloomberg | https://www.bloomberg.com/news/articles/2026-05-29/elon-musk-s-spacex-is-said-to-consider-merger-with-tesla-or-xai | 403 (paywall) | ⚠️ **INCONCLUSIVE** — Paywall blocks access. Similar Bloomberg article from Jan 30 exists (same slug pattern, 403). Bloomberg Law article exists: https://news.bloomberglaw.com/esg/early-spacex-investor-says-tesla-tie-up-is-only-a-matter-of-when (200 ✅) |
| Reuters | https://www.reuters.com/business/autos-transportation/elon-musks-spacex-consider-merger-with-tesla-sources-2026-05-29/ | 401 (paywall) | ⚠️ **INCONCLUSIVE** — Paywall. Cannot confirm or deny existence. |
| Seeking Alpha | https://seekingalpha.com/article/2026-05-29/spacex-tesla-merger-master-plan | 403 → redirect to generic | ❌ **SUSPECT/FABRICATED** — Redirects to generic site root, no evidence this article exists. |
| The Guardian | https://www.theguardian.com/technology/2026/may/29/spacex-musk-tesla-starlink | **404** | ❌ **FABRICATED URL** — Actual Guardian article about SpaceX/Tesla merger exists at: https://www.theguardian.com/science/2026/jan/30/spacex-considers-tesla-merger-xai-tie-up-elon-musk-report (200 ✅) but from January 30, 2026, not May 29. |

**Story Reality Check: The SpaceX-Tesla merger story IS real and widely covered.** Google News shows coverage from CNBC (May 26), Bloomberg (3 days ago — "Only a Matter of When"), Forbes, Semafor, Electrek, The Motley Fool, Investor's Business Daily, The Street, CleanTechnica, Teslarati, CoinDesk, and 24/7 Wall St. The underlying story exists; the specific source URLs in the article are fabricated/wrong.

### Financial Metrics Verification (vs Yahoo Finance Live Data)

| Metric | Article Claims | Actual (Yahoo Finance) | Verdict |
|--------|---------------|----------------------|---------|
| Stock Price | $442 | $442.10 (May 28 close) | ✅ **CORRECT** |
| Market Cap | $1.66T | $1.637T (at $435.79) / ~$1.41T at $442 (using 3.19B shares) or $1.637T (actual from yfinance) | ⚠️ **OFF by ~1.4%** (actual $1.637T vs claimed $1.66T). Using 3.755B shares at $442 = $1.66T — yfinance reports 3.756B shares outstanding. **CORRECT if using that share count.** ✅ |
| Revenue (TTM) | $97.9B | $97.88B | ✅ **VERIFIED** |
| Revenue Growth | 15.8% YoY | 15.8% | ✅ **VERIFIED** |
| Forward P/E | 176.2x | 173.6x | ⚠️ **Minor discrepancy** (off by ~1.5%) |
| Analyst Consensus | Buy (41 analysts) | Buy, 41 analysts | ✅ **VERIFIED** |
| Mean Target Price | $411 | $411.89 | ✅ **VERIFIED** |
| Operating Cash Flow | $16.5B | ~$14.75B (FY2025) / TTM varies | ⚠️ **Could not directly verify** — FY2025 shows ~$14.75B (FCF $6.22B + CapEx $8.527B). TTM may be higher. |
| Spacex Valuation | $1T-$2T | Not verifiable via public data | ⚠️ **Not independently verifiable** |
| Video ID | oRntlcxw8P8 | — | ✅ **SAFE** — NOT on blocklist |

## ARTICLE 8: Palantir Q1 Earnings Miss (`palantir-q1-earnings-miss-2026.json`)

### Source Link Verification

| Source | Claimed URL | HTTP Status | Verdict |
|--------|------------|-------------|---------|
| CNBC (Palantir earnings) | https://www.cnbc.com/2026/05/07/palantir-q1-2026-earnings.html | **404** | ❌ **FABRICATED URL** — Actual article exists at: https://www.cnbc.com/2026/05/04/palantir-pltr-q1-earnings-report-2026.html (200 ✅). Wrong date (May 7 → May 4) and wrong slug. |
| SaaStr | https://www.saastr.com/palantir-q1-2026-has-broken-the-enterprise | 301 → 200 ✅ | ✅ **RESOLVES** — Redirects to: https://www.saastr.com/palantir-q1-2026-has-broken-the-enterprise-software-mold-again-revenue-accelerates-to-85-at-6b-arr/ |
| CNBC (Burry short) | https://www.cnbc.com/2026/05/15/michael-burry-palantir-short-bet.html | **404** | ❌ **FABRICATED URL** — No CNBC article found at this URL. Burry's Palantir short position is reported by other outlets (MSN, AOL, Motley Fool, IBTimes, Morningstar), but the specific CNBC article cited does not exist. |

### Financial Metrics Verification (vs Yahoo Finance Live Data)

| Metric | Article Claims | Actual (Yahoo Finance / CNBC article) | Verdict |
|--------|---------------|--------------------------------------|---------|
| Q1 Revenue | ~$1.4B (estimated) | $1.63B (per actual CNBC article) | ❌ **SIGNIFICANTLY UNDERSTATED** — Actual Q1 revenue was $1.63B, not ~$1.4B |
| Revenue Growth | 85% YoY | 84.7% (yfinance) / 85% (CNBC article) | ✅ **VERIFIED** |
| ARR | $6.5B+ | Confirmed by SaaStr article title | ✅ **VERIFIED** |
| FY 2026 Guidance | Raised to 71% | "annual jump of 71%" (per CNBC article) | ✅ **VERIFIED** |
| Adjusted Operating Margin | 60% | 46.2% (yfinance operating margins) | ❌ **SIGNIFICANTLY OVERSTATED** — Actual operating margin is 46.2%, not 60% |
| RPO Growth | +134% YoY | $4.45B vs $1.9B = +134% (per CNBC article) | ✅ **VERIFIED** |
| Commercial Customers | 1,007 (+31% YoY) | 1,007, up 31% (per CNBC article) | ✅ **VERIFIED** |
| Revenue per Employee | $1.5M | $1.5M (stated by Alex Karp, per CNBC article) | ✅ **VERIFIED** |
| YTD Return | -19.4% | -19.36% (Dec 31 close $177.75 → May 28 close $143.34) | ✅ **VERIFIED** (CNBC says -18%) |
| Forward P/E | ~50x | 75.47x | ❌ **SIGNIFICANTLY UNDERSTATED** — Actual forward P/E is 75.5x, not ~50x |
| Rosenblatt Target | $225 | Not found in SaaStr article; cannot verify | ❌ **UNVERIFIED** — SaaStr article does not mention Rosenblatt |
| Burry Short Position | Worth <$50/share | Burry has shorted PLTR (multiple sources confirm), but specific $50 claim unverifiable | ⚠️ **PARTIALLY VERIFIED** — Short position is real, specific price target unsubstantiated |

---

## SUMMARY OF ISSUES

### Fabricated/Fake URLs (return 404):
1. **CNBC TSLA/SpaceX** — Claimed: `/2026/05/29/spacex-tesla-merger.html` → Should be: `/2026/05/26/spacex-tesla-merger-chatter-reignites-as-musk-rocket-company-nears-ipo.html`
2. **Guardian TSLA/SpaceX** — Claimed: `/technology/2026/may/29/spacex-musk-tesla-starlink` → Should be: `/science/2026/jan/30/spacex-considers-tesla-merger-xai-tie-up-elon-musk-report` (and from Jan, not May)
3. **CNBC Palantir earnings** — Claimed: `/2026/05/07/palantir-q1-2026-earnings.html` → Should be: `/2026/05/04/palantir-pltr-q1-earnings-report-2026.html`
4. **CNBC Burry short** — Claimed: `/2026/05/15/michael-burry-palantir-short-bet.html` → No equivalent article found at CNBC

### Financial Discrepancies:
1. **PLTR Forward P/E**: Claimed ~50x, actual 75.5x (**off by 51%**)
2. **PLTR Adjusted Operating Margin**: Claimed 60%, actual 46.2% (**off by 30%**)
3. **PLTR Q1 Revenue**: Claimed ~$1.4B, actual $1.63B (**understated by ~16%**)
4. **TSLA Market Cap**: Minor discrepancy ($1.66T vs $1.637T) — resolved by using actual share count
5. **TSLA Forward P/E**: Minor ($176.2x vs $173.6x)

### What's Verified Correct:
- TSLA stock price ($442), revenue ($97.9B), revenue growth (15.8%), analyst consensus (Buy, 41 analysts), mean target ($411)
- PLTR revenue growth (85%), ARR ($6.5B+), guidance (71%), RPO growth (+134%), commercial customers (1,007), revenue/employee ($1.5M), YTD return (-19.4%)
- SpaceX-Tesla merger story IS a real, widely-reported story
- Video ID oRntlcxw8P8 is NOT on the blocklist
- SaaStr source resolves correctly to a real, relevant article
