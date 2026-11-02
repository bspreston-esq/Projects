# Code Snippet Manager

**Category:** Files

## Problem

Another utility program that allows coders to put in functions, classes or other tidbits to save for use later. Organized by the type of snippet or language the coder can quickly look up code. Optional: For extra practice try adding syntax highlighting based on the language.

## Solution

SQLite store for snippets with title, language, comma-separated tags and the code body. Search matches title, code or tags and can be narrowed by language and tag; `--color` applies lightweight ANSI keyword/string/comment highlighting for Python, SQL and JavaScript.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --add "Read a file" python "files,io" "print(open('x').read())"
python3 main.py --search file --language python
python3 main.py --show 1 --color
python3 main.py --demo
```

## Example

```text
stored: 3
python snippets: ['Read a file']
tagged reporting: ['Top customers']
#2 Top customers [sql] tags=sqlite,reporting
SELECT name, SUM(total) AS spend
FROM orders
GROUP BY name
ORDER BY spend DESC;
```
