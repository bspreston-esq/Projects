#!/usr/bin/env python3
"""Caesar cipher: encode, decode, brute force and frequency analysis."""
import argparse
import collections
import string

def shift(text: str, key: int) -> str:
    """Shift letters by `key` (positive = encode), preserving case and punctuation."""
    key %= 26
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - 65 + key) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + key) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)

def encode(text: str, key: int) -> str:
    if not 1 <= key <= 25:
        raise ValueError("key must be between 1 and 25")
    return shift(text, key)

def decode(text: str, key: int) -> str:
    return shift(text, -key)

def brute_force(text: str):
    return [(key, shift(text, -key)) for key in range(1, 26)]

ENGLISH = {"e": 12.7, "t": 9.1, "a": 8.2, "o": 7.5, "i": 7.0, "n": 6.7,
           "s": 6.3, "h": 6.1, "r": 6.0, "d": 4.3}

def score(text: str) -> float:
    """Chi-squared distance from expected English letter frequencies (lower is better)."""
    letters = [char.lower() for char in text if char.isalpha()]
    if not letters:
        return float("inf")
    counts = collections.Counter(letters)
    total = len(letters)
    return sum((counts.get(letter, 0) / total - freq / 100) ** 2 for letter, freq in ENGLISH.items())

def crack(text: str):
    """Return (best_key, best_plaintext) by frequency scoring."""
    candidates = brute_force(text)
    key, plain = min(candidates, key=lambda item: score(item[1]))
    return key, plain

def demo() -> None:
    print("key 2:  HI ->", encode("HI", 2))
    print("key 20: HI ->", encode("HI", 20))
    message = "The quick brown fox jumps over the lazy dog"
    encrypted = encode(message, 11)
    print("encrypted:", encrypted)
    print("decrypted:", decode(encrypted, 11))
    key, plain = crack(encrypted)
    print(f"cracked key={key} -> {plain}")
    short = encode("Attack at dawn", 3)
    print("brute force (first 3):", [(k, text) for k, text in brute_force(short)[:3]])

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["encode", "decode", "crack", "brute"], default="encode")
    parser.add_argument("--text", default="Hello, World!")
    parser.add_argument("--key", type=int, default=3)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    try:
        if args.mode == "encode":
            print(encode(args.text, args.key))
        elif args.mode == "decode":
            print(decode(args.text, args.key))
        elif args.mode == "crack":
            key, plain = crack(args.text)
            print(f"key {key}: {plain}")
        else:
            for key, text in brute_force(args.text):
                print(f"{key:>2}: {text}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
