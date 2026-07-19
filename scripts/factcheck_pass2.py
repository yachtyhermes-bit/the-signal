#!/usr/bin/env python3
"""Pass 2: yfinance fact-checking for the 10 most recent articles."""
import json, glob, os
import yfinance as yf
import pandas as pd

os.chdir('/home/chino/thesignal')

files = sorted(glob.glob('articles/posts/*.json'))
arts = [(json.load(open(f)), f) for f in files]
arts.sort(key=lambda x: x[0]['date'], reverse=True)

print("=" * 80)
print("PASS 2: yfinance FINANCIAL VERIFICATION")
print("=" * 80)

for a, f in arts[:10]:
    slug = a['slug']
    ticker = a['ticker']
    art_price = a.get('price', 0)
    pub_date = a['date'][:10]  # "2026-07-18"
    
    print(f"\n{'─'*60}")
    print(f"📄 {ticker:6s} | {slug}")
    print(f"{'─'*60}")
    
    try:
        t = yf.Ticker(ticker)
        info = t.info
        current_price = info.get('currentPrice') or info.get('previousClose') or info.get('regularMarketPrice', 0)
        
        print(f"  📊 Current price: ${current_price:.2f}")
        
        # Price freshness check
        hist = t.history(period='1mo')
        pub_dt = pd.Timestamp(pub_date).tz_localize('America/New_York')
        hist_before = hist[hist.index <= pub_dt]
        
        if len(hist_before) > 0:
            last_close = hist_before.iloc[-1]['Close']
            diff = abs(art_price - last_close) / last_close * 100
            if diff > 5:
                print(f"  ❌ PRICE MISMATCH: article=${art_price:.2f}, hist close=${last_close:.2f} ({diff:.1f}% off)")
            else:
                print(f"  ✅ Price: article=${art_price:.2f}, hist close=${last_close:.2f} ({diff:.1f}% off)")
        else:
            print(f"  ⚠️  No historical data for {pub_date}")
        
        # Market cap
        mc = info.get('marketCap')
        if mc:
            mc_b = mc / 1e9
            print(f"  💰 Market Cap: ${mc_b:.2f}B")
        
        # Revenue info
        inc = t.income_stmt
        if inc is not None and 'Total Revenue' in inc.index:
            for col in inc.columns[:2]:
                try:
                    yr = col.strftime('%Y') if hasattr(col, 'strftime') else str(col)
                    rev = inc.loc['Total Revenue', col]
                    print(f"  📈 FY{yr} Revenue: ${rev/1e9:.2f}B")
                except:
                    pass
        
        # TTM revenue
        q_inc = t.quarterly_income_stmt
        ttm_rev = None
        if q_inc is not None and 'Total Revenue' in q_inc.index:
            q_revs = q_inc.loc['Total Revenue'].dropna()
            if len(q_revs) >= 4:
                ttm_rev = q_revs.head(4).sum()
                print(f"  📈 TTM Revenue: ${ttm_rev/1e9:.2f}B")
        
        # Margins
        gm = info.get('grossMargins')
        om = info.get('operatingMargins')
        pm = info.get('profitMargins')
        if gm: print(f"  📊 Gross Margin: {gm*100:.1f}%")
        if om: print(f"  📊 Operating Margin: {om*100:.1f}%")
        if pm: print(f"  📊 Profit Margin: {pm*100:.1f}%")
        
        # PE
        tpe = info.get('trailingPE')
        fpe = info.get('forwardPE')
        if tpe: print(f"  📊 Trailing P/E: {tpe:.1f}x")
        if fpe: print(f"  📊 Forward P/E: {fpe:.1f}x")
        
        # Revenue growth
        rg = info.get('revenueGrowth')
        if rg: print(f"  📊 Revenue Growth: {rg*100:.1f}%")
        
        # 52-week high
        high52 = info.get('fiftyTwoWeekHigh')
        if high52:
            drop_pct = (high52 - current_price) / high52 * 100
            print(f"  📊 52W High: ${high52:.2f} (down {drop_pct:.1f}%)")
        
        # Cash and debt
        cash = info.get('totalCash')
        debt = info.get('totalDebt')
        if cash: print(f"  💵 Cash: ${cash/1e9:.2f}B")
        if debt: print(f"  🏦 Total Debt: ${debt/1e9:.2f}B")
        
        # FCF
        fcf = info.get('freeCashflow')
        if fcf: print(f"  💵 FCF: ${fcf/1e9:.2f}B")
        
        # EBITDA
        ebitda = info.get('ebitda')
        if ebitda: print(f"  📊 EBITDA: ${ebitda/1e9:.2f}B")
        
        print(f"  ✅ yfinance data loaded for {ticker}")
        
    except Exception as e:
        print(f"  ⚠️  yfinance error for {ticker}: {e}")

# Now let me read each article and compare key claims
print(f"\n{'═'*80}")
print("ARTICLE CLAIM EXTRACTION")
print(f"{'═'*80}")

for a, f in arts[:10]:
    slug = a['slug']
    ticker = a['ticker']
    body = a.get('bodyHtml', '')
    
    # Extract key phrases that might contain numbers
    lines = body.split('\n')
    claims = []
    for line in lines:
        line = line.strip()
        if any(x in line for x in ['$', 'billion', 'million', '%', 'x P/E', 'EPS', 'margin']):
            # Strip HTML tags for readability
            import re
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean:
                claims.append(clean)
    
    if claims:
        print(f"\n📄 {ticker}: {slug[:50]}")
        for c in claims[:5]:
            print(f"   {c[:120]}")

print(f"\n{'═'*80}")
print("DONE — Now checking links")
