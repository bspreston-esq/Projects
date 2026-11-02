#!/usr/bin/env python3
"""Compute Euler's number e to a requested number of decimal places."""
import argparse
from decimal import Decimal, getcontext, ROUND_DOWN

MAX_DIGITS = 1000

def e_to_digits(digits: int) -> Decimal:
    """Return e truncated (not rounded) to `digits` decimal places using 1/k!."""
    if digits < 0:
        raise ValueError("number of digits cannot be negative")
    if digits > MAX_DIGITS:
        raise ValueError(f"limit is {MAX_DIGITS} decimal places")
    getcontext().prec = digits + 20
    total = Decimal(1)
    term = Decimal(1)
    k = 0
    # Each term adds ~1/k!; stop when it is below the last guard digit.
    epsilon = Decimal(1).scaleb(-(digits + 15))
    while term > epsilon:
        k += 1
        term /= k
        total += term
    return total.quantize(Decimal(1).scaleb(-digits), rounding=ROUND_DOWN)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("digits", nargs="?", type=int, help="decimal places (0-%d)" % MAX_DIGITS)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for d in (0, 2, 10, 50, 100):
            print(f"e to {d:>3} digits: {e_to_digits(d):.{d}f}")
        return

    digits = args.digits
    while digits is None:
        try:
            digits = int(input(f"How many decimal places of e (0-{MAX_DIGITS})? ").strip())
        except ValueError:
            print("Please enter an integer.")
    try:
        print(e_to_digits(digits))
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
