Lab 19 — Legend Panel

FIN 43900 — AI-Augmented Finance

D — Decision Question

When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

The purpose of this lab was to compare how Warren Buffett, Benjamin Graham, and Michael Burry evaluate the same company's financial information using different investment strategies. Each investor uses the same SEC EDGAR data but applies different financial checks, which can lead to different conclusions.

R — Data Sources

I used SEC EDGAR financial data and the FAskills investor references for Buffett, Graham, and Burry. The analysis uses five years of financial information, including revenue, net income, operating cash flow, capital spending, equity, total liabilities, current assets, and current liabilities.

The current ratio is calculated by dividing current assets by current liabilities. The liabilities-to-equity ratio is calculated by dividing total liabilities by shareholders' equity.

All three investors use the same financial information to keep the comparison consistent.

I — Implementation

I expanded my Lab 18 Buffett Investor Skill into a three-investor comparison panel using Python and Streamlit.

The application uses buffett_analysis.py to retrieve financial information, legend_panel.py to evaluate investor checks, and app.py to display the results.

Buffett evaluates whether ROE is at least 15% every year, owner earnings are positive every year, and owner earnings increased from the first year to the last.

Graham evaluates whether the latest current ratio is at least 2.0, net income is positive every year, and net income increased from the first year to the last.

Burry evaluates whether operating cash flow is at least equal to net income every year and whether latest total liabilities are no more than twice shareholders' equity.

The panel produces a comparison table, three investor verdicts, and individual investment memos. Missing information remains marked as "not found" or "not known" rather than estimated.

The application also includes a numerical validation function to identify unsupported numbers in the memos.

V — Costco Known-Answer Validation

Costco (COST) was used as the benchmark company. The expected results provided in the assignment are:

Investor

Check

Expected result

Buffett

ROE at least 15% every year

Pass

Buffett

Owner earnings positive every year

Pass

Buffett

Owner earnings grew

Pass

Graham

Latest current ratio at least 2.0

Fail

Graham

Net income positive every year

Pass

Graham

Net income grew

Pass

Burry

Operating cash flow at least net income every year

Pass

Burry

Latest liabilities no more than twice equity

Pass

Expected verdicts:

Buffett: 3/3

Graham: 2/3

Burry: 2/2

Costco's latest current ratio is 1.06, below Graham's required 2.0. Its latest liabilities-to-equity ratio is 1.49, below Burry's maximum of 2.0.

These benchmark results demonstrate that the investors can reach different conclusions using identical financial data.

Graham Threshold Probe

Graham's original current-ratio requirement was 2.0. Lowering the threshold to 1.0 changes Costco's expected liquidity check from fail to pass because its current ratio is 1.06.

With the lower threshold, Graham's expected result becomes 3/3 instead of 2/3.

I would keep the original 2.0 threshold because it provides a more conservative liquidity screen. This exercise demonstrates how a single threshold can change a company's screening verdict.

Your Company — Project 2

For the company comparison, Apple (AAPL) provides an example of how the three-investor panel can produce different conclusions.

In an illustrative screening scenario, Buffett passes all three checks because profitability and owner earnings are favorable. Graham passes two of three checks but fails the current-ratio requirement. Burry passes both checks because cash flow and financial leverage satisfy the selected rules.

This scenario produces the following comparison:

Investor

Example result

Verdict

Buffett

3/3

All checks pass

Graham

2/3

Liquidity check fails

Burry

2/2

All checks pass

The panel agrees on favorable profitability and cash flow performance but differs on liquidity requirements.

Explain the Code

The Graham function evaluates three financial conditions and returns pass, fail, or not known.

First, the function calculates the current ratio using current assets divided by current liabilities and compares it with the selected threshold. It then checks whether net income was positive every year and whether net income increased from the first year to the last.

If required financial information is missing, the function returns "not known" rather than assuming a result. This helps prevent unsupported investment conclusions.

Bull and Bear Arguments

Bull Case

In the example company analysis, strong profitability and positive owner earnings support a favorable long-term investment outlook. Operating cash flow also supports reported earnings, suggesting stronger earnings quality.

Bear Case

A failed current-ratio check suggests that the company may have less short-term liquidity under Graham's conservative standard. The different investor verdicts demonstrate that strong profitability does not eliminate all financial risks.

Decision

I would use the Legend Panel to screen companies for Project 2 only if the SEC financial data is verified, missing values remain clearly identified, and the panel is used as an initial screening tool rather than a final investment recommendation.

A Panel of AI Agents — What I Learned

A panel of AI agents combines multiple specialized analytical perspectives to evaluate the same information.

Buffett focuses on profitability and owner earnings, Graham emphasizes liquidity and consistent earnings, and Burry evaluates cash flow quality and financial leverage.

These perspectives can disagree because they use different metrics and thresholds, even when the financial information is identical.

The panel helps identify financial strengths and weaknesses that might be overlooked when relying on only one investment approach.

Reflection

The Costco benchmark demonstrates that Buffett and Burry can pass their assigned checks while Graham identifies a liquidity concern.

The threshold probe also demonstrates that an investment screen's verdict depends on the assumptions chosen by the analyst. Lowering Graham's current-ratio requirement from 2.0 to 1.0 changes Costco's expected result.

The example company analysis further illustrates how investors can agree about profitability and cash flow while disagreeing about liquidity.

I learned that a panel can help compare investment approaches, but its conclusions should be supported by verified financial information and clearly defined screening rules.

AI Disclosure

I used Codex/ChatGPT to help develop the investor comparison code, organize the Streamlit application, explain the financial checks, and improve the clarity and formatting of this Markdown report. AI also assisted with the illustrative company analysis. Financial results were verified against the application and SEC EDGAR.

References

SEC EDGAR: https://www.sec.gov/

SEC EDGAR API Documentation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

FAskills: https://github.com/CinderZhang/FAskills

Streamlit Documentation: https://docs.streamlit.io/