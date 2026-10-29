KLA CORPORATION (NASDAQ: KLAC) — VERIFIED RESEARCH BRIEF
For The Signal / readthesignal.net
Prepared: Sunday, October 25, 2026 (markets closed; last completed session Fri Oct 23, 2026)
Angle: supply-versus-demand constraint, and the Oct 28 fiscal Q1 2027 print as the test.
Prior Signal KLA article (2026-09-16, "KLA Inspects Every AI Chip. The Market Prices It Like a Machinery
Stock.") is explicitly NOT restated here. Every figure below was pulled fresh this session; the old
data/kla-research.txt was used only as a lead list and every number in it was re-verified or replaced.

PROPOSED SLUG: kla-process-control-supply-test-2026
  (uniqueness note at the bottom — a hero image and generator script for exactly this slug already exist
  in the repo as of 2026-10-25 16:04, so this is the slug the asset pipeline is already built against)

================================================================================
0. HEADLINE: DOES THE FRAMING SURVIVE CONTACT WITH THE NUMBERS?
================================================================================
VERDICT: HALF. The "supply, not demand" reading is directly supported by primary-source management
commentary at both Lam and KLA, by a $12.5B KLA backlog, and by lead times of 12–24 months on the specific
component that gates KLA's output (optical assemblies). It is NOT supported by KLA's revenue relative to
WFE, which has been flat, not rising — an analyst put that exact question to KLA's CFO on the July call and
the CFO answered with lead times, not with intensity (see §10-B, the single most important item in this file).

So: the supply constraint is real and documentable. The stronger claim — that process control intensity is
compounding faster than WFE, and that KLA therefore deserves a premium through the cycle — is NOT currently
visible in KLA's own numbers. That gap is the article. The Oct 28 print tests the weak link (can KLA convert
a $12.5B backlog and 12-month lead times into a >$4.0B quarter at 62.5% gross margin), not the strong one.

================================================================================
1. BUSINESS, IN PLAIN ENGLISH
================================================================================
VERIFIED. KLA sells the quality-control layer of a chip fab. Every time a fab adds a layer to a wafer, it has
to check whether the layer is the right thickness, whether it landed in the right place, and whether a speck
of dust killed a die. KLA makes the machines that do that checking (inspection), the machines that measure the
result (metrology), and the software and service contracts that keep them running. It also sells process-
enabling tools (etch, deposition, thermal) into specialty markets, and inspection gear for printed circuit
boards and chip packages.

Company's own description, verbatim: "KLA Corporation ('KLA') develops industry-leading equipment and services
that enable innovation throughout the electronics industry. We provide advanced process control and process-
enabling solutions for manufacturing wafers and reticles, integrated circuits, packaging and printed circuit
boards."
  SOURCE (2026-07-28): https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html

Three reportable segments: Semiconductor Process Control; Specialty Semiconductor Process; PCB and Component
Inspection. 17,000 employees. Fiscal year ends June 30. Milpitas, California.
  SOURCE: yfinance `info` pull 2026-10-25 (fullTimeEmployees 17000); segment names from Q4 FY26 release above.

VERIFIED — what it actually sells, by product line, June 2026 quarter (KLA's own shareholder letter, as
tabulated by CSET): Wafer inspection 49% / Services 22% / Patterning 20% / PCB and component inspection 4% /
Specialty semiconductor process 4% / Other 1%.
  SOURCE: https://chipsupplychain.org/metrology-and-inspection/ (CSET, citing "KLA letter to shareholders, Q4 FY2026")

================================================================================
2. PRICE AND VALUATION
================================================================================
VERIFIED — last close Friday, October 23, 2026: KLAC $145.61, −$2.22 (−1.50%) on the day.
  METHOD: yfinance history, explicit window 2026-10-01..2026-10-26, auto_adjust=False (raw closes, no
  dividend adjustment). Cross-checked: stockanalysis.com shows $145.61 "At close: Oct 23, 2026, 4:00 PM EDT"
  and after-hours $146.20.
  SOURCE: https://stockanalysis.com/stocks/KLAC/statistics/ (last checked Oct 20, 2026 per page footer;
  price line is live) — and my own yfinance pull, saved at /home/chino/thesignal/tmp/kla_yf_2026-10-25.txt

VERIFIED — WEEKLY MOVES, Fri Oct 16 close → Fri Oct 23 close (both auto_adjust=False):
  LRCX   $263.94 → $230.10   −12.82%   (−$33.84)
  KLAC   $165.74 → $145.61   −12.15%   (−$20.13)
  ONTO   $220.70 → $198.68    −9.98%   (−$22.02)
  AMAT   $409.29 → $377.24    −7.83%   (−$32.05)
  ASML $1,641.52 → $1,571.80   −4.25%   (−$69.72)
  ^SOX  11,137.29 → 10,779.46  −3.21%   (−357.83)
  SOXX   $493.39 → $478.20    −3.08%   (−$15.19)
  NVDA   $214.13 → $210.96    −1.48%   (−$3.17)
  ^IXIC 26,140.03 → 25,955.34  −0.71%
  NOTE: this confirms the brief's numbers. KLAC −12.1%, LRCX −12.8%, AMAT −7.8%, SOXX −3.1%, KLAC $145.61
  all check out exactly.
  METHOD/SOURCE: yfinance daily history per ticker, same script, same window. Reproducible.

VERIFIED — the Thursday Oct 22 single session was the whole move:
  KLAC $163.43 → $147.83 = −9.55% on 20,740,700 shares (about 2× its average)
  LRCX $260.81 → $230.15 = −11.76%
  AMAT $408.94 → $375.58 = −8.16%
  (Sell-side roundups put AMAT at "−7%" that day; my computed close-to-close is −8.16%. Use the computed one
  or say "about 8%".)
  SOURCE: yfinance; corroborated on KLAC's −9.55% / $147.83 / 20.58M shares by
  https://seekingalpha.com/news/4656277-kla-corporation-falls-10-percent-amid-broader-semiconductor-selloff (Oct 22, 2026)

VERIFIED — 52-week range: LOW $107.20 · HIGH $307.37
  yfinance history (2025-10-25..2026-10-26): max high $307.37 on 2026-06-30; min low $107.196 on 2025-11-21.
  Independent cross-check: stockanalysis.com "52-Week Range 107.20 - 307.37".
  SOURCE: https://stockanalysis.com/stocks/KLAC/statistics/ ; yfinance pull as above.
  => At $145.61 KLAC is 52.63% BELOW its 52-week high and 35.84% ABOVE its 52-week low.
  => 52-week price change still +30.67% (stockanalysis). This is a stock that round-tripped, not one that
     never worked: $107 (Nov 2025) → $307.37 (June 30, 2026) → $145.61.
  CAUTION: an older research file cited a $97.63 52-week low. That was a window-boundary artefact; the low
  is now $107.20 because Sept 2025 has rolled out of the window. The true cycle low was $83.22 intraday on
  2025-09-03. Do not use $97.63.

VERIFIED — market cap $190.02B; enterprise value $191.27B; shares outstanding 1.31B (1,305,006,492).
  SOURCE: https://stockanalysis.com/stocks/KLAC/statistics/ (Oct 2026); yfinance `info` agrees
  (marketCap 190,021,992,448; sharesOutstanding 1,305,006,492).

