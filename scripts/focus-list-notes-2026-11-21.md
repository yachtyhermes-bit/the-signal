# Focus List — 2026-11-21 · review notes

Live: https://readthesignal.net/article/focus-list-2026-11-21/
Slug: `focus-list-2026-11-21` · 2,124 words (lint count) · writer cost $0.0360 (Gemini 3.8 Flash, one call, 10,450 in / 7,510 out)
prose-lint: PASS (exit 0; WARNs only — article length vs the 500-900 daily target, rhythm SD 6.8)

## Selection — departed from the suggested four

Suggested: AVGO, CEG, SOFI + one non-AI name (RTX/AMZN/NFLX). Shipped: **AVGO, GOOGL, SOFI, AXON**.

- **CEG and NFLX were last week's names** (Nov 14 edition: CEG, RTX, NFLX, AMD) — repeating them seven days later would have made the scorecard an exercise in grading ourselves twice.
- **RTX and AMD both have articles inside the 5-day exclusion window** (rtx-navy-sewip-electronic-warfare, 11/20; amd-anthropic-ipo-stake, 11/18), as do MSFT, MU, VST, NVDA, INTC, ORCL, PANW, ASML, TSM, LHX, HOOD and NBIS.
- **GOOGL added for editorial reason, not just availability:** it is the other half of the week's biggest single-stock story. Broadcom fell 12% Friday on an unconfirmed note that *Google* cut TPU orders — so pairing them lets the piece argue both sides of one fact. GOOGL had never appeared in a Focus List.
- Sectors: ai (AVGO, GOOGL semis/cloud), fintech (SOFI), defense/public-safety (AXON) = four sectors, and both GOOGL and AXON are beginner-recognisable. AVGO is a two-week repeat (last 11/07, also 10/24) — accepted because the setup inverted completely.

## Prose corrections applied after the writer call (7)

The Gemini draft was factually sound on the big numbers; these were claim-precision defects:

1. **"our four Accumulate calls"** → three Accumulates and one wait. AMD was a *Wait* last week, and it was the call that saved money. Fixed and turned into the one self-congratulation the scorecard earns.
2. Netflix "lowest level since late summer" → **since the summer of 2024** (the source said August 2024; "late summer" silently re-dated it to 2026).
3. Anthropic "dropped below its first-day price" → **gave back most of its first-day gain**. It closed at $88.91 vs a $97.17 first-day close — still above the $83 IPO price; the original wording could be read as below IPO.
4. SoFi "adjusted cash earnings" → **adjusted EBITDA** ($469.8M, 34% margin). The label the writer invented implies a cash figure the release does not report.
5. Axon: Dedrone delays were "government budget freezes" → **pushed out amid federal funding and election cycles** (management's own framing); memory "pushed" margins to 59.2% → memory added ~50bp, **margins fell** to 59.2% (mix did the rest).
6. Axon "older weapon sales contracted 2%" → **TASER revenue, the franchise product, fell about 2%**. "Older weapons" undersold that this is the flagship line.
7. Skydio "$1.2 billion in cash" → **$1.2B for a 37% stake, now settling about 90% in cash** (the 8-K conversion on 13 Nov; the original announcement was ~60% stock).
8. Subtitle "marked down … to their yearly lows" → **to the bottom of their yearly ranges** (AVGO is 7% into its range, not at the low).
9. Two prose-lint HARD FAILs (35- and 47-word sentences) split — the second was the bottom-line parallel recap, now four short parallel sentences.

## Unverified / flagged in the piece

- **The Google TPU 8i cut is a third-party channel check** (Ming-Chi Kuo, TF International, 20 Nov). Neither Google nor Broadcom has confirmed it. The article names the report and says "unconfirmed"/"supply-chain reports" — never states it as fact. This is the single biggest factual exposure in the edition; if Broadcom's 9 Dec call contradicts it, the AVGO "wait" call looks smart and the framing still stands.
- **Q4 earnings dates for GOOGL, SOFI and AXON are not company-announced.** The article says "first week of February", "late January" and "in February" respectively — no specific dates. Do not add dates later without a company announcement.
- Menlo Ventures enterprise-API-share figure (Google 21%→9%) is one survey of ~400 buyers; the article does not use it (kept out of the final prose).

## Editorial judgment calls worth a human eye

- **Two "Wait" calls and two "Accumulate"** — AVGO and AXON get Wait because their next real information is 18 days and 3 months away respectively. If you would rather the weekly long read lean constructive, AVGO is the one to flip: 15.7x forward with $179.2B RPO is defensible as an accumulate.
- **The scorecard admits 3.6 points of underperformance** (equal-weight −12.2% vs S&P −8.6%). Deliberate: the format's credibility rests on grading, not defending.
- **Hero image not visually inspected.** The generator subagent had no vision tool; tesseract OCR returned zero characters (consistent with no text, not proof). FAL generated once (1 of 2 allowed). File: 1,200×675, 238,935 bytes, md5 97e2af6eba9c7103f01603b4c3d21494, R2 200 with matching ETag, mirrored to `_backup_dist`. If a human wants to eyeball it, that is the one outstanding check.
- Homepage: the build promoted the piece into the FEATURED hero slot (newest article). `featured: false` was left as-is, consistent with prior editions.

## Committed

`2c6d7c4d` — articles/posts/focus-list-2026-11-21.json + public/img/articles/… + _backup_dist/img/articles/… (JSON and both image copies together, pitfall 82). Pushed to main as a fast-forward.
