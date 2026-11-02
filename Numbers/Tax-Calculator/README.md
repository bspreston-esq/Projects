# Tax Calculator

**Category:** Numbers

## Problem

Asks the user to enter a cost and either a country or state tax. It then returns the tax plus the total cost with tax.

## Solution

Built-in tables cover all 50 US state base sales-tax rates and 13 common VAT countries; anything else can be given directly as a percentage. Tax is computed as `cost * rate / 100` and the total is printed alongside it.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --cost 49.99 --tax TX
python3 main.py --cost 80 --tax 8.25%
python3 main.py --demo
```

## Example

```text
$ 100.00 + 7.25% (US state CA): tax $7.25, total $107.25
$  49.99 + 6.25% (US state TX): tax $3.12, total $53.11
$ 250.00 + 19% (Germany): tax $47.50, total $297.50
$  80.00 + 8.25% (custom rate): tax $6.60, total $86.60
```
