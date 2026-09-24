# Lab 10 — Ulta Beauty (ULTA)

## My Contribution

I used my Lab 9 Python code and changed it to model Ulta Beauty. I updated the financial information and assumptions to fit Ulta's business. My model projects five years of financial statements and calculates an estimated value per share.

## 1. Historical Financial Data

Source: Ulta Beauty FY2025 and FY2024 10-K filings.
All figures are in USD millions.

| Item | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 11,207.3 | 11,295.7 | 12,392.8 |
| Gross profit | 4,381.1 | 4,387.3 | 4,845.2 |
| SG&A | 2,694.6 | 2,808.6 | 3,296.4 |
| Net income | 1,291.0 | 1,201.1 | 1,153.5 |
| Inventory | 1,742.1 | 1,968.2 | 2,181.1 |
| PP&E | 1,182.3 | 1,239.3 | 1,434.1 |
| Shareholders' equity | 2,279.3 | 2,488.4 | 2,803.5 |

### Historical Data Sources

- FY2025 10-K, pages 53–54: FY2024 and FY2025 financial data and FY2023–FY2025 income statements.
  https://www.sec.gov/Archives/edgar/data/1403568/000110465926035243/ulta-20260131x10k.htm

- FY2024 10-K, pages 51–52: FY2023 balance sheet data and historical income statements.
  https://www.sec.gov/Archives/edgar/data/1403568/000155837025003810/ulta-20250201x10k.htm

### Historical Data Verification

I checked Ulta's FY2025 10-K to verify its revenue of $12,392.8 million and net income of $1,153.5 million.

## 2. Historical Ratios

| Ratio | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Gross margin | 39.1% | 38.8% | 39.1% |
| SG&A / Gross profit | 61.5% | 64.0% | 68.0% |
| Inventory days | 93.1 | 104.0 | 105.5 |
| D&A / PP&E | 20.6% | 21.5% | 21.0% |
| Capital spending ($M) | 435.3 | 374.5 | 434.8 |
| Tax rate | 23.9% | 24.0% | 24.4% |
| Revenue growth | 9.8% | 0.8% | 9.7% |
| Comparable sales growth | 5.7% | 0.7% | 5.4% |

### Capital Spending Comparison

Ulta reported capital spending of $434.8 million in FY2025 in its 10-K. I used $435 million in my model to keep future spending close to that amount.

I could not confirm the data provider's capital spending figure, so I used the amount reported in Ulta's 10-K.

### 3. My Assumptions & Judgements

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth | 5% | Judgment | I assumed Ulta would continue growing, but not as quickly as its latest reported growth. |
| Gross margin | 39.1% | Judgment | I used Ulta's 2025 margin and kept it the same. |
| SG&A / Gross profit | 68.0% | Judgment | I used Ulta's 2025 expense ratio. |
| Inventory days | 105.5 | Judgment | I assumed Ulta would manage inventory similarly to 2025. |
| D&A / PP&E | 21.0% | Judgment | I used the 2025 ratio to estimate future depreciation and amortization. |
| Capital spending | $435M | Judgment | I assumed Ulta would spend about the same amount as in 2025. |
| Tax rate | 24.4% | Judgment | I kept the tax rate close to 2025. |
| Share buybacks | $0M | Judgment | I left out future buybacks to keep the model simple. |
| Minimum cash | $100M | Judgment | I assumed Ulta would keep some cash available. |
| Cost of equity | 10% | Judgment | I used 10% as the return investors would require. |
| Terminal growth | 2.5% | Judgment | I assumed Ulta would grow more slowly in the long run. |
 Existing debt interest rate | 5.5% | Judgment | I assumed a fixed borrowing rate. |
| Revolver interest rate | 6% | Judgment | I assumed this rate if Ulta needs to borrow money. |
| Revolver limit | $1,000M | Judgment | I used this limit as a simplified borrowing assumption. |
| Annual debt repayment | $0M | Judgment | I assumed no scheduled debt repayment. |
| Operating lease balances | Constant | Judgment | I kept lease balances unchanged to simplify the model. |
| Diluted shares | 44.991M | History/Judgment | I kept the FY2025 share count constant for valuation. |

## 4. What Makes Ulta Different?

ABG sells cars and uses floor plan financing to pay for inventory. Ulta sells beauty products and has operating leases for its stores.

I removed ABG's floor plan financing and included Ulta's operating lease assets and liabilities. I kept the lease balances constant to simplify my model.

## 5. Five-Year Forecast

All figures are in USD millions.

| Year | Revenue | Net Income | FCFE |
|---|---:|---:|---:|
| 2026 | 13,012.5 | 1,214.0 | 970.7 |
| 2027 | 13,663.1 | 1,274.9 | 1,054.3 |
| 2028 | 14,346.2 | 1,338.7 | 1,134.7 |
| 2029 | 15,063.6 | 1,405.8 | 1,213.3 |
| 2030 | 15,816.7 | 1,476.2 | 1,291.3 |

All five balance sheet checks passed with a zero gap. Cash stayed above the $100 million minimum, and Ulta did not need to borrow from the revolver.

## 6. Equity Valuation

| Item | Value |
|---|---:|
| PV of five-year FCFE | $4,236.8M |
| PV of terminal value | $10,958.0M |
| Total equity value | $15,194.8M |
| Diluted shares | 44.991M |
| Estimated value per share | $337.73 |

My model estimates Ulta's value at $337.73 per share.

Ulta's market price was $543.81 on September 23, 2026. My model gives a lower value, which makes me question whether my growth assumptions are too conservative or whether the market expects stronger future performance.

## 7. Organic Growth

Organic growth is growth from a company's existing business rather than acquisitions. Ulta uses comparable sales growth to show how its existing stores are performing.

Ulta reported 5.4% comparable sales growth in FY2025, compared with 9.7% total revenue growth.

The ABG example uses 1.8% instead of its reported 4.7% growth because the model assumes a lower rate of ongoing growth rather than expecting all reported growth to continue.

## 8. Reflection

I would defend my 2.5% terminal growth assumption because I do not think Ulta can keep growing at 5% forever.

One number that stood out to me was Ulta's $1.15 billion in net income for FY2025. This shows how much profit Ulta earned, even though its expenses were increasing.

My model is simplified because I kept lease balances constant and did not include future share buybacks. These assumptions could affect my estimated value per share.

## 9. Partner Review

**Partner's question:** Why did you assume Ulta's revenue would grow by 5% each year?

**My response:** I chose 5% because Ulta reported 5.4% comparable sales growth in FY2025. I would lower my assumption if Ulta's sales growth started slowing down.

**My question to my partner:** What made you choose your revenue growth assumption, and how would your valuation change if growth was lower?

## 10. AI Disclosure

I used ChatGPT to help adapt my Lab 9 Python code to Ulta Beauty, organize the financial information, calculate historical ratios, and prepare my Markdown report. I ran the Python model and reviewed its output.