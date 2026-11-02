#!/usr/bin/env python3
"""Sort a CSV file by any column, numerically or lexically, and write it back."""
import argparse
import csv
import os
import tempfile

def sort_csv(source: str, destination: str, field: str, numeric=False,
             reverse=False, has_header=True) -> int:
    with open(source, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        raise ValueError("file is empty")
    header = rows[0] if has_header else None
    data = rows[1:] if has_header else rows
    if header and field not in header:
        raise ValueError(f"unknown field '{field}'; available: {', '.join(header)}")
    index = header.index(field) if header else int(field)
    try:
        key = (lambda row: float(row[index])) if numeric else (lambda row: row[index].lower())
        data.sort(key=key, reverse=reverse)
    except (IndexError, ValueError) as exc:
        raise ValueError(f"cannot sort by '{field}': {exc}")
    with open(destination, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if header:
            writer.writerow(header)
        writer.writerows(data)
    return len(data)

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, "sales.csv")
        destination = os.path.join(tmp, "sorted.csv")
        with open(source, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["name", "region", "units", "revenue"])
            writer.writerows([["Ada", "EU", 12, 1440.50], ["Grace", "US", 40, 3200.00],
                              ["Alan", "EU", 7, 980.25], ["Katherine", "APAC", 25, 2750.75]])
        count = sort_csv(source, destination, "revenue", numeric=True, reverse=True)
        with open(destination, newline="") as fh:
            for row in csv.reader(fh):
                print(", ".join(row))
        print(f"sorted {count} rows by revenue (descending)")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--field", help="column name or zero-based index")
    parser.add_argument("--numeric", action="store_true")
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--no-header", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    if not args.input or not args.field:
        raise SystemExit("--input and --field are required (or use --demo)")
    destination = args.output or args.input
    try:
        count = sort_csv(args.input, destination, args.field, args.numeric, args.reverse, not args.no_header)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}")
    print(f"sorted {count} rows by {args.field} -> {destination}")

if __name__ == "__main__":
    main()
