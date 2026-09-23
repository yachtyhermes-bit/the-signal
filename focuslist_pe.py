import yfinance as yf, pandas as pd, numpy as np, json

TICKERS = ["AVGO", "CEG", "SOFI", "NFLX"]
out = {}
for t in TICKERS:
    tk = yf.Ticker(t)
    h = tk.history(period="7y", auto_adjust=False, actions=False)
    if getattr(h.index, "tz", None) is not None:
        h.index = h.index.tz_localize(None)
    close = h["Close"].dropna()
    try:
        ed = tk.get_earnings_dates(limit=40)
    except Exception as e:
        ed = None
    rows = []
    if ed is not None:
        for idx, r in ed.iterrows():
            rep = r.get("Reported EPS")
            if pd.notna(rep):
                rows.append((idx.tz_localize(None) if getattr(idx, "tz", None) is not None else idx, float(rep)))
    rows.sort()
    eps = pd.Series({d: v for d, v in rows})
    # TTM EPS at any date = sum of last 4 reported quarterly EPS available as of that date
    monthly = close.resample("ME").last()
    ttm_vals = {}
    dates = list(eps.index)
    for m in monthly.index:
        avail = [v for d, v in rows if d <= m]
        if len(avail) >= 4:
            ttm_vals[m] = sum(avail[-4:])
    series = pd.Series(ttm_vals)
    pe = monthly.reindex(series.index) / series
    pe = pe[pe > 0]
    last5 = pe[pe.index >= (pe.index[-1] - pd.DateOffset(years=5))]
    out[t] = dict(
        pe_5y_avg=round(float(last5.mean()), 1),
        pe_5y_median=round(float(last5.median()), 1),
        pe_min=round(float(last5.min()), 1),
        pe_max=round(float(last5.max()), 1),
        pe_now_trailing=round(float(pe.iloc[-1]), 1),
        n_months=int(len(last5)),
        quarters_used=len(rows),
        first_q=str(rows[0][0].date()) if rows else None,
        last_q=str(rows[-1][0].date()) if rows else None,
        ttm_eps_now=round(float(series.iloc[-1]), 2),
    )
    print(t, json.dumps(out[t], indent=1))
json.dump(out, open("/home/chino/thesignal/focuslist_pe_proxy.json", "w"), indent=1)
print("SAVED")
