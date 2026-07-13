import json, glob, datetime, collections

def parse_date(d):
    if isinstance(d, str):
        d_clean = d.replace('Z','').replace('T',' ')
        return datetime.date.fromisoformat(d_clean[:10])
    return datetime.date.fromisoformat(d)

now = datetime.date.today()
articles = sorted([json.load(open(f)) for f in glob.glob('articles/posts/*.json')], key=lambda a: parse_date(a['date']), reverse=True)
recent = [a for a in articles if (now - parse_date(a['date'])).days < 7]
ticker_counts = collections.Counter(a['ticker'] for a in recent if 'ticker' in a)
print('RECENT TICKERS (last 7 days):')
for t, c in ticker_counts.most_common():
    print(f'  {t}: {c}x')
print(f'Total articles in last 7 days: {len(recent)}')

all_recent_30 = [a for a in articles if (now - parse_date(a['date'])).days < 30]
ticker_counts_30 = collections.Counter(a['ticker'] for a in all_recent_30 if 'ticker' in a)
print()
print('TICKERS WITH 4+ in last 30 days (avoid):')
for t, c in ticker_counts_30.most_common():
    if c >= 4:
        print(f'  {t}: {c}x')

fin = json.load(open('data/financials.json'))
fin_tickers = set(k for k in fin.keys() if len(k) <= 5 and k == k.upper() and not any(ch.isdigit() for ch in k))
candidates = fin_tickers - set(ticker_counts.keys())
print(f'\nUNCOVERED IN LAST 7 DAYS ({len(candidates)}):')
for t in sorted(candidates):
    count_30 = ticker_counts_30.get(t, 0)
    if count_30 <= 3:
        print(f'  {t} (30d: {count_30}x)')
