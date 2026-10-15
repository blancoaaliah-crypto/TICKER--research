# FIN 439 - Lab 13: Portfolio Mandate Defense

## Meridian Foundation Reserve

The Meridian Foundation has a $100 million reserve. The goal of this lab is to determine which portfolios follow the client's investment rules and what needs to be clarified before building a portfolio.

## 1. Classifying the CIO Statements

S1: Hard constraint - The investment horizon is seven years, and the portfolio must be rebalanced annually.

S2: Objective - The foundation wants to earn CPI + 4% annually after costs over rolling five-year periods.

S3: Hard constraint - The foundation must pay $0.75 million quarterly and keep enough liquid reserves for four quarters.

S4: Preference - The CIO provided a benchmark of 60% global equities and 40% U.S. investment-grade bonds, but it is not a required allocation.

S5: Hard constraint - The portfolio must be long-only with no borrowing, short selling, or derivatives.

S6: Hard constraint - No single company can account for more than 8% of the portfolio.

S7: Hard constraint - Annual turnover cannot exceed 25% without committee approval.

S8: Hard constraint - At least 90% of the portfolio must be redeemable within five business days.

S9: Unverifiable promise - The CIO wants to avoid annual losses greater than 10%, but the measurement and breach rules are not defined. This cannot be guaranteed or tested with the available information.

S10: Missing - The CIO has not specified what the portfolio should optimize. There are also no sector, ESG, tax, or home-bias preferences.

## 2. Investment Policy Statement (IPS)

An Investment Policy Statement is a document that explains an investor's financial goals, investment rules, and restrictions.

It helps portfolio managers understand what they are trying to achieve and what limits they must follow.

For the Meridian Foundation, S2 explains the return objective. S1 and S3 describe the investment horizon and required payouts. S5 through S8 establish the investment restrictions. S4 provides a benchmark for comparing performance.

S9 needs clarification because the loss limit is not clearly defined. S10 also needs clarification because the CIO has not decided what the portfolio should optimize.

These statements help guide portfolio decisions before investments are selected.

## 3. Portfolio Checker Results

The portfolio has a total reserve of $100 million and quarterly distributions of $0.75 million.

Required reserve = 4 x 0.75 / 100 x 100 = 3.0%

The minimum required reserve is 3.0% of the portfolio.

### Candidate A

Weights sum: 100.0% - pass

Lowest weight: 0.0% - pass

Reserve-eligible weight: 14.0% - pass

Redeemable within five days: 100.0% - pass

Largest single company: 0.0% - pass

Calendar-year loss: requires CIO clarification

Verdict: Passes every checkable rule.

### Candidate B

Weights sum: 100.0% - pass

Lowest weight: 0.0% - pass

Reserve-eligible weight: 1.0% - FAIL

Redeemable within five days: 85.0% - FAIL

Largest single company: 9.0% - FAIL

Calendar-year loss: requires CIO clarification

Verdict: Fails 3 rules.

Candidate B does not hold enough liquid reserves, fails the five-day liquidity requirement, and exceeds the issuer concentration limit. Acme Corp bonds and stock count together toward the issuer limit.

### Candidate C

Weights sum: 100.0% - pass

Lowest weight: 0.0% - pass

Reserve-eligible weight: 2.0% - FAIL

Redeemable within five days: 100.0% - pass

Largest single company: 8.0% - pass

Calendar-year loss: requires CIO clarification

Verdict: Fails 1 rule.

Candidate C fails because its reserve-eligible investments only make up 2% of the portfolio instead of the required 3%.

## 4. Negative-Weight Test

To test the Python checker, I changed Candidate A's cash weight from 2% to -2% and increased its global equity index fund weight from 60% to 64%.

The total portfolio weight remained 100%.

The lowest weight became -2.0%, which caused the long-only rule to fail.

The reserve-eligible weight decreased from 14.0% to 10.0%, which still passed the reserve requirement.

No other rules failed.

This shows that the Python checker can identify a portfolio that violates the long-only restriction.

I then restored the original weights.

## 5. Candidate D - Challenge Portfolio

I created Candidate D with the following allocation:

- Cash: 0%
- Treasury bills: 100%
- Treasury 10-year note: 0%
- Global equity index fund: 0%
- Investment-grade bond fund: 0%
- Private real estate fund: 0%
- Acme Corp bonds: 0%
- Acme Corp stock: 0%

### Candidate D Results

Weights sum: 100.0% - pass

Lowest weight: 0.0% - pass

Reserve-eligible weight: 100.0% - pass

Redeemable within five days: 100.0% - pass

Largest single company: 0.0% - pass

Calendar-year loss: requires CIO clarification

Verdict: Passes every checkable rule.

### My Judgment

Yes, I think the CIO could reasonably reject Candidate D because investing everything in Treasury bills may not generate enough returns to meet the foundation's CPI + 4% objective.

This relates to S2 because even though the portfolio follows the checkable restrictions, it may not achieve the client's return goal.

## 6. Question for the CIO

My question:

Should the portfolio prioritize maximizing expected returns or minimizing risk while trying to achieve the CPI + 4% objective?

How the answer changes my portfolio:

If the CIO wants to prioritize returns, I would consider allocating more money toward global equities. If the CIO wants to minimize risk, I would allocate more toward Treasury securities and investment-grade bonds while still meeting the reserve and liquidity requirements.

## 7. Reflection

### Why can a portfolio pass every checkable rule and still be unsuitable for this client?

A portfolio can follow all the investment restrictions but still fail to achieve the client's financial goals. For example, Candidate D passes every rule because it is liquid, long-only, and does not violate the issuer limit.

However, investing 100% in Treasury bills may not provide enough growth to meet the foundation's CPI + 4% objective.

This shows that passing the rules does not automatically mean a portfolio is the best choice for the client.

### Which S1-S10 classification was hardest to decide?

S9 was the hardest for me because the CIO says the portfolio cannot lose more than 10% in a calendar year.

At first, this sounds like a hard constraint, but I realized that investment losses cannot be guaranteed against and the CIO did not explain how the limit should be measured or enforced.

Because of this, I classified S9 as an unverifiable promise that needs clarification.

## 8. Project 2 - Client Mandate

### Client

A young investor saving for a down payment on a house within five years.

### Investment Objective

The client wants to grow their savings while protecting the money needed for a future house down payment.

### Hard Constraints

- Investment horizon of five years.
- No borrowing or short selling.
- At least 20% of the portfolio must remain in cash or Treasury securities.
- At least 90% of the portfolio must be liquid within five business days.
- No individual company can make up more than 8% of the portfolio.

### One Question for the Client

How much short-term investment risk are you comfortable taking to potentially earn higher returns before purchasing your home?

The answer would help determine how much to invest in equities compared with safer investments such as Treasury securities and bonds.

AI Disclosure

I used Codex/ChatGPT to assist with writing and debugging the Python portfolio checker, interpreting the results, and organizing my Markdown file. AI also helped me understand the investment constraints and explain the portfolio comparisons. I reviewed the code and explanations to better understand how the rules were applied.