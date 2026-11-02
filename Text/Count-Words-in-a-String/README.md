# Count Words in a String

**Category:** Text

## Problem

Counts the number of individual words in a string. For added complexity read these strings in from a text file and generate a summary.

## Solution

Extracts words with a regex that keeps internal apostrophes, then reports character, line, word and unique-word counts plus the five most frequent words (case-insensitive). Reads from an argument, an interactive prompt, or `--file`.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py "the quick brown fox"
python3 main.py --file book.txt
python3 main.py --demo
```

## Example

```text
characters: 109, lines: 2, words: 24, unique: 10
top words: it x4, was x4, the x4, of x4, times x2
```
