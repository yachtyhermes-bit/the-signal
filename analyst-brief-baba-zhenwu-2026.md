# Analyst Brief — Alibaba (NYSE: BABA / 9988.HK): T-Head Zhenwu V900 + 20GW Cloud Buildout

**Event:** Alibaba Cloud Apsara Conference (Yunqi Conference), Hangzhou — Tuesday, September 22, 2026
**Brief compiled:** September 22, 2026 (CEST)
**Method:** curl + tag-stripping of syndicated copies; Google News RSS for dating/attribution; yfinance 1.4.1 via `/home/chino/video-venv/bin/python3`

---

## SOURCE URLS USED

| # | Label | URL | HTTP |
|---|-------|-----|------|
| S1 | **Alibaba official press release** (Media OutReach Newswire, 22 Sep 2026) | https://www.bastillepost.com/global/article/6178196-alibaba-unveils-roadmap-on-full-stack-ai-strategy-from-chips-cloud-infrastructure-models-to-agents | 200 |
| S2 | **AP wire** (via WTOP syndication, byline HONG KONG) | https://wtop.com/business-finance/2026/09/chinas-alibaba-unveils-new-powerful-chip-and-ambitious-ai-model-plans/ | 200 |
| S3 | **Bloomberg** (via Straits Times, "BLOOMBERG" credit; published Sep 22, 2026, 06:10 PM) | https://www.straitstimes.com/business/alibaba-unveils-powerful-ai-chip-to-drive-global-data-centre-expansion | 200 |
| S4 | **TrendForce** (citing ijiwei, EE Times China, ITHome) | https://www.trendforce.com/news/2026/09/22/news-alibaba-unveils-ai-chip-zhenwu-v900-for-1q27-mass-production-maps-out-new-server-cpus-for-3q27/ | 200 |
| S5 | **TechNode** (citing Yicai / Securities Times) | https://technode.com/2026/09/22/alibaba-unveils-zhenwu-v900-ai-chip-as-it-targets-20gw-of-cloud-data-centers-by-2032/ | 200 |
| S6 | **Forkast** | https://forkast.news/alibabas-zhenwu-v900-is-chinas-answer-to-nvidias-absence-and-export-controls-are-the-reason-it-exists/ | 200 |
| S7 | **CXO Digitalpulse** | https://www.cxodigitalpulse.com/alibaba-plans-5-10-trillion-parameter-ai-model-unveils-zhenwu-v900-chip/ | 200 |
| S8 | GuruFocus via Yahoo Finance (Citi note, May 13, 2026) | https://finance.yahoo.com/news/citi-thinks-alibabas-ai-story-151044826.html | 200 |

**Failed / not retrievable this session:** reuters.com, nikkei.com, bloomberg.com, cnbc.com, benzinga.com, nai500.com, investing.com, datacentremagazine.com, technology.org, sedaily.com, tradingview.com, r.jina.ai, msn.com — all 401/403/404/410 to curl. All claims below rest on the eight retrievable sources above plus dated Google News RSS headlines (which were used only to date/attribute stories, never as the sole basis for a claim).

---

## (1) VERIFIED FACTS

### A. The chip — VERIFIED