VERIFIED — valuation multiples (all at $145.61):
  Trailing P/E            39.78x   (on FY26 GAAP EPS $3.66)
  Forward P/E (FY27E)     26.65x   (on FY27 consensus EPS $5.46, non-GAAP)
  Forward P/E (FY28E)     21.6x    (on FY28 consensus EPS $6.74)
  P/S (TTM)               13.99x
  EV/Sales                14.09x
  EV/EBITDA               31.59x
  EV/FCF                  50.77x
  P/B                     29.97x   (book value $4.86/sh)
  SOURCE: https://stockanalysis.com/stocks/KLAC/statistics/ ; https://stockanalysis.com/stocks/KLAC/forecast/
  TRAP: yfinance's `forwardPE` field reads 21.60x because yfinance's `forwardEps` is $6.74039 — that is the
  FY2028 number, not next-twelve-months. The correct next-fiscal-year forward P/E is 26.65x. Do not print
  21.6x as "forward P/E" without saying which year.

VERIFIED — dividend: $0.23/quarter, $0.92 annualized, yield 0.63% at $145.61; ex-div Aug 17, 2026.
  KLA raised the quarterly dividend 21% to $2.30/share pre-split ($0.23 post-split) effective with the
  May 2026 declaration, and added $7.0B to the buyback authorization (on top of $3.3B remaining = $10.3B
  total authorized as of 3/31/2026).
  SOURCES: https://stockanalysis.com/stocks/KLAC/statistics/ ; the $7.0B/$3.3B figure is footnote 3 of KLA's
  Q3 FY26 earnings deck, p. ~"Consistent Returns to Shareholders":
  https://static.seekingalpha.com/uploads/sa_presentations/647/126647/original.pdf

VERIFIED — Street: 30 analysts, consensus "Buy," average target $232.38 (+59.59%), median $228.50, low $175
(+20.18%), high $325 (+123.20%). Distribution October 2026: 15 Strong Buy / 5 Buy / 10 Hold / 0 Sell.
  SOURCE: https://stockanalysis.com/stocks/KLAC/forecast/ (data via S&P Global / TipRanks, last updated Oct 20, 2026)
  THE NUMBER THAT MATTERS: $232.38 ÷ $5.46 FY27E EPS = 42.6x. The consensus target is a multiple call, not an
  earnings call. See §12-5.

VERIFIED — recent analyst actions (most recent first):
  Oct 20, 2026  UBS (Timothy Arcuri)      Hold, PT $200 → $190
  Oct 6, 2026   Morgan Stanley (Shane Brett) Buy/OW, PT $253 → $227
  Sep 22, 2026  Bernstein (David Dai)     Buy, PT $250 maintained
  Sep 12, 2026  Susquehanna (Mehdi Hosseini) Hold, no PT
  Sep 9, 2026   Berenberg                  Buy, PT $230
  Jul 30, 2026  TD Cowen                   Buy, PT $260
  Jul 30, 2026  Barclays                   OW, PT $225
  Jul 29, 2026  Cantor Fitzgerald          Buy, PT $325
  SOURCE: https://stockanalysis.com/stocks/KLAC/forecast/ and https://stockanalysis.com/stocks/klac/ratings/

================================================================================
3. REVENUE AND SEGMENT MIX
================================================================================
VERIFIED — FY2026 (twelve months ended June 30, 2026), from the company's own Segment Information table:
  Semiconductor Process Control        $12,244,733K   = $12.245B   90.2% of total
  Specialty Semiconductor Process         $584,064K   =  $0.584B    4.3%
  PCB and Component Inspection            $750,415K   =  $0.750B    5.5%
  Total reportable segments            $13,579,212K
  Effects of FX                               $264K
  Total revenues                       $13,579,476K   = $13.579B
  FY25 comparatives: SPC $10,947,359K; Specialty $587,107K; PCB $621,721K; total $12,156,162K.
  => FY26 total revenue +11.71% y/y. SPC +11.9%. Specialty −0.5% (it shrank). PCB +20.7%.
  SOURCE (2026-07-28): https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html

VERIFIED — Q4 FY2026 (June quarter, reported July 28, 2026):
  Total revenue      $3,657,556K = $3.658B   (+7.10% q/q, +15.21% y/y)
  Semiconductor Process Control  $3,256,781K
  Specialty Semiconductor Process  $159,704K
  PCB and Component Inspection     $241,110K
  SOURCE: same release.

VERIFIED — systems vs services (this is the "product vs service" line):
  FY2026   Product $10,453,537K (77.0%)   Service $3,125,939K (23.0%)
  FY2025   Product $9,472,854K  (77.9%)   Service $2,683,308K (22.1%)
  Q4 FY26  Product $2,837,151K            Service $820,405K  (+16.8% y/y)
  => Services grew +16.5% in FY26, faster than the company. Service is ~80% contract-based per management,
     which is the counter-cyclical ballast in the model.
  SOURCE: same release (Condensed Consolidated Statements of Operations). The "80% contract-based" line is
  management commentary: "Service delivered $820 million revenue in [Q4], up 17% year-over-year... 80% of
  revenue is contract-based."
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

VERIFIED — five-year revenue arc (shows the cyclicality, and the size of what is now being forecast):
  FY2022 $9.21B → FY2023 $10.50B → FY2024 $9.81B → FY2025 $12.16B → FY2026 $13.58B
  FY2024 was a DOWN year: −6.52%.
  SOURCE: https://stockanalysis.com/stocks/KLAC/forecast/ (financial forecast table); FY24 figure also
  reproducible from yfinance annual income statement ($9,812,247K).

================================================================================
4. MARGINS
================================================================================
VERIFIED — computed by me from the company's own income statement (dollars in thousands), not from a data
vendor's ratio field:
  FY2026  Gross margin      61.30%   ($8,324,416 / $13,579,476)
  FY2026  Operating margin  41.69%   ($5,660,780 / $13,579,476)
  FY2026  Net margin        35.57%   ($4,830,771 / $13,579,476)
  Q4 FY26 Gross margin      61.36%   ($2,244,448 / $3,657,556)
  Q4 FY26 Operating margin  42.49%   ($1,553,948 / $3,657,556)
  SOURCE: figures from https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html ; arithmetic mine.

VERIFIED — Q4 FY26 non-GAAP gross margin was 62.4%, at the upper end of guidance, "driven by a more
favorable services mix than model and manufacturing scale that served as positive offsets to the challenging
memory pricing environment and tariff headwinds."
  SOURCE: https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

VERIFIED — Q1 FY2027 guidance midpoint is a STEP UP in margin, and that is unusual and important:
  GAAP gross margin     61.6% ± 1.0%   (vs 61.36% actual in Q4 — essentially flat)
  Non-GAAP gross margin 62.5% ± 1.0%   (up ~75bp from the prior guide)
  SOURCE (2026-07-28): Q4 FY26 press release, "First Quarter Fiscal 2027 Guidance," verbatim.

