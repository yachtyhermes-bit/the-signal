# ETF Review — SMH (VanEck Semiconductor ETF) · 2026-11-18

Live: https://readthesignal.net/article/etf-review-smh-2026-11-18/
Writer: google/gemini-3.8-flash, one-shot, 7,589 in / 7,509 out, $0.0339
Final: 2,492 words · prose-lint 0 FAIL · reading ease 54 · avg sentence 14.6 words

## Rotation
Only SMH remained uncovered of the 10-fund list (SPMO, QQQM, SHLD, SEIM, SEIV, PAVE, MTUM, VOO,
AIPO, SMH). No daily-edition overlap on SMH in the last 3 days. With this edition the rotation list
is complete — the next edition should restart at SPMO or add new funds.

## The angle
Not the fee story. The **index rule** story: the MVIS 25 caps the biggest names at 20% only on the
quarterly rebalance date, so the cap is a *target*, not a brake. Nvidia sat at 20.19% on 31 Oct —
exactly at the ceiling, which proves the cap was setting the weight, not the market. After the
resignation it fell to 17.42%, and the December rebalance will top it back up to a fifth of the fund.

## Editorial corrections applied to the Gemini draft
1. **Rebalance mechanic was self-contradictory.** Draft said the rule "trims the excess back down to
   20%" and then, in the next clause, that it "re-buys it right back to that 20% limit". Corrected
   throughout to: the cap is a fixed target — trims when a name runs, tops it back up when it falls.
   The writer had absorbed an ambiguous line in my brief; the fix made the thesis stronger and
   fact-checkable.
2. **YTD give-back arithmetic was wrong.** Draft: "at the end of September… nearly 69%… over the
   subsequent seven weeks handed back roughly seventeen percentage points". Sept 30 → Nov 17 is ~41
   points (68.93 → 27.83). The 17 points is Oct 31 (45.17) → Nov 17. Rewritten with all three dates.
3. **UBS statistic over-specified.** Draft added "delayed or eliminated by grid and political
   bottlenecks" — mechanism not in the source. Softened to "roughly 30% of 2028 data-centre capacity
   is now at risk".
4. **Ballot-measure causality.** "resulted in restrictive ballot measures" → the sources say ballot
   measures *signalled* backlash. Reworded.
5. **SOXX 10-year basis.** 34.4% vs 32.4% is market-price through 30 Sept, while the issuer's 10Y NAV
   TR is 32.60%. Relabelled the basis explicitly rather than letting two bases sit side by side.
6. **"Nvidia's incoming leadership team"** → there is no incoming team; it is an interim CEO. Fixed.
7. **Summary had "look past past performance"** — duplicated word, fixed.
8. Subtitle "keeps buying the winner" → "keeps a fifth of the fund in one stock".

## Numbers verified independently of the research digest
- Drawdown: peak close $668.91 (2026-06-22) → low $447.73 (2026-11-05) = −33.07%; −31.2% from the
  peak at the 11-17 close. Confirmed from Yahoo daily bars.
- 2026-11-05 session: −11.21% close-to-close, confirmed.
- YTD: 68.93% (9/30 issuer) → 45.17% (10/31 issuer) → 27.83% (11/17 issuer NAV).
- Nvidia CEO transition: confirmed against nvidianews.nvidia.com and the 11/11 Form 8-K
  (resignation accepted 11 Nov, announced 12 Nov; Colette Kress interim CEO and staying CFO;
  Harvey Jones first-ever board chair). AP and Guardian corroborate.
- Fee arithmetic computed, not copied: 0.35% on $10,000 over 10 years at 8% gross = $690 of ending
  balance; vs SOXX 0.33% the ten-year difference is $39; vs SOXQ 0.19% it is $313.

## Deliberately left out
- **30-day median premium/discount to NAV** — VanEck publishes it but the site blocks automated
  access; only point readings existed (+0.035% on 11/16, −0.06% on 11/12). Said "trades at NAV".
- **Securities-lending revenue split** (fund vs lending agent) — unverified. Said lending exists
  (0.11% of assets on loan) and carries counterparty risk, nothing more.
- **Portfolio earnings growth rate** — no issuer-published figure found.
- Benzinga's "Nvidia cut to 8.9%" and JournalArta's "$502 / +39% YTD" both contradict VanEck's own
  files. Not used.

## Link status at publish
200: MarketVector index guide, MarketVector index page, Nvidia newsroom, stockanalysis SMH + SOXX,
ETF Strategy, tradewize, filing.fyi, FactSet PDF.
403 (bot-block, not dead): sec.gov 8-K, apnews.com. VanEck URLs 302 to a cookie-consent page for
automated clients; they are the canonical issuer pages and load normally in a browser.

## Build/deploy
`npm run build` → 1,607 files. Deployed from `dist/` after `rm -rf .vercel` + relink to project
`the-signal` (prj_injzyv7DMJ348G6KnMlHkz19i2U7 — matches the repo root, so no stray dist-* project).
Verified live: article 200 with the corrected phrase, R2 hero 200 / image/jpeg / 124,837 bytes
(ETag == local md5 83c3dd937fa18ecb49891da51d527604), sector card present on /sector/etfs, homepage 200.

## Hero
1200×675, 121.9 KB. Scene: silicon wafer with die grid against charcoal backdrop on brushed steel
bench, loupe + lens tissue. Single FAL generation, no retries. Note: the "rainbow diffraction" and
the wafer notch in the prompt did not render — caption and alt describe only what is actually in
frame.
