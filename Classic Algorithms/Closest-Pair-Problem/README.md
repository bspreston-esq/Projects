# Closest pair problem

**Category:** Classic Algorithms

## Problem

The closest pair of points problem or closest pair problem is a problem of computational geometry: given n points in metric space, find a pair of points with the smallest distance between them.

## Solution

Implements both a brute-force O(n^2) reference and the classic O(n log n) divide-and-conquer algorithm: sort by x, recurse on halves, then scan a y-sorted strip within the current best distance. The demo cross-checks that both methods agree.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --points 2000
python3 main.py --demo
```

## Example

```text
8 sample points -> (29.98, 8.99) and (47.29, 35.34), distance 31.5325
800 points: brute 1.426786 in 34.9 ms, divide-and-conquer 1.426786 in 0.9 ms, match=True
```
