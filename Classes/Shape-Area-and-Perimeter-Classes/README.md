# Shape Area and Perimeter Classes

**Category:** Classes

## Problem

Create an abstract class called Shape and then inherit from it other shapes like diamond, rectangle, circle, triangle etc. Then have each class override the area and perimeter functionality to handle each shape type.

## Solution

`Shape` declares abstract `area()` and `perimeter()` methods plus a shared formatted `__str__`. Circle, Rectangle/Square, Triangle (Heron's formula, triangle-inequality validated) and Diamond (rhombus from diagonals) each override both methods.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
circle     area=    28.274  perimeter=    18.850
rectangle  area=    24.000  perimeter=    20.000
square     area=    25.000  perimeter=    20.000
triangle   area=     6.000  perimeter=    12.000
diamond    area=    24.000  perimeter=    20.000
largest area: circle
```
