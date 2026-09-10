# Ulta Beauty DCF — Lab 06

# -----------------------------
# Inputs
# -----------------------------

starting_fcff = 1075.254   # USD millions
growth_rates = [0.07, 0.06, 0.05, 0.04, 0.03]

wacc = 0.091
terminal_growth = 0.03

cash = 424.243
debt = 62.287
diluted_shares = 44.991

# Sensitivity assumptions
wacc_values = [0.081, 0.091, 0.101]
terminal_growth_values = [0.02, 0.03, 0.04]

# Reverse DCF target
target_share_price = 542.05

# Search bounds for uniform growth-rate shift
lower_bound = -0.05
upper_bound = 0.10


# -----------------------------
# DCF Function
# -----------------------------

def calculate_dcf(
    starting_fcff,
    growth_rates,
    wacc,
    terminal_growth,
    cash,
    debt,
    diluted_shares
):
    # Prevent invalid terminal value
    if terminal_growth >= wacc:
        return None

    # Project FCFF for Years 1-5
    fcff_values = []
    current_fcff = starting_fcff

    for growth_rate in growth_rates:
        current_fcff *= (1 + growth_rate)
        fcff_values.append(current_fcff)

    # Present value of explicit FCFF
    pv_fcff = 0

    for year, fcff in enumerate(fcff_values, start=1):
        pv_fcff += fcff / ((1 + wacc) ** year)

    # Terminal value
    terminal_value = (
        fcff_values[-1] * (1 + terminal_growth)
    ) / (wacc - terminal_growth)

    # Present value of terminal value
    pv_terminal = terminal_value / ((1 + wacc) ** 5)

    # Enterprise value
    enterprise_value = pv_fcff + pv_terminal

    # Equity value
    equity_value = enterprise_value + cash - debt

    # Value per diluted share
    value_per_share = equity_value / diluted_shares

    # Terminal value percentage
    terminal_value_pct = pv_terminal / enterprise_value

    return (
        fcff_values,
        pv_fcff,
        terminal_value,
        pv_terminal,
        enterprise_value,
        equity_value,
        value_per_share,
        terminal_value_pct
    )


# -----------------------------
# Base Case
# -----------------------------

base_result = calculate_dcf(
    starting_fcff,
    growth_rates,
    wacc,
    terminal_growth,
    cash,
    debt,
    diluted_shares
)

(
    fcff_values,
    pv_fcff,
    terminal_value,
    pv_terminal,
    enterprise_value,
    equity_value,
    implied_share_price,
    terminal_value_pct
) = base_result

for year, fcff in enumerate(fcff_values, start=1):
    print(f"FCFF Year {year}: {fcff:.4f}")

print(f"PV of Five Explicit FCFF: {pv_fcff:.4f}")
print(f"Terminal Value at Year 5: {terminal_value:.4f}")
print(f"PV of Terminal Value: {pv_terminal:.4f}")
print(f"Enterprise Value: {enterprise_value:.4f}")
print(f"Equity Value: {equity_value:.4f}")
print(f"Value per Diluted Share: {implied_share_price:.4f}")
print(
    f"PV of Terminal Value / Enterprise Value: "
    f"{terminal_value_pct:.4f}"
)


# -----------------------------
# Sensitivity Grid
# -----------------------------

print("\nSensitivity Grid — Value per Diluted Share")
print("WACC \\ Terminal Growth       2%        3%        4%")

for test_wacc in wacc_values:

    row = f"{test_wacc:.1%}".ljust(26)

    for test_terminal_growth in terminal_growth_values:

        if test_terminal_growth >= test_wacc:
            row += "INVALID".rjust(10)

        else:
            result = calculate_dcf(
                starting_fcff,
                growth_rates,
                test_wacc,
                test_terminal_growth,
                cash,
                debt,
                diluted_shares
            )

            test_share_price = result[6]

            row += f"${test_share_price:.2f}".rjust(10)

    print(row)


# -----------------------------
# Reverse DCF
# -----------------------------

def price_with_growth_shift(shift):

    shifted_growth_rates = [
        growth_rate + shift
        for growth_rate in growth_rates
    ]

    # Refuse any growth rate of -100% or below
    if any(rate <= -1.0 for rate in shifted_growth_rates):
        return None

    result = calculate_dcf(
        starting_fcff,
        shifted_growth_rates,
        wacc,
        terminal_growth,
        cash,
        debt,
        diluted_shares
    )

    if result is None:
        return None

    return result[6]


lower_price = price_with_growth_shift(lower_bound)
upper_price = price_with_growth_shift(upper_bound)

print("\nReverse DCF")

if (
    lower_price is None
    or upper_price is None
    or not (
        min(lower_price, upper_price)
        <= target_share_price
        <= max(lower_price, upper_price)
    )
):
    print("No solution in the selected bracket.")

else:

    low = lower_bound
    high = upper_bound

    for _ in range(100):

        midpoint = (low + high) / 2
        midpoint_price = price_with_growth_shift(midpoint)

        if midpoint_price < target_share_price:
            low = midpoint
        else:
            high = midpoint

    solved_shift = (low + high) / 2

    solved_growth_rates = [
        growth_rate + solved_shift
        for growth_rate in growth_rates
    ]

    solved_price = price_with_growth_shift(solved_shift)

    print(f"Target Share Price: ${target_share_price:.2f}")

    print(
        f"Solved Uniform Growth Shift: "
        f"{solved_shift * 100:.2f} percentage points"
    )

    print(
        "Growth Rates After Shift: "
        + ", ".join(
            f"{rate:.2%}"
            for rate in solved_growth_rates
        )
    )

    print(f"Model Share Price After Shift: ${solved_price:.2f}")

    print(
        "Held Fixed: Starting FCFF, WACC, terminal growth, "
        "cash, debt, and diluted shares"
    )