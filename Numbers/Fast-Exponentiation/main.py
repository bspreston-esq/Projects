#!/usr/bin/env python3
"""Exponentiation by squaring in O(log b) multiplications."""
import argparse
import time

def fast_pow(base: int, exponent: int, modulus=None):
    """Return base**exponent (mod modulus if given) by repeated squaring."""
    if exponent < 0:
        if modulus is not None:
            raise ValueError("negative exponents are not supported with a modulus")
        return 1 / fast_pow(base, -exponent)
    result = 1
    base %= modulus if modulus else None
    while exponent:
        if exponent & 1:
            result = result * base
            if modulus:
                result %= modulus
        base = base * base
        if modulus:
            base %= modulus
        exponent >>= 1
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", nargs="?", type=int)
    parser.add_argument("exponent", nargs="?", type=int)
    parser.add_argument("--mod", type=int, help="optional modulus")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for base, exponent in ((2, 10), (3, 20), (7, 0), (2, 100), (5, -2)):
            expected = base ** exponent
            actual = fast_pow(base, exponent)
            print(f"{base}^{exponent} = {actual:g} (matches **: {abs(actual-expected) < 1e-9})")
        modulus = 1_000_000_007
        print(f"2^1000000 mod {modulus} = {fast_pow(2, 1_000_000, modulus)}")
        start = time.perf_counter()
        fast_pow(3, 10**6)
        fast = time.perf_counter() - start
        start = time.perf_counter()
        3 ** 10**6
        builtin = time.perf_counter() - start
        print(f"3^1000000: fast_pow {fast*1000:.1f} ms vs builtin {builtin*1000:.1f} ms")
        return

    base = args.base if args.base is not None else int(input("Base: "))
    exponent = args.exponent if args.exponent is not None else int(input("Exponent: "))
    try:
        print(fast_pow(base, exponent, args.mod))
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
