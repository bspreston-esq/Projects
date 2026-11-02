#!/usr/bin/env python3
"""Happy numbers, with cycle detection and a first-N finder."""
import argparse

def digit_square_sum(n: int) -> int:
    total = 0
    while n:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total

def is_happy(n: int) -> bool:
    """True if repeatedly summing squared digits reaches 1."""
    if n < 1:
        return False
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = digit_square_sum(n)
    return n == 1

def first_happy(count: int):
    found, candidate = [], 1
    while len(found) < count:
        if is_happy(candidate):
            found.append(candidate)
        candidate += 1
    return found

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int)
    parser.add_argument("--count", type=int, default=8, help="how many happy numbers to list")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        print("First 8 happy numbers:", first_happy(8))
        for n in (7, 19, 20, 97):
            chain, current = [n], n
            while current != 1 and current not in chain[:-1] and len(chain) < 12:
                current = digit_square_sum(current)
                chain.append(current)
            print(f"{n:>3}: " + " -> ".join(map(str, chain)) + (" (happy)" if current == 1 else " (unhappy)"))
        return

    if args.number is not None:
        print(f"{args.number} is {'happy' if is_happy(args.number) else 'unhappy'}")
        return
    print("First", args.count, "happy numbers:", first_happy(args.count))

if __name__ == "__main__":
    main()
