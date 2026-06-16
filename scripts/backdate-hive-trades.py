#!/usr/bin/env python3
"""
Backdate Hive Game Trades — v3
- Evenly distributed trades across Nov 2025 - Jun 2026
- Proper portfolio state simulation accounting for existing trades
- Realistic personas with varied returns
"""

import json
import random
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter

DATA_FILE = '/home/chino/thesignal/data/hive-data.json'
INITIAL_CASH = 100000
EXISTING_CUTOFF = datetime(2025, 10, 31)
BACKDATE_END = datetime(2026, 6, 14)

TICKERS = {
    'AI_CORE':     ['NVDA', 'AMD', 'AVGO', 'MRVL'],
    'AI_INFRA':    ['CRWV', 'CBRS', 'IREN', 'INTC'],
    'CYBER':       ['CRWD', 'PANW', 'FTNT', 'ZS', 'CHKP', 'TENB', 'RBRK', 'S'],
    'DEFENSE':     ['LMT', 'RTX', 'NOC', 'GD', 'LHX', 'KTOS', 'AVAV', 'PL', 'AXON', 'GE', 'PLTR'],
    'SPACE':       ['RKLB', 'RDW', 'LUNR', 'ASTS'],
    'MEGA':        ['MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX'],
    'QUANTUM':     ['IONQ', 'QBTS', 'QUBT'],
    'FINTECH':     ['SOFI', 'HOOD'],
}
ALL_TICKERS = sorted(set(t for group in TICKERS.values() for t in group))

