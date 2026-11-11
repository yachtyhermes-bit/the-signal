# ETF Review — Defiance AI & Power Infrastructure ETF (AIPO)
**Published:** 2026-11-11 · https://readthesignal.net/article/etf-review-aipo-2026-11-11/
**Rotation position:** 9 of 10 (SPMO, QQQM, SHLD, SEIM, SEIV, PAVE, MTUM, VOO covered → AIPO; SMH is next)

## Verified data set (all sourced)
| Item | Value | As-of | Source |
|---|---|---|---|
| Expense ratio | 0.69% (unitary, no waiver; net = gross) | prospectus 2025-12-23 | AIPO prospectus p.8/17 |
| AUM | $760.59M (peak $917.46M) | 2026-11-10 | issuer page; fact sheet 9/30 |
| Holdings | 88 | 2026-11-10 | issuer |
| Top-10 weight | 56.90% (top 3 = 26.2%) | 2026-11-11 | issuer |
| Index | MarketVector US Listed AI and Power Infrastructure (MVAIPO) | live since 2025-01-10 | MarketVector |
| Reconstitution | quarterly; next announce 2026-12-11, implementation 2026-12-18 | — | Index Guide v1.05 |
| 1Y price return | +3.5% fund vs POWR +3.0%, GRID +6.1%, VOO +12.7% | 2026-11-11 | yfinance |
| YTD | +11.4% fund vs VOO +12.5% | 2026-11-11 | yfinance |
| Since inception | +23.35% cum / +17.95% ann. (NAV) | 2026-10-31 | issuer fact sheet |
| Forward P/E | 21.8 fund vs 18.1 VOO (implied growth 28.7% vs 27.2%) | 2026-11-11 | stockanalysis |
| Dividend yield | 0.01%; 30-day SEC yield −0.12% | 2026-10-31 | issuer |
| Drawdown | ~33% from 2026-06-22 peak; vol 41% | 2026-11-10 | computed |

Sector split (issuer, 9/30/26): grid equipment 44.02%, data infra 18.57%, AI semis 13.49%, E&C 12.13%, utilities 11.79%.

## 1Y winners/laggards (price, 11/11/25 → 11/11/26)
Bloom +70.5%, GEV +42.7%, Quanta +37.4%, Vertiv +17.9%, Eaton +1.0%, AVGO +1.4%, GOOGL +1.2% — CEG −21.1%, CCJ −18.8%, NVDA −8.6%. Top-10 contribution ≈ +9.7pp vs fund +3.5%, so the long tail gave back ~6pp.

## Writer + build
- Writer: google/gemini-3.8-flash, one-shot, 2,728 words / 7,083 in + 7,226 out = **$0.0324**.
- Orchestrator trims: 2,728 → 2,468 words (hard cap 2,500). Two factual slips corrected: top-four contribution ("almost ten" → "roughly eleven" pp), and "eighteen-month-old index" → "less than two years old" (index is ~22 months; the fund is 18).
- prose-lint: **exit 0** (2468 words, 181 sentences, SD 6.3, avg 13.6, reading ease 48, slop 0.0/1k, em-dashes 0). Remaining WARNs: two 29/31-word sentences + the 500–900 word target (expected for the long-form edition).
- Hero: FAL flux/schnell, 2 attempts **hard cap respected**, 1536×864 JPEG 245KB, md5 82ec145d…, R2 200 + ETag match. Frame differs from the brief (no paper/mug; clamps instead) — caption and alt describe the actual frame.

## Deploy + verification
- Build: 1,561 files. `npx vercel --prod --yes` from `dist/` → ready.
- Live: root 200, article 200, `-o filter "industrial capex trade on leverage"` present, `/sector/etfs` 200 with 2 card hits, hero R2 200.
- Commit `31494e4a` (JSON + public/img + _backup_dist/img), pushed clean fast-forward to `main`.

## Source list used in links[]
Defiance AIPO product page · AIPO fact sheet 9/30/26 · AIPO prospectus 12/23/25 · MarketVector index page · Index Guide v1.05 · MVAIPO fact sheet 11/10/26 · stockanalysis.com/etf/AIPO · etfrc.com/AIPO · HANetf UCITS clone · Reuters 11/5/26 (AI data-center selloff).

## Notes for next run
- Next fund in rotation: **SMH** (last of the ten). After that the list cycles back to SPMO.
- Vendor disagreements to expect again: AUM (issuer $760.6M vs stockanalysis $728.6M vs Yahoo $823.2M — issuer wins), P/E (28.1 SA vs 31.5 Yahoo vs 34.8 index ex-negatives), Yahoo bid/ask field corrupt on this ticker.
- The UCITS clone (IE000WUTBLT5) is a separate fund, not a share class — do not describe it as one.
