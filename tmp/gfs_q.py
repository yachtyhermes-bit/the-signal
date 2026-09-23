import yfinance as yf, json
t = yf.Ticker("GFS")
out={}
def df2(d):
    try:
        d=d.dropna(how="all"); d=d.loc[:, ~d.columns.isna()]
        return {str(c.date()): {str(i): (None if v!=v else (round(float(v),1) if isinstance(v,(int,float)) or str(v).replace('.','',1).replace('-','',1).replace('e','',1).isdigit() else v)) for i,v in d[c].items()} for c in d.columns}
    except Exception as e:
        return {"err":str(e)}
try: out["income_q"]=df2(t.quarterly_income_stmt)
except Exception as e: out["income_q_err"]=str(e)
try: out["cashflow_q"]=df2(t.quarterly_cashflow)
except Exception as e: out["cf_q_err"]=str(e)
try: out["balance_q"]=df2(t.quarterly_balance_sheet)
except Exception as e: out["bs_q_err"]=str(e)
print(json.dumps(out, indent=1, default=str))
