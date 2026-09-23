import yfinance as yf
import pandas as pd
import json, sys

TICKERS = ["AVGO", "CEG", "SOFI", "RTX", "AMZN", "NFLX"]
OUT = {}

for t in TICKERS:
    tk = yf.Ticker(t)
    h = tk.history(period="6y", auto_adjust=False, actions=False)
    if getattr(h.index, "tz", None) is not None:
        h.index = h.index.tz_localize(None)
    close = h["Close"].dropna()
    info = tk.info
    last = close.iloc[-1]
    lastdate = close.index[-1].date()
    # 52wk
    w = close[close.index >= (close.index[-1] - pd.Timedelta(days=365))]
    hi, lo = w.max(), w.min()
    rng = hi - lo
    pos = (last - lo) / rng * 100 if rng else float("nan")
    frm_hi = (last / hi - 1) * 100
    frm_lo = (last / lo - 1) * 100
    ma50 = close.rolling(50).mean().iloc[-1]
    ma200 = close.rolling(200).mean().iloc[-1]
    d50 = (last / ma50 - 1) * 100
    d200 = (last / ma200 - 1) * 100
    # baselines
    def pick(day, altday):
        try:
            v = close.asof(pd.Timestamp(day))
        except Exception:
            v = None
        try:
            v2 = close.asof(pd.Timestamp(altday))
        except Exception:
            v2 = None
        return v, v2
    dec31 = close.asof(pd.Timestamp("2025-12-31"))
    jan2 = close.asof(pd.Timestamp("2026-01-02"))
    ytd_dec = (last / dec31 - 1) * 100
    ytd_jan = (last / jan2 - 1) * 100
    y1 = (last / close.asof(pd.Timestamp("2025-09-16")) - 1) * 100
    y3 = (last / close.asof(pd.Timestamp("2023-09-16")) - 1) * 100
    OUT[t] = dict(
        last_close=round(float(last), 2),
        last_date=str(lastdate),
        hi52=round(float(hi), 2), hi52_date=str(w.idxmax().date()),
        lo52=round(float(lo), 2), lo52_date=str(w.idxmin().date()),
        pct_of_range=round(float(pos), 1),
        pct_from_hi=round(float(frm_hi), 1),
        pct_from_lo=round(float(frm_lo), 1),
        ma50=round(float(ma50), 2), ma200=round(float(ma200), 2),
        dist_50d=round(float(d50), 1), dist_200d=round(float(d200), 1),
        dec31_close=round(float(dec31), 2), jan2_close=round(float(jan2), 2),
        ytd_vs_dec31=round(float(ytd_dec), 1), ytd_vs_jan2=round(float(ytd_jan), 1),
        chg_1y=round(float(y1), 1), chg_3y=round(float(y3), 1),
        info_price=info.get("currentPrice"),
        fwdPE=info.get("forwardPE"), trailPE=info.get("trailingPE"),
        mktcap=info.get("marketCap"), name=info.get("shortName"),
        peg=info.get("trailingPegRatio"),
        eps_fwd=info.get("forwardEps"), eps_trail=info.get("trailingEps"),
        rev_ttm=info.get("totalRevenue"), gm=info.get("grossMargins"),
        pm=info.get("profitMargins"), target=info.get("targetMeanPrice"),
        rec=info.get("recommendationKey"),
        ev_ebitda=info.get("enterpriseToEbitda"),
        ps=info.get("priceToSalesTrailing12Months"),
        pb=info.get("priceToBook"),
    )
    print("=" * 70)
    print(t, json.dumps(OUT[t], indent=1))

with open("/home/chino/thesignal/focuslist_yf_out.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("SAVED")
