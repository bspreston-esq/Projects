# Sorting

**Category:** Classic Algorithms

## Problem

Implement two types of sorting algorithms: Merge sort and bubble sort.

## Solution

Merge sort is a stable top-down divide-and-conquer implementation in O(n log n). Bubble sort uses an early-exit flag when a pass performs no swaps, which makes already-sorted input O(n) while the worst case stays O(n^2).

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 5,2,9,1,5,6
python3 main.py --demo
```

## Example

```text
input:       [5, 2, 9, 1, 5, 6, -3, 0]
merge sort:  [-3, 0, 1, 2, 5, 5, 6, 9]
bubble sort: [-3, 0, 1, 2, 5, 5, 6, 9]
2000 random ints: merge 1.81 ms, bubble 109.09 ms
```
