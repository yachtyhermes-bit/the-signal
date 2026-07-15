import json, glob, datetime
now = datetime.date.today()
articles = sorted(
    [json.load(open(f)) for f in glob.glob('articles/posts/*.json')],
    key=lambda a: a['date'][:10], reverse=True
)
recent = []
for a in articles:
    if 'ticker' not in a:
        continue
    try:
        d = datetime.date.fromisoformat(a['date'][:10])
        if (now - d).days < 7:
            recent.append(a)
    except:
        pass

from collections import Counter
ticker_counts = Counter(a['ticker'] for a in recent)
print('=== TICKERS IN LAST 7 DAYS ===')
for ticker, count in ticker_counts.most_common():
    entries = [(a['date'][:10], a['title'][:80]) for a in recent if a['ticker'] == ticker]
    print(f'  {ticker} ({count}x):')
    for d, t in entries:
        print(f'    {d}: {t}')
print(f'Total articles last 7 days: {len(recent)}')

# Last 30 days
all_30 = []
for a in articles:
    if 'ticker' not in a:
        continue
    try:
        d = datetime.date.fromisoformat(a['date'][:10])
        if (now - d).days < 30:
            all_30.append(a)
    except:
        pass
ticker_30 = Counter(a['ticker'] for a in all_30)
print()
print('=== TICKER COUNTS LAST 30 DAYS ===')
for ticker, count in ticker_30.most_common():
    flag = ''
    if count >= 7:
        flag = ' -- AVOID (7+)'
    elif ticker in ticker_counts:
        flag = ' -- AVOID (covered last 7d)'
    print(f'  {ticker}: {count}x{flag}')
