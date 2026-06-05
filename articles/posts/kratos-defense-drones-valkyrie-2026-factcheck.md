# Fact-Check Report: Kratos Is Quietly Building the Pentagon's Drone Army
## File: /home/chino/thesignal/articles/posts/kratos-defense-drones-valkyrie-2026.json

**Overall Verdict: ⚠️ MINOR ISSUES (with one data error)**

---

## Claim-by-Claim Analysis

### 1. TTM Revenue: $1.42B
**Status: ✅ CONFIRMED**
- yfinance totalRevenue: $1,415,200,000
- TTM calculation (Q2 2025 - Q1 2026): $351.5M + $347.6M + $345.1M + $371.0M = **$1,415.2M**
- Official Q1 2026 earnings release confirms $371.0M for the quarter

### 2. Revenue Growth: 22.6% YoY
**Status: ✅ CONFIRMED**
- yfinance revenueGrowth field: 0.226
- Official Q1 2026 earnings release: "Revenues of $371.0 Million Reflect 22.6 Percent Growth"
- ⚠️ Note: The article's **summary** says "18% revenue growth" — this is INCONSISTENT with the body's 22.6% figure and the verified data

### 3. Net Income: $29M
**Status: ✅ CONFIRMED (rounded)**
- yfinance netIncomeToCommon: $29,400,000
- TTM: FY2025 net income ($22.0M) - Q1 2025 ($4.5M) + Q1 2026 ($11.9M) = **$29.4M**
- Article rounds to $29M — acceptable rounding

### 4. Backlog: ~$1.8B
**Status: ⚠️ MINOR ISSUE (UNDERSTATED)**
- Actual total consolidated backlog per Q1 2026 earnings release: **$2.010B**
- KGS segment backlog: $1.635B; KUS segment backlog: $375.4M
- Funded backlog: $1.457B; Unfunded backlog: $553.5M
- Article says "approaching $1.8B" — actual backlog is higher ($2.01B). The article understates this bullish metric.

### 5. BQM-177A: "$400M+ in contracts from Navy and Air Force" / "supersonic target drone"
**Status: ❌ DATA ERROR (two issues)**

**(a) Speed classification:** BQM-177A is described in every source as **"subsonic"** (Sub-Sonic Aerial Target / SSAT), reaching Mach 0.9-0.95. The article calls it a "supersonic target drone" — this is incorrect.

**(b) Contract value:** The maximum contract value if all options exercised is ~$227.6M (per EIN Presswire on the Lot 7 contract). No source found showing $400M+ in total BQM-177A contracts. Additionally, all contracts found are Navy-only; no Air Force BQM-177A contracts were found.

### 6. Valkyrie CCA Additional Developmental Funding
**Status: ✅ CONFIRMED**
- Q1 2026 earnings release specifically mentions "Valkyrie CCA" as a funded initiative
- Northrop Grumman won a US Marine Corps contract for Valkyrie-based CCA development
- Airbus/Kratos partnership marketing Valkyrie for German Air Force

### 7. CCA Program: 1,000+ Autonomous Aircraft
**Status: ✅ CONFIRMED**
- Defense News (March 2023): "Air Force eyes fleet of 1,000 drone wingmen"
- AviationA2Z (May 16, 2026): Recent article confirms "1,000 wingman drones" target
- Air & Space Forces Magazine and other outlets confirm
- Long-term USAF vision: ~2 CCA drones per crewed fighter across ~500 fighters

### 8. Stock Price: ~$56
**Status: ✅ CONFIRMED**
- yfinance previousClose: $56.80
- Current price: $57.30
- Article dated May 26, 2026 — price was approximately $56-57 at that time

### 9. Forward P/E: 53x
**Status: ✅ CONFIRMED**
- yfinance forwardPE: 53.36

### 10. Analyst Targets: Mean $113, Range $75-$150, 20 Analysts
**Status: ✅ CONFIRMED EXACTLY**
- yfinance: targetMeanPrice $113.05, targetLowPrice $75.00, targetHighPrice $150.00, numberOfAnalystOpinions 20

### 11. Valkyrie Flown Alongside F-35s and F-22s
**Status: ✅ CONFIRMED**
- Air & Space Forces Magazine (Dec 2020): Skyborg/Valkyrie payload translated signals between F-22 and F-35 in test
- Facebook posts from Air Force Museum and Military Mechanics confirm XQ-58A Valkyrie formation flights with F-22 and F-35
- Reddit discussion of formation photos

### 12. Linked URLs
**Status: ⚠️ PARTIALLY VERIFIED**

| URL | HTTP Status | Notes |
|-----|------------|-------|
| https://ir.kratosdefense.com/ | 200 ✅ | JS-rendered IR site; curl gets empty body but URL is valid and resolves |
| https://www.defense.gov/Spotlight/Autonomous-Systems/ | 403 ❌ | Blocked by Cloudflare/edge CDN. The path exists but cannot be verified via curl. This is a DoD.gov page behind CDN protections |

### 13. "$8-10B Revenue if 20% CCA" Claim
**Status: ⚠️ SPECULATIVE / NOT VERIFIABLE**
- $8-10B over 10 years implies total CCA program value of $40-50B
- USAF requesting ~$1B in FY2027 for first CCA production
- At ~$20-40M per aircraft × 1,000+ aircraft = $20-40B total potential
- This range is plausible but entirely speculative at this stage — no official DoD budget documents confirm a $40-50B total program value

---

## Summary of Issues Found

| # | Claim | Status | Severity |
|---|-------|--------|----------|
| 1 | Revenue $1.42B | ✅ Confirmed | — |
| 2 | 22.6% revenue growth | ✅ Confirmed; summary says 18% | ⚠️ Minor inconsistency |
| 3 | Net income $29M | ✅ Confirmed | — |
| 4 | Backlog ~$1.8B | ⚠️ Understated (actual: $2.01B) | ⚠️ Minor |
| 5 | BQM-177A "supersonic" / "$400M+" | ❌ Subsonic, not supersonic; contract total ~$228M max | ❌ Data Error |
| 6 | Valkyrie CCA funding | ✅ Confirmed | — |
| 7 | CCA 1,000+ aircraft | ✅ Confirmed | — |
| 8 | Stock price $56 | ✅ Confirmed | — |
| 9 | Forward P/E 53x | ✅ Confirmed | — |
| 10 | Analyst targets $75-$150, mean $113, 20 analysts | ✅ Confirmed exactly | — |
| 11 | Valkyrie with F-35/F-22 | ✅ Confirmed | — |
| 12 | URLs | ⚠️ IR site OK, Defense.gov blocked by CDN | ⚠️ Minor |
| 13 | $8-10B at 20% CCA | ⚠️ Speculative but plausible range | ⚠️ Speculative |
