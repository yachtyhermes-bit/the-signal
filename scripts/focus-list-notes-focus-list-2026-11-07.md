# Focus List — 2026-11-07 (editorial notes for human review)

Live: https://readthesignal.net/article/focus-list-2026-11-07/
Writer: google/gemini-3.8-flash, one shot, 8,617 in / 7,633 out, $0.0351. Draft kept at
`/tmp/draft-focus-list-2026-11-07.md`; brief at `/tmp/brief-focus-list-2026-11-07.md`; research at
`focus_list_research_2026-11-07.md` (repo root, not committed).

## Selection

Suggested AVGO / CEG / SOFI + one non-AI name. **CEG was substituted out**: its article JSON
(`ceg-nuclear-contract-stack-2026.json`) was written 2 November, inside the 5-day recency window.
VST, BE, RBRK, NET, IREN, APP, NVDA, AMAT, ETN, CRWV, NVTS, ANET, AMD, META, MRVL, COHR, MSFT were
all also inside that window. RTX and NFLX were last week's picks, so repeating them a week later
would read as a rerun. Final four:

| Ticker | Sector | Call |
|---|---|---|
| AVGO | ai (semis) | Accumulate |
| AMZN | mega-cap | Accumulate |
| SOFI | fintech | Accumulate |
| ZS | cyber | Wait for a better entry |

Four sectors, two beginner-recognisable names (Amazon, Broadcom). No exact prices anywhere; prose-lint
exit 0. Length 2,706 words — over the job prompt's 1,600–2,200 band, inside the skill's 2,200–3,000
long-read spec. The writer was told not to be re-edited; the only edits applied were a lint fix pass
(three sentences over 34 words, two 7-sentence paragraphs split) and five factual corrections:

1. AVGO "down from a forward multiple near 49 times" → the 49x was the TRAILING multiple at the June
   peak, not a forward one. Re-anchored to the sales multiple (15.7x now vs ~26x at the peak), which
   is the apples-to-apples comparison.
2. SOFI "effective tax rate jumped from 17% to 22%" → management's own framing is 22%, 700bp above
   the original plan (≈15%); the 17% starting point was invented by the writer.
3. AMZN "gained roughly 6% following the elections while the wider market stumbled" → 4 November was
   a broad relief rally (the Dow's best day in 19 months). Reworded to "well ahead of a broad relief
   rally".
4. AMZN "federally protected infrastructure moat" → the moat is capacity already built and permitted,
   not federal protection.
5. "first seven months of 2026" → "first half of 2026" (the bond-issuance window cited is 1 Jan–7 Jul).

## Scorecard honesty check

VST is the only prior call whose catalyst has landed. It delivered operationally (revenue +27.7% to
$6.35B, adjusted EBITDA +50% to a record $2.38B, 2026 midpoint raised to $7.1–7.5B, first 2027 range
$7.7–8.5B) and rallied more than 10% on the print — but it is still BELOW where it traded when the
31 October edition was written (Oct 30 close 138.37 → Nov 6 close 124.80, −9.8%). The piece says
exactly that rather than claiming a win. AMAT (−14.7% since the edition) makes last week's "wait for a
better entry" look right so far, but the 12 November print is the actual test and the copy says so.
RTX (−5.1%) and NFLX (+2.1%) are ungraded; no catalyst has fired.

## Things a human may want to check

- **AVGO's 9 December print shares a date with the FOMC decision.** Verified from Tan's Q3 call date
  and the published Fed calendar; flagged in the "what we're watching" line as double event risk.
- **AMZN has no near catalyst.** Q4 lands in early February and the company has not announced a date;
  the copy points at the guided holiday quarter and the 2027 capex number instead of inventing one.
- **The $30bn Broadcom guarantee figure** is attributed to Bloomberg via Quartz in the research; the
  Apollo release itself only confirms the $35bn platform. The article says Broadcom provides "credit
  endorsements and residual-value guarantees on roughly $30 billion of that debt" — if a reader
  challenges it, the sourcing is Bloomberg, not the press release.
- **ZS is the one "wait" call.** The selloff is a BofA downgrade (3 Nov) plus Fortinet's guidance cut,
  not a lost deal and not a pre-announcement (no 8-K since 6 October). The 2 December net new ARR
  number ($95–100M implied) is the entry trigger named in the piece.
- **Hero** is a FAL flux/schnell kitchen-table still life, 1536×864, md5 cb227bfa1d2769f51fcb4641aa396acf,
  R2 200 with matching ETag. OCR found no text in frame; the subagent had no vision tool, so a human
  glance is still worth it (`public/img/articles/focus-list-2026-11-07.jpg`).

## Deploy

`npm run build` → 1,535 files in dist → `npx vercel --prod --yes` from `dist/` →
https://the-signal-e2ah5pggc-beachsquadlas-projects.vercel.app ready, aliased to readthesignal.net.
Live verified: article 200, title/h1/og:image correct, four "What we're watching" blocks, disclosure
present, pre-fix strings absent, hero 200 (190,993 bytes), homepage card present.

Note: `articles/posts/ai-gpu-depreciation-accounting-explainer-2026.json` was dirty in the working
tree from another session (SpaceX wording in one paragraph + bottomLine). It shipped with this build
as-is and was NOT committed by this run.
