# Text Editor

**Category:** Text

## Problem

Notepad style application that can open, edit, and save text documents. Optional: Add syntax highlighting and other features.

## Solution

Two front ends share one `Document` model: `--gui` opens a Tkinter window with Open/Save-as menus (requires Tk), while the default mode is a line editor with view/append/insert/delete/replace/save commands. The model itself is headless and fully testable, as the demo shows.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --gui
python3 main.py draft.txt
python3 main.py --demo
```

## Example

```text
1 | First final line
   2 | Inserted in the middle
saved: draft.txt (40 bytes)
```
