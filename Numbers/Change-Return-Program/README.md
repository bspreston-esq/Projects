# Change Return Program

**Category:** Numbers

## Problem

The user enters a cost and then the amount of money given. The program will figure out the change and the number of quarters, dimes, nickels, pennies needed for the change.

## Solution

Converts both amounts to integer cents to avoid floating-point drift, then uses greedy division over US denominations (quarter, dime, nickel, penny), which is optimal for this coin system. Rejects underpayment with the exact shortfall.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --cost 3.75 --paid 5.00
python3 main.py --demo
```

## Example

```text
Cost $3.75, paid $5.00: change $1.25 (5 quarters)
Cost $12.34, paid $20.00: change $7.66 (30 quarters, 1 dime, 1 nickel, 1 penny)
Cost $0.99, paid $1.00: change $0.01 (1 penny)
```
