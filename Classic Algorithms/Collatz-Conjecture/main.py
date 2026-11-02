#!/usr/bin/env python3
"""Collatz sequences: steps to reach 1, and the longest chain below a limit."""
import argparse

def collatz_sequence(n: int):
    if n < 1:
        raise ValueError("n must be a positive integer")
    sequence = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        sequence.append(n)
    return sequence

def collatz_steps(n: int) -> int:
    """Number of steps to reach 1, using O(1) memory."""
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

def longest_chain(limit: int):
    """Return (start, steps) with the longest chain for starts <= limit."""
    best_start, best_steps = 1, 0
    for start in range(2, limit + 1):
        steps = collatz_steps(start)
        if steps > best_steps:
            best_start, best_steps = start, steps
    return best_start, best_steps

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int)
    parser.add_argument("--limit", type=int, help="find the longest chain below this limit")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        print("27 ->", " -> ".join(map(str, collatz_sequence(27))))
        print(f"27 takes {collatz_steps(27)} steps")
        start, steps = longest_chain(10_000)
        print(f"Longest chain below 10,000: start {start} with {steps} steps")
        return

    if args.limit:
        start, steps = longest_chain(args.limit)
        print(f"Longest chain below {args.limit}: start {start}, {steps} steps")
        return
    n = args.number if args.number is not None else int(input("Starting number: "))
    try:
        sequence = collatz_sequence(n)
        print(" -> ".join(map(str, sequence)))
        print(f"{len(sequence) - 1} steps")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
