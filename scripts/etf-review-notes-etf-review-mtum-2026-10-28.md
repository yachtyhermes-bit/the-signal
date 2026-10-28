# ETF Review notes — MTUM (etf-review-mtum-2026-10-28)

**Published:** 2026-10-28 · live at https://readthesignal.net/article/etf-review-mtum-2026-10-28/
**Fund:** iShares MSCI USA Momentum Factor ETF (MTUM) · expense ratio 0.15% · ~$18.1B AUM
**Writer:** google/gemini-3.8-flash one-shot · 7,156 in / 5,050 out · $0.0243
**Length:** 3,000 words (brief asked 1,800-2,500; draft came back 3,087 and was left long on
purpose — it is the longest ETF Review so far, vs PAVE 2,705)
**prose-lint:** exit 0, WARNs only (0 FAILs after 7 sentence/paragraph splits)

## Rotation
List order: SPMO, QQQM, SHLD, SEIM, SEIV, PAVE, **MTUM**, VOO, AIPO, SMH.
Covered before this edition: SPMO (9/23), QQQM (9/17), SHLD (9/30), SEIM (10/7), SEIV (10/14),
PAVE (10/21). Next in rotation: **VOO**.

## The angle
You think you bought a momentum factor fund; you bought a 55% technology portfolio with roughly a
fifth of assets in five semiconductor names, wrapped in an index rule that forbids it from fully
trading its own signal. Two secondary threads: the fund is ~28% smaller than it was at the end of
July while its shares were roughly flat (i.e. money left, not performance), and it has lagged the
cheaper, simpler SPMO by nearly four points a year over a decade.

## Facts verified this run (and how)
| Claim | Value | Source |
|---|---|---|
| Expense ratio | 0.15% | iShares fund page + SEC 497K; stockanalysis.com |
| Index | MSCI USA Momentum **SR Variant** (not the plain MSCI USA Momentum Index) | iShares fund page; annual report (plain index until 11/2020) |
| Selection | top **125** from MSCI USA by momentum score | MSCI SR Variant methodology PDF, §2.3 — verified by direct PDF fetch + text extraction |
| Turnover cap | **30% one-way** per review, iterative substitution | same PDF, Appendix I §A — verified verbatim |
| Caps | 5% at issuer level; group entities >5% capped 25% aggregate; 4.5%/22.5% buffer | same PDF, §2.4/2.5 |
| Reviews | **quarterly** Feb/May/Aug/Nov; pro forma 9 business days prior | same PDF, §3.1.1 |
| AUM | ~$18.1B (10/28) vs $20.43B (9/30 fact sheet) vs $25.15B (7/31 annual report) | stockanalysis.com; iShares fact sheet; annual report |
| Top 10 | 35.2-35.5% (AMD 6.06, MU 5.00, INTC 3.92, CSCO 3.64, JNJ 3.45, XOM 2.96, PANW 2.88, GOOGL 2.62, AMAT 2.53, SNDK 2.42 on 10/28) | stockanalysis.com/etf/mtum/holdings — table parsed directly |
| Sectors | IT **54.6%**, Industrials 10.1, HC 9.4, Energy 8.5; top 4 = 82.6% (9/30) | iShares fact sheet; yfinance cross-check within 30bps |
| Earlier sector mix | IT 47.6% at 7/31 | annual report |
| Turnover | 104% FY26 (116% FY25) | annual report / 497K |
| Returns (9/30, NAV) | 27.19 / 24.39 / 32.44 / 13.83 / 16.48 / 15.78 since inception; benchmark 27.29 / 24.58 / 32.65 / 14.01 / 16.69 / 15.99 | iShares performance table |
| After-tax post-liquidation | 10Y 13.94% vs 16.48% pre-tax | same table |
| Current returns (10/28) | MTUM 21.4 YTD / 18.1 1Y / ~31 3Y / 11.4 5Y / 16.1 10Y; SPMO 19.1 5Y, 19.8 10Y; SPY 12.7 5Y, 15.5 10Y | own yfinance total-return calc |
| Spread / NAV | 0.03% median 30d bid-ask; 0.00% premium/discount | iShares |
| Tracking difference | -19bps 1Y, -21bps p.a. 3Y/10Y | iShares |
| Split | **4-for-1**, record 11/3, payable after close 11/4, ex 11/5; creation unit unchanged | SEC Form 497 (10/5/26) + OCC memo 60053 |
| Valuation | ~26x trailing vs ~24.5x S&P 500; yield 0.6%; beta 1.27; 3y σ 20.4% | stockanalysis/yfinance; iShares fact sheet |
| Bear case | Daniel & Moskowitz "Momentum Crashes" (JFE 2016): Mar-May 2009 losers +163% vs winners +8%; 14 of 15 worst months follow negative 2y market | paper fetched |
| Crowding | Bouchaud et al, momentum rebalancing = 1-2% of order flow; JPMorgan 100th percentile, from 25th in 3 months | arXiv 2001.04185; Yahoo Finance |
| Own record | 2023 +9.2% vs S&P 500 TR +26.2% (-17pp); 2022 -18.3%; COVID peak-trough -34.1% vs SPY -33.7% | own yfinance calc |

