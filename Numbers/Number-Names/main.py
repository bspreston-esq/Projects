#!/usr/bin/env python3
"""Spell out numbers in English, up to the quadrillions and with decimals."""
import argparse

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]
SCALES = [(10**15, "quadrillion"), (10**12, "trillion"), (10**9, "billion"),
          (10**6, "million"), (10**3, "thousand"), (1, "")]

def _below_thousand(n: int) -> str:
    words = []
    if n >= 100:
        words += [ONES[n // 100], "hundred"]
        n %= 100
        if n:
            words.append("and")
    if n >= 20:
        words.append(TENS[n // 10])
        if n % 10:
            words.append(ONES[n % 10])
    elif n:
        words.append(ONES[n])
    return " ".join(words)

def number_name(number) -> str:
    """Return the English name for an int/float, handling negatives and decimals."""
    negative = number < 0
    text = f"{abs(number):.10f}".rstrip("0").rstrip(".") if isinstance(number, float) else str(abs(int(number)))
    whole, _, fraction = text.partition(".")
    n = int(whole)
    if n == 0:
        words = "zero"
    else:
        parts = []
        for value, label in SCALES:
            if n >= value:
                chunk, n = divmod(n, value)
                parts.append(_below_thousand(chunk) + (f" {label}" if label else ""))
        words = " ".join(parts)
    if fraction:
        words += " point " + " ".join(ONES[int(d)] for d in fraction)
    return ("minus " + words) if negative else words

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for value in (0, 7, 21, 100, 101, 999, 1000, 1234567, 1000000001,
                      -42, 3.14, 1000000):
            print(f"{value:>12} = {number_name(value)}")
        return

    raw = args.number or input("Number: ").strip()
    try:
        value = float(raw) if "." in raw else int(raw)
        if isinstance(value, float) and abs(value) > 10**15:
            raise ValueError("absolute value must be below one quadrillion")
        print(number_name(value))
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
