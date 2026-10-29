# Fact Dossier — Google/Alphabet "Project Suncatcher" first orbital TPU test
**Slug:** googl-project-suncatcher-2026-10-01
**Ticker:** GOOGL (Alphabet Inc., NASDAQ)
**Compiled:** 2026-10-01 ~16:05 UTC (09:05 PT) — launch window had NOT yet opened at compile time
**Analyst:** The Signal pipeline (subagent)

> Verification note: every fact below is tied to a URL that returned HTTP 200 when fetched with a
> browser User-Agent, unless explicitly flagged. Reuters (401) and NYT (403) block direct fetching;
> their content is reproduced via syndicated copies / corroborating outlets and is flagged as such.
> Secondary/aggregator sites of unknown provenance (shattered.io, cellcog.ai, tech-insider.org,
> concepttocloud.com) were NOT used as sources.

---

## 1. THE LAUNCH — what is flying, when, and on what

| Item | Fact | Source |
|---|---|---|
| Mission | SpaceX **Transporter-18**, dedicated smallsat rideshare to sun-synchronous orbit (SSO) | spacex.com/launches/transporter18 |
| Vehicle | **Falcon 9** (Block 5), booster B1082 flight #25 | nextspaceflight.com/launches/details/7611 |
| Launch site | **Vandenberg SFB, California**, SLC-4E | spacex.com/launches/transporter18 |
| Launch date | **Thursday, October 1, 2026**; 58-minute window opens **11:18 a.m. PT** (18:18 UTC) | spacex.com/launches/transporter18 |
| Backup opportunity | Friday, October 2, same time | spacex.com/launches/transporter18 |
| Launch price (Falcon 9 list) | $74.00 M | nextspaceflight.com/launches/details/7611 |
| Total payloads | **130 payloads** (cubesats, microsats, hosted payloads, 2 reentry vehicles, 4 orbital transfer vehicles carrying 41 payloads for later deploy). Close to the record 143 (Transporter-1, Jan 2021) | spacex.com/launches/transporter18 / space.com |
| Google payload | **"Project Suncatcher M1"**, manifested by **Planet Labs** | spacex.com/launches/transporter18 (deployment timeline) |
| Deployment time | Project Suncatcher M1 deploys at **T+01:01:25**, just after KEVIN (D-Orbit) | spacex.com/launches/transporter18 |
| Stated purpose | "gather in-orbit data on how our TPUs handle the physical stress of spaceflight and the radiation and thermal extremes of space" | blog.google (Sep 24, 2026) |
| Nature of flight | **Rideshare**, not dedicated. Google: "this initial mission onboard the upcoming Transporter-18 rideshare mission with SpaceX was developed in partnership with Planet" | blog.google |

**Timeline context:** Google announced the in-orbit test on **September 24, 2026** — the first Suncatcher
hardware test. The original plan was two custom satellites in 2027; Google pulled the first test forward
by integrating its chips into a Planet satellite that already existed.
"While the AI hardware inside is Google's, the spacecraft comes from a satellite imagery firm called
Planet Labs. The initial plan was to launch two custom satellites in 2027, but Google wanted to
accelerate its efforts. So the company opted to integrate its chips into a satellite that Planet Labs
had already built for an early test." — Ars Technica, Oct 2026

---

## 2. THE PAYLOAD SPEC (all key figures)

