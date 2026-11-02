# SQL Query Analyzer

**Category:** Databases

## Problem

A utility application which a user can enter a query and have it run against a local database and look for ways to make it more efficient.

## Solution

Runs `EXPLAIN QUERY PLAN` alongside the query, times both, and flags full-table scans. For each scan it extracts predicate columns (resolving table aliases) and proposes a concrete `CREATE INDEX` statement. Works against any SQLite file or the built-in sample schema.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --db shop.db --query "SELECT * FROM orders WHERE customer_id = 1"
python3 main.py --demo
```

## Example

```text
query: SELECT * FROM orders
  rows=5 time=0.01 ms
  plan: SCAN orders
  suggestion: -- consider an index on orders for this predicate
query: SELECT * FROM orders WHERE customer_id = 1
  rows=2 time=0.02 ms
  plan: SEARCH orders USING INDEX idx_orders_customer (customer_id=?)
query: SELECT c.name, SUM(o.total) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name
  rows=3 time=0.03 ms
  plan: SCAN o
  plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
  plan: USE TEMP B-TREE FOR GROUP BY
  suggestion: CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```
