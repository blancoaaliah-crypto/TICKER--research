
# FIN 439 — Lab 15: Portfolio Stability Decision
# Streamlit Portfolio Optimization App

import streamlit as st

from portfolio import (
    assets,
    expected_returns,
    volatilities,
    correlations,
    search_lowest_risk,
    estimate_from_csv,
)

st.set_page_config(
    page_title="Portfolio Stability Decision",
    layout="wide"
)

st.title("Lab 15 — Portfolio Stability Decision")

st.caption(
    "Built with AI help, a learning demonstration, "
    "not investment advice."
)

# SIDEBAR SETTINGS
st.sidebar.header("Portfolio Settings")

objective = st.sidebar.number_input(
    "Expected Return Objective (%)",
    min_value=0.0,
    value=6.5,
    step=0.1
) / 100

reserve_min = st.sidebar.number_input(
    "Minimum Reserve Eligible (%)",
    min_value=0.0,
    max_value=100.0,
    value=3.0,
    step=1.0
) / 100

uploaded_file = st.sidebar.file_uploader(
    "Upload prices.csv",
    type=["csv"]
)

last_36 = st.sidebar.checkbox(
    "Use Last 36 Months",
    value=False
)

# LOAD PORTFOLIO DATA
if uploaded_file is not None:
    try:
        uploaded_file.seek(0)

        base_returns, base_vols, base_corr, names = (
            estimate_from_csv(uploaded_file, last36=False)
        )

        if last_36:
            uploaded_file.seek(0)

            returns, vols, corr, names = (
                estimate_from_csv(uploaded_file, last36=True)
            )
        else:
            returns = base_returns.copy()
            vols = base_vols.copy()
            corr = base_corr

        st.success("Historical price data loaded successfully.")

    except ValueError as error:
        st.error(f"CSV Error: {error}")
        st.stop()

else:
    names = assets.copy()

    base_returns = expected_returns.copy()
    base_vols = volatilities.copy()
    base_corr = correlations

    returns = base_returns.copy()
    vols = base_vols.copy()
    corr = base_corr

    st.info("Using Meridian Foundation training data.")

# EDIT EXPECTED RETURNS
st.subheader("Expected Return Estimates")

st.write(
    "Adjust expected returns to test how the "
    "recommended portfolio changes."
)

edited_returns = []

for i, name in enumerate(names):
    value = st.number_input(
        f"{name} Expected Return Estimate (%)",
        value=float(returns[i] * 100),
        step=0.1,
        format="%.2f",
        key=f"return_{name}"
    )

    edited_returns.append(value / 100)

# RESERVE ELIGIBILITY
st.subheader("Reserve Eligible Assets")

st.write("Select which investments count toward the reserve.")

eligible = []

for i, name in enumerate(names):
    default = (
        uploaded_file is None
        and i in (0, 1)
    )

    checked = st.checkbox(
        name,
        value=default,
        key=f"reserve_{name}"
    )

    eligible.append(checked)

# RUN OPTIMIZATION FROM PORTFOLIO.PY
baseline = search_lowest_risk(
    base_returns,
    base_vols,
    base_corr,
    objective,
    reserve_min,
    eligible
)

current = search_lowest_risk(
    edited_returns,
    vols,
    corr,
    objective,
    reserve_min,
    eligible
)

# DISPLAY RESULTS
def display_portfolio(result):
    if result is None:
        st.warning("No mix meets the objective.")
        return

    weights, ret, vol, reserve = result

    st.write("**Portfolio Weights**")

    for name, weight in zip(names, weights):
        st.write(f"{name}: {weight * 100:.2f}%")

    st.metric("Expected Return", f"{ret * 100:.2f}%")
    st.metric("Volatility", f"{vol * 100:.2f}%")
    st.metric("Reserve Eligible", f"{reserve * 100:.2f}%")


st.divider()

st.subheader("Lowest-Risk Portfolio")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### As Loaded")
    display_portfolio(baseline)

with col2:
    st.markdown("### Current Settings")
    display_portfolio(current)

# STABILITY TEST
st.divider()

st.subheader("Portfolio Stability")

if baseline is not None and current is not None:
    original_weights = baseline[0]
    changed_weights = current[0]

    changes = [
        abs(new - old) * 100
        for old, new in zip(
            original_weights,
            changed_weights
        )
    ]

    largest_change = max(changes)

    st.metric(
        "Largest Weight Change",
        f"{largest_change:.2f} percentage points"
    )

    if largest_change >= 20:
        st.warning(
            "The portfolio is sensitive to changes "
            "in expected return estimates."
        )
    else:
        st.success(
            "The portfolio has a smaller allocation "
            "change under these settings."
        )

else:
    st.warning(
        "Stability cannot be compared because "
        "at least one portfolio is infeasible."
    )

st.divider()

st.write(
    "The optimizer searches long-only portfolios "
    "in 5-percentage-point increments and selects "
    "the lowest-volatility mix meeting the "
    "return objective and reserve requirement."
)