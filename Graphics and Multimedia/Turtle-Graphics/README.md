# Turtle Graphics

**Category:** Graphics and Multimedia

## Problem

This is a common project where you create a floor of 20 x 20 squares. Using various commands you tell a turtle to draw a line on the floor. You have move forward, left or right, lift or drop pen etc. Do a search online for "Turtle Graphics" for more information. Optional: Allow the program to read in the list of commands from a file.

## Solution

A small command interpreter (F, L, R, U, D, HOME, COLOR, REPEAT) drives a turtle on a 20x20 floor. It records line segments for SVG export and rasterizes each stroke into grid cells for an ASCII view, so both the geometry and the floor coverage are visible. Commands can come from a file or a string.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --file drawing.turtle --svg drawing.svg
python3 main.py --commands "REPEAT 4 [ F 5 R 90 ]"
python3 main.py --demo
```

## Example

```text
....................
..........*********.
..........*....*....
..........*....*....
..........******....
....................
position: (18.0, 10.0) heading 0 degrees
svg bytes: 567, segments: 5
```