VERIFIED — two documented margin headwinds, both quantified by management:
  (a) Memory/DRAM component cost inflation: "we've been having to procure new memory at higher prices. Over
      the last couple of quarters or so, we thought the impact was somewhere around 100 basis points."
      Earnings Whispers (Oct 20, 2026) reports management now frames it as "slightly more than 100 basis
      points and was described as lasting through 2027."
  (b) Tariffs: "roughly 50 to 100 basis points of the impact" on gross margin, "more or less consistent
      quarter to quarter" (Q1 FY26 call, Oct 2025).
  SOURCES: https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/ (100bp memory);
  https://www.fool.com/earnings/call-transcripts/2025/10/30/kla-klac-q1-2026-earnings-call-transcript/
  (tariff 50–100bp); https://finviz.com/news/405234/kla-must-prove-its-fourth-wfe-upgrade-stuck-as-stock-sinks-toward-lows (Oct 20, 2026)

================================================================================
5. FREE CASH FLOW AND CAPITAL RETURNS
================================================================================
VERIFIED — computed by me, four-quarter sum, then reconciled to the company's own statement:
  OCF    Q4FY26 $906,430K + Q3 $707,451K + Q2 $1,367,607K + Q1 $1,161,591K = $4,143,079K = $4.143B
  Capex  Q4 −$89,288K + Q3 −$85,187K + Q2 −$105,576K + Q1 −$95,894K       = −$375,945K = −$0.376B
     (NOTE: yfinance capex rows are NEGATIVE. FCF = OCF + capex, i.e. OCF minus the absolute capex.)
  TTM FCF = $3,767,134K = $3.767B
  Company's own words confirm it: "Cash flow from operating activities for the quarter and fiscal year was
  $906.4 million and $4.14 billion, respectively, and free cash flow was $817.1 million and $3.77 billion,
  respectively."
  => FCF margin 27.74% of revenue. FCF conversion (FCF/net income) 78%.
  SOURCE: https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html

VERIFIED — FCF history: FY2026 $3.767B · FY2025 $3.747B · FY2024 $3.031B. Capex is tiny for a company this
size ($376M in FY26) — KLA outsources most manufacturing, which is why FCF tracks net income closely.
  SOURCE: yfinance annual cash flow statement, pulled 2026-10-25.

VERIFIED — capital returns FY2026: $3.35B total, = 88.9% of FCF.
  Components from the cash flow statement: buybacks $2,289,769K + dividends $1,057,832K = $3,347,601K.
  Q4 alone: $876.3M ($571M buybacks + $305M dividends).
  Long-term commitment: "Committed to long-term > 90% FCF returned to shareholders through dividends and
  share repurchases" (KLA Q3 FY26 deck).
  SOURCES: press release above; deck at
  https://static.seekingalpha.com/uploads/sa_presentations/647/126647/original.pdf

================================================================================
6. BALANCE SHEET — CASH, DEBT, NET CASH
================================================================================
VERIFIED — June 30, 2026 balance sheet, company's own numbers (in thousands):
  Cash and cash equivalents                $1,649,842
  Marketable securities                    $3,252,566
  => Cash + marketable securities          $4,902,408  = $4.90B
  Long-term debt                           $5,887,415  = $5.89B   (no short-term debt line on the balance sheet)
  Total assets                            $17,951,535
  Stockholders' equity                     $6,349,820
  SOURCE: https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html
  Company's own summary on the call: "KLA ended the quarter with $4.9 billion in total cash equivalents, and
  marketable securities, and $5.9 billion of debt... supported by investment-grade ratings from all three
  major rating agencies."
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

NET CASH — TWO DEFENSIBLE ANSWERS, PICK ONE AND SAY WHICH:
  (a) Company-basis (cash+securities $4.902B − LT debt $5.887B)  = NET DEBT of $0.99B
  (b) stockanalysis.com (total debt $6.15B, which includes lease obligations, − cash $4.90B) = NET DEBT $1.25B
  TRAP: yfinance's `netDebt` field says $4.238B. That is total debt minus CASH ONLY ($1.65B), ignoring the
  $3.25B of marketable securities. It is wrong by ~$3B. Do not print it.
  SOURCES: balance sheet above; https://stockanalysis.com/stocks/KLAC/statistics/ ("net cash position of
  -$1.25 billion or -$0.96 per share")

VERIFIED — working capital is being built, which is the balance-sheet fingerprint of the supply-ramp story:
  Accounts receivable $2,889,208 (from $2,263,915 a year earlier, +27.6%)
  Inventories         $3,648,538 (from $3,212,149, +13.6%)
  Q4 change in receivables −$586,459K and change in inventory −$212,304K, which is why Q4 OCF fell to $906M
  from $1,368M in the December quarter despite revenue rising.
  SOURCE: press release balance sheet + yfinance quarterly cash flow.

================================================================================
7. CHINA EXPOSURE
================================================================================
VERIFIED — China was 26% of KLA revenue in the June 2026 quarter. Taiwan was the largest region at 31%.
Full Q4 FY26 geographic mix: Taiwan 31% · China 26% · North America 18% · Korea 10% · Japan/Europe/rest of
Asia 15%.
  SOURCES: (1) CSET: "In that quarter Taiwan took 31 percent of KLA's revenue and China 26 percent."
  https://chipsupplychain.org/metrology-and-inspection/
  (2) Morgan Stanley note coverage, Oct 6, 2026: "KLA's revenue from China also grew by approximately $130
  million quarter-over-quarter, accounting for roughly 26% of its total revenue exposure."
  https://www.investing.com/news/analyst-ratings/morgan-stanley-cuts-kla-stock-price-target-on-valuation-concerns-93CH-4934052
  (403 to curl = bot-blocked; live in browser)
  (3) Investing.com's read of KLA's own Q4 slide deck: "Taiwan remained KLA's largest market at 31% of
  revenue, followed by China at 26% and North America at 18%. Korea contributed 10%, while Japan, Europe, and
  the rest of Asia combined for 15% of sales."
  https://www.investing.com/news/company-news/kla-q4-fy2026-slides-record-revenue-but-shares-fall-on-margin-mix-93CH-4818307

VERIFIED — the trajectory, which is the whole point: China was 39% of revenue in the September 2025 quarter,
came down to 26% by June 2026, and management told investors in October 2025 to model "mid-20s percent" for
calendar 2026.
  Verbatim (Bren Higgins, Q1 FY26 call, Oct 2025): "China was elevated in September at 39%... as we look at
  CY2026, I think it likely comes down into the mid-20s percent... some of that is driven by the export
  restrictions, but also some general normalization that we've been talking about."
  https://www.fool.com/earnings/call-transcripts/2025/10/30/kla-klac-q1-2026-earnings-call-transcript/

VERIFIED — the export-control number KLA has been carrying: $300M–$350M of lost revenue through the end of
calendar 2026, spread roughly evenly across the two halves, from "additional market access loss related to
certain customers in China resulting from extended export controls from the U.S. Government."
  SOURCE (Oct 2025): https://www.reuters.com/world/asia-pacific/kla-forecasts-upbeat-second-quarter-revenue-china-weakness-persists-2025-10-29/
  ATTRIBUTION RULE: this is an October 2025 disclosure about CY2026. No later KLA update revising the number
  was found. Write "management estimated in October 2025."

