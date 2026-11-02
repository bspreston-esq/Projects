#!/usr/bin/env python3
"""Count vowels, individually and in total."""
import argparse
from collections import Counter

VOWELS = "aeiou"

def count_vowels(text: str, include_y: bool = False):
    """Return (Counter of vowel counts, total)."""
    letters = VOWELS + ("y" if include_y else "")
    counts = Counter(character for character in text.lower() if character in letters)
    for vowel in letters:
        counts.setdefault(vowel, 0)
    return counts, sum(counts.values())

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--file", help="read text from a file instead")
    parser.add_argument("--y", action="store_true", help="count y as a vowel")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        sample = "The quick brown fox jumps over the lazy dog."
        counts, total = count_vowels(sample, include_y=True)
        print(f"text: {sample}")
        print("counts:", ", ".join(f"{v}={counts[v]}" for v in sorted(counts)))
        print(f"total vowels: {total}")
        return

    if args.file:
        with open(args.file, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    else:
        text = args.text if args.text is not None else input("Text: ")
    counts, total = count_vowels(text, args.y)
    for vowel in sorted(counts):
        print(f"{vowel}: {counts[vowel]}")
    print(f"total: {total}")

if __name__ == "__main__":
    main()
