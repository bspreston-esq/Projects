#!/usr/bin/env python3
"""Generate the Fibonacci sequence by term count or up to a maximum value."""
import argparse

def fib_terms(count: int):
    """Yield the first `count` Fibonacci numbers (F0=0, F1=1)."""
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b

def fib_upto(max_value: int):
    """Yield Fibonacci numbers less than or equal to `max_value`."""
    a, b = 0, 1
    while a <= max_value:
        yield a
        a, b = b, a + b

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int,
                        help="how many terms (default) or the upper bound with --max")
    parser.add_argument("--max", action="store_true",
                        help="treat the number as an upper bound instead of a term count")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        print("First 10 terms:", list(fib_terms(10)))
        print("Terms <= 100:  ", list(fib_upto(100)))
        return

    if args.number is None:
        raw = input("How many terms (or enter a maximum with 'max N')? ").strip().split()
        if len(raw) == 2 and raw[0].lower() == "max":
            args.max, args.number = True, int(raw[1])
        else:
            args.number = int(raw[0])

    if args.number < 0:
        print("Error: the number must be non-negative")
        return
    seq = list(fib_upto(args.number)) if args.max else list(fib_terms(args.number))
    print(", ".join(map(str, seq)) if seq else "(empty)")

if __name__ == "__main__":
    main()
