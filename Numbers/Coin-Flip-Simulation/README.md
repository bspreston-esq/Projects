# Coin Flip Simulation

**Category:** Numbers

## Problem

Write some code that simulates flipping a single coin however many times the user decides. The code should record the outcomes and count the number of tails and heads.

## Solution

Draws fair independent tosses with `random.choice`, tallies heads and tails, and also tracks the longest run of identical outcomes. `--seed` makes any run reproducible.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --flips 1000
python3 main.py --flips 1000 --seed 42
python3 main.py --demo
```

## Example

```text
10 flips: heads      8 (80.00%), tails      2 (20.00%), longest streak 5
   100 flips: heads     56 (56.00%), tails     44 (44.00%), longest streak 7
 10000 flips: heads   4984 (49.84%), tails   5016 (50.16%), longest streak 12
```
