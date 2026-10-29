import yfinance as yf, pandas as pd
pd.set_option('display.width',250)
t=yf.Ticker("AKAM")
h=t.history(period="5d", interval="5m", prepost=True)
d=h[(h.index>=pd.Timestamp("2026-09-24 15:55", tz="America/New_York"))&(h.index<=pd.Timestamp("2026-09-24 20:00", tz="America/New_York"))]
print("Sept24 15:55 -> 20:00 ET")
print(d[['Open','High','Low','Close','Volume']].to_string())
if not d.empty:
    print("max after-hours high:", d['High'].max(), d['High'].idxmax())
    print("last after-hours close:", d['Close'].iloc[-1])
