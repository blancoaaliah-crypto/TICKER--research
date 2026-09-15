from statistics import median

# -----------------------------
# INPUTS
# -----------------------------

target = {
    "ticker": "ABG",
    "name": "Asbury Automotive",
    "price": 243.03,
    "eps": 21.50
}

peers = [
    {
        "ticker": "AN",
        "name": "AutoNation",
        "price": 169.84,
        "eps": 16.92
    },
    {
        "ticker": "GPI",
        "name": "Group 1 Automotive",
        "price": 421.48,
        "eps": 36.81
    }
]


# -----------------------------
# FUNCTIONS
# -----------------------------

def is_valid(company):
    price = company.get("price")
    eps = company.get("eps")

    return (
        isinstance(price, (int, float))
        and isinstance(eps, (int, float))
        and price > 0
        and eps > 0
    )


def pe_ratio(company):
    return company["price"] / company["eps"]


# -----------------------------
# CLEAN PEER LIST
# -----------------------------

clean_peers = []
seen = set()

for peer in peers:
    ticker = peer["ticker"].upper()

    # Do not include Asbury as its own peer
    if ticker == target["ticker"].upper():
        continue

    # Remove duplicates
    if ticker in seen:
        continue

    seen.add(ticker)
    clean_peers.append(peer)


# -----------------------------
# CALCULATE PEER P/E
# -----------------------------

valid_peers = []

print("PEER P/E MULTIPLES")
print("-" * 40)

for peer in clean_peers:

    if is_valid(peer):
        pe = pe_ratio(peer)
        valid_peers.append((peer, pe))

        print(
            f'{peer["name"]} ({peer["ticker"]}): '
            f'{pe:.6f}x'
        )

    else:
        print(
            f'{peer["name"]} ({peer["ticker"]}): '
            "not meaningful"
        )


# -----------------------------
# IMPLIED ASBURY VALUE
# -----------------------------

print("\nASBURY IMPLIED VALUATION")
print("-" * 40)

if not is_valid(target):
    print("Target inputs are not meaningful.")

elif len(valid_peers) == 0:
    print("No usable peers.")

else:
    multiples = [pe for peer, pe in valid_peers]

    minimum_pe = min(multiples)
    median_pe = median(multiples)
    maximum_pe = max(multiples)

    minimum_price = minimum_pe * target["eps"]
    median_price = median_pe * target["eps"]
    maximum_price = maximum_pe * target["eps"]

    print(f"Minimum peer P/E: {minimum_pe:.6f}x")
    print(f"Median peer P/E:  {median_pe:.6f}x")
    print(f"Maximum peer P/E: {maximum_pe:.6f}x")

    if len(valid_peers) == 1:
        print(f"\nReference implied price: ${median_price:.2f}")
        print("Only one valid peer, so there is no range.")

    else:
        print(
            f"\nImplied price range: "
            f"${minimum_price:.2f} - ${maximum_price:.2f}"
        )

        print(f"Median implied price: ${median_price:.2f}")


# -----------------------------
# LEAVE-ONE-OUT CHECK
# -----------------------------

print("\nLEAVE-ONE-OUT ANALYSIS")
print("-" * 40)

if len(valid_peers) > 0 and is_valid(target):

    full_multiples = [pe for peer, pe in valid_peers]

    full_median_pe = median(full_multiples)

    full_median_price = (
        full_median_pe * target["eps"]
    )

    for removed_peer, removed_pe in valid_peers:

        remaining_multiples = [
            pe
            for peer, pe in valid_peers
            if peer["ticker"] != removed_peer["ticker"]
        ]

        print(
            f"\nRemove {removed_peer['name']} "
            f"({removed_peer['ticker']}):"
        )

        if len(remaining_multiples) == 0:
            print("No estimate remains.")

        else:
            remaining_median_pe = median(
                remaining_multiples
            )

            remaining_price = (
                remaining_median_pe * target["eps"]
            )

            change = (
                remaining_price - full_median_price
            )

            print(
                f"Remaining median-implied price: "
                f"${remaining_price:.2f}"
            )

            print(
                f"Change from full-peer estimate: "
                f"${change:+.2f}"
            )