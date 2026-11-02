# Bank Account Manager

**Category:** Classes

## Problem

Create a class called Account which will be an abstract class for three other classes called CheckingAccount, SavingsAccount and BusinessAccount. Manage credits and debits from these accounts through an ATM style program.

## Solution

`Account` is an ABC with shared deposit logic and an abstract `withdraw`. Checking allows a $500 overdraft with a $35 fee, Savings enforces a $100 minimum and earns 2% interest, Business charges $2.50 per withdrawal. The `ATM` class opens accounts, transfers funds and prints statements.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
C-1001   CheckingAccount  Ada          $      800.00
S-2001   SavingsAccount   Grace        $    5,000.00
B-3001   BusinessAccount  Initech      $   12,000.00
checking withdraw 900 -> debited $935.00
savings interest -> $100.00
```
