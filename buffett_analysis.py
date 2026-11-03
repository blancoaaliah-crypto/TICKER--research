
import argparse
import json
import os
import requests
from datetime import date, datetime

BASE = "https://www.sec.gov"
DATA = "https://data.sec.gov/api/xbrl/companyfacts"

TAGS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": [
        "NetCashProvidedByUsedInOperatingActivities"
    ],
    "capital_spending": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
    "equity": ["StockholdersEquity"],
}


def get_json(url, headers):
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def get_company(ticker, headers):
    companies = get_json(
        f"{BASE}/files/company_tickers.json", headers
    )
    for company in companies.values():
        if company["ticker"].upper() == ticker.upper():
            return company["cik_str"], company["title"]
    raise ValueError(f"Ticker not found: {ticker}")


def select_fact(facts, tags, fy_end, annual):
    for tag in tags:
        entries = (
            facts.get("us-gaap", {})
            .get(tag, {})
            .get("units", {})
            .get("USD", [])
        )

        matches = []
        for item in entries:
            if item.get("form") != "10-K":
                continue
            if item.get("end") != fy_end:
                continue
            if not isinstance(item.get("val"), (int, float)):
                continue

            if annual:
                if not item.get("start"):
                    continue
                days = (
                    date.fromisoformat(item["end"])
                    - date.fromisoformat(item["start"])
                ).days
                if not 330 <= days <= 380:
                    continue
            else:
                if item.get("start"):
                    continue

            matches.append(item)

        if matches:
            chosen = max(
                matches,
                key=lambda x: (
                    x.get("filed", ""),
                    x.get("accn", ""),
                ),
            )
            return chosen["val"] / 1_000_000, tag

    return None, "not found"


def calculate_row(facts, fy_end):
    row = {"fy_end": fy_end, "tags": {}}

    for metric, tags in TAGS.items():
        value, tag = select_fact(
            facts, tags, fy_end,
            annual=(metric != "equity")
        )
        row[metric] = value
        row["tags"][metric] = tag

    equity = row["equity"]
    net_income = row["net_income"]
    ocf = row["operating_cash_flow"]
    capex = row["capital_spending"]

    row["roe"] = (
        net_income / equity * 100
        if net_income is not None
        and equity is not None
        and equity > 0
        else None
    )

    row["owner_earnings"] = (
        ocf - capex
        if ocf is not None and capex is not None
        else None
    )

    row["tags"]["roe"] = "calculated: NetIncomeLoss / StockholdersEquity"
    row["tags"]["owner_earnings"] = (
        "calculated: operating cash flow - capital spending"
    )
    return row


def three_checks(rows):
    if len(rows) != 5:
        return {
            "roe_15_every_year": "not known",
            "owner_earnings_positive": "not known",
            "owner_earnings_grew": "not known",
        }

    def every_year(key, condition):
        values = [r[key] for r in rows]
        if any(v is None for v in values):
            return "not known"
        return "pass" if all(condition(v) for v in values) else "fail"

    owners = [r["owner_earnings"] for r in rows]

    growth = (
        "not known"
        if owners[0] is None or owners[-1] is None
        else "pass" if owners[-1] > owners[0] else "fail"
    )

    return {
        "roe_15_every_year": every_year(
            "roe", lambda x: x >= 15
        ),
        "owner_earnings_positive": every_year(
            "owner_earnings", lambda x: x > 0
        ),
        "owner_earnings_grew": growth,
    }


def analyze(ticker, user_agent):
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate",
    }

    cik, company = get_company(ticker, headers)
    facts = get_json(
        f"{DATA}/CIK{cik:010d}.json", headers
    )["facts"]

    # Find fiscal-year ends from 10-K revenue observations.
    ends = set()
    for tag in TAGS["revenue"]:
        entries = (
            facts.get("us-gaap", {})
            .get(tag, {})
            .get("units", {})
            .get("USD", [])
        )
        for item in entries:
            if (
                item.get("form") == "10-K"
                and item.get("fp") == "FY"
                and item.get("start")
                and item.get("end")
            ):
                days = (
                    date.fromisoformat(item["end"])
                    - date.fromisoformat(item["start"])
                ).days
                if 330 <= days <= 380:
                    ends.add(item["end"])

    years = sorted(ends, reverse=True)[:5]
    rows = [calculate_row(facts, end) for end in years]
    rows.reverse()

    return {
        "ticker": ticker.upper(),
        "company": company,
        "units": "USD millions except ROE percent",
        "rows": rows,
        "checks": three_checks(rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument(
        "--user-agent",
        default=os.getenv("SEC_USER_AGENT"),
    )
    args = parser.parse_args()

    if not args.user_agent or "@" not in args.user_agent:
        parser.error(
            "Set SEC_USER_AGENT to 'Your Name your@email.com'"
        )

    result = analyze(args.ticker, args.user_agent)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()