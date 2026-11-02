#!/usr/bin/env python3
"""Classic Fizz Buzz from 1 to 100."""
import argparse

def fizz_buzz(limit: int = 100):
    for number in range(1, limit + 1):
        if number % 15 == 0:
            yield "FizzBuzz"
        elif number % 3 == 0:
            yield "Fizz"
        elif number % 5 == 0:
            yield "Buzz"
        else:
            yield str(number)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    output = list(fizz_buzz(args.limit))
    print("\n".join(output if args.demo else output))
    if args.demo:
        print(f"\n({args.limit} values; Fizz x{output.count('Fizz')}, "
              f"Buzz x{output.count('Buzz')}, FizzBuzz x{output.count('FizzBuzz')})")

if __name__ == "__main__":
    main()
