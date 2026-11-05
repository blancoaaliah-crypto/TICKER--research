
---
name: graham-investor
description: Evaluate a company using Benjamin Graham's liquidity and earnings checks.
---

# Benjamin Graham Investor Skill

## Purpose

Evaluate a company's financial strength using a rules-based investment screen focused on liquidity and earnings consistency.

This is an educational implementation of the Graham approach used in FIN 43900 Lab 19.

## Data Source

Use SEC EDGAR 10-K financial information.

Use the same five fiscal years and financial data as the Buffett and Burry skills.

Do not estimate missing financial information.

## Required Financial Data

- Fiscal year end
- Current assets
- Current liabilities
- Net income

## Calculations

Current ratio = Current assets / Current liabilities

If current liabilities are zero, negative, or missing, mark the current ratio as not known.

## Investment Checks

### Check 1 — Current Ratio

The latest fiscal year's current ratio must be at least 2.0.

Pass: Current ratio >= 2.0

Fail: Current ratio < 2.0

Not known: Required financial data is unavailable or invalid.

### Check 2 — Positive Net Income

Net income must be positive in every year analyzed.

Pass: Net income > 0 in every year.

Fail: At least one year has zero or negative net income, with sufficient evidence to establish failure.

Not known: Missing information prevents a reliable conclusion.

### Check 3 — Net Income Growth

Net income in the latest fiscal year must exceed net income in the first fiscal year.

Pass: Latest net income > first-year net income.

Fail: Latest net income <= first-year net income.

Not known: Either required value is unavailable.

## Verdict

Report the number of passing checks out of three.

Do not describe a company as passing every check if any result is not known.

## Investment Memo

Generate a short memo containing:

- Company and ticker
- Latest current ratio
- Current-ratio threshold
- Net income trend
- Results of the three checks
- Overall verdict
- Limitations or missing information

Use only financial numbers printed by the analysis script.

Do not invent financial figures.

## Threshold Probe

Allow the current-ratio threshold to change from 2.0 to 1.0 for the Lab 19 sensitivity test.

Record how the verdict changes.

Use 2.0 as the default threshold unless the analyst explicitly chooses otherwise.

## Validation

Test against Costco (COST).

Expected latest current ratio: 1.06.

Expected results at threshold 2.0: two of three checks pass.

Expected results at threshold 1.0: three of three checks pass.

These expected results are validation targets, not hardcoded company data.