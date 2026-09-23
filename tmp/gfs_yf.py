import yfinance as yf, json, math
t = yf.Ticker("GFS")
out = {}
try:
    info = t.info
    keys = ["shortName","longName","currentPrice","previousClose","regularMarketPrice","marketCap","trailingPE","forwardPE","priceToBook","sharesOutstanding","floatShares","totalCash","totalDebt","freeCashflow","operatingCashflow","totalRevenue","grossMargins","operatingMargins","profitMargins","ebitdaMargins","revenueGrowth","earningsGrowth","dividendRate","dividendYield","payoutRatio","targetMeanPrice","targetHighPrice","targetLowPrice","targetMedianPrice","recommendationKey","recommendationMean","numberOfAnalystOpinions","fiftyTwoWeekHigh","fiftyTwoWeekLow","fiftyDayAverage","twoHundredDayAverage","beta","trailingEps","forwardEps","totalCashPerShare","enterpriseValue","earningsGrowth","country","sector","industry","fullTimeEmployees"]
    out["info"] = {k: info.get(k) for k in keys}
    out["info_all_keys_ok"] = True
except Exception as e:
    out["info_err"] = str(e)
try:
    h = t.history(period="12d", auto_adjust=False)
    out["history_12d"] = {str(i.date()): {"open":round(float(r["Open"]),4),"high":round(float(r["High"]),4),"low":round(float(r["Low"]),4),"close":round(float(r["Close"]),4),"adjclose":round(float(r["Adj Close"]),4),"volume":int(r["Volume"])} for i,r in h.iterrows()}
except Exception as e:
    out["hist_err"] = str(e)
try:
    h1 = t.history(period="1y", auto_adjust=False)
    out["hist_1y_rows"] = len(h1)
    out["hist_1y_low"] = {"close_min": round(float(h1["Close"].min()),4), "low_min": round(float(h1["Low"].min()),4), "date_low": str(h1["Low"].idxmin().date())}
    out["hist_1y_high"] = {"close_max": round(float(h1["Close"].max()),4), "high_max": round(float(h1["High"].max()),4), "date_high": str(h1["High"].idxmax().date())}
except Exception as e:
    out["hist1y_err"] = str(e)
print(json.dumps(out, indent=1, default=str))
