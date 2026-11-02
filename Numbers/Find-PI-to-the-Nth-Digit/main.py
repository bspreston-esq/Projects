#!/usr/bin/env python3
"""Compute pi to a requested number of decimal places (Chudnovsky algorithm)."""
import argparse
from decimal import Decimal, getcontext, ROUND_DOWN

MAX_DIGITS = 1000  # hard limit, as the problem asks

def pi_to_digits(digits: int) -> Decimal:
    """Return pi truncated (not rounded) to `digits` decimal places."""
    if digits < 0:
        raise ValueError("number of digits cannot be negative")
    if digits > MAX_DIGITS:
        raise ValueError(f"limit is {MAX_DIGITS} decimal places")
    getcontext().prec = digits + 20
    C = 426880 * Decimal(10005).sqrt()
    M, L, X, K, S = 1, 13591409, 1, 6, Decimal(13591409)
    for i in range(1, digits // 14 + 3):
        M = (K ** 3 - 16 * K) * M // i ** 3
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    pi = C / S
    return pi.quantize(Decimal(1).scaleb(-digits), rounding=ROUND_DOWN)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("digits", nargs="?", type=int, help="decimal places (0-%d)" % MAX_DIGITS)
    parser.add_argument("--demo", action="store_true", help="show sample output and exit")
    args = parser.parse_args()

    if args.demo:
        for d in (0, 2, 10, 50, 100):
            print(f"pi to {d:>3} digits: {pi_to_digits(d):.{d}f}")
        return

    digits = args.digits
    while digits is None:
        raw = input(f"How many decimal places of pi (0-{MAX_DIGITS})? ").strip()
        try:
            digits = int(raw)
        except ValueError:
            print("Please enter an integer.")
    try:
        print(pi_to_digits(digits))
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
