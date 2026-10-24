# Focus List 2026-10-24 — notes for human review

Live: https://readthesignal.net/article/focus-list-2026-10-24/
JSON: articles/posts/focus-list-2026-10-24.json · Hero: R2 `img/articles/focus-list-2026-10-24.jpg` (1920×1080, 421,719 B, ETag matches local md5 7997f687af81ea1e5789af46325073cf)
Writer: google/gemini-3.8-flash one-shot, two drafts ($0.0382 + $0.0220). Published draft = v2 (v1 was 3,164 words and carried two factual slips: "56% of semiconductor revenue" and "FTC antitrust inquiry").

## Selection, and why it differs from the suggested four
Suggested: AVGO, CEG, SOFI + one non-AI name. Actual: **AVGO, MU, MSFT, CEG.**
- **SOFI excluded** — `sofi-capital-light-illusion-2026.json` was modified 10/21, inside the 5-day no-repeat window.
- **ZS considered and dropped** — it rose ~23% in the week to Friday (207.38 → 255.15) and trades above its mean target; not a "we like it at these prices" name.
- **MU added** — −30% off its June high with estimates rising, 4.2x forward; the cleanest "hated" setup of the 26 covered tickers.
- **MSFT** carries the beginner-recognition slot.
- Sectors: ai (AVGO, MU), mega-cap (MSFT), ai-power (CEG) = 3 distinct sectors, rule satisfied. Article `sector` field set to `ai`.
- CEG repeats last week's edition. Deliberate: the scorecard grades the call that went wrong (−6.6% on an Accumulate), and the Oct 29 PJM refiling is a live, dated event. If repetition is unwanted, swap CEG for AMZN next time.

## Facts that are EXPECTED, not announced — do not upgrade them later without a source
1. **AVGO next print Dec 9** — from Broadcom's IR head on the Q3 call ("currently plans to report … on Wednesday, December 9, 2026"). No formal date notice issued as of Oct 24; several aggregators list Dec 10. Copy says "due Dec 9, as management said on the last call".
2. **CEG Q3 Nov 9** — four calendars + one wire agree; Constellation's IR page 403s to automation, so the primary posting was never read.
3. **MU FQ1** — written as "mid-to-late December"; vendors split Dec 16 vs Dec 23 and the company has not issued a date.

## Numbers worth a second pair of eyes
- AVGO: TTM revenue $89.10B, FCF $39.40B computed from quarterly statements; RPO $179.2B is quoted in the brief but not in the copy.
- MSFT: FCF $66.99B and capex $115.95B are computed from quarterly statements — yfinance's `info["freeCashflow"]` ($16.55B) is wrong for this name.
- MU: adjusted FCF $62.31B (OCF $89,675M − net capex $27,370M); yfinance's field ($29.1B) is wrong.
- CEG: TTM FCF ≈ $309M is a blended pre/post-Calpine period — the copy uses it only as "real trailing free cash flow after growth expenditures", which is defensible but is not a clean run-rate.
- MU "YTD +178%" and the CEG "~27x 12-quarter median multiple" (Q4'23 EPS estimated) sit in the brief, not the copy.

## Not verified, kept out of the copy
- Broadcom's $35B AI XPV tranche size (secondary sources only), Anthropic IPO timing/size, the CEG Rhode Island/Shell purchase, CEG short interest, and the Ratepayer Protection Act vote count.

## Checks run
- `prose-lint.py` → exit 0, zero FAIL (6 long paragraphs split at sentence boundaries; no wording changed).
- Six paragraph-split edits + four fact micro-edits applied post-writer; everything else is the writer's text verbatim.
- Build via `npm run build`; deploy from `dist` with `--archive=tgz`; live 200 + title, h2s, R2 hero `?v=` and disclosure confirmed; homepage, /sector/ai/ and /articles/ all carry the slug.
- No exact share prices in the copy (checked 321.68 / 524.51 / 877.55 / 253.45 → 0 hits).
