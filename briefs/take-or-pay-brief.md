# FACT BRIEF — Take-or-Pay Contracts: The Contract Structure Financing the AI Buildout
Prepared for The Signal (readthesignal.net) · Sunday weekly explainer · Analyst brief, 2026-09-13
Tickers: CRWV (main), pills CRWV / MSFT / NVDA

---

## A) ONE-PARAGRAPH ANGLE

Take-or-pay contracts are the legal device that converted AI demand forecasts into investment-grade-looking cash flows, and the article's thesis is that they relocate risk rather than remove it. Compute sellers insist on them and lenders finance against them because GPUs and purpose-built campuses are single-purpose assets with no second act, while buyers sign because capacity, not price, has been the binding constraint. The payoff for the reader is learning to trace that risk through the specific disclosure lines where it actually sits: remaining performance obligations, purchase obligations, customer prepayments, and off-balance-sheet residual-value guarantees.

---

## B) VERIFIED FIGURE TABLE

| figure | what it measures | source URL | source date | verified how |
|---|---|---|---|---|
| "committed contracts, which are take-or-pay" vs "on-demand, which is pay-as-you-go" | Seller's own taxonomy of its two revenue models | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm | filed 2026-03-02 | curl 200, SEC EDGAR, full text parsed |
| "We primarily finance our infrastructure development through asset-level debt supported by take-or-pay customer contracts" | Direct link between contract structure and borrowing capacity | same 10-K as above | filed 2026-03-02 | curl 200, full text parsed |
| 98% of revenue from committed (take-or-pay) contracts, Q2 2026 | Share of reported revenue protected by minimum-payment terms | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm | filed 2026-08-12 | curl 200, full text parsed |
| Weighted-average prepayment across active contracts = 15%–25% of total contract value (as of Dec 31, 2025, 2024, 2023) | Typical upfront cash a buyer must hand over before receiving service | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm | filed 2026-03-02 | curl 200, full text parsed |
| $103.7B unsatisfied RPO as of June 30, 2026; 41% expected within 24 months, 39% in months 25–48 | Contracted revenue not yet delivered, and its conversion schedule | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm | filed 2026-08-12 | curl 200, full text parsed |
| ~$104B revenue backlog as of June 30, 2026, excluding $25B+ of net new customer commitments added in early Q3 | Company's headline backlog, defined as RPO plus estimated future amounts under committed contracts | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000362/coreweave2q26earningspress.htm | 2026-08-11 | curl 200, SEC EDGAR exhibit |
| Deferred revenue $9.7B (Jun 30, 2026) vs $8.2B (Dec 31, 2025); contract assets $179M | Cash already collected but not yet recognized as revenue | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm | filed 2026-08-12 | curl 200, full text parsed |
| Customer A = 36% of revenue, Customer B = 26%, Customer C = 10% in Q2 2026 | Revenue concentration | same 10-Q as above | filed 2026-08-12 | curl 200, full text parsed |
| Microsoft = ~67% of revenue for FY2025 | Single-counterparty dependence | https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm | filed 2026-03-02 | curl 200, full text parsed |
| Oracle RPO $664B as of Aug 31, 2026, up $209B YoY; "booked more than $30 billion of additional AI cloud contracts in Q1" | Contracted future revenue for a hyperscaler-scale seller | https://www.sec.gov/Archives/edgar/data/1341439/000119312526387905/orcl-ex99_1.htm | 2026-09-10 | curl 200, SEC EDGAR exhibit |
| Oracle deferred revenue from "customer prepayments with significant financing component" increased $11,363M in Q1 FY27 | Scale of buyer cash advanced before delivery, large enough to warrant a financing-component label | same Oracle Q1 FY27 exhibit | 2026-09-10 | curl 200, full text parsed |
| Oracle FY2026 free cash flow negative $23.7B; FY26 capex $55.7B; raised $43B debt and $5B equity in FY26 | Cost of funding the capacity that the contracts require | https://www.sec.gov/Archives/edgar/data/1341439/000119312526265848/orcl-ex99_1.htm | 2026-06-10 | curl 200, SEC EDGAR exhibit |
| Oracle RPO $638B at May 31, 2026, up 363% YoY from $138B, up $85B sequentially from $553B | Growth rate of contracted obligations | same Oracle Q4 FY26 exhibit | 2026-06-10 | curl 200, SEC EDGAR exhibit |
| Microsoft "Purchase commitments" $194.06B total, of which $169.0B due in FY2027; footnote (d): "primarily relate to datacenters and include open purchase orders and take-or-pay contracts that are not presented as construction commitments" | The buyer-side obligation disclosed in the notes | https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm | filed 2026-07-29 | curl 200, SEC EDGAR, full text parsed |
| Microsoft operating and finance leases, including imputed interest: $443.5B total ($32.4B in FY2027) | Off-balance-sheet-looking but disclosed long-term capacity cost | same Microsoft FY2026 10-K | filed 2026-07-29 | curl 200, full text parsed |
| Nvidia order for CoreWeave residual capacity: initial value $6.3B; "in instances where the Company's datacenter capacity is not fully utilized by its own customers, NVIDIA is obligated to purchase the residual unsold capacity through April 13, 2032" | Supplier-side backstop of the seller's utilization risk | https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm | filed 2025-09-15 | curl 200, SEC EDGAR, full text parsed |
| OpenAI "contracted to purchase an incremental $250B of Azure services"; Microsoft gave up right of first refusal | Buyer-side take-or-pay-style commitment at hyperscaler scale | https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership | 2025-10-28 | curl 200, full text parsed |
| Meta Hyperion SPV: $30B total — Beignet Investor LLC co-owned Meta 20% / Blue Owl 80%, ~$27B loans (Pimco, BlackRock, Apollo) + ~$3B equity; Meta gave a residual value guarantee of up to ~$28B "described only in footnotes to Meta's most recent annual report and for which no liability has been recorded" | Off-balance-sheet project financing of an AI campus and the guarantee that makes it investment grade | https://www.quinnemanuel.com/the-firm/publications/client-alert-emerging-litigation-risks-in-financing-ai-data-centers-boom | 2026 (law-firm client alert) | curl 200, full text parsed |
| CoreWeave revenue backlog $55.6B at Sept 30, 2025, up 271% YoY; FY2025 outlook lowered on customer-related capacity delay | Backlog growth decoupled from near-term conversion | https://s205.q4cdn.com/133937190/files/doc_financials/2025/q3/Earnings-Deck-2025-Q3.pdf | 2025-11-10 | curl 200, company-hosted PDF |
| Duke Energy large-load tariff proposal: data centers "would pay a minimum bill amount for at least a decade, no matter their actual power use," at ≥75% of maximum potential energy use | Take-or-pay logic arriving on the utility/power side of the stack | https://www.canarymedia.com/articles/data-centers/duke-energy-proposes-special-rules-for-data-centers-in-north-carolina | 2026-07 | curl 200, full text parsed |
| S&P Global Ratings downgraded Oracle to 'BBB-/A-3' from 'BBB/A-2' (2026-07-09), citing aggressive AI spending and customer concentration; S&P text: "Despite recent contract terms requiring customer prepayments, Oracle's strong RPO growth…"; downgrade triggers include leverage >4.5x and no positive FOCF by FY2029 | Counterparty/credit-rating response to concentration | https://www.spglobal.com/ratings/en/regulatory/article/-/view/sourceId/101695609 | 2026-07-09 | curl 403 (paywalled, not 404); rating-action language confirmed via S&P's own published summary text surfaced in search and corroborated by multiple outlets |
| OpenAI accounts for roughly half of Oracle's $638B RPO (analyst estimate; S&P cited concentration explicitly) | The concentration that makes the take-or-pay chain fragile | https://finance.yahoo.com/markets/stocks/articles/oracles-638-billion-backlog-meets-144300499.html | 2026 | curl-checked via search index; estimate is analyst-derived, not company-disclosed — treat as attributed estimate, not a verified company figure |

