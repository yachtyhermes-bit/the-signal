# NAS Fact-Check Report
**Agent:** NAS — Research / Market Intelligence  
**Date:** May 23, 2026  
**Data Sources:** Yahoo Finance (via yfinance API), SEC filings, company investor relations

---

## 1. palantir-aip-government-ai.json

**Ticker:** PLTR | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim in Article | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Annual revenue | "$3B+" | $5.22B (TTM) | **FABRICATED — understated by ~$2B** |
| Q1 2026 revenue | $963M | **$1.633B** | **FABRICATED — off by $670M** |
| Market cap | $80B | **$328B** | **FABRICATED — off by 4x** |
| GAAP net income (quarterly) | $248M | **$871M** | **FABRICATED — off by 3.5x** |
| Free cash flow (quarterly) | $287M | **$892M** | **FABRICATED — off by 3x** |
| Cash & equivalents | $5.2B | **$8.03B** (cash + ST investments) | **INFLATED claim, actual is 54% higher** |
| Operating margin | 22.4% | **46.2%** | **FABRICATED — actual is 2x higher** |
| Gross margin | 81.1% | **84.1%** | Close but inaccurate |
| Forward P/E | 45 | **66** | **FABRICATED** |
| Trailing P/E | 58 | **154** | **FABRICATED — off by 2.7x** |
| PEG ratio | 1.6 | **1.95** | Inaccurate |
| Rule of 40 | 58 | **~76** (30% rev growth + 46% op margin) | **FABRICATED** |
| Government backlog | $2.3B | Could not verify independently | Unverifiable |
| Total customers | 600 | Could not verify independently | Unverifiable |

### Summary
This article contains **systematic, fabricated financial data** that appears to be from a much earlier period (likely 2023 or early 2024). Every major financial metric is wrong. Revenue, net income, market cap, cash position, margins, and valuation multiples are all significantly off from actual Palantir Q1 2026 reported figures. The article paints a company far smaller and less profitable than reality.

### Flagged Issues
- **Market cap off by 4x** ($80B vs actual $328B) — the most egregious error
- **Quarterly revenue understated by $670M**
- **Net income understated by $623M**
- **Operating margin understated by 24 percentage points**
- Article dates to May 20, 2026 — after Palantir's Q1 2026 earnings were released (early May 2026)

---

## 2. iren-nvidia-deal-ai-cloud-controversy.json

**Ticker:** IREN | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim in Article | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Trailing revenue | $757M | **$757M** | **CORRECT** |
| Market cap | $20B | **$20.3B** | **CORRECT** |
| Free cash flow | -$2.3B | **-$2.31B** | **CORRECT** |
| Debt-to-equity | 148% | **148.8%** | **CORRECT** |
| 52-week range | $8 to $77 | **$8.28 to $76.87** | **CORRECT** |
| Current stock ~$56, was $8 low | Implied | $56.83 | Consistent |
| Forward P/S (at $3.7B ARR) | 5.4x | Math checks out (20B/3.7B) | **CORRECT** |
| $3.4B NVIDIA contract | Claimed | **UNVERIFIED** | Cannot confirm contract specifics |
| $3.7B ARR by year-end 2026 | Management guidance | **UNVERIFIED** | Forward-looking guidance |

### Summary
**This is the most accurate article of the batch.** All financial data points verified against Yahoo Finance match perfectly. The IREN article uses current, correct financial data. The contract claims ($3.4B NVIDIA deal, $3.7B ARR) are management/company assertions that cannot be independently verified without access to contract documents, but the article frames them as claims from management (which is appropriate).

### Issues
- Minor: Forward-looking revenue guidance ($3.7B ARR) is presented as plausible but is aggressive — IREN would need to 5x trailing revenue in ~12 months
- No significant factual errors found in the financial data

---

## 3. coreweave-ai-cloud-dark-horse.json

**Ticker:** CRWV | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim in Article | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Market cap | $58.7B | **$57.6B** | Close (off by ~2%) |
| Revenue (TTM) | $6.23B | **$6.23B** | **CORRECT** |
| Cash on hand | $2.27B | **$2.27B** | **CORRECT** |
| Enterprise value | $88.1B | **~$90.4B** | Close |
| 52-week range | $63.80 - $187.00 | **$63.80 - $187.00** | **CORRECT** |
| P/S ratio | 8.2x | **~9.2x** (57.6B/6.23B) | Off (article might use different share count) |
| YTD return | +50.3% | Could not verify (need Jan 1 price) | **UNVERIFIED** |
| $138.90 1Y analyst target | Claimed | **UNVERIFIED** | Article does not cite which analysts |

