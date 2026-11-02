# Fizz Buzz

**Category:** Text

## Problem

Write a program that prints the numbers from 1 to 100. But for multiples of three print "Fizz" instead of the number and for the multiples of five print "Buzz". For numbers which are multiples of both three and five print "FizzBuzz".

## Solution

Iterates once over the range and checks divisibility by 15 first, then 3, then 5. A generator keeps it reusable and `--limit` allows other ranges.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py            # 1..100
python3 main.py --limit 15
python3 main.py --demo
```

## Example

```text
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```
