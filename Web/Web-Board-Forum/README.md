# Web Board (Forum)

**Category:** Web

## Problem

Create a forum for you and your buddies to post, administer and share thoughts and ideas.

## Solution

SQLite tables for topics and replies behind a stdlib HTTP server. The index lists threads with reply counts, `/topic/<id>` renders the thread and a reply form, and `POST /new` / `POST /topic/<id>/reply` insert records and redirect. All user text is HTML-escaped.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --port 8002 --db forum.db
python3 main.py --demo
```

## Example

```text
topic title present: True
reply present: True
listing shows 1 reply: True
```
