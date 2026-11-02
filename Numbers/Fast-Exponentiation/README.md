# Fast Exponentiation

**Category:** Numbers

## Problem

Ask the user to enter 2 integers a and b and output a^b (i.e. pow(a,b)) in O(lg n) time complexity.

## Solution

Binary exponentiation ("exponentiation by squaring"): each step halves the exponent, multiplying the accumulator only when the current bit is set. Runs in O(log b) multiplications; supports negative exponents (returning a float) and an optional modulus for modular exponentiation.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 2 100
python3 main.py 2 1000000 --mod 1000000007
python3 main.py --demo
```

## Example

```text
2^10 = 1024 (matches **: True)
3^20 = 3.48678e+09 (matches **: True)
7^0 = 1 (matches **: True)
2^100 = 1.26765e+30 (matches **: True)
5^-2 = 0.04 (matches **: True)
2^1000000 mod 1000000007 = 235042059
```
