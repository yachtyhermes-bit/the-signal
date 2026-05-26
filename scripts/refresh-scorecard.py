#!/usr/bin/env python3
"""Pull real yfinance metrics for all 6 scorecard stocks, calculate signals, write data/scorecard.json."""
import json, os, sys

try:
    import yfinance as yf
except ImportError:
    os.system(f"{sys.executable} -m pip install yfinance -q --break-system-packages")
    import yfinance as yf

TICKERS = ['AXON', 'META', 'PLTR', 'RTX', 'NFLX', 'RBRK']
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Company metadata
COMPANIES = {
    'AXON': {'name': 'Axon Enterprise', 'sector': 'Defense Tech', 'logo': 'https://logo.clearbit.com/axon.com'},
    'META': {'name': 'Meta Platforms', 'sector': 'Social Media', 'logo': 'https://logo.clearbit.com/meta.com'},
    'PLTR': {'name': 'Palantir Technologies', 'sector': 'AI Software', 'logo': 'https://logo.clearbit.com/palantir.com'},
    'RTX': {'name': 'RTX Corporation', 'sector': 'Defense', 'logo': 'https://logo.clearbit.com/rtx.com'},
    'NFLX': {'name': 'Netflix Inc.', 'sector': 'Entertainment', 'logo': 'https://logo.clearbit.com/netflix.com'},
    'RBRK': {'name': 'Rubrik Inc.', 'sector': 'Cybersecurity', 'logo': 'https://logo.clearbit.com/rubrik.com'},
}

def fmt_billions(v):
    """Format a value in billions with $ sign."""
    if v is None: return 'N/A'
    v = float(v)
    if abs(v) >= 1e12: return f'${v/1e12:.2f}T'
    if abs(v) >= 1e9: return f'${v/1e9:.2f}B'
    if abs(v) >= 1e6: return f'${v/1e6:.2f}M'
    return f'${v:.2f}'

def fmt_pct(v):
    if v is None: return 'N/A'
    v = float(v)
    sign = '+' if v > 0 else ''
    return f'{sign}{v:.1f}%'

def calc_signal(rev_growth, pe, upside, net_income, is_profitable):
    """Calculate signal type and score based on real metrics."""
    score = 50  # start neutral
    
    # Revenue growth contribution (0-25 points)
    if rev_growth and rev_growth > 0:
        score += min(rev_growth * 0.4, 25)
    elif rev_growth and rev_growth < 0:
        score -= min(abs(rev_growth) * 0.3, 20)
    
    # Profitability contribution (-15 to 10 points)
    if is_profitable and net_income and net_income > 0:
        score += 10
    else:
        score -= 15
    
    # PE sanity (-10 to 10 points)
    if pe and pe > 0:
        if pe < 25: score += 10
        elif pe < 40: score += 5
        elif pe < 80: score += 0
        else: score -= 5
    elif pe is None:  # N/A (unprofitable)
        score -= 5
    
    # Upside contribution (0-10 points)
    if upside and upside > 0:
        score += min(upside * 0.1, 10)
    elif upside and upside < 0:
        score -= min(abs(upside) * 0.1, 10)
    
    # Clamp
    score = max(10, min(98, score))
    
    if score >= 78:
        return 'Strong Bullish', round(score), '#10b981'
    elif score >= 60:
        return 'Bullish', round(score), '#84cc16'
    elif score >= 40:
        return 'Neutral', round(score), '#64748b'
    else:
        return 'Bearish', round(score), '#ef4444'