# Personas: (strategy, focus_tickers, trades_per_month_range, buy_ratio, sell_aggressiveness)
# sell_aggressiveness 0-1: how much of holdings to sell when selling
PERSONAS = {
    # Top 5 — hyperactive and profitable
    'usr_ee2913dcbfd9625a': ('swing_trader',    ['NVDA','CRWV','KTOS','PLTR','AXON','AVGO','RTX','TSLA','RKLB'], (5,8), 0.42, 0.55),
    'usr_cf8b38bc10316048': ('crypto_ai_bull',  ['IONQ','IREN','NVDA','QBTS','CRWV','PLTR'], (4,7), 0.38, 0.50),
    'usr_85b318fa7f5386be': ('defense_heavy',   ['PLTR','KTOS','AXON','RTX','LMT','NOC','LHX','AVAV'], (4,6), 0.45, 0.40),
    'usr_2403c9113f45afe1': ('mega_diversified',['MSFT','AMZN','GOOGL','META','TSLA','NVDA','AVGO'], (3,6), 0.48, 0.35),
    'usr_94badc24a68a4ca1': ('ai_maximalist',   ['NVDA','AVGO','CRWV','AMD','MRVL','CBRS','TSLA'], (5,7), 0.35, 0.50),

    # Mid-tier — solid, some swings
    'usr_63a5f948290cbc43': ('cyber_fortress',  ['CRWD','PANW','FTNT','ZS','CHKP','TENB','RBRK'], (3,5), 0.50, 0.35),
    'usr_d9a4e248bb9cdc0e': ('space_cowboy',    ['RKLB','ASTS','LUNR','RDW','PL'], (3,5), 0.40, 0.45),
    'usr_bb3634a037315b83': ('quantum_gambler', ['IONQ','QBTS','QUBT','NVDA'], (3,5), 0.35, 0.55),
    'usr_a9a2eebf1bb5c32e': ('defense_value',   ['LMT','RTX','NOC','GD','GE','LHX'], (2,4), 0.55, 0.25),
    'usr_f5c5d8724fe99417': ('industrial_mix',  ['GE','RTX','LHX','TSLA'], (2,4), 0.55, 0.30),
    'usr_a1dea1d07736d875': ('quantum_space',   ['QUBT','LUNR','IONQ','RKLB','QBTS'], (3,4), 0.45, 0.40),
    'usr_58de6363e9419f04': ('tech_generalist', ['PLTR','META','CHKP','NVDA','MSFT'], (3,4), 0.55, 0.30),
    'usr_31dbadba8ecb839e': ('cloud_believer',  ['DDOG','CRWV','AMZN','MSFT','ZS'], (2,4), 0.55, 0.25),
    'usr_779ec87afc2e8d0b': ('defense_tech',    ['AVAV','CHKP','KTOS','AXON','PLTR'], (2,4), 0.50, 0.35),
    'usr_a9ee61dbe78c6e74': ('cyber_ai_hybrid', ['CRWD','IONQ','PL','ZS','PANW','FTNT'], (2,4), 0.55, 0.30),
    'usr_bb93e637234053b7': ('value_hunter',    ['VRT','ANET','GE','TENB','CHKP'], (2,3), 0.60, 0.25),
    'usr_13bd8462edda2b24': ('defense_patriot', ['LHX','KTOS','NOC','LMT','RTX'], (2,3), 0.60, 0.25),
    'usr_b4ab31f3882d061d': ('crypto_defense',  ['COIN','LHX','GD','KTOS'], (2,3), 0.55, 0.35),
    'usr_9edfb43eca35a4a2': ('quiet_accum',     ['TENB','NOC','SOFI','GE','CHKP'], (2,3), 0.65, 0.20),
    'usr_ca82227c1e8f96c6': ('streaming_bull',  ['NFLX','MRVL','AMZN','META'], (2,3), 0.60, 0.25),
    'usr_f478bee0ab61c9b2': ('ride_share_bull', ['TSLA','AMZN'], (2,3), 0.65, 0.20),
    'usr_46dc83645688750b': ('fintech_cyber',   ['SOFI','CRWD','KTOS','HOOD'], (2,3), 0.55, 0.30),

    # Nov 2025 joiners
    'usr_353412010c5a7312': ('quant_ai',        ['NVDA','AVGO','IONQ','CRWV'], (3,5), 0.45, 0.40),
    'usr_bd7e95db529f90ac': ('space_defense',   ['RKLB','KTOS','AXON','RDW'], (3,4), 0.45, 0.40),
    'usr_07ed77036457c48f': ('cyber_guardian',  ['CRWD','ZS','PANW','FTNT'], (3,4), 0.50, 0.35),
    'usr_a5c30f0cf35d04c8': ('mega_momentum',   ['TSLA','NVDA','META','AMZN'], (3,5), 0.35, 0.50),
    'usr_d2842892c510755c': ('casual_observer', ['SOFI','PLTR','RKLB','MSFT'], (2,3), 0.55, 0.25),

    # Original early joiners — passive
    'usr_5b66bc6e49025e41': ('set_forget',      ['RKLB','NVDA','UBER'], (1,2), 0.75, 0.15),
    'usr_b7f62bd39a065227': ('quantum_skeptic', ['QBTS','TSM','HOOD','IONQ'], (1,2), 0.65, 0.25),
    'usr_8ab5296d0b2b69a0': ('intel_believer',  ['INTC','AVGO','AMD','NVDA'], (1,2), 0.60, 0.25),
    'usr_57d599bfd3e04b0a': ('space_dreamer',   ['RKLB','RDW','LUNR','ASTS'], (1,2), 0.55, 0.30),
    'usr_ad1e7655a3088e5f': ('ghost',           ['MSFT','AMZN','GOOGL'], (1,2), 0.85, 0.10),
}


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def fetch_historical_prices(tickers, start_date, end_date):
    import yfinance as yf
    prices = defaultdict(dict)
    print(f"Fetching prices for {len(tickers)} tickers {start_date.date()} → {end_date.date()}...")
    ticker_str = ' '.join(tickers)
    data = None
    try:
        data = yf.download(ticker_str, start=start_date.strftime('%Y-%m-%d'),
                          end=end_date.strftime('%Y-%m-%d'), progress=False,
                          group_by='ticker', auto_adjust=True)
    except Exception as e:
        print(f"  batch failed: {e}")

    for ticker in tickers:
        try:
            hist = None
            if data is not None:
                try:
                    hist = data.xs(ticker, axis=1, level=0)
                except (KeyError, AttributeError):
                    hist = None
            if hist is None or (hasattr(hist, 'empty') and hist.empty):
                t = yf.Ticker(ticker)
                hist = t.history(start=start_date.strftime('%Y-%m-%d'),
                                end=end_date.strftime('%Y-%m-%d'), auto_adjust=True)
            if hist is not None and not hist.empty:
                for idx, row in hist.iterrows():
                    ds = idx.strftime('%Y-%m-%d')
                    c = float(row['Close'])
                    if c > 0:
                        prices[ticker][ds] = round(c, 2)
            print(f"  {ticker}: {len(prices[ticker])} prices")
        except Exception as e:
            print(f"  {ticker}: ERROR {e}")
    return dict(prices)