**Not verified / excluded:** any "CoreWeave $115B payment backlog" figure (a social-media construct of adding long-dated lease commitments to revenue backlog — do not use). Any Nvidia–OpenAI "$100B investment" figure as a *backstop* (it was announced as an investment, 2025-09; framing it as residual-value support is NOT supported by a primary source I fetched). Any specific "Nvidia guarantees X% of CoreWeave lease payments" claim — reported by Business Insider in 2026-02, but I did not fetch the underlying primary document. **UNVERIFIED — DO NOT USE** for any specific percentage of lease backstop beyond the $6.3B residual-capacity order.

---

## C) KEY TERMS

**Take-or-pay contract** — An agreement in which the buyer must pay for a reserved amount of capacity whether or not it actually uses it. The seller gets a predictable revenue stream; the buyer absorbs the demand risk.

**RPO / backlog** — Remaining performance obligations are the contracted revenue a company has not yet delivered or billed, and they include both deferred revenue and amounts not yet invoiced; "backlog" is usually RPO plus additional amounts management estimates from committed contracts, which is why the two numbers rarely match.

**Prepayment** — Cash a buyer hands over up front, before receiving the service. It shows up as deferred revenue on the seller's balance sheet and as a use of cash on the buyer's, and CoreWeave's typical prepayment runs 15%–25% of total contract value.

