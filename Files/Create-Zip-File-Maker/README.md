# Create Zip File Maker

**Category:** Files

## Problem

The user enters various files from different directories and the program zips them up into a zip file. Optional: Apply actual compression to the files. Start with Huffman Algorithm.

## Solution

Uses `zipfile` with DEFLATE compression by default (`--store` disables it). Files keep their basename at the archive root; directories are walked recursively and preserved under their own folder name. The demo verifies the archive with `testzip()`.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --output bundle.zip ./docs ./photos
python3 main.py --output bundle.zip --store notes.txt
python3 main.py --demo
```

## Example

```text
added 3 files, archive 385 bytes
  docs/notes.md                   8 bytes -> 10 stored
  docs/readme.txt                14 bytes -> 16 stored
  photos/pixel.txt               19 bytes -> 21 stored
test: True
```
