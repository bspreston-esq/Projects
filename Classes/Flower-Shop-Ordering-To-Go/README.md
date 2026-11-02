# Flower Shop Ordering To Go

**Category:** Classes

## Problem

Create a flower shop application which deals in flower objects and use those flower objects in a bouquet object which can then be sold. Keep track of the number of objects and when you may need to order more.

## Solution

Flowers carry price, stock and a restock threshold; bouquets declare a composition that is priced from the catalogue plus labour. Selling decrements stock atomically (validating every line first), records an order, and the shop reports revenue and which flowers need reordering.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
order for Ada: Spring Mix = $33.20
restock needed: ['tulip']
after restock, tulips: 20
revenue: $33.20
```
