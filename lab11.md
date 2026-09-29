# Lab 11 — Ulta Beauty (ULTA) Sensitivity Analysis

## My Contribution

I used my Lab 10 Ulta Beauty Python model and added sensitivity analysis to test how changes in two assumptions affect the company's financial projections. I tested revenue growth and SG&A as a percentage of gross profit. I compared operating income, free cash flow to equity (FCFE), and estimated value per share.

## 1. Assumptions Tested

I used my original Lab 10 assumptions as the base case and tested each assumption one at a time. I used a one-percentage-point increase and decrease around each base assumption to compare how the results would change. I chose these ranges as simple illustrative changes, not company guidance.

| Assumption | Lower | Base | Higher |
|---|---:|---:|---:|
| Revenue growth | 4% | 5% | 6% |
| SG&A / Gross Profit | 67.034% | 68.034% | 69.034% |

Both assumptions were tested for FY2026–FY2030. All other independent assumptions remained at their base values.

## 2. Prediction

Prediction documented: 09/29/2026 at 1:35 PM.

I expected that increasing Ulta's revenue growth from 5% to 6% would increase operating income and cash flow because the company would generate more sales. I also expected that lowering SG&A expenses would increase operating income and cash flow because the company would spend less on operating expenses. My rough estimate was that higher revenue growth would increase operating income by around $50 million.


## 3. Revenue Growth Sensitivity

All financial amounts are in USD millions, except per-share values. Operating income and FCFE are for FY2030E.

| Revenue Growth | Operating Income | FCFE | Value Per Share |
|---|---:|---:|---:|
| 4% | 1,865.12 | 1,252.71 | $329.54 |
| 5% (Base) | 1,956.53 | 1,291.31 | $337.73 |
| 6% | 2,051.49 | 1,330.43 | $346.02 |

Increasing revenue growth from 5% to 6% increased 2030 operating income by $94.96 million and FCFE by $39.12 million. Estimated value per share increased by $8.29.

Higher revenue growth increases sales and gross profit. However, operating expenses and inventory also increase, which affects how much cash flow the company generates.

## 4. SG&A Sensitivity

| SG&A / Gross Profit | Operating Income | FCFE | Value Per Share |
|---|---:|---:|---:|
| 67.034% | 2,018.37 | 1,338.05 | $350.09 |
| 68.034% (Base) | 1,956.53 | 1,291.31 | $337.73 |
| 69.034% | 1,894.69 | 1,244.57 | $325.37 |

Reducing SG&A from 68.034% to 67.034% increased 2030 operating income by $61.84 million and FCFE by $46.74 million. Estimated value per share increased by $12.36.

Lower SG&A allows Ulta to keep more of its gross profit, increasing operating income and cash flow.

## 5. Output Spans

An output span is the highest result minus the lowest result.

| Output | Revenue Growth Span | SG&A Span |
|---|---:|---:|
| Operating Income | $186.37 million | $123.68 million |
| FCFE | $77.71 million | $93.48 million |
| Value Per Share | $16.48 | $24.73 |

Revenue growth had the larger effect on operating income, while SG&A had the larger effect on FCFE and estimated value per share over the ranges tested. These results depend on the assumptions and ranges selected.

## 6. Validation and Accounting Checks

I tested one independent assumption at a time while keeping the other assumptions at their original base values.

My Python model checked that the balance sheet remained balanced during each scenario. After running the sensitivity analysis, I restored the original base case.

Restored Base Check: PASS

The original base results matched the restored results.

For example, increasing revenue growth from 5% to 6% changed operating income from $1,956.53 million to $2,051.49 million.

2,051.49 - 1,956.53 = +94.96 million

This confirms the change from the base case.

## 7. Financial Judgment

The sensitivity results show that both revenue growth and operating expenses affect Ulta's projected performance. Revenue growth had the larger operating income span, while SG&A had the larger FCFE and valuation spans.

The SG&A assumption is worth researching further because changes in operating expenses significantly affected my estimated value per share. I would review Ulta's historical SG&A expenses to better understand whether my selected range is reasonable.

Sensitivity analysis does not show how likely each scenario is. It only shows how the model's results change when an assumption changes.

## 8. Partner Discussion

### Partner Exchange 1 — Prediction

**Partner's Question:** Why did you choose to test revenue growth and SG&A?

**My Response:** I chose revenue growth because it affects how much money Ulta makes from sales. I chose SG&A because it affects the company's operating expenses and profits. I wanted to see which assumption had a bigger effect on the results.

### Partner Exchange 2 — Validation

**What I Checked on My Partner's Model:** I checked my partner's change in operating income by subtracting her base operating income of $838.87 million from her new operating income of $993.96 million.

993.96 - 838.87 = +155.09 million

My calculation matched her Python output, confirming that the change in operating income was calculated correctly.

**Partner's Question About My Results:** How did you know your results were correct?

**My Response:** I checked that my balance sheets balanced and that my original base case matched after running the different scenarios. I also checked that increasing revenue growth from 5% to 6% increased operating income by $94.96 million.

### Partner Exchange 3 — Interpretation

**Partner's Question:** Why did SG&A have a bigger effect on cash flow and value than revenue growth?

**My Response:** Lower SG&A means Ulta spends less on operating expenses and keeps more of its gross profit. This increases cash flow and estimated value. SG&A had the bigger effect on these results over the ranges I tested. Changing the ranges could change which driver has the larger effect.

**What I Learned From My Partner:** I learned that my partner's company, ADM, has relatively thin profit margins, so changes in gross margin can have a large effect on its operating income.

## 9. Reflection

My prediction was partially correct. I expected that increasing Ulta's revenue growth from 5% to 6% would increase operating income and cash flow. I estimated that operating income would increase by around $50 million, but it actually increased by $94.96 million. I also expected that lowering SG&A expenses would improve operating income and cash flow, which the results supported.

What surprised me was that SG&A had a larger effect on FCFE and estimated value per share, even though revenue growth had a larger effect on operating income over the ranges tested. This showed me that controlling expenses can significantly affect Ulta's financial performance.

Based on these results, I would want to research Ulta's historical SG&A expenses to see whether my selected range is reasonable. This could help me better understand how operating expenses might affect the company's future value. The sensitivity results did not change my base valuation, but they showed me an assumption I should investigate further.

## AI Disclosure

I used ChatGPT/Codex to help modify my Lab 10 Python model to include sensitivity analysis, organize my results into tables, and understand how changes in assumptions affect operating income, FCFE, and estimated value per share. I reviewed the code and terminal results and used them to prepare my analysis.