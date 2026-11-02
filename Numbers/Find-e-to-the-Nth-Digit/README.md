# Find e to the Nth Digit

**Category:** Numbers

## Problem

Just like the previous problem, but with e instead of PI. Enter a number and have the program generate e up to that many decimal places. Keep a limit to how far the program will go.

## Solution

Sums the Taylor series e = 1 + 1/1! + 1/2! + ... in `decimal` at `digits + 20` precision, stopping once a term falls below the guard-digit threshold, then truncates. Capped at 1000 decimal places.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py            # prompts for a digit count
python3 main.py 50         # non-interactive
python3 main.py --demo     # fixed sample output
```

## Example

```text
e to   0 digits: 2
e to   2 digits: 2.71
e to  10 digits: 2.7182818284
e to  50 digits: 2.71828182845904523536028747135266249775724709369995
```
