import yfinance as yf, json, pandas as pd

data = json.load(open("/home/chino/thesignal/focuslist_yf_out.json"))
rows = {}
fwd_eps_fy1 = {"AVGO": 19.38391, "CEG": 13.34165, "SOFI": 0.82759, "NFLX": 3.81626}
fwd_eps_fy0 = {"AVGO": 11.65766, "CEG": 12.11777, "SOFI": 0.59625, "NFLX": 3.58437}
for t in ["AVGO", "CEG", "SOFI", "NFLX"]:
    d = data[t]
    p = d["last_close"]
    rows[t] = dict(
        px=p,
        pe_fy1=round(p / fwd_eps_fy1[t], 1),
        pe_fy0=round(p / fwd_eps_fy0[t], 1),
        yf_forwardPE=round(d["fwdPE"], 1),
        yf_trailingPE=round(d["trailPE"], 1),
        hi52=d["hi52"], lo52=d["lo52"],
        pct_from_hi=d["pct_from_hi"], pct_from_lo=d["pct_from_lo"], pct_of_range=d["pct_of_range"],
        dist50=d["dist_50d"], dist200=d["dist_200d"],
        ytd_dec=d["ytd_vs_dec31"], ytd_jan=d["ytd_vs_jan2"],
        c1y=d["chg_1y"], c3y=d["chg_3y"],
    )
    tk = yf.Ticker(t)
    try:
        sp = tk.splits
        rows[t]["splits"] = {str(k.date()): float(v) for k, v in sp.items()} if len(sp) else {}
    except Exception as e:
        rows[t]["splits"] = f"ERR {e}"
    print(t, json.dumps(rows[t]))

# derived thresholds for article accountability lines
print()
print("AVGO: pct of own 5y-avg trailing PE (32.0):", round(data["AVGO"]["fwdPE"] / 32.0 * 100, 1), "%")
print("CEG : pct of own 5y-avg trailing PE (30.8):", round(data["CEG"]["fwdPE"] / 30.8 * 100, 1), "%")
print("NFLX: pct of own 5y-avg trailing PE (40.1):", round(data["NFLX"]["fwdPE"] / 40.1 * 100, 1), "%")
print("NFLX PE on FY26 consensus 3.58437:", round(76.41 / 3.58437, 1))
print("SOFI PE on company FY26 guide 0.60:", round(16.84 / 0.60, 1))
print("CEG PE on company FY26 guide mid 12.00:", round(259.53 / 12.00, 1))
print("CEG PE on company FY26 guide low 11.50:", round(259.53 / 11.50, 1), " high 12.50:", round(259.53 / 12.50, 1))
print("CEG downside to 32 yf target:", round((348.30 / 259.53 - 1) * 100, 1), "%")
print("AVGO implied upside to yf target 531.85:", round((531.8468 / 339.51 - 1) * 100, 1), "%")
print("SOFI implied upside to yf target 20.34:", round((20.34091 / 16.84 - 1) * 100, 1), "%")
print("NFLX implied upside to yf target 93.88:", round((93.88222 / 76.41 - 1) * 100, 1), "%")
print("AVGO mktcap $T:", round(data["AVGO"]["mktcap"] / 1e12, 2))
print("NFLX mktcap $B:", round(data["NFLX"]["mktcap"] / 1e9, 1))
print("SOFI mktcap $B:", round(data["SOFI"]["mktcap"] / 1e9, 2))
print("CEG mktcap $B:", round(data["CEG"]["mktcap"] / 1e9, 1))
print("NFLX 52w range width %:", round((data["NFLX"]["hi52"] / data["NFLX"]["lo52"] - 1) * 100, 1))
print("AVGO 3y chg check (298.6%):", data["AVGO"]["chg_3y"])
print("NFLX implied shares (B):", round(data["NFLX"]["mktcap"] / data["NFLX"]["last_close"] / 1e9, 3))
