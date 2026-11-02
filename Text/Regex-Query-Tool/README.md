# Regex Query Tool

**Category:** Text

## Problem

A tool that allows the user to enter a text string and then in a separate control enter a regex pattern. It will run the regular expression against the source text and return any matches or flag errors in the regular expression.

## Solution

Compiles the pattern (optionally case-insensitive), runs `finditer` over the text, and prints each match with its span, matched value and capture groups. Invalid patterns are reported as errors rather than tracebacks; `--group` selects a single capture group.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --pattern "\b\w+@\w+\.\w+\b" --text "mail ada@example.com"
python3 main.py --pattern "(\w+)@(\w+)" --file contacts.txt --group 1
python3 main.py --demo
```

## Example

```text
pattern: \b\w+@\w+\.\w+\b
  [ 8:23] 'ada@example.com' groups=()
  [27:41] 'grace@navy.mil' groups=()
  2 match(es)
pattern: (\w+)@(\w+)
  [ 8:19] 'ada@example' groups=('ada', 'example')
  [27:37] 'grace@navy' groups=('grace', 'navy')
  2 match(es)
pattern: ([a-z
  error: invalid regular expression: unterminated character set at position 1
```
