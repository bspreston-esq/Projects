# Fibonacci Sequence

**Category:** Numbers

## Problem

Enter a number and have the program generate the Fibonacci sequence to that number or to the Nth number.

## Solution

A pair of generators produce either the first N terms or every term up to a maximum value, using O(1) memory per step.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 10         # first 10 terms
python3 main.py --max 100  # terms <= 100
python3 main.py --demo
```

## Example

```text
First 10 terms: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
Terms <= 100:   [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```
