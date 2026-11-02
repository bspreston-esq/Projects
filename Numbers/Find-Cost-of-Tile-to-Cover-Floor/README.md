# Find Cost of Tile to Cover W x H Floor

**Category:** Numbers

## Problem

Calculate the total cost of tile it would take to cover a floor plan of width and height, using a cost entered by the user.

## Solution

Multiplies width by height for the area, optionally adds a waste percentage for cuts and breakage, then multiplies by the per-square-unit price. All inputs are validated as positive numbers.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --width 12 --height 10 --cost 4.25 --waste 10
python3 main.py --demo
```

## Example

```text
12 x 10 @ 4.25/sq unit, 10% waste: 132.00 sq units -> $561.00
5.5 x 4 @ 9.99/sq unit, 5% waste: 23.10 sq units -> $230.77
20 x 20 @ 2.00/sq unit, 0% waste: 400.00 sq units -> $800.00
```
