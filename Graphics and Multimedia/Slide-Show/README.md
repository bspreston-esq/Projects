# Slide Show

**Category:** Graphics and Multimedia

## Problem

Make an application that shows various pictures in a slide show format. Optional: Try adding various effects like fade in/out, star wipe and window blinds transitions.

## Solution

Renders a self-contained HTML slideshow: each image is embedded as a base64 JPEG and a CSS keyframe animation cross-fades through the deck with per-slide delays. `--gui` opens a Tkinter viewer instead, cycling full-window images every four seconds. Requires Pillow.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py photo1.jpg photo2.jpg --output show.html --duration 5
python3 main.py photo*.jpg --gui
python3 main.py --demo
```

## Example

```text
slides: 4, bytes: 37,288
embedded images: 4
```
