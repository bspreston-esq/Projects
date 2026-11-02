# PDF Generator

**Category:** Files

## Problem

An application which can read in a text file, html file or some other file and generates a PDF file out of it. Great for a web based service where the user uploads the file and the program returns a PDF of the file. Optional: Deploy on GAE or Heroku if possible.

## Solution

A from-scratch PDF writer: wraps text to 85 characters, paginates at 56 lines per A4 page, emits Helvetica content streams, and builds a correct object table with xref offsets and trailer. HTML input is reduced to text by stripping tags, scripts and styles.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --input notes.txt --output notes.pdf
python3 main.py --input page.html --title "Web Page"
python3 main.py --demo
```

## Example

```text
wrote output.pdf: 9,684 bytes
header: %PDF-1.4
pages: 2 | xref present: True | eof: True
```
