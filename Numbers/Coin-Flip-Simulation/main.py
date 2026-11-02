#!/usr/bin/env python3
"""Simulate coin flips and report the head/tail split."""
import argparse
import random

def simulate(flips: int, seed=None):
    """Return (heads, tails, longest_run) for `flips` fair coin tosses."""
    if flips < 0:
        raise ValueError("number of flips cannot be negative")
    rng = random.Random(seed)
    heads = tails = longest = run = 0
    last = None
    for _ in range(flips):
        side = rng.choice(("H", "T"))
        if side == "H":
            heads += 1
        else:
            tails += 1
        run = run + 1 if side == last else 1
        last = side
        longest = max(longest, run)
    return heads, tails, longest

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--flips", type=int)
    parser.add_argument("--seed", type=int, help="reproducible results")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for flips in (10, 100, 10000):
            heads, tails, longest = simulate(flips, seed=42)
            print(f"{flips:>6} flips: heads {heads:>6} ({heads/flips:6.2%}), "
                  f"tails {tails:>6} ({tails/flips:6.2%}), longest streak {longest}")
        return

    flips = args.flips if args.flips is not None else int(input("How many flips? "))
    try:
        heads, tails, longest = simulate(flips, args.seed)
        print(f"Heads: {heads}")
        print(f"Tails: {tails}")
        print(f"Longest streak: {longest}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
