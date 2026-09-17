# Lab 08 — Ulta Beauty Peer Comparison

# Ulta Beauty
ulta_eps = 25.64

# Peer 1: Sally Beauty Holdings
sbh_price = 16.37
sbh_eps = 1.89

# Peer 2: Bath & Body Works
bbwi_price = 18.61
bbwi_eps = 3.11


# Calculate peer P/E ratios
sbh_pe = sbh_price / sbh_eps
bbwi_pe = bbwi_price / bbwi_eps


# Apply peer P/E ratios to Ulta's EPS
ulta_value_sbh = sbh_pe * ulta_eps
ulta_value_bbwi = bbwi_pe * ulta_eps


# Peer valuation range
low_value = min(ulta_value_sbh, ulta_value_bbwi)
high_value = max(ulta_value_sbh, ulta_value_bbwi)


# Print results
print("Lab 08 — Ulta Beauty Peer Comparison")
print()

print("Sally Beauty Holdings (SBH)")
print(f"P/E: {sbh_pe:.2f}x")
print(f"Implied Ulta value: ${ulta_value_sbh:.2f} per share")
print()

print("Bath & Body Works (BBWI)")
print(f"P/E: {bbwi_pe:.2f}x")
print(f"Implied Ulta value: ${ulta_value_bbwi:.2f} per share")
print()

print("Ulta Peer Valuation Range")
print(f"${low_value:.2f} - ${high_value:.2f} per share")
print()

# Validation check
print("Validation Check")
print(f"SBH: ${sbh_price} / ${sbh_eps} = {sbh_pe:.2f}x")
print()

# Peer removal test
print("Peer Removal Test")
print("If Bath & Body Works is removed:")
print(f"Remaining Sally Beauty reference = ${ulta_value_sbh:.2f} per share")