def get_price(prices_cache, ticker, date):
    if ticker not in prices_cache:
        return None
    ds = date.strftime('%Y-%m-%d')
    tp = prices_cache[ticker]
    if ds in tp:
        return tp[ds]
    for offset in range(1, 6):
        for sign in [-1, 1]:
            d = date + timedelta(days=offset*sign)
            d2 = d.strftime('%Y-%m-%d')
            if d2 in tp:
                return tp[d2]
    return None

def apply_existing_trades(existing_trades, uid):
    cash = INITIAL_CASH
    holdings = defaultdict(int)
    user_trades = sorted([t for t in existing_trades if t['uid'] == uid], key=lambda t: t['date'])
    for t in user_trades:
        if t['action'] == 'buy':
            cost = t['shares'] * t['price']
            if cost > cash:
                continue
            cash -= cost
            holdings[t['ticker']] += t['shares']
        else:
            held = holdings.get(t['ticker'], 0)
            shares = min(t['shares'], held)
            if shares <= 0:
                continue
            cash += shares * t['price']
            holdings[t['ticker']] -= shares
            if holdings[t['ticker']] <= 0:
                del holdings[t['ticker']]
    return cash, dict(holdings), user_trades

def generate_new_trades(uid, strategy, ticker_focus, trades_per_month_range,
                        buy_ratio, sell_aggressiveness, prices_cache,
                        starting_cash, starting_holdings, created_at):
    """Generate evenly distributed trades across the gap months."""
    trades = []
    created_str = created_at.replace('Z', '').replace('.000', '').split('+')[0].split('-04:')[0].split('-05:')[0]
    created = datetime.fromisoformat(created_str)

    # Define active months
    start_month = max(created.month if created.year == 2025 else 1,
                      EXISTING_CUTOFF.month + 1)  # November at earliest
    start_year = 2025 if start_month >= 11 else 2026

    months = []
    y, m = start_year, start_month
    end_y, end_m = 2026, 6
    while (y < end_y) or (y == end_y and m <= end_m):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1

    if not months:
        return trades

    # Generate trades for each month
    cash = starting_cash
    holdings = defaultdict(int, starting_holdings)

    for year, month in months:
        lo, hi = trades_per_month_range
        num_this_month = random.randint(lo, hi)

        # Determine month day range
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year, month, 31)
        else:
            next_month = month + 1 if month < 12 else 1
            next_year = year if month < 12 else year + 1
            month_end = datetime(next_year, next_month, 1) - timedelta(days=1)

        # Don't go past BACKDATE_END
        if month_end > BACKDATE_END:
            month_end = BACKDATE_END

        if month_start > month_end:
            continue

        # Pick trading days in this month (weekdays preferred)
        trading_days = []
        d = month_start
        while d <= month_end:
            if d.weekday() < 5:
                trading_days.append(d)
            d += timedelta(days=1)

        if not trading_days:
            continue

        # Pick trade dates
        if len(trading_days) <= num_this_month:
            chosen_dates = trading_days
        else:
            # Pick mostly clustered dates
            chosen_dates = []
            available = list(trading_days)
            while len(chosen_dates) < num_this_month and available:
                # Pick a day and maybe cluster around it
                idx = random.randrange(len(available))
                day = available.pop(idx)
                chosen_dates.append(day)
                # Maybe add the next day too
                next_day = day + timedelta(days=1)
                if next_day in available and len(chosen_dates) < num_this_month and random.random() < 0.4:
                    available.remove(next_day)
                    chosen_dates.append(next_day)

        chosen_dates.sort()

        for d in chosen_dates:
            if cash <= 50:  # almost broke
                # Force a sell to free up cash
                held_tickers = [t for t, s in holdings.items() if s > 0]
                if not held_tickers:
                    break
                ticker = random.choice(held_tickers)
                price = get_price(prices_cache, ticker, d)
                if price is None or price <= 0:
                    continue
                sell_shares = max(1, int(holdings[ticker] * random.uniform(0.3, 0.7)))
                proceeds = sell_shares * price
                cash += proceeds
                holdings[ticker] -= sell_shares
                if holdings[ticker] <= 0:
                    del holdings[ticker]
                trades.append({
                    'ticker': ticker, 'action': 'sell', 'shares': sell_shares,
                    'price': price, 'date': d.strftime('%Y-%m-%dT%H:%M:%SZ'), 'uid': uid
                })
                continue

            is_buy = random.random() < buy_ratio

            # Pick ticker
            if random.random() < 0.60 and ticker_focus:
                ticker = random.choice(ticker_focus)
            else:
                other = [t for t in ALL_TICKERS if t not in ticker_focus]
                ticker = random.choice(other) if other else random.choice(ticker_focus)

            price = get_price(prices_cache, ticker, d)
            if price is None or price <= 0:
                continue

            if is_buy:
                max_spend = cash * random.uniform(0.04, 0.30)
                shares = max(1, min(45, int(max_spend / price)))
                cost = shares * price
                if cost > cash:
                    shares = max(1, int(cash * 0.9 / price))
                    cost = shares * price
                if cost <= 0 or cost > cash:
                    continue
                cash -= cost
                holdings[ticker] += shares
                trades.append({
                    'ticker': ticker, 'action': 'buy', 'shares': shares,
                    'price': price, 'date': d.strftime('%Y-%m-%dT%H:%M:%SZ'), 'uid': uid
                })
            else:
                held_tickers = [t for t, s in holdings.items() if s > 0]
                if not held_tickers:
                    continue
                ticker = random.choice(held_tickers)
                held = holdings[ticker]
                sell_shares = max(1, min(held, int(held * sell_aggressiveness * random.uniform(0.6, 1.0))))
                proceeds = sell_shares * price
                cash += proceeds
                holdings[ticker] -= sell_shares
                if holdings[ticker] <= 0:
                    del holdings[ticker]
                trades.append({
                    'ticker': ticker, 'action': 'sell', 'shares': sell_shares,
                    'price': price, 'date': d.strftime('%Y-%m-%dT%H:%M:%SZ'), 'uid': uid
                })

    return trades


