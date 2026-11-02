# Mortgage Calculator

**Category:** Numbers

## Problem

Calculate the monthly payments of a fixed term mortgage over given Nth terms at a given interest rate. Also figure out how long it will take the user to pay back the loan. For added complexity, add an option for users to select the compounding interval (Monthly, Weekly, Daily, Continually).

## Solution

Standard amortization formula `P*i/(1-(1+i)^-n)` with the periodic rate derived from the chosen compounding interval; continuous compounding uses `e^(r/12)-1` for monthly payments. An optional extra payment simulates the balance period by period to report the true payoff time.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --principal 300000 --rate 6.5 --years 30 --interval monthly
python3 main.py --principal 300000 --rate 6.5 --years 30 --extra 250
python3 main.py --demo
```

## Example

```text
Loan $300,000 at 6.5% over 30 years
  monthly    payment   1,896.20 x 360   =   682,633.47 total
  weekly     payment     437.29 x 1560  =   682,173.92 total
  daily      payment      62.29 x 10950 =   682,055.69 total
  continuous payment   1,899.68 x 360   =   683,886.57 total
With $250 extra monthly: paid off in 262 months (21.8 years)
```