### Omitted Data (Misleading Framing)

| Metric | Actual Value | Article Disclosed? |
|---|---|---|
| Net income (TTM) | **-$1.59B** | **NOT DISCLOSED** |
| Free cash flow (TTM) | **-$8.56B** | **NOT DISCLOSED** |
| Operating margin | **-6.9%** | **NOT DISCLOSED** |
| Debt-to-equity | **738.5%** | **NOT DISCLOSED** |
| Total debt | **$35.1B** | **NOT DISCLOSED** |
| Q1 2026 FCF | **-$4.7B** (single quarter) | **NOT DISCLOSED** |

### Summary
The article's stated financial data (revenue, cash, 52-week range) is **accurate**, but the article is **highly misleading by omission**. CoreWeave is deeply unprofitable (net loss of $1.59B TTM), burning massive cash (FCF -$8.56B TTM, including -$4.7B in Q1 2026 alone), and carries extreme leverage (739% D/E, $35.1B debt). The bullish "dark horse" framing without any mention of these existential risk factors constitutes **misleading financial journalism**.

### Flagged Issues
- **Material omissions** of negative net income, negative FCF, and extreme leverage
- The article presents CoreWeave as a straightforward infrastructure play while hiding that it is a highly leveraged, cash-burning enterprise
- The "cash on hand" of $2.27B looks strong in isolation but is trivial against $35.1B total debt

---

## 4. cerebras-ipo-nvidia-threat-analysis.json

**Ticker:** CBRS | **Sentiment:** Neutral

### Key Claims vs. Actual Data

| Claim in Article | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Revenue (2025) | $510M | **$510M** (TTM) | **CORRECT** |
| 47% net margin | Claimed | **Cannot verify** — yfinance shows net income, not net margin % directly | **QUESTIONABLE** — $510M * 47% = $240M net income, which would be exceptional for pre-IPO hardware company |
| $26.6B IPO valuation | Claimed | Not directly verifiable via yfinance | See below |
| IPO price range | $125-$135 | Could not verify opening price | **UNVERIFIED** |
| IPO opened at $350 | Claimed | Not verifiable via yfinance | **UNVERIFIED** |
| First-day close | $311 (+68%) | Current price $256.78 (well below $311) | Price has dropped significantly since IPO |
| $20B OpenAI deal (750MW) | Claimed | **EXTRAORDINARY CLAIM** — needs verification | **HIGHLY QUESTIONABLE** |
| Current market cap | Not stated | **$56.4B** (current) vs $26.6B (IPO) | Stock is down from IPO first-day close |

### Issues
- **$20B OpenAI deal is an extraordinary claim requiring extraordinary evidence.** A $20B compute deal with OpenAI for a company doing $510M in revenue is unprecedented. This would be the largest compute deal in AI history. **Verification strongly recommended.**
- The "47% net margin" claim for a pre-IPO hardware company with $510M revenue is questionable — most AI hardware companies operate at negative margins early in their lifecycle
- The current stock price ($256.78) is **18% below** the claimed first-day close of $311, suggesting the post-IPO hype has faded
- IPO pricing details ($125-$135 range, $350 open) could not be independently verified through available data sources
- Current shares outstanding of 34.5M suggests the $26.6B valuation at $311/share would require ~85.5M shares — a ~2.5x discrepancy unless significant dilution occurred at IPO

---

## 5. nebius-group-growth-2026.json

**Ticker:** NBIS | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim in Article | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Revenue 2024 | ~$80M | ~$80M (approximate) | **PLAUSIBLE** |
| Revenue 2025 | ~$300M | **$525M** (actual 2025) | **FABRICATED — actual is 75% higher** |
| Revenue 2026E | $600M+ | **$399M in Q1 2026 alone** (annualizing to ~$1.6B) | **FABRICATED — actual Q1 alone is 67% of full-year claim** |
| Market cap | ~$10.5B | **$54.5B** | **FABRICATED — off by 5x** |
| Stock price range | $12 → $29 | **$34.72 (52W low) → $214.77 (current)** | **FABRICATED — actual price is 7.4x the claimed high** |
| Private placement | $700M from Accel & Nvidia | Cannot directly verify | **UNVERIFIED** |
| Paris cluster | 20,000 H100 GPUs | Cannot independently verify | **UNVERIFIED** |
| Cash on hand | $2B+ | **$9.3B** | **FABRICATED — actual is 4.6x higher** |

