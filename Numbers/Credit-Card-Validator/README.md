# Credit Card Validator

**Category:** Numbers

## Problem

Takes in a credit card number from a common credit card vendor (Visa, MasterCard, American Express, Discoverer) and validates it to make sure that it is a valid number (look into how credit cards use a checksum).

## Solution

Strips spaces and dashes, checks length and the issuer identification number (Visa, Mastercard, Amex, Discover, JCB), then runs the Luhn mod-10 checksum. The output never echoes more than the last four digits.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 4111-1111-1111-1111
python3 main.py --demo
```

## Example

```text
************1111  VALID   Visa             valid
   ************1112  INVALID Visa             failed the Luhn checksum
    ***********0005  VALID   American Express valid
   ************4444  VALID   Mastercard       valid
   ************1117  VALID   Discover         valid
```
