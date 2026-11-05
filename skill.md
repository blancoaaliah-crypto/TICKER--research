
---
name: burry-investor
description: Evaluate a company using Michael Burry's cash flow and leverage checks.
---

# Michael Burry Investor Skill

## Purpose

Evaluate a company's financial strength using cash flow quality and balance-sheet leverage.

This is an educational implementation of the Burry approach used in FIN 43900 Lab 19.

## Data Source

Use SEC EDGAR 10-K financial information.

Use the same fiscal years and financial information as the Buffett and Graham skills.

Do not estimate missing values.

## Required Financial Data

- Fiscal year end
- Net income
- Operating cash flow
- Total liabilities
- Shareholders' equity

## Calculations

Liabilities-to-equity ratio = Total liabilities / Shareholders' equity

If shareholders' equity is zero, negative, or missing, mark the ratio as not known.

## Investment Checks

### Check 1 — Cash Flow Quality

Operating cash flow must be at least equal to net income in every year analyzed.

Pass: Operating cash flow >= net income every year.

Fail: At least one year has operating cash flow below net income.

Not known: Missing information prevents a reliable conclusion.

### Check 2 — Financial Leverage

Latest total liabilities must be no more than twice shareholders' equity.

Pass: Liabilities / Equity <= 2.0.

Fail: Liabilities / Equity > 2.0.

Not known: Required financial information is unavailable or invalid.

## Verdict

Report the number of passing checks out of two.

If a check is not known, identify it clearly rather than assuming a pass.

## Investment Memo

Generate a short investment memo containing:

- Company and ticker
- Operating cash flow and net income
- Latest liabilities-to-equity ratio
- Results of both checks
- Overall verdict
- Missing information or limitations

Use only numbers printed by the analysis script.

Do not fabricate financial figures or unsupported conclusions.

## Validation

Test the skill using Costco (COST).

Expected latest liabilities-to-equity ratio: 1.49.

Expected results:

- Operating cash flow >= net income every year: Pass.
- Latest liabilities <= 2x equity: Pass.

Expected overall verdict: two of two checks pass.

These values are validation benchmarks and must not be hardcoded into the analysis.