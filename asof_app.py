
import io
from datetime import date
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st

# LAB 17 — POINT-IN-TIME AUDIT
# FIN 439 — AI-Augmented Finance

# R — SERIES
SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}

st.set_page_config(
    page_title="Point-in-Time Rates Audit",
    layout="wide"
)

st.title("Point-in-Time Rates Audit")
st.caption(
    f"Data from FRED and ALFRED, Federal Reserve Bank "
    f"of St. Louis, downloaded {date.today()}; "
    "built with AI help, a learning demonstration, "
    "not investment advice."
)

# I — DOWNLOAD DATA

def read_csv(url, series_id):
    response = requests.get(url, timeout=35)
    response.raise_for_status()

    frame = pd.read_csv(
        io.StringIO(response.text),
        na_values=["."]
    )

    if frame.shape[1] < 2:
        raise ValueError("Invalid CSV format")

    dates = pd.to_datetime(
        frame.iloc[:, 0], errors="coerce"
    )
    values = pd.to_numeric(
        frame.iloc[:, 1], errors="coerce"
    )

    result = pd.Series(
        values.to_numpy(),
        index=dates,
        name=series_id
    ).dropna()

    result = result.loc[result.index.notna()]

    if result.empty:
        raise ValueError("No numeric observations returned")

    return result.sort_index()


@st.cache_data(ttl=3600)
def download_today(series_id):
    url = (
        "https://fred.stlouisfed.org/graph/"
        f"fredgraph.csv?id={quote(series_id)}"
    )
    return read_csv(url, series_id)


@st.cache_data(ttl=3600)
def download_vintage(series_id, vintage):
    url = (
        "https://alfred.stlouisfed.org/graph/"
        f"alfredgraph.csv?id={quote(series_id)}"
        f"&vintage_date={vintage}"
    )
    return read_csv(url, series_id)


# SIDEBAR
with st.sidebar:
    st.header("Series and Dates")

    chosen = st.multiselect(
        "Interest-rate series",
        list(SERIES),
        default=list(SERIES),
        format_func=lambda x: f"{x} — {SERIES[x]}"
    )

    extra = st.text_input(
        "Additional FRED series ID (e.g. PAYEMS)"
    ).strip().upper()

    start = st.date_input(
        "Chart start date",
        value=date(2020, 1, 1)
    )

    vintage = st.date_input(
        "As known on",
        value=date.today(),
        max_value=date.today()
    )

ids = list(dict.fromkeys(
    chosen + ([extra] if extra else [])
))

if not ids:
    st.info("Select at least one series.")
    st.stop()


# V — COMPARE CURRENT AND HISTORICAL DATA
rows = []

for sid in ids:
    st.subheader(
        f"{sid} — {SERIES.get(sid, 'Additional FRED series')}"
    )

    try:
        today = download_today(sid)
        known = download_vintage(
            sid, vintage.isoformat()
        )

        known = known.loc[
            known.index <= pd.Timestamp(vintage)
        ]

        if known.empty:
            raise ValueError(
                "No observations available as of this date"
            )

        # Today's chart
        st.line_chart(
            today.loc[
                today.index >= pd.Timestamp(start)
            ]
        )

        last_known = known.index.max()
        last_today = today.index.max()

        # Compare observations on identical dates
        common = today.index.intersection(known.index)

        revised = int(
            (
                (today.loc[common] - known.loc[common])
                .abs() > 1e-8
            ).sum()
        )

        added = int(
            (today.index > last_known).sum()
        )

        st.write(
            f"Last known on **{vintage}**: "
            f"**{last_known.date()}**, "
            f"value **{known.loc[last_known]:,.3f}**"
        )

        rows.append({
            "ID": sid,
            "FRED source":
                f"https://fred.stlouisfed.org/series/{sid}",
            "Last date known then": last_known.date(),
            "Value known then": float(
                known.loc[last_known]
            ),
            "Latest date today": last_today.date(),
            "Latest value today": float(
                today.loc[last_today]
            ),
            "New observations since": added,
            "Revised overlapping values": revised
        })

    except Exception as exc:
        st.error(
            f"{sid}: Could not load this series: {exc}"
        )


# E — RESULTS TABLE
st.subheader("Point-in-Time Comparison")

if rows:
    table = pd.DataFrame(rows).set_index("ID")

    st.dataframe(
        table,
        column_config={
            "FRED source": st.column_config.LinkColumn(
                "FRED source"
            )
        },
        use_container_width=True
    )

    st.caption(
        "Revision counts compare values on identical "
        "observation dates. New observations are dates "
        "after the last observation known in the vintage."
    )
else:
    st.warning("No valid series loaded.")