def rebuild_all_portfolios(all_trades, accounts):
    portfolios = {}
    for username, acct in accounts.items():
        uid = acct['uid']
        portfolios[uid] = {
            'uid': uid, 'displayName': acct['displayName'],
            'photoURL': acct.get('photoURL'), 'cash': INITIAL_CASH,
            'holdings': {}, 'trades': [], 'createdAt': acct['createdAt']
        }

    sorted_trades = sorted(all_trades, key=lambda t: t['date'])
    skipped = 0
    for trade in sorted_trades:
        uid = trade['uid']
        if uid not in portfolios:
            skipped += 1; continue
        p = portfolios[uid]
        ticker, action, shares, price = trade['ticker'], trade['action'], trade['shares'], trade['price']
        if action == 'buy':
            cost = shares * price
            if cost > p['cash']:
                skipped += 1; continue
            p['cash'] -= cost
            p['holdings'][ticker] = p['holdings'].get(ticker, 0) + shares
        else:
            held = p['holdings'].get(ticker, 0)
            if shares > held:
                if held <= 0:
                    skipped += 1; continue
                shares = held
            p['cash'] += shares * price
            p['holdings'][ticker] -= shares
            if p['holdings'][ticker] <= 0:
                del p['holdings'][ticker]
        p['trades'].append(trade)

    for uid, p in portfolios.items():
        p['cash'] = round(p['cash'], 2)
        p['holdings'] = {t: s for t, s in p['holdings'].items() if s > 0}

    if skipped:
        print(f"  Skipped {skipped} invalid trades")
    return portfolios


