import yfinance as yf

# Check closes on specific dates for each article
checks = {
    'AMAT': {'article_price': 560.08, 'article_date': '2026-07-22'},
    'CRM': {'article_price': 167.00, 'article_date': '2026-07-22'},
    'RBRK': {'article_price': 75.80, 'article_date': '2026-07-22'},
    'AVAV': {'article_price': 145.40, 'article_date': '2026-07-21'},
    'SNOW': {'article_price': 267.80, 'article_date': '2026-07-23'},
}

print("Checking historical closes vs article prices...")
print(f"{'Ticker':<8} {'Date':<12} {'Article':<12} {'Close That Day':<16} {'Match':<10}")
print("-"*58)

for ticker, info in checks.items():
    t = yf.Ticker(ticker)
    h = t.history(start=info['article_date'], end='2026-07-24')
    close_that_day = h['Close'].iloc[0] if not h.empty else None
    
    if close_that_day:
        match = "✅" if abs(close_that_day - info['article_price']) < 0.05 else "❌"
        print(f"{ticker:<8} {info['article_date']:<12} ${info['article_price']:<8.2f} ${close_that_day:<12.2f} {match:<10}")
        if abs(close_that_day - info['article_price']) >= 0.05:
            diff = close_that_day - info['article_price']
            print(f"  Difference: ${diff:+.2f}")
    else:
        print(f"{ticker:<8} {info['article_date']:<12} ${info['article_price']:<8.2f} {'NO DATA':<16}")

# Also check previous day for July 22 tickers in case they used prev close
print("\n\nChecking previous day close (July 21) for July 22 articles...")
for ticker in ['AMAT', 'CRM', 'RBRK']:
    t = yf.Ticker(ticker)
    h = t.history(start='2026-07-21', end='2026-07-22')
    close = h['Close'].iloc[0] if not h.empty else None
    article_price = checks[ticker]['article_price']
    if close:
        match = "✅" if abs(close - article_price) < 0.05 else "❌"
        print(f"{ticker:<8} July 21 close: ${close:<8.2f} vs article: ${article_price:<8.2f} {match}")