| Claim | Status | Source + exact wording |
|---|---|---|
| T-Head (Alibaba's chip arm) unveiled the Zhenwu V900 AI accelerator at the Apsara Conference, Hangzhou, Sept 22, 2026 | **VERIFIED** | S1: "T-Head, Alibaba's chip design unit, has unveiled the **Zhenwu V900**, its latest AI training and inference processor featuring high-capacity memory and robust inter-chip bandwidth." Also S4, S5, S6 |
| CEO Eddie Wu called it "the most powerful AI chip in China today" | **VERIFIED** — exact quote | S2: 'CEO Eddie Wu said the new Zhenwu V900 chip is the **"most powerful AI chip in China today"** and can deliver three times the performance of the company's previous generation Zhenwu M890 chip.' S6: "CEO Eddie Wu called it 'the most powerful AI chip in China today.'" S3 frames as "what it calls China's most powerful AI chip" |
| 3× the performance of predecessor Zhenwu M890 | **VERIFIED** | S1: "delivers **three times the performance** of its predecessor, the Zhenwu M890 (released in May)." S3: "it says trebles the performance of its predecessor" |
| 216GB memory | **VERIFIED** | S1: "Featuring **216 GB of GPU memory**…" S4 (citing ijiwei): "features **216GB of memory**" S6 renders it as "216 GB of HBM memory" (HBM wording is Forkast's, not in the official release) |
| 1,200GB/s chip-to-chip interconnect bandwidth | **VERIFIED** | S1: "…and **1,200 GB/s of inter-chip bandwidth**…" S4 (citing ijiwei): "**1,200GB/s of chip-to-chip interconnect bandwidth**" |
| Native FP8 + FP4 low-precision support | **VERIFIED** | S1: "native support across multiple data precisions, **including FP8 and FP4**." S4 (citing ijiwei): "native support for low-precision **FP8 and FP4** computing" |
| In-house ICN Switch can connect up to 500,000 V900 chips in a single cluster | **VERIFIED** | S4 (citing EE Times China): "T-Head's in-house **ICN Switch can connect up to 500,000 V900 chips in a single cluster**" S1: "the server can support a supernode cluster comprising **up to 500,000 cards**." S3: "can be combined in clusters of up to 500,000 units" |
| That cluster size is "enough to train/run frontier models of 5–10 trillion parameters" | **VERIFIED** | S4 (citing EE Times China): "providing enough computing capacity to train and run frontier AI models with **5 trillion to 10 trillion parameters**." S7: "a single cluster based on the V900 can support up to 500,000 cards for frontier AI model training and inference" |

### B. The model roadmap — VERIFIED

| Claim | Status | Source + exact wording |
|---|---|---|
| Alibaba plans to train a new model of 5T–10T parameters | **VERIFIED** | S1: "roadmap for the upcoming Qwen 4.5 and Qwen 5 model series, **projected to scale up to 5 to 10 trillion parameters**." S2: "plans to train a new AI model at the scale of five to 10 trillion parameters" |
| Qwen 3.8 Max currently reported at 2.4T params | **VERIFIED** | S2: "Its latest **Qwen3.8-Max** model, the most powerful of its Qwen AI series models, **has 2.4 trillion parameters**." S7 concurs. (Arithmetic: 5T/2.4T = **2.08×**, 10T/2.4T = **4.17×** — S7 renders this as "roughly two to four times larger in parameter count") |
| Qwen 4 is currently in training | **VERIFIED** | S1: "Alibaba revealed that its next-generation model, **Qwen 4, is currently in training**." |

### C. Product timelines — VERIFIED, with two scoping caveats

| Claim | Status | Source + exact wording |
|---|---|---|
| Mass production + large-scale deployment of V900 in Q1 2027 | **VERIFIED** | S1: "scheduled for **mass production and commercial release in Q1 2027**." S4 (citing EE Times China): "scheduled to enter **mass production and begin large-scale deployment in 1Q27**" |
| Next-gen Zhenwu J900 in Q3 2027 | **VERIFIED (secondary source only)** — with a source conflict, see §4 | S4 (citing EE Times China): "T-Head also unveiled the timeline for its next-generation **Zhenwu J900, which is set to launch in 3Q27**." **Conflict:** S6 says "A J900 successor is already on the roadmap for **Q3 2028**." Not mentioned in the official release (S1) |
| New Panjiu supernode server (V900 + ICN) in Q1 2027 | **PARTIALLY VERIFIED** — the server is verified, the name and date are not | S1 confirms an "**upgraded supernode server**, which integrates the Zhenwu V900 processor, **ICN Switch**, Panmai SmartNIC, and Zhenyue SSD controller chip… can support a supernode cluster comprising up to 500,000 cards" — but S1 does **not** use the name "Panjiu" and gives **no** Q1 2027 date. S4 (citing ITHome): "the company plans to launch a new **Panjiu supernode server** powered by the Zhenwu V900 and ICN Switch in **1Q27**" |
| New T-Head Yitian 720/730 server CPUs in Q3 2027 | **PARTIALLY VERIFIED** — CPUs verified, "Q3" scoping is not | S1: "roadmap for next-generation proprietary CPUs tailored for agentic AI tasks, **scheduled for launch in 2027**. The **Yitian 720** features enhanced single-core performance, higher core density, and increased energy efficiency compared to its predecessor, the **Yitian 710**; The **Yitian 730**, the first CPU built on T-Head's proprietary microarchitecture, boasts up to a **40% increase in SPECint2017/GHz performance** over Yitian 710's." S1 says only "2027", not Q3. S4 (citing ITHome) gives both as **3Q27** |

### D. Infrastructure + spending — VERIFIED (with one important correction)

| Claim | Status | Source + exact wording |
|---|---|---|
| Alibaba Cloud global data-center capacity target: >20 gigawatts by 2032 | **VERIFIED** | S1 (Eddie Wu, direct quote): "our target is that **by 2032, the global data center capacity operated by Alibaba Cloud will surpass 20GW**, fueling the industry's exponentially rising demand for AI." S2, S3, S5 concur |
| Wu: global AI data-center supply-chain shortages are "currently limiting the speed at which we can scale" | **VERIFIED** — exact quote | S2: 'Global shortages across the AI data center supply chain, for example, "**are currently limiting the speed at which we can scale our compute infrastructure**" for AI, he added.' S7: "shortages across the AI data-centre supply chain were limiting how quickly Alibaba Cloud could expand" |
| AI infrastructure commitment: more than $53B (≈RMB 380B) over three years | **VERIFIED AS A RESTATEMENT — NOT a new Sept-22 number.** See §4-c | S3: "It is **committed to spending more than US$53 billion** (S$67.6 billion) **over a three-year period** to expand its AI capabilities." S4 (citing EE Times China): "committed to investing **more than US$53 billion, or around RMB 380 billion**, in AI infrastructure over the next three years." The figure **does not appear in Alibaba's official Sept 22 press release (S1)**. Originating announcement: **Feb 24, 2025** (Reuters: "Alibaba to invest more than $52 billion in AI over next 3 years"; SCMP: "Alibaba to pour US$53 billion into AI infrastructure") |

### E. Business metrics + market context — VERIFIED

| Claim | Status | Source + exact wording |
|---|---|---|
| T-Head delivered 560,000 units of the Zhenwu family; deployed by more than 400 external customers | **VERIFIED AS REPORTED** — but the customer count is superseded by Alibaba's own Sept-22 figure. See §4-a | S3: "**T-Head**, which is angling for a stock market listing, **has delivered 560,000 units of the Zhenwu product family, and its processors have been deployed by more than 400 external customers**, Alibaba has said. BLOOMBERG" S6 attributes the same numbers specifically to the **M890**: "The M890, released in May 2026, has already shipped **over 560,000 units to more than 400 external customers across 20 industries**." |
| T-Head is angling for a stock market listing | **VERIFIED — but pre-existing, not new on Sept 22.** See §4-d | S3 (Sept 22 restatement): "T-Head, which is angling for a stock market listing…" Original report: **Bloomberg, Jan 22, 2026** — "Alibaba Is Said to Plan IPO for AI Chipmaking Unit T-Head" (Reuters matched same day) |
| Citigroup estimate: the 20GW plan could drive >$160B of external revenue for Alibaba Cloud | **VERIFIED — single-sourced to Bloomberg** | S3: "he then set a target of 20 gigawatts of data centre capacity for the Alibaba Cloud service globally by 2032 — a big expansion that **Citigroup estimates could drive more than US$160 billion of external revenue for the fast-growing division**." No primary Citi research note was retrievable to confirm independently. Separately, a **May 13, 2026** Citi note (analyst **Alicia Yap**, Buy, **$205 PT**) forecast AI-related revenue at a **90% CAGR FY2026–FY2031**, with MaaS alone at ~**RMB 439B by 2031** (S8) |
| AI-related revenue ambition: quintuple to ~$100B within five years (Straits Times) | **VERIFIED AS REPORTED — but the target predates Sept 22.** See §4-b | S3: "It also **aims to quintuple annual cloud and AI revenue to US$100 billion in five years**." S3 also: "annualised revenue from AI-related products expected to reach **US$10 billion in the current quarter**." Original announcement: **March 19, 2026** (Q3 FY2026 earnings call) — Bloomberg headline "Alibaba Targets $100 Billion of AI Revenue in Five Years"; AP "China's Alibaba targets $100B in AI and cloud revenue over 5 years"; Nikkei "Alibaba aims for $100bn cloud, AI revenue after posting 66% profit drop" |
| Announcement lands days before a Trump–Xi meeting where AI chip policy is central | **VERIFIED** | S2: "days ahead of a meeting between Chinese and U.S. leaders at which competition to lead on AI technology is expected to be a major theme… Chinese leader **Xi Jinping is set to arrive in Washington on Wednesday** for a state visit and meeting with U.S. President Donald Trump." S3: "**on the eve of a historic summit** between US President Donald Trump and his Chinese counterpart Xi Jinping… top-level US executives like Nvidia boss **Jensen Huang** and Microsoft's **Satya Nadella** attend a White House state dinner." S3 also: Bessent–He Lifeng talks agreed to set up a **US–China AI dialogue** |
| Alibaba last unveiled a new AI chip in May 2026 | **VERIFIED** | S3: "Alibaba — which **last unveiled a new AI chip in May** — plans to update that line-up every year." S1 confirms the predecessor M890 was "released in May". Prior launch covered May 19–21, 2026 |
| T-Head plans annual chip updates | **VERIFIED** | S3: "plans to **update that line-up every year**." S4: T-Head "expects its annual AI-chip shipments to grow substantially"; S5 concurs |
| Shares jumped on the announcement | **VERIFIED** | S3: "Its shares **leapt more than 5 per cent in Hong Kong**, while WeChat operator **Tencent Holdings surged more than 7 per cent**." Cross-check: 9988.HK printed an intraday high of HK$118.30 vs prior close HK$112.60 = **+5.06%**, then closed at HK$114.80 (**+1.95%**) per yfinance |
| Qwen is the world's most-downloaded AI model; profit fell >75% in the last quarter | **VERIFIED** | S3: "has created the **world's most popular AI model by downloads**… the company saw **profit plunge by more than 75 per cent in the last quarter**, after a nearly **US$10 billion spending spree**." yfinance corroborates: earnings growth **-79.4%** |
| Alibaba raised ~$10.2B in an August follow-on share offering | **VERIFIED** | S3: "raised about **US$10.2 billion** from a follow-on share offering in August" |
| Additional Sept-22 disclosed items | **VERIFIED** | S1: T-Head Zhenwu chips "have been serving **over 650 customers**" across automotive, finance, LLM, embodied intelligence, energy and manufacturing. Qwen3.8-Max completed **33 automated RSI cycles** in >1 month, lifting its Artificial Analysis score **from 40 to 45**; a chip-design experiment logged **>10,000 EDA tool calls** and cut chip area **42%** with no performance loss. Qwen3.8-LiveTranslate cuts latency from **2.8s to 2.3s** (~20%). Yitian 730 up to **40% SPECint2017/GHz** over Yitian 710. HPN 8.0 Pro delivers **100 petabits** of networking. Wu (S2/S1): "Machine Thinking" is "**less than 3% of all Human Thinking**" today but could scale to **1,000×** human capacity |

---

## (2) FINANCIALS — yfinance 1.4.1 (pulled Sept 22, 2026)

### BABA — NYSE, USD (primary listing for the article)

```
Price (last)                  118.55
Previous close                115.75        Change +2.80 / +2.42%
Open / Day range              120.15 / 118.40 – 120.40   (day high = +4.02% vs prev close)
Market cap                    $294,670,663,680   (~$294.7B)
Enterprise value              $215,835,033,600   (~$215.8B)
Shares outstanding            2,485,623,615
Trailing P/E                  26.76         Forward P/E   12.78
P/S (TTM)                     0.282         P/B           1.770
Price / 50-DMA                118.05  (+0.42%)    200-DMA  133.06  (-10.9%)
52-week high / low            192.67 / 91.99       (+28.9% off low, -38.5% from high)
1-year price change           -29.02%
Avg volume (3-mo)             11,922,401
Beta                          0.50          Dividend yield 0.91%
Trailing EPS / Forward EPS    $4.43 / $9.28
Earnings growth (YoY)         -79.4%

Total revenue (TTM)           ¥1,044,970,995,712   (~¥1.045T)
Revenue growth (YoY)          +8.6%
Gross margin                  38.20%    Operating margin 7.30%    Profit margin 7.04%
EBITDA                        ¥99,512,999,936   (~¥99.5B)
Free cash flow                -¥82,644,123,648  (~-¥82.6B; -7.9% of TTM revenue)
Total cash                    ¥385,696,989,184
Total debt                    ¥266,529,996,800
Net cash position              +¥119.2B
Debt / equity                 23.93          Return on equity 6.36%

Analyst consensus             strong_buy  (39 opinions)
Mean / high / low target      $185.91 / $238.62 / $95.36   (+56.8% to mean)
Quote currency USD  |  Financial currency CNY
```

### 9988.HK — Hong Kong, HKD

```
Price (last)                  114.80       Previous close 112.60   Change +2.20 / +1.95%
Day range                     114.00 – 118.30   (day high = +5.06% vs prev close)
Market cap                    HK$2,282,796,613,632   (~HK$2.283T)
Enterprise value              HK$2,048,043,646,976
Shares outstanding            19,884,988,918
Trailing P/E                  26.39        Forward P/E 12.50      P/B 1.753
50-DMA / 200-DMA              115.46 / 129.82
52-week high / low            186.20 / 88.65
1-year price change           -29.36%
Avg volume (3-mo)             98,735,233
Trailing EPS / Forward EPS    HK$4.35 / HK$9.18
Earnings growth (YoY)         -79.4%
Analyst consensus             strong_buy (22 opinions), mean target HK$174.68
```

**Notes / caveats**
- `BABA.MX` (Mexico listing) returned `KeyError: 'exchangeTimezoneName'` in yfinance — no data; omit from any chart.
- yfinance `enterpriseValue` and `marketCap` are quoted in the **quote** currency (USD), while `ebitda`, `totalRevenue`, cash and debt are in the **financial** currency (CNY). Do not divide USD EV by CNY EBITDA: at the implied rate used by the $53B/RMB 380B pairing (~7.17), EV/EBITDA ≈ **15.5×**, not 2.2×.
- Prior Signal BABA articles quoted **$113.24 @ $281.5B market cap** (Sept 7) and **$119.34 @ $282.3B** (Aug 24). Market cap is now **$294.7B** (+4.7% vs the Sept 7 figure).
- Free cash flow is **negative** (-¥82.6B TTM) — a direct consequence of the AI capex ramp and a live tension with the 20GW/5–10T-parameter commitments.
- `forwardPE` 12.78 vs the two prior articles' 12.1 / 12.6 — consistent.

---

## (3) HOW THIS ANGLE DIFFERS FROM THE SIGNAL'S TWO PRIOR BABA ARTICLES

1. **`baba-record-ai-share-placement-2026`** (Aug 24, 2026, *"Alibaba's Record $10.2B Share Sale Is a Full-Stack Bet on AI"*, sentiment neutral) covered **how Alibaba FINANCES the buildout** — Hong Kong's largest-ever share placement, 100% of proceeds earmarked for AI, sovereign-fund oversubscription.
2. **`baba-blackwell-export-loophole-2026`** (Sept 7, 2026, *"Washington Drew a Line on AI Chips. Alibaba's Demand Stepped Over It."*, sentiment positive) covered **how Alibaba SOURCES compute despite sanctions** — the NYT's Aivres/Inspur story on >$3B of Nvidia Blackwell servers routed to Alibaba and ByteDance via Southeast Asia.

**The new angle is the supply side:** this is the first of the three stories about silicon Alibaba **builds itself** — T-Head's own accelerator roadmap (V900 specs, 500,000-chip single-cluster scaling, Q1 2027 production), the 20GW/2032 capacity target, and the 5–10T-parameter Qwen 4.5/5 model plan. Where the prior two explained Alibaba's *demand for and purchase of* frontier compute, this one is about Alibaba *becoming the supplier* — and it lands days before a Trump–Xi summit where AI chip policy is the central agenda item. Prior scores were neutral and positive; this event produced a positive tape reaction (+2.42% NYSE close, +5.06% HK intraday) alongside a negative-FCF capex backdrop.

---

## (4) UNVERIFIED, CORRECTED, OR SOURCE-CONFLICTED

**a. CORRECTION — "more than 400 external customers" is stale; Alibaba's own Sept-22 figure is "over 650 customers."**
Bloomberg (S3) and Forkast (S6) both carry "more than 400 external customers," and Forkast explicitly ties the 400 number to the **M890 (May 2026)** cohort. Alibaba's **official Sept 22 press release (S1)** says: "T-Head's Zhenwu AI chips have been **serving over 650 customers** across different industries." Use **650** for the Sept 22 figure and, if citing 400, attribute it to the May-2026 M890 disclosure. The **560,000-unit** family total is corroborated only by Bloomberg/Forkast (not in S1); TrendForce reported **470,000** unit shipments as of March 2026, so 560,000 is a plausible later figure but rests on a single origin.

**b. CORRECTION — the "$100 billion AI revenue / quintuple in five years" is NOT a Sept-22 announcement.**
It dates to **March 19, 2026** (Q3 FY2026 earnings call), reported then by Bloomberg, AP, Nikkei and SCMP. Bloomberg's Sept 22 story restates it and supplies the "quintuple" framing. Do not present it as new. Related and *also* pre-existing: the **$10B annualised AI-product revenue** run-rate expected in the current quarter.

**c. CORRECTION — the ">$53 billion (≈RMB 380 billion) over three years" is NOT a Sept-22 announcement.**
It originates from **Feb 24, 2025**. It appears in the Sept 22 coverage only via secondary sources (S3, S4), and is **absent from Alibaba's official Sept 22 release (S1)**. It was also *already* superseded in Sept 2025, when Alibaba said it would spend **beyond** the $53B plan at the 2025 Apsara Conference. Prefer: "Alibaba restated its existing three-year, >$53B (≈RMB 380B) AI infrastructure commitment, first announced February 2025."

**d. CORRECTION — T-Head's listing ambition is NOT new.**
Reported by Bloomberg and Reuters on **Jan 22, 2026**. Bloomberg's Sept 22 piece mentions it in passing ("angling for a stock market listing"). Attribute to January 2026.

**e. SOURCE CONFLICT — Zhenwu J900 timing: Q3 2027 vs Q3 2028.**
TrendForce, citing EE Times China (S4), says **3Q27**. Forkast (S6) says **Q3 2028**. Neither is confirmed by Alibaba's official release. Recommend hedging ("a next-generation Zhenwu J900 is on the roadmap for 2027, per EE Times China; at least one outlet reports 2028") or omitting the date.

**f. UNCONFIRMED DETAIL — "Panjiu" supernode name and its Q1 2027 date.**
The upgraded V900+ICN supernode server is confirmed by Alibaba (S1) but the release never names it "Panjiu" and gives no launch date. Name + Q1 2027 come only from TrendForce citing ITHome (S4).

**g. UNCONFIRMED DETAIL — Yitian 720/730 "Q3 2027."**
Official release (S1) says only "**2027**." The "3Q27" scoping is TrendForce/ITHome (S4).

**h. SINGLE-SOURCED — Citigroup's ">$160 billion of external revenue."**
Attributed to Citigroup by Bloomberg (S3). No primary Citi note retrievable. Do not present as a published Citi report with a price target; frame as "Citigroup estimates, per Bloomberg." (The separately retrievable Citi note — May 13, 2026, analyst Alicia Yap, $205 PT, 90% AI-revenue CAGR — is a *different* piece of research and should not be conflated.)

**i. UNVERIFIED — no primary-source access to the wire originals.**
reuters.com, bloomberg.com, nikkei.com and cnbc.com all blocked curl this session. Every Bloomberg-attributed item above rests on the Straits Times syndication (S3), which carries a "BLOOMBERG" credit. Reuters-attributed items rest on AP (S2) or syndicated headlines. All performance figures for the V900 are **vendor-reported and not independently benchmarked** (explicitly flagged by Forkast, S6).

**j. NOT FOUND / no support located.**
No evidence was found that Alibaba disclosed the **manufacturer/foundry** for the V900 (SMIC is speculated but unconfirmed; Bloomberg notes US controls largely block TSMC for Chinese firms) or a **per-unit price / capex split** for the 20GW plan. The claim that Alibaba's T-Head will pursue an **annual** chip cadence is verified (S3), but no specific 2028 product besides the disputed J900 was named.

---

## (5) SLUG

**Proposed slug: `baba-zhenwu-v900-ai-chip-stack-2026`**

**Uniqueness: CONFIRMED.**
- `articles/posts/baba-zhenwu-v900-ai-chip-stack-2026.json` — **does not exist** (posts dir holds 447 files; none with this slug).
- Not present in `articles/index.json` (101 entries; zero BABA-related slugs indexed there).
- Repo-wide grep for the literal string returns exactly one hit: `scripts/gen-baba-zhenwu-v900-hero-20260922.py` — the pre-existing hero-image generator written for this article.
- A matching hero asset has already been generated and mirrored:
  - `public/img/articles/baba-zhenwu-v900-ai-chip-stack-2026.jpg` (171,554 bytes)
  - `_backup_dist/img/articles/baba-zhenwu-v900-ai-chip-stack-2026.jpg` (171,554 bytes)
- The nearest prior BABA slugs — `baba-blackwell-export-loophole-2026` and `baba-record-ai-share-placement-2026` — are distinct.
- Wildcard alternatives also verified unused: `baba-zhenwu-v900-ai-chip-20gw-2026`, `baba-zhenwu-v900-20gw-cloud-buildout-2026`, `baba-zhenwu-v900-2026`.

**No file was created or modified under `articles/posts/`.**
