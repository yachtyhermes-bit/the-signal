import yfinance as yf, pandas as pd
pd.set_option('display.width',250)
t=yf.Ticker("AKAM")
h=t.history(period="5d", interval="5m", prepost=True)
print("rows",len(h))
print(h[['Open','High','Low','Close','Volume']].tail(30).to_string())
