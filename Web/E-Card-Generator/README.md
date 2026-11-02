# E-Card Generator

**Category:** Web

## Problem

Make a site that allows people to generate their own little e-cards and send them to other people. Do not use Flash. Use a picture library and perhaps insightful mottos or quotes.

## Solution

Generates a standalone HTML card from one of three templates (birthday, holiday, thank you), with per-template gradients, escaped user text, an optional image, and a signature line. No JavaScript or Flash; the output file works offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --template birthday --name Ada --from Grace
python3 main.py --template thankyou --name Alan --message "Thanks!" --output card.html
python3 main.py --demo
```

## Example

```text
ecard_birthday.html: 1034 bytes, title contains 'Ada': True
ecard_thankyou.html: 1008 bytes, title contains 'Alan': True
```
