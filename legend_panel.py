
"""Lab 19 — Legend Panel: Buffett, Graham, and Burry."""

import re
import math

CHECK_LABELS = {
    "Buffett": [
        ("roe_15_every_year", "ROE >= 15% every year"),
        ("owner_earnings_positive", "Owner earnings positive every year"),
        ("owner_earnings_grew", "Owner earnings grew, first to last"),
    ],
    "Graham": [
        ("current_ratio", "Current ratio >= threshold, latest year"),
        ("net_income_positive", "Net income positive every year"),
        ("net_income_grew", "Net income grew, first to last"),
    ],
    "Burry": [
        ("ocf_covers_income", "Operating cash flow >= net income every year"),
        ("liabilities_to_equity", "Liabilities <= 2x equity, latest year"),
    ],
}

def number(value):
    """Return a finite float or None for missing inputs."""
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (ValueError, TypeError):
        return None


def status(condition):
    if condition is None:
        return "not known"
    return "pass" if condition else "fail"


def every_year(rows, keys, test):
    if not rows:
        return "not known"
    values = []
    for row in rows:
        items = [number(row.get(k)) for k in keys]
        if any(v is None for v in items):
            return "not known"
        values.append(test(*items))
    return status(all(values))


def grew(rows, key):
    if len(rows) < 2:
        return "not known"
    first = number(rows[0].get(key))
    last = number(rows[-1].get(key))
    if first is None or last is None:
        return "not known"
    return status(last > first)


def make_checks(rows, graham_threshold=2.0):
    """Rows must be sorted oldest to newest."""
    rows = sorted(rows, key=lambda r: r["fy_end"])
    latest = rows[-1] if rows else {}

    current_assets = number(latest.get("assets_current"))
    current_liabilities = number(latest.get("liabilities_current"))
    liabilities = number(latest.get("liabilities"))
    equity = number(latest.get("equity"))

    current_ratio = (
        current_assets / current_liabilities
        if current_assets is not None
        and current_liabilities is not None
        and current_liabilities > 0
        else None
    )

    liabilities_to_equity = (
        liabilities / equity
        if liabilities is not None
        and equity is not None
        and equity > 0
        else None
    )

    checks = {
        "Buffett": {
            "roe_15_every_year": every_year(
                rows, ["roe"], lambda roe: roe >= 15
            ),
            "owner_earnings_positive": every_year(
                rows, ["owner_earnings"], lambda oe: oe > 0
            ),
            "owner_earnings_grew": grew(rows, "owner_earnings"),
        },
        "Graham": {
            "current_ratio": status(
                current_ratio >= graham_threshold
                if current_ratio is not None else None
            ),
            "net_income_positive": every_year(
                rows, ["net_income"], lambda ni: ni > 0
            ),
            "net_income_grew": grew(rows, "net_income"),
        },
        "Burry": {
            "ocf_covers_income": every_year(
                rows, ["operating_cash_flow", "net_income"],
                lambda ocf, ni: ocf >= ni
            ),
            "liabilities_to_equity": status(
                liabilities_to_equity <= 2
                if liabilities_to_equity is not None else None
            ),
        },
    }

    ratios = {
        "current_ratio": current_ratio,
        "liabilities_to_equity": liabilities_to_equity,
    }
    return checks, ratios


def verdict(checks):
    passed = sum(v == "pass" for v in checks.values())
    total = len(checks)
    unknown = sum(v == "not known" for v in checks.values())

    if unknown:
        decision = "Incomplete — not known"
    elif passed == total:
        decision = "All checks pass"
    else:
        decision = "At least one check fails"

    return f"{passed}/{total} pass — {decision}"


def panel_table(checks):
    result = []
    for investor, labels in CHECK_LABELS.items():
        for key, label in labels:
            result.append({
                "Investor": investor,
                "Check": label,
                "Status": checks[investor][key],
            })
    return result


def fmt(value, decimals=2):
    v = number(value)
    return "not found" if v is None else f"{v:,.{decimals}f}"


