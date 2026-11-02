#!/usr/bin/env python3
"""Run a query against SQLite, show its plan, timing and index suggestions."""
import argparse
import re
import sqlite3
import time

SAMPLE = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total REAL);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
"""
SAMPLE_DATA = """
INSERT INTO customers VALUES (1,'Ada','UK'),(2,'Grace','US'),(3,'Alan','UK');
INSERT INTO orders VALUES (1,1,'2026-01-04',120.0),(2,1,'2026-02-11',80.5),
  (3,2,'2026-02-14',220.0),(4,3,'2026-03-02',15.0),(5,2,'2026-03-09',310.0);
INSERT INTO products VALUES (1,'Keyboard','input',89.99),(2,'Monitor','display',249.0),(3,'Cable','input',12.5);
"""

def build_sample() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(SAMPLE + SAMPLE_DATA)
    return connection

def analyze(connection, query: str):
    """Return (plan_lines, row_count, elapsed_ms, suggestions)."""
    start = time.perf_counter()
    try:
        plan = connection.execute("EXPLAIN QUERY PLAN " + query).fetchall()
        cursor = connection.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as exc:
        raise ValueError(str(exc)) from exc
    elapsed = (time.perf_counter() - start) * 1000
    suggestions = []
    for entry in plan:
        detail = entry[-1]
        match = re.search(r"SCAN (?:TABLE )?(\w+)", detail, re.IGNORECASE)
        if match:
            table = match.group(1)
            aliases = {}
            for clause in re.finditer(r"(?:FROM|JOIN)\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?", query, re.IGNORECASE):
                real, alias = clause.group(1), clause.group(2)
                aliases[real] = real
                if alias:
                    aliases[alias] = real
            table = aliases.get(table, table)
            reserved = {"select", "from", "where", "join", "on", "and", "or", "group", "order",
                        "by", "having", "limit", "as", "inner", "left", "right", "outer", "using"}
            columns = re.findall(r"(\w+)\s*(?:>=|<=|=|>|<|\bLIKE\b|\bIN\b|\bBETWEEN\b)", query, re.IGNORECASE)
            columns = [column for column in dict.fromkeys(columns) if column.lower() not in reserved]
            if columns:
                suggestions.append(f"CREATE INDEX idx_{table}_{'_'.join(columns)} ON {table}({', '.join(columns)});")
            else:
                suggestions.append(f"-- consider an index on {table} for this predicate")
    return [entry[-1] for entry in plan], len(rows), elapsed, suggestions

SAMPLE_QUERIES = [
    "SELECT * FROM orders",
    "SELECT * FROM orders WHERE customer_id = 1",
    "SELECT c.name, SUM(o.total) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name",
]

def demo() -> None:
    connection = build_sample()
    for query in SAMPLE_QUERIES:
        plan, count, elapsed, suggestions = analyze(connection, query)
        print(f"query: {query}")
        print(f"  rows={count} time={elapsed:.2f} ms")
        for line in plan:
            print("  plan:", line)
        for suggestion in suggestions:
            print("  suggestion:", suggestion)
    connection.close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", help="SQLite file (omit for the built-in sample)")
    parser.add_argument("--query")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    connection = sqlite3.connect(args.db) if args.db else build_sample()
    query = args.query or input("SQL query: ").strip()
    try:
        plan, count, elapsed, suggestions = analyze(connection, query)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
    print(f"rows: {count}, elapsed: {elapsed:.2f} ms")
    for line in plan:
        print("plan:", line)
    if suggestions:
        print("suggestions:")
        for suggestion in suggestions:
            print(" ", suggestion)
    connection.close()

if __name__ == "__main__":
    main()