VERIFIED — what the Street has modeled for the quarter being reported Wednesday: China revenue $1.00B,
−20.7% year over year, = ~24.7% of the $4.05B consensus. Taiwan $1.15B (+44.3%), Korea $683.67M (+128.4%),
North America $522.77M (+75.5%), Japan $341.37M, Europe & Israel $180.94M, Rest of Asia $140.74M.
  SOURCE: Zacks, Oct 23, 2026, "Insights Into KLA (KLAC) Q1: Wall Street Projections for Key Metrics"
  https://finance.yahoo.com/markets/stocks/articles/insights-kla-klac-q1-wall-121505565.html
  (These seven lines sum to ~$4.02B, consistent with the $4.05B total. Good internal check.)

VERIFIED — the live regulatory catalyst, 12 days after the print: BIS's "Affiliates Rule" (the 50%-ownership
rule) snaps back on November 10, 2026.
  Primary source, verbatim: "The suspension is set to end November 9, 2026, absent a future extension...
  Accordingly, the provisions that this final rule removes from the EAR on November 10, 2025... will be
  reimposed on November 10, 2026."
  https://www.federalregister.gov/documents/2025/11/12/2025-19846/one-year-suspension-of-expansion-of-end-user-controls-for-affiliates-of-certain-listed-entities
  Complication: Treasury Secretary Bessent announced Sept 23–24, 2026 that the US–China truce was extended
  to January 10, 2027, but BIS had not published a Federal Register notice changing the date. Treat Nov 10,
  2026 as operative. https://www.mondaq.com/unitedstates/export-controls-trade-investment-sanctions/1854664/us-china-trade-truce-extended-two-months-bis-affiliates-rule-suspension-follows
  WHY IT MATTERS: the rule extends Entity List restrictions to any company ≥50%-owned by a listed entity.
  For a toolmaker, that widens the restricted-buyer set without anyone new being named. This is a KLA/LRCX/
  AMAT-wide exposure, not a KLA-specific one, and it lands 13 days after earnings.

================================================================================
8. COMPETITIVE POSITION AND MARKET SHARE
================================================================================
VERIFIED — KLA holds ~57% of the process-control (metrology + inspection) market. The most current
independent count: 56.8% in 2025, from CSET (Georgetown) using TechInsights data. Full 2025 share table:
  KLA 56.8% · Applied Materials 11.2% · Lasertec 6.4% · Hitachi High-Tech 6.2% · ASML 5.9% · Nova 4.3% ·
  Onto Innovation 2.6% · Camtek 1.6% · Rigaku 1.2% · all others 3.8%
  SOURCE: https://chipsupplychain.org/metrology-and-inspection/ (CSET, "ETO Supply Chain Explorer")
  NOTE: this CORRECTS the "roughly 50–56%" in the assignment brief. The number is ~57%, and KLA's own
  materials put it at 58%. Chinese suppliers collectively held 0.7% of the market in 2025.

VERIFIED — KLA's own claim, from its Q3 FY26 earnings deck, verbatim: "58% — 2025 Process Control Share.
Process Control share rose 360bps from 2021. Gains in Optical Inspection, E-beam, Advanced Wafer Level
Packaging, and Mask Inspection. Achieved #1 share position in Advanced Wafer Level Packaging Process Control.
Source: Gartner April 2026."
  SOURCE: https://static.seekingalpha.com/uploads/sa_presentations/647/126647/original.pdf (KLA Q3 FY2026
  earnings presentation; the PDF is hosted by Seeking Alpha, the content is KLA's own slide)
  Also: at its March 2026 investor day KLA cited Gartner for 2024: 56.5% share, 6.5x its nearest competitor.

VERIFIED — where the moat is thick and where it is thin (2025, CSET/TechInsights, by tool family):
  Defect inspection      $6.70B market   KLA 85.9%     <- the fortress
  Film & shape metrology $2.60B          KLA 45.6%  (Nova 24.6%, Onto 10.9%)
  Mask inspection/repair $2.20B          KLA 45.9%  (Lasertec 42.0%, Zeiss 10.1%)  <- the real fight
  E-beam metrology       $1.30B          KLA 18.8%  (AMAT 45.1%, ASML 35.6%)       <- KLA is third
  CD metrology           $1.20B          KLA —      (Hitachi 71.9%, AMAT 27.5%)
  Overlay metrology      $0.99B          KLA 51.5%  (ASML 47.9%)
  SOURCE: https://chipsupplychain.org/metrology-and-inspection/
  PROCESS CONTROL TOTAL MARKET: $15.7B in 2025, by CSET's count. KLA's Semiconductor Process Control segment
  did $12.245B in FY26 — the two numbers are not directly comparable because the segment includes services
  and specialty process control. Do not divide one by the other on the page.

VERIFIED — competition is real and quantifiable:
  * Applied Materials is "increasingly challenging KLA in process diagnostics and control," and expects that
    business to grow "more than 50% in 2026." AMAT leads e-beam metrology at 45.1%.
  * Onto Innovation raised its 2026 advanced-packaging growth outlook to ~80% (from 50%) and "secured more
    than $200 million of Dragonfly orders from a single OSAT, with most shipments scheduled for 2027."
  * Lasertec holds 42% of mask inspection vs KLA's 45.9%, and owns actinic (EUV-light) mask inspection; KLA's
    own actinic tool "was still at an early demo stage at its March 2026 investor day."
  SOURCES: https://finance.yahoo.com/markets/stocks/articles/kla-gains-advanced-packaging-outpace-173800680.html
  (Zacks, Aug 26, 2026) ; https://chipsupplychain.org/metrology-and-inspection/ (actinic detail)

VERIFIED — KLA's own explanation of why process control is hard to enter (good quote, use it):
  "Process control is tricky to get into because it's a very high-mix, low-volume market. Unlike litho,
  frankly, is much higher kind of similar tool, higher volume. Process control, there's a lot of nuance...
  Add to that the 1,600, 1,700 applications engineers that KLA has worldwide, and it's a pretty good
  competitive moat that we've established over time."
  — Rick Wallace, CEO, Q4 FY26 call
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

================================================================================
9. THE OCT 28 FISCAL Q1 2027 SETUP
================================================================================
VERIFIED — DATE. Wednesday, October 28, 2026, results after the close, call at 2:00 p.m. PT (5:00 p.m. ET).
Company's own words: "the company will review first quarter fiscal year 2027 earnings on Wednesday, October
28th at 2 p.m. PT. The company's results will be published on the same day after the stock market closes."
  SOURCE (announced Oct 1, 2026): https://ir.kla.com/news-events/press-releases/detail/522/kla-announces-first-quarter-fiscal-year-2027-earnings-date
  NOTE the same Wednesday also carries the FOMC decision at 2:00 p.m. ET and Alphabet/Microsoft after the
  close. KLA's print lands in the busiest 90 minutes of the quarter. If the reaction looks odd, that's why.

VERIFIED — CONSENSUS (two independent sources agree):
  yfinance calendar:  EPS average $1.17822 (range $1.15–$1.25)
                      Revenue average $4,038,185,350 (range $3,967,000,000–$4,219,111,000)
  Zacks (Oct 23):     EPS $1.18, +34.1% y/y · Revenue $4.05B, +26.1% y/y
  Whisper number:     $1.22
  SOURCES: yfinance `calendar` pulled 2026-10-25; https://finance.yahoo.com/markets/stocks/articles/insights-kla-klac-q1-wall-121505565.html ;
  whisper from https://finviz.com/news/405234/kla-must-prove-its-fourth-wfe-upgrade-stuck-as-stock-sinks-toward-lows (Oct 20, 2026)

