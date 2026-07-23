import yfinance as yf
import json
from datetime import datetime

articles = {
    'SNOW': 'snow-ai-data-cloud-consumption-2026',
    'AMAT': 'amat-picks-shovels-ai-supercycle-2026',
    'CRM': 'crm-agentforce-doubt-discount-2026',
    'RBRK': 'rbrk-cyber-resilience-secular-growth-2026',
    'AVAV': 'avav-counterdrone-switchblade-contracts-2026',
}

for ticker, slug in articles.items():
    print(f"\n{'='*60}")
    print(f"  {ticker} ({slug})")
    print('='*60)
    
    t = yf.Ticker(ticker)
    
    # Get the article text
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    
    body = a.get('bodyHtml', '')
    
    # Info
    info = t.info or {}
    
    # Quarterly income statement
    qi = t.quarterly_income_stmt
    qb = t.quarterly_balance_sheet
    qc = t.quarterly_cashflow
    
    if qi is not None and not qi.empty:
        print(f"\n  Latest quarterly revenue:")
        for col in qi.columns[:4]:
            try:
                rev = qi.loc['Total Revenue', col] if 'Total Revenue' in qi.index else None
                if rev:
                    print(f"    {col.strftime('%Y-%m-%d')}: ${rev/1e9:.2f}B")
            except:
                pass
    
    # Annual income statement
    inc = t.income_stmt
    if inc is not None and not inc.empty:
        print(f"\n  Key annual metrics:")
        for metric in ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']:
            if metric in inc.index:
                vals = inc.loc[metric]
                for col in vals.index[:3]:
                    try:
                        v = vals[col]
                        label = f"${v/1e9:.2f}B" if abs(v) >= 1e9 else f"${v/1e6:.2f}M" if abs(v) >= 1e6 else f"${v:,.0f}"
                        print(f"    {metric} ({col.strftime('%Y-%m-%d')}): {label}")
                    except:
                        pass
    
    # Key stats from info
    market_cap = info.get('marketCap')
    enterprise_value = info.get('enterpriseValue')
    pe_ratio = info.get('trailingPE')
    forward_pe = info.get('forwardPE')
    revenue_growth = info.get('revenueGrowth')
    
    print(f"\n  Key stats from info:")
    if market_cap: print(f"    Market Cap: ${market_cap/1e9:.2f}B")
    if enterprise_value: print(f"    Enterprise Value: ${enterprise_value/1e9:.2f}B")
    if pe_ratio: print(f"    Trailing P/E: {pe_ratio:.2f}")
    if forward_pe: print(f"    Forward P/E: {forward_pe:.2f}")
    if revenue_growth: print(f"    Revenue Growth (YoY): {revenue_growth*100:.1f}%")
    
    # Free cash flow
    cf = t.cashflow
    if cf is not None and 'Free Cash Flow' in cf.index:
        fcf = cf.loc['Free Cash Flow']
        print(f"\n  Free Cash Flow (annual):")
        for col in fcf.index[:3]:
            try:
                v = fcf[col]
                print(f"    {col.strftime('%Y-%m-%d')}: ${v/1e9:.2f}B" if abs(v) >= 1e9 else f"    {col.strftime('%Y-%m-%d')}: ${v/1e6:.2f}M")
            except:
                pass
    
    print()

print("=== VERIFICATION COMPLETE ===")
