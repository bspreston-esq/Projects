#!/usr/bin/env python3
"""Factorial by loop and by recursion, with memoisation for the recursive path."""
import argparse
import sys

sys.setrecursionlimit(10000)

def factorial_loop(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result

def factorial_recursive(n: int, _memo=None) -> int:
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    if _memo is None:
        _memo = {0: 1, 1: 1}
    if n not in _memo:
        _memo[n] = n * factorial_recursive(n - 1, _memo)
    return _memo[n]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for n in (0, 1, 5, 10, 20, 52):
            loop_value = factorial_loop(n)
            rec_value = factorial_recursive(n)
            assert loop_value == rec_value
            shown = str(loop_value) if len(str(loop_value)) <= 30 else f"{str(loop_value)[:12]}... ({len(str(loop_value))} digits)"
            print(f"{n:>3}! = {shown}")
        print("Loop and recursive results match for all samples.")
        return

    n = args.number
    while n is None:
        try:
            n = int(input("Enter a non-negative integer: ").strip())
        except ValueError:
            print("Please enter an integer.")
    try:
        print(f"loop:      {factorial_loop(n)}")
        print(f"recursion: {factorial_recursive(n)}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