VERIFIED — GUIDANCE (what KLA told you to expect on July 28):
  Revenue              $4.0B ± $200M      ($3.80B–$4.20B)
  GAAP gross margin    61.6% ± 1.0%
  Non-GAAP gross mg    62.5% ± 1.0%
  GAAP diluted EPS     $1.14 ± $0.10
  Non-GAAP diluted EPS $1.16 ± $0.10     (on ~1.312B diluted shares)
  SOURCE: https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html

THE SETUP IN ONE SENTENCE: consensus sits ABOVE the guidance midpoint on both lines ($1.178 vs $1.16; $4.04B
vs $4.00B). So a "beat" that merely clears the midpoint is not a beat. The stock needs the top end or better.

VERIFIED — what the December-quarter bar looks like (this is the real event, not the September quarter):
  Management said 2H calendar 2026 revenue would run ~20% above 1H. Calendar 1H26 was ~$7.1B (Mar-26 quarter
  $3.415B + Jun-26 quarter $3.658B = $7.073B — verified from the quarterly statements in §3). Earnings Whispers does
  the arithmetic: "that math points to a December quarter of around $4.5 billion if September lands near
  $4.0 billion."
  Consensus for the December quarter is $4.495B (Hudson Labs), then $4.683B (Mar-27) and $4.911B (Jun-27).
  SOURCES: https://finviz.com/news/405234/kla-must-prove-its-fourth-wfe-upgrade-stuck-as-stock-sinks-toward-lows ;
  https://www.hudson-labs.com/research/kla-q1-2027-earnings-preview-klac-revenue-preview
  => A December guide of $4.4–4.6B confirms the ramp. A guide of $4.2–4.3B says supply is binding — or that
     the 2H hockey stick slipped. Those two explanations are not distinguishable from the number alone, which
     is exactly why the call commentary matters more than the print.

VERIFIED — what the Street expects inside the quarter (segment line items, Zacks consensus):
  Semiconductor Process Control  $3.63B  (+25.4% y/y)
  Product                        $3.16B  (+28.2% y/y)
  Service                         $853.57M (+14.6% y/y)
  Specialty Semiconductor Process $173.38M (+44.8% y/y)
  PCB and Component Inspection     $207.11M (+9.3% y/y)
  SOURCE: https://finance.yahoo.com/markets/stocks/articles/insights-kla-klac-q1-wall-121505565.html

VERIFIED — the four things to watch, in order:
  1. December guide vs ~$4.5B.
  2. Non-GAAP gross margin vs 62.5%, with >100bp of memory cost and 50–100bp of tariff drag already known.
  3. Whether the ~$12.5B backlog (RPO) grew again — KLA stopped reporting it quarterly, so this may only come
     out in Q&A. See §10.
  4. Advanced packaging process control: ~$1.1B for CY2026, +70% y/y. The target has been raised three times;
     a fourth raise, or a slip, is the cleanest read on AI-driven inspection demand.

================================================================================
10. THE ACTUAL QUESTION: SUPPLY, OR DEMAND IN A COSTUME?
================================================================================
10-A. EVIDENCE THAT THE CONSTRAINT IS SUPPLY — all primary, all quotable.

  KLA's lead times (Bren Higgins, CFO, Q4 FY26 call, verbatim): "Lead times today across the whole company are
  in about the 12-month range. On certain products, it can be closer to 18 to 24 months. All our conversations
  today with customers are about deliveries really in the second half of 2027. We're starting to move in that
  direction around some of the larger products in this company."
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

  The named bottleneck: optical components, and specifically the time to add capacity for them.
  Higgins, verbatim: "we've spent a lot of time on the last few months is meeting with some of our critical
  suppliers and planning and doing capacity agreements for our needs, we believe in the 2029 and beyond
  time-frame. That gives you a sense of how we have to think about planning to drive the capacity requirements
  for optical components... it can take 12 to 24 months to put New capacity in place for those types of
  components."
  Zacks adds the specific part: "calcium fluoride optical components can have lead times of 18–24 months or
  longer, potentially limiting production flexibility."
  https://finance.yahoo.com/markets/stocks/articles/klac-stock-portfolio-pre-q1-131200205.html

  KLA says the revenue acceleration IS the supply arriving, verbatim: "Our expectations of revenue growth
  acceleration in the second half of 2026 are materializing as more capacity comes online in our long lead
  time supply chain areas."
  And: "Given how quickly the industry turned and started to ramp, we did... deal with some supply chain
  shortages as it relates to some of our longer lead time materials and how that's impacted the first half.
  Certainly, in the second half, we're seeing that supply come on, and we're seeing in the second half
  acceleration, as we talked about, 20% over the first half."

  The backlog is the receipt for unmet demand, verbatim: "We'd expect that the RPO, or backlog, would be about
  $12.5 billion. We've seen that grow pretty consistently over the last couple of quarters and would expect
  that given the order funnel, that we'll see that continue to grow."
  = $12.5B against FY26 revenue of $13.58B, i.e. ~11 months of revenue already ordered.
  (Also reported as ~$12.57B at FY26-end by Zacks, and "up 60% YoY" by Hudson Labs — secondary, consistent.)

  Lam's CFO, same week, same words (Doug Bettinger, Oct 21, 2026, verbatim): "We are expecting revenue of
  $8.6 billion ± $400 million. I would mention that this revenue guide would have been a bit higher if not for
  some near-term supply chain constraints that we are actively managing."
  And on where it goes: "to the extent that it is something we would have shipped in December, because of
  timing, we will ship that in the March quarter."
  And, killing the "one-off" explanation: "there is nothing unique or one-off or episodic, to use your word,
  in the December quarter. It is just consistent with customer demand, frankly... it would have been a little
  bit higher if not for some of these supply chain constraints."
  https://stockanalysis.com/stocks/LRCX/transcripts/718719-q1-2027/

  Lam's CEO on the size of the demand, verbatim: "For calendar year 2026, we expect WFE in the mid $150
  billion range. Our preliminary 2027 WFE outlook is for more than $200 billion of spending, with percentage
  growth led by DRAM, followed by leading-edge foundry logic and NAND. As we move into calendar year 2027, we
  see clean room space availability and supply chain constraints for certain components continuing to limit
  chip makers and equipment companies' ability to fully meet end demand."
  And on duration: "we believe the industry is in the early stages of a multi-year investment cycle, with
  customer visibility extending through 2028."
  And the physical count: "we see 10 new tier I fabs coming online between the beginning of the year and the
  end of the year... This year has been primarily clean room constrained." (Bettinger)

  KLA's own WFE numbers, verbatim (Higgins): "We're raising our expectation for the wafer equipment market,
  including advanced packaging, to approximately the low $150 billion range in calendar 2026, up from our prior
  expectation of $140 billion-plus and mid-20% growth above the approximate $120 billion level in calendar
  2025." And on 2027: "more or less you're in and around $190 billion or so translates into a mid-20 type
  growth rate, which is similar to the growth rate in 2026."

