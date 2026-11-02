# Count Vowels

**Category:** Text

## Problem

Enter a string and the program counts the number of vowels in the text. For added complexity have it report a sum of each vowel found.

## Solution

Lower-cases the input and counts a, e, i, o and u with a `Counter`, reporting each vowel individually plus the total. `--y` optionally treats y as a vowel, and `--file` reads from disk instead of the argument.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py "The quick brown fox"
python3 main.py --file essay.txt --y
python3 main.py --demo
```

## Example

```text
text: The quick brown fox jumps over the lazy dog.
counts: a=1, e=3, i=1, o=4, u=2, y=1
total vowels: 12
```
