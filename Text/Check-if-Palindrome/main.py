#!/usr/bin/env python3
"""Check whether a string is a palindrome, ignoring case and punctuation."""
import argparse
import re

def normalize(text: str) -> str:
    """Keep only alphanumeric characters, lower-cased."""
    return re.sub(r"[^a-z0-9]", "", text.lower())

def is_palindrome(text: str) -> bool:
    cleaned = normalize(text)
    return cleaned == cleaned[::-1]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        samples = ["racecar", "A man, a plan, a canal: Panama",
                   "No 'x' in Nixon", "hello world", "Was it a car or a cat I saw?"]
        for sample in samples:
            print(f"{is_palindrome(sample)!s:>5}  {sample}")
        return

    text = args.text if args.text is not None else input("Text: ")
    print("palindrome" if is_palindrome(text) else "not a palindrome")

if __name__ == "__main__":
    main()
