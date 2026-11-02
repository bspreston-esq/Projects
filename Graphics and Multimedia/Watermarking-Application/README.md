# Watermarking Application

**Category:** Graphics and Multimedia

## Problem

Have some pictures you want copyright protected? Add your own logo or text lightly across the background so that no one can simply steal your graphics off your site. Make a program that will add this watermark to the picture. Optional: Use threading to process multiple images simultaneously.

## Solution

Builds a rotated text tile, repeats it across a transparent RGBA layer at the requested opacity, and alpha-composites it onto the image. Batch mode processes all images through a thread pool (Pillow releases the GIL during image work).

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py photos/*.jpg --text "(c) Kambiz" --opacity 110 --output watermarked
python3 main.py --demo
```

## Example

```text
watermarked 1200x800 -> 1200x800
changed pixels: 146,053 of 960,000
output bytes: 42,871
```
