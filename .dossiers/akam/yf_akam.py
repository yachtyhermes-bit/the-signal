import yfinance as yf, pandas as pd, json
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
t=yf.Ticker("AKAM")
h=t.history(start="2026-09-15", end="2026-09-26", auto_adjust=False)
print("=== DAILY OHLCV ===")
print(h[['Open','High','Low','Close','Volume']].to_string())
print()
i=t.info
for k in ['shortName','currentPrice','previousClose','regularMarketPreviousClose','marketCap','sharesOutstanding','fiftyTwoWeekHigh','fiftyTwoWeekLow','longName','sector','industry','fullTimeEmployees']:
    print(k,":",i.get(k))
