import yfinance as yf, pandas as pd
pd.set_option('display.width',250)
t=yf.Ticker("AKAM")
for iv in ["1m","5m"]:
    try:
        h=t.history(period="2d", interval=iv, prepost=False)
        if h.empty: continue
        h=h[h.index.date==pd.Timestamp("2026-09-25").date()]
        print("== interval",iv,"rows",len(h))
        print(h[['Open','High','Low','Close','Volume']].iloc[[0,1,2,3,-4,-3,-2,-1]].to_string())
        print("session high", h['High'].max(), "at", h['High'].idxmax())
        print("session low", h['Low'].min(), "at", h['Low'].idxmin())
        mid=h.index[len(h)//2]
        print("midday row", mid, h.loc[mid,'Close'])
    except Exception as e:
        print("err",iv,e)
