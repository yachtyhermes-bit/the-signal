import yfinance as yf

# ANET - get more quarterly data to verify 35% growth claim
print("===== ANET Detailed Revenue Growth =====")
tk = yf.Ticker("ANET")
try:
    q = tk.quarterly_financials
    if q is not None and 'Total Revenue' in q.index:
        revs = q.loc['Total Revenue']
        print(f"All available quarters ({len(revs)} total):")
        for i, (idx, val) in enumerate(revs.items()):
            print(f"  {i}: {idx.strftime('%Y-%m-%d')} - ${val/1e9:.2f}B")
        
        if len(revs) >= 8:
            current_ttm = revs.iloc[0:4].sum()
            prior_ttm = revs.iloc[4:8].sum()
            print(f"\nCurrent TTM (4 most recent): {current_ttm/1e9:.2f}B")
            print(f"Prior TTM (prev 4): {prior_ttm/1e9:.2f}B")
            print(f"TTM Growth: {(current_ttm-prior_ttm)/prior_ttm*100:.1f}%")
        
        # Check YoY growth for latest quarter
        if len(revs) >= 5:
            latest_q = revs.iloc[0]
            same_q_ly = revs.iloc[4]
            print(f"\nLatest Quarter: ${latest_q/1e9:.2f}B")
            print(f"Same Q Last Year: ${same_q_ly/1e9:.2f}B")
            print(f"YoY Q Growth: {(latest_q-same_q_ly)/same_q_ly*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")

# MRVL - check YoY growth
print("\n===== MRVL Detailed Revenue Growth =====")
tk = yf.Ticker("MRVL")
try:
    q = tk.quarterly_financials
    if q is not None and 'Total Revenue' in q.index:
        revs = q.loc['Total Revenue']
        print(f"All available quarters ({len(revs)} total):")
        for i, (idx, val) in enumerate(revs.items()):
            print(f"  {i}: {idx.strftime('%Y-%m-%d')} - ${val/1e9:.2f}B")
        
        if len(revs) >= 8:
            current_ttm = revs.iloc[0:4].sum()
            prior_ttm = revs.iloc[4:8].sum()
            print(f"\nCurrent TTM: {current_ttm/1e9:.2f}B")
            print(f"Prior TTM: {prior_ttm/1e9:.2f}B")
            print(f"TTM Growth: {(current_ttm-prior_ttm)/prior_ttm*100:.1f}%")
        
        if len(revs) >= 5:
            latest_q = revs.iloc[0]
            same_q_ly = revs.iloc[4]
            print(f"\nLatest Quarter: ${latest_q/1e9:.2f}B")
            print(f"Same Q Last Year: ${same_q_ly/1e9:.2f}B")
            print(f"YoY Q Growth: {(latest_q-same_q_ly)/same_q_ly*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")
