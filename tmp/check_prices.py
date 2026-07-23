import json, subprocess, sys

# Check each ticker's actual price via yfinance
tickers = {
    'snow-ai-data-cloud-consumption-2026': 'SNOW',
    'amat-picks-shovels-ai-supercycle-2026': 'AMAT',
    'crm-agentforce-doubt-discount-2026': 'CRM',
    'rbrk-cyber-resilience-secular-growth-2026': 'RBRK',
    'avav-counterdrone-switchblade-contracts-2026': 'AVAV',
}

for slug, ticker in tickers.items():
    print(f"\n=== {slug} ({ticker}) ===")
    
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    
    article_price = a.get('price')
    print(f"Article price: ${article_price}")
    
    # yfinance
    try:
        script = f"""
import yfinance as yf
t = yf.Ticker('{ticker}')
h = t.history(period='1d')
if not h.empty:
    print(f"Close: {{h['Close'].iloc[-1]:.2f}}")
    print(f"Open: {{h['Open'].iloc[-1]:.2f}}")
    print(f"High: {{h['High'].iloc[-1]:.2f}}")
    print(f"Low: {{h['Low'].iloc[-1]:.2f}}")
    print(f"Volume: {{h['Volume'].iloc[-1]:.0f}}")
else:
    print("NO_DATA - could be after hours/weekend")
    # Try 5d
    h5 = t.history(period='5d')
    if not h5.empty:
        print(f"Last 5d close: {{h5['Close'].iloc[-1]:.2f}}")
    else:
        print("NO 5D DATA EITHER")
"""
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True, text=True, timeout=30
        )
        print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr[:200]}")
    except Exception as e:
        print(f"yfinance error: {e}")

print("\n=== DONE ===")
