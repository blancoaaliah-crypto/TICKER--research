# FIN 439 - Lab 13: Portfolio Mandate Defense
# Meridian Foundation Reserve

# -------- EDITABLE INPUTS --------

reserve_size = 100.0  # USD millions
quarterly_distribution = 0.75
quarters_to_cover = 4
liquidity_window = 5  # business days
minimum_liquid_share = 90.0  # percent
issuer_limit = 8.0  # percent

# Holding: (issuer, business days to redeem, reserve eligible)
holdings = {
    "Cash": ("none", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

# Portfolio weights in percent
candidates = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    # Candidate D: passes mechanical checks but raises
    # suitability concerns about the return objective.
    "D": {
        "Cash": 0,
        "Treasury bills": 100,
        "Treasury 10-year note": 0,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

# -------- PORTFOLIO CHECKER --------

reserve_minimum = (
    quarters_to_cover * quarterly_distribution / reserve_size
) * 100

print(f"Reserve minimum: {reserve_minimum:.1f}%")

exempt_issuers = {"none", "U.S. Treasury", "diversified fund"}


def check_portfolio(name, weights):
    print(f"\nCandidate {name}")
    failed_rules = 0

    # Check 1: Weights sum to 100%
    total_weight = sum(weights.values())
    passes = abs(total_weight - 100.0) < 1e-9

    print(f"Weights sum to 100: {total_weight:.1f} "
          f"{'pass' if passes else 'FAIL'}")

    if not passes:
        failed_rules += 1

    # Check 2: Long-only, no negative weights
    lowest_weight = min(weights.values())
    passes = lowest_weight >= 0

    print(f"Long-only (lowest weight): {lowest_weight:.1f} "
          f"{'pass' if passes else 'FAIL'}")

    if not passes:
        failed_rules += 1

    # Check 3: Required payout reserve
    reserve_weight = sum(
        weight for holding, weight in weights.items()
        if holdings[holding][2]
    )
    passes = reserve_weight >= reserve_minimum

    print(f"Reserve eligible: {reserve_weight:.1f} "
          f"{'pass' if passes else 'FAIL'}")

    if not passes:
        failed_rules += 1

    # Check 4: Liquidity within five business days
    liquid_weight = sum(
        weight for holding, weight in weights.items()
        if holdings[holding][1] <= liquidity_window
    )
    passes = liquid_weight >= minimum_liquid_share

    print(f"Redeemable within {liquidity_window} days: "
          f"{liquid_weight:.1f} "
          f"{'pass' if passes else 'FAIL'}")

    if not passes:
        failed_rules += 1

    # Check 5: Single-company issuer concentration
    company_weights = {}

    for holding, weight in weights.items():
        issuer = holdings[holding][0]

        if issuer not in exempt_issuers:
            company_weights[issuer] = (
                company_weights.get(issuer, 0) + weight
            )

    largest_company = max(company_weights.values(), default=0)
    passes = largest_company <= issuer_limit

    print(f"Largest single company: {largest_company:.1f} "
          f"{'pass' if passes else 'FAIL'}")

    if not passes:
        failed_rules += 1

    # Check 6: Unverifiable loss rule
    print("Calendar-year loss: requires CIO clarification")

    # Final verdict
    if failed_rules == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failed_rules} rule(s)")


# -------- RUN ALL CANDIDATES --------

for name, weights in candidates.items():
    check_portfolio(name, weights)