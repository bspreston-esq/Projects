#!/usr/bin/env python3
"""Translate English words to Pig Latin."""
import argparse
import re
import string

VOWELS = set("aeiou")

def pig_latin_word(word: str) -> str:
    """Translate a single word, preserving capitalization and punctuation."""
    match = re.match(r"^([^A-Za-z]*)([A-Za-z]+)([^A-Za-z]*)$", word)
    if not match:
        return word
    prefix, core, suffix = match.groups()
    lower = core.lower()
    if lower[0] in VOWELS:
        translated = lower + "way"
    else:
        index = 0
        while index < len(lower) and lower[index] not in VOWELS:
            index += 1
        if index == len(lower):  # no vowel, e.g. "rhythm"
            translated = lower + "ay"
        else:
            translated = lower[index:] + lower[:index] + "ay"
    if core[0].isupper() and core[1:].islower():
        translated = translated.capitalize()
    elif core.isupper():
        translated = translated.upper()
    return prefix + translated + suffix

def pig_latin(text: str) -> str:
    return " ".join(pig_latin_word(word) for word in text.split(" "))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for sample in ("banana", "Hello world", "apple", "Sky, the rhythm!",
                       "STRONG words", "Pig Latin is fun"):
            print(f"{sample!r:>24} -> {pig_latin(sample)!r}")
        return

    print(pig_latin(args.text if args.text is not None else input("Text: ")))

if __name__ == "__main__":
    main()
