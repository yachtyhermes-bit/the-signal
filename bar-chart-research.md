# Bar Chart Research for The Signal Stock Pages

## 1. Current State

### What exists now (Overview tab):
- **OHLC Heikin-Ashi candlestick chart** — LightweightCharts, main chart
- **Volume histogram** — LightweightCharts histogram below the candlestick chart
- **Key metrics boxes** — Market Cap, P/E, 52W Range, Volume, Beta

### What exists now (Financials tab — div-based HTML/CSS bars, NOT LightweightCharts):
- **Income Statement bars** — Total Revenues vs Net Income per quarter/annum
- **Balance Sheet bars** — Total Assets vs Total Liabilities per quarter/annum

Both are **hand-rolled div bars**, not LightweightCharts series. They have no crosshair interaction, no zoom, no click detail.

## 2. Data Already in financials.json (zero API cost)

The `quarterlyFinancials` object per ticker contains:
| Field | Description | Tickers Available |
|---|---|---|
| `revenue[]` | Quarterly revenue, actual + estimated (0q, +1q) | All 19 |
| `netIncome[]` | Quarterly net income, actual | All 19 |
| `eps[]` | Quarterly EPS actual + estimated | All 19 |
| `ebit[]` | Quarterly EBIT | All 19 |
| `totalAssets[]` | Quarterly total assets | All 19 |
| `totalLiabilities[]` | Quarterly total liabilities | All 19 |
| `segmentData.segments[]` | Revenue breakdown by business segment | NVDA, TSLA, AMZN, PLTR, RKLB |

### Data available from yfinance but NOT yet fetched:
| Field | Source | Notes |
|---|---|---|
| Gross Profit (quarterly) | `quarterly_income_stmt['Gross Profit']` | Available, not in quarterlyFinancials |
| Operating Income (quarterly) | `quarterly_income_stmt['Operating Income']` | Available, only in stats as TTM |
| R&D / SG&A (quarterly) | `quarterly_income_stmt['Research And Development', 'Selling General And Administration']` | Not fetched |
| Free Cash Flow (quarterly) | `quarterly_cash_flow['Free Cash Flow']` | Not fetched quarterly |
| Operating Cash Flow (quarterly) | `quarterly_cash_flow['Operating Cash Flow']` | Not fetched quarterly |
| CapEx (quarterly) | `quarterly_cash_flow['Capital Expenditure']` | Not fetched quarterly |
| Diluted EPS (quarterly) | `quarterly_income_stmt['Diluted EPS']` | More precise than earnings estimates |

## 3. LightweightCharts Bar Chart Support

LightweightCharts 4.x supports these relevant series types:
- **HistogramSeries** — Vertical bars, perfect for single-value bar charts (revenue, net income, FCF). Supports color per bar (green for up, red for down).
- **BarSeries** — OHLC bars (open/high/low/close), already used via candlestick. Not useful for financial bar charts.
- **LineSeries** — Trend lines (could overlay on histogram for estimates/guidance).
- **BaselineSeries** — Area with fill above/below a baseline (good for showing positive/negative values).

**What LightweightCharts does NOT support natively:**
- Grouped/clustered bars (side-by-side bars for Rev vs Net Income)
- Stacked bars (segment breakdown over time)
- Categorical x-axis (it requires time-based x-axis)

