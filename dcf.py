"""Five-year FCFF discounted cash flow model (USD millions)."""

# Editable inputs
starting_fcff = 100.0  # USD millions
growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 50.0  # USD millions
debt = 300.0  # USD millions
diluted_shares = 50.0  # millions


def main():
    if terminal_growth >= wacc:
        print("Error: terminal growth must be less than WACC.")
        return

    fcffs = []
    current_fcff = starting_fcff
    for growth_rate in growth_rates:
        current_fcff *= 1 + growth_rate
        fcffs.append(current_fcff)

    discount_factors = [(1 + wacc) ** year for year in range(1, 6)]
    pv_explicit_fcff = sum(fcff / factor for fcff, factor in zip(fcffs, discount_factors))

    terminal_value_year_5 = fcffs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value_year_5 / discount_factors[-1]
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt
    value_per_diluted_share = equity_value / diluted_shares
    pv_terminal_value_share_of_ev = pv_terminal_value / enterprise_value

    for year, fcff in enumerate(fcffs, start=1):
        print(f"FCFF Year {year}: {fcff:.4f}")
    print(f"PV of Five Explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of Terminal Value: {pv_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(f"PV of Terminal Value / Enterprise Value: {pv_terminal_value_share_of_ev:.4f}")


if __name__ == "__main__":
    main()