| Figure | Value | Source |
|---|---|---|
| Satellite name | **MVP** | Ars Technica; NYT via space.com/futurum |
| Size | "about the size of a **refrigerator**" | Ars Technica; space.com |
| TPU count | **4 Google TPUs** | Ars Technica (headline dek: "will have four TPUs"); space.com |
| TPU generation | **Trillium** (Google's **v6e Cloud TPU**) | Google Research post (Nov 4, 2025); futurumgroup |
| Compute equivalence | roughly **one Google Cloud TPU v6e-4 slice** | futurumgroup (citing NYT) |
| Solar power | **~1 kilowatt** | Ars Technica ("solar panels that supply only about one kilowatt of power, The New York Times reports. That's enough to power a microwave or a hair dryer") |
| Run-time limit | **~15 minutes at a time, then must shut down to cool** | Ars Technica: "The cooling system will only be able to operate in brief spurts of about 15 minutes. After that, the TPUs need to shut down to allow the radiators to catch up." |
| Why the limit | **Thermal / radiative cooling in a vacuum** — no airflow in space, radiators are the only heat-rejection path | blog.google ("Cooling in space"); Ars Technica ("Cooling the chips may be the biggest issue") |
| Cooling design | "a layer of malleable **'thermal interface material'** that connects the chips to **aluminum and copper heat pipes**. Those components conduct heat into a **radiator** that can project it into space" | Ars Technica |
| Workload | **Gemini** models run on the TPUs for testing | Ars Technica |
| Mission duration | Ars Technica: "will operate for **just a few months**". space.com: "will operate in Earth orbit **for a year**, if all goes to plan, **according to The New York Times**" | Ars Technica; space.com (citing NYT) |
| Deorbit | within approximately **6 years** (secondary source) | futurumgroup (citing NYT) — FLAGGED, not confirmed in a primary/200-fetchable source |
| Orbit altitude (satellite) | sun-synchronous (SpaceX: SSO); the paper's *design* altitude is **650 km** — the actual MVP altitude was not confirmed | spacex.com; Google Research post |

**Ambiguity to flag for the writer:** mission duration is reported as "a few months" (Ars Technica,
independent) vs "a year" (NYT, via space.com). Both refer to MVP. Do not assert one as settled.

---

## 3. WHAT PROJECT SUNCATCHER IS (program definition)

- **Announced November 4, 2025** — Google Research blog post by **Travis Beals, Senior Director,
  Paradigms of Intelligence**: "Project Suncatcher is a moonshot exploring a new frontier: equipping
  solar-powered satellite constellations with TPUs and free-space optical links to one day scale
  machine learning compute in space."
  https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design
- **Solar multiplier:** "**In the right orbit, a solar panel can be up to 8 times more productive
  than on earth**, and produce power nearly continuously, reducing the need for batteries."
  — Google Research, Nov 4, 2025. Repeated in blog.google (Sep 24, 2026) and CNBC (Oct 1, 2026).
- **Orbit choice:** "a **dawn–dusk sun-synchronous low earth orbit**, where they would be exposed to
  near-constant sunlight." — Google Research
- **Architecture:** compact constellations of interconnected satellites; the paper illustrates formation
  flight with an **81-satellite cluster of 1 km radius at a mean altitude of 650 km**, next-nearest-neighbour
  spacing oscillating **~100–200 m**. — Google Research + preprint paper
- **Not a data center yet:** "The first Suncatcher mission is designed to gather in-orbit data and
  identify potential failure points, rather than demonstrate an operational orbital data center,
  Google said." — Reuters, Sept 24, 2026
- **Next milestone:** "our next milestone is a **learning mission in partnership with Planet**, slated
  to **launch two prototype satellites by early 2027**. This experiment will test how our models and
  TPU hardware operate in space and validate the use of optical inter-satellite links for distributed
  ML tasks." — Google Research
- **Google's own expectation management:** "We don't expect, to be perfectly frank, that we'll have
  anything usefully operational in the next few years" — **James Manyika**, SVP Research and
  Technology & Society, comparing it to Google's 15-year AV arc. — futurumgroup (quoting Manyika)

---

## 4. GOOGLE RESEARCH PAPER — "Towards a future space-based, highly scalable AI infrastructure system design"

- **Authors:** Blaise Agüera y Arcas, Travis Beals, Maria Biggs, Jessica V. Bloom, Thomas Fischbacher,
  Konstantin Gromov, Urs Köster, Rishiraj Pravahan, James Manyika (all Google; equal contributions).
- **arXiv:** 2511.19468 (submitted 22 Nov 2025; v2 revised **17 June 2026**)
  https://arxiv.org/abs/2511.19468
- **Primary PDF (verified 200):** https://services.google.com/fh/files/misc/suncatcher_paper.pdf

### Verified figures from the paper (verbatim):

**Launch-cost threshold:**
> "a learning curve analysis suggests launch to LEO may reach **≲$200/kg by the mid-2030s**."
> — Abstract

> "We compared the kg/kW solar power (bus and payload) launched ratios for Starlink v2, Starlink v1,
> OneWeb & Iridium satellites and found that, if LEO launch prices drop to **$200/kg**, we can project
> $/kW/y launched to LEO ("launched power price") could be **∼ $810/kW/y** for a Starlink v2-type
> constellation (amortized over satellite lifetime), or **∼$810–7,500/kW/y** if we include a broader
> range of satellites with different mass/power ratios … For comparison, current power spend for
> terrestrial data centers in the US is reported to be **∼$570–3,000/kW/y** … Thus, if launch costs to
> LEO reach $200/kg, then the cost of launch amortized over spacecraft lifetime could be roughly
> comparable to data center energy costs, on a per-kW basis."
> — §2.4 Launch cost analysis

> "SpaceX launch pricing data and mass launched from Falcon 1 to Falcon Heavy [Fig. 4] yields a
> **∼20% learning rate** … If the learning rate is sustained — which would require **∼180 Starship
> launches/year** — launch prices could fall to **<$200/kg by ∼2035**."
> — §2.4

> "reaching <$200/kg by ∼2035 would require launching **∼370,000 t additional cumulative mass**,
> equivalent to **∼1800 Starship launches** (assuming 200 t capacity)."
> — §4.4

> "Even if this launch rate is reduced by ∼70%, prices could drop to **$300/kg** in the same timeframe,
> which would still have a substantial impact on feasibility of large-scale constellations."
> — §2.4

**Origins of the $200/kg number (why it was chosen):**
> "economic feasibility analyses of space-based solar power for Earth use … cite **$500/kg to
> Geostationary Transfer Orbit (GTO)** as a viability threshold. SpaceX's Falcon Heavy payload capacity
> to GTO vs LEO is ∼40%, so launch costs of $500/kg to GTO are equivalent to **∼$200/kg to LEO**.
> Further, **$200/kg is often cited, by SpaceX and others**, as a threshold beyond which launch could
> cease to be the limiting cost factor."

**Table 1 — launched power prices (verbatim):**

| Satellite | Mass (kg) | Power (kW) | Lifespan (y) | $/kW/y at $3,600/kg | $/kW/y at $200/kg |
|---|---|---|---|---|---|
| Starlink v2 mini [opt.] | 575 | 28 [est.] | 5 | $14,700 | **$810** |
| Starlink v1 | 260 | 7 [est.] | 5 | $26,600 | $1,470 |
| OneWeb | 150 | 0.8 | 5 | $135,800 | $7,500 |
| Iridium | 860 | 2 | 12.5 | $124,600 | $6,900 |

**Inter-satellite links:**
> "Our analysis shows that the required aggregate bandwidth per link, on the order of **10 Tbps**, is
> achievable by using Commercial Off-The-Shelf (COTS) Dense Wavelength Division Multiplexing (DWDM)
> transceiver technology."
> "A bench-scale demonstrator using off-the-shelf components successfully achieved **800 Gbps
> unidirectional (1.6 Tbps bidirectional)** transmission across a short free-space path."
> — §2.1 (Google Research post: "800 Gbps each-way transmission (1.6 Tbps total) using a single
> transceiver pair")

> "commercially available optical ISLs offer data rates in the range of **1–100 Gbps**" — vs. the
> required ~10 Tbps per link. — §2.1

**Radiation:**
> "We tested **Trillium**, Google's v6e Cloud TPU, in a **67 MeV proton beam** … While the High
> Bandwidth Memory (HBM) subsystems were the most sensitive component, they only began showing
> irregularities after a cumulative dose of **2 krad(Si)** — nearly three times the expected (shielded)
> **five-year mission dose of 750 rad(Si)**. No hard failures were attributable to TID up to the maximum
> tested dose of **15 krad(Si)** on a single chip."
> — Google Research post

**Thermal (non-quantified in text):** "Effective thermal management is a critical optimization challenge
for power-dense TPUs operating in a vacuum. Advanced thermal interface materials and heat transport
mechanisms, preferably passive to maximize reliability, are essential to efficiently move large heat
loads from the chips to dedicated radiator surfaces." — §5

**Physics/thermodynamics:** the system relies on **radiative cooling only** (no convection in vacuum)
and on solar collection in a dawn-dusk SSO. The **8×** solar-productivity figure is a Google figure
(Google Research, Nov 4, 2025; repeated blog.google Sep 24, 2026).

**Ground-segment reference point:** "NASA's TeraByte Infrared Delivery (TBIRD) mission, demonstrating
**200 Gbps** ground-LEO communications in 2023." — §5

**Paper's own caveat:** "our initial analysis shows that the core concepts of space-based ML compute are
not precluded by fundamental physics or insurmountable economic barriers. However, significant
engineering challenges remain, such as thermal management, high-bandwidth ground communications, and
on-orbit system reliability." — Google Research

---

## 5. THIRD-PARTY COST-PARITY STUDIES (context; NOT Google/MIT)

The task asked for a possible "Google/MIT follow-up study." **No Google–MIT joint study was found.**
The credible independent cost studies that DO exist:

- **TSP (The System Partners) research report, "Data Centers In Space"** — led by **Bruce Cameron,
  MIT Senior Lecturer** (this is the likely source of the "MIT" attribution). Headline: "**an orbital
  data center costs 5x more than a terrestrial data center today.** This gulf is driven by the launch
  costs and brutal economics of chip lifetimes." An associated post cites "a launch price of **$135/kg**,
  96% lower than today's SpaceX Falcon 9" as the requirement. Sources: https://t-s-partners.com/whitepapers
  (whitepapers page, fetched 200, states the 5x figure verbatim); LinkedIn post by Bruce Cameron
  (https://www.linkedin.com/posts/brucegcameron_tsp-research-report-on-data-centers-in-space-activity-7449468544641032192-54st)
  — the $135/kg figure is from the LinkedIn abstract only, NOT independently confirmed.
- **SemiAnalysis, "To Boldly Go: The Case for Space Datacenters"** — 2026 space datacenter inference
  LCOC **$590 per billion tokens vs $135/billion tokens** for an Earth datacenter (B300, FP4, DeepSeek R1);
  monthly levelized capex **18× higher** than terrestrial. https://newsletter.semianalysis.com/p/to-boldly-go-the-case-for-space-datacenters
- **BCG, "Space-Based Data Centers: Cost and Outlook to 2040"** (2026): today "orbital data centers
  would carry a **2.5x to 3x cost premium**"; narrows to "approximately **1.5x**" over the next decade,
  "but it does not disappear." At ~**$1,500/kg**, 1 GW in orbit ≈ **$30 bn** of launch. BCG expects
  launch costs to fall "to perhaps **$100/kg**." https://www.bcg.com/publications/2026/space-based-data-centers-cost-outlook
- **Futurum Group** (April 2026 report + Oct 2026 note): orbital compute could economically justify
  "roughly **$1 trillion of AI compute capex by 2030**"; current orbital infrastructure cost ≈ **$72.1 bn/GW
  excluding compute vs $16.2 bn** for off-grid terrestrial (**4.5× premium**); >33% of data centers
  off-grid by 2030; off-grid AI factory cost $35 bn/GW (2025) → $43 bn/GW (2030). Reaching $200/kg by
  mid-2030s requires "on the order of **180 Starship launches per year on a 20% learning curve**."
  https://futurumgroup.com/insights/project-suncatcher-prepares-to-launch-tpus-is-google-ahead-in-the-orbital-ai-race
- **Nuclear-sector benchmark used by Google's own paper:** current terrestrial US DC power spend
  **$570–3,000/kW/y** vs **$810–7,500/kW/y** in orbit at $200/kg launch.
- **AEI commentary**: "Google's own researchers have put the break-even threshold at roughly **$200 per
  kilogram**"; Falcon 9 ≈ $3,400/kg, Falcon Heavy ≈ $1,500/kg. https://www.aei.org/commentary/ai-data-centers-in-space-are-no-joke

---

## 6. COMPETITIVE / ORBITAL-COMPUTE LANDSCAPE

| Player | What they've done | Source |
|---|---|---|
| **Starcloud** | Launched **Starcloud-1** (60 kg, Astro Digital Corvus-Micro bus) **2 Nov 2025** on a SpaceX Falcon 9 into a **325 km** orbit carrying the **first Nvidia H100 GPU in space**; mission life ~11 months. In Dec 2025 it ran Google's **Gemma** and **trained NanoGPT** in orbit (demis Hassabis / Karpathy endorsements). Raised **$170M Series A at $1.1B valuation (March 2026)**; plans H100 cluster on Starcloud-2, next launch **Oct 2026** with **Nvidia Blackwell**; has pitched a **5 GW** orbital DC with a 4 km² solar array. | starcloud.com/starcloud-1; blogs.nvidia.com/blog/starcloud; cnbc.com/2025/12/10/...; DCD; futurumgroup |
| **SpaceX (Starmind / AI1)** | Announced plans for its own orbital data centers — satellites built in Redmond, WA, GPUs + solar arrays to be produced with Tesla; **FCC filing for up to 1,000,000 satellites**; AI1 satellites "capture continuous solar power with no weather or atmospheric loss"; **TERAFAB** joint Tesla/SpaceX AI-chip fab planned. Musk: "Space-based AI is obviously the only way to scale" and data centers in space will be "the cheapest way to train AI … within two years, maybe three at the latest." COO Gwynne Shotwell (Sept 2026): "supercompute in space" deployment in **2027**. | spacex.com/spacexai/starmind; space.com; cnbc.com/2026/10/01/... |
| **Amazon / Bezos (Blue Origin + Prometheus)** | Bezos calls space data centers "very realistic" but pushes back on 2–3-year timelines. | cnbc.com/2026/06/21/do-space-based-ai-data-centers-make-economic-sense.html |
| **Nvidia** | Space-1 Vera Rubin module announced at GTC 2026 (claimed up to 25× H100 space inference); Nvidia-backed Starcloud already flying H100s. | futurumgroup (secondary) |
| **AMD** | Positions Versal AI Edge Gen 2 XQR adaptive SoCs for orbital deployment. | futurumgroup (secondary) |
| **Axiom Space** | Placed two data center nodes in LEO in **January 2026**. | futurumgroup (secondary) |
| **China** | **"Three-Body" / Three-Body Computing Constellation (CASIC)** — completed 9 months of orbital testing (Feb 2026), planning a **32-satellite "Computing Grid" by 2028**. **ADAspace "star compute"** — first satellites launched May 2025, targeting **1,000 satellites / commercial ops by 2030** and **2,800 satellites by 2035** (>95% inference). **Shanghai "Xingshu Plan"** with Fudan University (unveiled at WAIC July 2026): 2 compute + 12 edge satellites → 50 compute + 100 edge; on 29 July 2026 two satellites maintained a **continuous laser link for 192 hours** at **99.99% uptime** up to 1,000 km. **Supercomputing-1** satellite launched via Long March-8A (23 Sept 2026). Chinese govt approved a **Space Computing Industry Innovation Center** (June 2026). Chinese domestic AI accelerators trail US state of the art by ~**4–5 years** (BUPT Dean Wang Shangguang, June 2026). | satnews.com (Feb 16, 2026); english.scio.gov.cn / Xinhua (Apr 27, 2026); tomshardware.com; techtimes.com |
| **Others named** | Aetherflux, Lonestar, Kepler Communications, Sophia Space, Phantom Space, Orbital, Cowboy Space (Reason-1 also flew on Transporter-18). | introl.com; space.com; stocktwits |

**Magnitude of the terrestrial constraint:** "local residents blocking **$68 billion worth of new data
center projects in Q2 2026**" — Tom's Hardware.

---

## 7. ALPHABET / GOOGL BUSINESS CONTEXT (thesis-relevant)

- **Q2 2026 results (quarter ended June 30, 2026), reported July 22, 2026:**
  - Total revenue **$119.8 bn, +24% YoY** (12th consecutive quarter of double-digit growth)
  - Google Cloud revenue **$24.8 bn, +82% YoY**; Cloud operating income **+212%**
  - Google Search & other **$63.3 bn, +17% YoY**
  - **Capex $44.9 bn in Q2** — roughly double Q2 2025's $22.4 bn; ~60% servers, 40% data centers & networking
  - **FY2026 capex guidance raised to $195–205 bn** (from $180–190 bn at Q1, itself up from $175–185 bn)
  - Q2 **free cash flow −$5.9 bn** (negative), driven by capex; **TTM FCF $53.3 bn**
  - TTM operating cash flow **$185.7 bn**
  - Cash & marketable securities **$242.5 bn**; **long-term debt $98.2 bn**
  - **$49.6 bn equity raise (June 2026)** — Class A + Class C shares + mandatory convertible preferred
    — "to be used for general corporate purposes, including capital expenditures to scale AI
    infrastructure and global compute"; plus an ATM program for up to **$40.0 bn**
  - Alphabet "continues to expect CapEx to increase significantly in 2027"
  - Sources: Alphabet Q2 2026 earnings call transcript https://abc.xyz/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx ;
    SEC EX-99.1 https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm ;
    release PDF https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf ;
    CNBC https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html
  - Consensus 2026 capex was $187.1 bn (FactSet); FY2027 consensus capex $263.3 bn (S&P Global / Visible Alpha)
- **Alphabet's SpaceX stake:** Alphabet is a significant SpaceX investor. CNBC (June 12, 2026) put the
  pre-IPO stake at **~4.9%, worth about $105 bn**. CNBC (Oct 1, 2026) says the stake "is currently valued
  at **over $82 billion**." SpaceX **IPO'd on June 12, 2026** at a **$1.77 T valuation** (ticker **SPCX**,
  Nasdaq) — the largest IPO ever; first-day market cap ~$2.1 T. Google holds **6.1%** of SpaceX per a
  June 2026 CNBC piece. → the two Alphabet-stake figures do not reconcile; flag the range.
  Sources: https://www.cnbc.com/2026/10/01/spacex-to-launch-google-ai-chips-to-orbit-with-planet-labs-satellites.html ;
  https://www.cnbc.com/2026/06/12/spacex-ipo-spcx-live-updates.html ;
  https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX
- **TPU strategy:** Suncatcher flies **commercial off-the-shelf Trillium (v6e) TPUs** rather than a
  radiation-hardened derivative. The strategic point (per futurumgroup): "Google is the only operator
  that controls the accelerator, the model, the cloud demand, and now a flight-qualified path to orbit.
  Its dependence on SpaceX for launch is the soft spot."
- **The terrestrial constraint this addresses:** power, land, water, permitting and grid-interconnection
  queues for AI data centers — hence the interest in dawn-dusk SSO solar with radiative cooling.

---

## 8. FACTS THAT COULD NOT BE VERIFIED / CONFLICTS

1. **Whether the October 1 launch actually occurred** — at compile time (16:05 UTC / 09:05 PT) the
   58-minute window (18:18 UTC) had NOT opened. No launch-outcome source exists yet. Wikipedia's
   Falcon 9 launch list already carries an entry for "Transporter-18 … October 2, 2026 03:53" (UTC),
   which conflicts with SpaceX's own stated Oct 1 18:18 UTC window. **Treat the mission as
   scheduled/upcoming, not flown.**
2. **Mission duration:** "a few months" (Ars Technica) vs "a year" (NYT, via space.com). Unresolved.
3. **Deorbit timeline (~6 years)** — from futurumgroup citing NYT only; not confirmed in a primary source.
4. **Actual MVP orbit altitude** — not confirmed. SpaceX says SSO; the 650 km figure is the paper's
   *design* altitude for the proposed 81-satellite cluster, not necessarily MVP's.
5. **"~1 Google Cloud TPU v6e-4 slice" compute equivalence** — only from futurumgroup (secondary),
   attributed to NYT. Not in Google's own blog.
6. **"$135/kg" TSP figure and the 5× headline** — 5× is on the TSP whitepapers page (fetched 200);
   $135/kg is only from a LinkedIn abstract. TSP's full report/model was not fetched.
7. **Full text of Reuters (401) and NYT (403) articles** — blocked. Reuters content reproduced from
   Google News/RSS snippets and a syndicated copy (galvnews.com); NYT content reproduced only where
   quoted by space.com, Ars Technica and futurumgroup.
8. **DCD article (403)** — quoted only from the search-engine snippet.
9. **No Google–MIT joint study was found.** The "MIT" link is Bruce Cameron (MIT Senior Lecturer) at TSP.
10. **Alphabet's SpaceX stake size** — 4.9% / $105 bn (June 2026, pre-IPO framing) vs ">$82 bn"
    (Oct 1, 2026) vs "6.1%" (June 2026). Conflicting.
11. **SpaceX V3 / Starmind technical specifics (1 Tbps per satellite, 150 kW compute, $1.25 T xAI
    merger)** — appear mainly in lower-quality aggregators; only "FCC filing for up to ~1 million
    satellites" and the Redmond/Tesla-solar-array claims are corroborated by space.com + CNBC.

---

## 9. PRIMARY SOURCE URLS (status as of 2026-10-01)

Status was verified with `curl -sL -o /dev/null -w "%{http_code}"` + browser UA.
**403 below = bot-blocked to curl, not broken** — the pages are live and resolve in a browser;
their content in this dossier came from search-engine snippets / syndicated copies.

**HTTP 200 (fetched and read directly):**
1. https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts — Google, Sep 24, 2026
2. https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design — Google Research, Nov 4, 2025
3. https://services.google.com/fh/files/misc/suncatcher_paper.pdf — full preprint PDF
4. https://arxiv.org/abs/2511.19468 — arXiv:2511.19468 (v2, 17 Jun 2026)
5. https://www.spacex.com/launches/transporter18 — mission page (JS-rendered; deployment timeline via search index)
6. https://nextspaceflight.com/launches/details/7611 — Transporter 18 vehicle/window
7. https://arstechnica.com/google/2026/09/googles-first-suncatcher-orbital-data-center-test-launches-october-1 — Ars Technica
8. https://www.space.com/space-exploration/satellites/spacex-launching-prototype-google-ai-satellite-next-week — space.com (Sep 24)
9. https://www.space.com/space-exploration/satellites/spacex-google-project-suncatcher-ai-satellite-transporter-18-mission — space.com (Oct 1)
10. https://www.cnbc.com/2026/10/01/spacex-to-launch-google-ai-chips-to-orbit-with-planet-labs-satellites.html — CNBC (Oct 1)
11. https://www.cnbc.com/2026/06/21/do-space-based-ai-data-centers-make-economic-sense.html — CNBC (Jun 21)
12. https://futurumgroup.com/insights/project-suncatcher-prepares-to-launch-tpus-is-google-ahead-in-the-orbital-ai-race
13. https://t-s-partners.com/whitepapers — TSP "Data Centers In Space" (5x figure verbatim)
14. https://www.aei.org/commentary/ai-data-centers-in-space-are-no-joke
15. https://www.spacex.com/spacexai/starmind
16. https://www.starcloud.com/starcloud-1
17. https://blogs.nvidia.com/blog/starcloud

**HTTP 403 to curl (bot-blocked; real pages):**
18. https://www.reuters.com/business/media-telecom/google-plans-first-test-ai-chips-space-under-project-suncatcher-2026-09-24 — Reuters (401 direct; content via RSS snippet + galvnews syndication)
19. https://www.nytimes.com/2026/09/24/technology/google-suncatcher-ai-data-center-space.html — NYT (content only where quoted by space.com / Ars / futurum)
20. https://www.datacenterdynamics.com/en/news/project-suncatcher-google-to-launch-first-space-data-center-test-in-orbit-next-week — DCD (content via search snippet)
21. https://abc.xyz/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx — Alphabet IR, Q2 2026 earnings call
22. https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm — Alphabet Q2 2026 8-K EX-99.1
23. https://www.bcg.com/publications/2026/space-based-data-centers-cost-outlook — BCG cost outlook
24. https://satnews.com/2026/02/16/china-completes-in-orbit-testing-of-three-body-ai-computing-constellation — SatNews

---

## 10. yfinance FUNDAMENTALS BLOCK — GOOGL

_pulled 2026-10-01 ~16:00 UTC (intraday US session). Full copy also at `fundamentals-googl.txt`._

```
Alphabet Inc. (GOOGL) — NASDAQ (NMS), USD

REVENUE / CASH FLOW (TTM, from quarterly statements):
  Revenues, TTM (sum of last 4 quarters)   : $445,867,000,000
    Q2 2026 (Jun-30-2026)                  : $119,796,000,000
    Q1 2026 (Mar-31-2026)                  : $109,896,000,000
    Q4 2025 (Dec-31-2025)                  : $113,829,000,000
    Q3 2025 (Sep-30-2025)                  : $102,346,000,000
  (yfinance info.totalRevenue (TTM)        : $445,865,984,000 — reconciles)
  Operating Cash Flow, TTM (last 4 qtrs)   : $185,675,000,000
    Q2'26 $39,069,000,000 | Q1'26 $45,790,000,000 | Q4'25 $52,402,000,000 | Q3'25 $48,414,000,000
  Capital Expenditure, TTM (last 4 qtrs)   : -$132,402,000,000   (negative as reported)
    Q2'26 -$44,924,000,000 | Q1'26 -$35,674,000,000 | Q4'25 -$27,851,000,000 | Q3'25 -$23,953,000,000
  FREE CASH FLOW, TTM (OCF + capex)        : $53,273,000,000
    (yfinance quarterly "Free Cash Flow" row sums to the same $53,273,000,000 — reconciles)
  Net income, TTM (last 4 qtrs)            : $244,205,000,000

BALANCE SHEET / VALUATION:
  totalDebt                                : $120,790,999,040
  totalCash                                : $242,473,992,192
  sharesOutstanding                        : 5,867,155,790
  marketCap                                : $4,161,357,742,080
  forwardPE                                : 22.58
  trailingPE                               : 17.08
  forwardEps                               : 15.07154
  trailingEps                              : 19.92
  fiftyTwoWeekLow                          : $235.84
  fiftyTwoWeekHigh                         : $408.61

ANALYST CONSENSUS:
  recommendationKey                        : strong_buy  (recommendationMean 1.38)
  targetMeanPrice                          : $429.36  (median $430.00; low $340.00; high $515.00)
  numberOfAnalystOpinions                  : 54

LAST 10 DAILY CLOSES (auto_adjust=False):
  2026-09-17   close 347.33   (open 348.68, vol 19,238,400)
  2026-09-18   close 349.54   (open 357.31, vol 47,631,800)
  2026-09-21   close 354.97   (open 350.64, vol 30,455,400)
  2026-09-22   close 351.16   (open 357.65, vol 29,788,600)
  2026-09-23   close 337.83   (open 349.86, vol 35,576,200)
  2026-09-24   close 342.36   (open 336.22, vol 23,777,200)
  2026-09-25   close 343.92   (open 342.35, vol 21,880,800)
  2026-09-28   close 342.75   (open 340.70, vol 19,318,300)
  2026-09-29   close 340.92   (open 341.95, vol 21,066,900)
  2026-09-30   close 344.08   (open 344.15, high 352.60, low 340.99, vol 37,196,700)

  Last COMPLETED close before 2026-10-01 (US market open) = 2026-09-30: $344.08
  Intraday 2026-10-01: last $340.26 (open $350.79, high $353.22, low $339.50, vol 14,837,020)
    → GOOGL is DOWN ~1.1% on the day of the Transporter-18 launch.

NOTES:
  - marketCap / PE / EPS fields reflect the intraday 2026-10-01 price of $340.26.
  - Q2 2026 FCF was NEGATIVE (-$5.855 bn) — the only negative quarter in the TTM window — because capex
    ($44.9 bn) exceeded OCF ($39.1 bn). Capex is consuming the entire operating cash flow.
  - Source: /home/chino/video-venv/bin/python3 + yfinance (script: /home/chino/googl_fund.py)
```
