Lab 17 — Point-in-Time Audit

FIN 43900 — AI-Augmented Finance

D — Decision Question

Was each number in my series knowable on the day I would have traded on it, and may Project 2 use it?

The purpose of this lab was to determine whether financial data was actually available on a historical decision date. Using today's revised or newly published values in a historical backtest can introduce look-ahead bias.

I selected DGS10, the 10-year Treasury yield, because interest rates affect Treasury securities, bond prices, and portfolio allocation decisions.

R — Data Sources

I used data from the Federal Reserve Bank of St. Louis through FRED and ALFRED.

BAA: Moody's Baa corporate bond yield, monthly

FEDFUNDS: Effective federal funds rate, monthly

DGS10: 10-year Treasury yield, daily

MORTGAGE30US: 30-year fixed mortgage rate, weekly

PAYEMS: Total nonfarm payroll employment, monthly

FRED provides current data, while ALFRED provides historical vintages showing what was known on an earlier date.

I — Application

I created asof_app.py using Python and Streamlit.

The application downloads current and historical data, displays individual line charts, allows users to add additional series, and compares observations across decision dates.

It also identifies observations published after the historical date and counts revised values. Cached download functions reduce repeated requests, and invalid series IDs are handled without stopping the application.

V — Known-Answer Validation

I tested the application using October 5, 2026.

Series

Last Date Known

Value

Result

BAA

September 2026

6.47

PASS

FEDFUNDS

September 2026

3.75

PASS

DGS10

October 2, 2026

5.28

PASS

MORTGAGE30US

October 1, 2026

7.28

PASS

All four values matched the expected results provided in the lab instructions.

PAYEMS Revision Test

I added PAYEMS and selected January 15, 2025.

Last observation known: December 2024

Historical value: 159,536 thousand jobs

Today's December 2024 value: lower than the historical value

Revised observation count: greater than zero

This confirmed that the application distinguishes historical vintages from current data and detects revisions.

E — My Series: DGS10

Data Card

Series ID: DGS10

Source: Board of Governors of the Federal Reserve System, distributed through FRED.

Source link: https://fred.stlouisfed.org/series/DGS10

Measure: Market yield on U.S. Treasury securities at a constant maturity of 10 years.

Units: Percent per annum, not seasonally adjusted.

Frequency: Daily, on applicable business days.

Publication lag: The H.15 interest-rate data is generally published on business days. An observation's date does not guarantee that its value was available before a trading decision on that date.

Revisions: Market interest-rate data generally experiences fewer revisions than economic statistics such as employment, but corrections are possible. Historical vintages must still be checked.

Download date: October 29, 2026.

Historical Availability

For the October 5, 2026 decision date, the latest DGS10 observation known in the app was October 2, 2026, with a yield of 5.28%.

This demonstrates that an observation can have a measurement date earlier than the decision date. Values published later must not be included in a historical trading signal.

Three FRED Source Checks

Observation Date

DGS10 Value

October 27, 2026

4.99%

October 26, 2026

5.00%

October 23, 2026

5.00%

I manually compared all three observations with the FRED DGS10 source page and my application's current series and confirmed that the values matched.

September 30 vs. October 29

Historical decision date: September 30, 2026

Current comparison date: October 29, 2026

Last observation known on September 30: September 29,2026

New observations since September 30: 21

Revised observations: 0

This comparison illustrates that observations appearing after September 30 would not have been available for a trading decision on that date. DGS10 is a daily market-rate series, so I would expect relatively few revisions compared with economic indicators such as PAYEMS.

V — Explain the Code

The download_vintage() function accepts a FRED series ID and a historical vintage date. It constructs an ALFRED CSV download URL and retrieves the values available for that vintage.

The read_csv() function reads the downloaded file, converts dates and numerical values, removes missing observations, and sorts the data chronologically.

The application filters the historical observations to the selected decision date and compares them with today's values.

The most important protection against look-ahead bias is requesting the historical vintage rather than using today's complete dataset for earlier decisions.

Partner question: How does the app prevent future information from being used in a historical decision?

My answer: The app downloads historical data from ALFRED using the selected vintage date instead of relying only on today's FRED data. It then filters observations to the decision date, preventing later observations from entering the historical comparison.

Partner Attack

Field challenged: Publication timing 

Potential concern: A yield dated October 5 might not have been available when a trading decision was made earlier that day.

Response: The observation date and publication date are not necessarily identical, so using same-day data could introduce look-ahead bias. I would check the ALFRED vintage and use the latest previously available observation when the exact publication time cannot be verified.

Your Call — Project 2

Decision: Conditional Admit — DGS10

I would admit DGS10 into Project 2 only when the observations are restricted to information available by each historical decision date.

DGS10 is relevant to my Treasury and bond portfolio because changes in interest rates influence bond valuations and risk.

As-of rule: Use the latest DGS10 observation confirmed to be available before the trading decision. If same-day publication timing cannot be established, use the latest confirmed prior-business-day value.

Condition: If the historical availability or publication timing cannot be verified, quarantine the observation until reliable point-in-time evidence is available. Reject its use if the information cannot be verified.

Learn on My Own

1. What is a data card?

A data card documents the source, measure, units, frequency, publication lag, revisions, and download date of a dataset. It helps determine whether the data is appropriate for a particular analysis.

2. Which fields prevent information leakage?

Publication timing, observation dates, historical vintages, and revision history help prevent look-ahead bias. These fields establish what information was available when a historical decision was made.

3. Why is "cleaned the data" not a data card?

Cleaning data only describes formatting, missing-value treatment, or duplicate removal. A data card also explains where the information came from and whether it was available at the correct time. Clean data can still contain future information.

Reflection

DGS10 is reported daily, but the observation date does not necessarily indicate when the information became available to investors.

The app demonstrates how the available dataset changes when selecting an earlier decision date. Observations appearing in today's dataset may not have been available at that time.

Using today's complete dataset in a historical backtest could overstate the accuracy of trading signals and portfolio performance because the model might react to information unavailable to investors.

This lab showed me why point-in-time validation is necessary before using financial data in investment decisions.

AI Disclosure

I used Codex/ChatGPT to help develop and debug the Streamlit application, organize the Markdown documentation, and improve clarity. I independently ran the application and verified the required known-answer tests.

Files for Submission

asof_app.py — Streamlit application

lab17_point_in_time_audit.md — Lab documentation

Both files will be uploaded to GitHub and submitted through Brightspace.
