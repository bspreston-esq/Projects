# Product Inventory Project

**Category:** Classes

## Problem

Create an application which manages an inventory of products. Create a product class which has a price, id, and quantity on hand. Then create an inventory class which keeps track of various products and can sum up the inventory value.

## Solution

`Product` is a validated dataclass with an id, name, price and quantity; `Inventory` owns a product dictionary and supports adding, removing, adjusting stock, computing total value and reporting low-stock items. The demo exercises every operation.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py            # interactive command loop
python3 main.py --demo
```

## Example

```text
P001   Mechanical keyboard    $   89.99 x  10 = $    899.90
P002   USB-C cable            $   12.50 x  40 = $    500.00
P003   27-inch monitor        $  249.00 x   3 = $    747.00
TOTAL                                      $    2,146.90
low stock: 27-inch monitor (3)
total inventory value: $2,146.90
```
