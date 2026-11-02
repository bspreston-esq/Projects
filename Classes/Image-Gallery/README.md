# Image Gallery

**Category:** Classes

## Problem

Create an image abstract class and then a class that inherits from it for each image type. Put them in a program which displays them in a gallery style format for viewing.

## Solution

`Image` is an ABC with metadata and thumbnail behavior; `PngImage`, `JpgImage` and `GifImage` subclass it. `Gallery` indexes a directory, prints each image's format/size/mode, and renders a self-contained HTML grid with base64 JPEG thumbnails (no external files needed). Requires Pillow.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --dir ./photos --output gallery.html
python3 main.py --demo
```

## Example

```text
indexed 3 images
PNG    sunset.png                320x240  RGB
JPEG   ocean.jpg                 320x240  RGB
GIF    forest.gif                320x240  RGB
html written: 14522 bytes, embedded thumbnails: 3
```