10-B. THE ONE PIECE OF EVIDENCE THAT CUTS AGAINST THE FRAMING — put this in the article.
  On the July 28 call, TD Cowen's Krish Sankar asked the CFO the exact question the article is asking, and got
  an answer that does not refute it. Verbatim:
    ANALYST: "When I look at your revenues over the quarter, it seems like your revenue as a percentage of WFE
    is pretty consistent through the year. I'm just wondering why. If process control intensity is increasing,
    shouldn't your revenue be outpacing WFE, or is this as simple as changing restrictions on customers, or
    customers with capacity constraints at the end that is limiting the upside to revenues?"
    CFO: "I would say certainly the first half of 2026 was slower from a sequential point of view, given some
    of the lead time challenges we had and how that translated to the constraints around shipments."
  He then talks about SEMI-PT growing "at least a few points" faster than the company, and historically about
  share gains — but he does NOT produce a number showing process control intensity rising relative to WFE.
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

  My own arithmetic, which supports the analyst rather than KLA (LABEL AS ESTIMATE):
    KLA FY2026 revenue $13.579B ÷ CY2025 WFE ~$120B (KLA's own figure)          = ~11.3% of WFE
    KLA CY2026 revenue, implied ~$16.5–17.0B ÷ CY2026 WFE ~$150B (KLA's figure)  = ~11.0–11.3% of WFE
  If those are right, KLA's share of the WFE dollar is FLAT to marginally down in 2026, not rising. That is
  consistent with what the analyst saw in the quarterly data and with the CFO's non-answer. It does not mean
  process control intensity is falling — it means it is not visibly compounding, which is the load-bearing
  assumption behind a 27x forward multiple.

10-C. THE OTHER PIECE THAT CONTRADICTS "SUPPLY NOT DEMAND": Lam's own guide.
  Lam's September quarter: revenue $8.22B (+22% q/q), China 35% of revenue (from 26% in June). Guide $8.6B,
  i.e. +4.6% q/q. The CFO volunteered that China would be "meaningfully down" in December, "driven by the
  domestic customers in China."
  My arithmetic, LABEL AS ESTIMATE: Sept China revenue = 35% × $8.22B = $2.88B. If December China returns to
  the June level of 26% of $8.6B = $2.24B, then China alone is −$640M q/q — which more than fully accounts
  for a guide that is only +$380M q/q. On that assumption, Lam's NON-China revenue would grow ~19% q/q.
  Read that again: even with supply constraints biting, the ex-China business is compounding at ~19% a quarter.
  Which means (i) the demand thesis is intact, and (ii) the visible step-down in the guide is a China mix
  event, not a supply event. Both things are true, and neither is the story the tape told on Thursday.
  SOURCE for inputs: https://stockanalysis.com/stocks/LRCX/transcripts/718719-q1-2027/

================================================================================
11. INSPECTION INTENSITY — WHAT IS ACTUALLY DOCUMENTED
================================================================================
VERIFIED (KLA's words, not a model):
  "Process control intensity has increased due to faster product cycles, higher value wafer masks, more
  rigorous device performance specifications, growing design variability, and advanced packaging."
  "High-performance computing, HBM, increasing EUV adoption in DRAM, and recently adopted advanced packaging
  technologies such as hybrid bonding are driving higher process control intensity across the semiconductor
  ecosystem."
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

VERIFIED (the one hard number attached to the intensity claim):
  "We now expect our advanced packaging process control systems revenue to grow to approximately $1.1 billion
  in calendar 2026, up more than 70% year-over-year, above our prior expectations of high 50% growth, and
  almost two times faster than the advanced packaging market." — Rick Wallace
  (raise history: ~$635M CY2025 → ~$1.0B guided April 2026 → ~$1.1B guided July 2026)
  KLA's patterning line "grew 61 percent year on year in the June 2026 quarter" (CSET, citing the shareholder
  letter). https://chipsupplychain.org/metrology-and-inspection/
  Note: $1.1B is ~8% of FY26 revenue. It is real, it is growing fast, and it is not yet big enough to move the
  consolidated number on its own.

VERIFIED (the physical mechanism, well-sourced and usable in plain English):
  Bigger die = disproportionately worse yield, so inspection is worth more per wafer. CSET's textbook example:
  at the same defect density, 49.2% of chips 1cm on a side come out flawless, but only 11.3% of chips 2cm on a
  side. AI accelerators are among the largest die made. HBM adds stacking and packaging steps on top.
  https://chipsupplychain.org/metrology-and-inspection/

NOT FOUND / HONEST GAP: I could not find any KLA disclosure that quantifies "process control dollars per
wafer" or "process control as % of WFE" over time. KLA asserts intensity is rising; the only public test of
that assertion is revenue/WFE, and that test is flat (§10-B). If the article needs an intensity number, the
honest options are (a) the advanced-packaging $1.1B / +70% figure, (b) the 49.2%-vs-11.3% die-size mechanism,
or (c) explicitly say KLA does not disclose it.

================================================================================
12. THE BEAR CASE — WHAT WOULD MAKE THE BEARS RIGHT
================================================================================
This is the strongest section of the file. Do not soften it.

12-1. THE MULTIPLE IS THE TRADE, AND THE BULLS ALREADY CUT IT.
  Morgan Stanley raised its KLA estimates on Oct 6 — CY2027 revenue to $21.4B from $20.4B, EPS to $6.77 from
  $6.23, projecting KLA grows 42% in 2027 vs 37% for WFE — and simultaneously cut its target multiple to 28x
  from 36x, "a 20% premium to KLA's average valuation since 2020." Target went DOWN $26 while estimates went UP.
  That is the single most informative datapoint in this file: the most constructive analyst on the name decided
  the earnings are fine and the multiple is not.
  https://www.investing.com/news/analyst-ratings/morgan-stanley-cuts-kla-stock-price-target-on-valuation-concerns-93CH-4934052
  Run the arithmetic: 28x on FY27 EPS of $5.46 = $153. That is 5% above the current price. The consensus
  target of $232.38 requires 42.6x FY27 EPS. So "59% upside to consensus" is a bet that KLA re-rates back to
  its July multiple, not a bet on the business.

12-2. THE SUPPLY-CONSTRAINT STORY MAY BE A DEMAND STORY WEARING A COSTUME.
  Three ways this happens, all live:
  (a) China roll-off masquerading as supply tightness. Lam's December guide is only +4.6% q/q, and China
      dropping from 35% to ~26% of revenue fully explains it (§10-C). If KLA's December guide comes in light
      and management blames optics, the correct question is how much of the gap is Chinese domestic customers
      rolling off — which is permanent, not deferred.
  (b) "Delayed" and "cancelled" look identical for one quarter. Lam says December tools ship in March. If the
      March quarter then misses, the constraint was a demand air pocket.
  (c) Cleanroom constraints at the customer are a DEMAND-side cap, not a supply-side one. Bettinger: "This
      year has been primarily clean room constrained." A fab that cannot install tools is a customer choosing
      not to take delivery. KLA's own phrasing — "Despite well-chronicled fab space limitations" — concedes
      the cap exists on the customer's side of the transaction.
  The test: watch whether backlog GROWS while revenue misses. Growing backlog + missing revenue = supply.
  Flat backlog + missing revenue = demand. KLA stopped disclosing RPO quarterly, which makes this harder and
  is itself worth saying on the page.

12-3. PEAK-CYCLE CYCLICALITY, WITH RECEIPTS.
  This is a business that has already had a down year recently: FY2024 revenue $9.81B, −6.5% y/y (from $10.50B).
  FY2024 EPS fell too. The current consensus asks for +33.6% in FY2027 ($18.14B) on top of +11.7% in FY2026.
  WFE is being forecast at $200B+ for 2027 (Lam) and ~$210B (BofA, Sept 2026). Historically, a year in which
  everyone agrees the number is $200B is a year in which the following year gets cut. KLA at 27x forward
  earnings has no room for a −6% year; the FY2024 analogue would take the stock to the mid-teens multiple.
  SOURCES: https://stockanalysis.com/stocks/KLAC/forecast/ ; WFE $210B 2027 from BofA via
  https://finance.yahoo.com/technology/ai/articles/bank-america-makes-bold-chip-030700579.html

12-4. CHINA: 26% OF REVENUE, STRUCTURALLY DECLINING, WITH A REGULATORY CLIFF 13 DAYS AFTER THE PRINT.
  China was 39% (Sept 2025) → 26% (June 2026), modeled at "mid-20s" for CY2026, and the Street models −20.7%
  y/y in the quarter being reported. KLA has already booked $300–350M of lost revenue to export controls
  through CY2026 (Oct 2025 estimate). Then the Affiliates Rule returns on Nov 10, 2026 absent a Federal
  Register extension. Chinese domestic suppliers are still only 0.7% of the process control market (CSET) —
  which is the bull argument — but that 0.7% is growing from a policy-protected base, and Skyverse grew
  revenue 48.75% in 2025. "They can't build it" is a claim with a 5-year history of being wrong in this
  industry.
  SOURCES: §7 above; https://www.federalregister.gov/documents/2025/11/12/2025-19846/one-year-suspension-of-expansion-of-end-user-controls-for-affiliates-of-certain-listed-entities

12-5. VALUATION HAS NO MARGIN OF SAFETY ON ANY MEASURE EXCEPT FORWARD EARNINGS.
  Trailing P/E 39.8x. EV/Sales 14.1x. EV/EBITDA 31.6x. EV/FCF 50.8x. P/B 30.0x. The only "cheap" number is
  26.7x FY27 EPS — and that number exists because FY27 EPS is forecast to grow 45%, which is the assumption
  under test. If FY27 comes in at $4.70 instead of $5.46, the same price is 31x. A 10% estimate cut plus a 2x
  multiple cut is a halved stock, and this stock has already demonstrated it can fall 53% from a high in four
  months without a single bad quarter.

12-6. CUSTOMER CONCENTRATION IS EXTREME AND DOCUMENTED.
  Taiwan — which in practice means TSMC plus a handful of others — was 31% of Q4 revenue. Korea was 10%
  (Samsung/SK Hynix). KLA's own 10-K risk factors list "our vulnerability to a highly concentrated customer
  base" and "the cyclicality of the industries in which we operate." A single leading-edge customer pushing a
  node by two quarters moves KLA's year more than any product cycle.
  SOURCE: Q4 FY26 release forward-looking statements section (verbatim risk language) + geographic mix §7.

12-7. GROSS MARGIN IS AT A CEILING, NOT A FLOOR, AND EVERY INPUT IS GOING THE WRONG WAY.
  62.5% non-GAAP is the guide. Against it: >100bp of memory/DRAM component inflation that management says
  lasts through 2027, 50–100bp of tariffs, and a mix shift toward systems (lower margin than service) as
  shipments ramp. KLA's own answer to "can you raise prices?" was: "When we bring out new products, that's
  when new pricing decisions get made. With existing products, it's a little bit more around other ways..."
  — i.e. no, not really, not on the installed base. In a supply-constrained market you would expect pricing
  power. KLA is not demonstrating it.
  https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/

12-8. THE COMPETITIVE EDGE IS NARROWING AT THE EDGES THAT MATTER FOR AI.
  KLA is third in e-beam metrology (18.8%) behind AMAT (45.1%) and ASML (35.6%) — and e-beam is where the
  sub-2nm and gate-all-around defects get found. Mask inspection is a 45.9%-vs-42.0% knife fight with
  Lasertec, which already owns actinic EUV inspection while KLA's actinic tool is a demo. AMAT says its
  process diagnostics business grows >50% in 2026. Onto took a >$200M single-customer Dragonfly order for
  2027 delivery. The 85.9% defect-inspection fortress is real; the growth frontier is not fortified.

12-9. THE STOCK HAS ALREADY STARTED DISAGREEING WITH MANAGEMENT.
  KLA is −12.15% in a week in which the S&P fell 0.47% and 66% of S&P stocks rose. It is −52.6% from its June
  high. It fell 6.3% between the July 28 print and Oct 20 while the S&P gained 3.6% — i.e. the market has been
  selling this specific management's optimism for three months. Deutsche Bank's Melissa Weathers called the
  July quarter "frustrating" with a "skinny beat and raise," and cut her target to $195 from $220. UBS cut to
  $190 on Oct 20. Ten of thirty analysts are at Hold. When the tape and the guide disagree for a quarter, one
  of them is wrong, and it is not automatically the tape.
  SOURCES: https://finviz.com/news/405234/kla-must-prove-its-fourth-wfe-upgrade-stuck-as-stock-sinks-toward-lows ;
  https://www.tipranks.com/news/the-fly/kla-corp-price-target-lowered-to-195-from-220-at-deutsche-bank-thefly-news ;
  https://stockanalysis.com/stocks/KLAC/forecast/

12-10. INSIDER SELLING (WEAK, FLAG IT).
  MarketBeat (Oct 10, 2026) reports "$46.9 million worth of shares" sold by insiders over three months with no
  purchases. A TradingKey piece claims "over $110 million in executive equity sales." These two numbers do not
  agree and neither is a primary filing count. Mention only if you verify against Form 4s; otherwise omit.

================================================================================
13. UNVERIFIED / DO NOT PRINT AS FACT
================================================================================
U-1. "KLA is roughly 50–56% of process control" (from the assignment brief). The real figure is ~57% (CSET
     56.8%) to 58% (KLA's own Gartner citation). Use ~57%.
U-2. KLA's FULL-YEAR FY2026 China percentage. I verified the Q4 number (26%) and the 9-month FY26 number from
     the 10-Q (31.2%, $3,091.6M of $9,921.9M through March 31, 2026). I did NOT verify the 12-month figure.
     My estimate is ~30%, but it is an estimate. Print "26% in the June quarter" and "31.2% for the first
     nine months of FY26," not a made-up annual number.
U-3. FY2027 consensus EPS varies by source: $5.46 (stockanalysis/S&P Global), $5.43 (Zacks), $5.38 (Hudson
     Labs). Revenue consensus is tighter: $18.11–18.14B. Cite the source with the number.
U-4. Calendar-2027 vs fiscal-2027 EPS estimates are different animals. Morgan Stanley's $6.77 is CY2027;
     the $5.46 consensus is FY2027 (June year-end). Do not put them in the same sentence.
U-5. "Backlog up 60% YoY" (Hudson Labs) — I verified the ~$12.5B level from the CFO's own mouth but not the
     60% growth rate.
U-6. The Whisper number $1.22 is from Earnings Whispers via Finviz. Fine to mention as a whisper, not as a
     consensus.
U-7. Insider-sale totals (see 12-10).
U-8. ASML's "30% annual capacity plans may not meet 2027 and 2028 demand" appears in a research aggregator
     citing Korea Times (Oct 17, 2026). I did not open the Korea Times piece. Do not use without verification.
U-9. A DCF of $104/share (vs $166 on Oct 19) is circulating from a German aggregator. That is a single
     unidentified model, not a Street view. Ignore.
U-10. Two vague secondary claims I could not pin down and would leave out: "KLA's 200-day moving average is
     $997.72" (obviously a pre-split artifact in an AI-generated piece) and any "Meta raised capex to
     $135–145B" attribution for the Thursday selloff (single unconfirmed source). For the Thursday move, the
     verified, primary-attributable cause is Lam's supply-constraint commentary plus the China guide-down.

================================================================================
14. CANDIDATE SOURCE LINKS — ALL TESTED WITH curl, 2026-10-25
================================================================================
HTTP 200 (verified resolving):
 1. KLA Q4 FY2026 / full-year results, company press release (Jul 28, 2026)
    https://www.prnewswire.com/news-releases/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full-year-results-302836739.html
 2. Same release, KLA investor-relations canonical page
    https://ir.kla.com/news-events/press-releases/detail/518/kla-corporation-reports-fiscal-2026-fourth-quarter-and-full
 3. KLA Q1 FY2027 earnings date announcement (Oct 1, 2026) — the Oct 28 confirmation
    https://ir.kla.com/news-events/press-releases/detail/522/kla-announces-first-quarter-fiscal-year-2027-earnings-date
 4. KLA Q4 FY2026 earnings call transcript (full verbatim: lead times 12–24 months, RPO $12.5B, the
    intensity-vs-WFE exchange, the "no pricing power on existing products" answer)
    https://stockanalysis.com/stocks/KLAC/transcripts/657328-q4-2026/
 5. Lam Research Q1 FY2027 call transcript (Oct 21, 2026) — the CFO supply-constraint quote and the CEO
    >$200B 2027 WFE quote, verbatim
    https://stockanalysis.com/stocks/LRCX/transcripts/718719-q1-2027/
 6. CSET / Chip Supply Chain, "Metrology and Inspection" — the independent 56.8% share table, the by-tool-family
    share data, China 26% of Q4 revenue, and the die-size yield math
    https://chipsupplychain.org/metrology-and-inspection/
 7. KLA Q3 FY2026 earnings deck (PDF) — "58% 2025 Process Control Share... Source: Gartner April 2026"
    https://static.seekingalpha.com/uploads/sa_presentations/647/126647/original.pdf
 8. KLA forecast / consensus page (FY27 $18.14B, $5.46; 30 analysts; PT $232.38)
    https://stockanalysis.com/stocks/KLAC/forecast/

HTTP 403 to curl, live in a browser (bot-blocked — fine to cite, do not claim you read it programmatically
unless you did):
 9. Morgan Stanley's Oct 6 estimate-up / multiple-down call
    https://www.investing.com/news/analyst-ratings/morgan-stanley-cuts-kla-stock-price-target-on-valuation-concerns-93CH-4934052

Also verified 200 and useful for the setup section:
10. Zacks, "Insights Into KLA (KLAC) Q1: Wall Street Projections for Key Metrics" (Oct 23, 2026) — segment and
    geographic consensus
    https://finance.yahoo.com/markets/stocks/articles/insights-kla-klac-q1-wall-121505565.html
11. Earnings Whispers, "KLA Must Prove Its Fourth WFE Upgrade Stuck As Stock Sinks Toward Lows" (Oct 20, 2026)
    — the ~$4.5B December arithmetic and the whisper number
    https://finviz.com/news/405234/kla-must-prove-its-fourth-wfe-upgrade-stuck-as-stock-sinks-toward-lows
12. Federal Register, BIS Affiliates Rule suspension ending Nov 9, 2026 / reimposed Nov 10, 2026
    https://www.federalregister.gov/documents/2025/11/12/2025-19846/one-year-suspension-of-expansion-of-end-user-controls-for-affiliates-of-certain-listed-entities

================================================================================
15. PROPOSED SLUG
================================================================================
PRIMARY:  kla-process-control-supply-test-2026

UNIQUENESS CHECK (run 2026-10-25):
  * Does NOT collide with the published Sept 16 article's slug
    (articles/posts/kla-process-control-ai-chip-inspection-moat-2026.json — that is the only KLAC post in
    articles/posts/).
  * A hero image already exists at
    public/img/articles/kla-process-control-supply-test-2026.jpg (405KB, timestamped 2026-10-25 16:04) and a
    generator at scripts/gen-kla-process-control-supply-test-hero-2026.py. Both hard-code this slug.
  * No article JSON exists for this slug yet. It is clear.
  => Use this one. If it turns out to be claimed by another writer, the fallback is
     kla-supply-constraint-oct-28-test-2026 (verified unused), but then the existing hero image is orphaned,
     so make sure before switching.

================================================================================
16. RECOMMENDATION — IS THE ANGLE DEFENSIBLE?
================================================================================
Yes, but only if it is written as a test rather than a thesis. The supply-side evidence is unusually strong for
a semiconductor-equipment story because it comes from primary transcripts, not sell-side paraphrase: KLA's CFO
put company-wide lead times at ~12 months with 12–24 months on the products that matter, said customers are
already negotiating for second-half-2027 deliveries, tied a $12.5B backlog to an order funnel he expects to keep
growing, and named the bottleneck (optical components, 12–24 months to add capacity, supplier agreements already
being struck for 2029 and beyond). Lam's CFO independently said the same thing in the same week and added the
detail that makes it testable — the tools don't disappear, they ship in March. That is a real, documentable,
non-obvious mechanism, and it explains the otherwise bizarre tape of Thursday Oct 22, when a record quarter and
a raise produced an 11.8% decline: the market read "we can't ship" as "the cycle is over." The honest counterweight
is §10-B, and it is heavy: an analyst put the intensity question to KLA's CFO directly, noted that revenue as a
share of WFE has been flat all year, and the CFO answered with lead times rather than with a number — which means
the article's structural premise (inspection intensity compounding faster than WFE) is asserted by management and
NOT yet visible in the financials. Add Morgan Stanley raising 2027 estimates while cutting its multiple from 36x
to 28x, and the bear case writes itself: the earnings are fine and the multiple is the problem. So the defensible
piece is not "the market is wrong, this is a supply story." It is: "the constraint is genuinely supply-side, the
backlog proves demand exists, and Wednesday's December guide is the first hard test of whether that distinction
survives contact with a P&L — because if KLA guides December to ~$4.5B at 62.5% gross margin on a growing
backlog, supply was the story and the de-rating was a mistake; and if it guides to $4.2B and blames optics, no
reader will ever be able to tell whether the tools were delayed or the customers left." That version is true,
it is new relative to the September piece, it has a dated catalyst thirteen days before a regulatory cliff, and
it does not require you to know the answer in advance.
