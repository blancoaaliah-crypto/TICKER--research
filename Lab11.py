# Lab 11 - Ulta Beauty Sensitivity Analysis
# All financial amounts are in USD millions.
# These are student assumptions, not Ulta forecasts.

# FY2025 historical information from Lab 10
revenue_2025 = 12392.820
gross_profit_2025 = 4845.224
sga_2025 = 3296.411
cost_of_sales_2025 = 7547.596

# Original Lab 10 assumptions
base_growth = 0.05
base_sga = sga_2025 / gross_profit_2025

gross_margin = gross_profit_2025 / revenue_2025
preopening_ratio = 15.821 / revenue_2025
inventory_days = 2181.127 / cost_of_sales_2025 * 365
depreciation_rate = 300.772 / 1434.062
tax_rate = 373.869 / 1531.205

annual_capex = 435.0
cost_of_equity = 0.10
terminal_growth = 0.025
shares = 44.991

# Starting balance sheet from Lab 10
starting_cash = 424.243
starting_inventory = 2181.127
starting_ppe = 1434.062
starting_debt = 62.287
starting_equity = 2803.451

lease_assets = 1813.074
other_assets = 6999.294 - starting_cash - starting_inventory - starting_ppe - lease_assets

lease_liabilities = 306.671 + 1813.103
other_liabilities = 4195.843 - starting_debt - lease_liabilities


# Run the five-year forecast
def run_model(growth, sga_ratio):

    revenue = revenue_2025
    inventory = starting_inventory
    ppe = starting_ppe
    cash = starting_cash
    debt = starting_debt
    equity = starting_equity
    revolver = 0.0

    cash_flows = []
    statements = []

    for year in range(2026, 2031):

        # Income statement
        revenue = revenue * (1 + growth)
        gross_profit = revenue * gross_margin
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * sga_ratio
        preopening = revenue * preopening_ratio

        operating_income = gross_profit - sga - preopening

        interest = debt * 0.055 + revolver * 0.06
        pretax_income = operating_income - interest
        taxes = max(0, pretax_income) * tax_rate
        net_income = pretax_income - taxes

        # Balance sheet
        new_inventory = cost_of_sales * inventory_days / 365
        change_inventory = new_inventory - inventory
        inventory = new_inventory

        depreciation = ppe * depreciation_rate
        ppe = ppe + annual_capex - depreciation

        equity = equity + net_income

        # Free cash flow to equity
        fcfe = (
            net_income
            + depreciation
            - annual_capex
            - change_inventory
        )

        cash = cash + fcfe

        # Revolver financing, if needed
        if cash < 100:
            draw = 100 - cash
            revolver = revolver + draw
            cash = 100

        elif revolver > 0:
            repayment = min(revolver, cash - 100)
            revolver = revolver - repayment
            cash = cash - repayment

        if revolver > 1000:
            raise ValueError("Revolver limit exceeded")

        # Check the balance sheet
        assets = cash + inventory + ppe + lease_assets + other_assets

        liabilities = (
            debt + revolver + lease_liabilities + other_liabilities
        )

        difference = assets - liabilities - equity

        if abs(difference) > 0.01:
            raise ValueError("Balance sheet does not balance")

        cash_flows.append(fcfe)
        statements.append([year, revenue, gross_profit, sga,
                           operating_income, fcfe, difference])

    # Equity valuation using FCFE
    value_per_share = None

    if fcfe > 0:
        pv_cash_flows = 0

        for year_number in range(5):
            pv_cash_flows += (
                cash_flows[year_number]
                / (1 + cost_of_equity) ** (year_number + 1)
            )

        terminal_value = (
            fcfe * (1 + terminal_growth)
            / (cost_of_equity - terminal_growth)
        )

        pv_terminal = terminal_value / (1 + cost_of_equity) ** 5

        equity_value = pv_cash_flows + pv_terminal
        value_per_share = equity_value / shares

    return operating_income, fcfe, value_per_share, statements


# Original base case
base = run_model(base_growth, base_sga)

print("ULTA BEAUTY - LAB 11 SENSITIVITY ANALYSIS")
print("----------------------------------------")

print("\nOriginal Base Case")
print("2030 Operating Income:", round(base[0], 2))
print("2030 FCFE:", round(base[1], 2))
print("Value Per Share:", round(base[2], 2))


# Test revenue growth
print("\nREVENUE GROWTH SENSITIVITY")

growth_results = []

for growth in [0.04, 0.05, 0.06]:

    result = run_model(growth, base_sga)
    growth_results.append(result)

    print("\nRevenue Growth:", round(growth * 100, 2), "%")
    print("Operating Income:", round(result[0], 2))
    print("FCFE:", round(result[1], 2))
    print("Value Per Share:", round(result[2], 2))
    print("Change in Operating Income:", round(result[0] - base[0], 2))
    print("Change in FCFE:", round(result[1] - base[1], 2))
    print("Change in Value Per Share:", round(result[2] - base[2], 2))


# Test SG&A as a percentage of gross profit
print("\nSG&A SENSITIVITY")

sga_results = []

for sga_ratio in [base_sga - 0.01, base_sga, base_sga + 0.01]:

    result = run_model(base_growth, sga_ratio)
    sga_results.append(result)

    print("\nSG&A Ratio:", round(sga_ratio * 100, 3), "%")
    print("Operating Income:", round(result[0], 2))
    print("FCFE:", round(result[1], 2))
    print("Value Per Share:", round(result[2], 2))
    print("Change in Operating Income:", round(result[0] - base[0], 2))
    print("Change in FCFE:", round(result[1] - base[1], 2))
    print("Change in Value Per Share:", round(result[2] - base[2], 2))


# Compare output spans
print("\nOUTPUT SPANS")

for name, results in [
    ("Revenue Growth", growth_results),
    ("SG&A Ratio", sga_results)
]:

    for index, output in [
        (0, "Operating Income"),
        (1, "FCFE"),
        (2, "Value Per Share")
    ]:

        values = [result[index] for result in results
                  if result[index] is not None]

        if values:
            span = max(values) - min(values)
            print(name, output, "Span:", round(span, 2))


# Restore the original base case
restored = run_model(base_growth, base_sga)

print("\nRESTORED BASE CHECK")

if restored == base:
    print("PASS - Original base case matches")
else:
    print("FAIL - Base case changed")

print("\nAll valid scenario balance sheet checks passed.")
print("FCFE means Free Cash Flow to Equity.")