def build_scorecard():
    results = []
    
    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            annual = t.financials
            
            # Revenue TTM
            revenue = info.get('totalRevenue')
            
            # Rev Growth YoY
            rev_growth_yoy = None
            if annual is not None and not annual.empty:
                if 'Total Revenue' in annual.index:
                    rev_vals = annual.loc['Total Revenue'].dropna()
                    if len(rev_vals) >= 2:
                        rev_growth_yoy = ((float(rev_vals.iloc[0]) - float(rev_vals.iloc[1])) / float(rev_vals.iloc[1])) * 100
            if rev_growth_yoy is None:
                rg = info.get('revenueGrowth')
                if rg is not None: rev_growth_yoy = rg * 100
            
            # Net Income
            net_income = info.get('netIncomeToCommon')
            
            # P/E
            pe = info.get('trailingPE')
            
            # Price/Sales
            ps = info.get('priceToSalesTrailing12Months')
            
            # Target price
            target_median = info.get('targetMedianPrice')
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            upside = None
            if target_median and current_price:
                upside = ((target_median / current_price) - 1) * 100
            
            is_profitable = bool(net_income and net_income > 0)
            
            # Build drivers
            drivers = []
            if rev_growth_yoy and rev_growth_yoy > 15:
                drivers.append(f'Revenue up {fmt_pct(rev_growth_yoy)} YoY to {fmt_billions(revenue)}')
            elif rev_growth_yoy:
                drivers.append(f'Revenue up {fmt_pct(rev_growth_yoy)} YoY to {fmt_billions(revenue)}')
            
            if is_profitable and pe and pe < 30:
                drivers.append(f'P/E at {pe:.1f}x — attractively valued')
            elif pe and pe > 80:
                drivers.append(f'Premium valuation at {pe:.0f}x P/E')
            elif not is_profitable:
                drivers.append(f'Still operating at net loss {fmt_billions(net_income)}')
            
            if upside and upside > 20:
                drivers.append(f'Target upside {fmt_pct(upside)}')
            elif upside and upside > 10:
                drivers.append(f'Moderate upside {fmt_pct(upside)}')
            
            # Ensure 3 drivers
            while len(drivers) < 3:
                if is_profitable and len(drivers) < 3:
                    drivers.append(f'Net income {fmt_billions(net_income)}')
                elif ps and len(drivers) < 3:
                    drivers.append(f'P/S multiple at {ps:.1f}x')
                else:
                    drivers.append(f'Market cap {fmt_billions(info.get("marketCap"))}')
            
            drivers = drivers[:3]
            
            # Calculate signal
            signal, score, color = calc_signal(rev_growth_yoy, pe, upside, net_income, is_profitable)
            
            entry = {
                'ticker': ticker,
                'name': COMPANIES[ticker]['name'],
                'sector': COMPANIES[ticker]['sector'],
                'signal': signal,
                'score': score,
                'color': color,
                'drivers': drivers,
                'upside': fmt_pct(upside),
                'logo': COMPANIES[ticker]['logo'],
                'metrics': {
                    'revenue': fmt_billions(revenue),
                    'growth': fmt_pct(rev_growth_yoy),
                    'netIncome': fmt_billions(net_income) if net_income else 'N/A',
                    'pe': f'{pe:.1f}x' if pe else 'N/A',
                    'ps': f'{ps:.1f}x' if ps else 'N/A',
                }
            }
            
            results.append(entry)
            
        except Exception as e:
            print(f'  ⚠️  Failed to fetch {ticker}: {e}', file=sys.stderr)
            # Use last known values as fallback
            results.append(None)
    
    return results

if __name__ == '__main__':
    print('📊 Refreshing scorecard data from yfinance...')
    scorecard = build_scorecard()
    
    outpath = os.path.join(DATA_DIR, 'scorecard.json')
    with open(outpath, 'w') as f:
        json.dump(scorecard, f, indent=2)
    
    count_ok = sum(1 for r in scorecard if r is not None)
    print(f'  ✅ {count_ok}/{len(TICKERS)} stocks refreshed')
    print(f'  📁 Written to {outpath}')
    
    # Print summary
    for entry in scorecard:
        if entry:
            print(f'  {entry["ticker"]}: {entry["signal"]} ({entry["score"]}) — Rev {entry["metrics"]["growth"]}, Upside {entry["upside"]}')
