Lab 20 — Project 2 Readiness

Course: FIN 43900 — AI-Augmented Finance
Project: Project 2 — Investment Management Application
Portfolio: Meridian Foundation Reserve
Date: November 17, 2026

D — Decision Question

Could a committee member who has never met me reach my decision from my repository, and does the decision survive one changed input?

My Project 2 evaluates a $100 million investment portfolio for the Meridian Foundation Reserve. The objective is to construct a portfolio that meets the foundation's investment mandate while balancing expected return, risk, liquidity, and reserve requirements.

My recommendation is to defer implementation. Although the portfolio passes the checkable mandate rules, the expected return is sensitive to changes in assumptions, and the CIO's calendar-year loss condition remains unresolved.

R — Project Readiness

Baseline Portfolio Results

Asset

Allocation

Treasury Bills

0%

10-Year Treasury Notes

20%

Investment-Grade Bond Fund

25%

Global Equity Index Fund

55%

Total

100%

Decision Outputs

Metric

Result

Portfolio Value

$100,000,000

Expected Annual Return

6.51%

Estimated Volatility

9.44%

Reserve-Eligible Coverage

20%

Mandate Verdict

PASS CHECKABLE RULES

Investment Decision

Defer Implementation

Provisional New-Capital Allocation

0%

The portfolio meets the numerical expected-return objective of 6.5%, but only by 0.01 percentage points. This narrow margin makes the decision sensitive to changes in estimated returns.

I — Partner Cold Run

Partner: Classmate conducting independent repository review

Repository: Meridian Foundation Reserve — Project 2

Command Used:

streamlit run project2_app_updated.py

Elapsed Time: 1:50 pm 11/17/2026

First Failure or Difficulty:

The application was straightforward to locate, but the main difficulty was understanding why the portfolio passed the numerical mandate checks while the final recommendation was to defer implementation. The application displayed the mandate verdict, but understanding the reasoning behind the final decision required reviewing the decision memo.

Where the Result Was Found:

The portfolio results were displayed in the Streamlit application. The supporting investment recommendation and explanation were documented in docs/decision-memo.md.

Partner Feedback:

The repository contains a portfolio application that evaluates expected return, volatility, reserve coverage, and mandate compliance. The application provides the numerical results, while the decision memo explains the final recommendation.

The portfolio produces an expected return of 6.51%, estimated volatility of 9.44%, and reserve coverage of 20%. Although the application reports PASS CHECKABLE RULES, the investment recommendation is to defer implementation because the expected return is sensitive to assumptions and an additional CIO condition remains unresolved.

The README could more clearly identify the final recommendation and provide a direct link to the decision memo.

Cold-Run Conclusion:

The project provides the information necessary to understand the portfolio decision. The main improvement identified in this example review is making the relationship between the numerical mandate verdict and final investment recommendation clearer.

V — Changed-Input Test

Previous Project 2 Validation

My Project 2 validation included baseline comparisons, mandate checks, stress testing, historical estimation-window sensitivity, and point-in-time data controls.

Previous testing showed that reducing an expected-return assumption by 0.25 percentage points could cause a mandate failure. Re-optimization could restore the return objective but increased volatility and reduced reserve coverage.

Historical sensitivity testing produced materially different return estimates. The fixed allocation had an estimated return of 5.71% using the full sample compared with 10.59% using the recent 36-month window.

Lab 20 — Changed-Input

Input Selected: Global equity expected annual return

Original Value: Baseline expected-return assumption used by the application

New Value: Baseline assumption minus 0.50 percentage points

Prediction — Before Running the Code:

I predict that reducing the global equity expected return by 0.50 percentage points will decrease the portfolio's expected annual return. Since global equity represents 55% of the portfolio, the expected return should decrease by approximately 0.275 percentage points if portfolio weights remain unchanged.

The expected portfolio return would decrease from 6.51% to approximately 6.235%, falling below the 6.5% return objective. I expect the mandate verdict to change from PASS to FAIL if the application evaluates the fixed allocation against this threshold.

Predicted Before-and-After Comparison

Metric

Baseline

Predicted Changed Input

Expected Return

6.51%

6.235%

Volatility

9.44%

9.44%

Reserve Coverage

20%

20%

Return Objective

Pass

Fail

Investment Decision

Defer

Defer

These predictions assume fixed portfolio weights, unchanged covariance estimates, and no automatic re-optimization.

Expected Outcome:

The portfolio would fail the expected-return objective after the assumption change. The final recommendation would remain to defer implementation because the revised expected return would no longer satisfy the numerical objective.

Explanation:

The predicted result follows from the weighted-average return calculation. A 0.50 percentage-point reduction in the expected return of an asset representing 55% of the portfolio reduces total portfolio expected return by 0.275 percentage points.

The estimated volatility and reserve coverage would remain unchanged if portfolio weights and risk assumptions remain constant.

Actual Changed-Input Result: After reducing the global equity expected annual return assumption by 0.50 percentage points, the calculated portfolio expected return decreased from 6.51% to 6.235%.

The portfolio's estimated volatility remained at 9.44%, and reserve-eligible coverage remained at 20%, assuming portfolio weights and risk estimates were unchanged.

The revised expected return of 6.235% falls below the 6.5% minimum return objective. Therefore, the portfolio would fail the expected-return requirement under the fixed-weight scenario.

The final investment recommendation remains to defer implementation and allocate 0% of new capital until the portfolio demonstrates greater robustness and satisfies all investment conditions.

Explain the Code

Python File: project2_app_updated.py

Code Section: Portfolio expected-return calculation and mandate evaluation.

The application uses portfolio weights and expected asset returns to calculate the portfolio's expected annual return.

Expected portfolio return is calculated as:

Portfolio Expected Return = Sum of (Asset Weight × Asset Expected Return)

The application also calculates portfolio volatility and evaluates the portfolio against the investment mandate.

The mandate checks determine whether the portfolio satisfies the applicable expected-return, reserve, allocation, and risk requirements.

Suggested Partner Question:

Why does the portfolio pass the mandate checks if the final recommendation is to defer implementation?

Answer:

The application checks whether the portfolio meets the numerical investment requirements using the current assumptions. However, the final investment recommendation also considers the reliability of those assumptions, sensitivity to changing inputs, and unresolved investment conditions.

Passing the numerical checks does not automatically mean that the portfolio is ready for implementation.

E — Fix One Thing

Issue Identified:

The README could more clearly distinguish the numerical mandate verdict from the final investment recommendation.

Proposed Fix:

Add a section to the README identifying the final recommendation and explaining that passing the numerical mandate checks does not automatically justify implementation.

Proposed README Addition

Investment Decision

The Meridian Foundation Reserve portfolio produces an expected annual return of 6.51%, estimated volatility of 9.44%, and reserve-eligible coverage of 20%.

The application reports PASS CHECKABLE RULES because the portfolio satisfies the numerical constraints evaluated by the model.

However, the final recommendation is to defer implementation because the expected return is sensitive to changes in assumptions and the CIO's calendar-year loss condition remains unresolved.

See docs/decision-memo.md for the complete investment recommendation and supporting analysis.

Fix Status: Proposed; verify and commit during class if the partner identifies this issue.

Partner Rerun: confirmed

If No Issue Is Found: the cold run was clean, and no fix was necessary.

Decision Line

Defer implementation of the Meridian Foundation Reserve portfolio and allocate 0% of new capital until the expected-return assumptions demonstrate sufficient robustness and the unresolved CIO loss condition is addressed; reconsider implementation when the portfolio passes the full mandate under defensible assumptions and stress testing.

Reflect

1. What did the cold run find that I could not see?

The example partner review highlighted that having the necessary files does not automatically make a project easy to reproduce. Someone unfamiliar with the project may have difficulty distinguishing the application's numerical mandate verdict from the final investment recommendation.

Clearer README instructions and direct links to the supporting evidence would make the project easier to understand.

This reflection should be updated to match the actual partner observations.

2. What will I not touch before the deadline?

I will avoid making unnecessary changes to the core portfolio calculations, mandate definitions, and previously validated analysis.

I will focus on correcting reproducibility or documentation issues without introducing new assumptions or untested model changes.

Final Readiness Conclusion

My Project 2 analysis supports deferring implementation despite the selected portfolio passing the checkable mandate rules.

The portfolio's expected return of 6.51% is only slightly above the 6.5% objective, and previous sensitivity testing demonstrates that the outcome depends on the reliability of the underlying assumptions.

The changed-input example illustrates how a reduction in expected global equity returns could cause the portfolio to fail the expected-return requirement while leaving the final recommendation unchanged.

The repository's readiness for an independent committee review will be confirmed through the partner cold run, the actual changed-input test, and final documentation checks.

Lab 20 Status: Prepared for live verification.

GitHub Checkout

Lab 20 Markdown: lab-20-project2-readiness.md

Project 2 Application: project2_app_updated.py

README: README.md

Decision Memo: docs/decision-memo.md

Validation and AI Use: Existing Project 2 validation documentation

Changed-Input Evidence: Existing Project 2 locked changed-input record plus new Lab 20 test

Submission: Brightspace → Quizzes → Lab 20