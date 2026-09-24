
"""Lab 10 | Ulta Beauty (ULTA) five-year simplified three-statement pro forma.

USD millions except per-share figures. FY2025 ended January 31, 2026;
FY2026E through FY2030E are FORECASTS, not Ulta guidance.

Primary source: Ulta Beauty fiscal 2025 10-K filed March 26, 2026:
https://www.sec.gov/Archives/edgar/data/1403568/000110465926035243/ulta-20260131x10k.htm

IMPORTANT: A teaching model using simplified, explicitly labeled assumptions.
See companion lab10_assumptions.md for judgment reasons and limitations.
"""

COMPANY = "ULTA BEAUTY (ULTA)"
YEARS = range(2026, 2031)

# Historical FY2025 amounts in millions, 10-K pp. 53-56.
HISTORY = {
    "revenue": 12392.820,
    "cost_of_sales": 7547.596,
    "gross_profit": 4845.224,
    "sga": 3296.411,
    "preopening": 15.821,
    "depreciation_amortization": 300.772,
    "pretax_income_before_affiliate": 1531.205,
    "income_taxes": 373.869,
    "capex": 434.829,
    "net_income": 1153.479,
}

# --------------------------------------------------
# 1. ULTA ASSUMPTIONS
# --------------------------------------------------

# Judgment assumptions, NOT published company forecasts.
revenue_growth = 0.05

# Historical ratios held flat as a judgment.
gross_margin = HISTORY["gross_profit"] / HISTORY["revenue"]
sga_ratio = HISTORY["sga"] / HISTORY["gross_profit"]
preopening_ratio = HISTORY["preopening"] / HISTORY["revenue"]

inventory_days = (
    2181.127 / HISTORY["cost_of_sales"] * 365
)

depreciation_rate = (
    HISTORY["depreciation_amortization"] / 1434.062
)

# D&A includes amortization, not just PP&E depreciation.
# The PP&E roll-forward is therefore approximate.

tax_rate = (
    HISTORY["income_taxes"]
    / HISTORY["pretax_income_before_affiliate"]
)

annual_capex = 435.0
annual_share_buyback = 0.0
annual_debt_repayment = 0.0

# Financing assumptions
minimum_cash = 100.0
revolver_limit = 1000.0
revolver_interest_rate = 0.06
existing_debt_interest_rate = 0.055

# Valuation assumptions
cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 44.991

# --------------------------------------------------
# 2. FY2025 OPENING FINANCIAL STATEMENTS
# --------------------------------------------------

opening = {
    "revenue": HISTORY["revenue"],
    "cash": 424.243,
    "inventory": 2181.127,
    "ppe": 1434.062,
    "lease_assets": 1813.074,

    # Other assets are derived from reported total assets.
    "other_assets": (
        6999.294
        - 424.243
        - 2181.127
        - 1434.062
        - 1813.074
    ),

    "existing_debt": 62.287,
    "revolver": 0.0,

    "lease_liabilities": (
        306.671 + 1813.103
    ),

    # Other liabilities are derived from reported total liabilities.
    "other_liabilities": (
        4195.843
        - 62.287
        - 306.671
        - 1813.103
    ),

    "equity": 2803.451,
}


# --------------------------------------------------
# 3. VALIDATION FUNCTIONS
# --------------------------------------------------

def asset_total(s):
    return (
        s["cash"]
        + s["inventory"]
        + s["ppe"]
        + s["lease_assets"]
        + s["other_assets"]
    )


def liability_total(s):
    return (
        s["existing_debt"]
        + s["revolver"]
        + s["lease_liabilities"]
        + s["other_liabilities"]
    )


def assert_balanced(year, s):
    gap = (
        asset_total(s)
        - liability_total(s)
        - s["equity"]
    )

    if abs(gap) > 0.01:
        raise ValueError(
            f"FY{year}E balance sheet does not balance: "
            f"gap ${gap:,.3f}m"
        )

    if s["cash"] < minimum_cash - 0.01:
        raise ValueError(
            f"FY{year}E cash ${s['cash']:,.3f}m "
            f"is below ${minimum_cash:,.1f}m floor"
        )

    return gap


# --------------------------------------------------
# 4. PRINT FINANCIAL STATEMENTS
# --------------------------------------------------