def main():
    print("=== Hive Trade Backdating v3 ===\n")
    print("Loading data...")
    data = load_data()
    accounts = data['accounts']
    existing_trades = data.get('trades', [])
    price_cache = data.get('priceCache', {})
    print(f"  {len(accounts)} accounts, {len(existing_trades)} existing trades")

    print("\nFetching historical prices...")
    hist_prices = fetch_historical_prices(ALL_TICKERS,
                                         EXISTING_CUTOFF + timedelta(days=1),
                                         BACKDATE_END + timedelta(days=1))
    success = sum(1 for t in ALL_TICKERS if t in hist_prices and len(hist_prices[t]) > 0)
    print(f"  Got prices for {success}/{len(ALL_TICKERS)} tickers")

    print("\nGenerating new trades...")
    new_trades = []
    for username, acct in accounts.items():
        uid = acct['uid']
        persona = PERSONAS.get(uid, ('casual', ['NVDA', 'MSFT', 'AMZN'], (1,2), 0.60, 0.20))
        strategy, ticker_focus, tpm_range, buy_ratio, sell_agg = persona

        cash, holdings, user_existing = apply_existing_trades(existing_trades, uid)
        fresh = generate_new_trades(uid, strategy, ticker_focus, tpm_range,
                                   buy_ratio, sell_agg, hist_prices,
                                   cash, holdings, acct['createdAt'])
        new_trades.extend(fresh)
        print(f"  {acct['displayName']:20s} ({strategy:20s}): {len(user_existing):>2} old → {len(fresh):>2} new | pre: ${cash:,.0f}")

    print(f"\n  Total new trades: {len(new_trades)}")
    all_trades = existing_trades + new_trades
    print(f"  Total all trades: {len(all_trades)}")

    print("\nRebuilding portfolios...")
    portfolios = rebuild_all_portfolios(all_trades, accounts)

    print(f"\n{'Rank':>4}  {'Player':<20} {'Trades':>6} {'Cash':>10} {'Stk':>4} {'Value':>10} {'Return':>8}")
    print("-" * 80)

    portfolio_list = []
    for uid, p in portfolios.items():
        hv = 0
        for ticker, shares in p['holdings'].items():
            pc = price_cache.get(ticker, {})
            price = pc.get('price', 0) if isinstance(pc, dict) else 0
            if price == 0 and ticker in hist_prices and hist_prices[ticker]:
                price = hist_prices[ticker][max(hist_prices[ticker].keys())]
            hv += shares * price
        tv = p['cash'] + hv
        ret = ((tv - INITIAL_CASH) / INITIAL_CASH) * 100
        p['_tv'] = tv; p['_ret'] = ret
        portfolio_list.append(p)

    portfolio_list.sort(key=lambda p: p['_ret'], reverse=True)
    for i, p in enumerate(portfolio_list):
        print(f"{i+1:>4}  {p['displayName'][:19]:<20} {len(p['trades']):>6} ${p['cash']:>9,.2f} {len(p['holdings']):>4} ${p['_tv']:>9,.2f} {p['_ret']:>7.1f}%")

    # Write
    print("\nWriting hive-data.json...")
    clean = {}
    for uid, p in portfolios.items():
        clean[uid] = {k: v for k, v in p.items() if not k.startswith('_')}
    data['trades'] = all_trades
    data['portfolios'] = clean
    save_data(data)
    print(f"  ✅ {len(all_trades)} trades, {len(clean)} portfolios")

    returns = [p['_ret'] for p in portfolio_list]
    print(f"\n=== Stats ===")
    print(f"  Best: {max(returns):.1f}%  Worst: {min(returns):.1f}%  Avg: {sum(returns)/len(returns):.1f}%")
    print(f"  Positive: {sum(1 for r in returns if r>0)}/{len(returns)}  Negative: {sum(1 for r in returns if r<0)}/{len(returns)}")

    months = Counter(t['date'][:7] for t in all_trades)
    print("\nMonthly distribution:")
    for m in sorted(months):
        bar = '█' * (months[m] // 3)
        print(f"  {m}: {months[m]:>4} {bar}")

    print("\n✅ Done!")


if __name__ == '__main__':
    random.seed(42)
    main()
