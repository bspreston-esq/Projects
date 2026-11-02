# Quote Tracker (market symbols etc)

**Category:** Text

## Problem

A program which can go out and check the current value of stocks for a list of symbols entered by the user. The user can set how often the stocks are checked. For CLI, show whether the stock has moved up or down. Optional: If GUI, the program can show green up and red down arrows to show which direction the stock value has moved.

## Solution

Downloads latest quotes as CSV from Stooq (no API key), tracks the previous price per symbol between checks, and prints the percentage move with an up/down arrow. `--interval` polls continuously; the demo runs two simulated checks offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --symbols AAPL,MSFT,GOOG
python3 main.py --symbols AAPL --interval 60
python3 main.py --demo
```

## Example

```text
check 1:
AAPL       190.00  -> +0.00%
MSFT       410.50  -> +0.00%
check 2:
AAPL       192.40  ^ +1.26%
MSFT       407.10  v -0.83%
```
