# Remote SQL Tool

**Category:** Databases

## Problem

A utility that can execute queries on remote servers from your local computer across the Internet. It should take in a remote host, user name and password, run the query and return the results.

## Solution

A token-authenticated JSON-over-TCP protocol: the server holds a SQLite file and executes one statement per connection, returning columns/rows for SELECTs or a row count for writes. The client can be run from anywhere the port is reachable. Bind to localhost or a private network and use a strong SQL_TOKEN.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
SQL_TOKEN=secret python3 main.py serve --db shop.db --port 9000
SQL_TOKEN=secret python3 main.py query --host 127.0.0.1 --port 9000 --sql "SELECT * FROM items"
python3 main.py --demo
```

## Example

```text
columns: ['name', 'qty']
  ['nut', 75]
  ['bolt', 40]
  ['washer', 12]
bad token: unauthorized
after update: [[76]]
```