def make_memos(rows, checks, ratios, graham_threshold=2.0):
    """Create memos only from the calculated and displayed facts."""
    rows = sorted(rows, key=lambda r: r["fy_end"])
    latest = rows[-1] if rows else {}

    first = rows[0] if rows else {}
    year = latest.get("fy_end", "not found")

    memos = {}

    memos["Buffett"] = (
        "### Buffett Investment Memo\n\n"
        f"Latest fiscal year: {year}.\n\n"
        f"Latest ROE: {fmt(latest.get('roe'), 1)}%. "
        f"Latest owner earnings: "
        f"{fmt(latest.get('owner_earnings'), 1)} million.\n\n"
        f"First-year owner earnings: "
        f"{fmt(first.get('owner_earnings'), 1)} million.\n\n"
        f"Checks: {verdict(checks['Buffett'])}.\n\n"
        "Focus: profitability and owner earnings."
    )

    memos["Graham"] = (
        "### Graham Investment Memo\n\n"
        f"Latest fiscal year: {year}.\n\n"
        f"Current assets: {fmt(latest.get('assets_current'), 1)} million. "
        f"Current liabilities: "
        f"{fmt(latest.get('liabilities_current'), 1)} million.\n\n"
        f"Current ratio: {fmt(ratios['current_ratio'])}. "
        f"Threshold: {graham_threshold:.1f}.\n\n"
        f"First-year net income: "
        f"{fmt(first.get('net_income'), 1)} million. "
        f"Latest net income: "
        f"{fmt(latest.get('net_income'), 1)} million.\n\n"
        f"Checks: {verdict(checks['Graham'])}.\n\n"
        "Focus: liquidity and consistent earnings."
    )

    memos["Burry"] = (
        "### Burry Investment Memo\n\n"
        f"Latest fiscal year: {year}.\n\n"
        f"Operating cash flow: "
        f"{fmt(latest.get('operating_cash_flow'), 1)} million. "
        f"Net income: {fmt(latest.get('net_income'), 1)} million.\n\n"
        f"Liabilities: {fmt(latest.get('liabilities'), 1)} million. "
        f"Equity: {fmt(latest.get('equity'), 1)} million.\n\n"
        f"Liabilities/equity: "
        f"{fmt(ratios['liabilities_to_equity'])}.\n\n"
        f"Checks: {verdict(checks['Burry'])}.\n\n"
        "Focus: cash flow quality and balance-sheet risk."
    )

    return memos


def audit_memos(rows, ratios, memos, graham_threshold=2.0):
    """Flag numerical tokens absent from the approved printed facts."""
    allowed = {0.0, 2.0, 3.0, 5.0, 15.0,
               float(graham_threshold)}

    keys = [
        "revenue", "net_income", "operating_cash_flow",
        "capital_spending", "equity", "roe",
        "owner_earnings", "liabilities",
        "assets_current", "liabilities_current",
    ]

    for row in rows:
        year = str(row.get("fy_end", ""))
        if len(year) >= 4 and year[:4].isdigit():
            allowed.add(float(year[:4]))
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", year):
            for part in year.split("-"):
                allowed.add(float(part))

        for key in keys:
            value = number(row.get(key))
            if value is not None:
                allowed.update([
                    round(value, 0),
                    round(value, 1),
                    round(value, 2),
                ])

    for value in ratios.values():
        v = number(value)
        if v is not None:
            allowed.update([round(v, 0), round(v, 1), round(v, 2)])

    pattern = r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?%?(?![A-Za-z0-9])"
    flagged = {}

    for investor, memo in memos.items():
        unsupported = []
        for token in re.findall(pattern, memo):
            value = float(token.replace(",", "").replace("%", ""))
            if round(value, 2) not in allowed:
                unsupported.append(token)
        flagged[investor] = unsupported

    return flagged


def run_panel(rows, graham_threshold=2.0):
    """Main function for the Streamlit app."""
    rows = sorted(rows, key=lambda r: r["fy_end"])
    checks, ratios = make_checks(rows, graham_threshold)
    memos = make_memos(rows, checks, ratios, graham_threshold)
    flags = audit_memos(rows, ratios, memos, graham_threshold)

    return {
        "checks": checks,
        "ratios": ratios,
        "table": panel_table(checks),
        "verdicts": {
            name: verdict(values)
            for name, values in checks.items()
        },
        "memos": memos,
        "flags": flags,
    }