**Capacity reservation** — Buying guaranteed access to a specific amount of compute for a set term, rather than buying usage on demand. It is what makes a take-or-pay clause meaningful, because the seller has to build the capacity before the buyer pays for it.

**Counterparty risk** — The risk that the company on the other side of a contract cannot pay. In a take-or-pay structure the seller's revenue is only as good as the buyer's balance sheet and continued access to capital.

**Off-balance-sheet / SPV** — A special purpose vehicle is a separate legal entity, often co-owned by the sponsor and investors, that owns and borrows for a project so the debt does not appear on the sponsor's balance sheet. The sponsor's lease and residual-value guarantee usually carry the credit instead.

---

## D) BOTTOM LINE

Take-or-pay contracts do not eliminate AI demand risk; they relocate it. Sellers like CoreWeave convert an uncertain market into a contractual revenue stream, and lenders finance billion-dollar campuses against that paper. But the obligation only holds if the buyer keeps paying, and today the largest buyers are loss-making AI labs and hyperscalers booking enormous purchase commitments of their own. The disclosures are the tell: purchase obligations in the footnotes, prepayments undercutting reported free cash flow, and residual-value guarantees that stay off the balance sheet until they don't. Read the contract, not the backlog headline.

*(94 words)*

---

## E) TITLES

**Candidates**
1. The Take-or-Pay Machine: How AI Compute Deals Shift Demand Risk
2. Take-or-Pay Contracts Explain Why AI Backlogs Are Not Guaranteed Cash
3. Read the Purchase-Obligation Footnote Before Trusting AI Backlog Numbers
4. Take-or-Pay Contracts Rewrite Who Owns AI Demand Risk
5. Take-or-Pay Contracts Are the AI Buildout's Quiet Risk Transfer

**Subtitle (37 words)**
AI's largest compute deals are signed as take-or-pay contracts, which move demand risk from the seller to the buyer. The disclosures that matter sit in purchase obligations, remaining performance obligations, and prepayments rather than in headline backlog.

**Summary (61 words)**
Take-or-pay contracts require a buyer to pay for reserved compute whether or not it uses it. That structure lets AI infrastructure sellers borrow against contracted revenue and push demand risk onto customers. It also explains why backlog can exceed recognized revenue and why purchase obligations and prepayments now matter more than headline contract values when judging who actually bears the downside.

---

## F) SIX SOURCE LINKS (all confirmed; 200 unless noted)

1. **CoreWeave FY2025 Form 10-K** — take-or-pay definition, asset-level debt, prepayment range (15%–25% of TCV), Microsoft 67% concentration, $60.7B RPO
   https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm — curl 200
2. **CoreWeave Q2 2026 Form 10-Q** — 98% of revenue from take-or-pay contracts, $103.7B RPO with conversion schedule, $9.7B deferred revenue, customer concentration table
   https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm — curl 200
3. **Oracle Q1 FY2027 Form 8-K, Exhibit 99.1** — RPO $664B (+$209B YoY), >$30B new AI cloud contracts booked, $11.36B increase in deferred revenue from customer prepayments with a financing component
   https://www.sec.gov/Archives/edgar/data/1341439/000119312526387905/orcl-ex99_1.htm — curl 200
4. **Microsoft FY2026 Form 10-K** — "Purchase commitments" $194.1B including "take-or-pay contracts", leases $443.5B, and the risk factor on overestimating AI demand
   https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm — curl 200
5. **CoreWeave Form 8-K (Sept 2025)** — Nvidia's $6.3B obligation to purchase residual unsold capacity through April 13, 2032
   https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm — curl 200
