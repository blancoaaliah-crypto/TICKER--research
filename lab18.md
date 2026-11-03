Lab 18 — Legend Investor as Skill

FIN 43900 — AI-Augmented Finance

D — Decision Question

Can an investor's philosophy become a skill that AI runs consistently, with every financial number calculated by code from a company's 10-K and the investment judgment made by the AI model?

The purpose of this lab was to turn Warren Buffett's investment philosophy into a reusable AI skill. Python retrieves and calculates the financial data, while the AI interprets the results to determine whether a company meets Buffett's investment criteria.

R — Data Sources and Rules

I used SEC EDGAR to retrieve financial information from companies' 10-K filings. The analysis covers the last five fiscal years and uses XBRL tags to identify revenue, net income, operating cash flow, capital spending, and stockholders' equity.

The script calculates return on equity (ROE) by dividing net income by year-end equity. Owner earnings are calculated by subtracting capital spending from operating cash flow.

The three Buffett checks are:

ROE must be at least 15% every year.

Owner earnings must be positive every year.

Owner earnings must increase from the first year to the last year.

Missing values are not estimated. Instead, the script represents them as missing data, and checks that depend on those values return "not known."

I — Implementation

I created SKILL.md to provide instructions for applying Buffett's investment philosophy consistently. The skill directs the AI to use financial data calculated by Python rather than generating its own numbers.

I created buffett_analysis.py to retrieve company facts from SEC EDGAR using a stock ticker. The script identifies the last five fiscal years, extracts the required financial information, calculates ROE and owner earnings, and evaluates Buffett's three checks.

I also created buffett_app.py using Streamlit. The app displays a five-year financial table, a chart comparing net income and owner earnings, the three Buffett checks, and an investment memo.

The app also checks the memo for numerical values that were not included in the script's financial results.

V — Validation and Probes

Costco (COST)

I tested my Python script using Costco and compared the results with the known-answer table provided in the lab instructions.

The financial results matched all five fiscal years from FY2022 through FY2026.

Buffett Check

Result

ROE at least 15% every year

Pass

Owner earnings positive every year

Pass

Owner earnings increased from first to last year

Pass

Costco's ROE was 28.3% in FY2022 and 25.8% in FY2026. Owner earnings increased from $3,501 million in FY2022 to $9,382 million in FY2026.

The Streamlit app successfully displayed the financial results, chart, checks, and investment memo.

JPMorgan (JPM)

I also tested JPMorgan to verify how the script handles missing financial information.

Capital spending and owner earnings were unavailable under the required XBRL tags. The script returned missing values for these metrics, and both owner-earnings checks returned "not known."

JPMorgan's ROE check returned "fail."

This confirmed that the script does not estimate missing financial information.

Unsupported Number Test

I manually added an unsupported ROE of 40.0% to Costco's investment memo.

The Streamlit app correctly displayed the warning:

"Unsupported numbers in memo: 40.0%"

This confirmed that the app could identify a number that was not supported by the script's output.

Fresh-Chat Comparison

A fresh AI chat without the installed Buffett skill would not necessarily follow the same SEC EDGAR retrieval rules or provide reproducible calculations. This comparison remains to be tested separately.

Explain the Code

The calculate_row() function converts SEC EDGAR company facts into financial results for one fiscal year.

First, it identifies the appropriate XBRL tags for each financial metric. It selects values from 10-K filings that match the fiscal-year-end date and uses annual periods for income and cash flow information.

Next, it calculates ROE by dividing net income by stockholders' equity and multiplying by 100.

It calculates owner earnings by subtracting capital spending from operating cash flow.

If a required value is unavailable, the function returns None rather than estimating a number. The app can then display the missing value as "not found."

The calculations are performed by Python, while the AI is responsible for interpreting the financial results.

Decision — Buffett's Verdict on Costco

Recommendation: OWN

I generally trust the Buffett-style assessment of Costco because the company passed all three financial checks. Costco maintained strong ROE and positive owner earnings throughout the five-year period, with owner earnings increasing overall.

However, the analysis only evaluates business quality and does not consider the stock price. Therefore, the results do not determine whether Costco is attractively valued.

Learn — Agent Skills

An AI skill is a reusable set of instructions that helps an AI complete a specific task consistently.

A skill contains a SKILL.md file with a name, description, and instructions. The AI can initially read the name and description to determine whether the skill is relevant, then load the detailed instructions when needed.

Financial calculations belong in Python because code follows defined formulas and data-selection rules consistently. The AI model is better suited for interpreting those results and explaining the investment judgment.

Reflect

My Buffett skill makes the financial data retrieval, calculations, and three investment checks consistent each time it runs. The AI model is responsible for interpreting the results and deciding whether to recommend owning, watching, or passing on a business.

Reporting "not found" is better than estimating a missing value because estimates could create misleading financial results. Using only available SEC data makes the analysis more transparent, consistent, and reproducible.

AI Disclosure

I used AI assistance to help develop and debug the Python script, create the Streamlit app, organize the skill instructions, and improve the clarity and formatting of this write-up. I ran the code and verified the Costco and JPMorgan results against the lab requirements.