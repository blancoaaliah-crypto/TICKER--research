FIN 439 — Lab 15: Portfolio Stability Decision

Objective

The goal of this lab was to build a Streamlit app that finds the lowest-risk portfolio while meeting a return objective and reserve requirement. I also tested how changes in expected returns affect the recommended portfolio.

Meridian Training Results

I used the Meridian Foundation training data with a 6.5% return objective and a 3% minimum reserve requirement.

Asset

Original

Equity Return at 7%

Treasury bills

0%

0%

Treasury 10-year note

20%

10%

Investment-grade bond fund

25%

10%

Global equity index fund

55%

80%

Expected return

6.51%

6.53%

Volatility

9.44%

12.94%

Reserve eligible

20%

10%

When the equity return estimate decreased from 8% to 7%, the equity allocation increased from 55% to 80%.

The largest weight change was 25 percentage points.

This showed that a small change in one estimate can cause a large change in the portfolio allocation.

Engine Validation

I changed the correlation between investment-grade bonds and global equity from 0.25 to 0.50 in both cells of portfolio.py.

The optimizer returned:

Treasury bills: 0%

Treasury 10-year note: 40%

Investment-grade bond fund: 0%

Global equity index fund: 60%

Expected return: 6.52%

Volatility: 9.73%

These results matched the training answer. I then restored the original correlation values to 0.25.

This confirmed that the Streamlit app uses the calculations from my Python engine.

Historical Price Data

I selected four ETFs for my portfolio.

Ticker

Investment

Source

SGOV

Short-term Treasury ETF

Yahoo Finance

IEF

7–10 Year Treasury ETF

Yahoo Finance

AGG

U.S. investment-grade bond ETF

Yahoo Finance

VT

Global stock market ETF

Yahoo Finance

Historical period: September 2021 – September 2026

Data frequency: Monthly adjusted closing prices

Download date: October 22, 2026

Price observations: 61 months

Monthly return observations: 60 months

Source links:

SGOV: https://finance.yahoo.com/quote/SGOV/history/

IEF: https://finance.yahoo.com/quote/IEF/history/

AGG: https://finance.yahoo.com/quote/AGG/history/

VT: https://finance.yahoo.com/quote/VT/history/

I calculated monthly returns from the adjusted closing prices. I multiplied the average monthly return by 12 to estimate annual returns and multiplied monthly standard deviation by the square root of 12 to estimate annual volatility.

These values are historical estimates, not guaranteed future returns.

My Portfolio Mandate

For this analysis, I used the following assumptions:

Return objective: 6.5% annually

Reserve requirement: At least 3%

Reserve-eligible asset: SGOV

Investment universe: SGOV, IEF, AGG, and VT

Portfolio rule: Long-only, with weights adding to 100%

Optimization: Find the lowest-volatility portfolio in 5-percentage-point increments that meets both requirements

The purpose was to see which combination had the lowest estimated risk while still meeting the objective.

Historical Return Estimates

I calculated the following annualized return estimates from my CSV data.

Ticker

All 60 Returns

Last 36 Returns

SGOV

3.72%

4.44%

IEF

-1.79%

3.07%

AGG

-0.41%

4.15%

VT

11.90%

20.25%

The estimates changed depending on the historical period. VT had a much higher average return estimate over the last 36 months.

Portfolio Results — All Months vs. Last 36 Months

I ran the optimizer using the full historical data and then compared it with the last 36 monthly returns.

Asset / Metric

All Months

Last 36 Months

SGOV

65%

85%

IEF

0%

0%

AGG

0%

0%

VT

35%

15%

Expected return

6.58%

6.81%

Volatility

5.29%

1.79%

Reserve eligible

65%

85%

Meets 6.5% objective

Yes

Yes

Meets 3% reserve rule

Yes

Yes

Largest weight change: 20 percentage points.

The optimizer selected 65% SGOV and 35% VT using all historical returns.

When I changed the sample to the last 36 months, the allocation changed to 85% SGOV and 15% VT.

The allocation changed because the return and volatility estimates were different. The more recent data gave VT a higher expected return, so the optimizer needed less equity to reach the objective.

Both portfolios met the return objective and reserve requirement.

Stability Test

I also calculated an additional stress scenario using the full historical sample.

I reduced VT's estimated annual return by one percentage point, from approximately 11.90% to 10.90%.

Result

Original Estimate

VT Return Reduced

SGOV

65%

60%

IEF

0%

0%

AGG

0%

0%

VT

35%

40%

Expected return

6.58%

6.59%

Volatility

5.29%

6.03%

Largest weight change: 5 percentage points.

The optimizer increased the VT allocation because its expected return decreased, and more equity exposure was needed to satisfy the 6.5% objective.

This result was less sensitive than the Meridian example, but it still showed that changing one estimate affected the recommended portfolio.

This was an additional calculated scenario. The separate partner stress test should be documented with the estimate the partner actually chooses.

Partner Stress Test

Partner's selected estimate: Decrease VT's expected return from 11.90% to 10.90%.

Partner's resulting allocation: SGOV: 60%

IEF: 0%

AGG: 0%

VT: 40%

Expected return: 6.59%

Volatility: 6.03%

Largest weight change: 5 percentage points.

My response: Lowering VT's expected return caused the optimizer to increase its allocation from 35% to 40% to meet the return objective. I would be cautious about adopting this portfolio because a small change in assumptions affected the recommended investment mix.

My Decision

Decision: Pilot, not adopt.

I would pilot the recommended portfolio instead of immediately adopting it.

The full historical sample recommended 65% SGOV and 35% VT, while the last 36 months recommended 85% SGOV and 15% VT. This 20-percentage-point change shows that the recommended allocation depends on the time period used for the estimates.

I would consider adopting the portfolio only after reviewing the return estimates, testing more scenarios, and confirming that it meets the client's full investment mandate.

Estimation Risk

Estimation risk is the possibility that expected returns, volatility, and correlations are inaccurate.

An optimizer uses these inputs to find the lowest-risk portfolio meeting the objective. Even small differences in expected returns can cause the optimizer to shift investments.

In the Meridian example, lowering the equity return estimate by one percentage point increased the equity allocation by 25 percentage points.

In my historical portfolio, changing from the full sample to the last 36 months moved 20 percentage points between SGOV and VT.

These results show why the optimizer's recommendation should not automatically be treated as the best portfolio for the future.

Reflection

The lowest-risk portfolio changed because the estimated returns and risks were different across the two historical periods.

The optimizer selected different weights while continuing to meet the same return objective.

Before adopting the portfolio, I would want more confidence in the historical estimates, additional stress testing, and confirmation that the client's liquidity and risk requirements were satisfied.

I learned that a portfolio can meet the objective mathematically but still need further review before being used for a real investment decision.

AI Disclosure

I used ChatGPT to help build and debug my Python portfolio optimizer and Streamlit app. AI helped explain the code, fix errors, and calculate the portfolio results from my historical CSV data.

I verified the Meridian training calculations using the app and compared the outputs against the provided expected results.

The portfolio analysis is a learning demonstration and not investment advice.