6. **Quinn Emanuel client alert, AI data center financing litigation risks** — Meta Hyperion $30B SPV (Beignet Investor, Meta 20% / Blue Owl 80%), ~$28B residual value guarantee with no recorded liability, private-credit tranches, rating-action and litigation exposure
   https://www.quinnemanuel.com/the-firm/publications/client-alert-emerging-litigation-risks-in-financing-ai-data-centers-boom — curl 200

**Verified spares (use if a link is dropped at edit time):**
- Microsoft corporate blog, "The next chapter of the Microsoft–OpenAI partnership", 2025-10-28 — OpenAI's incremental $250B Azure purchase — https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership — curl 200
- Oracle Q4 FY2026 Form 8-K, Exhibit 99.1 — RPO $638B, FY26 FCF –$23.7B — https://www.sec.gov/Archives/edgar/data/1341439/000119312526265848/orcl-ex99_1.htm — curl 200
- Moody's Ratings, "Power without delivery" (private credit / AI infrastructure), 2026-07-31 — hyperscaler capex approaching $785B in 2026 — https://www.moodys.com/web/en/us/insights/credit-risk/private-credit/power-without-delivery.html — curl 200
- S&P Global Ratings, Oracle downgraded to 'BBB-/A-3', 2026-07-09 — https://www.spglobal.com/ratings/en/regulatory/article/-/view/sourceId/101695609 — curl 403 (paywalled; never 404)
- Canary Media on Duke Energy's large-load tariff, 2026-07 — utilities copying take-or-pay logic — https://www.canarymedia.com/articles/data-centers/duke-energy-proposes-special-rules-for-data-centers-in-north-carolina — curl 200

---

## G) BEAT OUTLINE (700–800 words, hook first, no stats-lede)

1. **Hook — the contract nobody reads.** Open on the sentence buried in a filing that says a customer must pay for reserved compute whether or not it uses it. No numbers yet: frame the tension that a business whose product did not exist five years ago is being financed on electricity-style, multi-decade obligations. Establish that the point of this piece is contract mechanics, not any one company's quarter.

2. **What take-or-pay actually is.** Define it plainly: a minimum payment for reserved capacity, not a purchase of delivered output. Distinguish it from take-and-pay, note the "make-up" right that lets a shortfall be taken later, and explain why the clause exists at all — the seller must build the asset before the buyer needs it, and the asset has no second use. Anchor on the seller's own filing language and the 98%-of-revenue figure. One date anchor here.

3. **Why the money insists on it.** Move to the lender's and landlord's seat. Asset-level debt is sized off contracted cash flow, so a take-or-pay contract is what converts a speculative build into a financeable one. Bring in prepayments (15%–25% of contract value), the utility analogue where a data center must pay a minimum bill regardless of consumption, and the SPV structure where the sponsor's guarantee, not the asset, carries the credit.

4. **How it hides in the numbers, part one: RPO and backlog.** Explain remaining performance obligations as a GAAP-governed disclosure, why "backlog" is a looser company definition that runs larger than RPO, and why neither is cash. Show the conversion schedule — how much of the obligation is expected to be recognized inside 24 months — and note that a long tail of RPO is closer to an aspiration than a receivable.

5. **How it hides in the numbers, part two: purchase obligations and prepayments.** Cover the buyer side. Purchase commitments in the notes to the financial statements explicitly include take-or-pay contracts, and they are large. Cover deferred revenue versus RPO, and the signal that customer prepayments are big enough to be booked as a financing component — which is cash in the door today against an obligation to deliver later.

6. **Who bears the downside.** Name it directly. Demand risk now sits with the buyer, but the buyer's ability to pay is the unstated variable — and the largest buyers are unprofitable AI labs whose own funding depends on the market continuing. Bring in the rating-agency response: concentration flagged as a credit risk, and the guarantee that sits in a footnote with no liability recorded against it.

7. **The counter-case, factually.** Where the structure has already been tested: guidance cut on a capacity delivery delay rather than a customer exit, hyperscalers trimming their own lease pipeline, and the seller's own risk language about overestimating demand and impairing infrastructure. Be precise that these are early stress signals, not defaults — overstating them would be wrong.

8. **Close — what to watch.** Land the takeaway that take-or-pay is a risk-transfer instrument, not a risk-elimination one, and that the honest test of any AI infrastructure story is the conversion schedule, the counterparty's balance sheet, and what the notes disclose rather than what the press release headlines. Point forward to how the utility, private-credit and hyperscaler layers are now replicating the same clause.
