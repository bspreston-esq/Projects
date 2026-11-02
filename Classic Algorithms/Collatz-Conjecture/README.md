# Collatz Conjecture

**Category:** Classic Algorithms

## Problem

Start with a number n > 1. Find the number of steps it takes to reach one using the following process: If n is even, divide it by 2. If n is odd, multiply it by 3 and add 1.

## Solution

Applies the two Collatz rules until the value reaches 1, counting steps with constant memory; a separate sequence mode records every term. `--limit` scans all starting values below a bound for the longest chain.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 27
python3 main.py --limit 10000
python3 main.py --demo
```

## Example

```text
27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94 -> ... -> 4 -> 2 -> 1
27 takes 111 steps
Longest chain below 10,000: start 6171 with 261 steps
```
