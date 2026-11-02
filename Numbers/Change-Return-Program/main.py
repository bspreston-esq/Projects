#!/usr/bin/env python3
"""Compute change and the coins needed to make it."""
import argparse

DENOMINATIONS = [("quarter", 25), ("dime", 10), ("nickel", 5), ("penny", 1)]

def make_change(cost: float, paid: float):
    """Return (change_in_cents, {coin: count}) or raise ValueError."""
    cost_c, paid_c = round(cost * 100), round(paid * 100)
    if cost_c < 0 or paid_c < 0:
        raise ValueError("amounts cannot be negative")
    if paid_c < cost_c:
        raise ValueError(f"insufficient payment: short by ${(cost_c - paid_c) / 100:.2f}")
    remaining = paid_c - cost_c
    coins = {}
    for name, value in DENOMINATIONS:
        count, remaining = divmod(remaining, value)
        if count:
            coins[name] = count
    return paid_c - cost_c, coins

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cost", type=float)
    parser.add_argument("--paid", type=float)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for cost, paid in ((3.75, 5.00), (12.34, 20.00), (0.99, 1.00)):
            cents, coins = make_change(cost, paid)
            parts = ", ".join(f"{n} {name}{'s' if n > 1 else ''}" for name, n in coins.items())
            print(f"Cost ${cost:.2f}, paid ${paid:.2f}: change ${cents/100:.2f} ({parts})")
        return

    cost = args.cost if args.cost is not None else float(input("Cost: "))
    paid = args.paid if args.paid is not None else float(input("Amount given: "))
    try:
        cents, coins = make_change(cost, paid)
        print(f"Change: ${cents / 100:.2f}")
        for name, count in coins.items():
            print(f"  {count:>3} {name}{'s' if count > 1 else ''}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
