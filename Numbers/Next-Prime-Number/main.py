#!/usr/bin/env python3
"""Find the next prime number after a starting value, on demand."""
import argparse

class PrimeFinder:
    """Incremental sieve-backed prime generator."""

    def __init__(self, start: int = 0):
        self.candidate = max(2, start + 1)

    @staticmethod
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    def next(self) -> int:
        while not self.is_prime(self.candidate):
            self.candidate += 1
        result = self.candidate
        self.candidate += 1
        return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0, help="search after this number")
    parser.add_argument("--count", type=int, default=5, help="primes to print in demo mode")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    finder = PrimeFinder(args.start)
    if args.demo:
        print(f"First {args.count} primes after {args.start}:")
        for _ in range(args.count):
            print(finder.next(), end=" ")
        print()
        return

    print(f"Searching for primes after {args.start}. Press Enter for the next one, 'q' to quit.")
    while True:
        answer = input("next prime? [Enter/q] ").strip().lower()
        if answer == "q":
            break
        print(finder.next())

if __name__ == "__main__":
    main()
