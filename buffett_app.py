
import re
import os
import streamlit as st
import pandas as pd

from buffett_analysis import analyze

st.set_page_config(page_title="Buffett Investor Skill", layout="wide")

st.title("Lab 18 — Buffett Investor Skill")
st.caption(
    "Data from SEC EDGAR; built with AI help, "
    "a learning demonstration, not investment advice."
)

ticker = st.text_input("Enter stock ticker", "COST").strip().upper()

user_agent = os.getenv("SEC_USER_AGENT")

if not user_agent:
    st.error("Set SEC_USER_AGENT with your name and email.")
    st.stop()

try:
    result = analyze(ticker, user_agent)
except Exception as e:
    st.error(f"Unable to retrieve company data: {e}")
    st.stop()

rows = result["rows"]
checks = result["checks"]

st.subheader(f"{result['company']} ({ticker})")

# Financial table
df = pd.DataFrame(rows)
columns = [
    "fy_end", "revenue", "net_income",
    "operating_cash_flow", "capital_spending",
    "equity", "roe", "owner_earnings"
]

display_df = df[columns].copy()
display_df = display_df.rename(columns={
    "fy_end": "Fiscal Year End",
    "revenue": "Revenue ($M)",
    "net_income": "Net Income ($M)",
    "operating_cash_flow": "Operating Cash Flow ($M)",
    "capital_spending": "Capital Spending ($M)",
    "equity": "Equity ($M)",
    "roe": "ROE (%)",
    "owner_earnings": "Owner Earnings ($M)"
})

st.subheader("Five-Year Financial Results")
st.dataframe(display_df.fillna("not found"), use_container_width=True)

# Chart
st.subheader("Owner Earnings vs. Net Income")

chart_df = df.set_index("fy_end")[
    ["owner_earnings", "net_income"]
]
chart_df.columns = ["Owner Earnings", "Net Income"]

st.line_chart(chart_df)

# Buffett checks
st.subheader("Buffett's Three Checks")

labels = {
    "roe_15_every_year": "ROE >= 15% every year",
    "owner_earnings_positive": "Owner earnings positive every year",
    "owner_earnings_grew": "Owner earnings grew from first to last year"
}

for key, label in labels.items():
    st.write(f"**{label}:** {checks[key]}")

# XBRL tags
with st.expander("View SEC XBRL Tags"):
    for row in rows:
        st.write(f"**{row['fy_end']}**")
        st.json(row["tags"])

# Investment memo
st.subheader("Buffett Investment Memo")

memo_path = f"buffett_memo_{ticker}.md"

if os.path.exists(memo_path):
    with open(memo_path, encoding="utf-8") as f:
        original_memo = f.read()
else:
    original_memo = ""

memo = st.text_area(
    "Memo (editable for validation test)",
    value=original_memo,
    height=250
)

# Flag numerical values not printed by the analysis script.
# Include ROE rounded to one decimal and financial values in millions.
allowed = set()

for row in rows:
    for key in [
        "revenue", "net_income", "operating_cash_flow",
        "capital_spending", "equity", "owner_earnings", "roe"
    ]:
        value = row.get(key)
        if value is not None:
            allowed.add(round(float(value), 1))
            allowed.add(round(float(value), 0))

# Include fiscal-year labels and the three-check threshold.
for row in rows:
    allowed.add(float(row["fy_end"][:4]))

allowed.add(15.0)
allowed.add(5.0)

numbers = re.findall(
    r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?%?(?![A-Za-z0-9])",
    memo
)
unsupported = []

for number in numbers:
    numeric = float(number.replace(",", "").replace("%", ""))
    if round(numeric, 1) not in allowed:
        unsupported.append(number)

if unsupported:
    st.error(
        "Unsupported numbers in memo: "
        + ", ".join(unsupported)
    )
else:
    st.success("No unsupported numbers detected.")

st.markdown("### Memo Preview")
st.markdown(memo)