## Corrections applied to the writer's draft
1. **10-year compounding multiples** — draft said the 16.1% vs 19.8% gap meant "3.5x versus 5x"; the
   real multiples are **4.45x vs 6.09x**. (The error originated in my own brief; fixed in both.)
2. **2023 comparison basis** — the draft used the S&P 500's *price* return (+24%) against MTUM's
   *total* return (+9.2%), implying a 15pp gap. Like-for-like TR gap is **~17pp** (SPY TR +26.2%).
3. **Portfolio-size advice** — "perhaps 5% to 10% of a portfolio" softened to a satellite framing
   (analysis, not advice).
4. Seven prose-lint splits: six sentences over 34 words broken up, the 8-sentence shrinkage
   paragraph split in two, and the scoreboard's raw number list de-listed per the house "weave,
   never list" rule.

## Deliberately NOT used
- The **16.98 "forward P/E"** shown by stockanalysis — it sits *below* the trailing multiple, which
  is implausible and almost certainly a data artefact.
- The fact sheet's **OCR'd calendar-year return row** (13.45 / -18.23 / 9.10 / 32.88 / 22.10) — it
  does not reconcile and appears column-shifted. Computed calendar years used instead.
- **Constituent-level adds/deletes at the August review** — MSCI does not publish them for this
  variant; no credible public list exists, so the piece describes the *effect* (IT 47.6% -> 54.6%)
  rather than claiming specific names entered or left.

## Hero
`etf-review-mtum-2026-10-28.jpg` — brass gimbal gyroscope on matte slate, window light from the
left. One FAL generation (flux/schnell, 1440x810 -> 1920x1080 crop, q92), md5
40c5716281c9a4e98e08bcaea4f29f46, R2 ETag matched. tesseract found no real text, skin-tone pixel
fraction 0.000. Script: `scripts/gen-etf-review-mtum-hero-20261028.py`.

## Deploy
`npm run build` → 1,466 files in dist → `vercel --prod` from `dist/` after `vercel link --project
the-signal` (projectId prj_injzyv7DMJ348G6KnMlHkz19i2U7) → Aliased https://readthesignal.net.
Verified live: article 200, title present 6x, both corrected phrases present, hero R2 200,
/sector/etfs 200 with card, homepage 200, `public/img/articles/` intact (71 files).

## Watch list for the next edition
- Nov 5: split takes effect (cosmetic).
- End of November: quarterly MSCI review — does the turnover-capped algorithm cut semis *after* the
  October drawdown? That is the live test of the thesis.
- SPMO's next rebalance: March 19, 2027.
