# Company Manager

**Category:** Classes

## Problem

Create an hierarchy of classes - abstract class Employee and subclasses HourlyEmployee, SalariedEmployee, Manager and Executive. Every one's pay is calculated differently, research a bit about it. After you've established an employee hierarchy, create a Company class that allows you to manage the employees. You should be able to hire, fire and raise employees.

## Solution

`Employee` is an ABC requiring `pay()` and `_apply_raise()`; hourly staff get time-and-a-half beyond 80 hours per biweekly period, salaried staff earn annual/26, managers add a prorated bonus, and executives add a stock-option component. `Company` tracks the roster and exposes hire, fire, raise and payroll.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
Initech payroll (4 employees)
E001  Ada                HourlyEmployee   $  2,300.00
E002  Grace              SalariedEmployee $  4,000.00
E003  Alan               Manager          $  5,461.54
E004  Katherine          Executive        $ 10,769.23
TOTAL                                    $ 22,530.77
after 5% raise to E002 and firing E001: payroll $20,430.77
```
