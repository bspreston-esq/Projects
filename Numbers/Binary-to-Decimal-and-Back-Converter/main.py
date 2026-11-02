#!/usr/bin/env python3
"""Convert between decimal and binary representations."""
import argparse

def decimal_to_binary(n: int) -> str:
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    bits = []
    while n:
        bits.append("1" if n & 1 else "0")
        n >>= 1
    return sign + "".join(reversed(bits))

def binary_to_decimal(text: str) -> int:
    s = text.strip().replace(" ", "").replace("_", "")
    sign = 1
    if s.startswith(("-", "+")):
        sign = -1 if s[0] == "-" else 1
        s = s[1:]
    if not s or any(ch not in "01" for ch in s):
        raise ValueError(f"'{text}' is not a valid binary number")
    value = 0
    for ch in s:
        value = value * 2 + (ch == "1")
    return sign * value

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--to-binary", metavar="DECIMAL")
    group.add_argument("--to-decimal", metavar="BINARY")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for n in (0, 10, 255, 1024, -42):
            print(f"decimal {n:>6} -> binary {decimal_to_binary(n)}")
        for b in ("1010", "11111111", "10000000000", "-101010"):
            print(f"binary {b:>12} -> decimal {binary_to_decimal(b)}")
        return

    if args.to_binary is not None:
        try:
            print(decimal_to_binary(int(args.to_binary)))
        except ValueError:
            print("Error: enter an integer in decimal")
    elif args.to_decimal is not None:
        try:
            print(binary_to_decimal(args.to_decimal))
        except ValueError as exc:
            print(f"Error: {exc}")
    else:
        choice = input("Convert (1) decimal to binary or (2) binary to decimal? ").strip()
        if choice == "1":
            print(decimal_to_binary(int(input("Decimal number: "))))
        elif choice == "2":
            print(binary_to_decimal(input("Binary number: ")))
        else:
            print("Unknown choice")

if __name__ == "__main__":
    main()
