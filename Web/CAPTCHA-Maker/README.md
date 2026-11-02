# CAPTCHA Maker

**Category:** Web

## Problem

Ever see those images with letters a numbers when you signup for a service and then asks you to enter what you see? It keeps web bots from automatically signing up and spamming. Try creating one yourself for online forms.

## Solution

Generates a 6-character code from an unambiguous alphabet and renders it as SVG with per-character rotation, vertical jitter and six noise lines, so text extraction is not trivial. Verification uses `hmac.compare_digest` and accepts case-insensitive answers.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --output captcha.svg
python3 main.py --verify ABC123
python3 main.py --demo
```

## Example

```text
captcha G5WJQU: 1561 bytes, valid svg: True
  verify correct: True, wrong: False
```