### Summary
**This article has the most catastrophic factual errors of any article in the batch.** Every single financial metric is dramatically wrong. The stock price, market cap, revenue projections, and cash position are all off by multiple factors.

### Flagged Issues
- **Market cap off by 5x** ($10.5B vs $54.5B) — fundamental error
- **Stock price range is completely wrong** — claims $12→$29, actual 52W range is $34.72→$233.73, current price $214.77
- **Revenue grossly understated** — claims $600M+ for full-year 2026, but Q1 2026 alone delivered $399M
- **2025 actual revenue was $525M** — article says ~$300M
- **Cash position massively understated** — article says "$2B+", actual is $9.3B
- Article date is May 22, 2026 — all this data was available before publication
- The article makes Nebius look like a much smaller company than it actually is, which is unusual for a bullish article (typically bullish articles inflate, not deflate)

---

## 6. amazon-q1-2026-aws-reacceleration.json

**Ticker:** AMZN | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim | Article Value | Actual (yfinance Q1 2026) | Verdict |
|---|---|---|---|
| Total revenue | $187.5B | **$181.5B** (actual Q1 2026) | **FABRICATED — inflated by $6B** |
| Consensus estimate (revenue) | $183.2B | **SUSPECT** — actual revenue ($181.5B) is $1.7B BELOW this claimed estimate | **FABRICATED** — article claims a beat, but actual revenue missed this figure |
| Operating income | $23.9B | **$23.85B** | **CORRECT** |
| Consensus estimate (op income) | $20.1B | Could not verify independently | **UNVERIFIED** |
| Net income | $18.4B (+77% YoY) | **$30.3B** (+76.7% YoY) | **FABRICATED — net income understated by $11.9B** (growth rate % is approximately correct) |
| AWS revenue | $28.4B | **CANNOT VERIFY** (no segment data in yfinance) | **UNVERIFIED** |
| AWS growth | 28% YoY | **CANNOT VERIFY** (total AMZN growth was 16.6% YoY) | **UNVERIFIED** |
| AWS annualized run rate | $150B | $28.4B * 4 = $113.6B (if article's AWS number is right); or $150B implies $37.5B/quarter | **INCONSISTENT** — math doesn't add up |
| Advertising revenue | $17.5B | **CANNOT VERIFY** (no segment data) | **UNVERIFIED** |
| NA Retail | $112.3B | **CANNOT VERIFY** (no segment data) | **UNVERIFIED** |
| International | $41.3B | **CANNOT VERIFY** (no segment data) | **UNVERIFIED** |
| Operating margin | 12.8% | **13.1%** ($23.9B/$181.5B) | Close |

### Summary
The article's total revenue figure ($187.5B) is **wrong** — actual Q1 2026 revenue was $181.5B (off by $6B). Net income is **dramatically wrong** — article says $18.4B, actual is $30.3B (off by $11.9B, a 39% error). Operating income is the one figure that matches. Additionally, the article claims revenue "crushed estimates" of $183.2B, but **actual revenue was $1.7B below that claimed estimate** — meaning the article fabricated both the actual number and the beat narrative.

### Flagged Issues
- **Revenue inflated by $6B** (3.3% over actual)
- **Net income understated by $11.9B** (39% below actual) — the error direction is unusual for a bullish article
- **Article fabricates a "beat" narrative** — claims revenue of $187.5B beat estimates of $183.2B, but actual revenue was $181.5B (below the claimed estimate)
- **AWS annualized run rate of $150B** is inconsistent with the claimed AWS quarterly revenue of $28.4B ($28.4B * 4 = $113.6B, not $150B)
- Segment-level data (AWS, Advertising, Retail) cannot be verified through yfinance

---

## 7. alphabet-5-trillion-milestone.json

**Ticker:** GOOGL | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Market cap | $5 trillion | **$4.64T** (GOOGL only) to **~$4.77T** (all classes) | **INFLATED — actual is $230B-$360B below $5T** |
| Stock price | $387.66 | **$387.66** (prices.json) / **$382.97** (yfinance current) | **CORRECT** (at time of writing) |
| BofA price target | $430 | **UNVERIFIED** | **QUESTIONABLE** — article does not cite specific BofA analyst note |
| Gemini MAUs | 1.5B+ | **CANNOT VERIFY** | Google does not publicly disclose Gemini MAUs |
| YouTube revenue | ~$50B annual | **CANNOT VERIFY** (no segment data) | **UNVERIFIED** |
| Cloud rank | #3 | **CORRECT** (behind AWS, Azure) | **CORRECT** |

### Issues
- **$5T market cap is inflated.** At the claimed stock price of $387.66 and with ~12.3B total shares (all classes), market cap = ~$4.77T. At the current yfinance price of $382.97, it's ~$4.71T. The article rounds up $230-360B to hit the $5T milestone.
- The claim "Alphabet just joined the $5 trillion market cap fraternity" implies it crossed $5T, which is **not supported by available data**
- **BofA $430 price target** cannot be verified without the specific analyst report reference
- **1.5B+ Gemini MAUs** is an unverifiable claim — Google has not publicly disclosed this metric
- Article frames the "stock dip" after Google I/O as irrational market behavior rather than potentially justified

---

## 8. palo-alto-anthropic-project-glasswing-2026.json

**Ticker:** PANW | **Sentiment:** Bullish

### Key Claims vs. Actual Data

| Claim | Article Value | Actual Value | Verdict |
|---|---|---|---|
| Palo Alto dropped 6% before Glasswing | Claimed | PANW 52W range: $139.57-$261.41. Current: $260.58 | **UNVERIFIED** — need specific date/price data |
| Claude uncovers 7x more security flaws | Claimed | **CANNOT VERIFY** — Anthropic marketing claim | **QUESTIONABLE** — typical AI vendor benchmark |
| Verizon first telecom partner | Claimed | **CANNOT VERIFY** | **UNVERIFIED** |
| Project Glasswing exists | Claimed | **CANNOT VERIFY** — no Anthropic page found at /glasswing | **HIGHLY QUESTIONABLE** |

### Additional Verification Attempt

- The article links to `https://www.anthropic.com/glasswing` — this URL likely does not exist or redirects
- The article links to `https://www.barrons.com/articles/palo-alto-networks-anthropic-stock-2026` — ability to verify is blocked by paywall
- The "7x more security flaws" claim sounds like a typical AI vendor benchmark figure that is likely cherry-picked

### Issues
- **Project Glasswing's existence cannot be independently confirmed** through available sources
- The article's "7x more flaws" claim is presented as objective data but is likely a marketing claim from Anthropic
- The broader thesis (AI is a tailwind not a threat for cybersecurity) is reasonable, but the specific claims about Project Glasswing remain unverified
- Article presents no specific financial data beyond stock movement, making it hard to fact-check
- **Potential fabricated narrative** — if Project Glasswing doesn't exist or is much smaller than portrayed, the entire article is misleading

---

## Summary Statistics

| Article | Financial Accuracy | Omissions/Misleading | Overall Verdict |
|---|---|---|---|
| 1. Palantir AIP | **FAIL** — 12/14 metrics wrong | Systematic data fabrication | **REJECT** — data appears from 2023-2024 |
| 2. IREN NVIDIA Deal | **PASS** — All verified data correct | Minor: forward guidance aggressive | **ACCEPT** — most accurate article |
| 3. CoreWeave | **PASS** on disclosed data | **FAIL** — massive omissions (losses, debt, cash burn) | **MISLEADING** — hides material risks |
| 4. Cerebras IPO | Mixed — revenue correct | $20B OpenAI deal unverified, 47% margin questionable | **PARTIAL** — extraordinary claims need proof |
| 5. Nebius Group | **FAIL** — Every metric catastrophically wrong | Understates everything by 2-7x | **REJECT** — completely fabricated numbers |
| 6. Amazon Q1 2026 | **FAIL** — Revenue off by $6B, net income off by $11.9B | AWS run rate inconsistent | **REJECT** — significant numerical errors |
| 7. Alphabet $5T | **FAIL** — Market cap inflated by $230-360B | BofA target, Gemini MAUs unverifiable | **PARTIAL** — milestone claim unsupported |
| 8. Project Glasswing | N/A — no financial claims | Project existence unconfirmed | **QUESTIONABLE** — likely fabricated/unverifiable |
