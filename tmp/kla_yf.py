import yfinance as yf, pandas as pd, json, datetime as dt

pd.set_option('display.width', 250)
pd.set_option('display.max_columns', 40)

out = []

def sec(s):
    out.append("\n" + "="*90)
    out.append(s)
    out.append("="*90)

# 1. Weekly closes Oct 16 and Oct 23 for tickers
sec("WEEKLY MOVES Fri 2026-10-16 close -> Fri 2026-10-23 close (auto_adjust=False)")
tick = ['KLAC','LRCX','AMAT','SOXX','NVDA','^SOX','ASML','ONTO','^IXIC']
for t in tick:
    try:
        df = yf.Ticker(t).history(start='2026-10-01', end='2026-10-26', auto_adjust=False)
        if df.empty:
            out.append(f"{t}: EMPTY")
            continue
        df.index = [d.strftime('%Y-%m-%d') for d in df.index]
        out.append(f"\n--- {t} ---")
        out.append(df[['Open','High','Low','Close','Volume']].round(2).to_string())
        c = df['Close']
        if len(c) >= 2:
            a = c.iloc[-2]; b = c.iloc[-1]
            out.append(f"LAST TWO CLOSES: {c.index[-2]}={a:.2f}  {c.index[-1]}={b:.2f}  chg={b-a:+.2f} ({(b/a-1)*100:+.2f}%)")
        # explicit oct16 and oct23
        try:
            x = c.loc['2026-10-16']; y = c.loc['2026-10-23']
            out.append(f"OCT16={x:.2f} OCT23={y:.2f} WEEK={((y/x)-1)*100:+.2f}%  abs={y-x:+.2f}")
        except Exception as e:
            out.append(f"oct16/23 lookup fail: {e}")
    except Exception as e:
        out.append(f"{t} ERROR {e}")

# 2. 1-year history for KLAC -> 52w low/high
sec("KLAC 1-YEAR RANGE (auto_adjust=False), window 2025-10-25 .. 2026-10-25")
df = yf.Ticker('KLAC').history(start='2025-10-25', end='2026-10-26', auto_adjust=False)
out.append(f"rows={len(df)}")
h = df['High']; l = df['Low']; cl = df['Close']
out.append(f"MAX HIGH = {h.max():.4f} on {h.idxmax()}")
out.append(f"MIN LOW  = {l.min():.4f} on {l.idxmin()}")
last = cl.iloc[-1]; lastd = cl.index[-1]
out.append(f"LAST CLOSE = {last:.4f} on {lastd}")
out.append(f"% off 52w high = {(last/h.max()-1)*100:.2f}%")
out.append(f"% above 52w low = {(last/l.min()-1)*100:.2f}%")
# monthly closes
m = cl.resample('ME').last()
out.append("\nMONTHLY CLOSES (last 14):")
out.append(m.tail(14).round(2).to_string())
out.append("\nLAST 15 DAILY CLOSES:")
out.append(cl.tail(15).round(2).to_string())

# 3. info
sec("INFO")
tk = yf.Ticker('KLAC')
info = tk.info
keys = ['longName','marketCap','enterpriseValue','forwardPE','trailingPE','forwardEps','trailingEps',
        'sharesOutstanding','floatShares','fiftyTwoWeekLow','fiftyTwoWeekHigh','allTimeHigh',
        'currentPrice','previousClose','regularMarketPrice','recommendationKey','recommendationMean',
        'numberOfAnalystOpinions','targetMeanPrice','targetMedianPrice','targetHighPrice','targetLowPrice',
        'totalRevenue','freeCashflow','operatingCashflow','totalDebt','totalCash','ebitda',
        'dividendRate','dividendYield','trailingAnnualDividendRate','beta','fullTimeEmployees',
        'priceToSalesTrailing12Months','enterpriseToEbitda','returnOnEquity','grossMargins','operatingMargins','profitMargins','bookValue','priceToBook']
