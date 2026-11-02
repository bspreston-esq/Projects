#!/usr/bin/env python3
"""Caesar, Vigenere and Vernam (XOR) ciphers."""
import argparse
import base64

def caesar(text: str, key: int, decrypt: bool = False) -> str:
    if not 1 <= key <= 25:
        raise ValueError("Caesar key must be 1-25")
    shift = -key if decrypt else key
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)

def _key_letters(key: str):
    letters = [ord(c.lower()) - 97 for c in key if c.isalpha()]
    if not letters:
        raise ValueError("Vigenere key must contain letters")
    return letters

def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    letters = _key_letters(key)
    result, position = [], 0
    for char in text:
        if char.isalpha():
            shift = letters[position % len(letters)]
            position += 1
            base = 65 if char.isupper() else 97
            result.append(chr((ord(char) - base + (-shift if decrypt else shift)) % 26 + base))
        else:
            result.append(char)
    return "".join(result)

def vernam(text: str, key: str, decrypt: bool = False) -> str:
    """XOR the UTF-8 bytes with a repeating key; output is base64."""
    if not key:
        raise ValueError("Vernam key cannot be empty")
    if decrypt:
        data = base64.b64decode(text)
        plain = bytes(byte ^ ord(key[i % len(key)]) for i, byte in enumerate(data))
        return plain.decode("utf-8", errors="replace")
    data = text.encode("utf-8")
    cipher = bytes(byte ^ ord(key[i % len(key)]) for i, byte in enumerate(data))
    return base64.b64encode(cipher).decode("ascii")

CIPHERS = {"caesar": caesar, "vigenere": vigenere, "vernam": vernam}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cipher", choices=sorted(CIPHERS), default="caesar")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], default="encrypt")
    parser.add_argument("--text", default="Hello, World!")
    parser.add_argument("--key", default="3")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    def apply(cipher, text, key, decrypt):
        if cipher == "caesar":
            return CIPHERS[cipher](text, int(key), decrypt)
        return CIPHERS[cipher](text, key, decrypt)

    if args.demo:
        message = "Attack at dawn!"
        for cipher, key in (("caesar", "3"), ("vigenere", "LEMON"), ("vernam", "s3cret")):
            encrypted = apply(cipher, message, key, False)
            decrypted = apply(cipher, encrypted, key, True)
            print(f"{cipher:<8} key={key:<6} encrypted={encrypted}")
            print(f"{'':<8} decrypted={decrypted}  roundtrip={decrypted == message}")
        print("caesar key=20, 'HI' ->", caesar("HI", 20))
        return

    encrypted = args.mode == "decrypt"
    try:
        print(apply(args.cipher, args.text, args.key, encrypted))
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
