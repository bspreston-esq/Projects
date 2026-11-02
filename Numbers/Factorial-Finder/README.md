# Factorial Finder

**Category:** Numbers

## Problem

The Factorial of a positive integer, n, is defined as the product of the sequence n, n-1, n-2, ...1 and the factorial of zero, 0, is defined as being 1. Solve this using both loops and recursion.

## Solution

Provides two implementations: an iterative product and a recursive version with a memo dictionary and a raised recursion limit. Negative inputs raise `ValueError`; the demo cross-checks that both methods agree.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 20
python3 main.py --demo
```

## Example

```text
0! = 1
  1! = 1
  5! = 120
 10! = 3628800
 20! = 2432902008176640000
 52! = 806581751709... (68 digits)
Loop and recursive results match for all samples.
```
