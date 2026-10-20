
import math

# LAB 14 — PORTFOLIO BASELINES
# FIN 439 — AI-Augmented Finance

# R — INPUTS
assets = [
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund"
]

expected_returns = [0.035, 0.043, 0.050, 0.080]
volatilities = [0.005, 0.070, 0.060, 0.160]

correlations = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00]
]

objective_return = 0.065


# I — VALIDATE CORRELATIONS
def validate_correlations(corr):
    n = len(assets)

    if len(corr) != n or any(len(row) != n for row in corr):
        raise ValueError("Correlation table must be 4 by 4.")

    for i in range(n):
        for j in range(n):
            if not -1 <= corr[i][j] <= 1:
                raise ValueError(
                    "Invalid correlation: must be between -1 and 1."
                )

            if not math.isclose(corr[i][j], corr[j][i]):
                raise ValueError(
                    "Correlation table must be symmetric."
                )

            if i == j and not math.isclose(corr[i][j], 1.0):
                raise ValueError(
                    "Diagonal correlations must equal 1."
                )


# BUILD COVARIANCE MATRIX
def build_covariance_matrix(corr, vols):
    return [
        [
            corr[i][j] * vols[i] * vols[j]
            for j in range(len(vols))
        ]
        for i in range(len(vols))
    ]


# PORTFOLIO WEIGHTS
def benchmark_weights():
    return [0.0, 0.0, 0.40, 0.60]


def equal_weights():
    return [1 / len(assets)] * len(assets)


def inverse_volatility_weights(vols):
    inverse = [1 / v for v in vols]
    total = sum(inverse)
    return [value / total for value in inverse]


# EXPECTED PORTFOLIO RETURN
def portfolio_return(weights, returns):
    return sum(
        weights[i] * returns[i]
        for i in range(len(weights))
    )


# PORTFOLIO VOLATILITY
def portfolio_volatility(weights, covariance):
    variance = 0.0

    for i in range(len(weights)):
        for j in range(len(weights)):
            variance += (
                weights[i]
                * weights[j]
                * covariance[i][j]
            )

    return math.sqrt(max(variance, 0.0))


# RESERVE-ELIGIBLE WEIGHT
def reserve_weight(weights):
    return weights[0] + weights[1]


# CHECK RETURN OBJECTIVE
def meets_objective(port_return):
    return port_return >= objective_return


# DISPLAY RESULTS
def print_portfolio(name, weights, covariance):
    ret = portfolio_return(weights, expected_returns)
    vol = portfolio_volatility(weights, covariance)
    reserve = reserve_weight(weights)

    print(f"\n{name}")
    print("-" * 45)

    for asset, weight in zip(assets, weights):
        print(f"{asset}: {weight * 100:.1f}%")

    print(f"Expected return: {ret * 100:.2f}%")
    print(f"Volatility: {vol * 100:.2f}%")
    print(f"Reserve eligible: {reserve * 100:.1f}%")
    print(
        "Meets 6.5% objective:",
        "Yes" if meets_objective(ret) else "No"
    )


# RUN ALL THREE PORTFOLIOS
def main():
    validate_correlations(correlations)

    covariance = build_covariance_matrix(
        correlations, volatilities
    )

    portfolios = {
        "Benchmark": benchmark_weights(),
        "Equal Weight": equal_weights(),
        "Inverse Volatility": inverse_volatility_weights(
            volatilities
        )
    }

    print("LAB 14 — PORTFOLIO BASELINES")

    for name, weights in portfolios.items():
        print_portfolio(name, weights, covariance)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)