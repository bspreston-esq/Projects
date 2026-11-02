# Number Names

**Category:** Numbers

## Problem

Show how to spell out a number in English. You can use a preexisting implementation or roll your own, but you should support inputs up to at least one million (or the maximum value of your language's default bounded integer type, if that's less). Optional: Support for inputs other than positive integers (like zero, negative integers, and floating-point numbers).

## Solution

Decomposes the integer part into three-digit groups against a scale table (thousand through quadrillion), spells each group with the standard British "and" for hundreds, then spells the fractional digits individually after "point". Handles zero, negatives and floats.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 1234567
python3 main.py --demo
```

## Example

```text
0 = zero
          21 = twenty one
         101 = one hundred and one
        1000 = one thousand
     1234567 = one million two hundred and thirty four thousand five hundred and sixty seven
  1000000001 = one billion one
         -42 = minus forty two
        3.14 = three point one four
```
