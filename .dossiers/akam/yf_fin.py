import yfinance as yf, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',60); pd.set_option('display.max_rows',200)
t=yf.Ticker("AKAM")
print("=== QUARTERLY CASHFLOW (last 6) ===")
cf=t.quarterly_cashflow
if cf is not None and not cf.empty:
    cols=list(cf.columns)[:6]
    for lab in ['Operating Cash Flow','Capital Expenditure','Free Cash Flow','Purchase Of PPE','Issuance Of Debt','Repayment Of Debt','Repurchase Of Capital Stock','Stock Based Compensation']:
        if lab in cf.index:
            print(lab, [None if pd.isna(cf.loc[lab,c]) else float(cf.loc[lab,c]) for c in cols])
    print("cols:",[str(c) for c in cols])
print()
print("=== ANNUAL CASHFLOW ===")
af=t.cashflow
if af is not None and not af.empty:
    print("cols:",[str(c) for c in af.columns])
    for lab in ['Operating Cash Flow','Capital Expenditure','Free Cash Flow','Purchase Of PPE']:
        if lab in af.index:
            print(lab, [None if pd.isna(af.loc[lab,c]) else float(af.loc[lab,c]) for c in af.columns])
print()
print("=== QUARTERLY BALANCE SHEET ===")
qb=t.quarterly_balance_sheet
if qb is not None and not qb.empty:
    cols=list(qb.columns)[:4]
    print("cols:",[str(c) for c in cols])
    for lab in ['Cash And Cash Equivalents','Cash Cash Equivalents And Short Term Investments','Other Short Term Investments','Long Term Debt','Current Debt','Total Debt','Capital Lease Obligations','Long Term Capital Lease Obligations','Net Debt','Ordinary Shares Number','Share Issued','Stockholders Equity','Total Liabilities Net Minority Interest']:
        if lab in qb.index:
            print(lab, [None if pd.isna(qb.loc[lab,c]) else float(qb.loc[lab,c]) for c in cols])
print()
print("=== INFO extras ===")
i=t.info
for k in ['totalCash','totalDebt','freeCashflow','operatingCashflow','totalRevenue','ebitda','trailingPE','sharesShort','floatShares']:
    print(k,":",i.get(k))
