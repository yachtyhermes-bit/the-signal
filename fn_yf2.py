#!/usr/bin/env python3
"""Pull FN analyst estimates & news via yfinance."""
import json
import yfinance as yf

t = yf.Ticker("FN")
out = {}

for attr in ["analyst_price_targets", "earnings_estimate", "revenue_estimate",
             "growth_estimates", "earnings_history", "recommendations_summary",
             "upgrades_downgrades", "calendar"]:
    try:
        v = getattr(t, attr)
        if hasattr(v, "to_json"):
            out[attr] = json.loads(v.to_json())
        else:
            out[attr] = v
    except Exception as e:
        out[attr] = {"err": str(e)}

try:
    news = t.news
    items = []
    for n in (news or [])[:25]:
        items.append({"title": n.get("title"), "publisher": n.get("publisher"),
                      "link": n.get("link"), "providerPublishTime": n.get("providerPublishTime")})
    out["news"] = items
except Exception as e:
    out["news_err"] = str(e)

print(json.dumps(out, indent=1, default=str))
