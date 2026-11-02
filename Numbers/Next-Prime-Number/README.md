# Next Prime Number

**Category:** Numbers

## Problem

Have the program find prime numbers until the user chooses to stop asking for the next one.

## Solution

A small `PrimeFinder` class keeps the search cursor and returns the next prime on each call, testing candidates with trial division by 2 and odd numbers up to the square root.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py           # interactive: Enter for next prime, q to quit
python3 main.py --start 1000 --count 8 --demo
```

## Example

```text
First 5 primes after 1000:
1009 1013 1019 1021 1031
```
