"""Lab 09: ABG Five-Year Three-Statement Pro-Forma Model."""

# All financial figures are in USD millions unless stated otherwise.

# --------------------------------------------------
# 1. ABG ASSUMPTIONS
# --------------------------------------------------

# Judgment assumptions
revenue_growth = 0.018
gross_margin = 0.1705
sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]
annual_impairment = 120.0
tax_rate = 0.255
other_wc_rate = 0.008
annual_debt_repayment = 150.0
annual_share_buyback = 150.0

# Historical assumptions
depreciation_rate = 82.4 / 3070.4
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floor_plan_ratio = 2027.0 / 2135.8
floor_plan_interest_rate = 0.0467
term_debt_interest_rate = 0.0544

# Capital spending: guidance
annual_capex = 250.0

# Financing assumptions
minimum_cash = 25.0
revolver_limit = 850.0
revolver_interest_rate = 0.06

# Valuation assumptions
cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 17.951349

# --------------------------------------------------
# 2. FY2025 OPENING FINANCIAL STATEMENTS
# --------------------------------------------------

opening = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

# --------------------------------------------------
# 3. VALIDATION FUNCTION
# --------------------------------------------------

def assert_balanced(year, gap, cash):
    if abs(gap) > 0.01:
        raise ValueError(
            f"FY{year}E balance sheet does not balance. "
            f"Gap: {gap:.1f} million."
        )

    if cash < minimum_cash - 0.01:
        raise ValueError(
            f"FY{year}E cash is below the minimum. "
            f"Cash: {cash:.1f} million."
        )


# --------------------------------------------------
# 4. BUILD THE FIVE-YEAR MODEL
# --------------------------------------------------

