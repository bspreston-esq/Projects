# Sort Excel/CSV File Utility

**Category:** Files

## Problem

Reads a file of records, sorts them, and then writes them back to the file. Allow the user to choose various sort style and sorting based on a particular field.

## Solution

Parses the CSV (handling BOM and quoted fields), resolves the sort column by header name or zero-based index, and sorts either numerically or case-insensitively. Writes back in place or to a new file, preserving the header.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --input sales.csv --field revenue --numeric --reverse
python3 main.py --input sales.csv --field name --output sorted.csv
python3 main.py --demo
```

## Example

```text
name, region, units, revenue
Grace, US, 40, 3200.0
Katherine, APAC, 25, 2750.75
Ada, EU, 12, 1440.5
Alan, EU, 7, 980.25
sorted 4 rows by revenue (descending)
```
