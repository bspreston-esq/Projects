# Happy Numbers

**Category:** Numbers

## Problem

A happy number is defined by the following process. Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers, while those that do not end in 1 are unhappy numbers. Display an example of your output here. Find first 8 happy numbers.

## Solution

Repeatedly sums squared digits while recording visited values in a set, which terminates on either 1 or a repeat (the unhappy cycle). Unhappy numbers necessarily enter the 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 cycle.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 19
python3 main.py --count 8
python3 main.py --demo
```

## Example

```text
First 8 happy numbers: [1, 7, 10, 13, 19, 23, 28, 31]
  7: 7 -> 49 -> 97 -> 130 -> 10 -> 1 (happy)
 19: 19 -> 82 -> 68 -> 100 -> 1 (happy)
 20: 20 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 (unhappy)
 97: 97 -> 130 -> 10 -> 1 (happy)
```
