# Complex Number Algebra

**Category:** Numbers

## Problem

Show addition, multiplication, negation, and inversion of complex numbers in separate functions. (Subtraction and division operations can be made with pairs of these operations.) Print the results for each operation tested.

## Solution

An immutable `Complex` dataclass implements the four required primitives: `__add__`, `__mul__`, unary `__neg__` and `inverse()` (conjugate over squared modulus). Subtraction and division are derived as `a + (-b)` and `a * (1/b)` respectively, exactly as the problem suggests.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py            # enter two complex numbers as "real imag"
python3 main.py --demo
```

## Example

```text
a = 3 + 4i, b = 1 - 2i
a + b      = 4 + 2i
a * b      = 11 - 2i
-a         = -3 - 4i
1 / a      = 0.12 - 0.16i
a - b      = 2 + 6i   (derived: a + (-b))
a / b      = -1 + 2i   (derived: a * (1/b))
|a|        = 5
```
