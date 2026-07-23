import yfinance as yf

# Check wider range for AMAT, CRM, AVAV
for ticker in ['AMAT', 'CRM', 'AVAV']:
    t = yf.Ticker(ticker)
    h = t.history(start='2026-07-17', end='2026-07-24')
    if not h.empty:
        print(f"\n=== {ticker} ===")
        for date, row in h.iterrows():
            print(f"  {date.strftime('%Y-%m-%d')}: Close ${row['Close']:.2f}")

# For SNOW, try 5d
print("\n=== SNOW (5d) ===")
t = yf.Ticker('SNOW')
h = t.history(period='5d')
if not h.empty:
    for date, row in h.iterrows():
        print(f"  {date.strftime('%Y-%m-%d')}: Close ${row['Close']:.2f}")