for k in keys:
    out.append(f"{k:38s} {info.get(k)}")

# 4. calendar
sec("CALENDAR")
try:
    out.append(str(tk.calendar))
except Exception as e:
    out.append(f"cal err {e}")

# 5. quarterly financials
sec("QUARTERLY INCOME STATEMENT (raw)")
qf = tk.quarterly_financials
out.append(str(qf.round(1)))
out.append("\nQUARTERLY income stmt (transposed, key rows)")
rows = ['Total Revenue','Gross Profit','Operating Income','Net Income','Diluted EPS','Basic EPS']
for r in rows:
    if r in qf.index:
        out.append(f"\n{r}: ")
        out.append(qf.loc[r].round(3).to_string())

sec("ANNUAL INCOME STATEMENT")
af = tk.financials
for r in ['Total Revenue','Gross Profit','Operating Income','Net Income','Diluted EPS']:
    if r in af.index:
        out.append(f"\n{r}: ")
        out.append(af.loc[r].round(3).to_string())

sec("QUARTERLY CASHFLOW")
qc = tk.quarterly_cashflow
out.append(str(qc.round(1)))

sec("ANNUAL CASHFLOW")
ac = tk.cashflow
for r in ['Operating Cash Flow','Capital Expenditure','Free Cash Flow','Repurchase Of Capital Stock','Cash Dividends Paid']:
    if r in ac.index:
        out.append(f"\n{r}: ")
        out.append(ac.loc[r].round(1).to_string())

sec("QUARTERLY BALANCE SHEET")
qb = tk.quarterly_balance_sheet
for r in ['Cash And Cash Equivalents','Cash Cash Equivalents And Short Term Investments','Total Debt','Long Term Debt','Current Debt','Net Debt','Stockholders Equity','Total Assets']:
    if r in qb.index:
        out.append(f"\n{r}: ")
        out.append(qb.loc[r].round(1).to_string())

sec("ANNUAL BALANCE SHEET")
ab = tk.balance_sheet
for r in ['Cash And Cash Equivalents','Cash Cash Equivalents And Short Term Investments','Total Debt','Long Term Debt','Net Debt','Stockholders Equity']:
    if r in ab.index:
        out.append(f"\n{r}: ")
        out.append(ab.loc[r].round(1).to_string())

sec("SPLITS / DIVIDENDS")
try:
    out.append(str(tk.splits.tail(6)))
except Exception as e: out.append(str(e))

sec("EARNINGS DATES")
try:
    out.append(str(tk.earnings_dates.head(12)))
except Exception as e:
    out.append(f"err {e}")

sec("TTM COMPUTATION")
qrev = qf.loc['Total Revenue'].dropna().sort_index(ascending=False)
out.append("Last 4 quarterly revenues (newest first):")
out.append(qrev.head(6).to_string())
out.append(f"SUM of newest 4 = {qrev.head(4).sum():,.0f}")
qocf = qc.loc['Operating Cash Flow'].dropna().sort_index(ascending=False) if 'Operating Cash Flow' in qc.index else None
qcapex = qc.loc['Capital Expenditure'].dropna().sort_index(ascending=False) if 'Capital Expenditure' in qc.index else None
if qocf is not None and qcapex is not None:
    out.append("\nOCF newest 4 (newest first):")
    out.append(qocf.head(6).to_string())
    out.append("\nCapex newest 4 (newest first) -- NOTE often NEGATIVE:")
    out.append(qcapex.head(6).to_string())
    out.append(f"\nTTM OCF sum = {qocf.head(4).sum():,.0f}")
    out.append(f"TTM Capex sum = {qcapex.head(4).sum():,.0f}")
    out.append(f"TTM FCF (OCF+capex) = {qocf.head(4).sum()+qcapex.head(4).sum():,.0f}")

txt = "\n".join(str(x) for x in out)
open('/home/chino/thesignal/tmp/kla_yf_2026-10-25.txt','w').write(txt)
print(txt)
