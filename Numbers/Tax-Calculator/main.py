#!/usr/bin/env python3
"""Add sales tax or VAT to a price using built-in or custom rates."""
import argparse

# US state-level base sales tax rates (percent); local rates vary.
US_STATES = {
    "AL": 4.0, "AK": 0.0, "AZ": 5.6, "AR": 6.5, "CA": 7.25, "CO": 2.9,
    "CT": 6.35, "DE": 0.0, "FL": 6.0, "GA": 4.0, "HI": 4.0, "ID": 6.0,
    "IL": 6.25, "IN": 7.0, "IA": 6.0, "KS": 6.5, "KY": 6.0, "LA": 4.45,
    "ME": 5.5, "MD": 6.0, "MA": 6.25, "MI": 6.0, "MN": 6.875, "MS": 7.0,
    "MO": 4.225, "MT": 0.0, "NE": 5.5, "NV": 6.85, "NH": 0.0, "NJ": 6.625,
    "NM": 4.875, "NY": 4.0, "NC": 4.75, "ND": 5.0, "OH": 5.75, "OK": 4.5,
    "OR": 0.0, "PA": 6.0, "RI": 7.0, "SC": 6.0, "SD": 4.2, "TN": 7.0,
    "TX": 6.25, "UT": 6.1, "VT": 6.0, "VA": 5.3, "WA": 6.5, "WV": 6.0,
    "WI": 5.0, "WY": 4.0,
}
COUNTRIES = {"uk": 20.0, "germany": 19.0, "france": 20.0, "italy": 22.0,
             "spain": 21.0, "netherlands": 21.0, "ireland": 23.0,
             "canada": 5.0, "australia": 10.0, "japan": 10.0,
             "india": 18.0, "brazil": 17.0, "mexico": 16.0}

def tax_rate(location: str):
    """Resolve a state code, country name or percent string to a rate."""
    loc = location.strip()
    if loc.upper() in US_STATES:
        return US_STATES[loc.upper()], f"US state {loc.upper()}"
    if loc.lower() in COUNTRIES:
        return COUNTRIES[loc.lower()], loc.title()
    try:
        return float(loc.rstrip("%")), "custom rate"
    except ValueError:
        raise ValueError(f"unknown location '{location}'; use a US state code, country, or percentage")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cost", type=float)
    parser.add_argument("--tax", help="state code (e.g. CA), country, or percent")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for cost, where in ((100.0, "CA"), (49.99, "TX"), (250.0, "germany"), (80.0, "8.25%")):
            rate, label = tax_rate(where)
            tax = cost * rate / 100
            print(f"${cost:>7,.2f} + {rate:g}% ({label}): tax ${tax:,.2f}, total ${cost + tax:,.2f}")
        return

    cost = args.cost if args.cost is not None else float(input("Cost: "))
    where = args.tax or input("State code, country, or tax percent: ").strip()
    try:
        rate, label = tax_rate(where)
        tax = cost * rate / 100
        print(f"Tax ({label}, {rate:g}%): ${tax:,.2f}")
        print(f"Total: ${cost + tax:,.2f}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
