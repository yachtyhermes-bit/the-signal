import json, yfinance as yf

KEYS = ["currentPrice","marketCap","fiftyTwoWeekHigh","fiftyTwoWeekLow","trailingPE","forwardPE",
        "freeCashflow","totalCash","totalDebt","totalRevenue","revenueGrowth","grossMargins",
        "operatingMargins","profitMargins","targetMeanPrice","targetHighPrice","targetLowPrice",
        "recommendationKey","numberOfAnalystOpinions","enterpriseValue","sharesOutstanding","beta",
        "shortPercentOfFloat","ebitda","earningsGrowth","forwardEps","trailingEps"]

out = {}
for tk in ["ASTS", "VRT", "HOOD", "CEG"]:
    t = yf.Ticker(tk)
    fi = t.fast_info
    d = {}
    for k, v in fi.items():
        d[k] = str(v)[:50] if v is not None else None
    try:
        info = t.info
    except Exception as e:
        info = {"error": str(e)}
    try:
        news = t.news
    except Exception as e:
        news = [{"error": str(e)}]
    try:
        rec = t.recommendations.head(6).to_dict() if hasattr(t.recommendations, "head") else str(t.recommendations)
    except Exception as e:
        rec = {"error": str(e)}
    try:
        cal = t.calendar
    except Exception as e:
        cal = {"error": str(e)}
    out[tk] = {
        "fast_info": d,
        "info": {k: v for k, v in info.items() if k in KEYS},
        "news": [{"title": n.get("title"), "publisher": n.get("publisher"), "link": n.get("link"),
                  "providerPublishTime": n.get("providerPublishTime")} for n in news[:8]],
        "rec": rec,
        "calendar": cal,
    }

with open("candidates_yf_out.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
