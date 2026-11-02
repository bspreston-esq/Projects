#!/usr/bin/env python3
"""Find all primes up to N with the Sieve of Eratosthenes."""
import argparse
import math
import time

def sieve(limit: int):
    """Return a list of primes <= limit using a bytearray sieve."""
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for number in range(2, math.isqrt(limit) + 1):
        if flags[number]:
            start = number * number
            flags[start:limit + 1:number] = b"\x00" * (((limit - start) // number) + 1)
    return [i for i, is_prime in enumerate(flags) if is_prime]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("limit", nargs="?", type=int)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for limit in (10, 100, 1_000_000):
            start = time.perf_counter()
            primes = sieve(limit)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"up to {limit:>9,}: {len(primes):>7,} primes, "
                  f"largest {primes[-1]:>7,}, {elapsed:6.1f} ms")
        return

    limit = args.limit if args.limit is not None else int(input("Find primes up to: "))
    primes = sieve(limit)
    print(f"{len(primes)} primes up to {limit}")
    print(", ".join(map(str, primes[:50])) + (" ..." if len(primes) > 50 else ""))

if __name__ == "__main__":
    main()
