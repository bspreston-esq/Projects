# GIF Creator

**Category:** Graphics and Multimedia

## Problem

A program that puts together multiple images (PNGs, JPGs, TIFFs) to make a smooth GIF that can be exported. Optional: Make the program convert small video files to GIFs as well.

## Solution

Loads each frame with Pillow, normalizes them to RGB, centers them on a common canvas, and saves an optimized animated GIF with configurable per-frame duration and loop count. Frame order is the argument order.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py frame_*.png --output animation.gif --duration 120
python3 main.py --demo
```

## Example

```text
gif: 320x240, frames=12, duration=80 ms, loop=0
bytes: 4,866
```
