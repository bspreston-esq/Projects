#!/usr/bin/env python3
"""Reverse a string, by slicing and by hand."""
import argparse

def reverse_slice(text: str) -> str:
    return text[::-1]

def reverse_manual(text: str) -> str:
    """Reverse by walking from the end, without slicing."""
    result = []
    index = len(text) - 1
    while index >= 0:
        result.append(text[index])
        index -= 1
    return "".join(result)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for sample in ("hello", "racecar", "A man, a plan!", "éclair", ""):
            reversed_text = reverse_slice(sample)
            assert reversed_text == reverse_manual(sample)
            print(f"{sample!r:>20} -> {reversed_text!r}")
        print("Both implementations agree on every sample.")
        return

    text = args.text if args.text is not None else input("Enter a string: ")
    print(reverse_slice(text))

if __name__ == "__main__":
    main()
