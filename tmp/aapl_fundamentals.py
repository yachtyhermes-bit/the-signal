import json, yfinance as yf

t = yf.Ticker("AAPL")
info = t.info

keys = ["currentPrice","regularMarketPrice","marketCap","enterpriseValue","trailingPE","forwardPE","trailingEps",
        "grossMargins","operatingMargins","profitMargins","debtToEquity","totalDebt","totalCash",
        "freeCashflow","operatingCashflow","totalRevenue","revenueGrowth","earningsGrowth","sharesOutstanding",
        "floatShares","bookValue","priceToBook","dividendYield","dividendRate","beta","fiftyTwoWeekHigh",
        "fiftyTwoWeekLow","fiftyTwoWeekChange","targetMeanPrice","targetHighPrice","targetLowPrice",
        "recommendationKey","numberOfAnalystOpinions","sector","industry","longName","shortName","market",
        "exchange","financialCurrency","currency","totalCashPerShare","currentRatio","quickRatio","returnOnEquity",
        "returnOnAssets","totalAssets","totalLiabilities","longTermDebt","ebitda","evToEBITDA","evToRevenue"]

out = {}
for k in keys:
    v = info.get(k)
    if isinstance(v, float):
        v = round(v, 4)
    out[k] = v

print(json.dumps(out, indent=1))

# Quarterly financials for TTM calc
print("\n=== QUARTERLY (income statement) ===")
try:
    q = t.quarterly_income_stmt
    print(q.loc[["Total Revenue","Net Income","Gross Profit","Diluted EPS"]].to_string())
except Exception as e:
    print("q income err:", e)

print("\n=== QUARTERLY (cashflow) ===")
try:
    c = t.quarterly_cashflow
    print(c.loc[["Operating Cash Flow","Free Cash Flow","Capital Expenditure"]].to_string())
except Exception as e:
    print("q cf err:", e)

print("\n=== BALANCE SHEET (annual) ===")
try:
    b = t.balance_sheet
    print(b.loc[["Total Debt","Long Term Debt","Cash And Cash Equivalents","Total Assets","Stockholders Equity"]].to_string())
except Exception as e:
    print("bs err:", e)
