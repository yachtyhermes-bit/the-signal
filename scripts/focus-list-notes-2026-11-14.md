# Focus List 2026-11-14 — notes for review (not part of the article)

Live: https://readthesignal.net/article/focus-list-2026-11-14/
Slug: `focus-list-2026-11-14` · 2,542 words · writer gemini-3.8-flash ($0.0429) · prose-lint PASS

## Names and verdicts
| # | Ticker | Nickname | Verdict | Sector |
|---|--------|----------|---------|--------|
| 1 | CEG | The Toll Road | Accumulate | ai-power |
| 2 | RTX | The Parts Counter | Accumulate | defense |
| 3 | NFLX | The Gym Membership | Accumulate | mega-cap |
| 4 | AMD | The Second Source | Wait for a better entry | ai |

Series rotation: AMD is the first appearance in this series. CEG appeared 10/17 and 10/24, RTX and NFLX
on 10/31 — all three came back this edition because each had a material new datapoint since:
CEG's Q3 print and second guidance raise (9 Nov), RTX's S&P upgrade to A- (13 Nov), NFLX sliding to a
52-week low after cutting 2026 ad revenue to ~$2.7B. If the user wants stricter non-repetition, the
rotation rule needs to be tightened in the cron prompt (currently only "no article JSON touched in the
last 5 days").

## Facts verified against primary sources
All four quarters verified from the 8-K exhibit on SEC EDGAR (links in the article):
- CEG Q3'26: revenue $9,550M vs $6,570M (+45%); adj operating EPS $5.06 vs $3.04; GAAP $5.19;
  FY guide raised/narrowed to $12.50–$12.80; 55 GW fleet; 690 MW / 20-yr Amazon PPA at Calvert Cliffs
  (>$3B); Google 20-yr PPA (>$4.3B uprates, 11 PJM units), 15-yr 2,700 MW load-following, Peak+ 270 MW;
  RISEC 609 MW purchase.
- RTX Q3'26: sales $24,965M (+11%, +12% organic); adj EPS $2.26 (+33%, incl $0.25 IEEPA); FCF $2,119M
  vs $4,025M (−47%); backlog $340B ($176B/$164B); >$81B awards; FY guide adj sales $97.0–97.5B,
  adj EPS $7.65–7.75, FCF $9.0–9.2B; $363M customer-bankruptcy charge.
- NFLX Q3'26: revenue $12,870M (+11.8%); op margin 34.6% vs 28.2%; diluted EPS $0.87 (+49%); FCF
  $2,884M; Q4 guide $13.4B; FY26 ~$51.1B / 31.5% margin; ad revenue ~$2.7B vs ~$3B previously;
  buyback 63.9M shares for $4.8B, $22.3B left; gross debt $15.3B.
- AMD Q3'26: revenue $13,377M (+45%); DC $8.5B (+97% y/y); non-GAAP GM 56%; non-GAAP EPS $2.09 (+74%);
  Q4 guide ~$17B ±3% (+66% y/y) at ~55% GM; FCF $554M (vs $2,570M in Q1); inventories $11,463M vs
  $7,920M a year earlier; total debt $7,079M vs $3,220M.
- Tape (Fri 11/6 → Fri 11/13 closes, yfinance auto_adjust=False): CEG +12.1%, RTX +4.8%, NFLX −2.0%,
  AMD +18.9%; scorecard AVGO +18.2%, AMZN +2.8%, SOFI −4.9%, ZS −2.6% — all match the prose.
- 52-week/200-day positions computed from `history(period='1y', auto_adjust=False)`.

## Corrections made to the model draft (facts frozen, rhythm pass)
- Broadcom's $21.7B AI-semiconductor bar is QUARTERLY, not annual.
- CEG "topped consensus by ~30%" was unverified → replaced with the verified year-over-year comparison.
- RTX $9.0–9.2B is FREE CASH FLOW guidance, not operating cash.
- AMD debt/inventory restated to the balance-sheet lines ($7.1B total debt; $11.5B vs $7.9B inventory)
  instead of the analyst agent's $8.9B / "35% in one quarter", which did not reconcile.
- SpaceX opening sentence corrected to the two sites' actual power strategies (Texas self-generates;
  Arizona is negotiating with rural co-ops and needs a Cochise County vote on 9 Dec).
- Calpine acquisition date removed (not verified this session).

## Open items / not verified
- CEG's exact Q4 report date (Feb 24, 2027) is the customary schedule, not a company-confirmed date.
- Fed December decision date (Dec 9) is inherited from the 11/07 edition; the FOMC calendar page was
  not parsed this session. The article only says "December rate verdict" — no date stated.
- AMD's "2027 revenue growth above 80%" is an earnings-call statement, not guidance; the article says
  so explicitly.
- yfinance `forwardPE` used for the relative multiples (CEG 20.8, RTX 24.5, NFLX 16.5, AMD 30.2,
  AVGO 17.8, VST 14.2, LMT 17.9, NOC 18.4). NVDA's yfinance forward P/E (10.3) looked implausible and
  was deliberately NOT used in the prose.

## Hero
`gen-focus-list-2026-11-14-hero-20261114.py` (fal flux/schnell, seed 331057, attempt 2 of 2).
1536×864, 227KB, R2 200 with matching ETag. Attempt 1 was rejected (generated a smartphone on an open
book). Attempt 2 deviates from the brief: an open book with faint illegible print texture rather than a
closed blank-cover hardcover, and the armchair/blanket are not in frame. The editorial decision was to
ship it rather than spend a third generation (cap). Caption and alt describe only what is in frame.
