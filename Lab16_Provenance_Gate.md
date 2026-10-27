FIN 439 — Lab 16: Provenance Gate

Objective

The goal of this lab was to build a Python point-in-time filter to determine what financial data was actually available on a specific investment decision date. This helps prevent look-ahead bias, which happens when a backtest uses information that was not available at the time of the decision.

Methodology

I created asof.py using Python's standard library and applied four filtering rules in the required order:

Quarantine: Remove rows with missing tickers.

Duplicates: Remove identical observations.

Publication Dates: Remove data published after the decision date.

Revisions: Keep the latest published value for each ticker and month.

The original decision date was March 31, 2026. I also tested April 15, 2026, to confirm that the filter updates correctly when additional information becomes available.

Row Funnel Results — March 31, 2026

Filtering Step

Rows Removed

Missing ticker

11

Exact duplicate

7

Published after decision date

3, 8, 10

Older revision

2

Final as-of panel

1, 4, 5, 6, 9, 12

The program correctly applied the four rules and produced the expected final panel of six observations.

As-of vs. Naive Signals — March 31, 2026

Ticker

As-of Signal

Naive Signal

AAA

+1.98% (February)

+5.83% (March)

BBB

-1.02% (February)

-5.15% (March)

CCC

+0.91% (February)

+1.82% (February, revised)

All six calculated signals matched the professor's expected answers.

Revision Example — AAA

AAA had two February observations:

Row 2: Index 104.0, published March 10.

Row 4: Index 103.0, published March 25.

Since both were available by March 31, the program kept the newer publication, row 4.

As-of signal:

(103 / 101 - 1) × 100 = +1.98%

The naive calculation uses March's index of 109.0, which was not published until April 10.

Naive signal:

(109 / 103 - 1) × 100 = +5.83%

The difference of 3.85 percentage points shows how information published later can change the investment signal.

Validation — April 15, 2026

I changed the decision date in asof.py to April 15, 2026, and ran the program again.

Row Funnel Results:

Filtering Step

Rows Removed

Missing ticker

11

Exact duplicate

7

Published after decision date

None

Older revisions

2, 12

Final as-of panel

1, 3, 4, 5, 6, 8, 9, 10

Signal Results:

Ticker

As-of Signal

Naive Signal

AAA

+5.83% (March)

+5.83% (March)

BBB

-5.15% (March)

-5.15% (March)

CCC

+1.82% (February)

+1.82% (February)

All three as-of signals matched the naive signals.

This confirms that the filter correctly accounts for publication dates and revisions. By April 15, all observations in the training table had been published, so the as-of and naive calculations were identical.

Point-in-Time Learning

1. What is look-ahead bias?

Look-ahead bias occurs when an investment strategy uses information that was not available when the investment decision was originally made. This can create misleading backtest results.

2. Why do event time, publication time, and revisions matter?

The month measured tells us when the economic activity occurred, while the publication date tells us when investors could actually access that information. Revisions update previously published values, but they should only be used after the revision becomes available.

3. Why is AAA's naive signal misleading?

AAA's naive signal is +5.83% because it uses March data published on April 10. That information was unavailable on March 31. The correct signal based on available information was +1.98%.

Reflection

1. Which filtering rule mattered most?

Rule 3, removing late publications, was especially important because it prevented future information from affecting the March 31 signals. Rule 4 also mattered because it ensured that the latest available revision was used instead of an outdated observation.

2. What would a naive backtest claim?

A naive backtest could make an investment strategy appear more accurate or effective than it actually was. For example, AAA's naive signal was +5.83%, compared with the knowable +1.98% signal. Using future information could lead to unrealistic investment conclusions.

Conclusion

This lab demonstrated why point-in-time data is important for financial analysis. My Python filter successfully removed missing tickers, duplicates, late publications, and outdated revisions.

The March 31 results matched the professor's expected answers, and the April 15 validation confirmed that the as-of and naive signals became identical once all observations were available.

This approach helps make historical investment analysis more accurate by ensuring that decisions are based only on information available at the time.

Files

asof.py — Python code implementing the four filtering rules and calculating the signals.

Lab16_Provenance_Gate.md — Documentation of the results, validation, and reflection.

AI Disclosure

I used Codex/ChatGPT to assist with writing and debugging my Python code, applying the point-in-time filtering rules, and organizing my Markdown documentation. I ran the code myself, verified the results against the professor's expected answers, and tested the April 15 decision date to confirm the filter worked correctly.