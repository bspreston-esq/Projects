# Find PI to the Nth Digit

**Category:** Numbers

## Problem

Enter a number and have the program generate PI up to that many decimal places. Keep a limit to how far the program will go.

## Solution

Uses the Chudnovsky series with Python's `decimal` module at `digits + 20` guard digits, then truncates to the requested precision. Output is capped at 1000 decimal places.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py            # prompts for a digit count
python3 main.py 50         # non-interactive
python3 main.py --demo     # fixed sample output
```

## Example

```text
pi to   0 digits: 3
pi to   2 digits: 3.14
pi to  10 digits: 3.1415926535
pi to  50 digits: 3.14159265358979323846264338327950288419716939937510
```
