# Reverse a String

**Category:** Text

## Problem

Enter a string and the program will reverse it and print it out.

## Solution

Ships two implementations: Python's slice idiom `text[::-1]` and an explicit index-walking loop, cross-checked in demo mode. Both handle Unicode code points.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py "hello world"
python3 main.py --demo
```

## Example

```text
'hello' -> 'olleh'
           'racecar' -> 'racecar'
      'A man, a plan!' -> '!nalp a ,nam A'
            'éclair' -> 'rialcé'
                '' -> ''
Both implementations agree on every sample.
```