def main():

    statements = []
    previous = opening.copy()

    for index, year in enumerate(range(2026, 2031)):

        # INCOME STATEMENT

        revenue = previous["revenue"] * (1 + revenue_growth)

        gross_profit = revenue * gross_margin

        cost_of_sales = revenue - gross_profit

        sga = gross_profit * sga_ratios[index]

        depreciation = previous["ppe"] * depreciation_rate

        impairment = annual_impairment

        operating_income = (
            gross_profit - sga - depreciation - impairment
        )

        interest = (
            previous["floor_plan"] * floor_plan_interest_rate
            + previous["term_debt"] * term_debt_interest_rate
            + previous["revolver"] * revolver_interest_rate
        )

        pretax_income = operating_income - interest

        taxes = max(0, pretax_income) * tax_rate

        net_income = pretax_income - taxes

        # BALANCE SHEET EXCLUDING CASH

        inventory = cost_of_sales * inventory_days / 365

        floor_plan = inventory * floor_plan_ratio

        ppe = previous["ppe"] + annual_capex - depreciation

        change_in_revenue = revenue - previous["revenue"]

        change_in_other_wc = other_wc_rate * change_in_revenue

        other_assets = (
            previous["other_assets"]
            + change_in_other_wc
            - impairment
        )

        term_debt = previous["term_debt"] - annual_debt_repayment

        other_liabilities = previous["other_liabilities"]

        equity = (
            previous["equity"]
            + net_income
            - annual_share_buyback
        )

        # CASH FLOW STATEMENT

        change_in_inventory = inventory - previous["inventory"]

        change_in_floor_plan = floor_plan - previous["floor_plan"]

        fcfe = (
            net_income
            + depreciation
            + impairment
            - annual_capex
            - change_in_inventory
            - change_in_other_wc
            + change_in_floor_plan
            - annual_debt_repayment
        )

        # CASH IS CALCULATED LAST

        cash_before_revolver = (
            previous["cash"]
            + fcfe
            - annual_share_buyback
        )

        revolver = previous["revolver"]

        if cash_before_revolver < minimum_cash:

            required_draw = minimum_cash - cash_before_revolver

            available_credit = revolver_limit - revolver

            revolver_draw = min(
                required_draw, available_credit
            )

            revolver += revolver_draw

            cash = cash_before_revolver + revolver_draw

        else:

            revolver_repayment = min(
                revolver,
                cash_before_revolver - minimum_cash
            )

            revolver -= revolver_repayment

            cash = cash_before_revolver - revolver_repayment

        # BALANCE SHEET CHECK

        total_assets = cash + inventory + ppe + other_assets

        total_liabilities = (
            floor_plan
            + term_debt
            + revolver
            + other_liabilities
        )

        balance_sheet_gap = (
            total_assets - total_liabilities - equity
        )

        # STORE THE YEAR'S RESULTS

        result = {
            "year": year,
            "revenue": revenue,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": impairment,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "taxes": taxes,
            "net_income": net_income,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "total_assets": total_assets,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "total_liabilities": total_liabilities,
            "equity": equity,
            "fcfe": fcfe,
            "balance_sheet_gap": balance_sheet_gap,
        }

        statements.append(result)

        # Use the current year as the next year's opening balance.

        previous = {
            "revenue": revenue,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }

    # --------------------------------------------------
    # 5. PRINT THE THREE FINANCIAL STATEMENTS
    # --------------------------------------------------

    def print_table(title, rows):
        print("\n" + title)
        print("-" * 90)

        print(
            f"{'USD millions':<30}"
            + "".join(
                f"{item['year']:>12}"
                for item in statements
            )
        )

        for label, key in rows:
            print(
                f"{label:<30}"
                + "".join(
                    f"{item[key]:>12,.1f}"
                    for item in statements
                )
            )

    print_table(
        "INCOME STATEMENT",
        [
            ("Revenue", "revenue"),
            ("Cost of sales", "cost_of_sales"),
            ("Gross profit", "gross_profit"),
            ("SG&A", "sga"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Operating income", "operating_income"),
            ("Interest expense", "interest"),
            ("Pretax income", "pretax_income"),
            ("Taxes", "taxes"),
            ("Net income", "net_income"),
        ],
    )

    print_table(
        "BALANCE SHEET",
        [
            ("Cash", "cash"),
            ("Inventory", "inventory"),
            ("PP&E", "ppe"),
            ("Other assets", "other_assets"),
            ("Total assets", "total_assets"),
            ("Floor plan", "floor_plan"),
            ("Term debt", "term_debt"),
            ("Revolver", "revolver"),
            ("Other liabilities", "other_liabilities"),
            ("Total liabilities", "total_liabilities"),
            ("Equity", "equity"),
        ],
    )

    print_table(
        "CASH FLOW STATEMENT",
        [
            ("Free cash flow to equity", "fcfe"),
            ("Ending cash", "cash"),
        ],
    )

    # --------------------------------------------------
    # 6. CHECK THE BALANCE SHEET BEFORE VALUATION
    # --------------------------------------------------

    print("\nBALANCE SHEET CHECKS")
    print("-" * 60)

    for item in statements:

        print(
            f"FY{item['year']}E: "
            f"Balance sheet gap = "
            f"{item['balance_sheet_gap']:.1f}, "
            f"Cash = {item['cash']:.1f}"
        )

        assert_balanced(
            item["year"],
            item["balance_sheet_gap"],
            item["cash"],
        )

    print("\nAll balance sheet checks passed.")

    # --------------------------------------------------
    # 7. EQUITY VALUATION
    # --------------------------------------------------

    if terminal_growth >= cost_of_equity:
        raise ValueError(
            "Terminal growth must be below cost of equity."
        )

    pv_fcfe = sum(
        item["fcfe"] / (1 + cost_of_equity) ** index
        for index, item in enumerate(statements, start=1)
    )

    final_fcfe = statements[-1]["fcfe"]

    terminal_value = (
        (final_fcfe + annual_debt_repayment)
        * (1 + terminal_growth)
        / (cost_of_equity - terminal_growth)
    )

    pv_terminal_value = terminal_value / (1 + cost_of_equity) ** 5

    equity_value = pv_fcfe + pv_terminal_value

    terminal_value_share = pv_terminal_value / equity_value

    value_per_share = equity_value / shares_outstanding

    print("\nABG EQUITY VALUATION")
    print("-" * 60)

    print(f"PV of five-year FCFE: ${pv_fcfe:,.1f} million")

    print(
        f"PV of terminal value: "
        f"${pv_terminal_value:,.1f} million"
    )

    print(f"Equity value: ${equity_value:,.1f} million")

    print(
        f"Share of value after 2030: "
        f"{terminal_value_share:.1%}"
    )

    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()