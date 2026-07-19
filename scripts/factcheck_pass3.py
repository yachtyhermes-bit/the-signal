#!/usr/bin/env python3
"""Pass 3: Read articles and verify specific claims against yfinance data."""
import json, glob, os, re
import yfinance as yf
import pandas as pd

os.chdir('/home/chino/thesignal')

files = sorted(glob.glob('articles/posts/*.json'))
arts = [(json.load(open(f)), f) for f in files]
arts.sort(key=lambda x: x[0]['date'], reverse=True)

print("=" * 80)
print("PASS 3: SPECIFIC CLAIM VERIFICATION")
print("=" * 80)

for a, f in arts[:10]:
    slug = a['slug']
    ticker = a['ticker']
    body = a.get('bodyHtml', '')
    body_clean = re.sub(r'<[^>]+>', ' ', body)
    art_price = a.get('price', 0)
    pub_date = a['date'][:10]
    
    print(f"\n{'─'*60}")
    print(f"📄 {ticker}: {slug}")
    
    try:
        t = yf.Ticker(ticker)
        info = t.info
        current_price = info.get('currentPrice') or info.get('previousClose') or info.get('regularMarketPrice', 0)
        
        # Price freshness - detailed check
        hist = t.history(period='1mo')
        pub_dt = pd.Timestamp(pub_date).tz_localize('America/New_York')
        hist_before = hist[hist.index <= pub_dt]
        
        if len(hist_before) > 0:
            last_close = hist_before.iloc[-1]['Close']
            diff = abs(art_price - last_close) / last_close * 100
            print(f"  Price: article=${art_price:.2f}, last hist close=${last_close:.2f} ({diff:.1f}% off)")
            
            # Show last few closes
            print(f"  Last 5 closes:")
            for i in range(min(5, len(hist_before))):
                r = hist_before.iloc[-(i+1)]
                print(f"    {r.name.strftime('%b %d')}: ${r['Close']:.2f}")
        
        # Check RDDT specifically - price of $198 in article
        if ticker == 'RDDT' and art_price > 190:
            print(f"\n  🔍 RDDT DEEP CHECK:")
            # Get wider history
            hist_wider = t.history(period='3mo')
            pub_dt2 = pd.Timestamp('2026-07-16').tz_localize('America/New_York')
            hb = hist_wider[hist_wider.index <= pub_dt2]
            print(f"  All closes before Jul 16:")
            for i in range(min(10, len(hb))):
                r = hb.iloc[-(i+1)]
                print(f"    {r.name.strftime('%b %d')}: O={r['Open']:.2f} H={r['High']:.2f} L={r['Low']:.2f} C={r['Close']:.2f}")
        
        # === CHECK FOR SPECIFIC CLAIMS ===
        
        # 1. Market cap claim
        mc_texts = re.findall(r'(\$[\d,.]+)\s*(trillion|billion|T|B)\s*(market cap|valuation|market value)', body_clean, re.IGNORECASE)
        if mc_texts:
            print(f"\n  📋 Market cap claims found: {mc_texts}")
            mc = info.get('marketCap')
            if mc:
                print(f"  Actual: ${mc/1e9:.1f}B")
        
        # 2. Revenue claims
        rev_texts = re.findall(r'(\$[\d,.]+)\s*(billion|B)\s*(in revenue|revenue|sales)', body_clean, re.IGNORECASE)
        if rev_texts:
            print(f"\n  📋 Revenue claims found: {rev_texts}")
            # Check annual revenue
            inc = t.income_stmt
            if inc is not None and 'Total Revenue' in inc.index:
                for col in inc.columns[:2]:
                    try:
                        yr = col.strftime('%Y') if hasattr(col, 'strftime') else str(col)
                        rev = inc.loc['Total Revenue', col]
                        print(f"  Actual FY{yr}: ${rev/1e9:.1f}B")
                    except:
                        pass
            # TTM
            q_inc = t.quarterly_income_stmt
            if q_inc is not None and 'Total Revenue' in q_inc.index:
                q_revs = q_inc.loc['Total Revenue'].dropna()
                if len(q_revs) >= 4:
                    print(f"  Actual TTM: ${q_revs.head(4).sum()/1e9:.1f}B")
        
        # 3. Growth rate claims
        growth_texts = re.findall(r'(\d+\.?\d*)\s*%\s*(growth|jump|surge|increase|rise)', body_clean, re.IGNORECASE)
        if growth_texts:
            print(f"\n  📋 Growth claims found: {growth_texts}")
            rg = info.get('revenueGrowth')
            if rg:
                print(f"  Actual revenueGrowth: {rg*100:.1f}%")
        
        # 4. FCF claim (PANW specific)
        if '$' in body_clean and 'free cash flow' in body_clean.lower():
            fcf_texts = re.findall(r'(\$[\d,.]+)\s*(billion|B)?\s*(free cash flow|FCF)', body_clean, re.IGNORECASE)
            if fcf_texts:
                print(f"\n  📋 FCF claims found: {fcf_texts}")
                fcf = info.get('freeCashflow')
                if fcf:
                    print(f"  Actual FCF: ${fcf/1e9:.2f}B")
        
        # 5. PE claim
        pe_texts = re.findall(r'(\d+\.?\d*)\s*x\s*(P/E|price.to.earnings|trailing PE)', body_clean, re.IGNORECASE)
        if pe_texts:
            print(f"\n  📋 P/E claims found: {pe_texts}")
            tpe = info.get('trailingPE')
            if tpe:
                print(f"  Actual trailing P/E: {tpe:.1f}x")
        
        # 6. "Down from high" claims
        down_texts = re.findall(r'(down|below|off)\s*(\d+\.?\d*)\s*%\s*(from|below|off)\s*(its|their|all.time|52.week|record|high)', body_clean, re.IGNORECASE)
        if down_texts:
            print(f"\n  📋 'Down from high' claims found: {down_texts}")
            high52 = info.get('fiftyTwoWeekHigh')
            if high52:
                actual_drop = (high52 - current_price) / high52 * 100
                print(f"  Actual: 52W high=${high52:.2f}, current=${current_price:.2f}, drop={actual_drop:.1f}%")
        
        # 7. Margin claims
        margin_texts = re.findall(r'(\d+\.?\d*)\s*%\s*(gross|operating|profit|net)\s*(margin|margins)', body_clean, re.IGNORECASE)
        if margin_texts:
            print(f"\n  📋 Margin claims found: {margin_texts}")
            for m in margin_texts:
                margin_type = m[1].lower()
                margin_pct = float(m[0])
                actual = None
                if 'gross' in margin_type:
                    actual = info.get('grossMargins')
                elif 'operating' in margin_type:
                    actual = info.get('operatingMargins')
                elif 'profit' in margin_type or 'net' in margin_type:
                    actual = info.get('profitMargins')
                if actual:
                    actual_pct = actual * 100
                    diff_m = abs(margin_pct - actual_pct)
                    if diff_m > 3:
                        print(f"  ⚠️  {margin_type.title()} margin: article={margin_pct}%, actual={actual_pct:.1f}% (diff={diff_m:.1f}pp)")
                    else:
                        print(f"  ✅ {margin_type.title()} margin: article={margin_pct}%, actual={actual_pct:.1f}%")
        
        # 8. Backlog / RPO (ORCL specific)
        if ticker == 'ORCL':
            backlog_texts = re.findall(r'\$[\d,.]+\s*(billion|B)?\s*(backlog|RPO|remaining performance obligation)', body_clean, re.IGNORECASE)
            if backlog_texts:
                print(f"\n  📋 Backlog claims: {backlog_texts}")
                print(f"  ⚠️  Backlog/RPO data not available via yfinance — press release verification recommended")
        
        # 9. Debt claims
        debt_texts = re.findall(r'(\$[\d,.]+)\s*(billion|B)\s*(in debt|debt|borrowing)', body_clean, re.IGNORECASE)
        if debt_texts:
            print(f"\n  📋 Debt claims: {debt_texts}")
            debt = info.get('totalDebt')
            if debt:
                print(f"  Actual totalDebt: ${debt/1e9:.2f}B")
                bs = t.quarterly_balance_sheet
                if bs is not None:
                    lt_debt = bs.loc['Long Term Debt'].iloc[0] if 'Long Term Debt' in bs.index else 0
                    curr_debt = bs.loc['Current Debt'].iloc[0] if 'Current Debt' in bs.index else 0
                    if lt_debt or curr_debt:
                        print(f"  Balance sheet: LT Debt=${lt_debt/1e9:.2f}B, Current Debt=${curr_debt/1e9:.2f}B")
        
    except Exception as e:
        print(f"  ⚠️  Error: {e}")

print(f"\n{'═'*80}")
print("DONE - Pass 3 complete")
