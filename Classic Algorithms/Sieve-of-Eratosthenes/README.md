# Sieve of Eratosthenes

**Category:** Classic Algorithms

## Problem

The sieve of Eratosthenes is one of the most efficient ways to find all of the smaller primes (below 10 million or so).

## Solution

Allocates a bytearray of flags, then for every prime up to sqrt(limit) clears its multiples starting at p^2 using extended-slice assignment, which pushes the inner loop into C. Memory is O(n) bytes and time is O(n log log n).

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 1000000
python3 main.py --demo
```

## Example

```text
up to        10:       4 primes, largest       7,    0.0 ms
up to       100:      25 primes, largest      97,    0.0 ms
up to 1,000,000:  78,498 primes, largest 999,983,   23.5 ms
```
