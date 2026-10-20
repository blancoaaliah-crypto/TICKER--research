
# FIN 439 — Lab 14: Portfolio Baselines

## Objective

The goal of this lab was to build a Python portfolio risk engine and compare three portfolio strategies for the Meridian Foundation Reserve. I calculated expected returns, volatility, and reserve-eligible weights to see whether the portfolios met the 6.5% return objective.

## Portfolio Results

| Portfolio | Expected Return | Volatility | Reserve Eligible | Meets Return Objective |
|---|---|---|---|---|
| Benchmark | 6.80% | 10.46% | 0.0% | Yes |
| Equal Weight | 5.20% | 5.21% | 50.0% | No |
| Inverse Volatility | 3.77% | 1.05% | 90.3% | No |

The benchmark has the highest expected return but also the highest volatility. The inverse volatility portfolio has the lowest risk but does not meet the return objective.

## Diversification

Diversification means spreading investments across different assets to reduce overall portfolio risk.

It works because investments do not always move in the same direction. When the correlation between assets is below +1, combining them can reduce risk compared with assets moving perfectly together.

For the benchmark portfolio, I used 40% investment-grade bonds and 60% global equities.

Portfolio variance:

(0.40^2 × 0.06^2) + (0.60^2 × 0.16^2) + (2 × 0.40 × 0.60 × 0.06 × 0.16 × 0.25)

= 0.010944

Portfolio volatility:

sqrt(0.010944) = 10.46%

This shows how the correlation between the two investments affects total portfolio risk.

## Inverse Volatility

Inverse volatility gives higher portfolio weights to investments with lower volatility.

Treasury bills receive the largest allocation because their volatility is only 0.5%, which is much lower than the other investments.

This results in a portfolio with low risk but a lower expected return of 3.77%.

## CIO Recommendation

I would show the CIO the benchmark portfolio first because it has the highest expected return of 6.80% and meets the 6.5% return objective.

However, it does not meet Meridian's reserve requirement, so I would explain that the portfolio needs adjustments before it could be considered suitable.

## Validation and Testing

I ran the validation tests in VS Code to make sure my Python code worked correctly.

Known Answer Test: All three portfolios matched the expected returns, volatilities, and reserve weights from the lab.

Correlation Test: I changed the IG bond and equity correlation from 0.25 to 0.50 in both cells. The benchmark volatility increased from 10.46% to 11.00%, as expected.

Invalid Correlation Test: I changed a correlation to 1.3, and the program correctly rejected the invalid input.

Mandate Test: I ran mandate.py with Candidate E. It failed one rule because its reserve-eligible weight was 0.0%.

After testing, I restored the original correlation values in portfolio.py.

All validation tests passed.

## Mandate Checker — Candidate E

I updated my Lab 13 mandate.py file to include Candidate E, consisting of:

- 40% investment-grade bond fund
- 60% global equity index fund

The results were:

- Weights sum to 100%: Pass
- Long-only requirement: Pass
- Reserve eligible: 0.0% — FAIL
- Liquidity within five days: Pass
- Issuer concentration: Pass
- Calendar-year loss: Requires CIO clarification

Final verdict: Candidate E fails one checkable mandate rule.

Although the benchmark meets the expected return objective, it fails Meridian's minimum 3% reserve requirement.

## Files

- portfolio.py — Calculates portfolio weights, returns, volatility, and reserve eligibility.
- mandate.py — Checks portfolio allocations against Meridian's mandate rules.

## AI Disclosure

I used Codex/ChatGPT to assist with writing and organizing the Python code for the portfolio risk engine, including the covariance matrix, portfolio volatility calculations, and input validation. I also used AI to help add Candidate E to my existing mandate checker and organize my written explanations for this lab.

I reviewed the code and compared the outputs with the known answers provided in the assignment. AI was used as a coding and learning assistant, while I was responsible for running the programs, checking the results, and completing the lab.