def print_table(title, statements, rows):
    print("\n" + title)
    print("-" * 91)

    print(
        f"{'USD millions':<30}"
        + "".join(
            f"{s['year']:>12}"
            for s in statements
        )
    )

    for label, key in rows:
        print(
            f"{label:<30}"
            + "".join(
                f"{s[key]:>12,.1f}"
                for s in statements
            )
        )


# --------------------------------------------------
# 5. BUILD THE FIVE-YEAR MODEL
# --------------------------------------------------

def main():

    opening_gap = (
        asset_total(opening)
        - liability_total(opening)
        - opening["equity"]
    )

    if abs(opening_gap) > 0.01:
        raise ValueError(
            f"FY2025 opening balance sheet gap "
            f"${opening_gap:,.3f}m"
        )

    if not 0 <= terminal_growth < cost_of_equity:
        raise ValueError(
            "Terminal growth must be >=0 "
            "and below cost of equity"
        )

    if shares_outstanding <= 0 or annual_capex < 0:
        raise ValueError(
            "Check share count and capex inputs"
        )

    previous = opening.copy()
    statements = []

    for year in YEARS:

        # ------------------------------------------
        # INCOME STATEMENT
        # ------------------------------------------

        revenue = (
            previous["revenue"]
            * (1 + revenue_growth)
        )

        gross_profit = revenue * gross_margin

        cost_of_sales = revenue - gross_profit

        sga = gross_profit * sga_ratio

        preopening = revenue * preopening_ratio

        # Ulta reports SG&A inclusive of D&A.
        # Do not deduct D&A again.
        operating_income = (
            gross_profit
            - sga
            - preopening
        )

        interest = (
            previous["existing_debt"]
            * existing_debt_interest_rate
            + previous["revolver"]
            * revolver_interest_rate
        )

        pretax = operating_income - interest

        taxes = max(0.0, pretax) * tax_rate

        net_income = pretax - taxes

        # ------------------------------------------
        # BALANCE SHEET EXCLUDING CASH
        # ------------------------------------------

        inventory = (
            cost_of_sales
            * inventory_days
            / 365
        )

        depreciation = (
            previous["ppe"]
            * depreciation_rate
        )

        ppe = (
            previous["ppe"]
            + annual_capex
            - depreciation
        )

        # Simplified forecast:
        # Lease assets, lease liabilities, and
        # other balance sheet items remain constant.

        lease_assets = previous["lease_assets"]
        other_assets = previous["other_assets"]

        lease_liabilities = (
            previous["lease_liabilities"]
        )

        other_liabilities = (
            previous["other_liabilities"]
        )

        existing_debt = max(
            0.0,
            previous["existing_debt"]
            - annual_debt_repayment
        )

        debt_repayment = (
            previous["existing_debt"]
            - existing_debt
        )

        equity = (
            previous["equity"]
            + net_income
            - annual_share_buyback
        )

        # ------------------------------------------
        # CASH FLOW STATEMENT
        # ------------------------------------------

        change_inventory = (
            inventory
            - previous["inventory"]
        )

        fcfe = (
            net_income
            + depreciation
            - annual_capex
            - change_inventory
            - debt_repayment
        )

        # ------------------------------------------
        # CASH AND REVOLVER
        # ------------------------------------------

        cash_before_revolver = (
            previous["cash"]
            + fcfe
            - annual_share_buyback
        )

        revolver = previous["revolver"]

        draw = 0.0
        repayment = 0.0

        if cash_before_revolver < minimum_cash:

            draw = min(
                minimum_cash - cash_before_revolver,
                revolver_limit - revolver
            )

            revolver += draw

            cash = cash_before_revolver + draw

        else:

            repayment = min(
                revolver,
                cash_before_revolver - minimum_cash
            )

            revolver -= repayment

            cash = cash_before_revolver - repayment

        # ------------------------------------------
        # STORE THE YEAR'S RESULTS
        # ------------------------------------------

        s = dict(
            year=year,
            revenue=revenue,
            cost_of_sales=cost_of_sales,
            gross_profit=gross_profit,
            sga=sga,
            preopening=preopening,
            operating_income=operating_income,
            interest=interest,
            pretax=pretax,
            taxes=taxes,
            net_income=net_income,
            depreciation=depreciation,
            inventory=inventory,
            ppe=ppe,
            lease_assets=lease_assets,
            other_assets=other_assets,
            cash=cash,
            existing_debt=existing_debt,
            revolver=revolver,
            lease_liabilities=lease_liabilities,
            other_liabilities=other_liabilities,
            equity=equity,
            fcfe=fcfe,
            revolver_draw=draw,
            revolver_repayment=repayment
        )

        s["total_assets"] = asset_total(s)

        s["total_liabilities"] = liability_total(s)

        # Refuse to continue if the model does not balance.
        s["balance_sheet_gap"] = assert_balanced(
            year, s
        )

        statements.append(s)

        previous = s

    # --------------------------------------------------
    # 6. PRINT FINANCIAL STATEMENTS
    # --------------------------------------------------

    print(
        COMPANY
        + " | FY2026E-FY2030E "
        + "| illustrative student assumptions"
    )

    print_table(
        "INCOME STATEMENT",
        statements,
        [
            ("Revenue", "revenue"),
            ("Cost of sales", "cost_of_sales"),
            ("Gross profit", "gross_profit"),
            ("SG&A (incl. D&A)", "sga"),
            ("Pre-opening", "preopening"),
            ("Operating income", "operating_income"),
            ("Interest expense", "interest"),
            ("Pretax income", "pretax"),
            ("Taxes", "taxes"),
            ("Net income", "net_income")
        ]
    )

    print_table(
        "BALANCE SHEET",
        statements,
        [
            ("Cash", "cash"),
            ("Inventory", "inventory"),
            ("PP&E", "ppe"),
            ("Operating lease assets", "lease_assets"),
            ("Other assets", "other_assets"),
            ("Total assets", "total_assets"),
            ("Existing debt", "existing_debt"),
            ("Revolver", "revolver"),
            (
                "Operating lease liabilities",
                "lease_liabilities"
            ),
            ("Other liabilities", "other_liabilities"),
            ("Total liabilities", "total_liabilities"),
            ("Equity", "equity")
        ]
    )

    print_table(
        "CASH FLOW SUMMARY (simplified)",
        statements,
        [
            ("Net income", "net_income"),
            ("D&A proxy", "depreciation"),
            ("FCFE before new revolver", "fcfe"),
            ("Revolver draw", "revolver_draw"),
            ("Revolver repayment", "revolver_repayment"),
            ("Ending cash", "cash")
        ]
    )

    # --------------------------------------------------
    # 7. BALANCE SHEET CHECKS
    # --------------------------------------------------

    print("\nBALANCE SHEET CHECKS")

    for s in statements:

        print(
            f"FY{s['year']}E: "
            f"gap = {s['balance_sheet_gap']:.3f}m, "
            f"cash = ${s['cash']:,.1f}m, "
            f"revolver = ${s['revolver']:,.1f}m"
        )

    print(
        "All five annual checks passed. "
        "Opening balance sheet also reconciled."
    )

    # --------------------------------------------------
    # 8. EQUITY VALUATION
    # --------------------------------------------------

    pv_fcfe = sum(
        s["fcfe"] / (1 + cost_of_equity) ** i
        for i, s in enumerate(statements, 1)
    )

    final_fcfe = statements[-1]["fcfe"]

    if final_fcfe <= 0:

        print(
            "\nTerminal FCFE is nonpositive; "
            "no perpetuity terminal value is computed."
        )

        print(
            "A perpetual negative distributable "
            "cash flow does not provide a defensible "
            "positive terminal equity value."
        )

        terminal_value = 0.0

    else:

        terminal_value = (
            final_fcfe
            * (1 + terminal_growth)
            / (cost_of_equity - terminal_growth)
        )

    pv_terminal = (
        terminal_value
        / (1 + cost_of_equity) ** len(statements)
    )

    equity_value = pv_fcfe + pv_terminal

    print(
        "\nULTA EQUITY VALUATION (ILLUSTRATIVE)"
    )

    print(
        f"PV of five-year FCFE: "
        f"${pv_fcfe:,.1f}m"
    )

    print(
        f"PV of terminal value: "
        f"${pv_terminal:,.1f}m"
    )

    print(
        f"Equity value: "
        f"${equity_value:,.1f}m"
    )

    print(
        f"Value per share "
        f"(fixed {shares_outstanding:.3f}m diluted shares): "
        f"${equity_value / shares_outstanding:,.2f}"
    )

    print(
        "NOTE: Model value is a judgment-based scenario, "
        "NOT a market-price forecast."
    )

    return statements


if __name__ == "__main__":
    main()