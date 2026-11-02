#!/usr/bin/env python3
"""Find all prime factors of an integer, with multiplicities."""
import argparse

def factorize(n: int):
    """Return a list of (prime, exponent) pairs for n. Raises for n < 2."""
    if n < 2:
        raise ValueError("prime factorization is defined for integers >= 2")
    factors = []
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    if count:
        factors.append((2, count))
    p = 3
    while p * p <= n:
        count = 0
        while n % p == 0:
            n //= p
            count += 1
        if count:
            factors.append((p, count))
        p += 2
    if n > 1:
        factors.append((n, 1))
    return factors

def format_factors(factors) -> str:
    return " x ".join(str(p) if e == 1 else f"{p}^{e}" for p, e in factors)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for n in (12, 97, 360, 1001, 999999):
            print(f"{n:>7} = {format_factors(factorize(n))}")
        return

    n = args.number
    while n is None:
        try:
            n = int(input("Enter an integer (>= 2): ").strip())
        except ValueError:
            print("Please enter an integer.")
    try:
        print(f"{n} = {format_factors(factorize(n))}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
