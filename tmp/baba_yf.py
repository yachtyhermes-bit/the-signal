import yfinance as yf, json
out={}
for t in ["BABA","9988.HK","BABA.MX"]:
    try:
        tk=yf.Ticker(t)
        info=tk.info
        fast=tk.fast_info
        out[t]={"info":{k:info.get(k) for k in ["shortName","longName","currentPrice","previousClose","regularMarketPrice","regularMarketPreviousClose","marketCap","enterpriseValue","trailingPE","forwardPE","priceToSalesTrailing12Months","priceToBook","sharesOutstanding","totalRevenue","revenueGrowth","grossMargins","operatingMargins","profitMargins","ebitda","freeCashflow","totalCash","totalDebt","debtToEquity","returnOnEquity","fiftyTwoWeekHigh","fiftyTwoWeekLow","fiftyDayAverage","twoHundredDayAverage","targetMeanPrice","targetHighPrice","targetLowPrice","numberOfAnalystOpinions","recommendationKey","beta","dividendYield","trailingEps","forwardEps","earningsGrowth","totalCashPerShare","averageVolume","currency","financialCurrency","quoteType","exchange"]},
             "fast":{k:(str(v)) for k,v in dict(fast).items()} if fast else {}}
        try:
            h=tk.history(period="1mo")
            out[t]["hist_1mo"]=h.reset_index().to_dict('records')
        except Exception as e:
            out[t]["hist_err"]=str(e)
    except Exception as e:
        out[t]={"error":str(e)}
print(json.dumps(out,default=str,indent=1))
