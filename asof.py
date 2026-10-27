
from datetime import date

# FIN 439 — LAB 16: PROVENANCE GATE

# EDITABLE INPUTS
DECISION_DATE = "2026-03-31"

# Row, Ticker, Month measured, Published on, Index
DATA = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def filter_rows(rows, decision_date=None, show_funnel=False):
    remaining = list(rows)

    # RULE 1: Quarantine missing tickers
    quarantined = [r for r in remaining if not r[1].strip()]
    remaining = [r for r in remaining if r[1].strip()]

    # RULE 2: Remove exact duplicates
    seen = set()
    deduplicated = []
    duplicates = []

    for row in remaining:
        fingerprint = row[1:]

        if fingerprint in seen:
            duplicates.append(row)
        else:
            seen.add(fingerprint)
            deduplicated.append(row)

    remaining = deduplicated

    # RULE 3: Remove late publications
    late = []

    if decision_date is not None:
        cutoff = date.fromisoformat(decision_date)

        late = [
            r for r in remaining
            if date.fromisoformat(r[3]) > cutoff
        ]

        remaining = [
            r for r in remaining
            if date.fromisoformat(r[3]) <= cutoff
        ]

    # RULE 4: Keep latest publication for each ticker/month
    latest = {}

    for row in remaining:
        key = (row[1], row[2])

        if key not in latest or (
            row[3], row[0]
        ) > (
            latest[key][3], latest[key][0]
        ):
            latest[key] = row

    chosen_ids = {r[0] for r in latest.values()}

    replaced = [
        r for r in remaining
        if r[0] not in chosen_ids
    ]

    panel = sorted(latest.values(), key=lambda r: r[0])

    if show_funnel:
        steps = [
            ("Rule 1 - No ticker", quarantined),
            ("Rule 2 - Exact duplicate", duplicates),
            ("Rule 3 - Published too late", late),
            ("Rule 4 - Older revision", replaced),
        ]

        for label, removed in steps:
            numbers = [r[0] for r in removed]
            print(
                f"{label}: removed {len(removed)} "
                f"row(s): {numbers}"
            )

        print("As-of panel rows:", [r[0] for r in panel])

    return panel


def signals(panel):
    by_ticker = {}

    for row in panel:
        by_ticker.setdefault(row[1], []).append(row)

    result = {}

    for ticker, rows in sorted(by_ticker.items()):
        rows.sort(key=lambda r: r[2])

        if len(rows) < 2:
            result[ticker] = None
            continue

        previous, current = rows[-2], rows[-1]

        change = (current[4] / previous[4] - 1) * 100

        result[ticker] = (current[2], change)

    return result


def main():
    print("Decision date:", DECISION_DATE)

    print("\nROW FUNNEL")
    asof_panel = filter_rows(
        DATA, DECISION_DATE, show_funnel=True
    )

    print("\nAS-OF PANEL")
    print("Row | Ticker | Month | Published | Index")

    for number, ticker, month, published, index in asof_panel:
        print(
            f"{number:>3} | {ticker:>6} | {month} | "
            f"{published} | {index:.1f}"
        )

    # Naive uses all publication dates
    naive_panel = filter_rows(DATA)

    asof = signals(asof_panel)
    naive = signals(naive_panel)

    print("\nSIGNALS")

    for ticker in sorted(set(asof) | set(naive)):

        def display(signal):
            if signal is None:
                return "N/A (fewer than two months)"

            month, pct = signal
            month_name = date.fromisoformat(
                month + "-01"
            ).strftime("%B")

            return f"{pct:+.2f}% ({month_name})"

        print(
            f"{ticker}: as-of {display(asof.get(ticker))} "
            f"| naive {display(naive.get(ticker))}"
        )


if __name__ == "__main__":
    main()