**Workaround options:**
1. For single-metric bars: `HistogramSeries` works perfectly — use it.
2. For "actual vs estimated" (two bars): Overlay two HistogramSeries at slightly different x-offsets, or use HistogramSeries + LineSeries.
3. For grouped/stacked bars: Keep the existing div-based approach (it's actually fine for the Financials tab).
4. For segment breakdown: Could use multiple HistogramSeries stacked (manual stacking) or keep div-based.

## 4. Recommended Bar Charts — Prioritized

### TIER 1 (P0) — Data already available, high visual value, low effort

#### 1. EPS Actual vs Estimate (Quarterly Bar Chart)
- **Data source**: `quarterlyFinancials.eps[]` — already has `actual` and `estimated` per quarter
- **Chart type**: HistogramSeries (bars) for actual EPS + LineSeries for estimate line
- **Value**: Shows earnings beats/misses visually — the most important metric for investors
- **Effort**: Low (~1-2 hours)
  - Add a new `<div id="epsChart">` in the Overview tab
  - ~30 lines of JS in stock-chart.js
  - Color green for beat, red for miss
- **Placement**: Overview tab, below the price chart
- **Rendering**: LightweightCharts HistogramSeries

#### 2. Revenue by Segment (Stacked Bar Chart) — for tickers that have it
- **Data source**: `segmentData.segments[]` — already fetched for NVDA, TSLA, AMZN, PLTR, RKLB
- **Chart type**: Div-based stacked horizontal or vertical bars
- **Value**: Shows which business segments are driving growth (e.g., NVDA Data Center vs Gaming)
- **Effort**: Low (~2 hours)
  - Add new section in Overview tab, visible only when segment data exists
  - Use stacked div bars (like the Financials tab pattern)
  - Color-coded by segment with legend
- **Placement**: Overview tab or new "Segments" section
- **Note**: LightweightCharts doesn't do native stacked bars — div-based is the pragmatic choice

#### 3. Free Cash Flow & Operating Cash Flow (Quarterly Bar Chart)
- **Data source**: Needs adding — `quarterly_cash_flow['Free Cash Flow']` and `['Operating Cash Flow']` from yfinance
- **Chart type**: Dual HistogramSeries (FCF bars + OCF bars), or a combined chart
- **Value**: Cash flow tells the real story — high insider value for readers
- **Effort**: Low (~1-2 hours)
  - Add ~15 lines in fetch-financials.py to pull quarterly FCF/OCF
  - Add ~30 lines in stock-chart.js
- **Placement**: Overview tab or Financials tab
- **Color coding**: Green for positive FCF, red for negative

### TIER 2 (P1) — Minor data additions, good value

#### 4. Revenue vs Revenue Estimates (Bar + Line)
- **Data source**: `quarterlyFinancials.revenue[]` — already has actual and estimated
- **Chart type**: HistogramSeries (actual revenue) + LineSeries (estimate) or overlaid bar
- **Value**: Shows guidance performance — did the company beat revenue estimates?
- **Effort**: Low (~1 hour)
- **Note**: Most tickers only have 0q/+1q estimates, so this is a simpler version of the EPS chart

#### 5. Gross Margin & Operating Margin Trend
- **Data source**: Needs computing from quarterly income statement (Gross Profit / Revenue; Operating Income / Revenue)
- **Chart type**: LineSeries (two lines, one for gross margin %, one for operating margin %)
- **Value**: Shows profitability trajectory — margin compression/expansion is a key signal
- **Effort**: Medium (~2-3 hours)
  - Add quarterly margin computation in fetch-financials.py
  - Add LineSeries chart in stock-chart.js
- **Placement**: Overview tab, could share space with revenue bar chart

#### 6. Revenue Bar Chart (Overview tab copy)
- **Data source**: Already in quarterlyFinancials.revenue
- **Chart type**: LightweightCharts HistogramSeries
- **Value**: Quick visual of revenue trajectory without clicking to Financials tab
- **Effort**: Low (~1 hour)
- **Note**: Already exists in Financials tab in div form. Moving a copy to Overview as a LightweightCharts histogram would increase discoverability.

### TIER 3 (P2) — Nice-to-have

#### 7. R&D vs SG&A (Expense Breakdown)
- **Data source**: `quarterly_income_stmt['Research And Development']` and `['Selling General And Administration']`
- **Chart type**: Stacked bars or overlaid bars
- **Value**: Shows investment in innovation vs overhead
- **Effort**: Medium (~3 hours, adding data + chart)

#### 8. Debt vs Cash / Net Debt Trend
- **Data source**: `quarterlyFinancials.totalAssets/liabilities` or stats.totalDebt/totalCash
- **Chart type**: HistogramSeries showing net debt trend
- **Value**: Balance sheet health visualization
- **Effort**: Low (~1 hour, data already there)

#### 9. CapEx & Buybacks (Capital Allocation)
- **Data source**: `quarterly_cash_flow['Capital Expenditure']` and `['Repurchase Of Capital Stock']` from yfinance
- **Chart type**: Shared bar chart
- **Value**: Shows how company invests/shareholder returns
- **Effort**: Medium (~3 hours, adding data + chart)

## 5. Implementation Approach

### Recommended architecture:
```
stock-chart.js ── initMainChart()          // existing OHLC candlestick
                ── initEpsChart()          // NEW: EPS actual vs estimate bars
                ── initRevenueChart()      // NEW: Revenue bar chart (overview)
                ── initSegmentChart()      // NEW: Segment breakdown (if data exists)
                ── initCashFlowChart()     // NEW: FCF/OCF bars
                ── initFinChart()          // existing Financials tab bars
```

### Data flow:
1. `fetch-financials.py` — already runs on deploy, adds quarterly data to financials.json
2. `build-stock-page.js` — already embeds `quarterly` data into page JS
3. `stock-chart.js` — reads embedded data, renders charts client-side

No changes needed to the backend pipeline. Only changes needed:
- `fetch-financials.py` — for P1 charts that need new data sources (cash flow, margins)
- `build-stock-page.js` — pass additional data fields to the embedded JS object
- `stock-chart.js` — add new chart init functions
- `stock-card.css` — minimal layout additions

### LightweightCharts vs Div-based decision:

| Chart Type | Recommended Approach | Reason |
|---|---|---|
| Single metric bars (revenue, FCF) | LightweightCharts HistogramSeries | Interactive, crosshair, consistent UX |
| Actual vs estimated | HistogramSeries + LineSeries overlay | Shows comparison clearly |
| Grouped bars (Rev vs NI side-by-side) | Keep div-based | LightweightCharts doesn't support grouping |
| Stacked bars (segment breakdown) | Div-based | No native stacked bar in LC |
| Margin trends (%, over time) | LightweightCharts LineSeries | Multiple lines, time-based data |
| Capital allocation | LightweightCharts combo | Time-based, mix of bars and lines |

## 6. Recommendation Summary

### Do first (highest ROI, minimal effort):
1. **EPS Actual vs Estimate bar chart** (P0, ~2h) — data already embedded, huge value
2. **Segment Revenue stacked bars** (P0, ~2h) — data already there for 5 key tickers
3. **Revenue overview bar chart** (P1, ~1h) — LightweightCharts histogram in Overview tab

### Do second (still high value, need minor data additions):
4. **Free Cash Flow quarterly bars** (P1, ~2h) — needs 10 lines in fetch-financials.py
5. **Margin trend lines** (P1, ~3h) — needs quarterly margin computation

### Defer:
6. Expense breakdown, debt/cash, CapEx/buybacks — niche charts, lower reader engagement

### Total estimated effort: ~10 hours for all 6 recommendations
### Data changes needed: Only ~25 lines added to fetch-financials.py
### No new API keys or external costs
