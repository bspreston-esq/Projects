#!/usr/bin/env python3
"""Validate card numbers with the Luhn checksum and issuer prefix rules."""
import argparse
import re

def luhn_valid(digits: str) -> bool:
    total, parity = 0, len(digits) % 2
    for index, char in enumerate(digits):
        value = int(char)
        if index % 2 == parity:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0

def detect_issuer(digits: str):
    """Return the card network for a number, or None if the prefix is unknown."""
    n = len(digits)
    if digits.startswith("4") and n in (13, 16, 19):
        return "Visa"
    if n == 15 and digits[:2] in ("34", "37"):
        return "American Express"
    prefix2, prefix4 = int(digits[:2]), int(digits[:4])
    if n == 16 and (51 <= prefix2 <= 55 or 2221 <= prefix4 <= 2720):
        return "Mastercard"
    if (n == 16 and (digits.startswith("6011") or digits.startswith("65")
                     or 644 <= int(digits[:3]) <= 649)) or (n == 19 and digits.startswith("65")):
        return "Discover"
    if n in (15, 16, 19) and (digits.startswith("3528") or digits.startswith("3529")
                              or digits.startswith("353") or digits.startswith("354")
                              or digits.startswith("355") or digits.startswith("356")
                              or digits.startswith("357") or digits.startswith("358")):
        return "JCB"
    return None

def validate(number: str):
    """Return (is_valid, issuer, reason)."""
    cleaned = re.sub(r"[\s-]", "", number)
    if not cleaned.isdigit():
        return False, None, "contains characters that are not digits"
    if not 12 <= len(cleaned) <= 19:
        return False, None, "length must be 12-19 digits"
    issuer = detect_issuer(cleaned)
    if issuer is None:
        return False, None, "unknown issuer prefix"
    if not luhn_valid(cleaned):
        return False, issuer, "failed the Luhn checksum"
    return True, issuer, "valid"

def mask(number: str) -> str:
    digits = re.sub(r"\D", "", number)
    return "*" * max(0, len(digits) - 4) + digits[-4:]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        samples = ["4111111111111111", "4111111111111112", "378282246310005",
                   "5555555555554444", "6011111111111117", "30569309025904",
                   "1234-5678-9012-3456"]
        for number in samples:
            ok, issuer, reason = validate(number)
            print(f"{mask(number):>19}  {'VALID' if ok else 'INVALID':<7} {issuer or '-':<16} {reason}")
        return

    number = args.number or input("Card number: ").strip()
    ok, issuer, reason = validate(number)
    print(f"{'Valid' if ok else 'Invalid'} {issuer or ''}: {reason}")

if __name__ == "__main__":
    main()
