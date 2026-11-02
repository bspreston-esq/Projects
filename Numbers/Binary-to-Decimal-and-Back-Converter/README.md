# Binary to Decimal and Back Converter

**Category:** Numbers

## Problem

Develop a converter to convert a decimal number to binary or a binary number to its decimal equivalent.

## Solution

Implements both directions manually rather than using `bin()`/`int(x, 2)`: repeated bit extraction for encoding, and Horner's method for decoding. Accepts signs, spaces and underscores, and rejects any non-binary digit.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --to-binary 255
python3 main.py --to-decimal 11111111
python3 main.py --demo
```

## Example

```text
decimal    255 -> binary 11111111
decimal   1024 -> binary 10000000000
decimal    -42 -> binary -101010
binary         1010 -> decimal 10
binary   -101010 -> decimal -42
```
