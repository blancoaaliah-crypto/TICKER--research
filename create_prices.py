# FIN 439 — Lab 15
# Download real historical ETF prices

import yfinance as yf
import pandas as pd
from datetime import date

tickers = ["SGOV", "IEF", "AGG", "VT"]

# Five years of monthly prices, ending with
# the last fully completed month.
start_date = "2021-09-01"
end_date = "2026-10-01"

prices = {}

for ticker in tickers:
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=False,
        progress=False,
        multi_level_index=False
    )

    if data.empty or "Adj Close" not in data.columns:
        raise ValueError(f"Missing price data: {ticker}")

    # Last adjusted closing price of each month
    monthly = data["Adj Close"].resample("ME").last()
    prices[ticker] = monthly

df = pd.DataFrame(prices).dropna()
df.index.name = "Date"

if len(df) < 61:
    raise ValueError(
        f"Expected 61 monthly prices; found {len(df)}. "
        "Check the download or date range."
    )

df.to_csv("prices.csv", float_format="%.6f")

print("prices.csv created successfully!")
print("Source: Yahoo Finance")
print("Download date:", date.today())
print("Tickers:", tickers)
print("Monthly price rows:", len(df))
print("First date:", df.index.min().date())
print("Last date:", df.index.max().date())