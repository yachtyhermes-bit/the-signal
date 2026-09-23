import yfinance as yf, json
for t in ["AVGO","CEG","SOFI","RTX","AMZN","NFLX"]:
    tk = yf.Ticker(t)
    try:
        cal = tk.calendar
    except Exception as e:
        cal = f"ERR {e}"
    print("="*60)
    print(t, "CALENDAR:", cal)
    try:
        ed = tk.get_earnings_dates(limit=8)
        print("EARNINGS DATES:\n", ed)
    except Exception as e:
        print("ed err", e)
    try:
        print("EARNINGS EST:", tk.get_earnings_estimate())
    except Exception as e:
        print("est err", e)
